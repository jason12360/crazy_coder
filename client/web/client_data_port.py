import time
import sys,os
from socket import *
import file
import my_protocol

# DATA_HOST = ''
# DATA_PORT = 18528
# DATA_ADDR = (DATA_HOST, DATA_PORT)
# SYS_FIlE_PATH_U= ""
# SYS_FIlE_PATH_D= "/home/tarena/ftp_web(2)/op/"
def run(op,data_addr,file,view_handeler):
    # TODO:创建TCP套接字,注意将端口设为0即让系统随机分配端口
    #为了防止服务器端端口被占用,所以需要不断产生套接字直到端口可使用为止
    data_socket = socket()
    data_socket.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    #客户端监听套接字
    data_socket.bind(data_addr)
    data_socket.listen(5)
    s,addr = data_socket.accept()
    #通过套接字做相应处理
    print('data_port connected from',addr)
    data_socket.close()
    if op=='u':
        try:
            #获取文件路径
            op_path=file.get_server_path()+'/'+file.get_name()
            total_size = int(file.get_size())
            current_size =0      
            with open(op_path,'rb') as f:
                while True:
                    data=f.read(4096)
                    if not data:
                        break 
                    s.send(data)
                    current_size +=len(data)
                    view_handeler.show_progress(current_size,total_size)
        except Exception as E:
            print(E)
            #如果出错向前端句柄返回错误码'14'
            CODE_NUM='14'
            view_handeler.do_message(CODE_NUM)
        else:
            #防止粘包
            time.sleep(0.1)
            s.send(b'upld+ + +@end')
            ask = my_protocol.unpake_TCP(s)[2]
            #print(ask)
            if ask=='ok':
                CODE_NUM='0'
                view_handeler.do_message(CODE_NUM,filename = file.get_name()) 
                view_handeler.do_list()
            else:
                print('上传失败')
                CODE_NUM="13"
                view_handeler.do_message(CODE_NUM)
        finally:
            s.close()
    elif op=='d':
        try: 
            #接收文件(用户的下载)
            #路径选择   
            with open(file,'wb') as f:
                while True:
                    data=s.recv(4096)
                    if data==b'@end':
                        break
                    f.write(data)
        except Exception as E:
            print(E)
            CODE_NUM='12'
            s.send(b'12')
            view_handeler.do_message(CODE_NUM)
        else:
            time.sleep(0.1)
            #下载完成发送ok
            s.send(b'ok')
            
            #返回结果给进程
        finally:
            CODE_NUM = s.recv(1024).decode()
            if CODE_NUM =='11':
                view_handeler.do_message(CODE_NUM)
            else:
                view_handeler.do_message('4',filename = file.split('/')[-1])
                # print('下载完成')
            s.close() 
        # #关闭套接字

    
    
  



