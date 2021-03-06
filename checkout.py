#!/usr/bin/python
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--mime", 
		    help="""Extract files by their mime/type""",
		    action="append",
		    default=[])
parser.add_argument("--name", 
		    help="""Extract image/jpeg files""",
		    action="append",
		    default=[])
parser.add_argument("--limit", 
		    help="""Limit the number of files extracted""",
		    action="store",
		    type=int,
		    default=1000)

args = parser.parse_args()

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

for dir in (config.ExfilterDirectory, config.OKDirectory, 
		config.COPYRIGHTDirectory, config.XDirectory):
	if not os.path.isdir(dir):
		print "W: Creating", dir
		os.mkdir(dir)

prevdst = ""
count = 0
for (hash, mimetype, path,file) in dao.exfilter(mimetype=args.mime,
						filename=args.name):
    ext = mimetypes.guess_extension(mimetype)
    if ext is None:
	ext = ".unknown"
    src = os.path.join(path,file)
    dst = os.path.join(config.ExfilterDirectory, "%s%s") % (hash,ext)
    if dst != prevdst:
        try:    
    	    shutil.copy2(src, dst)

	    f = File(config.ExfilterDirectory,"%s%s" % (hash,ext))
	    if f.hash != hash:
		# Non matchinh hash occurs when the target file has changed
		# since last check
		print "*", dst,"(",src,")"
		os.unlink(dst)
	    else:
	        print ">", dst,"(",src,")"
	        prevdst = dst
		count = count+1
		if count == args.limit:
		    break
        except IOError, e:	
    	    print "X", dst,"(",src,")", e.args[1]
    else:
        print '"', dst,"(",src,")"
