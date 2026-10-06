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

#use_arduino=True
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
        self.real_idx = [
            [4, 5, 4, 0, 2, 4, 5, 4, 3, 6, 4, 5, 4, 2, 0, 4, 5, 4, 5, 6, 1], # left
            [3, 2, 4, 0, 5, 2, 4, 1, 5, 2, 4, 0, 5, 2, 4, 1, 5, 2, 4, 6, 5], # center
            [5, 1, 3, 4, 5, 1, 3, 4, 5, 1, 3, 4, 5, 1, 3, 4, 5, 1, 0, 6, 4]  # right
        ]
        self.LeftReal =  Real((650, 0), [self.name_arr[i] for i in self.real_idx[0]], self.speed)
        self.CenterReal= Real((350, 0), [self.name_arr[i] for i in self.real_idx[1]], self.speed)
        self.RightReal = Real(( 50, 0), [self.name_arr[i] for i in self.real_idx[2]], self.speed)
        
        self.img_ready = pygame.transform.scale(pygame.image.load(os.path.join(pic_folder,"ready_img"+pic_type)).convert_alpha(), width, height)
        
        self.state = "INIT"
        self.real_state = [false, false, flase]
        self.serial = serial.Serial(baudrate = 9600) #timeout = ...
        
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
                    self.real.state = [True, True, True]
                    self.state = "PLAY"
            case "PLAY":
                self.LeftReal.draw()
                self.CenterReal.draw()
                self.RightReal.draw()
                
                self.real_state = [command == cmd for cmd in ["left", "center", "right"]]
                
                if self.real_state[0]: self.LeftReal.move()
                if self.real_state[1]: self.CenterReal.move()
                if self.real_state[2]: self.RightReal.move()
                
                if self.real_state == [False, False, False]: self.state = "END"
            case "END":
                print(f"left real :{self.LeftReal.names[self.LeftRsal.target_id]}")
                print(f"center real :{self.CenterReal.names[self.CenterReal.target_id]}")
                print(f"right real :{self.RightReal.names[self.RightReal.target_id]}")
                self.state = "READY"
                self.real_state = [False, False, False]
        
    def typed(self, key, mod):
        if key == K_q: self.real_state[0] = false
        if key == K_w: self.real_state[1] = false
        if key == K_e: self.real_state[2] = false
        
    def startSerial(self):
        
    
    def readCommand(self):
        match self.serial.readline():
            case b"S\r\n": # for start playing
            case b"R\r\n": # for stop right real
            case b"C\r\n": # for stop center real
            case b"L\r\n": # for stop left real
            case b"T\r\n": # for timeout (= stop all real)
            
    
