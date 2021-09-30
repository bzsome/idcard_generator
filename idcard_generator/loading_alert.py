# 加载/处理中对话框
import tkinter as tk
from tkinter import ttk
import threading
import time


def format_form(form, width, height):
    """设置居中显示"""
    # 得到屏幕宽度
    win_width = form.winfo_screenwidth()
    # 得到屏幕高度
    win_height = form.winfo_screenheight()

    # 计算偏移量
    width_adjust = (win_width - width) / 2
    height_adjust = (win_height - height) / 2

    form.geometry("%dx%d+%d+%d" % (width, height, width_adjust, height_adjust))


class LoadingBar(object):

    def __init__(self, title="提示", content="正在处理...", width=200, height=100):

        self.__title = title
        self.__content = content
        # 设置滚动条的宽度
        self.__width = width
        # 设置窗体高度
        self.__height = height
        self.__parent = None
        # 存储显示窗体
        self.__dialog = None
        self.progress_bar = None
        self.__showFlag = False
        self.__sleep = 1

    def show(self, parent=None, speed=10, sleep=1):
        """显示的时候支持重置滚动条速度和标识判断等待时长"""
        # 防止重复创建多个
        if self.__dialog is not None:
            return

        # 线程内读取标记的等待时长（单位秒）
        self.__sleep = sleep
        self.__parent = parent
        # 记录显示标识
        self.__showFlag = True

        # 创建窗体
        self.__dialog = tk.Toplevel(parent)
        self.__dialog.title(self.__title)
        format_form(self.__dialog, self.__width, self.__height)
        # 设置置顶
        self.__dialog.wm_attributes("-topmost", True)
        # 禁止拉伸窗口
        self.__dialog.resizable(0, 0)
        # 去除边框
        # self.__dialog.overrideredirect(-1)
        # 去掉窗口最大化最小化按钮，只保留关闭
        # self.__dialog.attributes("-toolwindow", 2)
        # 设置关闭方式
        self.__dialog.protocol("WM_DELETE_WINDOW", lambda: None)

        tk.Label(self.__dialog, text=self.__content).pack(side=tk.TOP)

        # 父窗口禁用
        self.__parent.grab_set()

        # 实际的滚动条控件
        self.progress_bar = ttk.Progressbar(self.__dialog, length=self.__width, mode="indeterminate",
                                            orient=tk.HORIZONTAL)
        self.progress_bar.pack(expand=True)
        # 数值越小，滚动越快
        self.progress_bar.start(speed)
        # # 开启新线程保持滚动条显示（使用会报错，使用after代替）
        # waitThread = threading.Thread(target=self.wait_close)
        # waitThread.setDaemon(True)
        # waitThread.start()
        self.__dialog.after(250, self.wait_close)

    def wait_close(self):
        print(self.__showFlag)
        if self.__showFlag:
            self.__dialog.after(250, self.wait_close)
            return

        # 非空情况下销毁
        if self.__dialog is not None:
            self.__dialog.destroy()

        # 重置必要参数
        self.__dialog = None
        # 父窗口解除禁用
        self.__parent.grab_release()

    def close(self):
        # 设置显示标识为不显示
        self.__showFlag = False

    def stop(self):
        time.sleep(5)
        self.close()


# 模拟显示一个弹窗，并禁用父窗口，5秒后关闭弹窗
if __name__ == '__main__':
    root = tk.Tk()
    root.title('Loading滚动条演示')
    format_form(root, 400, 300)

    loading = LoadingBar("提示", "任务需要处理5秒")
    # 展示滚动条,指定速度
    loading.show(parent=root, speed=5)

    timer = threading.Timer(5, loading.close)
    timer.start()

    root.mainloop()
