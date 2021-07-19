import random
import threading
import tkinter
from tkinter.filedialog import *
from tkinter.messagebox import *
from tkinter.ttk import *

import PIL.Image as PImage
import cv2
import numpy
from PIL import ImageFont, ImageDraw

from idcard_generator import id_card_utils, name_utils, utils, loading_alert

asserts_dir = os.path.join(utils.get_base_path(), 'asserts')
print("asserts_dir", asserts_dir)


def set_entry_value(entry, value):
    entry.delete(0, tkinter.END)
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
    lower_blue = numpy.array(gb - diff)
    upper_blue = numpy.array(gb + diff)
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
        random_name = name_utils.random_name()
        set_entry_value(self.eName, random_name["name_full"])
        set_entry_value(self.eSex, '女' if random_name['sex'] == 0 else "男")
        set_entry_value(self.eNation, "汉")
        year = random.randint(1900, 2020)
        set_entry_value(self.eYear, year)
        month = random.randint(1, 12)
        set_entry_value(self.eMon, month)
        day = id_card_utils.random_day(year, month)
        set_entry_value(self.eDay, day)
        set_entry_value(self.eAddr, "四川省成都市武侯区益州大道中段722号复城国际")
        set_entry_value(self.eIdn, id_card_utils.random_card_no(year=str(year), month=str(month), day=str(day)))
        set_entry_value(self.eOrg, "四川省成都市锦江分局")
        start_time = id_card_utils.get_start_time()
        expire_time = id_card_utils.get_expire_time()
        set_entry_value(self.eLife, start_time + "-" + expire_time)

    def generator_image(self):
        self.f_name = askopenfilename(initialdir=os.getcwd(), title='选择头像')
        if len(self.f_name) == 0:
            return

        self.loading_bar = loading_alert.LoadingBar(title="提示", content="图片正在生成...")
        self.loading_bar.show(self.root)

        # 开启新线程保持滚动条显示
        wait_thread = threading.Thread(target=self.handle_image)
        wait_thread.setDaemon(True)
        wait_thread.start()

    def handle_image(self):
        avatar = PImage.open(self.f_name)  # 500x670
        empty_image = PImage.open(os.path.join(asserts_dir, 'empty.png'))

        name_font = ImageFont.truetype(os.path.join(asserts_dir, 'fonts/hei.ttf'), 72)
        other_font = ImageFont.truetype(os.path.join(asserts_dir, 'fonts/hei.ttf'), 64)
        birth_date_font = ImageFont.truetype(os.path.join(asserts_dir, 'fonts/fzhei.ttf'), 60)
        id_font = ImageFont.truetype(os.path.join(asserts_dir, 'fonts/ocrb10bt.ttf'), 90)

        draw = ImageDraw.Draw(empty_image)
        draw.text((630, 690), self.eName.get(), fill=(0, 0, 0), font=name_font)
        draw.text((630, 840), self.eSex.get(), fill=(0, 0, 0), font=other_font)
        draw.text((1030, 840), self.eNation.get(), fill=(0, 0, 0), font=other_font)
        draw.text((630, 975), self.eYear.get(), fill=(0, 0, 0), font=birth_date_font)
        draw.text((950, 975), self.eMon.get(), fill=(0, 0, 0), font=birth_date_font)
        draw.text((1150, 975), self.eDay.get(), fill=(0, 0, 0), font=birth_date_font)

        # 住址
        addr_loc_y = 1115
        addr_lines = self.get_addr_lines()
        for addr_line in addr_lines:
            draw.text((630, addr_loc_y), addr_line, fill=(0, 0, 0), font=other_font)
            addr_loc_y += 100

        # 身份证号
        draw.text((900, 1475), self.eIdn.get(), fill=(0, 0, 0), font=id_font)

        # 背面
        draw.text((1050, 2750), self.eOrg.get(), fill=(0, 0, 0), font=other_font)
        draw.text((1050, 2895), self.eLife.get(), fill=(0, 0, 0), font=other_font)

        if self.eBgvar.get():
            avatar = cv2.cvtColor(numpy.asarray(avatar), cv2.COLOR_RGBA2BGRA)
            empty_image = cv2.cvtColor(numpy.asarray(empty_image), cv2.COLOR_RGBA2BGRA)
            empty_image = change_background(avatar, empty_image, (500, 670), (690, 1500))
            empty_image = PImage.fromarray(cv2.cvtColor(empty_image, cv2.COLOR_BGRA2RGBA))
        else:
            avatar = avatar.resize((500, 670))
            avatar = avatar.convert('RGBA')
            empty_image.paste(avatar, (1500, 690), mask=avatar)
            # im = paste(avatar, im, (500, 670), (690, 1500))

        empty_image.save('color.png')
        empty_image.convert('L').save('bw.png')

        self.loading_bar.close()
        showinfo('成功', '文件已生成到目录下,黑白bw.png和彩色color.png')

    def show_ui(self, root):
        self.root = root
        root.title('AIRobot身份证图片生成器')
        # root.geometry('640x480')
        root.resizable(width=False, height=False)
        link = Label(root, text='请遵守法律法规，获取帮助:', cursor='hand2', foreground="#FF0000")
        link.grid(row=0, column=0, sticky=tkinter.W, padx=3, pady=3, columnspan=3)
        link.bind("<Button-1>", utils.open_url)

        link = Label(root, text='https://github.com/bzsome', cursor='hand2', foreground="blue")
        link.grid(row=0, column=2, sticky=tkinter.W, padx=26, pady=3, columnspan=4)
        link.bind("<Button-1>", utils.open_url)

        Label(root, text='姓名:').grid(row=1, column=0, sticky=tkinter.W, padx=3, pady=3)
        self.eName = Entry(root, width=8)
        self.eName.grid(row=1, column=1, sticky=tkinter.W, padx=3, pady=3)
        Label(root, text='性别:').grid(row=1, column=2, sticky=tkinter.W, padx=3, pady=3)
        self.eSex = Entry(root, width=8)
        self.eSex.grid(row=1, column=3, sticky=tkinter.W, padx=3, pady=3)
        Label(root, text='民族:').grid(row=1, column=4, sticky=tkinter.W, padx=3, pady=3)
        self.eNation = Entry(root, width=8)
        self.eNation.grid(row=1, column=5, sticky=tkinter.W, padx=3, pady=3)
        Label(root, text='出生年:').grid(row=2, column=0, sticky=tkinter.W, padx=3, pady=3)
        self.eYear = Entry(root, width=8)
        self.eYear.grid(row=2, column=1, sticky=tkinter.W, padx=3, pady=3)
        Label(root, text='月:').grid(row=2, column=2, sticky=tkinter.W, padx=3, pady=3)
        self.eMon = Entry(root, width=8)
        self.eMon.grid(row=2, column=3, sticky=tkinter.W, padx=3, pady=3)
        Label(root, text='日:').grid(row=2, column=4, sticky=tkinter.W, padx=3, pady=3)
        self.eDay = Entry(root, width=8)
        self.eDay.grid(row=2, column=5, sticky=tkinter.W, padx=3, pady=3)
        Label(root, text='住址:').grid(row=3, column=0, sticky=tkinter.W, padx=3, pady=3)
        self.eAddr = Entry(root, width=32)
        self.eAddr.grid(row=3, column=1, sticky=tkinter.W, padx=3, pady=3, columnspan=5)
        Label(root, text='证件号码:').grid(row=4, column=0, sticky=tkinter.W, padx=3, pady=3)
        self.eIdn = Entry(root, width=32)
        self.eIdn.grid(row=4, column=1, sticky=tkinter.W, padx=3, pady=3, columnspan=5)
        Label(root, text='签发机关:').grid(row=5, column=0, sticky=tkinter.W, padx=3, pady=3)
        self.eOrg = Entry(root, width=32)
        self.eOrg.grid(row=5, column=1, sticky=tkinter.W, padx=3, pady=3, columnspan=5)
        Label(root, text='有效期限:').grid(row=6, column=0, sticky=tkinter.W, padx=3, pady=3)
        self.eLife = Entry(root, width=32)
        self.eLife.grid(row=6, column=1, sticky=tkinter.W, padx=3, pady=3, columnspan=5)
        Label(root, text='选项:').grid(row=7, column=0, sticky=tkinter.W, padx=3, pady=3)
        self.eBgvar = tkinter.IntVar()
        self.eBgvar.set(1)
        self.ebg = Checkbutton(root, text='自动抠图', variable=self.eBgvar)
        self.ebg.grid(row=7, column=1, sticky=tkinter.W, padx=3, pady=3, columnspan=5)

        random_btn = Button(root, text='随机', width=8, command=self.random_data)
        random_btn.grid(row=8, column=0, sticky=tkinter.W, padx=16, pady=3, columnspan=2)
        generator_btn = Button(root, text='选择头像并生成', width=24, command=self.generator_image)
        generator_btn.grid(row=8, column=2, sticky=tkinter.W, padx=1, pady=3, columnspan=4)

        # 触发随机生成
        self.random_data()

    # 获得要显示的住址数组
    def get_addr_lines(self):
        addr = self.eAddr.get()
        addr_lines = []
        start = 0
        while start < utils.get_show_len(addr):
            show_txt = utils.get_show_txt(addr, start, start + 22)
            addr_lines.append(show_txt)
            start = start + 22

        return addr_lines

    def run(self):
        root = tkinter.Tk()
        self.show_ui(root)
        ico_path = os.path.join(asserts_dir, 'ico.ico')
        root.iconbitmap(ico_path)
        root.protocol('WM_DELETE_WINDOW', lambda: sys.exit(0))
        root.mainloop()
