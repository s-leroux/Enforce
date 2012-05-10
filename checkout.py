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
#mt="image/jpeg"
#mt="image/gif"
#mt="image/png"
fn=None
mt="video/%"
mt="audio/mpeg"
#fn="%.exe"

for dir in (config.ExfilterDirectory, config.OKDirectory, 
		config.COPYRIGHTDirectory, config.XDirectory):
	if not os.path.isdir(dir):
		print "W: Creating", dir
		os.mkdir(dir)

prevdst = ""
for (hash, mimetype, path,file) in dao.exfilter(mimetype=mt,limit=2000):
    ext = mimetypes.guess_extension(mimetype)
    src = os.path.join(path,file)
    dst = os.path.join(config.ExfilterDirectory, "%s%s") % (hash,ext)
    if dst != prevdst:
        try:    
    	    shutil.copy2(src, dst)
    	    print ">", dst,"(",src,")"
	    prevdst = dst
        except IOError, e:	
    	    print "X", dst,"(",src,")", e.args[1]
    else:
        print '"', dst,"(",src,")"
