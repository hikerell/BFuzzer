import ConfigParser
import os

class conf():
	"""parse config.ini"""
	def __init__(self):
		pwd = os.getcwd()
		if pwd.find('\\fuzzutil')==-1:
			self.homedir = pwd
		else:
			self.homedir = pwd[:pwd.find('\\fuzzutil')]
		
		self.cf = ConfigParser.ConfigParser()
		self.cf.read(self.homedir+'\\config.ini')
		self.host = self.cf.get('server', 'host')
		self.port = self.cf.get('server', 'port')
		self.target = self.cf.get('moniter', 'target')
		self.targetpath = self.cf.get(self.target, 'path')
		self.image = self.targetpath[self.targetpath.rfind('\\')+1:]
		self.logspath = self.homedir + '\\logs'
