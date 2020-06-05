from bypy import ByPy
from tkinter import *


def startUpdate(rootUpdate, newVersionNum):
    bp=ByPy()
    bp.download("gui_version.exe")
    bp.download("parse_file.py")
    with open("current_version.txt", "w") as f:
        f.write(newVersionNum)
    topUpdateSuccess = Toplevel()
    label0 = Label(topUpdateSuccess, text = "更新完成！请退出当前界面并重启自动答题机").grid(row = 0, column = 0)
    btnQuirSyc = Button(topUpdateSuccess, text="退出", command=rootUpdate.quit).grid(row=1, column=0)

rootUpdate = Tk()
rootUpdate.title("更新")
newVersionNum = ""
with open ("version.txt") as f:
    newVersionNum = f.readline()

btn_input2 = Button(rootUpdate, text="开始更新", command=lambda: startUpdate(rootUpdate, newVersionNum)).grid(row=0, column=0)
btnQuit = Button(rootUpdate, text="退出", command=rootUpdate.quit).grid(row=1, column=0)
mainloop()