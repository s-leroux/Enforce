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

    def createDB(self):
	c = self.db.cursor()
	c.execute("""CREATE TABLE IF NOT EXISTS file (
				hash CHAR(32) NOT NULL,
				mimetype CHAR(64) NOT NULL,
				size INT(10),
				status ENUM('?', 'X', 'OK') DEFAULT '?',
				PRIMARY KEY(hash),
				INDEX(mimetype)
			    ) ENGINE INNODB""")
	c.execute("""CREATE TABLE IF NOT EXISTS path (
				hash CHAR(32) NOT NULL,
				date DATETIME NOT NULL,
				path VARCHAR(255) NOT NULL,
				owner CHAR(20) NOT NULL,
				PRIMARY KEY(date, path),
				INDEX(owner),
				FOREIGN KEY (hash) REFERENCES file(hash)
			    ) ENGINE INNODB""")

    def insertFile(self,file):
	c=self.db.cursor()
	try:
	    c.execute("""INSERT IGNORE
			    INTO file (hash, mimetype, size)
			    VALUES (%s, %s, %s)""",
			    (file.hash, file.mimetype, file.size))
	    # c = self.db.cursor()
	    c.execute("""INSERT IGNORE
			    INTO path (hash, date, path, owner)
			    VALUES (%s, %s, %s, %s)""",
			    (file.hash, theDate, file.fullName, file.owner))
	    self.db.commit()
	finally:
	    c.close()

    def exfilter(self, status=None, mimetype=None,filename=None):
	if status == None:
	    status = '?'
	if mimetype == None:
	    mimetype = '%'
	if filename == None:
	    filename = '%'

	c=self.db.cursor()
	try:
	    c.execute("""SELECT DISTINCT file.hash,file.mimetype, path.path 
				FROM file JOIN path USING (hash)
				WHERE status = %s
				AND mimetype LIKE %s
				AND path.path LIKE %s
				""", (status, mimetype, filename)); 
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
	
	
