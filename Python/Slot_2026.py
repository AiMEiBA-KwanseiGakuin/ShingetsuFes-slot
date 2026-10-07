""" Slot_2026.py
 スロットマシーンを作り直す
 画面表示:pygame
 シリアル通信:PySerial
"""
import sys, os
import serial
import serial.tools.list_ports
import pygame
from pygame.locals import *
import gui_template as gui

USE_SERIAL=False
pic_folder=os.path.join(os.getcwd(),"img")
pic_type = ".jpeg"

class Reel:
    def __init__(self, area_topleft, pic_name_arr, speed):
        self.pic_size = (150,300)
        self.names = pic_name_arr
        self.imgs = [ pygame.transform.scale(
                        pygame.image.load(os.path.join(pic_folder,name+pic_type)).convert_alpha(),
                        *self.pic_size) 
                     for name in pic_name_arr ]
        self.origin = area_topleft
        self.diff_pos = 0
        self.speed = speed
        self.target_id = 0 
        
    def draw(self, screen):
        # 一旦3枚分だけ描画
        screen.blit(self.imgs[self.target_id-2], (self.origin[0], self.origin[1] - self.pic_size[1] + self.diff_pos))
        screen.blit(self.imgs[self.target_id-1], (self.origin[0], self.origin[1] + self.diff_pos))
        screen.blit(self.imgs[self.target_id], (self.origin[0], self.origin[1] + self.pic_size[1] + self.diff_pos))
        screen.blit(self.imgs[(self.target_id+1) % len(self.imgs)],
                    (self.origin[0], self.origin[1] + (self.pic_size[1]*2) + self.diff_pos))
        
    def move(self):
        self.diff_pos = (self.diff_pos + self.speed) % (self.pic_size[1]*3)
        if self.diff_pos > self.pic_size[1] /2: self.target_id = (self.target_id + 1) % len(self.imgs)
    
    def setTarget(self, target_id):
        self.target_id = target_id
        self.diff_pos = 0

class Slot(gui.GUI):
    name_arr = ["bar", "bell", "cerry", "juggler", "mascat", "replay", "seven"]
    def __init__(self, width=920, height=490+200):
        super().__init__(width, height, title="Slot Machine", bg=(0,0,0), typekey=True)
        self.speed = 2        
        #self.img_ready = pygame.transform.scale(pygame.image.load(os.path.join(pic_folder,"ready_img"+pic_type)).convert_alpha(), width, height)
        self.state = "INIT"
        self.serial = serial.Serial(baudrate = 9600, timeout = 0.5)


        self.Reels = {
            "Left":  {"rotation": False, "reel": Reel((650, 0), [self.name_arr[i] for i in [
                4, 5, 4, 0, 2, 4, 5, 4, 3, 6, 4, 5, 4, 2, 0, 4, 5, 4, 5, 6, 1]], self.speed)
            },
            "Center":{"rotation": False, "reel": Reel((350, 0), [self.name_arr[i] for i in [
                3, 2, 4, 0, 5, 2, 4, 1, 5, 2, 4, 0, 5, 2, 4, 1, 5, 2, 4, 6, 5]], self.speed)
            },
            "Right": {"rotation": False, "reel": Reel(( 50, 0), [self.name_arr[i] for i in [
                5, 1, 3, 4, 5, 1, 3, 4, 5, 1, 3, 4, 5, 1, 3, 4, 5, 1, 0, 6, 4]], self.speed)
            }
        }
        
    def setup(self):
        while USE_SERIAL:
            if self.startSerial(): break
        self.state = "READY"
        
    def loop(self):
        command = self.readCommand()
        print(f"Command: {command}")
        match self.state:
            case "READY":
                self.screen.blit(self.img_ready, 0,0)
                if command == "start":
                    self.Reels["Left"]["rotation"] = True
                    self.Reels["Center"]["rotation"] = True
                    self.Reels["Right"]["rotation"] = True
                    self.state = "PLAY"
            case "PLAY":
                # draw reels
                self.Reels["Left"]["reel"].draw()
                self.Reels["Center"]["reel"].draw()
                self.Reels["Right"]["reel"].draw()
                
                # stop reals
                if command != "Unknown":
                    self.Reels[command]["rotation"] = False
                    if command == "Timeout":
                        print("TimeOut!")
                        self.Reels["Left"]["rotation"] = False
                        self.Reels["Center"]["rotation"] = False
                        self.Reels["Right"]["rotation"] = False
                
                # move reals
                if self.Reels["Left"]["rotation"]: self.Reels["Left"]["reel"].move()
                if self.Reels["Center"]["rotation"]: self.Reels["Center"]["reel"].move()
                if self.Reels["Right"]["rotation"]: self.Reels["Right"]["reel"].move()
                
                # check if all reals are stopped
                if self.Reels["Right"]["rotation"] + self.Reels["Center"]["rotation"] + self.Reels["Left"]["rotation"] == 0:
                    self.state = "END"
            case "END":
                print("left reel :",end = "")
                print(self.Reels["Left"]["reel"].names[self.Reels["Left"]["reel"].target_id])
                print("center reel :",end = "")
                print(self.Reels["Center"]["reel"].names[self.Reels["Center"]["reel"].target_id])
                print("right reel :",end = "")
                print(self.Reels["Right"]["reel"].names[self.Reels["Right"]["reel"].target_id])
                self.state = "READY"
        
    def typed(self, key, mod):
        if self.state == "READY":
            self.Reels["Left"]["rotation"] = True
            self.Reels["Center"]["rotation"] = True
            self.Reels["Right"]["rotation"] = True
            self.state = "PLAY"
        if self.state == "PLAY":
            if key == K_q: self.Reels["Left"]["rotation"] = False
            if key == K_w: self.Reels["Center"]["rotation"] = False
            if key == K_e: self.Reels["Right"]["rotation"] = False
        
    def startSerial(self):
        ports = list(serial.tools.list_ports.comports())
        for p in ports:
            if "Arduino" in p.description:
                self.serial.port = p.device
                self.serial.open()
                print(f"Serial port {p.device} opened.")
                return True
        print("No Arduino found. Please connect the device.")
        return False
    
    def readCommand(self):
        if not USE_SERIAL:
            return "Unknown"
        if not self.serial.is_open:
            print("Serial port is not open.")
            return "Unknown"
        match self.serial.readline():
            case b"S\r\n":# for start playing
                return "start"
            case b"R\r\n":# for stop right reel
                return "Right"
            case b"C\r\n":# for stop center reel
                return "Center"
            case b"L\r\n":# for stop left reel
                return "Left"
            case b"T\r\n":# for timeout (= stop all reels)
                return "Timeout"
            case _:
                return "Unknown"

if __name__ == "__main__":
    slot = Slot()
    slot.main()
