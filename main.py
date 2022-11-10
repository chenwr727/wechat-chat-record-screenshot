"""
  @author: chenwr
  @email: worry369@163.com
  @version: 1.0
"""


import base64
import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar

from utils import __doc__ as about_version
from utils.icon import ICON_BASE64
from utils.tools import selectPicture

help_entries = (("发版说明", about_version), ("关于", __doc__))


class App(object):
    def __init__(self):
        self.root = root = tk.Tk()
        root.title("切图")
        root.resizable(False, False)
        self.setIcon()
        root.wm_protocol("WM_DELETE_WINDOW", self._destroy)

        # menu
        self.mBar = tk.Menu(root)
        self.mBar.add_cascade(menu=self.makeFileMenu(self.mBar), label="文件")
        self.mBar.add_cascade(menu=self.makeHelpMenu(self.mBar), label="帮助")
        root["menu"] = self.mBar

        # frame
        self.row = 0
        self.floder_path = self.makeLoadFolder()
        self.btn_run = tk.Button(root, text="运行", width=8, command=self.runApp)
        self.btn_run.grid(row=self.row, column=2, sticky=tk.E, padx=3, pady=3)
        self.btn_run["state"] = "disable"
        self.progress = Progressbar(root, orient=tk.HORIZONTAL, mode="indeterminate")

        # center
        self.setWindowCenter()

    def setIcon(self):
        with open("tmp.ico", "wb") as tmp:
            tmp.write(base64.b64decode(ICON_BASE64))
        self.root.iconbitmap("tmp.ico")
        os.remove("tmp.ico")
        return None

    def setWindowCenter(self):
        self.root.update()
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()
        screen_width, screen_height = self.root.maxsize()
        center_x = (screen_width - window_width) // 2
        center_y = (screen_height - window_height) // 2
        size_xy = "%dx%d+%d+%d" % (window_width, window_height, center_x, center_y)
        self.root.geometry(size_xy)

    def makeFileMenu(self, master):
        menu = tk.Menu(master, tearoff=0)
        menu.add_command(label="退出", command=self.root.quit)
        return menu

    def makeHelpMenu(self, master):
        menu = tk.Menu(master, tearoff=0)
        for help_label, help_file in help_entries:

            def show(help_label=help_label, help_file=help_file):
                messagebox.showinfo(title=help_label, message=help_file)

            menu.add_command(label=help_label, command=show)
        return menu

    def makeLoadFolder(self):
        def load():
            floder_path = filedialog.askdirectory(title="选择图片文件夹")
            if floder_path != "":
                path.set(floder_path)
                self.btn_run["state"] = "normal"

        path = tk.StringVar()
        tk.Label(self.root, text="图片文件夹路径：").grid(
            row=self.row, column=0, padx=3, pady=3
        )
        tk.Entry(self.root, width=50, textvariable=path, state="disable").grid(
            row=self.row, column=1
        )
        tk.Button(self.root, text="选择文件夹", width=8, command=load).grid(
            row=self.row, column=2
        )
        self.row += 1
        return path

    def runApp(self):
        def run():
            def start():
                self.btn_run["state"] = "disable"
                self.progress.grid(row=self.row, column=0, columnspan=2)
                self.progress.start()

            def stop():
                self.progress.stop()
                self.progress.grid_forget()
                self.btn_run["state"] = "normal"

            start()
            try:
                selectPicture(self.floder_path.get())
                messagebox.showinfo(title="成功", message="程序运行成功")
            except Exception as e:
                messagebox.showerror(title="运行错误", message=f"{e}")
            stop()

        threading.Thread(target=run).start()

    def _destroy(self):
        self.root.destroy()
        self.root = None


def main():
    app = App()
    app.root.mainloop()


if __name__ == "__main__":
    main()
