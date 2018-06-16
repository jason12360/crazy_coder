'''
文件传输协议
包头关键字 list  upld  dwld  quit  chat
结构：请求类别+属性+内容+结束符
list +null+foldername+@end  
dwld+size+filename+@end
upld + size +filename+@end
chat+null+message+@end
quit+null+null+@end
'''
BUFFERSIZE=4096

from socket import *
#打包TC
def list_bale_TCP(conn,foldername):
    s='list+'+' '+'+'+foldername+'+@end'
    print(conn.getpeername())
    conn.send(s.encode())

def upld_bale_TCP(conn,f_property,filename):
    s='upld+'+f_property+'+'+filename+'+@end'
    conn.send(s.encode())

def dwld_bale_TCP(conn,f_property,filename):
    s='dwld+'+f_property+'+'+filename+'+@end'
    conn.send(s.encode())

def chat_bale_TCP(conn,message):
    s='chat+'+' '+'+'+message+'+@end'
    conn.send(s.encode())

def login_request(conn,admin,password):
    s='login+'+admin+'+'+password+'+@end'
    conn.send(s.encode())

def reg_request(conn,admin,password):
    s='reg+'+admin+'+'+password+'+@end'
    conn.send(s.encode())

def quit_bale_TCP(conn):
    s='quit+'+' '+'+'+' '+'+@end'
    # print(s)
    conn.send(s.encode())

#TCP解包
def unpake_TCP(connfd):
    #接收数据包
    data=connfd.recv(BUFFERSIZE).decode()
    #解释
    x=data.split('+')
    print(x)
    #判断头尾是否完整，不完整，则为丢包,完整就返回list
    #处理客户端意外退出，发送过来的b''字节🌟🌟🌟
    if x[0] in ['list','upld','dwld','chat','quit','login','reg']:
        if x[3]=='@end':
            return x
        else:
            print('数据丢包')
            connfd.send("请求失败，数据包丢失".encode())
            #不再往下选择功能
            return -1 
    elif x[0]=='':
            print("客户端意外退出")
            connfd.close()
            return -1           
    else:
        print('数据丢包')
        connfd.send("请求失败，数据包丢失".encode())
        return -1

#------------------------------------
#打包UDP
# def _bale_UDP(conn,data,addr):
#     s='list+'+str(len(data))+'+'+str(data)+'+@end'
#     conn.sendto(s.encode(),addr)

# #UDP解包
# def unpake_UDP(connfd):
#     #接收数据包
#     data,addr=connfd.recvfrom(BUFFERSIZE).decode()
#     #解释
#     x=data.split('+')
#     print(x)
#     #判断头尾是否完整，不完整，则为丢包,完整就返回list
#     if x[0] in ['list','upld','dwld','chat','quit']:
#         if x[3]=='@end':
#             #判断数据是否完整
#             if len(x[2])==int(x[1]):
#                 return x,addr
#             else:
#                 print('数据丢包')
#                 return -1
#         else:
#             print('数据丢包')
#             connfd.send("请求失败，数据包丢失".encode())
#             #不再往下选择功能
#             return -1            
#     else:
#         print('数据丢包')
#         connfd.send("请求失败，数据包丢失".encode())
#         return -1
  
