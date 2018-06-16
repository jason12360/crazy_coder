import time
import sys,os
from socket import *

import model.file
DATA_HOST = ''
DATA_PORT = 18528
DATA_ADDR = (DATA_HOST, DATA_PORT)
SYS_FIlE_PATH_U= ""
SYS_FIlE_PATH_D= "/home/tarena/ftp_web(2)/op/"
def run(op,_socket,filename,set_data):
    #等待服务端连接
    s,addr = _socket.accept()
    #通过套接字做相应处理
    if op=='u':
        try:
            #路径选择
            op_path=SYS_FIlE_PATH_U+filename      
            with open(op_path,'rb') as f:
                while True:
                    data=f.read(2048)
                    if not data:
                        break 
                    s.send(data)
        except Exception as E:
            print(E)
            #返回结果给进程
            CODE_NUM=13
            set_data(CODE_NUM)
        else:
            time.sleep(0.1)
            s.send(b'@end')
            ask = s.recv(1024)
            if ask==b'ok':
                print('上传成功')
                CODE_NUM=12
                set_data(CODE_NUM) 
            else:
                print('上传失败')
                CODE_NUM=13
                set_data(CODE_NUM)
    elif op=='d':
        try: 
            #接收文件(用户的下载)
            #路径选择
            op_path=SYS_FIlE_PATH_D+filename      
            with open(op_path,'wb') as f:
                while True:
                    data=s.recv(1024)
                    if data==b'@end':
                        break
                    f.write(data)
        except Exception as E:
            print(E)
            CODE_NUM=11
            set_data(CODE_NUM)
        else:
            time.sleep(0.1)
            #下载完成发送ok
            s.send(b'ok')
            print('下载完成')
            #返回结果给进程
            CODE_NUM=10
            set_data(CODE_NUM)
        # #关闭套接字

    s.close()
    
  



