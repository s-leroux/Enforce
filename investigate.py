#!/usr/bin/python

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("hash", help="""The hash of the file to investigate""")
args = parser.parse_args()

print args.hash

import config
from dao import DAO

dao = DAO()

data = dao.getInfoByHash(args.hash)

print data
