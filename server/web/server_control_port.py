from threading import Thread
from socket import *
import signal
from threading import Thread
import sys,os
import time
import data_port
import my_protocol
from file_folder import *
from database_handler import *

# 服务器文件夹
SYS_FIlE_PATH = "/home/tarena/ftp_web(2)/"

#上传路径
SYS_FIlE_PATH_O= "/home/tarena/ftp_web(2)/op/"

def run(myconnection, addr):
    # 把myconnection传给handler进行相关的登录操作
    # 以下为控制端函数
    get_command(myconnection,addr)



def get_command(connfd,addr):
    # 创建客户端通信对象
    c_ftp = MyFtp_Server(connfd,addr)
    while True:
        
        # 接受完的data判断是否丢包,进行解包处理
        l = my_protocol.unpake_TCP(connfd)

        # 客户端功能选择
        if l != -1:
            # l返回的结构：请求类别 + 属性 + 内容 + 结束符
            #             l[0]   l[1]   l[2]   l[3]
            if l[0] == 'list':
                c_ftp.list(l[2])
            elif l[0] == 'upld':
                c_ftp.receive(l[1], l[2])
            elif l[0] == 'dwld':
                c_ftp.send(l[1], l[2])
            elif l[0] == 'chat':
                # l[2] ismessage
                c_ftp.chat(l[2])
            elif l[0] == 'login':
                # l[1] 是账号
                # l[2] 是密码
                c_ftp.login(l[1], l[2])
            elif l[0]=='reg':
                c_ftp.register(l[1],l[2])
            elif l[0] == 'quit':
                c_ftp.quit()
        else:
            sys.exit(0)


class MyFtp_Server():
    '''
    MyFtp_server 有五个函数
    '''

    def __init__(self, conn,addr):

        self.client = conn
        self.addr=addr
        self.ms = My_Mysql()
    # 获取list
    #子线程给父进程传参用
    def set_data(self,v):
        global R
        R = v   

    def list(self, foldername):
        self.file_all = self.ms.select_all_files()
        # 请求服务器内的文件，整理和文件列表和属性列表
        data = self.file_all.pack()
        #发送整个服务器文件的属性列表给客户端,data以字符串的形式
        my_protocol.list_bale_TCP(self.client,str(data))       

    # 接受客户端下载请求，发送文件
    def send(self, f_property,filename):
        CODE_NUM=0
        # 如果需要上传下载,开辟新线程进行处理
        # 搜索系统是否有这个文件
        fd = self.ms.select_file_by_filename(filename)
        if fd == None:
            # 返回不存在的代码
            CODE_NUM='2'
            #属性为空，返回报错代码
            my_protocol.dwld_bale_TCP(self.client,'',CODE_NUM)
        else:
            my_protocol.upld_bale_TCP(self.client,'','go')
            #建立套接字
            DATA_HOST = self.addr[0]
            DATA_PORT = int(my_protocol.unpake_TCP(self.client)[2])
            DATA_ADDR = (DATA_HOST, DATA_PORT)
            t = Thread(target=data_port.run, args=('d', DATA_ADDR,filename,self.ms))
            t.start()
            #回发一个属性过去 
            # f_property=fd.pack()
            # print(f_property)
            # my_protocol.dwld_bale_TCP(self.client,str(f_property),'')
            # t.join()
            #TODO 判断用户是否下载成功，是---》添加日志
            #把用户的操作添加到数据库里的日志

            # if R==10:
            #     log=(self.addr,filename,time.strftime('%Y-%m-%d %H:%M:%S'),"下载")
            #     self.ms.add_userlog(log)
            #     #报错代码 10为下载成功 11为下载失败
            #     CODE_NUM=10
            # else:
            #     CODE_NUM=11 


    # 接受客户端上传请求，接收文件
    def receive(self, f_property,filename):
        #初始化错误码
        CODE_NUM=0
        # filename = os.path.split(filename)[-1]
        # 搜索系统是否有这个文件
        fd = self.ms.select_file_by_filename(filename)
        if fd == None:
            # 不存在,可以上传,给予客户端回应,客户端接收到此消息后,打开副线程进行主动连接,并回复
            #服务端相应端口号,用于数据通信
            my_protocol.upld_bale_TCP(self.client,'','go')
            DATA_HOST = self.addr[0]
            DATA_PORT = int(my_protocol.unpake_TCP(self.client)[2])
            DATA_ADDR = (DATA_HOST, DATA_PORT)
            
            t = Thread(target=data_port.run,args=('u',DATA_ADDR,f_property,self.ms))
            t.setDaemon(True)
            t.start()
            # #编写属性
            # op_file = SYS_FIlE_PATH+filename
            # up=File(filename,
            #         os.path.getsize(op_file),
            #         op_file,
            #         time.strftime('%Y-%m-%d %H:%M:%S'),
            #         time.strftime('%Y-%m-%d %H:%M:%S'))   
            # #添加到mysql
            # self.ms.add_file(up)
            # #TODO 判断用户是否下载成功，是---》添加日志
            # if R==12:
            #     #把用户的操作添加到数据库里的日志
            #     log=(self.addr,filename,time.strftime('%Y-%m-%d %H:%M:%S'),"上传")
            #     self_ms.add_userlog(log) 
            #      #报错代码 10为下载成功 11为下载失败
            #     CODE_NUM=12
            # else:
            #     CODE_NUM=13
            # Q.put(CODE_NUM)
            #chat进程  get就ok
   
        else:
            #文件已存在或重名(覆盖操作可以在这)
            # 返回不存在的代码
            CODE_NUM='3'
            #属性为空，返回报错代码
            my_protocol.upld_bale_TCP(self.client,'',CODE_NUM)
 

    # 登录
    def login(self, username, password):
        # 和mysql比对后返回
        result = self.ms.select_user(username)
        if not result:
            self.client.send(b'N')
        else: 
            if password == result[0][2]:
                self.username = username
                self.client.send(b'Y')
            else:
                self.client.send(b'N')
   
    def register(self,username,password):
        result = self.ms.select_user(username)
        if not result:
            self.ms.add_user(username,password)
            self.username = username
            self.client.send(b'Y')
        else:
            self.client.send(b'N')
    # 退出
    def quit(self):
        self.client.close()
        print("客户端退出")
        sys.exit(0)
