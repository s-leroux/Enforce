import os
import magic
import hashlib

#
# Initialize libmagic
mime=magic.open(magic.MAGIC_MIME)
mime.load()

class File:
    def __init__(self, root, name):
	self.root = root
	self.name = name
	self.fullName = os.path.join(root, name)
	(self.dirName, self.baseName) = os.path.split(self.fullName)
	self.size = os.path.getsize(self.fullName)

	stat = os.stat(self.fullName)
	self.size = stat.st_size
	self.mtime = stat.st_mtime
	self.atime = stat.st_atime
	self.ctime = stat.st_ctime

	try:
	    self.owner = self.root.split(os.sep)[3]
	except IndexError:
	    self.owner="UNKNOWN"
	self.hash = self._hash()
	self.mimetype = self._mimetype()

    def _mimetype(self):
	global mime
	if mime == None:
	    mime = magic.Magic()
	    mime.load()
	return mime.file(self.fullName).partition(";")[0]


    def _hash(self):
	def fileDataBlock(f):
	    while True:
	        block = f.read(16*1024)
	        if (len(block)==0):
		    break
		yield block

	m = hashlib.md5()
	with open(self.fullName, "rb") as f:
	    for data in fileDataBlock(f):
		m.update(data)

	return m.hexdigest()

