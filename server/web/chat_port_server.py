from socket import *
def run():
    HOST = ''
    PORT = 18529
    global ADDR
    ADDR = (HOST, PORT)
    global s
    s = socket(AF_INET, SOCK_DGRAM)
    s.bind(ADDR)
    user = {}
    # 循环接收请求
    while True:
        msg, addr = s.recvfrom(1024)
        msg = msg.decode()
        print(msg)
        cmd = msg.split(' ')
        if cmd[0] == 'L':
            do_login(s, user, cmd[1], addr)
        elif cmd[0] == 'C':
            do_chat(s, user, cmd,addr)
        elif cmd[0] == 'Q':
            do_quit(s,user,cmd[1])
        else:
            s.sendto('请求错误'.encode(), addr)

def do_login(s, user, name, addr):
    msg = '\n欢迎 %s 进入聊天室' % name
    # 通知所有人
    for i in user:
        s.sendto(msg.encode(), user[i])
    # 将用户加入字典
    user[addr] = name
    return

# 实现群聊功能
def do_chat(s, user, cmd,addr):
    msg = '\n%-4s: %s' % (user[addr], ' '.join(cmd[1:]))
    # 发送给所有人除了自己
    for i in user:
        # if i != cmd[1]:
        s.sendto(msg.encode(), i)
    return

# 实现退出功能
def do_quit(s,user,name):
    del user[name]
    msg = '\n' + name +'离开了聊天室'
    for i in user:
        s.sendto(msg.encode(),user[i])
    return