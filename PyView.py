# PyView.py
# A program to display computer related things
# written by Roger Woollett

from sys import version_info
if version_info[0] < 3:
	import Tkinter as tk
	import tkMessageBox as msg
else:
	import tkinter as tk
	import tkinter.messagebox as msg
	
try:
	import psutil as ps
except:
	psok = False
else:
	psok = True
	
from osview import OsView
from cpuview import CpuView
from memview import MemView

FRAME_WIDTH = 470
FRAME_HEIGHT = 320

class Mainframe(tk.Frame):
	# Mainframe contains views which are shown one at a time
	
	def __init__(self,master,*args,**kwargs):
		# *args packs positional arguments into tuple args
		#  **kwargs packs keyword arguments into dict kwargs
		
		tk.Frame.__init__(self,master,*args,**kwargs)
		# in this case the * an ** operators unpack the parameters
		
		self.rowconfigure(0,minsize = FRAME_HEIGHT)
		self.columnconfigure(0,minsize = FRAME_WIDTH)
		self.views = dict()
		self.views['osview'] = OsView(self,width = FRAME_WIDTH, height = FRAME_HEIGHT,bd = 0)
		self.views['cpuview'] = CpuView(self,width = FRAME_WIDTH,height = FRAME_HEIGHT,bd = 0)
		self.views['memview'] = MemView(self,width = FRAME_WIDTH,height = FRAME_HEIGHT,bd = 0)
					
		self.currentview = self.views['osview']
		self.currentview.grid(row = 0,column = 0,sticky = tk.N)
		
	def show_view(self,view):
		self.currentview.stop()
		self.currentview.grid_forget()
		self.currentview = self.views[view]
		self.currentview.grid(row = 0,column = 0,sticky = tk.N)
		self.currentview.start()

class App(tk.Tk):
	def __init__(self):
		tk.Tk.__init__(self)
			   
		# set the title bar text
		self.title('PyView')
		
		if not psok:
			msg.showinfo('Information','You must install the import libary psutil to use this program')
			self.destroy()
			return
		  
		# create a menu bar
		mainMenu = tk.Menu(self)
		self.config(menu=mainMenu)
		
		# create a file menu with an exit entry
		# you may need to add more entries
		fileMenu = tk.Menu(mainMenu)
		fileMenu.add_command(label='Exit',command=self.quit)
		mainMenu.add_cascade(label='File',menu=fileMenu)
		
		# create a view menu
		viewMenu = tk.Menu(mainMenu)
		viewMenu.add_command(label = 'Information',command = lambda: self.show_view('osview'))
		viewMenu.add_command(label = 'Cpu times',command = lambda: self.show_view('cpuview'))
		viewMenu.add_command(label = 'Memory usage',command = lambda: self.show_view('memview'))		
		mainMenu.add_cascade(label = 'View',menu = viewMenu)
		
		# any main menu should have a help entry
		helpMenu = tk.Menu(mainMenu)
		helpMenu.add_command(label = 'About',command = self.show_about)
		mainMenu.add_cascade(label = 'Help',menu = helpMenu)
		
		# create and pack a Mainframe window
		self.frame = Mainframe(self,width = FRAME_WIDTH,height = FRAME_HEIGHT,bd=0)
		self.columnconfigure(0,minsize = FRAME_WIDTH)
		self.frame.grid(row = 0,column = 0)
		
	def show_about(self):
		# show the about box
		msg.showinfo('About', 'PyView - 1.0\nA program to show system data \nwritten by Roger Woollett')
		
	def show_view(self,view):
		# switch to the selected view
		self.frame.show_view(view)
			
# create and run an App object
App().mainloop()
