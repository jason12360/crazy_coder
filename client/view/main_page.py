from fyc_version10 import Application

class MainPage(Application):
	def __init__(self):
		super().__init__()
	def run(self):
		self.root.protocol("WM_DELETE_WINDOW", self.main_handler.do_cancel)
		super().run()
	def register_handler(self,main_handler):
		self.main_handler = main_handler

	def download(self,event):
		download_path = super().download(event)
		self.main_handler.do_dwld(self.dwlabel.cget('text'),download_path)
	def upload(self,event):
		super().upload(event)
		self.main_handler.do_upld(self.upName)
	def close(self):
		self.root.destroy()
	

