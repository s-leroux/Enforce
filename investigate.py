#!/usr/bin/python

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("hash", help="""The hash of the file to investigate""")
args = parser.parse_args()

import config
from dao import DAO

dao = DAO()

data = dao.getInfoByHash(args.hash)

if data == None:
    print "Don't know about %s" % args.hash
else:
    print data["hash"], "is", data["mimetype"]
    print "found %d times" % len(data["path"])
    n = 0
    powner = None
    ppath = None
    for (date, owner, path) in data["path"]:
	if powner != owner:
	    powner = owner
	    ppath = None
	if path is not None:
	    print "  %s | %10s | %s" % (date, owner, path)
	    n = n+1
	elif path is None and ppath is not None:
	    print "  ----"
	ppath = path

    print "Total found %d" % n
