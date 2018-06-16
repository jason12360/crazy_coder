from tkinter import *
import client_control_port
import sys
class view():
    def __init__(self,server):
        self.server = server
        self.root = Tk()
        l = Label(self.root,text = '协议结构：请求类别 + 属性 + 内容 + 结束符')
        l.pack()
        e = Entry(self.root)
        self.e = e
        e.pack()
        b = Button(self.root,text = '提交',command=self.start)
        b.pack()
    def run(self):
        self.root.mainloop()

    def start(self):
        # print(self.e.get(),self.server)
        client_control_port.comment_handler(self.e.get(),self.server)
    
if __name__ == '__main__':
    c_ftp='c'
    view1 = view(c_ftp)
    view1.run()

            
