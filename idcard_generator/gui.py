import os
import sys

import PIL.Image as PImage
import cv2
import numpy as np
from PIL import ImageFont, ImageDraw

try:
    from Tkinter import *
    from ttk import *
    from tkFileDialog import *
    from tkMessageBox import *
except ImportError:
    from tkinter import *
    from tkinter.ttk import *
    from tkinter.filedialog import *
    from tkinter.messagebox import *

if getattr(sys, 'frozen', None):
    base_dir = os.path.join(sys._MEIPASS, '../asserts')
else:
    base_dir = os.path.join(os.path.dirname(__file__), '../asserts')


def set_entry_value(entry, value):
    entry.delete(0, END)
    entry.insert(0, value)


def change_background(img, img_back, zoom_size, center):
    # 缩放
    img = cv2.resize(img, zoom_size)
    rows, cols, channels = img.shape

    # 转换hsv
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # 获取mask
    # lower_blue = np.array([78, 43, 46])
    # upper_blue = np.array([110, 255, 255])
    diff = [5, 30, 30]
    gb = hsv[0, 0]
    lower_blue = np.array(gb - diff)
    upper_blue = np.array(gb + diff)
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    # cv2.imshow('Mask', mask)

    # 腐蚀膨胀
    erode = cv2.erode(mask, None, iterations=1)
    dilate = cv2.dilate(erode, None, iterations=1)

    # 粘贴
    for i in range(rows):
        for j in range(cols):
            if dilate[i, j] == 0:  # 0代表黑色的点
                img_back[center[0] + i, center[1] + j] = img[i, j]  # 此处替换颜色，为BGR通道

    return img_back


def paste(avatar, bg, zoom_size, center):
    avatar = cv2.resize(avatar, zoom_size)
    rows, cols, channels = avatar.shape
    for i in range(rows):
        for j in range(cols):
            bg[center[0] + i, center[1] + j] = avatar[i, j]
    return bg


class IDGen:
    def random_data(self):
        set_entry_value(self.eName, "张三")
        set_entry_value(self.eSex, "男")
        set_entry_value(self.eNation, "汉")
        set_entry_value(self.eYear, "1995")
        set_entry_value(self.eMon, "7")
        set_entry_value(self.eDay, "17")
        set_entry_value(self.eAddr, "四川省成都市武侯区益州大道中段722号复城国际")
        set_entry_value(self.eIdn, "513701199512121234")
        set_entry_value(self.eOrg, "四川省成都市锦江分局")
        set_entry_value(self.eLife, "2010.01.01-2020.12.12")

    def generator(self):
        addr = self.eAddr.get()

        f_name = askopenfilename(initialdir=os.getcwd(), title='选择头像')
        im = PImage.open(os.path.join(base_dir, 'empty.png'))
        avatar = PImage.open(f_name)  # 500x670

        name_font = ImageFont.truetype(os.path.join(base_dir, 'fonts/hei.ttf'), 72)
        other_font = ImageFont.truetype(os.path.join(base_dir, 'fonts/hei.ttf'), 60)
        birth_date_font = ImageFont.truetype(os.path.join(base_dir, 'fonts/fzhei.ttf'), 60)
        id_font = ImageFont.truetype(os.path.join(base_dir, 'fonts/ocrb10bt.ttf'), 72)

        draw = ImageDraw.Draw(im)
        draw.text((630, 690), self.eName.get(), fill=(0, 0, 0), font=name_font)
        draw.text((630, 840), self.eSex.get(), fill=(0, 0, 0), font=other_font)
        draw.text((1030, 840), self.eNation.get(), fill=(0, 0, 0), font=other_font)
        draw.text((630, 980), self.eYear.get(), fill=(0, 0, 0), font=birth_date_font)
        draw.text((950, 980), self.eMon.get(), fill=(0, 0, 0), font=birth_date_font)
        draw.text((1150, 980), self.eDay.get(), fill=(0, 0, 0), font=birth_date_font)
        start = 0
        loc = 1120
        while start + 11 < len(addr):
            draw.text((630, loc), addr[start:start + 11], fill=(0, 0, 0), font=other_font)
            start += 11
            loc += 100
        draw.text((630, loc), addr[start:], fill=(0, 0, 0), font=other_font)
        draw.text((950, 1475), self.eIdn.get(), fill=(0, 0, 0), font=id_font)
        draw.text((1050, 2750), self.eOrg.get(), fill=(0, 0, 0), font=other_font)
        draw.text((1050, 2895), self.eLife.get(), fill=(0, 0, 0), font=other_font)

        if self.eBgvar.get():
            avatar = cv2.cvtColor(np.asarray(avatar), cv2.COLOR_RGBA2BGRA)
            im = cv2.cvtColor(np.asarray(im), cv2.COLOR_RGBA2BGRA)
            im = change_background(avatar, im, (500, 670), (690, 1500))
            im = PImage.fromarray(cv2.cvtColor(im, cv2.COLOR_BGRA2RGBA))
        else:
            avatar = avatar.resize((500, 670))
            avatar = avatar.convert('RGBA')
            im.paste(avatar, (1500, 690), mask=avatar)
            # im = paste(avatar, im, (500, 670), (690, 1500))

        im.save('color.png')
        im.convert('L').save('bw.png')

        showinfo('成功', '文件已生成到目录下,黑白bw.png和彩色color.png')

    def show_ui(self, root):
        root.title('AIRobot身份证图片生成器 请遵守法律法规')
        # root.geometry('640x480')
        root.resizable(width=False, height=False)
        Label(root, text='姓名:').grid(row=0, column=0, sticky=W, padx=3, pady=3)
        self.eName = Entry(root, width=8)
        self.eName.grid(row=0, column=1, sticky=W, padx=3, pady=3)
        Label(root, text='性别:').grid(row=0, column=2, sticky=W, padx=3, pady=3)
        self.eSex = Entry(root, width=8)
        self.eSex.grid(row=0, column=3, sticky=W, padx=3, pady=3)
        Label(root, text='民族:').grid(row=0, column=4, sticky=W, padx=3, pady=3)
        self.eNation = Entry(root, width=8)
        self.eNation.grid(row=0, column=5, sticky=W, padx=3, pady=3)
        Label(root, text='出生年:').grid(row=1, column=0, sticky=W, padx=3, pady=3)
        self.eYear = Entry(root, width=8)
        self.eYear.grid(row=1, column=1, sticky=W, padx=3, pady=3)
        Label(root, text='月:').grid(row=1, column=2, sticky=W, padx=3, pady=3)
        self.eMon = Entry(root, width=8)
        self.eMon.grid(row=1, column=3, sticky=W, padx=3, pady=3)
        Label(root, text='日:').grid(row=1, column=4, sticky=W, padx=3, pady=3)
        self.eDay = Entry(root, width=8)
        self.eDay.grid(row=1, column=5, sticky=W, padx=3, pady=3)
        Label(root, text='住址:').grid(row=2, column=0, sticky=W, padx=3, pady=3)
        self.eAddr = Entry(root, width=32)
        self.eAddr.grid(row=2, column=1, sticky=W, padx=3, pady=3, columnspan=5)
        Label(root, text='证件号码:').grid(row=3, column=0, sticky=W, padx=3, pady=3)
        self.eIdn = Entry(root, width=32)
        self.eIdn.grid(row=3, column=1, sticky=W, padx=3, pady=3, columnspan=5)
        Label(root, text='签发机关:').grid(row=4, column=0, sticky=W, padx=3, pady=3)
        self.eOrg = Entry(root, width=32)
        self.eOrg.grid(row=4, column=1, sticky=W, padx=3, pady=3, columnspan=5)
        Label(root, text='有效期限:').grid(row=5, column=0, sticky=W, padx=3, pady=3)
        self.eLife = Entry(root, width=32)
        self.eLife.grid(row=5, column=1, sticky=W, padx=3, pady=3, columnspan=5)
        Label(root, text='选项:').grid(row=6, column=0, sticky=W, padx=3, pady=3)
        self.eBgvar = IntVar()
        self.ebg = Checkbutton(root, text='自动抠图', variable=self.eBgvar)
        self.ebg.grid(row=6, column=1, sticky=W, padx=3, pady=3, columnspan=5)

        randomBtn = Button(root, text='随机', width=8, command=self.random_data)
        randomBtn.grid(row=7, column=0, sticky=W, padx=16, pady=3, columnspan=2)
        genBtn = Button(root, text='生成', width=24, command=self.generator)
        genBtn.grid(row=7, column=2, sticky=W, padx=1, pady=3, columnspan=4)

    def run(self):
        root = Tk()
        self.show_ui(root)
        root.iconbitmap(os.path.join(base_dir, 'ico.ico'))
        root.mainloop()
