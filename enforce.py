#!/usr/bin/python
import os
import MySQLdb

import config
from dao import DAO
from file import File
	
#
# Process one file
def processFile(dao, f):
    dao.insertFile(f)
    print f.hash, ":", name, f.size, "(%s)" % f.mimetype
    

#
# main
#
# Walk throught directories
dao = DAO()
for root, dirs, files in os.walk(config.BaseDirectory):
    for name in files:
	try:
	    file = File(root, name)
	    processFile(dao, file)
	except IOError as (errno, strerror):
	    print "E : IOError", errno, "while processing", name, "(",strerror,")"

