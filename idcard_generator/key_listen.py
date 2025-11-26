import tkinter as tk

from utils import res_util


def on_key_press(event):
    """按键按下事件回调，判断组合键"""
    # 1. 监听 Ctrl + C
    if (event.state & 0x4) and event.keysym == 'c':
        print("触发组合键：Ctrl + C（复制）")
    # 1. 监听 Ctrl + C
    elif (event.state & 0x4) and event.keysym == 'a':
        print("触发组合键：Ctrl + A")
        res_util.print_sys_info()

    # 2. 监听 Shift + S
    elif (event.state & 0x1) and event.keysym == 's':
        print("触发组合键：Shift + S（保存为）")

    # 3. 监听 Alt + D
    elif (event.state & 0x8) and event.keysym == 'd':
        print("触发组合键：Alt + D（删除）")

    # 4. 监听 Ctrl + Shift + Q（退出程序）
    elif (event.state & 0x5) and event.keysym == 'q':
        print("触发组合键：Ctrl + Shift + Q（退出）")
        root.quit()


if __name__ == "__main__":
    # 创建 Tkinter 窗口
    root = tk.Tk()
    root.title("Tkinter 组合按键监听")
    root.geometry("400x300")

    # 绑定所有按键按下事件（<Key> 表示监听所有按键）
    root.bind("<Key>", on_key_press)

    # 启动窗口主循环
    root.mainloop()
