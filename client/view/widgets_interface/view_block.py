from tkinter import *
class Block(Frame):
	def __init__(self,parent,**kwargs):
		super().__init__(parent,kwargs)
		self.config(highlightthickness = 2,highlightbackground = '#BBBBBB',highlightcolor = '#BBBBBB',padx = 20,pady = 10)
		self.body()
		self.buttonbox()
		self.parent = parent
	def body(self):
		pass
	def buttonbox(self):
		pass