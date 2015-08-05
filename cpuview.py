# psview.py
# written by Roger Woollett

from sys import version_info
if version_info[0] < 3:
	import Tkinter as tk
else:
	import tkinter as tk
	
import psutil as ps
from graph import ScrollGraph,XAxis,YAxis
	
class CpuLabel(tk.Frame):
	# helper class for CpuGraph
	def __init__(self,master,*args,**kwargs):
		tk.Frame.__init__(self,master,*args,**kwargs)
		
		tk.Label(self,text = 'system',fg = 'red',pady = 0,bd = 0).grid(row = 0,column = 0)
		self.sys = tk.Label(self,text = '-.-',fg = 'red',pady = 0,bd = 0)
		self.sys.grid(row = 1,column = 0)

		tk.Label(self,text = 'user',fg = 'green',pady = 0,bd = 0).grid(row = 2,column = 0)
		self.usr = tk.Label(self,text = '-.-',fg = 'green',pady = 0,bd = 0)
		self.usr.grid(row = 3,column = 0)		
	
class CpuGraph(tk.Frame):
	# show data for one core
	def __init__(self,master,*args,**kwargs):
		tk.Frame.__init__(self,master,*args,**kwargs)
		
		col0 = 60
		xaxis = 4
		yaxis = 4
		graphheight = self['height'] - xaxis 
		self.columnconfigure(0,minsize = col0)

		# create labels for col 0
		self.lab = CpuLabel(self)
		self.lab.grid(column = 0,row = 0)
		
		# create graph in col 1
		graphwidth = self['width'] - col0 - yaxis
		self.graph = ScrollGraph(self \
					,width = graphwidth, height = graphheight \
					,borderwidth = 0,highlightthickness = 0)
		self.graph.grid(row = 0,column = 2)
		
		# create an X axis without ticks to show a base line
		XAxis(self,0,0,width = graphwidth,height = xaxis,bd = 0,highlightthickness = 0) \
		.grid(row = 1,column = 2)
		
		#create a Y axis without ticks
		YAxis(self,0,0,width = yaxis,height = graphheight,bd = 0,highlightthickness = 0) \
		.grid(row = 0,column = 1)
		
	def set_sys(self,value):
		self.lab.sys.configure(text = value)
		
	def set_usr(self,value):
		self.lab.usr.configure(text = value)
		
	def clear(self):
		self.graph.clear()
	
class CpuView(tk.Frame):
	# show system and cpu times for all cores
	def __init__(self,master,*args,**kwargs):
		tk.Frame.__init__(self,master,*args,**kwargs)
		
		tk.Label(self,text = 'CPU time used per core').grid(row = 0,column = 0)
		self.columnconfigure(0,minsize = self['width'])	
		self.graphs = list()
		self.procs = ps.cpu_count()
		for i in range(0,self.procs):
			self.graphs.append(CpuGraph(self,width = self['width'],height = 70))
			
		for i in range(0,self.procs):
			self.graphs[i].graph.add_trace('user',1000,0,colour = 'green',size = 1)
			self.graphs[i].graph.add_trace('system',1000,0,colour = 'red',size = 1)
			self.graphs[i].grid(column = 0,row = i + 1)
				
	def bumptimes(self):
		# called repeatedly to update graphs
		x = ps.cpu_times_percent(interval = 0,percpu = True)
		for i in range(0,self.procs):
			user = x[i].user
			system = x[i].system
			scrollgraph = self.graphs[i]
			scrollgraph.graph.scrollex('user',0,10*user)
			scrollgraph.graph.scrollex('system',10*user,10*user + 10*system)
			scrollgraph.set_sys(str(system) + '%')
			scrollgraph.set_usr(str(user) + '%')
			
		self.afterid = self.after(1000,self.bumptimes)
		
	def start(self):
		# start the process of collecting data
		# call cpu_times_percent once and discard result
		ps.cpu_times_percent(interval = 0,percpu = True)
		self.bumptimes()
		
	def stop(self):
		# stop collecting data and clear graphs
		self.after_cancel(self.afterid)
		for graph in self.graphs:
			graph.clear()
			
		

