import os
import magic
import hashlib
import MySQLdb
from warnings import filterwarnings
from log import Log

import config

from datetime import datetime
theDate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

class DAO:
    def __init__(self):
	self.db = MySQLdb.connect(host=config.DBHost, 
				    passwd=config.DBPass, 
				    db=config.DBName, 
				    user=config.DBUser)
	
	self.updateDBVersion()

    def createDB(self):
	filterwarnings('ignore', category = MySQLdb.Warning)
	self.runSQLScript("./sql/CreateDB.sql")
	filterwarnings('default', category = MySQLdb.Warning)

    def updateDBVersion(self):
	c=self.db.cursor()
	c.execute("SHOW TABLES")
	if ("file",) not in c.fetchall(): # assume no table
	    Log.echo("INFO", "Creating DB");
	    self.createDB()
	c.close()
	
	version = int(self.getDBVersion())
	for v in (1,2,3,4):
	    if version < v:
		Log.echo("INFO", "Updating DB to version %d" % v);
		self.runSQLScript("./sql/UpdateDBToVersion%d.sql" % v)

    def runSQLScript(self,script):
	c=self.db.cursor()
	try:
	    with open(script, "rt") as f:
		# MySQLdb cursors are missing the 'executescript' method...
		script = f.read()
		for statement in script.split(";"):
		    statement = statement.strip()
		    if statement != "":
			Log.write("SQL", statement)
			c.execute(statement)
		self.db.commit()
	finally:
	    c.close()

    def getDBVersion(self):
	c=self.db.cursor()
	try:
	    filterwarnings('ignore', category = MySQLdb.Warning)
	    c.execute("""SELECT value FROM config WHERE name='version'""")
	    filterwarnings('default', category = MySQLdb.Warning)
	    row = c.fetchone();
	    return row[0]
	except:
	    return 0
	finally:
	    c.close()

    def insertFile(self,file):
	c=self.db.cursor()
	try:
	    c.execute("""INSERT IGNORE
			    INTO file (hash, stime, mimetype, size)
			    VALUES (%s, %s, %s, %s)""",
			    (file.hash, theDate, file.mimetype, file.size))
	    c.execute("""INSERT IGNORE
			    INTO path (basename, dirname)
			    VALUES (%s, %s)""",
			    (file.baseName, file.dirName))
	    # c = self.db.cursor()
	    c.execute("""INSERT IGNORE
			    INTO node (hash, date, owner, mtime, ctime, atime, pid)
			    SELECT %s, %s, %s, 
				    FROM_UNIXTIME(%s), 
				    FROM_UNIXTIME(%s), 
				    FROM_UNIXTIME(%s), path.id
				FROM path
				WHERE basename = %s AND dirname = %s""",
			    (file.hash, theDate, file.owner,
			     file.mtime, file.ctime, file.atime, 
			     file.baseName, file.dirName))
	    self.db.commit()
	finally:
	    c.close()

    def done(self):
	"""Record the index date in the DB. Should be called after
	the last 'insertFile' call."""
	c=self.db.cursor()
	try:
	    c.execute("""INSERT IGNORE INTO session(date) VALUES(%s)""",
			theDate)
	    self.db.commit()
	finally:
	    c.close()

    def exfilter(self, **options):
	if not "status" in options:
	    options["status"] = '?' # default to untagged files
	if not "filename" in options:
	    options["filename"] = ()
	if not "mimetype" in options:
	    options["mimetype"] = ()

	query = """SELECT DISTINCT file.hash,file.mimetype, 
				    path.dirname, path.basename 
		    FROM file 
		    JOIN node USING (hash)
		    INNER JOIN path ON node.pid = path.id
		    WHERE 
		    """
	params = []
	# WHERE clause
	opt = options["mimetype"]
	if opt:
	    params += opt
	    query += "(" + " OR ".join(("mimetype LIKE %s",)*len(opt)) + """) AND
		"""

	opt = options["filename"]
	if opt:
	    params += opt
	    query += "(" + " OR ".join(("basename LIKE %s",)*len(opt)) + """) AND
		"""

	opt = options["status"]
	if opt:
	    params += opt
	    query += "(" + " OR ".join(("status = %s",)*len(opt)) + """) AND
		"""

	query += """1
		"""

	# LIMIT clause
	if "limit" in options:
	    query += """LIMIT %d
		     """ % options["limit"]

	c=self.db.cursor()
	try:
	    c.execute(query, params)
	    while True:
		row = c.fetchone()
		if row:
		    yield row

		else:
		    break
	finally:
	    c.close()

    def mark(self, hash, status):
	c=self.db.cursor()
	try:
	    c.execute("""UPDATE file SET status = %s, stime = %s 
			WHERE hash = %s""",
			(status, theDate, hash))
	    self.db.commit()
	finally:
	    c.close()

    def getInfoByHash(self, hash):
	c=self.db.cursor()
	try:
	    result = {}
	    c.execute("""SELECT hash,size,mimetype,status 
	    			FROM file WHERE hash = %s""", hash)
	    row = c.fetchone()

	    result["hash"] = row[0]
	    result["size"] = row[1]
	    result["mimetype"] = row[2]
	    result["status"] = row[3]

	    c.execute("""SELECT session.date,owner,concat(dirname,basename)
	    		    FROM (SELECT * FROM node 
						JOIN path ON pid=id
					WHERE hash = %s
					ORDER BY owner ASC, date ASC) AS n 
			    RIGHT JOIN session
			    USING(date)""", hash)
	    result["path"] = c.fetchall()
	        

	    return result
	except:
	    return None
	finally:
	    c.close()
    	

