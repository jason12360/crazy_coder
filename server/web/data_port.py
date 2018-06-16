import time
import sys,os
from socket import *
from file import *
import my_protocol
# 服务器文件夹
SYS_FIlE_PATH= "/home/tarena/ftp_web(2)/"
#上传路径
SYS_FIlE_PATH_O= "/home/tarena/ftp_base/"

def run(op,addr,f_property,ms):
    conn = socket()
    time.sleep(0.1)
    conn.connect(addr)
	#通过套接字做相应处理
    if op=='d':
        try:
            #路径选择
            op_path=SYS_FIlE_PATH+filename      
            with open(op_path,'rb') as f:
                while True:
                    data=f.read(1024)
                    if not data:
                        break 
                    conn.send(data)
        except Exception as E:
            print(E)
            #返回结果给进程
            CODE_NUM=11
            set_data(CODE_NUM)
        else:
            time.sleep(0.1)
            conn.send(b'@end')
            ask=conn.recv(1024,10)
            if ask==b'ok':
                print('用户接受完毕')
                CODE_NUM=10
                set_data(CODE_NUM)
            else:
                print('用户接受失败')
                CODE_NUM=11
                set_data(CODE_NUM)
        finally:
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
                    data=conn.recv(1024)
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
            ms.add_file(file)
            print('finish')
            conn.send(b'upld+ +ok+@end')
            #返回结果给进程
        finally:
             # #关闭套接字
            conn.close()
