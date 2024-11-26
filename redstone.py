from tkinter import  filedialog
import tkinter
import tkinter.messagebox
import webbrowser
import os
import subprocess

def setting():
    with open("set.ini",'r') as file:
        jluj1 = file.read()
        jluj1
    with open("login.ini",'r') as file:
        login = file.read()
    def java():
        lj1.config(text="Java路径:暂无设置")
        with open("set.ini",'w') as file:
            file.write("暂无设置")
    def select_file():
        # 打开文件选择对话框
        file_path = filedialog.askopenfilename()
        if file_path:
            # 如果用户选择了一个文件，打印文件路径
            print("选中的文件路径:", file_path)
            lj1.config(text=f"Java路径:{file_path}")
            with open('set.ini','w') as file:
                file.write(file_path)
            subprocess.run(f'java -jar cmcl.jar config javaPath "{file_path}"')


    def zb():
        subprocess.run("java -jar cmcl.jar account --login=microsoft")
        with open('login.ini',"w") as file:
            file.write("微软正版")
        login1.config(text="登录方式:微软正版")
    def lx():
        lx = lx3.get()
        subprocess.run(f"java -jar cmcl.jar account --login=offline --name={lx}")
        with open('login.ini','w') as file:
            file.write(f"离线登录:{lx}")
        login1.config(text=f"登录方式:离线登录({lx})")
    set = tkinter.Tk()
    set.title("红石启动器(设置)")
    set.iconbitmap("redstone.ico")
    set.geometry("500x300")
    lj1 = tkinter.Label(set,text=f"Java路径:{jluj1}")
    lj1.pack()
    btn_select_file = tkinter.Button(set, text="选择文件", command=select_file)
    btn_select_file.pack(pady=20)
    bj1 = tkinter.Button(set,text="清空",command =lambda:java())
    bj1.pack()

    login1 = tkinter.Label(set,text=f"登录方式:{login}")
    login1.pack()
    zb2 = tkinter.Button(set,text="微软正版",command=lambda:zb())
    zb2.pack()
    lx1 = tkinter.Label(set,text="离线登录:")
    lx1.pack()
    lx3 = tkinter.Entry(set)
    lx3.pack()
    lx2 = tkinter.Button(set,text="离线",command=lambda:lx())
    lx2.pack()

    bwj1 = tkinter.Button(set,text="打开游戏文件夹",command=lambda: os.startfile(os.getcwd()))
    bwj1.pack()
    set.mainloop()


def redstone():
    def start():
        with open("login.ini", 'r') as file:
            login = file.read()
        ban = os.getcwd()
        directory_path = fr'{ban}\.minecraft\versions'
        directories = []
        for item in os.listdir(directory_path):
            # 构造完整的文件/文件夹路径
            item_path = os.path.join(directory_path, item)
            # 使用os.path.isdir()检查是否是一个文件夹
            if os.path.isdir(item_path):
                # 如果是文件夹，则添加到列表中
                directories.append(item)

        def qd():
            babe1 = ban3.get()
            qdq.destroy()
            star.destroy()
            subprocess.run(f'java -jar cmcl.jar {babe1}')

        star = tkinter.Tk()
        star.title("红石启动器(启动)")
        star.iconbitmap("redstone.ico")
        star.geometry("500x300")
        login1 = tkinter.Label(star, text=f"登录方式:{login}")
        login1.pack()
        ban1 = tkinter.Label(star, text=f"可用版本:{directories}\n请在下方输入框输入版本")
        ban1.pack()
        ban3 = tkinter.Entry(star)
        ban3.pack()
        star2 = tkinter.Button(star, text="启动", command=lambda: qd())
        star2.pack()

        star.mainloop()
    print("启动")
    tkinter.messagebox.showinfo(title="红石启动器",message="欢迎使用红石启动器")
    qdq = tkinter.Tk()
    qdq.title("红石启动器")
    qdq.iconbitmap("redstone.ico")
    qdq.geometry("500x15")
    cd = tkinter.Menu(qdq)
    cd.add_command(label="启动",command=lambda: start())
    cd.add_command(label="下载",command=lambda: download())
    cd.add_command(label="设置",command=lambda: setting())
    zz = tkinter.Menu(cd)
    cd.add_cascade(label="作者",menu=zz)
    zz.add_command(label="抖音",command=lambda: webbrowser.open("https://www.douyin.com/user/MS4wLjABAAAA12ny7Oj3OZfizPAANMltdKajQNYLa-eMFxFQgqAsHhutZ2-99ot4HTXujukV0tlj"))
    zz.add_command(label="bilibili",command=lambda: webbrowser.open("https://space.bilibili.com/2139464112?spm_id_from=333.337.0.0"))
    qdq.config(menu=cd)
    qdq.mainloop()

def download():
    def select():
        print("原版")
        def bb4():
            bb5 = bb3.get()
            subprocess.run(f"java -jar cmcl.jar install {bb5} -s")
            tkinter.messagebox.showinfo(title="红石启动器", message="下载完成")
            bb0.destroy()

        bb0 = tkinter.Tk()
        bb0.title("红石启动器(下载:原版)")
        bb0.geometry("300x150")
        bb0.iconbitmap("redstone.ico")
        bb1 = tkinter.Label(bb0,text="请输入你想下载的版本（例如:1.8.9）：")
        bb1.pack()
        bb3 =tkinter.Entry(bb0)
        bb3.pack()
        bb2 = tkinter.Button(bb0,text="下载",command=lambda:bb4())
        bb2.pack()
        bb0.mainloop()


    dd = tkinter.Tk()
    dd.title("红石启动器(下载)")
    dd.iconbitmap("redstone.ico")
    dd.geometry("300x150")
    s2 =tkinter.Button(dd,text="原版下载",command=lambda:select())
    s2.pack()
    fb2 = tkinter.Button(dd,text="fabric版本下载",command=lambda:tkinter.messagebox.showinfo(title="红石启动器",message="暂未开发"))
    fb2.pack()
    fo2 = tkinter.Button(dd,text="forge版本下载",command=lambda:tkinter.messagebox.showinfo(title="红石启动器",message="暂未开发"))
    fo2.pack()
    op2 = tkinter.Button(dd,text="optifine版本下载",command=lambda:tkinter.messagebox.showinfo(title="红石启动器",message="暂未开发"))
    op2.pack()

    dd.mainloop()


def sym():
  if os.path.exists("cmcl.jar"):
      y = e1.get()
      x = "by:redstone"
      if y == x:
         yzm.destroy()
         redstone()
      else:
         tkinter.messagebox.showerror(title="使用码错误",message="请输入正确使用码")
  else:
      tkinter.messagebox.showerror(title="error", message="检测到主程序丢失\n请重新安装")

yzm = tkinter.Tk()
yzm.title("请输入使用码")
yzm.iconbitmap("redstone.ico")
yzm.geometry("300x100")
l1 = tkinter.Label(yzm,text="请输入使用码")
l1.pack()
e1 = tkinter.Entry(yzm)
e1.pack()
b1 = tkinter.Button(yzm,text="确认",command=sym)
b1.pack()
b2 =tkinter.Button(yzm,text="点击前往官网获取",command=lambda:webbrowser.open("https://www.douyin.com/user/MS4wLjABAAAA12ny7Oj3OZfizPAANMltdKajQNYLa-eMFxFQgqAsHhutZ2-99ot4HTXujukV0tlj"))
b2.pack()
yzm.mainloop()
