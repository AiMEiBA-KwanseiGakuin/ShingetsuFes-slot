import pygame,sys
from pygame.locals import *

class GUI:
    Numbers={K_0:0,K_1:1,K_2:2,K_3:3,K_4:4,K_5:5,K_6:6,K_7:7,K_8:8,K_9:9,
                K_KP0:0,K_KP1:1,K_KP2:2,K_KP3:3,K_KP4:4,K_KP5:5,K_KP6:6,K_KP7:7,K_KP8:8,K_KP9:9}
    Arrows={K_UP:"up",K_DOWN:"down",K_RIGHT:"right",K_LEFT:"left",
                K_w:"up",K_s:"down",K_a:"left",K_d:"right"}
    def __init__(self,width,height,**kwargs):
        pygame.init()
        self.winsize=(width,height)
        self.option=kwargs.get("option",0)
        self.screen=pygame.display.set_mode((width,height),self.option)
        pygame.display.set_caption(kwargs.get("title","title"))
        self.color_bg=kwargs.get("bg",(0,0,0))
        
        self.fps=kwargs.get("fps",60)
        self.clock=pygame.time.Clock()
        
        self.mouse=kwargs.get("mouse")
        self.onkey=kwargs.get("onkey")
        self.typekey=kwargs.get("typekey")
        
        self.running=True
        
    def main(self):
        self.setup()
        #self.step=0
        while self.running:
            #self.step+=1
            self.loop()
            
            if self.onkey:
                self.pressed(pygame.key.get_pressed())
                
            for event in pygame.event.get():
                if self.mouse and event.type==MOUSEBUTTONDOWN:
                    self.clicked(pygame.mouse.get_pos(),event.button)
                
                if self.mouse and event.type==MOUSEMOTION:
                    self.draged(pygame.mouse.get_pos(),pygame.mouse.get_pressed())
                elif self.mouse:
                    self.undraged(pygame.mouse.get_pos(),pygame.mouse.get_pressed())
                
                if self.typekey and event.type==KEYDOWN:
                    self.typed(event.key,event.mod)

                if event.type==QUIT:
                    pygame.quit()
                    sys.exit()
                    
            self.clock.tick(self.fps)
            pygame.display.update()

    def setup(self):
        ...

    def loop(self):
        self.screen.fill(self.color_bg)
    
    def clicked(self,pos,button):
        ...
        
    def draged(self,pos,state):
        ...

    def undraged(self,pos,state):
        ...

    def pressed(self,keys):
        self.keys=keys
        ...

    def typed(self,key,mod):
        ...
        
