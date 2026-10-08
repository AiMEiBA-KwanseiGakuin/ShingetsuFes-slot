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
pic_folder=os.path.join(os.getcwd(),"Python","img")
pic_type = ".jpeg"

class Reel:
    def __init__(self, area_topleft, pic_name_arr, speed):
        self.pic_size = (300,150)
        self.names = pic_name_arr
        self.imgs = [ pygame.transform.scale(
                        pygame.image.load(os.path.join(pic_folder,name+pic_type)).convert_alpha(),
                        self.pic_size) 
                     for name in pic_name_arr ]
        self.origin = area_topleft
        self.diff_pos = 0
        self.speed = speed
        self.target_id = 0
        self.will_stop = False
        self.is_move = False
        
    def draw(self, screen):
        screen.blit(self.imgs[(self.target_id+2) % len(self.imgs)], (self.origin[0], self.origin[1] - self.pic_size[1] + self.diff_pos))
        screen.blit(self.imgs[(self.target_id+1) % len(self.imgs)], (self.origin[0], self.origin[1] + self.diff_pos))
        screen.blit(self.imgs[self.target_id], (self.origin[0], self.origin[1] + self.pic_size[1] + self.diff_pos))
        screen.blit(self.imgs[self.target_id-1], (self.origin[0], self.origin[1] + (self.pic_size[1]*2) + self.diff_pos))
        screen.blit(self.imgs[self.target_id-2], (self.origin[0], self.origin[1] + (self.pic_size[1]*3) + self.diff_pos))
        
    def move(self):
        if not self.is_move: return
        self.diff_pos = self.diff_pos + self.speed
        if self.diff_pos > self.pic_size[1]:
            self.diff_pos -= self.pic_size[1]
            self.target_id = (self.target_id + 1) % len(self.imgs)
        if self.will_stop and self.diff_pos - self.pic_size[1] < self.speed:
            self.target_id = (self.target_id + 1) % len(self.imgs)
            self.diff_pos = 0
            self.will_stop = False
            self.is_move = False
        print(f"target_id: {self.target_id}, diff_pos: {self.diff_pos}, will_stop: {self.will_stop}, is_move: {self.is_move}")
    
    def setTarget(self, target_id):
        self.is_move = True
        self.target_id = target_id
        self.diff_pos = 0
    
    def setStop(self):
        if self.is_move: self.will_stop = True
    
class Slot(gui.GUI):
    name_arr = ["bar", "bell", "cerry", "juggler", "mascat", "replay", "seven"]
    def __init__(self, width=870, height=500):
        super().__init__(width, height, title="Slot Machine", bg=(0,0,0), typekey=True, fps=60)
        self.speed = 30
        ##self.img_ready = pygame.transform.scale(pygame.image.load(os.path.join(pic_folder,"ready_img"+pic_type)).convert_alpha(), width, height)
        self.state = "INIT"
        self.serial = serial.Serial(baudrate = 9600, timeout = 0.5)

        self.LeftReel = Reel((0,25), [self.name_arr[i] for i in [
            4, 5, 4, 0, 2, 4, 5, 4, 3, 6, 4, 5, 4, 2, 0, 4, 5, 4, 5, 6, 1]], self.speed)
        self.CenterReel = Reel((300,25), [self.name_arr[i] for i in [
            3, 2, 4, 0, 5, 2, 4, 1, 5, 2, 4, 0, 5, 2, 4, 1, 5, 2, 4, 6, 5]], self.speed)
        self.RightReel = Reel((600,25), [self.name_arr[i] for i in [
            5, 1, 3, 4, 5, 1, 3, 4, 5, 1, 3, 4, 5, 1, 3, 4, 5, 1, 0, 6, 4]], self.speed)
        
    def setup(self):
        while USE_SERIAL:
            if self.startSerial(): break
        self.state = "READY"
        
    def loop(self):
        command = self.readCommand()
        if command != "Unknown": print(f"Command: {command}")
        match self.state:
            case "READY":
                self.screen.fill((150,0,0),(200,100,470,250))
                ###self.screen.blit(self.img_ready, 0,0)
                if command == "start":
                    self.LeftReel.setTarget(0)
                    self.CenterReel.setTarget(0)
                    self.RightReel.setTarget(0)
                    self.state = "PLAY"
                    
            case "PLAY":
                # move reals
                self.LeftReel.move()
                self.CenterReel.move()
                self.RightReel.move()

                # draw reels
                self.screen.fill(self.color_bg)
                self.LeftReel.draw(self.screen)
                self.CenterReel.draw(self.screen)
                self.RightReel.draw(self.screen)

                # stop reals
                match command:
                    case "Left":
                        self.LeftReel.setStop()
                    case "Center":
                        self.CenterReel.setStop()
                    case "Right":
                        self.RightReel.setStop()
                    case "Timeout":
                        print("TimeOut!")
                        self.LeftReel.setStop()
                        self.CenterReel.setStop()
                        self.RightReel.setStop()
                    case _:
                        print(f"Unknown command: {command}")                
                
                # check if all reals are stopped
                if not self.LeftReel.is_move and not self.CenterReel.is_move and not self.RightReel.is_move:
                    self.state = "END"
                    print("left reel :",end = "")
                    print(self.LeftReel.names[self.LeftReel.target_id])
                    print("center reel :",end = "")
                    print(self.CenterReel.names[self.CenterReel.target_id])
                    print("right reel :",end = "")
                    print(self.RightReel.names[self.RightReel.target_id])
                    
            case "END":
                if command == "start":
                    self.LeftReel.setTarget(0)
                    self.CenterReel.setTarget(0)
                    self.RightReel.setTarget(0)
                    self.state = "PLAY"
        
    def typed(self, key, mod):
        if self.state == "READY" or self.state == "END" and key == K_RETURN:
            self.LeftReel.setTarget(0)
            self.CenterReel.setTarget(0)
            self.RightReel.setTarget(0)
            self.state = "PLAY"
        if self.state == "PLAY":
            if key == K_q or key == K_SPACE: self.LeftReel.setStop()
            if key == K_w or key == K_SPACE: self.CenterReel.setStop()
            if key == K_e or key == K_SPACE: self.RightReel.setStop()
        
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
