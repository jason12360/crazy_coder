from fyc_version10 import Application

class MainPage(Application):
	def __init__(self):
		super().__init__()
	def register_handler(self,login_handler):
		self.login_handler = login_handler

	def download(self,event):
		download_path = super().download(event)
		self.login_handler.do_dwld(self.dwlabel.cget('text'),download_path)
	def upload(self,event):
		super().upload(event)
		self.login_handler.do_upld(self.upName)
	

