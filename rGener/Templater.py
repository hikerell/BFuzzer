"""
Define the elements of HTML + JS

HTMLs [] collect elements of HTML
JS_add [] collects the functions which are relative with JS nodes *add* operations 
JS_ref [] collects the functions which are relative with JS nodes *reference* operations
JS_rm [] collects the functions which are relative with JS nodes *remove* operations  
"""

import random

colorbase = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
HTMLs = ['a', 'abbr', 'acronym', 'address', 'area', 'artical', 'aside', 'audio', 'b', 'base', 'basefont', 'bdi','bdo', 'big', 'blockquote', 'br', 'button', 'canvas','caption', 'center', 'cite', 'code', 'col','colgroup','command', 'datalist', 'dd', 'del', 'details','dir', 'div', 'dfn', 'dialog', 'dl', 'dt', 'em', 'embed', 'fieldset', 'figcaption', 'figure', 'font', 'footer', 'form', 'frame', 'frameset', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'header', 'hr', 'i', 'iframe', 'img', 'input', 'ins', 'isindex', 'kbd', 'keygen', 'label', 'legend', 'li', 'link','map', 'mark', 'menu', 'menuitem', 'meter', 'nav', 'noframes', 'noscript', 'object', 'ol', 'optgroup', 'option','output', 'p', 'param', 'pre', 'progress', 'q', 'rp', 'rt', 'ruby', 's', 'samp', 'section', 'select', 'small', 'source', 'span', 'strike', 'strong', 'style', 'sub', 'summary', 'sup', 'table', 'tbody', 'td', 'textarea', 'tfoot', 'th', 'thead', 'time', 'tr', 'track', 'tt', 'u', 'ul', 'var', 'video', 'wbr', 'xmp']

class JSTemplater():
	ids_min = 15
	ids_max = 25
	nodes = 0
	ids = 0
	def __init__(self, cf):
		self.cf = cf
		self.urlnext = 'http://'+cf.host+':'+cf.port+'/next'

	"""
	create new node
	string name : element tag name
	"""
	def node_create(self,name):
		self.nodes += 1
		#[out] document.createElement('div')
		return "document.createElement('"+name+"')"

	"""
	create new node
	name : element tag name and save in the variable 'id_x'
	"""
	def node_create_with_var(self,name):
		self.nodes += 1
		self.ids += 1
		#[out] var id_2=document.createElement('div');id_2.id = 'id_2';
		return "var id_"+ str(self.ids) +"=document.createElement('"+name+"');"+"id_"+ str(self.ids) +".id='id_" + str(self.ids) +"';"

	
		

	"""
	get element by id_x 
	string id_x : element's id
	"""
	def node_get_by_id(self,id_x):
		#[out] document.getElementById('id_x')
		return "document.getElementById('id_"+ id_x +"')"


	"""
	add child node under the existed parent node using the function f.
	string id_child : element's name defined in HTMLs
	string id_parent : the id of the existed node
	"""
	def node_add_by_innerHTML(self, id_child, id_parent):
		#[out] id_parent.innerHTML=id_child;
		return id_parent+".innerHTML="+id_child+".innerHTML;"

	def node_add_by_appendChild(self, id_child, id_parent):
		r = random.randint(0,3)
		if r<2:
			cxt = "document.createElement('"+random.choice(HTMLs[1:])+"')"
			#[out] id_parent.appendChild(document.createElement('div'));
			return id_parent+".appendChild("+cxt+");"
		else:
			#[out] id_parent.appendChild(id_child);
			return id_parent+".appendChild("+id_child+");"

	def node_add_by_applyElement(self, id_child, id_parent):
		r = random.randint(0,3)
		if r<2:
			cxt = "document.createElement('"+random.choice(HTMLs[1:])+"')"
			#[out] document.createElement('div').applyElement(id_parent);
			return cxt+".applyElement("+id_parent+");"
		else:
			#[out] id_parent.applyElement(id_child);
			return id_child+".applyElement("+id_parent+");"

	def node_add_by_outerHTML(self, id_child, id_parent):
		r = random.randint(0,1)
		if r==0:
			#[out] id_child.outerHTML()='';
			return id_child+".outerHTML='';"
		else:
			#[out] id_parent.outerText='';
			return id_parent+".outerText='';"

	"""
	random 
	"""
	def randTagIndex(self):
		return random.randint(0,len(HTMLs)-1)

	def randTagName(self):
		return HTMLs[self.randTagIndex()]

	def randNodeId(self):
		return random.randint(1,self.ids)

	def randTwoNodes(self):
		idOne = self.randNodeId()
		idTwo = self.randNodeId()
		while idOne == idTwo :
			idTwo = self.randNodeId()
		return ["id_"+str(idOne), "id_"+str(idTwo)]

	def GC(self):
		return "CollectGarbage();"

	def initTree(self):
		bgcolor = random.choice(colorbase)+random.choice(colorbase)+random.choice(colorbase);
		cxt="document.body.style.backgroundColor = '#"+bgcolor+"';";
		while( self.ids < self.ids_min):
			cxt += self.node_create_with_var(self.randTagName())
			cxt += "document.body.appendChild(id_"+str(self.ids)+");"
		return cxt

	def JSGen(self):
		self.nodes = 0
		self.ids = 0
		add_fns = [self.node_add_by_innerHTML, self.node_add_by_appendChild, self.node_add_by_applyElement, self.node_add_by_outerHTML]
		cxt=""
		cxt = self.initTree()
		HTMLs.append('body')

		add_opts = random.randint(5, self.ids/2+5)
		while add_opts > 0:
			rnodes = self.randTwoNodes()
			cxt +=random.choice(add_fns)(rnodes[0], rnodes[1])
			add_opts -= 1;
		
		cxt += self.GC()
		#return "<script>"+cxt+"</script>"
		#for debug

		cxt = '<script>function fzz(){try{'+cxt+'}catch(e){/*alert("syntax error:"+e); window.location.href=*/};CollectGarbage();window.location.href = "'+self.urlnext+'?xxxxxxxx"}</script>'
		#cxt = '<script>function fzz(){try{'+cxt+'}catch(e){/*alert("syntax error:"+e);*/ window.location.href="'+self.urlnext+'?bbbb"};CollectGarbage();}</script>'
		#print cxt
		return cxt




if __name__=="__main__":
    js = JSTemplater()
    print js.JSGen()
