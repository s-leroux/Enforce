import sys

class Logger:
    def __init__(self):
	self.file = open("log.txt", "wt")

    def write(self, cat, text):
	self._write(cat, text, self.file)

    def echo(self, cat, text):
	self._write(cat, text, self.file)
	self._write(cat, text, sys.stdout)

    def _write(self, cat, text, dst):
	cat = cat.ljust(6)
	for line in text.split('\n'):
	    dst.write(cat + ": " + line + '\n')
	dst.flush()


Log=Logger()
