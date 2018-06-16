# 分配两个进程,分别处理聊天与主要功能
# 第一个进程将使用tcp首先接收客户端连接请求,为客户端分配单独进程处理相应请求
# 第二个进程将使用udp进行聊天通信
from socket import *
from signal import *
from multiprocessing import Process,Queue
import signal
if __name__=='__main__':
    import web.server_control_port as server_control_port
    import web.chat_port_server as chat_port
else:
    import server_control_port
    import chat_port

#创建队列
Q=Queue(1)

# def server_control_port(myconnection, addr):
#     server_control_port.run(data_socket, myconnection, addr)


def control_port():
    # 建立登录和主要功能连接,端口号为xxx
    CTRL_HOST = ''
    CTRL_PORT = 18527
    CTRL_ADDR = (CTRL_HOST, CTRL_PORT)
    ctrl_socket = socket()
    ctrl_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    ctrl_socket.bind(CTRL_ADDR)
    ctrl_socket.listen(10)
    # TODO:创建TCP套接字
    # DATA_HOST = ''
    # DATA_PORT = 18528
    # DATA_ADDR = (DATA_HOST, DATA_PORT)
    # data_socket = socket()
    # data_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    # data_socket.bind(DATA_ADDR)
    # data_socket.listen(50)
    # data_socket.accept()
    print("等待连接")
    # 为不同的client分配不同的进程
    while True:
        myconnection, addr = ctrl_socket.accept()
        print('用户已登录',addr)
        process = Process(target=server_control_port.run,
                          args=(myconnection, addr))
        process.start()
    #
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
