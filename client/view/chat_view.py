from tkinter import *

class Mybubble(Frame):
    def __init__(self,master,text,**kwargs):
        super().__init__(master,height=80,width=300,bg='#FFFFFF')
        self.pack_propagate(0)
        self.text = text
        # self.pack(fill=X)
        #用于测试,如果主函数调用则,使用下方图片路径,非主函数条用使用上方图片路径
        if __name__ =='__main__':
            photo = PhotoImage(file='widgets_interface/resources/bubble.gif')
        else:
            photo = PhotoImage(file='view/widgets_interface/resources/bubble.gif')
        self.image_lable = Label(self,image = photo,anchor=W,bg='#FFFFFF')
        self.image_lable.image = photo
        self.image_lable.place(relx = 0.5,rely = 0.5,anchor=CENTER)
        self.text_lable = Label(self,anchor=W)
        self.text_lable.config(bg='#E2A2E4',text = self.text,justify=LEFT,wraplength=230,padx=5,fg='#FFFFFF')
        self.text_lable.place(relx = 0.04,rely = 0,relwidth = 0.8,anchor = NW)

class Scrollabe_Frame(Canvas):
    def __init__(self,master,**kwargs):
        super().__init__(master,kwargs)
        # self.pack_propagate(0)
        self.width = 1000
        frame=Frame(self,height=2000,width=self.width,bg='#FFFFFF')
        frame.pack_propagate(0) 
        vbar=Scrollbar(self,orient=VERTICAL) #竖直滚动条
        vbar.pack(side=RIGHT, fill=Y)
        vbar.config(command=self.yview)
        self.config(yscrollcommand=vbar.set) #设置  
        
        self.create_window((0,0), window=frame,anchor=NW)  #create_window
        self.frame =frame
        self.bar = vbar
    def flush(self):
        self.delete(self.frame)
        self.frame=Frame(self,height=2000,width=self.width,bg='#FFFFFF')
        self.create_window((0,0), window=self.frame,anchor=NW)


class ChatView(Frame):
    def __init__(self, parent,**kwargs):
        self.parent = parent
        super().__init__(parent,kwargs)
        self.config(bd=1)
        # self.pack_propagate(0)
        # self.width = self.cget('width')
        # self.height = self.cget('height')
        self.display()
        self.words = []

    def display(self):
        '''
        用来画聊天试图
        '''
        self.s = Scrollabe_Frame(self,scrollregion=(0,0,400,2000))
        self.s.place(relx=0,rely=0,relwidth=1,relheight=0.7)
        self.t = Text(self)
        self.t.place(relx=0,rely=0.7,relwidth=1,relheight=0.2)
        # self.s.yview_moveto(1.0)
        b = Button(self,text = '发送',command=self.launch)
        b.place(relx=0,rely=0.9,relwidth=1,relheight=0.1)
    def launch(self):
        if len(self.words)>19:
            self.words.pop(0)
        self.words.append(self.t.get(1.0,END))
        self.s.flush()
        self.position = 0
        step = 0.05
        for word in self.words:
            Mybubble(self.s.frame,text=word).pack(pady=10)
            self.position+=step
        if self.position/step >5:
            self.s.yview_moveto(self.position-5*step)
        self.t.delete(1.0,END)
    	


class MainView(Frame):
    def __init__(self, parent):
        self.parent = parent
        super().__init__(parent)
        self.config(width=800, height=900, bd=1, bg='#FFFFFF')
        self.pack(side=RIGHT)
        self.pack_propagate(0)
        self.display()

    def display(self):
        '''
        用来画聊天试图
        '''
        l = Label(self, text='这是主视图')
        l.pack()

if __name__=='__main__':
    root = Tk()
    root.geometry('1200x900')
    root.resizable(width=False, height=True)
    main_view = MainView(root)


    chat_view = ChatView(root)
    chat_view.place(relx=0,rely=0,relwidth=0.4,relheight=1,anchor=NW)

    root.mainloop()
