from socket import *
import sys
import os
import time
import signal
from threading import Thread
import client_data_port
#导入model相关模块
from file import *
from file_folder import *
from database_handler import *
import my_protocol
#导入视图的相关模块
from login_view import Login_Page
from login_handler import Login_handler
from main_page import MainPage
from main_handler import Main_handler
# 用户路径
file_path = '/home/tarena/ftp_web(2)/'
#错误代码
# CODE_NUM=0

def run(ctrl_socket,child_pid,recv_queue,send_queue):
    # 把myconnection传给handler进行相关的登录操作
    # 创建客户端请求对象
    global _ctrl_socket
    _ctrl_socket = ctrl_socket
    c_ftp = MyFtp_Client(_ctrl_socket,recv_queue)
#    界面
    login_page = Login_Page()
    login_handler = Login_handler(login_page)
    login_handler.bind(comment_handler,c_ftp)
    login_page.register_handler(login_handler)
    login_handler.setup(child_pid,send_queue)
    login_page.run()
    main_page = MainPage()
    global main_handler
    main_handler =Main_handler(main_page)
    c_ftp.set_view_handler(main_handler)
    main_handler.bind(comment_handler,c_ftp)
    main_page.register_handler(main_handler)
    #设置父进程监听子进程信号
    signal.signal(40,main_handler.display_chat)

    main_handler.setup(child_pid,send_queue)
    main_page.run() 
    # 协议结构：请求类别 + 属性 + 内容 + 结束符
    # comment='list+'+str(client_add)+'+'+''+'+@end'


# 控制端--功能选择界面调用函数

#控制线程,这个线程中只做控制,具体传输反馈由父线程完成
def comment_handler(comment, c_ftp):
    data = comment.split('+')
    print(data)
    if data[0] == "list":
        if not data[2]:
            # 判断有没文件夹，没有，就发送list
            return c_ftp.list_request()
        else:
            # data[2]is 文件夹,有酒发送list data[2]
            return c_ftp.list_request(data[2])
    elif data[0] == "upld":
        return c_ftp.upload_request(data[1],data[2])
    elif data[0] == "dwld":
        return c_ftp.download_request(data[1],data[2])
        # 这两个功能只靠tcp---------------------------
    elif data[0] == 'chat':
        # data[2]是聊天内容
        c_ftp.chat_request(data[2])
        # 登录
    elif data[0] == "login":
        # data[1] 是账号
        # data[2] 是密码
        return c_ftp.login_request(data[1], data[2])
        #---------------------------------------------
    elif data[0] == "reg":
        # data[1] 是账号
        # data[2] 是密码
        return c_ftp.register_request(data[1], data[2])
        #---------------------------------------------
    elif data[0] == "quit":
        c_ftp.quit_request()
        return 0
    else:
        print("commond is not defined")


class MyFtp_Client():
    def __init__(self, s,chat_queue):
        self.s = s
        self.chat_queue = chat_queue
    def list_request(self, foldername=''):
        # 发送
        my_protocol.list_bale_TCP(self.s, foldername)
        # 等待接收
        data = my_protocol.unpake_TCP(self.s)
        if data != -1:
            f_property = data[2]
            return f_property

    #为服务器绑定视图句柄,供副线程调用
    def set_view_handler(self,handler):
        self.view_handler = handler

  #这个线程只负责告知服务器需要发送的文件名和文件属性,服务器会首先判断文件是否重名,
  #如果重名,则返回文件重名,如果不重名则添加相应文件信息到数据库  
    def upload_request(self, file_property,filename):
        #初始化错误码用于反馈结果
        CODE_NUM='1'
        # 打包发送
        my_protocol.upld_bale_TCP(self.s,file_property,filename)
        # 等待接收
        #生成file对象传给副进程使用
        file = File()
        file.unpack(file_property)
        data = my_protocol.unpake_TCP(self.s)
        if data != -1:
            if data[2] == '3':
                CODE_NUM='3'
            elif data[2]=='go':
                DATA_HOST = self.s.getsockname()[0]
                DATA_PORT = 0
                DATA_ADDR = (DATA_HOST, DATA_PORT)
                data_socket = socket()
                data_socket.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
                #客户端监听套接字
                data_socket.bind(DATA_ADDR)
                # data_socket.listen(10)
                data_addr = data_socket.getsockname()
                #给服务端发送端口号
                my_protocol.upld_bale_TCP(self.s,'',str(data_socket.getsockname()[1]))
                #等待服务端连接
                data_socket.close()
                
                # 开辟新的线程，上传文件
                t = Thread(target=client_data_port.run, args=(
                    'u', data_addr,file,self.view_handler))
                t.setDaemon(True)
                t.start()
        return CODE_NUM

    def download_request(self,download_path,filename):
        CODE_NUM="1"
        my_protocol.dwld_bale_TCP(self.s,'',filename)
        # 等待接收
        data = my_protocol.unpake_TCP(self.s)
        if data != -1:
            if data[2] == '2':
                # print("文件在服务器里不存")
                CODE_NUM='2'
            elif data[2]=='go':
                file_path = download_path +'/'+filename
                DATA_HOST = self.s.getsockname()[0]
                DATA_PORT = 0
                DATA_ADDR = (DATA_HOST, DATA_PORT)
                data_socket = socket()
                data_socket.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
                #客户端监听套接字
                data_socket.bind(DATA_ADDR)
                # data_socket.listen(10)
                data_addr = data_socket.getsockname()
                #给服务端发送端口号
                my_protocol.upld_bale_TCP(self.s,'',str(data_socket.getsockname()[1]))
                #等待服务端连接
                data_socket.close()
                t = Thread(target=client_data_port.run, args=(
                    'd', data_addr,file_path,self.view_handler))
                t.start()
                # if R==10:
                #     CODE_NUM=10
                # else:
                #     CODE_NUM=11
        return CODE_NUM

    def chat_request(self, message):
        # my_protocol.chat_bale_TCP(self.s,message)
        pass

    def login_request(self, admin, password):
        # tcp通信传给服务端数据库中的用户表比对,成功则登录
        # 注：admin,password:必须为字符串
        my_protocol.login_request(self.s, admin, password)
        response = self.s.recv(1024).decode()
        return response
    def register_request(self, admin, password):
        # 注：admin,password:必须为字符串
        my_protocol.reg_request(self.s, admin, password)
        response = self.s.recv(1024).decode()
        return response
    def get_chat_word(self):
        return self.chat_queue.get()
    def quit_request(self):
        # 通过协议打包发送
        my_protocol.quit_bale_TCP(self.s)
        self.s.close()
        print("已退出")
