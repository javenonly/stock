import tkinter
import tkinter.messagebox
def but():
    tkinter.messagebox.showinfo('提示', '人生苦短')
    #tkinter.messagebox.showwarning('警告', '明日有大雨')
    #tkinter.messagebox.showerror('错误', '出错了')
root=tkinter.Tk()
# root.title('GUI')#标题
# root.geometry('800x600')#窗体大小
# root.resizable(False, False)#固定窗体
tkinter.Button(root, text='hello button',command=but).pack()
# root.mainloop()