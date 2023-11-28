import random

from PySide6.QtGui import QPalette, QBrush, QPixmap
import os
from pathlib import Path
import sys

from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QTextBrowser
from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader


# 获取随机的素数
def get_random_p():
    p = random.randint(100, 255)
    return p


# 计算给定素数的原根
def calculate_primitive_root(p):
    num_list = []  # 保存取模后的结果
    primitive_root = []  # 保存符合条件的原根
    # p表示随机生成的素数，范围为100-255
    for a in range(1, p):
        num_list = []
        for i in range(1, p):
            b = pow(a, i) % p
            if b not in num_list:
                num_list.append(b)
            else:
                break

        for i in range(1, p):
            if i not in num_list:
                break
            if i == p - 1:
                primitive_root.append(a)

    return primitive_root


# 每次交换前获取原根和素数
def get_p_a():
    while True:
        p = get_random_p()
        primitive_root = calculate_primitive_root(p)

        if len(primitive_root) != 0:
            break

    return p, primitive_root[0]


# 随机生成私密密钥
def get_private_key():
    return random.randint(1, 512)


# 计算公开密钥
def calculate_public_key(private_key, prime_num, primitive_root):
    public_key = pow(primitive_root, private_key) % prime_num

    return public_key


# 计算共享密钥
def calculate_share_key(public_key, prime_num, private_key):
    share_key = pow(public_key, private_key) % prime_num

    return share_key


p, a = get_p_a()


def get_pri():
    # 获取私密密钥
    pri_a = get_private_key()
    pri_b = get_private_key()
    return pri_a, pri_b


# 实现D-H密钥交换
def get_pub(pri_a, pri_b):
    # 计算公开密钥
    pub_a = calculate_public_key(pri_a, p, a)
    pub_b = calculate_public_key(pri_b, p, a)
    return pub_a, pub_b


def get_share(pri_a, pri_b, pub_a, pub_b):
    # 计算共享密钥
    share_a = calculate_share_key(pub_b, p, pri_a)
    share_b = calculate_share_key(pub_a, p, pri_b)
    return share_a, share_b


class Widget(QWidget):
    def __init__(self):
        super(Widget, self).__init__()
        self.load_ui()
        # 设置背景图片
        palette = self.palette()
        palette.setBrush(QPalette.Window, QBrush(QPixmap("./bk.jpg")))
        self.setPalette(palette)

    def load_ui(self):
        loader = QUiLoader()
        path = os.fspath(Path(__file__).resolve().parent / "form.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        loader.load(ui_file, self)
        ui_file.close()

        # 查找textBrowser
        self.textBrowser = self.findChild(QTextBrowser, "textBrowser")

        # 添加按钮点击事件处理逻辑
        self.pushButton = self.findChild(QPushButton, "pushButton")
        self.pushButton.clicked.connect(self.on_pushButton_clicked)

        # 添加按钮点击事件处理逻辑
        self.pushButton_2 = self.findChild(QPushButton, "pushButton_2")
        self.pushButton_2.clicked.connect(self.on_pushButton_2_clicked)

        # 添加按钮点击事件处理逻辑
        self.pushButton_3 = self.findChild(QPushButton, "pushButton_3")
        self.pushButton_3.clicked.connect(self.on_pushButton_3_clicked)

        # 添加按钮点击事件处理逻辑
        self.pushButton_4 = self.findChild(QPushButton, "pushButton_4")
        self.pushButton_4.clicked.connect(self.on_pushButton_4_clicked)

    # 按钮点击事件处理逻辑
    def on_pushButton_clicked(self):
        self.textBrowser.append("随机生成的素数为: "+str(p))
        self.textBrowser.append("生成的原根为: "+str(a))
        self.textBrowser.append("\n")

    def on_pushButton_2_clicked(self):
        global pri_a, pri_b
        pri_a, pri_b = get_pri()
        self.textBrowser.append("生成的私密密钥1为: "+str(pri_a))
        self.textBrowser.append("生成的私密密钥2为: "+str(pri_b))
        self.textBrowser.append("\n")

    def on_pushButton_3_clicked(self):
        global pub_a,pub_b
        pub_a,pub_b = get_pub(pri_a,pri_b)
        self.textBrowser.append("生成的公开密钥1为: "+str(pub_a))
        self.textBrowser.append("生成的公开密钥2为: "+str(pub_b))
        self.textBrowser.append("\n")

    def on_pushButton_4_clicked(self):
        global share_a,share_b
        share_a,share_b = get_share(pri_a,pri_b,pub_a,pub_b)
        self.textBrowser.append("生成的共享密钥1为: "+str(share_a))
        self.textBrowser.append("生成的共享密钥2为: "+str(share_b))
        self.textBrowser.append("\n")


if __name__ == "__main__":
    app = QApplication([])
    widget = Widget()
    widget.show()
    sys.exit(app.exec())
