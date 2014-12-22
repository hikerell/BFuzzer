import Templater

class Fuzz():
	def __init__(self, cf):
		self.cf = cf
		self.urlnext = 'http://'+cf.host+':'+cf.port+'/next'
		self.Tlper = Templater.JSTemplater(cf)
		self.num = 1
		self.refreshCnt = '<meta http-equiv="refresh" content="1; url='+self.urlnext+'/long" />'

	# return the next html document
	def getNext(self):
		script = self.Tlper.JSGen()
		data = '<html><head>'+self.refreshCnt+script+'<body onload="fzz();"></body></html>'
		self.num += 1
		return data
		
