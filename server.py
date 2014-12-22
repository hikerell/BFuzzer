import BaseHTTPServer
import rGener
from fuzzutil import conf

cf = conf()
fuzz = rGener.Fuzz(cf)
curHTML = ""
initHTML = """
   			<html>
			<head>
			<meta http-equiv="refresh" content="3; url=http://"""+cf.host+':'+cf.port+"""/next" />
			</head>
			<body>
			Waiting for fuzzing...
			</body>
			"""

class FuzzRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
	def do_GET(self):
		global curHTML
		global cf
		global fuzz
		global initHTML
		if 'next' in self.requestline:
			curHTML = fuzz.getNext()
			self.send_response(200)
			self.send_header("Content-type", "text/html; charset=utf-8")
			self.send_header("Content-Length", str(len(curHTML)))
			self.end_headers()
			self.wfile.write(curHTML)
			print '[*] sample cases:'+str(fuzz.num)+'\r',
		elif 'init' in self.requestline:
			self.send_response(200)
			self.send_header("Content-type", "text/html; charset=utf-8")
			self.send_header("Content-Length", str(len(initHTML)))
			self.end_headers()
			self.wfile.write(initHTML)
		elif 'cur' in self.requestline:
			self.send_response(200)
			self.send_header("Content-type", "text/html; charset=utf-8")
			self.send_header("Content-Length", str(len(curHTML)))
			self.end_headers()
			self.wfile.write(curHTML)
		else:
			self.send_response(200)
			self.send_header("Content-type", "text/html; charset=utf-8")
			self.send_header("Content-Length", str(len('')))
			self.end_headers()
			self.wfile.write('')
			
		


if __name__ == '__main__':
	cf = conf()
	print '[*] server start on '+cf.host+':'+cf.port 
	server = (cf.host, int(cf.port))
	httpd = BaseHTTPServer.HTTPServer(server, FuzzRequestHandler)
	httpd.serve_forever()
