import os
import sys
import re
import time
# if sys.version_info[0] == 2:
#     from Tkinter import *
#     from tkFont import Font
#     from ttk import *
#     #Usage:showinfo/warning/error,askquestion/okcancel/yesno/retrycancel
#     from tkMessageBox import *
#     #Usage:f=tkFileDialog.askopenfilename(initialdir='E:/Python')
#     #import tkFileDialog
#     #import tkSimpleDialog
# else:  #Python 3.x
from tkinter import *
import tkinter as tk
from tkinter import PhotoImage
from tkinter.font import Font
from tkinter.ttk import *
import tkinter.filedialog
from tkinter import messagebox

if __name__=='__main__':
    from widgets_interface.my_widgets import *

else:
    from view.widgets_interface.my_widgets import *

# import tkinter.simpledialog as tkSimpleDialog   #askstring()






def show_dw_filedialog(aaa):
    fileN = tkinter.filedialog.askdirectory(
        filetypes=[("py格式", ".py")])
    print(fileN)
    return fileN
def show_ask_filedialog():
    fileN = tkinter.filedialog.askdirectory(filetypes=[("py格式", ".py")])
    print(fileN)
    return fileN
# def show_error(string)



place_json={
    "TabStrip":{"relx":0.03, "rely":0.05,"relwidth":0.528, "relheight":0.55},
    "Tab_title":{"relx":0.004, "rely":0, "relwidth":1, "relheight":0.19},
    "Tab_frame":{"relx":0.2, "rely":0.893, "relwidth":0.6, "relheight":0.1},
    "Tab_label":{"relx":0.035, "rely":0.884, "relwidth":0.16, "relheight":0.12},
    "Tab_listbox":{"relx":0.003,"rely":0.115,"relwidth":0.98,"relheight":0.7},
    "Tab_scroll":{"relx":0.98, "rely":0, "relwidth":0.02, "relheight":1},
    "Online_listbox":{"relx":0.37,"rely":0.65,"relwidth":0.188,"relheight":0.337},
    "Online_scroll":{"relx":0.93, "rely":0, "relwidth":0.068, "relheight":1},
    "Combox":{"relx":0.03, "rely":0.9, "relwidth":0.25, "relheight":0.07},
    "Frame":{
        '': {"relx": 0.063, "rely": 0.655, "relwidth": 0.204, "relheight": 0.065},
        '上传文件': {"relx": 0.03, "rely": 0.618, "relwidth": 0.314, "relheight": 0.369},
        '聊天区': {"relx": 0.603, "rely": 0.02, "relwidth": 0.382, "relheight": 0.967}
        },
    "Button":{
        '浏览 (V)': {"relx": 0.274, "rely": 0.666, "relwidth": 0.06, "relheight": 0.045},
        '上传 (U)': {"relx": 0.274, "rely": 0.927, "relwidth": 0.06, "relheight": 0.045},
        #'撤回(Z)': {"relx": 0.83, "rely": 0.927, "relwidth": 0.06, "relheight": 0.045},
        #'发送(S)': {"relx": 0.91, "rely": 0.927, "relwidth": 0.06, "relheight": 0.045}
        },
    '下载 (D)': {"relx":0.85, "rely":0.89, "relwidth":0.12, "relheight":0.1},
        '导出选中日志(L)…':{"relx":0.35, "rely":0.9, "relwidth":0.22, "relheight":0.07},
    "Search":{"relx":0.368, "rely":0.028, "relwidth":0.19, "relheight":0.046},
    "Chat":{"relx":0.618,"rely":0.062,"relwidth":0.352,"relheight":0.92},
    "Radio":{
        "显示所有":{"relx":0.23, "rely":0.028, "relwidth":0.064, "relheight":0.042},
        "模糊匹配":{"relx":0.3,"rely":0.029, "relwidth":0.064, "relheight":0.042}
        },
    "Img1":{"relx":0.036, "rely":0.666, "relwidth":0.015, "relheight":0.029},
    "Up_Label":{"relx":0.065, "rely":0.665, "relwidth":0.185, "relheight":0.040},
    "Down_Label":{"relx":0.21, "rely":0.91, "relwidth":0.55, "relheight":0.07},
    "Logout_Label":{"relx":0.55, "rely":0.884, "relwidth":0.4, "relheight":0.12},
    "Up_line0":{"relx":0.367, "rely":0.614, "relwidth":0.15, "relheight":0.029},
    "Up_line1":{"relx":0.035, "rely":0.725, "relwidth":0.242, "relheight":0.040},
    "Up_line2":{"relx":0.035, "rely":0.768, "relwidth":0.242, "relheight":0.040},
    "Up_line3":{"relx":0.035, "rely":0.811, "relwidth":0.242, "relheight":0.040},
    "Up_line4":{"relx":0.035, "rely":0.865, "relwidth":0.242, "relheight":0.040},
    "Up_line5":{"relx":0.035, "rely":0.925, "relwidth":0.142, "relheight":0.040}
}



class MyGUI(Frame):
    # 这个类仅实现界面生成功能，具体事件处理代码在子类Application中。
    def __init__(self, master,place_dic,**kwargs):
        Frame.__init__(self, master)
        self.top = self.winfo_toplevel()
        self.dic=place_dic
        self.button_dic={}
        self.createNotebook()      
        self.createTab1(self.Tab1)
        self.createTab2(self.Tab2)
        self.createLableFrame()
        self.createButton()
        self.createSearch()
        self.createRadio()
        self.createChat()
        self.createOnline()
        self.createImg()
        self.createLabel()


    def createNotebook(self):
        self.style = Style()
        self.TabStrip = Notebook(self.top)
        self.TabStrip.place(**self.dic["TabStrip"])
        T=['      服务器文件仓储      ','      用户操作记录      ']
        Tabs=[]
        width = float(self.TabStrip.cget('width'))
        for t in range(len(T)):
            Tabs.append(Frame(self.TabStrip,width=width))
            self.TabStrip.add(Tabs[t], text=T[t])
            Tabs[t].title=Scrollabe_Listbox(Tabs[t])
            Tabs[t].title.place(**self.dic["Tab_title"])
            Tabs[t].lbox=Scrollabe_Listbox(Tabs[t])
            Tabs[t].lbox.place(**self.dic["Tab_listbox"])
        self.Tab1,self.Tab2=Tabs

 
    def createTab1(self,master):     
        self.Tab1.fr = LabelFrame(master)
        self.Tab1.fr.place(**self.dic["Tab_frame"])
        self.dwlabel = Label(master)
        self.dwlabel.place(**self.dic["Down_Label"])
        self.Tab1.lb = Label(master,text="已选择文件：")
        self.Tab1.lb.place(**self.dic["Tab_label"])
        self.Tab1.bt = Mybutton(master,self.undefined,text="下载 (D)")
        self.button_dic["下载 (D)"]=self.Tab1.bt
        self.Tab1.bt.place(**self.dic["下载 (D)"])
        
    def createTab2(self,master):    
        self.Tab2.bt=Mybutton(master,self.undefined,text="导出选中日志(L)…")
        self.button_dic["导出选中日志(L)…"]=self.Tab2.bt
        self.Tab2.bt.place(**self.dic['导出选中日志(L)…'])
        self.combox=self.createCombox(master)
        self.combox.place(**self.dic["Combox"])
        self.logoutlabel = Label(master)
        self.logoutlabel.place(**self.dic["Logout_Label"])
        
    def createLableFrame(self):
        for k, v in self.dic["Frame"].items():
            fr = LabelFrame(self.top, text=k)
            fr.place(**v)

    def createButton(self):
        for k, v in self.dic["Button"].items():
            self.button = Mybutton(self.top,self.undefined, text=k)
            self.button_dic[k]=self.button
            self.button.place(**v)

    def createSearch(self):
        self.search = Myentry(self.top)
        self.search.place(**self.dic["Search"])

    def createChat(self):
        self.chat_view = ChatView(self.top)
        self.chat_view.place(**self.dic["Chat"])
        

    def createImg(self):
        self.img1 = Label(self.top, text="图")
        self.img1.place(**self.dic["Img1"])
        LabelFrame(self.top, text="").place(**self.dic["Frame"][""])

    def createRadio(self):
        self.v = IntVar()
        self.v.set(1)
        self.r1 = Radiobutton(self.top, 
            variable=self.v, text="显示所有", value=1)
        self.r1.place(**self.dic["Radio"]["显示所有"])
        self.r2 = Radiobutton(self.top, 
            variable=self.v, text="模糊匹配", value=2)
        self.r2.place(**self.dic["Radio"]["模糊匹配"])
    
    def createOnline(self):
        self.lbox2=self.createScrollbox(self.top)
        self.lbox2.place(**self.dic["Online_listbox"])
        self.lbox2.scrollbar.place(**self.dic["Online_scroll"])

    def createLabel(self):
        self.uplabel = Label(self.top)
        self.uplabel.place(**self.dic["Up_Label"])
        L=[]
        for i in range(6):
            L.append(Label(self.top,anchor=W))
            L[i].place(**self.dic["Up_line"+str(i)])
        self.upline0,self.upline1,self.upline2,\
            self.upline3,self.upline4,self.upline5=L

    def createScrollbox(self,master):
        listbox=Listbox(master, selectmode=EXTENDED)
        listbox.scrollbar = Scrollbar(listbox, orient=VERTICAL)
        listbox.config(yscrollcommand=listbox.scrollbar.set)
        listbox.scrollbar.config(command=listbox.yview)
        return listbox
    
    def createCombox(self,master):
        comvalue=tkinter.StringVar() 
        comboxlist=tkinter.ttk.Combobox(master,textvariable=comvalue)
        return comboxlist

    def undefined(self):
        print("undefined")


class Application(MyGUI):
    # 这个类实现具体的事件处理回调函数。界面生成代码在Application_ui中。
    def __init__(self, **kwargs):
        self.root = tk.Tk()
        self.root.geometry("1280x800")
        self.root.title("疯狂码头")
        self.root.resizable(True, True)

        MyGUI.__init__(self, self.root,place_json,**kwargs)
        

        Button_fun={'浏览 (V)': self.ready_up, 
                '上传 (U)': self.upload,'下载 (D)':self.download,
                "导出选中日志(L)…":self.logout }
        Menu_fun={
            "文件(F)": {'上传本地文件  (Upload)': self.upload,
                  '下载文件到本地  (Dwload)':self.download, "退出  (Quit)": self.hello},
            "查看(V)": {"查看用户信息  (Info))": self.hello,
                  "查看用户登录日志  (Log)": self.hello, '查看文件详情  (Content)': self.hello},
            "界面设置(S)": {"更换壁纸  (W)": self.hello, "字体设置  (P)": self.hello,
                  "进度条样式(Y)": self.hello, "关于 (A)": self.help_about}
            }


  
        self.button_bind(Button_fun)
        self.menu_bind(Menu_fun)
        self.combox_bind()        

        self.uplabel.config(text="＊＊当前未选择任何文件上传＊＊")
        self.upline0.config(text="在线用户列表")
        

        self.upline3.config(text="第三行")
        self.upline4.config(text=chr(9989)+chr(9993)+"bfdbdf进度条进度条进度条进度条进度条进度条进度条进20%")
        self.upline5.config(text="上传完毕!!!")
        
        

        '''file_SQL=[
             ["file.py","2048","2018-01-01 07:22:22","2018-01-01 07:22:22","/home/tarena/lwh/my_ftp/file.py"],
             ["mysql_test.py","196","2018-03-06 11:42:13","2018-01-01 07:22:22","/home/tarena/lwh/my_ftp/mysql_test.py"],
             ["my_protocol.py","744","2018-02-27 22:20:37","2018-01-01 07:22:22","/home/tarena/lwh/my_ftp/my_protocol.py"],
             ["test_view.py","611","2018-05-06 01:02:58","2018-01-01 07:22:22","/home/tarena/lwh/my_ftp/upload/test_view.py"],
             ["server_class.py","690","2018-01-31 19:54:02","2018-01-01 07:22:22","/home/tarena/lwh/my_ftp/upload/server_class.py"],
             ["filefolder.py","387","2018-03-14 15:19:26","2018-01-01 07:22:22","/home/tarena/lwh/my_ftp/upload/filefolder.py"],
              ["file.py","2048","2018-01-01 07:22:22","2018-01-01 07:22:22","/home/tarena/lwh/my_ftp/file.py"],
             ["mysql_test.py","196","2018-03-06 11:42:13","2018-01-01 07:22:22","/home/tarena/lwh/my_ftp/mysql_test.py"],
             ["my_protocol.py","744","2018-02-27 22:20:37","2018-01-01 07:22:22","/home/tarena/lwh/my_ftp/my_protocol.py"],
         ]'''

        log_SQL=[
            ["3306","20148","up","2018-01-01 07:22:22","/home/tarena/lwh/my_ftp/file.py"],
            ["9999","1910106","down","2018-01-01 07:22:22","/home/tarena/lwh/my_ftp/mysql_test.py"],
            ["4444","744","down","2018-01-01 07:22:22","/home/tarena/lwh/my_ftp/my_protocol.py"],
            ["4156","611","up","2018-01-01 07:22:22","/home/tarena/lwh/my_ftp/upload/test_view.py"],
            ["8462","690","up","2018-01-01 07:22:22","/home/tarena/lwh/my_ftp/upload/server_class.py"],
            ["2983","387","down","2018-01-01 07:22:22","/home/tarena/lwh/my_ftp/upload/filefolder.py"],
            ["3306","20148","up","2018-01-01 07:22:22","/home/tarena/lwh/my_ftp/file.py"],
            ["9999","1910106","down","2018-01-01 07:22:22","/home/tarena/lwh/my_ftp/mysql_test.py"],
            ["4444","744","down","2018-01-01 07:22:22","/home/tarena/lwh/my_ftp/my_protocol.py"],
            ["4156","611","up","2018-01-01 07:22:22","/home/tarena/lwh/my_ftp/upload/test_view.py"],
            ["8462","690","up","2018-01-01 07:22:22","/home/tarena/lwh/my_ftp/upload/server_class.py"],
            ["2983","387","down","2018-01-01 07:22:22","/home/tarena/lwh/my_ftp/upload/filefolder.py"]
        
        ]
        # self.files_display(file_SQL)
        self.logs_display(log_SQL)
      
        user_online=[["用户"+str(iii),"172.16.122."+str(iii)] for iii in range(1,100)]
        self.user_display(self.lbox2,user_online)

    def menu_bind(self,Menu_fun):
        menubar = Mymenu(self.top)
        for k, v in Menu_fun.items():
            menubar.add_menu(v, k)
        self.top['menu'] = menubar
    def button_bind(self,Button_fun):
        for k,v in Button_fun.items():
            self.button_dic[k].bind('<Button-1>',v)

    def combox_bind(self):
        log_type=(
            "       以  .py  格式文件",
            "       以  .txt  格式文件",
            "       以  .html  格式文件")
        self.combox["values"]=(log_type)  
        self.combox.current(0)  #选择第一个  
        self.combox.bind("<<ComboboxSelected>>",self.logselect)  

    def files_display(self,files_list):
        widths=[15,7,20,20,40]
        title1=["文件名","大小","修改时间","创建时间","储存路径"]
        ListItems(self.Tab1.title.frame,"#DDDDDD",widths,title1)
        self.Tab1.lbox.config(scrollregion=(0,0,1200,50*len(files_list)))
        self.Tab1.lbox.flush()
        self.Tab1.lbox.bar.place(**self.dic["Tab_scroll"])
        self.FL=[]
        for file in files_list:
            self.FL.append(ListItems(self.Tab1.lbox.frame,'#FFFFFF',widths,file))   
        for FL in self.FL:
            FL.bind_label(self.dwlabel)
            FL.actions()
    def logs_display(self,logs_list):
        widths=[13,7,7,17,40]
        title2=["用户名","文件名","操作类型","操作时间","储存路径"]
        ListItems(self.Tab2.title.frame,"#DDDDDD",widths,title2)
        self.Tab2.lbox.config(scrollregion=(0,0,1200,50*len(logs_list)))
        self.Tab2.lbox.flush()
        self.Tab2.lbox.bar.place(**self.dic["Tab_scroll"])
        for log in logs_list:
            ListItems(self.Tab2.lbox.frame,'#DDDDDD',widths,log).actions()
    def user_display(self,lbox,onlinelist):
        for fs in onlinelist:
            fs="{0:15}   ({1!s:^})".format(*fs)            
            lbox.insert(END,fs)
            lbox.bind("<Button-1>", self.searchuser) 
            lbox.select_set(onlinelist.index(onlinelist[0]))
            lbox.see(onlinelist.index(onlinelist[0]))
    def searchuser(self,event):
        self.search.get("2")
        #print(self.search)
    def logselect(self,event):
        print(self.combox.current)

    def logout(self,event):
        print("logout")
        self.logoutlabel.config(text="成功导出日志至路径……")
    def ready_up(self,event):
        self.upName = tkinter.filedialog.askopenfilename(
            initialdir=os.path.abspath("fyc_version5"),
            filetypes=[("py格式", ".py")])
        self.uplabel.config(text=self.upName)
        self.upsize=os.path.getsize(self.upName)
        self.upline1.config(text="文件大小:    "+str(self.upsize))
        aaaa=time.ctime(os.path.getmtime(self.upName))
        self.upline2.config(text="最后修改时间:    "+aaaa)
    def upload(self,event):
        self.uplabel.config(text="正在执行上传操作……")
        self.upline1.config(text="正在上传:    "+self.upName)
        for i in range(6):
            each=self.upsize/5
            self.upline2.config(text="已上传:    "+str(each*i)+"/"+str(self.upsize))
    def hello(self):
        print("未绑定")

    def download(self,event):
        self.dwName=tkinter.filedialog.askdirectory()
        print(self.dwName)
    def help_about(self):
        about='''
        团队：疯狂码头
        成员: 张晋 李文辉 方毅超 刘章杰
                    谭锐锋 谭永权 杨凌枫
        verion 1.0
        感谢您的使用！
        ©2018 ''' 
        messagebox.showinfo('关于', about)  
    def run(self):    
        self.root.mainloop()
    def close(self):
        pass
    def show_error_message(self,e):
        messagebox.showerror(
                '您的操作状态',
                e)
    def show_message(self,e):
        messagebox.showinfo(
                '您的操作状态',
                e)
    

if __name__=="__main__":
    Application().run()


