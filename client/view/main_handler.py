
# 这是一个用于处理主视图中各个事件的模块
# 用来控制视图的IO响应
# 这个类需要在主视图的初始化时建立
# 客户端网络接口类方法comment_handler和client实例
# 将通过这个类的bind方法给这个类传入，
# （接上）用于向服务端发送用户传入的信息。
import time
from model.file import File
from model.file_folder import Filefolder

class Main_handler:
	def __init__(self,page):
	#初始化时传入视图模块，以便调用视图的各个widgets
		self.page = page
		self.ERROR_MAP={
			2 :'服务器文件不存在',
			3 :'文件已存在',
			10:'下载成功',
			11:'下载失败',
			12:'上传成功',
			13:'上传失败'
			#这里定义各种错误返回什么信息
			}	
	def bind(self,comment_handler,client):
		self.comment_handler = comment_handler
		self.client = client
	def setup(self):
		#初始化时调用此方法获取相关数据
		#获取用户名并显示
		#获取在线用户信息并显示

		#获取文件列表并显示
		command = "list+ + +@end"
		file_folder_str = self.comment_handler(command,self.client)
		self.file_folder = Filefolder()
		self.file_folder.unpack(file_folder_str)
		self.do_list()
				
#以下函数将会定义主视图的IO事件
	def do_list(self):
		self.page.files_display(self.file_folder.to_list())
#当用户点击下载，调用此函数
	def do_dwld(self,filename):
		# file_dir = self.page.show_dw_filedialog()
		command = "dwld+"+' '+'+'+filename+"+@end"
		result = self.comment_handler(command,self.client)
		if result != 10:
			self.page.show_error_message(self.ERROR_MAP[result])
			return 
		else:
			self.page.show_message('下载成功')




#当用户点击上传，调用此函数
	def do_upld(self,filename):
	#弹出文件选择器
	#读取选取文件路径
		# filename = self.page.show_up_filedialog()
	#根据文件路径生成文件实例
		my_file = File()
		my_file.create_file(filename)
		# filename = my_file.get_name()
		my_file.set_last_mtime(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
		my_file.set_file_create_time(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
		file_property= my_file.pack()
	#向数据端发送指令
		command = "upld+"+file_property+'+'+filename+"+@end"
		result = self.comment_handler(command,self.client)
	#处理异常	
		if result != 12:

			self.page.show_error_message(self.ERROR_MAP[result])
			return
	
		for file in self.file_folder.get_file_list():
			if file.get_name() == my_file.get_name():
				file.set_last_mtime(my_file.get_last_mtime())
				break
		else:
			self.file_folder.add_file(my_file)
	#等到数据端接收完成后,刷新文件列表页面
		self.do_list()