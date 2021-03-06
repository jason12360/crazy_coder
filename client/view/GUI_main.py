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
from my_widgets import *


place_json={
    "TabStrip":{"relx":0.03, "rely":0.05,"relwidth":0.528, "relheight":0.55},
    "Tab_title":{"relx":0.004, "rely":0, "relwidth":1, "relheight":0.19},
    "Tab_frame":{"relx":0.2, "rely":0.893, "relwidth":0.4, "relheight":0.1},
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
    '刷新 (X)':{"relx":0.68, "rely":0.89, "relwidth":0.12, "relheight":0.1},
    "Search":{"relx":0.368, "rely":0.028, "relwidth":0.19, "relheight":0.046},
    "Chat":{"relx":0.618,"rely":0.062,"relwidth":0.352,"relheight":0.92},
    "Radio":{
        "显示所有":{"relx":0.23, "rely":0.028, "relwidth":0.064, "relheight":0.042},
        "模糊匹配":{"relx":0.3,"rely":0.029, "relwidth":0.064, "relheight":0.042}
        },
    "Img1":{"relx":0.036, "rely":0.666, "relwidth":0.015, "relheight":0.029},
    "Up_Label":{"relx":0.065, "rely":0.665, "relwidth":0.185, "relheight":0.040},
    "Down_Label":{"relx":0.21, "rely":0.91, "relwidth":0.3, "relheight":0.07},
    "Logout_Label":{"relx":0.55, "rely":0.884, "relwidth":0.4, "relheight":0.12},
    "Up_line0":{"relx":0.367, "rely":0.614, "relwidth":0.15, "relheight":0.029},
    "Up_line1":{"relx":0.035, "rely":0.740, "relwidth":0.249, "relheight":0.040},
    "Up_line2":{"relx":0.035, "rely":0.798, "relwidth":0.242, "relheight":0.040},
    "Up_line3":{"relx":0.035, "rely":0.931, "relwidth":0.142, "relheight":0.045},
    "Up_line4":{"relx":0.035, "rely":0.865, "relwidth":0.242, "relheight":0.040},
    "Up_line5":{"relx":0.291, "rely":0.865, "relwidth":0.042, "relheight":0.040}
}


class MyGUI(Frame):

    # 这个类仅实现界面生成功能，具体事件处理代码在子类Application中。
    def __init__(self, master, place_dic, **kwargs):
        Frame.__init__(self, master)
        self.top = self.winfo_toplevel()
        self.dic = place_dic
        self.button_dic = {}
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
        T = ['      服务器文件仓储      ',
             '      用户操作记录      ']
        Tabs = []
        width = float(self.TabStrip.cget('width'))
        for t in range(len(T)):
            Tabs.append(Frame(self.TabStrip, width=width))
            self.TabStrip.add(Tabs[t], text=T[t])
            Tabs[t].title = Scrollabe_Listbox(Tabs[t])
            Tabs[t].title.place(**self.dic["Tab_title"])
            Tabs[t].lbox = Scrollabe_Listbox(Tabs[t])
            Tabs[t].lbox.place(**self.dic["Tab_listbox"])
        self.Tab1, self.Tab2 = Tabs

    def createTab1(self, master):
        self.Tab1.fr = LabelFrame(master)
        self.Tab1.fr.place(**self.dic["Tab_frame"])
        self.dwlabel = Label(master)
        self.dwlabel.place(**self.dic["Down_Label"])
        self.Tab1.lb = Label(master, text="已选择文件：")
        self.Tab1.lb.place(**self.dic["Tab_label"])
        self.Tab1.bt = Mybutton(master, self.undefined, text="下载 (D)")
        self.button_dic["下载 (D)"] = self.Tab1.bt
        self.Tab1.bt.place(**self.dic["下载 (D)"])
        self.Tab1.bt2 = Mybutton(master, self.undefined, text="刷新 (X)")
        self.button_dic["刷新 (X)"] = self.Tab1.bt2
        self.Tab1.bt2.place(**self.dic["刷新 (X)"])

    def createTab2(self, master):
        self.Tab2.bt = Mybutton(master, self.undefined, text="导出选中日志(L)…")
        self.button_dic["导出选中日志(L)…"] = self.Tab2.bt
        self.Tab2.bt.place(**self.dic['导出选中日志(L)…'])
        self.combox = self.createCombox(master)
        self.combox.place(**self.dic["Combox"])
        self.logoutlabel = Label(master)
        self.logoutlabel.place(**self.dic["Logout_Label"])

    def createLableFrame(self):
        for k, v in self.dic["Frame"].items():
            fr = LabelFrame(self.top, text=k)
            fr.place(**v)

    def createButton(self):
        for k, v in self.dic["Button"].items():
            self.button = Mybutton(self.top, self.undefined, text=k)
            self.button_dic[k] = self.button
            self.button.place(**v)

    def createSearch(self):
        self.search = MySearchEntry(self.top, self)
        self.search.place(**self.dic["Search"])

    def createChat(self):
        self.chat_view = ChatView(self.top)
        self.chat_view.place(**self.dic["Chat"])

    def createImg(self):
        self.img1 = Label(self.top, text=chr(9875), font=("微软雅黑", 18))
        self.img1.place(**self.dic["Img1"])
        LabelFrame(self.top, text="").place(**self.dic["Frame"][""])

    def createRadio(self):
        self.v = IntVar()
        self.v.set(1)
        self.r1 = Radiobutton(
            self.top, variable=self.v, text="显示所有", value=1)
        self.r1.place(**self.dic["Radio"]["显示所有"])
        self.r2 = Radiobutton(
            self.top, variable=self.v, text="模糊匹配", value=2)
        self.r2.place(**self.dic["Radio"]["模糊匹配"])

    def createOnline(self):
        self.lbox2 = self.createScrollbox(self.top)
        self.lbox2.place(**self.dic["Online_listbox"])
        self.lbox2.scrollbar.place(**self.dic["Online_scroll"])

    def createLabel(self):
        self.uplabel = Label(self.top)
        self.uplabel.place(**self.dic["Up_Label"])
        L = []
        for i in range(6):
            L.append(Label(self.top, anchor=W))
            L[i].place(**self.dic["Up_line" + str(i)])
        self.upline0, self.upline1, self.upline2,\
            self.upline3, self.upline4, self.upline5 = L

    def createScrollbox(self, master):
        listbox = Listbox(master, selectmode=EXTENDED)
        listbox.scrollbar = Scrollbar(listbox, orient=VERTICAL)
        listbox.config(yscrollcommand=listbox.scrollbar.set)
        listbox.scrollbar.config(command=listbox.yview)
        return listbox

    def createCombox(self, master):
        comvalue = tkinter.StringVar()
        comboxlist = tkinter.ttk.Combobox(master, textvariable=comvalue)
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
        MyGUI.__init__(self, self.root, place_json, **kwargs)

        Button_fun = {'浏览 (V)': self.ready_up,
                      '上传 (U)': self.upload,
                      '下载 (D)': self.download,
                      "导出选中日志(L)…": self.logout,
                      '刷新 (X)': self.refresh}
        Menu_fun = [
            {"文件(F)": {
                '上传本地文件  (Upload)': self.upload,
                '下载文件到本地  (Dwload)': self.download,
                "退出  (Quit)": self.hello}},
            {"查看(W)": {
                "查看用户信息  (Info)": self.hello,
                "导出用户登录日志  (Log)": self.hello,
                '查看文件详情  (Content)': self.hello}},
            {"界面设置(J)": {
                "更换气泡  (Bubble)": self.hello,
                "字体设置  (fonTs)": self.hello,
                "进度条样式(Probar)": self.hello,
                "关于  (About)": self.help_about}}
        ]

        self.button_bind(Button_fun)
        self.menu_bind(Menu_fun)
        self.combox_bind()
        self.up_queue = []
        self.uplabel.config(text="＊＊当前未选择任何文件上传＊＊")
        self.upline0.config(text="在线用户列表")
        self.upline1.config(text="", font=("微软雅黑", 12))
        self.upline2.config(text="        可以支持同时多下载和上传", font=("微软雅黑", 12))
        self.upline3.config(text="上传队列无上传任务", font=("微软雅黑", 12))

    def menu_bind(self, Menu_fun):
        menubar = Mymenu(self.top)
        for q in range(len(Menu_fun)):
            for k, v in Menu_fun[q].items():
                menubar.add_menu(v, k)
        self.top['menu'] = menubar

    def button_bind(self, Button_fun):
        for k, v in Button_fun.items():
            self.button_dic[k].bind('<Button-1>', v)

    def combox_bind(self):
        log_type = (
            "       以  .py  格式文件",
            "       以  .txt  格式文件",
            "       以  .html  格式文件")
        self.combox["values"] = (log_type)
        self.combox.current(0)
        self.combox.bind("<<ComboboxSelected>>", self.logselect)

    def files_display(self, files_list):
        widths = [15, 9, 20, 20, 40]
        title1 = ["文件名", "大小", "修改时间", "创建时间", "储存路径"]
        ListItems(self.Tab1.title.frame, "#DDDDDD", widths, title1)
        self.Tab1.lbox.config(scrollregion=(0, 0, 1200, 50 * len(files_list)))
        self.Tab1.lbox.flush()
        self.Tab1.lbox.bar.place(**self.dic["Tab_scroll"])
        self.FL = []
        for file in files_list:
            self.FL.append(ListItems(
                self.Tab1.lbox.frame, '#FFFFFF', widths, file))
        for FL in self.FL:
            FL.bind_label(self.dwlabel)
            FL.actions()

    def set_file_list(self, file_list):
        self.file_list = file_list

    def get_file_list(self):
        return self.file_list

    def logs_display(self, logs_list):
        widths = [13, 20, 9, 22]
        title2 = ["用户名", "文件名", "操作类型", "操作时间"]
        ListItems(self.Tab2.title.frame, "#DDDDDD", widths, title2)
        self.Tab2.lbox.config(scrollregion=(0, 0, 1200, 50 * len(logs_list)))
        self.Tab2.lbox.flush()
        self.Tab2.lbox.bar.place(**self.dic["Tab_scroll"])
        for log in logs_list:
            ListItems(self.Tab2.lbox.frame, '#DDDDDD', widths, log).actions()

    def user_display(self, onlinelist):
        self.lbox2.delete(0, END)
        for fs in onlinelist:
            self.lbox2.insert(END, fs)
            self.lbox2.select_set(onlinelist.index(onlinelist[0]))
            self.lbox2.see(onlinelist.index(onlinelist[0]))
            self.lbox2.bind("<Button-1>", self.searchuser)

    def searchuser(self, event):
        print("选择用户")
        select = self.lbox2.get(self.lbox2.curselection())
        print(select)
        self.search.config(show=select.split(" ")[0])

    def logselect(self, event):
        print(self.combox.current)

    def logout(self, event):
        print("logout")
        self.logoutlabel.config(text="成功导出日志至路径……")

    def ready_up(self, event):
        self.upName = tkinter.filedialog.askopenfilename(
            initialdir=os.path.abspath("GUI_main.py"))
        if self.upName:
            self.uplabel.config(text=self.upName)
        self.upsize = os.path.getsize(self.upName)
        self.upline1.config(text="文件大小:    " + self.deal_upsize(self.upsize))
        last_time = time.ctime(os.path.getmtime(self.upName))
        self.upline2.config(text="最后修改时间:    " + last_time)
        self.upline5.config(text="")
        self.progress_bar()

    def upload(self, event):
        self.up_queue.append(self.upName)
        self.uplabel.config(text="正在执行上传操作……")
        self.upline1.config(text="正在上传:    " + self.upName)

    def progress_bar(self):
        progress = Frame(self.root).place(**self.dic['Up_line4'])
        self.mycanvas = Canvas(progress, width=220, height=30, bg="#DDDDDD")
        self.mycanvas.place(**self.dic['Up_line4'])
        self.x1 = StringVar()
        self.out_rec = self.mycanvas.create_rectangle(
            5, 5, 305, 25, outline='#32CD32', width=1)
        self.fill_rec = self.mycanvas.create_rectangle(
            5, 5, 5, 25, outline="", width=0, fill='#32CD32')
        Label(progress, textvariable=self.x1, font=(
            "微软雅黑", 12)).place(**self.dic['Up_line5'])

    def change_schedule(self, now_schedule, all_schedule):
        self.mycanvas.coords(self.fill_rec, (
            5, 5, 6 + (now_schedule / all_schedule) * 300, 25))
        self.root.update()
        self.x1.set(str(round(now_schedule / all_schedule * 100, 2)) + '%')
        self.upline2.config(
            text="已上传:    " +
            self.deal_upsize(now_schedule) +
            "/" + self.deal_upsize(self.upsize))
        self.upline3.config(
            text="上传队列还剩%d个任务" % len(self.up_queue))
        if round(now_schedule / all_schedule * 100, 2) == 100.00:
            self.x1.set("完成 " + chr(9989))

    def hello(self):
        print("未绑定")

    def deal_message(self, code):
        ql = len(self.up_queue) - 1
        if code == '0':
            self.up_queue.pop(0)
        if not ql:
            self.upline3.config(text="上传队列无上传任务")

    def deal_upsize(self, t):
        if t < 1024:
            return str(t) + " B"
        elif t < 1024**2:
            K = str(round(t / 1024, 3)) + " K"
            return K
        elif t < 1024**3:
            M = str(round(t / 1024**2, 3)) + " M"
            return M
        else:
            G = str(round(t / 1024**3, 3)) + " G"
            return G

    def download(self, event):
        if not self.dwlabel.cget('text'):
            self.show_error_message('请选择要下载的文件')
            return ''
        else:
            self.dwName = tkinter.filedialog.askdirectory()
            return self.dwName

    def help_about(self):
        about = '''
        团队：疯狂码头
        成员: 张晋 李文辉 方毅超 刘章杰
                    谭锐锋 谭永权 杨凌枫
        verion 1.0
        感谢您的使用！
        ©2018 '''
        messagebox.showinfo('关于', about)

    def refresh(self, event):
        pass

    def close(self):
        pass

    def show_error_message(self, e):
        messagebox.showerror('您的操作状态', e)

    def show_message(self, e):
        messagebox.showinfo('您的操作状态', e)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    Application().run()
