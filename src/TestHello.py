from time import sleep
import tkinter
import tkinter.messagebox #这个是消息框，对话框的关键

i = 0
while True:
    print("hello")
    i+=1
    sleep(2)
    if i == 2:
        tkinter.messagebox.showinfo('提示', '人生苦短')