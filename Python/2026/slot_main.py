import sys
import serial
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap


## QLabel,QPixmap画像  2:1
## ちいぱちCOM4

image_paths = [
    "bar.png",
    "bell.png",
    "cherry.png",
    "juggler.png",
    "mascat.png",
    "replay.png",
    "seven.png"
]


#使う数値
img_0=0;  img_05=62
img_1=125;img_15=187
img_2=250;img_25=312
img_3=375;img_35=437
img_4=500;img_45=562
img_5=625;img_55=687
img_6=750


# =========================
# 画像表示
# ========================
class ImageLabel(QLabel):

    def __init__(self, image_path):
        super().__init__()
        self.set_image(image_path)

    def set_image(self, image_path):
        image = QPixmap(image_path)


        self.setPixmap(image)
        self.setScaledContents(True)  #画像をラベルのサイズに合わせて拡大縮小する!




# =========================
# ウィンドウ
# =========================

class Window(QWidget):

    def serial_open(self):
        self.ser = serial.Serial("COM4", 9600, timeout=0)
        # self.ser.open()  ##うえのでもう開いてるらしい
        ##ないときもb'n\r\n'を受信
        self.timer_ser = QTimer(self)
        self.timer_ser.timeout.connect(self.get_serial)
        self.timer_ser.start(10)


    def start_spin(self):
        # self.command = b''  # 初期化
        

        self.timer_l = QTimer(self)
        self.timer_l.timeout.connect(self.spin_left)
        self.timer_l.start(10)

        self.timer_c = QTimer(self)
        self.timer_c.timeout.connect(self.spin_center)
        self.timer_c.start(10)

        self.timer_r = QTimer(self)
        self.timer_r.timeout.connect(self.spin_right)
        self.timer_r.start(10)# 30

    def get_serial(self):
        self.command = self.ser.readline()
        self.ser.reset_input_buffer()
        print(self.command)


    def spin_left(self):
        speed = 10

        for label in self.reel_label_l:
            xl = label.x()
            yl = label.y() + speed         ##x()ていう

            if yl >= 1200:
                yl = yl - 7*200            ##-=

            label.move(xl, yl)

        
        ##spinのなか↓     あとキーボード入力でも停止できるように
        
        # print(type(StringSig))
        # ThirdSS = StringSig[2]
        # print(ThirdSS)

            if self.command == b'l\r\n':
                
                # print(f"信号きてる_l")
                if img_0<yl<=img_1:
                    self.stop_left()
                    label.move(xl, img_05)
                    
                elif img_1<yl<=img_2:
                    self.stop_left()
                    label.move(xl, img_15)
                elif img_2<yl<=img_3:
                    self.stop_left()
                    label.move(xl, img_25)
                elif img_3<yl<=img_4:
                    self.stop_left()
                    label.move(xl, img_35)
                elif img_4<yl<=img_5:
                    self.stop_left()
                    label.move(xl, img_45)
                elif img_5<yl<=img_6:
                    self.stop_left()
                    label.move(xl, img_55)
                else:
                    pass

    def spin_center(self):
        speed = 10

        for label in self.reel_label_c:
            xc = label.x()
            yc = label.y() + speed-2
            if yc >= 1200:
                yc = yc - 7*200
            label.move(xc, yc)

        
            if self.command == b'c\r\n':
                
                # print(f"信号きてる_c")
                if img_0<yc<=img_1:
                    self.stop_center()
                    label.move(xc, img_05)
                    
                elif img_1<yc<=img_2:
                    self.stop_center()
                    label.move(xc, img_15)
                elif img_2<yc<=img_3:
                    self.stop_center()
                    label.move(xc, img_25)
                elif img_3<yc<=img_4:
                    self.stop_center()
                    label.move(xc, img_35)
                elif img_4<yc<=img_5:
                    self.stop_center()
                    label.move(xc, img_45)
                elif img_5<yc<=img_6:
                    self.stop_center()
                    label.move(xc, img_55)
                else:
                    pass
    
    def spin_right(self):
        speed = 10

        for label in self.reel_label_r:
            xr = label.x()
            yr = label.y() + speed+2
            if yr >= 1200:
                yr = yr - 7*200
            label.move(xr, yr)

            if self.command == b'r\r\n':
                
                # print(f"信号きてる_r")
                if img_0<yr<=img_1:
                    self.stop_right()
                    label.move(xr, img_05)
                    
                elif img_1<yr<=img_2:
                    self.stop_right()
                    label.move(xr, img_15)
                elif img_2<yr<=img_3:
                    self.stop_right()
                    label.move(xr, img_25)
                elif img_3<yr<=img_4:
                    self.stop_right()
                    label.move(xr, img_35)
                elif img_4<yr<=img_5:
                    self.stop_right()
                    label.move(xr, img_45)
                elif img_5<yr<=img_6:
                    self.stop_right()
                    label.move(xr, img_55)
                else:
                    pass
        


    def stop_left(self):
        self.timer_l.stop()
    def stop_center(self):
        self.timer_c.stop()
    def stop_right(self):
        self.timer_r.stop()

    # def keyPressEvent(self, event):

    def __init__(self):
        super().__init__()

        #
        self.setWindowTitle("slot")
        self.resize(1600, 1200)                 
        # self.showFullScreen()
        self.setStyleSheet("background-color: #000000;") 

        self.setWindowFlags(Qt.FramelessWindowHint)  # ウィンドウの枠を非表示にする(あとで)
        self.setCursor(Qt.BlankCursor)  # カーソルを非表示にする（あとで
        # self.setDisabled(True)  # ウィンドウを無効化して操作できないようにする??


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
            image_label_l =ImageLabel(path)
            image_label_l.setFixedSize(400, 200)
            image_label_l.setStyleSheet("border: 2px solid black;")
            image_label_l.setParent(self)
            image_label_l.move(0, i * 200)
            self.reel_label_l.append(image_label_l)

        #中央
        for i, path in enumerate(image_paths):
            image_label_c =ImageLabel(path)
            image_label_c.setFixedSize(400, 200)
            image_label_c.setStyleSheet("border: 2px solid black;")
            image_label_c.setParent(self)
            image_label_c.move(440, i * 200)
            self.reel_label_c.append(image_label_c)

        #右
        for i, path in enumerate(image_paths):
            image_label_r =ImageLabel(path)
            image_label_r.setFixedSize(400, 200)
            image_label_r.setStyleSheet("border: 2px solid black;")
            image_label_r.setParent(self)
            image_label_r.move(880, i * 200)
            self.reel_label_r.append(image_label_r)
    

        self.start_spin()
        self.serial_open()
        


    







# =========================

app = QApplication(sys.argv)

window = Window()

# =========================
# 表示
# =========================
window.show()
sys.exit(app.exec())
