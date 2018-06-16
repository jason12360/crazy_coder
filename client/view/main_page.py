from view.fyc_version10 import Application

class MainPage(Application):
	def __init__(self):
		super().__init__()
	def register_handler(self,login_handler):
		self.login_handler = login_handler
		self.login_handler.setup()
	def download(self,event):
		self.login_handler.do_dwld(self.dwlabel.cget('text'))
	def upload(self,event):
		super().upload(event)
		self.login_handler.do_upld(self.upName)
	

