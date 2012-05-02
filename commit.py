#!/usr/bin/python
import os
import shutil
import mimetypes

import config
from dao import DAO
from file import File
#
# main
#
dao = DAO()

for (status, directory) in (('OK', config.OKDirectory),
			    ('X', config.XDirectory),
			    ('COPYRIGHT', config.COPYRIGHTDirectory)):
    for root, dirs, files in os.walk(directory):
	for name in files:
	    file = File(root,name)
	    dao.mark(file.hash, status)
	    print "%-10s : %s" % (status, file.fullName)
	    os.unlink(file.fullName)
	
