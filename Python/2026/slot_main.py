import sys
import serial
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap

## QLabel,QPixmap画像  2:1
## ちいぱちCOM4

speed = 40
boost = 0


image_pathsl = [
    "bell.png",
    "replay.png",
    "mascat.png",
    "seven.png",
    "bar.png",
    "juggler.png",
    "mascat.png"
]

image_pathsc = [
    "mascat.png",
    "bar.png",
    "bell.png",
    "juggler.png",
    "replay.png",
    "seven.png",
    "bell.png"
]

image_pathsr = [
    "replay.png",
    "bar.png",
    "replay.png",
    "bell.png",
    "seven.png",
    "juggler.png",
    "mascat.png"
]


#使う数値
img_b05=-100
img_0=0;  img_05=100
img_1=200;img_15=300
img_2=400;img_25=500
img_3=600;img_35=700
img_4=800;img_45=900
img_5=1000;img_55=1100
img_6=1200;img_65=1300
img_7=1400;img_75=1500
img_8=1600


atari = "あたり"
ohatari="大当たり"
hazure= "はずれ"



# =========================
# 画像表示
# ========================
class ImageLabel(QLabel):

    def __init__(self, image_path):
        super().__init__()
        self.set_image(image_path)
        self.name = image_path  # 画像の名前を保持する属性を追加

    def set_image(self, image_path):
        image = QPixmap(image_path)


        self.setPixmap(image)
        self.setScaledContents(True)  #画像をラベルのサイズに合わせて拡大縮小する!





# =========================
# ウィンドウ
# =========================

class Window(QWidget):

    def serial_open(self):
        self.ser = serial.Serial("COM5", 9600, timeout=0)
        # self.ser.open()  ##うえのでもう開いてるらしい
        ##ないときもb'n\r\n'を受信
        self.timer_ser = QTimer(self)
        self.timer_ser.timeout.connect(self.get_serial)
        self.timer_ser.start(15)

    # key = "R"

    def start_spin(self):
        self.command = b''  # 初期化
        if self.is_spinning:
            return

        self.is_spinning = True
        self.key = None
        self.target_l=""
        self.target_c=""
        self.target_r=""
        self.target_label.hide()

        self.timer_l = QTimer(self)
        self.timer_l.timeout.connect(self.spin_left)
        self.timer_l.start(30)

        self.timer_c = QTimer(self)
        self.timer_c.timeout.connect(self.spin_center)
        self.timer_c.start(30)

        self.timer_r = QTimer(self)
        self.timer_r.timeout.connect(self.spin_right)
        self.timer_r.start(30)# 30

        

    def get_serial(self):
        self.command = self.ser.readline()
        self.ser.reset_input_buffer()
        print(self.command)
        if (not self.is_spinning and self.command == b's\r\n'):
            self.start_spin()
            self.target_label.hide()
            print("started")

    #回転ひだり
    def spin_left(self):

        stop=self.command == b'l\r\n' or self.key == 'A'
        for label in self.reel_label_l:

            if label.y() >= 1300:
                yl = -100#yl - 7*200            ##-=
            else:
                yl = label.y()

            xl = label.x()
            yl = yl + speed         ##x()ていう

            label.move(xl, yl)

        
            ##spinのなか↓     あとキーボード入力でも停止できるように

            if stop:
                
                yl = label.y()
                if yl<=img_0:
                    self.stop_left()
                    label.move(xl, img_b05)
                elif img_0<yl<=img_1:
                    self.stop_left()
                    label.move(xl, img_05)
                        
                elif img_1<yl<=img_2:
                    self.target_l = label.name
                    self.stop_left()
                    label.move(xl, img_15)
                    
                    print(label.name)
                    
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
               
                elif img_6<yl<=img_7:
                    self.stop_left()
                    label.move(xl, img_65)
              
                elif img_7<yl:
                    self.stop_left()
                    label.move(xl, img_75)
                 
                 
                else:
                    pass
        else:
            return

  
    #回転真ん中
    def spin_center(self):


        for label in self.reel_label_c:
            if label.y() >= 1300:
                yc = -100#yl - 7*200            ##-=
            else:
                yc = label.y()

            xc = label.x()
            yc = yc + speed         ##x()ていう

            label.move(xc, yc)

            if self.command == b'c\r\n' or self.key == 'S':
                                     
                yc = label.y()

                if yc<=img_0:
                    self.stop_center()
                    label.move(xc, img_b05)
                elif img_0<yc<=img_1:
                    self.stop_center()
                    label.move(xc, img_05)
                elif img_1<yc<=img_2:
                    
                    self.target_c = label.name
                    self.stop_center()
                    label.move(xc, img_15)
                    print(label.name)
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
                elif img_6<yc<=img_7:
                    self.stop_center()
                    label.move(xc, img_65)
                elif img_7<yc:
                     self.stop_center()
                     label.move(xc, img_75)    ##7=1400
                else:
                    print(f"error:{label.y()}")
                    pass
                    
                print(label.y())
        else:
            return
    
            # for label2 in self.reel_label_c[1:]:
            #     new_y = label2.y() + self.delta_c
            #     # リールの循環
            #     new_y = ((new_y + 200) % (1200 + 200)) - 200
            #     label2.move(label2.x(), new_y)
            # self.delta_c = 0
    #回転みぎ
    def spin_right(self):
        for label in self.reel_label_r:
            if label.y() >= 1300:
                yr = -100#yl - 7*200            ##-=
            else:
                yr = label.y()

            xr = label.x()
            yr = yr + speed         ##x()ていう
            label.move(xr, yr)

        if (self.command == b'r\r\n' or self.key == 'D'):
            #
            for label in self.reel_label_r:

                yr = label.y()

                if yr<=img_0:
                    self.stop_right()
                    label.move(xr, img_b05)
                elif img_0<yr<=img_1:
                    self.stop_right()
                    label.move(xr, img_05)
                elif img_1<yr<=img_2:
                    self.target_r = label.name
                    self.stop_right()
                    label.move(xr, img_15)
                    
                    print(label.name)
                                 
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
               
                elif img_6<yr<=img_7:
                    self.stop_right()
                    label.move(xr, img_65)
              
                elif img_7<yr:
                    self.stop_right()
                    label.move(xr, img_75)
                else:
                    pass
        else:
            return



    def stop_left(self):
        self.timer_l.stop()
        self.check_all_spin_stopped()
    def stop_center(self):
        self.timer_c.stop()
        self.check_all_spin_stopped()
    def stop_right(self):
        self.timer_r.stop()
        self.check_all_spin_stopped()




    def check_all_spin_stopped(self):

        if (    not self.timer_l.isActive()
            and not self.timer_c.isActive()
            and not self.timer_r.isActive()):

            self.is_spinning = False
            #delay 500ms
            print(self.target_r,self.target_c,self.target_l)

            if (self.target_l==self.target_c and self.target_c==self.target_r):
                print("あたり")
                self.target_label.setText(atari)
                self.target_label.setAlignment(Qt.AlignCenter)
                self.target_label.setStyleSheet("background-color: lightgray ; color:orange; font-size:80px;")
                self.target_label.resize(1600,100)
                self.target_label.move(0,350)
                self.target_label.raise_()
                self.target_label.show()

                if (self.target_c == "seven.png"):
                    self.target_label.hide()
                    print("大当たり")
                    #self.target_label =QLabel(ohatari,self)
                    self.target_label.setText(ohatari)
                    self.target_label.setAlignment(Qt.AlignCenter)
                    # self.target_label.setStyleSheet("background-color: lightgray ; color:orange; font-size:80px;")
                    # self.target_label.resize(1600,100)
                    # self.target_label.move(0,350)
                    self.target_label.raise_()
                    self.target_label.show()
                    print(self.target_r)
            # elif (self.target_l == "seven.png" 
            #       and self.target_c == "seven.png" 
            #       and self.target_r=="seven.png"):
            #     print("大当たり")
            #     #self.target_label =QLabel(ohatari,self)
            #     self.target_label.setText(ohatari)
            #     self.target_label.setAlignment(Qt.AlignCenter)
            #     self.target_label.setStyleSheet("background-color: lightgray ; color:orange; font-size:80px;")
            #     self.target_label.resize(1600,100)
            #     self.target_label.move(0,350)
            #     self.target_label.raise_()
            #     self.target_label.show()
            #     print(self.target_r)
            else:
                #self.target_label =QLabel(hazure,self)
                self.target_label.setText(hazure)
                self.target_label.setAlignment(Qt.AlignCenter)
                self.target_label.setStyleSheet("background-color: lightgray ; color:orange; font-size:80px;")
                print("はずれ")
                self.target_label.resize(1600,100)
                self.target_label.move(0,350)
                self.target_label.raise_()
                self.target_label.show()
                print(self.target_r)
                                

            ##isActive()はQTimer




    #=========================
    #keyPressEvent
    #=========================
        ##eventそのままつかえる override
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_A:
            self.key = "A"
        elif event.key() == Qt.Key_S:
            self.key = "S"
        elif event.key() == Qt.Key_D:
            self.key = "D"
        elif event.key() == Qt.Key_R:
            if not self.is_spinning:
                self.start_spin()
                self.target_label.hide()
                print("started")
        else:
            self.key =None


    def __init__(self):
        super().__init__()

        
        self.setWindowTitle("slot")
        self.resize(1600, 1200)                 
        self.showFullScreen()
        self.setStyleSheet("background-color: #000000;") 

        self.setWindowFlags(Qt.FramelessWindowHint)  # ウィンドウの枠を非表示にする(あとで)
        # self.setCursor(Qt.BlankCursor)  # カーソルを非表示にする（あとで
        


        
        self.reel_labels = []

        self.reel_label_l=[]
        self.reel_label_c=[]
        self.reel_label_r=[]
        self.target_label = QLabel("",self)

        #左
        for i, path in enumerate(image_pathsl):
            image_label_l =ImageLabel(path)
            image_label_l.setFixedSize(400, 200)
            # image_label_l.setStyleSheet("border: 2px solid black;")
            image_label_l.setParent(self)
            image_label_l.move(0, i * 200)
            self.reel_label_l.append(image_label_l)

        #中央
        for i, path in enumerate(image_pathsc):
            image_label_c =ImageLabel(path)
            image_label_c.setFixedSize(400, 200)
            # image_label_c.setStyleSheet("border: 2px solid black;")
            image_label_c.setParent(self)
            image_label_c.move(440, i * 200)
            self.reel_label_c.append(image_label_c)

        #右
        for i, path in enumerate(image_pathsr):
            image_label_r =ImageLabel(path)
            image_label_r.setFixedSize(400, 200)
            # image_label_r.setStyleSheet("border: 2px solid black;")
            image_label_r.setParent(self)
            image_label_r.move(880, i * 200)
            self.reel_label_r.append(image_label_r)


    
        self.is_spinning = False


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
