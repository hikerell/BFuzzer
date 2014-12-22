# -*- coding: utf-8 -*-

from pydbg import *
from pydbg.defines import *
import utils
import re
import os
import urllib
import datetime
import hashlib
		

def deal_accessv(dbg):
	if dbg.dbg.u.Exception.dwFirstChance:
		return DBG_EXCEPTION_NOT_HANDLED
	crash_bin = utils.crash_binning.crash_binning()
	crash_bin.record_crash(dbg)
	name = hashlib.md5(str(datetime.datetime.now())).hexdigest()
	crashfile = dbg.cf.logspath + '\\crash-'+name+'.txt'
	f = open(crashfile, 'w')
	f.write(crash_bin.crash_synopsis())
	f.close()
	pocfile = dbg.cf.logspath + '\\poc-' + name + '.html'
	pocurl = 'http://'+dbg.cf.host + ':' + dbg.cf.port + '/cur'
	print "will gen poc file"
	urllib.urlretrieve(pocurl, pocfile)
	print "poc file gen success"
	dbg.terminate_process()
	print  'crash info and poc have been saved!'
	return DBG_EXCEPTION_NOT_HANDLED

class crasher():
	"""docstring for crasher"""
	def __init__(self, cf):
		self.cf = cf
		self.cases = 1

	def hook(self, dbg):
		return self.hookIE(dbg)

	def hookIE(self, dbg):
		loadpid = dbg.pid
		dbg.detach()
		dbg = pydbg()
		dbg.cf = self.cf
		print "IE first process PID = %d"%loadpid
		pattern = r'iexplore.exe\s*([0-9]*)\s*Console'
		count = 0
		while count<=1:
			p = os.popen('tasklist|find "iexplore"')
			pids = re.findall(pattern, p.read())
			count = len(pids)
		print "find IE pids:" + str(pids)
		for pid in pids:
			if loadpid == int(pid):
				continue
			try:
				dbg.attach(int(pid))
				dbg.set_callback(EXCEPTION_ACCESS_VIOLATION, deal_accessv)
				dbg.set_callback(EXCEPTION_ACCESS_VIOLATION, deal_accessv)
				dbg.set_callback(EXCEPTION_ACCESS_VIOLATION, deal_accessv)
				print 'hook IE(pid=%s) success!'%(pid)
				return dbg
			except Exception, e:
				print 'hook IE(pid=%s) failed!'%(pid)
				print e
				return None


		