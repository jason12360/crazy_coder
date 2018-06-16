#导入相关tkinter模块
from tkinter import *
import tkinter.font as tkFont
import tkinter.messagebox
# 导入自定义widgets模块  
from view.widgets_interface.view_block import Block
from view.widgets_interface.my_widgets import *
#导入注册子视图模块
from view.register_view import Register_View


#登录子视图类
class Login_View(Block):
	def __init__(self,parent,font,login_handler):
		self.font = font
		self.login_handler = login_handler
		super().__init__(parent)
		self.config(height = 300,width =300)
		self.place(relx=0.75,rely =0.5, anchor=CENTER)
		self.bind_all('<Return>',self.login)
		
	def buttonbox(self):
		box = Frame(self)
		w = Mybutton(box,text= '登录',width =20,fun=self.login,font = self.font)
		w.pack(side=TOP,padx = 5,pady = 5)
		w = Mybutton(box,text= '注册',width =20,fun=self.register,font = self.font)
		w.pack(side = BOTTOM,padx =5,pady = 5)

		self.bind('<Return>',self.login)
		self.bind('<Escape>',self.cancel)
		box.place(relx=0.5,rely =0.8,anchor=CENTER)

	def body(self):
		body = Frame(self)
		Label(body,font = self.font,text='用户名：',fg = '#555555',anchor = W,width = 20).grid(row = 0)
		Label(body,font = self.font,text='密码：',fg = '#555555',anchor = W,width = 20).grid(row = 2)

		self.e1 = Myentry(body,font = self.font)
		self.e2 = MyPasswordEntry(body,font = self.font)

		self.e1.grid(row = 1)
		self.e2.grid(row = 3)
		body.place(relx=0.5,rely =0.3,anchor=CENTER)

	def login(self,event = None):
		self.login_handler.do_login()
		
	def register(self,event = None):
		self.login_handler.login_do_register()
	def cancel(self,event = None):
		self.login_handler.do_cancel()
	def show_error_message(self,e):
		tkinter.messagebox.showerror(
				'检测用户名',
				e)
	def close(self):
		self.destroy()


#登录页面类
class Login_Page:
	def __init__(self):
		root = Tk()
		self.root = root
		#创建对应的背景
		root.geometry('800x600')
		root.resizable(width=False,height=False)
		root.config(bg = '#333333')
		ftext = Frame(root)
		ftext.config(bg = '#333333')
		ft_header = tkFont.Font(size = 60,weight=tkFont.BOLD)
		self.ft_font = tkFont.Font(size = 15)
		l = Label(ftext,text = '疯狂码头',fg = '#EEEEEE',bg='#333333',font = ft_header)
		l.pack()
		l1 = Label(ftext,justify = LEFT,text = '一个简易的中期项目，在这里你可以上传\n下载你上课的笔记和代码，并可以和你的\n组员一起聊天',font = self.ft_font,fg = '#EEEEEE',bg='#333333')
		l1.pack()
		ftext.place(relx=0.3,rely =0.45,anchor=CENTER)
		#创建登录界面视图
	def register_handler(self,login_handler):
		self.login_handler = login_handler		
		self.login_view = Login_View(self.root,self.ft_font,self.login_handler) 
	def get_login_handler(self):
		return self.login_handler
	def run(self):
		self.root.protocol("WM_DELETE_WINDOW", self.login_handler.do_cancel)
		self.root.mainloop()
	def close_login_view(self):
		self.login_view.destroy()
	def create_register_view(self):
		self.register_view = Register_View(self.root,self.ft_font,self.login_handler)
	def close(self):
		self.root.destroy()

if __name__=='__main__':
	main()