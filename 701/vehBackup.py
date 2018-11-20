import pygame
import time, sys
import math
import paho.mqtt.client as mqtt
from graphics import *

pygame.init()

display_width = 1024
display_height = 682

white = (255,255,255)
green = (0,255,0)
red = (255,0,0)
yellow=(255,255,0)
gray=(150,150,150)

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Vehicle Simulation')
clock=pygame.time.Clock()

mapImg=pygame.image.load('map.jpg')




def background():
        gameDisplay.blit(mapImg,(0,0))

def car(carx,cary):
        pygame.draw.circle(gameDisplay, green,(carx,cary),20)


def speed_detect(x1,y1,x2,y2):
        v=math.sqrt((x2-x1)*(x2-x1)+(y2-y1)*(y2-y1))
        return v

def text_objects(text, font):
        textSurface=font.render(text, True, white)
        return textSurface, textSurface.get_rect()

def time_display(text):
        largeText=pygame.font.Font('freesansbold.ttf',50)
        TextSurf, TextRect=text_objects(text,largeText)
        TextRect.center=(100,100)
        gameDisplay.blit(TextSurf, TextRect)

def speed_display(text):
        largeText=pygame.font.Font('freesansbold.ttf',50)
        TextSurf, TextRect=text_objects(text,largeText)
        TextRect.center=(100,140)
        gameDisplay.blit(TextSurf, TextRect)


def game_loop():
        
        car1_startx = 100
        car1_starty = 650
        car1_xspeed = 10
        car1_yspeed = -5
        
        carx1=0
        cary1=0
        exit= False
        
        while not exit:
            gameDisplay.blit(mapImg,(0,0))
               
                     
            car(car1_startx, car1_starty)
                            
            car1_startx += car1_xspeed
            car1_starty += car1_yspeed

            timeOri=0
            time1=timeOri
            time=pygame.time.get_ticks()
            time1=int(time)
            t1=str(time1/1000)
            if time1>timeOri:
                    speed1=speed_detect(carx1,cary1,car1_startx,car1_starty)
                    carx1=car1_startx
                    cary1=car1_starty
            time_display(t1)
            v1=str(speed1)
            speed_display(v1)
            if car1_startx > display_width:
                    car1_startx=0
                    car1_starty=650
            pygame.display.update()
            clock.tick(60)


game_loop()
pygame.quit()
quit()
            
            
