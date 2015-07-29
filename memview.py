# memview.py
# written by Roger Woollett

from sys import version_info
if version_info[0] < 3:
	import Tkinter as tk
else:
	import tkinter as tk
	
import psutil as ps
from graph import ScrollGraph,XAxis

class MemLabel(tk.Frame):
	def __init__(self,master,*args,**kwargs):
		tk.Frame.__init__(self,master,*args,**kwargs)
		
		self.percent = tk.Label(self,bd = 0)
		self.percent.grid(row = 0,column = 0)
		self.kb = tk.Label(self,bd = 0)
		self.kb.grid(row = 1,column = 0)

class MemView(tk.Frame):
	# memory usage
	def __init__(self,master,*args,**kwargs):
		tk.Frame.__init__(self,master,*args,**kwargs)
		
		col0 = 100
		self.columnconfigure(0,minsize = col0)
		
		tk.Label(self,text = 'Memory use (total - available)').grid(row = 0,column = 1)
		
		self.lab = MemLabel(self,bd = 0)
		self.lab.grid(row = 1,column = 0)
		
		graphwidth = self['width'] - col0
		self.graph = ScrollGraph(self \
					,width = graphwidth, height = 200 \
					,borderwidth = 0,highlightthickness = 0)
		self.graph.grid(row = 1,column = 1)
		
		self.graph.add_trace('mem',1000,0,colour = 'red')
		
		# create an X axis without ticks to show a base line
		XAxis(self,0,0,width = graphwidth,height = 4,bd = 0,highlightthickness = 0) \
		.grid(row = 2,column = 1)
		
	def bump(self):
		 x = ps.virtual_memory()
		 mem = x.percent
		 self.graph.scrollex('mem',0,10*mem)
		 
		 self.lab.percent.configure(text = str(mem) + '%')
		 self.lab.kb.configure(text = '{0:.2f}'.format((x.total - x.available)/1048576) + ' MB')
		 
		 self.afterid = self.after(1000,self.bump)
		
	def start(self):
		self.bump()
		
	def stop(self):
		self.after_cancel(self.afterid)
		self.graph.clear()

