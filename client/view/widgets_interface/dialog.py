from tkinter import *
class Dialog(Toplevel):
	def __init__(self,parent,title = None):
		super().__init__(parent)
		self.transient(parent)

		if title:
			self.title(title)
		self.parent = parent
		self.result = None
		body = Frame(self)
		self.initial_focus = self.body(body)
		body.pack(padx = 5,pady = 5)
		self.buttonbox()
		self.grab_set()
		if not self.initial_focus:
			self.initial_focus = self
		self.protocol('WM_DELETE_WINDOW',self.cancel)
		self.geometry('+%d+%d'%(parent.winfo_rootx()+50,parent.winfo_rooty()+50))
		self.initial_focus.focus_set()
		self.wait_window(self)
	def body(self,master):
		pass
	def buttonbox(self):
		pass
	
	def validate(self):
		return 1
	def apply(self):
		pass