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
        
        """
        self.state
        self.level
        
        self.baoudrate
        """
        
    def setup(self):
        ...
        
    def loop(self):
        ...
        
    def typed(self, key, mod):
        ...
        
    def readCommand(self):
        ...
