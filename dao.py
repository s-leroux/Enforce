import os
import magic
import hashlib
import MySQLdb

import config

from datetime import datetime
theDate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

class DAO:
    def __init__(self):
	self.db = MySQLdb.connect(host=config.DBHost, 
				    passwd=config.DBPass, 
				    db=config.DBName, 
				    user=config.DBUser)
	
	self.createDB()
	self.updateDBVersion()

    def createDB(self):
	self.runSQLScript("./sql/CreateDB.sql")

    def updateDBVersion(self):
	version = int(self.getDBVersion())
	c=self.db.cursor();
	if version < 1:
	    self.runSQLScript("./sql/UpdateDBToVersion1.sql")

    def runSQLScript(self,script):
	c=self.db.cursor()
	try:
	    with open(script, "rt") as f:
		# MySQLdb cursors are missing the 'executescript' method...
		script = f.read()
		for statement in script.split(";"):
		    statement = statement.strip()
		    if statement != "":
			print "SQL: %s" % statement
			c.execute(statement)
		self.db.commit()
	finally:
	    c.close()

    def getDBVersion(self):
	c=self.db.cursor()
	try:
	    c.execute("""SELECT value FROM config WHERE name='version'""")
	    row = c.fetchone();
	    return row[0]
	finally:
	    c.close()

    def insertFile(self,file):
	c=self.db.cursor()
	try:
	    c.execute("""INSERT IGNORE
			    INTO file (hash, mimetype, size)
			    VALUES (%s, %s, %s)""",
			    (file.hash, file.mimetype, file.size))
	    c.execute("""INSERT IGNORE
			    INTO path (basename, dirname)
			    VALUES (%s, %s)""",
			    (file.baseName, file.dirName))
	    # c = self.db.cursor()
	    c.execute("""INSERT IGNORE
			    INTO node (hash, date, owner, pid)
			    SELECT %s, %s, %s, path.id
				FROM path
				WHERE basename = %s AND dirname = %s""",
			    (file.hash, theDate, file.owner,file.baseName, file.dirName))
	    self.db.commit()
	finally:
	    c.close()

    def exfilter(self, **options):
	if not "status" in options:
	    options["status"] = '?' # default to untagged files

	limit = ""
	if "limit" in options:
	    limit = "LIMIT %d" % options["limit"]

	where = "WHERE 1"
	if "status" in options:
	    where += " AND status='%s'" % options["status"]
	if "mimetype" in options:
	    where += " AND mimetype LIKE '%s'" % options["mimetype"]
	if "filename" in options:
	    where += " AND basename LIKE '%s'" % options["filename"]

	c=self.db.cursor()
	try:
	    print("""SELECT DISTINCT file.hash,file.mimetype, path.dirname, path.basename 
				FROM file JOIN node USING (hash)
					    INNER JOIN path ON node.pid = path.id
				%s
				ORDER BY file.hash
				%s
				""" % (where, limit))
	    c.execute("""SELECT DISTINCT file.hash,file.mimetype, path.dirname, path.basename 
				FROM file JOIN node USING (hash)
					    INNER JOIN path ON node.pid = path.id
				%s
				ORDER BY file.hash
				%s
				""" % (where, limit))
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
	    c.execute("""UPDATE file SET status = %s WHERE hash = %s""",
			(status, hash))
	    self.db.commit()
	finally:
	    c.close()
	
	

