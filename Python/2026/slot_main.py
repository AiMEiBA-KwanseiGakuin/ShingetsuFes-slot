import sys
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap


## QMainWindow??違った ,  QLabel,QPixmap画像

image_paths = [
    "0.jpg",
    "1.jpg",
    "2.jpg",
    "3.jpg",
    "4.jpg",
    "5.jpg",
    "6.jpg"
]

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


# label = ImageLabel(image_paths[0])
#  # 別の画像に変更する
# label.set_image(image_paths[1]) ##やめ


# =========================
# ウィンドウ
# =========================

class Window(QWidget):

    def __init__(self):
        super().__init__()

        #
        self.setWindowTitle("slot")
        self.resize(800, 600)                 ##4:3にする(あとで)

        self.setStyleSheet("background-color: #000000;") 

        self.setWindowFlags(Qt.FramelessWindowHint)  # ウィンドウの枠を非表示にする
        self.setCursor(Qt.BlankCursor)  # カーソルを非表示にする
        #self.setDisabled(True)  # ウィンドウを無効化して操作できないようにする??



        self.reel_labels = []
        for _ in range(3):
            images = [ImageLabel(path) for path in image_paths]
            self.reel_labels.append(images)

        main_layout = QHBoxLayout()
        for images in self.reel_labels:
            reel_layout = QVBoxLayout()
            for image_label in images:
                image_label.setFixedSize(230,230)
                reel_layout.addWidget(image_label)
                image_label.setStyleSheet("border: 5px solid white;")  #リールの境界線 白
                
                reel_layout.setAlignment(Qt.AlignCenter)  # リールの中央に配置（意味ない希ガス
                #reel_layout.setContentsMargins(0, 0, 0, 0)  # リールの余白
                reel_layout.setSpacing(0)  # リールの間隔を0に設定

            main_layout.addLayout(reel_layout)

        # self.reels= [
        #     image_paths.copy(),
        #     image_paths.copy(),
        #     image_paths.copy()
        # ]
        # for reel in self.reels:
        #     reel.setFixedSize(200, 200)
        #     reel.setStyleSheet("border: 1px solid white;")  # リールの境界線 白

        # 横並びに配置する
        # layout = QHBoxLayout()
        # for reel in self.reels:
        #     layout.addWidget(reel)

        self.setLayout(main_layout)





# =========================
# くるくるQTimer
# =========================

class ReelsTimer():

    def __init__(self, ):
        super().__init__()

        # 
        #self

    # =========================
    # 
    # =========================

    #def 
    # =========================
    # 
    # =========================

    #def 

    # =========================
    # 
    # =========================

    #def 

    # =========================
    # 
    # =========================


    # =========================
    # 
    # =========================


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
# 
# ========================





# =========================
# 表示
# =========================

window.show()

sys.exit(app.exec())