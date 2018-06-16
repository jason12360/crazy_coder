from socket import *
import sys
import os
import time
from threading import Thread
if __name__=='__main__':
    import client_data_port
    import file
    from file_folder import *
    from database_handler import *
    import my_protocol
else:
    import web.client_data_port as client_data_port
    import model.file
    from model.file_folder import *
    from model.database_handler import *
    import web.my_protocol as my_protocol
#导入视图的相关模块
from view.login_view import Login_Page
from view.login_handler import Login_handler
from view.main_page import MainPage
from view.main_handler import Main_handler
# 用户路径
file_path = '/home/tarena/ftp_web(2)/'
#错误代码
# CODE_NUM=0

def run(ctrl_socket, data_socket):
    # 把myconnection传给handler进行相关的登录操作
    # 创建客户端请求对象
    c_ftp = MyFtp_Client(ctrl_socket, data_socket)
    # 界面
    login_page = Login_Page()
    login_handler = Login_handler(login_page)
    login_handler.bind(comment_handler,c_ftp)
    login_page.register_handler(login_handler)
    login_page.run()
    main_page = MainPage()
    main_handler =Main_handler(main_page)
    main_handler.bind(comment_handler,c_ftp)
    main_page.register_handler(main_handler)
    main_handler.setup()
    main_page.run() 
    # 协议结构：请求类别 + 属性 + 内容 + 结束符
    # comment='list+'+str(client_add)+'+'+''+'+@end'


# 控制端--功能选择界面调用函数


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
        return c_ftp.upload_request(data[2])
    elif data[0] == "dwld":
        return c_ftp.download_request(data[2])
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
    def __init__(self, s, data_socket):
        self.s = s
        self.data_socket = data_socket

    def list_request(self, foldername=''):
        # 发送
        my_protocol.list_bale_TCP(self.s, foldername)
        # 等待接收
        data = my_protocol.unpake_TCP(self.s)
        if data != -1:
            f_property = data[2]
            return f_property
    #子线程给父进程传参用
    def set_data(self,v):
        global R
        R = v   
    def upload_request(self, filename):
        CODE_NUM=0
        # 打包发送
        my_protocol.upld_bale_TCP(self.s,'',filename)
        # 等待接收

        data = my_protocol.unpake_TCP(self.s)
        if data != -1:
            if data[2] == '3':
                CODE_NUM=3
                print("文件已存在(重名)")
            elif data[2]=='go':
                # 开辟新的线程，上传文件
                t = Thread(target=client_data_port.run, args=(
                    'u', self.data_socket, filename,self.set_data))
                t.start()
                t.join()
                if R==12:
                    CODE_NUM=12
                else:
                    CODE_NUM=13
        return CODE_NUM

    def download_request(self, filename):
        CODE_NUM=0
        my_protocol.dwld_bale_TCP(self.s,'',filename)
        # 等待接收
        data = my_protocol.unpake_TCP(self.s)
        if data != -1:
            if data[2] == '2':
                # print("文件在服务器里不存")
                CODE_NUM=2
            else:
                # 接收属性
                f_property = data[1]
                print(f_property)
                # 开辟新的线程，接收文件
                t = Thread(target=client_data_port.run, args=(
                    'd', self.data_socket, filename,self.set_data))
                t.start()
                t.join()
                if R==10:
                    CODE_NUM=10
                else:
                    CODE_NUM=11
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
    def quit_request(self):
        # 通过协议打包发送
        my_protocol.quit_bale_TCP(self.s)
        self.s.close()
        sys.exit()
        print("已退出")
