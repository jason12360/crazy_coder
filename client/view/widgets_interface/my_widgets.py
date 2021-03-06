import re
import os
import tkinter as tk
from tkinter import *
import tkinter.font as tkFont 


class Mybutton(tk.Label):
    def __init__(self,master,fun,**kwargs):
        super().__init__(master,kwargs)
        self.fun = fun
        self.config(fg = '#555555')
        self.config(bg = '#F8F8FF')
        self.bind('<Button-1>',self.fun_button1)
        self.bind('<ButtonRelease-1>',self.fun_br1)
        self.bind('<Enter>',self.fun_enter)
        self.bind('<Leave>',self.fun_leave)
    def fun_enter(self,event):
        self.config(bg = '#32CD32')
        self.config(fg = '#FFFFFF')
    def fun_leave(self,event):
        self.config(bg = '#F8F8FF')
        self.config(fg = '#555555')
    def fun_button1(self,event):
        self.config(relief = tk.SUNKEN)
        self.fun()
    def fun_br1(self,event):
        self.config(relief = tk.FLAT)

class Myentry(tk.Entry):
    def __init__(self,master,**kwargs):
        super().__init__(master,kwargs)
        self.config(highlightcolor = '#32CD32',highlightthickness = 2,bd = 0.5,relief = tk.FLAT,highlightbackground='#CCCCCC')
class MyPasswordEntry(Myentry):
    def __init__(self,master,**kwargs):
        super().__init__(master,**kwargs)
        self.config(show='*')
#继承此类,复写key方法,完成相应处理
class MySearchEntry(Myentry):

    def __init__(self, master, page, **kwargs):
        super().__init__(master, **kwargs)
        self.page = page
        self.bind('<KeyRelease>', self.key)

    def key(self, event):
        self.new_list = []
        self.keyrelease = self.get()
        print("键入结果：", self.keyrelease)
        for ii in self.page.get_file_list():
            if self.keyrelease in ii[0]:
                self.new_list.append(ii)
        for FL in self.page.FL:
            FL.destroy()
        self.page.files_display(self.new_list)



class Mybubble(Frame):
    def __init__(self,master,text,path,b_color,t_color,**kwargs):
        super().__init__(master,height=80,width=300,bg='#FFFFFF')
        self.pack_propagate(0)
        self.text = text
        #用于测试,如果主函数调用则,使用下方图片路径,非主函数条用使用上方图片路径
        photo = PhotoImage(file=path)
        self.image_lable = Label(self,image = photo,anchor=W,bg='#FFFFFF')
        self.image_lable.image = photo
        self.image_lable.place(relx = 0.5,rely = 0.5,anchor=CENTER)
        self.text_lable = Label(self,anchor=W)
        self.text_lable.config(bg=b_color,text = self.text,justify=LEFT,wraplength=230,padx=5,fg=t_color)
        self.text_lable.place(relx = 0.04,rely = 0,relwidth = 0.8,anchor = NW)

class Scrollabe_Frame(Canvas):
    def __init__(self,master,**kwargs):
        super().__init__(master,kwargs)
        self.width = 430
        frame=Frame(self,height=2000,width=self.width,bg='#FFFFFF')
        frame.pack_propagate(0) 
        vbar=Scrollbar(self,orient=VERTICAL) 
        vbar.pack(side=RIGHT, fill=Y)
        vbar.config(command=self.yview)
        self.config(yscrollcommand=vbar.set)  
        self.create_window((0,0), window=frame,anchor=NW)  #create_window
        self.frame =frame
        self.bar = vbar
    def flush(self):
        self.delete(self.frame)
        self.frame=Frame(self,height=2000,width=self.width,bg='#FFFFFF')
        self.create_window((0,0), window=self.frame,anchor=NW)
        self.bar.pack(side=RIGHT, fill=Y)



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
        self.s = Scrollabe_Frame(self,scrollregion=(0,0,400,2000))
        self.s.place(relx=0,rely=0,relwidth=1,relheight=0.7)
        self.t = Text(self,font=("微软雅黑",21))
        self.t.place(relx=0,rely=0.745,relwidth=1,relheight=0.28)
        b = Button(self,text = '发送  (S)',command=self.launch)
        b.place(relx=0,rely=0.952,relwidth=1,relheight=0.05)
    def setup(self,child_id,send_queue):
        self.child_pid= child_id
        self.send_queue = send_queue
    def show(self,text):
        if len(self.words)>19:
            self.words.pop(0)
        self.words.append(text)
        self.s.flush()
        self.position = 0
        step = 0.05
        for word in self.words:
            n = 0
            if word[0] in ['C','A','U','D']:
                Mybubble(self.s.frame,text=''.join(word[1:]),
                    path='view/widgets_interface/resources/bubble.gif',
                    b_color='#E2A2E4',t_color='#FFFFFF').place(x=0,y=self.position/step*100+20)
                self.position+=step
            elif word[0] == 'S':
                Mybubble(self.s.frame,text=''.join(word[1:]),
                    path='view/widgets_interface/resources/bubble3.gif',
                    b_color='#6CEF48',t_color='#555555').place(x=100,y=self.position/step*100+20)
                self.position+=step
        if self.position/step >5:
            self.s.yview_moveto(self.position-5*step)
    def launch(self):
        text = 'C '+self.t.get(1.0,END)
        self.send_queue.put(text)
        os.kill(self.child_pid,41)
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
        l = Label(self, text='这是主视图')
        l.pack()

class Scrollabe_Listbox(tk.Canvas):
    def __init__(self,master,_height=20000,**kwargs):
        super().__init__(master,kwargs)
        self.frame=tk.Frame(self,width=1000,height=_height)
        self.frame.pack_propagate(0) 
        self.bar=tk.Scrollbar(self,orient=tk.VERTICAL) 
        self.bar.config(command=self.yview)
        self.config(yscrollcommand=self.bar.set)     
        self.create_window((0,0), window=self.frame,anchor=tk.NW) 

    def flush(self):
        self.delete(self.frame)
        self.delete(self.bar)
        self.frame=tk.Frame(self)
        self.bar=tk.Scrollbar(self,orient=tk.VERTICAL)
        self.bar.config(command=self.yview)
        self.config(yscrollcommand=self.bar.set)
        self.create_window((0,0), window=self.frame,anchor=tk.NW)

class Mymenu(tk.Menu):
    def __init__(self, master, **kwargs):
        super().__init__(master, kwargs)

    def hotkey(self, whole):
        d = {}
        d[whole] = "Alt+"+re.findall("[A-Z]", whole)[0]
        return d

    def add_menu(self, cas_dic, menu_name):
        self.cascade = tk.Menu(self, tearoff=0)
        m = menu_name
        for k, v in cas_dic.items():
            self.cascade.add_separator()
            h = self.hotkey(k)[k]
            self.cascade.add_command(label=k, command=v, accelerator=h)
        self.add_cascade(label=m, menu=self.cascade,accelerator=self.hotkey(m)[m])



class ListItems(Frame):
    def __init__(self,master,color,widths,textlist):
        super().__init__(master)
        self.color=color
        self.config(width=1000,height=50,bg=color)
        self.config(highlightbackground='#CCCCCC',highlightthickness=1)
        self.pack_propagate(0)
        self.pack(anchor=NW)
        self.textlist=textlist
        self.labels=[]
        self.widths=iter(widths)
        self.create_labels()
        self.file_name = textlist[0]

    def bind_label(self,label):
        self.dwlabel = label
        self.bind('<Button-1>',self.dw)

    def dw(self,event):
        self.dwlabel.config(text=self.file_name)
        print(self.file_name)
        
    def actions(self):
        self.bind('<Enter>',self.selected)
        self.bind('<Leave>',self.leaved)
    def selected(self,event):
        self.config(bg='#EEEEEE')
        for label in self.labels:
            label.config(bg='#EEEEEE')
    def leaved(self,event):
        self.config(bg=self.color)
        for label in self.labels:
            label.config(bg=self.color)
    def create_labels(self):        
        for t in self.textlist:
            self.labels.append(Label(self,text=self.hide(t),width=next(self.widths)))
        for label in self.labels:
            label.config(anchor=W)
            label.config(bg=self.color)
            label.pack(side=LEFT,padx=10)
            label.bind('<Button-1>',self.dw)


    def hide(self,t):
        if '/' in t:
            ts= t.split("/")
            if len(ts)>3:
                return "/"+ts[1]+"/…/"+"/".join(ts[-2:])
        elif re.findall("^\d+$",t):
            t=int(t)
            if t<1024:
                return str(t)+"B"
            elif t<1024**2:
                K=str(round(t/1024,3))+"K"
                return K
            elif t<1024**3:
                M=str(round(t/1024**2,3))+"M"
                return M
            else:
                G=str(round(t/1024**3,3))+"G"
                return G
        return t









def fun1():
    print('hahahhah')
def main():
    top = tk.Tk()
    top.geometry('400x500')
    BIG_FONT = tkFont.Font(size = 20)
    se = MySearchEntry(top)
    se.pack()
    l = tk.Label(top,text = '用户名:',anchor = tk.W,width = 20,height =1,fg = '#555555')
    l.pack()
    e = Myentry(top)
    e.pack()
    e.focus_set()
    l = tk.Label(top,text = '密码:',anchor = tk.W,width = 20,height =1,fg = '#555555')
    l.pack()
    e = MyPasswordEntry(top)
    e.pack()
    b = Mybutton(top,fun1,text = '登录',width = 15,height =2)
    b.pack(pady = 10)
    s = Scrollabe_Frame(top,_width=400,_height=500
        ,scrollregion=(0,0,400,2500))
    s.pack()
    s.bar.pack(side=tk.RIGHT, fill=tk.Y)
    text_list = ['python.py','4kb','/tarena/home/aid1803/tt/s','2018-9-14 23:00:00','2018-9-14 23:00:00']

    for i in range(100):

        file_displayer.ListItems(s.frame,text_list)
    


    top.wm_title('菜单')
    top.mainloop()

if __name__ == '__main__':
    main()