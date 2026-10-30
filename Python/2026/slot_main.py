import sys
import serial
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap



## QLabel,QPixmap画像  2:1    60秒で一気に止める

image_paths = [
    "0.jpg",
    "1.jpg",
    "2.jpg",
    "3.jpg",
    "4.jpg",
    "5.jpg",
    "6.jpg"
]

img_0=0;img_05=62
img_1=125;img_15=187
img_2=250;img_25=312
img_3=375;img_35=437
img_4=500;img_45=562;img_5=625

img_55=687;img_6=750

# =========================
# 画像表示
# ========================
class ImageLabel(QLabel):

    def __init__(self, image_path):
        super().__init__()
        self.set_image(image_path)

    def set_image(self, image_path):
        image = QPixmap(image_path)
        if image.isNull():
            raise FileNotFoundError(f"File not found: {image_path}")

        self.setPixmap(image)
        #self.setScaledContents(True)  # 画像をラベルのサイズに合わせて拡大縮小する




# =========================
# ウィンドウ
# =========================

class Window(QWidget):

    def __init__(self):
        super().__init__()

        #
        self.setWindowTitle("slot")
        self.resize(800, 600)                 ##ipadの4:3にする(あとで)

        self.setStyleSheet("background-color: #000000;") 

        #self.setWindowFlags(Qt.FramelessWindowHint)  # ウィンドウの枠を非表示にする(あとで)
        #self.setCursor(Qt.BlankCursor)  # カーソルを非表示にする（あとで
        ##self.setDisabled(True)  # ウィンドウを無効化して操作できないようにする??


        #
        self.reel_labels = []
        # for _ in range(3):
        #     images = [ImageLabel(path) for path in image_paths]
        #     self.reel_labels.append(images)
        self.reel_label_l=[]
        self.reel_label_c=[]
        self.reel_label_r=[]
        

        #左
        for i, path in enumerate(image_paths):
            image_label_l = ImageLabel(path)
            image_label_l.setFixedSize(250, 125)
            image_label_l.setStyleSheet("border: 5px solid white;")
            image_label_l.setParent(self)
            image_label_l.move(50, i * 125)
            self.reel_label_l.append(image_label_l)

        #中央
        for i, path in enumerate(image_paths):
            image_label_c = ImageLabel(path)
            image_label_c.setFixedSize(250, 125)
            image_label_c.setStyleSheet("border: 5px solid white;")
            image_label_c.setParent(self)
            image_label_c.move(285, i * 125)
            self.reel_label_c.append(image_label_c)

        #右
        for i, path in enumerate(image_paths):
            image_label_r = ImageLabel(path)
            image_label_r.setFixedSize(250, 125)
            image_label_r.setStyleSheet("border: 5px solid white;")
            image_label_r.setParent(self)
            image_label_r.move(520, i * 125)
            self.reel_label_r.append(image_label_r)
    

        self.start_spin()
        self.serial_open()
        if self.ser.readline() == b'stop_l\r\n':
            if img_0<self.yl<=img_1:
                self.stop_spin()
                self.yl=img_05
            elif img_1<self.yl<=img_2:
                self.stop_spin()
                self.yl=img_15
            elif img_2<self.yl<=img_3:
                self.stop_spin()
                self.yl=img_25
            elif img_3<self.yl<=img_4:
                self.stop_spin()
                self.yl=img_35
            elif img_4<self.yl<=img_5:
                self.stop_spin()
                self.yl=img_45
            else:
                self.stop_spin()
                self.yl=img_55



    def serial_open(self):
        ser = serial.Serial("COM6", 9600)
        ser.open()
        ser.readline()


    def start_spin(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.spin_reels)
        self.timer.start(30)

    def spin_reels(self):
        speed = 10


        for label in self.reel_label_l:
            xl = label.x()
            yl = label.y() + speed         ##x()ていう

            if yl >= 600:
                yl = yl - 7*125            ##-=

            label.move(xl, yl)
    #３つ
        for label in self.reel_label_c:
            xc = label.x()
            yc = label.y() + speed-2
            if yc >= 600:
                yc = yc - 7*125
            label.move(xc, yc)
        for label in self.reel_label_r:
            xr = label.x()
            yr = label.y() + speed+2
            if yr >= 600:
                yr = yr - 7*125
            label.move(xr, yr)


        def stop_spin(self):
            self.timer.stop()



# =========================
# くるくるQTimer　移動した
# =========================
#class ReelsTimer(QTimer):

#     # def update_reels(self):
#     #     self.
#     # def stop_timer(self):
#     #     self.stop()



# =========================
# スイッチ検出
# =========================
class switch_detect:

    def __init__(self, switch):
        self.switch = switch

    def detect(self):
        if self.switch.__():
            pass
        else:
            pass


# =========================
# アプリ
# =========================

app = QApplication(sys.argv)


# =========================
# キャンバス
# =========================

window = Window()




# =========================
# タイマー的な
# ========================
#timer = ReelsTimer(window)
#timer.start_timer()





# =========================
# 表示
# =========================

window.show()

sys.exit(app.exec())
