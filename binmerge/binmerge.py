#! python3
import os
import tkinter as tk
import tkinter.filedialog as tkFileDialog
import tkinter.messagebox as tkMessageBox


def merge():
    try:
        app = open(App.get(), 'rb').read()
    except Exception as e:
        tkMessageBox.showerror(title='文件错误', message='APP 文件不存在')
        return

    try:
        boot = open(Boot.get(), 'rb').read() 
    except Exception as e:
        tkMessageBox.showerror(title='文件错误', message='BOOT文件不存在')
        return

    try:
        addr = int(Addr.get(), 16)
    except Exception as e:
        tkMessageBox.showerror(title='地址错误', message='地址不是十六进制数')
        return

    '''
    app = list(app)
    app[0x20:0x24] = struct.pack('<L', 0x0B11FFAC)
    app = ''.join(app)
    '''
    
    out = app + b'\xFF' * (addr - len(app)) + boot

    open(App.get()[:-4] + '_withBOOT.bin', 'wb').write(out)

    tkMessageBox.showinfo(title='合并完成', message='已完合并生成：\n%s' %(App.get()[:-4] + '_withBOOT.bin'))


def getFile(Var):
    dir = os.path.split(Var.get())[0]
    file = tkFileDialog.askopenfilename(initialdir=dir, filetypes = [('BIN', '.bin')])
    if file:
        Var.set(file)


win = tk.Tk()

App = tk.StringVar(win, r'C:\Users\wmx\Desktop\SWM181_App.bin')
Boot = tk.StringVar(win, r'C:\Users\wmx\Desktop\SWM181_UserBoot.bin')
Addr = tk.StringVar(win, '0x1C000')

tk.Label(win, text='App 文件：').grid(row=0, column=0)
tk.Entry(win, width=64, textvariable=App).grid(row=0, column=1)
tk.Button(win, text='...', width=4, command=lambda Var=App: getFile(Var)).grid(row=0, column=2)

tk.Label(win, text='Boot文件：').grid(row=1, column=0)
tk.Entry(win, width=64, textvariable=Boot).grid(row=1, column=1)
tk.Button(win, text='...', width=4, command=lambda Var=Boot: getFile(Var)).grid(row=1, column=2)

tk.Label(win, text='Boot地址：').grid(row=2, column=0)
tk.Entry(win, width=12, textvariable=Addr).grid(row=2, column=1, sticky="W")
tk.Button(win, text='合并', width=4, command=lambda: merge()).grid(row=2, column=2)

win.mainloop()
