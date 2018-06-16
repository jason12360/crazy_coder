# 分配两个进程,分别处理聊天与主要功能
# 第一个进程将使用tcp首先接收客户端连接请求,为客户端分配单独进程处理相应请求
# 第二个进程将使用udp进行聊天通信
from socket import *
import signal
from multiprocessing import Process,Queue
import web.client_control_port as client_control_port
import web.chat_port_client as chat_port_client

#创建队列
Q=Queue(1)
# def client_control_port(control_socket, data_socket):
#     client_control_port.run(data_socket, ctrl_socket)

# def client_control_port(control_socket, data_socket):
#     client_control_port.run(data_socket, ctrl_socket)


def control_port():
    # 建立登录和主要功能连接,端口号为xxx
    CTRL_HOST = ''
    CTRL_PORT = 18527
    CTRL_ADDR = (CTRL_HOST, CTRL_PORT)
    ctrl_socket = socket()
    ctrl_socket.connect(CTRL_ADDR)
    # TODO:创建TCP套接字
    DATA_HOST = ''
    DATA_PORT = 18528
    DATA_ADDR = (DATA_HOST, DATA_PORT)
    data_socket = socket()
    data_socket.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    #客户端监听套接字
    data_socket.bind(DATA_ADDR)
    data_socket.listen(10)
    # data_socket.connect(DATA_ADDR)
    #功能选择
    client_control_port.run(ctrl_socket, data_socket)

# 当用户成功登录后,分配进程用来处理聊天,聊天将为群聊,故使用udp协议	
 

def main():
    # 设置父进程信号处理僵尸进程
    # TODO
    signal.signal(signal.SIGCHLD, signal.SIG_IGN)
    t1 = Process(target=control_port)
    # t2 = Process(target=chat_port)
    t1.start()
    # t2.start()

if __name__ == '__main__':
	main()



