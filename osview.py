# views.py
# written by Roger Woollett

from sys import version_info
if version_info[0] < 3:
	import Tkinter as tk
else:
	import tkinter as tk
	
import os
import platform as pl
import psutil as ps

class OsView(tk.Frame):
	def __init__(self,master,*args,**kwargs):
		tk.Frame.__init__(self,master,*args,**kwargs)
		
		col0 = 160
		self.columnconfigure(0,minsize = col0)

		row = 0
		
		self.add_entry(row,'User id: ',os.getlogin())
		row += 1 
		self.add_entry(row,'Machine id: ',pl.node())
		row += 1
		self.add_entry(row,'Operating system: ',pl.platform())
		row += 1
		self.add_entry(row,'Machine type: ',pl.machine())
		row += 1
		self.add_entry(row,'Python version: ',pl.python_version())
		row += 1
				
		if pl.system() == 'Linux':
			self.add_entry(row,'Linux distribution: ',pl.linux_distribution())
			row += 1
		
		self.add_entry(row,'Number of processors: ',ps.cpu_count())
		row += 1
		
		x=ps.virtual_memory()
		self.add_entry(row,'Total memory:',x.total)
		row += 1
		self.add_entry(row,'Available memory: ',x.available)
		row += 1
			
	def add_entry(self,row,prompt,text):
		tk.Label(self,text = prompt,justify = tk.RIGHT,bd = 0,highlightthickness = 0) \
		.grid(row = row,column = 0,sticky = tk.E)
		
		tk.Label(self,text = text,justify = tk.LEFT, bd = 0,highlightthickness = 0) \
		.grid(row = row,column = 1,sticky = tk.W)
		
	def stop(self):
		pass
		
	def start(self):
		pass

			   
		
