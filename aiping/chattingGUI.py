"""
Created on Fri Apr 19 2019
Description: Chatting with Aiping

@author: Siping Wang
"""
import json
from tkinter import *
import time
import urllib.request
import sys
from .aihttp import TuringRequest

path = sys.argv[0]
path = path[:-7]

class Base():
    def __init__(self, master):
        self.root = master
        self.root.config()
        self.root.title('与Aiping聊天')
        self.root.geometry('400x415')
        Initface(self.root)

class Initface():
    def __init__(self, master):
        self.master = master
        self.master.config(bg='Aquamarine')
        self.initface = Frame(self.master)
        self.initface.pack(expand=YES, fill=X, anchor=CENTER)
        author = Label(self.initface, text='欢迎，人类！')
        author.pack(side=TOP, fill=X)
        button1 = Button(self.initface, text='内测入口', command=self.log)
        button1.pack(side=LEFT, expand=NO, padx=50)
        button2 = Button(self.initface, text='索要账号', command=self.need)
        button2.pack(side=RIGHT, expand=NO, padx=50)

    def log(self):
        self.initface.destroy()
        LogIn(self.master)

    def need(self):
        self.initface.destroy()
        Pay(self.master)

class Pay():
    def __init__(self, master):
        self.master = master
        self.master.config(bg='Aquamarine')
        self.pay = Frame(self.master)
        self.pay.pack(expand=YES, fill=BOTH, anchor=CENTER, padx=20)
        img = PhotoImage(file= path + "pay.gif")
        lblImage = Label(self.pay, image=img)
        lblImage.image = img
        lblImage.pack()

class LogIn():
    def __init__(self, master):
        self.master = master
        self.master.config(bg='Aquamarine')
        self.login = Frame(self.master)
        self.login.pack(expand=YES, fill=X, anchor=CENTER)
        Label(self.login, text='               用户名                    ').grid(column=0, sticky=W)
        Label(self.login, text='               密码 (*/ω＼*)           ').grid(column=0, sticky=W)
        self.e1 = Entry(self.login)
        self.e1.grid(row=0, column=1, columnspan=2, sticky=W + E)
        self.e2 = Entry(self.login)
        self.e2.grid(row=1, column=1, columnspan=2, sticky=W + E)

        Button(self.login, text='START !', command=self.go).grid(row=2, column=1, columnspan=2, sticky=W)
        Button(self.login, text='BACK', command=self.back).grid(row=2, column=1, columnspan=2, sticky=E)

    def go(self):
        if str(self.e1.get()) == "human" and str(self.e2.get()) == "iloveaiping":
            self.login.destroy()
            Chat(self.master)
        else:
            Label(self.login, text='哼你才不是内测人员~', fg='red').grid(row=2)
            self.e1.delete(0, len(self.e1.get()))
            self.e2.delete(0, len(self.e2.get()))
            return 0

    def back(self):
        self.login.destroy()
        Initface(self.master)

class Chat():
    def __init__(self, master):
        self.master = master
        self.master.config(bg='Black')

        self.frmLT = Canvas(self.master, width=400, height=270, scrollregion=(0, 0, 400, 363))
        self.frmLT.place(x=0, y=0)
        self.ffrmLT = Frame(self.frmLT)
        self.ffrmLT.place(width=400, height=10000)

        self.repeatvbar = Scrollbar(self.frmLT, orient=VERTICAL)  # 竖直滚动条
        self.repeatvbar.place(x=380, width=20, height=270)
        self.repeatvbar.configure(command=self.frmLT.yview)
        self.frmLT.config(yscrollcommand=self.repeatvbar.set)

        self.frmLT.create_window((278, 180), window=self.ffrmLT)

        self.frmLC = Canvas(self.master, width=403, height=100, scrollregion=(0, 0, 520, 520))
        self.frmLC.place(x=-3, y=278)
        self.ffrmLC = Frame(self.frmLC)
        self.frmLB = Frame(self.master, width=400, height=30)

        self.ffrmLC.place(width=400, height=100)

        self.frmLB.place(x=0, y=386, width=400)

        self.ffrmLC.grid_propagate(0)
        self.frmLB.grid_propagate(0)

        self.txtMsgList = Text(self.ffrmLT, bg='MintCream')
        self.txtMsgList.tag_config('greencolor', foreground='#008C00')  # 创建tag
        self.txtMsgList.tag_config('bluecolor', foreground='#0000FF')
        self.txtMsg = Text(self.ffrmLC)

        self.btnSend = Button(self.frmLB, text='发送', width=8, command=self.sendMsg)
        self.btnCancel = Button(self.frmLB, text='重写', width=8, command=self.cancelMsg)
        self.btnQuit = Button(self.frmLB, text='不聊了 ´_>`', width=12, command=self.goBack)
        self.btnSend.grid(row=2, column=0)
        self.btnCancel.grid(row=2, column=1)
        self.btnQuit.pack(side=RIGHT)
        self.txtMsgList.grid()
        self.txtMsg.grid()


    def sendMsg(self):#发送消息
        if len(str(self.txtMsg.get('0.0', END))) == 0:
            return 0
        strMsg = "我:" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n'
        self.txtMsgList.insert(END, strMsg, 'greencolor')
        self.txtMsgList.insert(END, self.txtMsg.get('0.0', END))
        self.reply()
        self.txtMsg.delete('0.0', END)


    def cancelMsg(self):#取消信息
        self.txtMsg.delete('0.0', END)

    def reply(self):
        replyMsg = "Aiping:"+ time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n'
        try:
            req = TuringRequest(str(self.txtMsg.get(0.0, END)))
            results_text = req.send()
        except FileNotFoundError as e:
            results_text = str(e)
        except Exception as e:
            print(e)
            results_text = "没有网了 QAQ"

        self.txtMsgList.insert(END, replyMsg, 'bluecolor')
        self.txtMsgList.insert(END, results_text + '\n')

    def goBack(self):
        self.frmLT.destroy()
        self.frmLB.destroy()
        self.frmLC.destroy()
        Initface(self.master)


if __name__ == "__main__":
    print(path + 'api.rtf')