# -*- coding: utf-8 -*-
import fuzzutil
import os
import pydbg
import time
import datetime
import urllib
import hashlib

class moniter():
	"""moniter"""
	def __init__(self):
		self.cf = fuzzutil.conf()
		self.crasher = fuzzutil.crasher(self.cf)
		self.InitPage = 'http://'+self.cf.host+':'+self.cf.port+'/init'
		self.tellme('Taregt: ' + self.cf.target)
		self.tellme('Path: ' + self.cf.targetpath)

	def tellme(self, message):
		t = str(datetime.datetime.now())
		t = t[:t.rfind('.')]
		print '['+t+'] ' + message

	def run(self):
		while 1:
			os.system('taskkill /T /F /IM '+ self.cf.image + '> logs/null')
			time.sleep(3)
			dbg = pydbg.pydbg()
			dbg.load(self.cf.targetpath, command_line=self.InitPage)
			self.tellme(self.cf.image + ' running...' + 'pid='+str(dbg.pid))
			time.sleep(1)
			dbg_browser = self.crasher.hook(dbg)
			if dbg_browser!=None:
				dbg_browser.run()
				self.tellme(self.cf.target + ' crash... ')
				dosfile = self.cf.logspath + '\\dos-' + hashlib.md5(str(datetime.datetime.now())).hexdigest() + '.html'
				dosurl = 'http://'+self.cf.host + ':' + self.cf.port + '/cur'
				urllib.urlretrieve(dosurl, dosfile)
		
	
if __name__=='__main__':
	moniter().run()