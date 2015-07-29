# graph.py
# class to show a moving graph
# written by Roger Woollett

from sys import version_info
if version_info[0] < 3:
	import Tkinter as tk
else:
	import tkinter as tk

class Trace():
	# class to represent a single trace in a ScrollGraph
	def __init__(self,master,max_y,min_y,colour,size):
		
		self.master = master
		self.size = size
		self.scale = master.height/(max_y - min_y)
		self.offset = -self.scale*min_y
		
		# create a list of line ids
		self.lines=[]
		i = 0
		while i < master.width:
			self.lines.append(master.create_line(i,0,i,0,fill = colour,width = size))
			i += 1
			
	def scrollex(self,miny,maxy):
		# alternative scroll where you can set top and bottom of pixel line
		self.scrollview()
		
		low = self.master.height - (self.scale*miny + self.offset)
		high = self.master.height - (self.scale*maxy + self.offset)
		self.master.coords(self.lines[0],0,low,0,high)
	
	def scroll(self,value):
		# scroll to the right and add new value
		self.scrollview()
		
		value = self.scale*value + self.offset
		# we want positive upwards
		value = self.master.height - value           
		# add new value
		self.master.coords(self.lines[0],0,value,0,value + self.size)
		
	def clear(self):
		# clear the trace
		for index in self.lines:
			self.master.coords(index,0,0,0,0)
	
	def scrollview(self):
		# do scroll
		i = self.master.width - 1
		coords = self.master.coords
		while i > 0:
			x = coords(self.lines[i - 1])
			coords(self.lines[i],i,x[1],i,x[3])
			i -= 1
		  
class ScrollGraph(tk.Canvas):
	# class to show a scrolling graph
	def __init__(self,master,*args,**kwargs):
		tk.Canvas.__init__(self,master,*args,**kwargs)
		
		self.width = int(self['width'])
		self.height = int(self['height'])
		
		self.traces = {}
		 
	def add_trace(self,name,max_x,min_x,colour = 'black',size = 1):
		# call to add a trace to the graph
		self.traces[name] = Trace(self,max_x,min_x,colour=colour,size = size)
	
	def scroll(self,name,value):
		# call to add a new value to a trace
		self.traces[name].scroll(value)
		
	def scrollex(self,name,miny,maxy):
		self.traces[name].scrollex(miny,maxy)
		
	def clear(self):
		# clear all traces
		for trace in self.traces:
			self.traces[trace].clear()
		
class XAxis(tk.Canvas):
	# class to show horizantal x axis with ticks
	def __init__(self,master,big,small,size = 1,*args,**kwargs):
		tk.Canvas.__init__(self,master,*args,**kwargs)
		
		width = int(self['width'])
		height = int(self['height'])
		
		self.create_line(0,0,width-1,0,width = size)
			
		# do small ticks
		if small > 0:
			i = small
			while i < width:
				self.create_line(i,0,i,height/2,width = size)
				i += small
			
		# do big ticks
		if big > 0:
			i = 0
			while i < width:
				self.create_line(i,0,i,height,width = size)
				i += big
