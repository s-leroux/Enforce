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

mt=None
#mt="video/mpeg"
mt="image/jpeg"
#mt="image/gif"
fn=None
# mt=None # "video/mpeg"
#fn="%.exe"

for dir in (config.ExfilterDirectory, config.OKDirectory, 
		config.COPYRIGHTDirectory, config.XDirectory):
	if not os.path.isdir(dir):
		print "W: Creating", dir
		os.mkdir(dir)

for (hash, mimetype, path) in dao.exfilter(mimetype=mt,filename=fn):
    ext = mimetypes.guess_extension(mimetype)
    src = path
    dst = os.path.join(config.ExfilterDirectory, "%s%s") % (hash,ext)

    try:    
	shutil.copy2(src, dst)
	print ">", dst,"(",src,")"
    except IOError, e:	
	print "X", dst,"(",src,")", e.args[1]
