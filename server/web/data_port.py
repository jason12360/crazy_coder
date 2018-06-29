import time
import sys,os
from socket import *
from file import *
import my_protocol
from database_handler import *
# 服务器文件夹
SYS_FIlE_PATH= "/home/tarena/ftp_base/"
#上传路径
SYS_FIlE_PATH_O= "/home/tarena/ftp_base/"

def run(op,addr,f_property):
    conn = socket()
    time.sleep(0.1)
    conn.connect(addr)
	#通过套接字做相应处理
    if op=='d':
        try:
            #路径选择
            op_path=SYS_FIlE_PATH+f_property      
            with open(op_path,'rb') as f:
                while True:
                    data=f.read(4096)
                    if not data:
                        break 
                    conn.send(data)
        except Exception as E:
            print(E)
            #返回结果给进程
            CODE_NUM='11'
            # conn.send(b'upld+ +11+@end')
        else:
            time.sleep(0.1)
            conn.send(b'@end')
            ask=conn.recv(1024)
            if ask==b'ok':
                CODE_NUM='0'
                print('用户接受完毕')
            else:
                print('用户接受失败')
                CODE_NUM='11'
        finally:
            if CODE_NUM == '11':
                conn.send(b'11')
            else:
                conn.send(b'ok')
            conn.close()


    elif op=='u': 
        try:
            #接收文件到服务器
            #路径选择
            file = File()
            file.unpack(f_property)
            op_path=SYS_FIlE_PATH_O+file.get_name()
            file.set_server_path(op_path)      
            with open(op_path,'wb') as f:
                while True:
                    data=conn.recv(4096)
                    if data==b'upld+ + +@end':
                        break
                    f.write(data)
        except Exception as E:
            print(E)
            #如果发生错误则通知客户端服务器端发生错误
            conn.send(b'upld+ +13+@end')
        else:
            #没有发生错误,通知客户端发送成功
            time.sleep(0.1)
            #接收完成发送ok
            ms = My_Mysql()
            ms.add_file(file)
            ms.close()
            print('finish')
            conn.send(b'upld+ +ok+@end')
            #返回结果给进程
        finally:
             # #关闭套接字
            conn.close()
