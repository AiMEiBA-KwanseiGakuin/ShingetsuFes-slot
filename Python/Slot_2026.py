""" Slot_2026.py
 スロットマシーンを作り直す
 画面表示:pygame
"""
import sys, os
import serial
import serial.tools.list_ports
#import numpy as np
import pygame
from pygame.locals import *
import gui_template as gui

USE_SERIAL=True
pic_folder=os.path.join(os.getcwd(),"img")
pic_type = ".jpeg"

class Real:
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
        self.img_ready = pygame.transform.scale(pygame.image.load(os.path.join(pic_folder,"ready_img"+pic_type)).convert_alpha(), width, height)
        self.state = "INIT"
        self.serial = serial.Serial(baudrate = 9600) #timeout = ...

        self.Reals = {
            "Left":  {"rotation": False, "real": Real((650, 0), [self.name_arr[i] for i in [
                4, 5, 4, 0, 2, 4, 5, 4, 3, 6, 4, 5, 4, 2, 0, 4, 5, 4, 5, 6, 1]], self.speed)},
            "Center":{"rotation": False, "real": Real((350, 0), [self.name_arr[i] for i in [
                3, 2, 4, 0, 5, 2, 4, 1, 5, 2, 4, 0, 5, 2, 4, 1, 5, 2, 4, 6, 5]], self.speed)},
            "Right": {"rotation": False, "real": Real(( 50, 0), [self.name_arr[i] for i in [
                5, 1, 3, 4, 5, 1, 3, 4, 5, 1, 3, 4, 5, 1, 3, 4, 5, 1, 0, 6, 4]], self.speed)},
        }
        
    def setup(self):
        while True:
            if self.startSerial(): break
        self.state = "READY"
        
    def loop(self):
        command = self.readCommand()
        match self.state:
            case "READY":
                self.screen.blit(self.img_ready, 0,0)
                if command == "start":
                    self.Reals["Left"]["rotation"] = True
                    self.Reals["Center"]["rotation"] = True
                    self.Reals["Right"]["rotation"] = True
                    self.state = "PLAY"
            case "PLAY":
                # draw reals
                self.Reals["Left"]["real"].draw()
                self.Reals["Center"]["real"].draw()
                self.Reals["Right"]["real"].draw()
                
                # stop reals
                self.Reals[command]["rotation"] = False
                if command == "Timeout":
                    self.Reals["Left"]["rotation"] = False
                    self.Reals["Center"]["rotation"] = False
                    self.Reals["Right"]["rotation"] = False
                
                # move reals
                if self.Reals["Left"]["rotation"]: self.Reals["Left"]["real"].move()
                if self.Reals["Center"]["rotation"]: self.Reals["Center"]["real"].move()
                if self.Reals["Right"]["rotation"]: self.Reals["Right"]["real"].move()
                
                # check if all reals are stopped
                if self.Reals["Right"]["rotation"] + self.Reals["Center"]["rotation"] + self.Reals["Left"]["rotation"] == 0:
                    self.state = "END"
            case "END":
                print(f"left real :{self.Reals["Left"]["real"].names[self.Reals["Left"]["real"].target_id]}")
                print(f"center real :{self.Reals["Center"]["real"].names[self.Reals["Center"]["real"].target_id]}")
                print(f"right real :{self.Reals["Right"]["real"].names[self.Reals["Right"]["real"].target_id]}")
                self.state = "READY"
        
    def typed(self, key, mod):
        if self.state == "PLAY":
            if key == K_q: self.Reals["Left"]["rotation"] = False
            if key == K_w: self.Reals["Center"]["rotation"] = False
            if key == K_e: self.Reals["Right"]["rotation"] = False
        
    def startSerial(self):
        ...
    
    def readCommand(self):
        match self.serial.readline():
            case b"S\r\n":# for start playing
                return "start"
            case b"R\r\n":# for stop right real
                return "Right"
            case b"C\r\n":# for stop center real
                return "Center"
            case b"L\r\n":# for stop left real
                return "Left"
            case b"T\r\n":# for timeout (= stop all real)
                return "Timeout"
            
    
