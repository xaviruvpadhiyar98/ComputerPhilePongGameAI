#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 19:37:38 2020

@author: Dhruv Padhiyar
"""


import pygame
from random import randint
import pandas as pd
from sklearn.neighbors import KNeighborsRegressor

#   Variables
WIDTH = 800
HEIGHT = 400
bgColor = pygame.Color('black')
fgColor = pygame.Color('white')


# Classes

class Ball:
    RADIUS = 10
    SCORE = 0
    velocity = [randint(4,8),randint(-8,8)]
    
    def __init__(self,x,y):
        self.x = x
        self.y = y
        
    def show(self, color):
        pygame.draw.circle(screen, color, (self.x, self.y), self.RADIUS)

    def update(self):
        ball.show(bgColor)

        if self.x > WIDTH:
            self.x = WIDTH//2
            self.y = HEIGHT//2
            self.SCORE = 0
            
        elif self.x < 0:
            self.velocity[0] = -self.velocity[0]
        elif self.y > HEIGHT or self.y < 0:
            self.velocity[1] = -self.velocity[1]
            
        elif self.x + self.RADIUS > WIDTH - Paddle.WIDTH and abs(self.y - paddle.y) < Paddle.HEIGHT//2:
            ball.bounce()
            self.SCORE += 1
            
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        ball.show(fgColor)

    def bounce(self):
        self.velocity[0] = -self.velocity[0]
        self.velocity[1] = randint(-8,8)
    
class Paddle:
    WIDTH = 20
    HEIGHT = 100
    BORDER = 10

    def __init__(self, y):
        self.y = y
    
    def show(self, color):
        pygame.draw.rect(screen, color, pygame.Rect(WIDTH-self.WIDTH, self.y-self.HEIGHT//2, self.BORDER,HEIGHT//5))
        
    def update(self,mouse):
        self.show(bgColor)
        #self.y = pygame.mouse.get_pos()[1]
        self.y = mouse
        self.show(fgColor)   
        

    
#   Initalize PYGAME
pygame.init()

#   Initalize Screen
screen = pygame.display.set_mode((WIDTH,HEIGHT))

#   Screen Name
pygame.display.set_caption("Pong")


#   Background Elements of Screen
ball = Ball(WIDTH//2, HEIGHT//2)
paddle = Paddle(HEIGHT//2)

clock = pygame.time.Clock()


#   DATA SCIENCE STUFF
pong = pd.read_csv("game.csv")
pong = pong.drop_duplicates()
x = pong.drop(columns="Paddle.y")
y = pong["Paddle.y"]

clf = KNeighborsRegressor(n_neighbors=3)
clf.fit(x,y)
df = pd.DataFrame(columns=['x','y','vx','vy'])


#   Close Window Event Capture
while True:
    
    screen.fill(bgColor)
    
    e = pygame.event.poll()
    if e.type == pygame.QUIT:
        break
    #with open('game.csv','a') as f:
    #    f.write(str(ball.x) + "," + str(ball.y) + "," + str(ball.velocity[0]) + "," + str(ball.velocity[1]) + "," + str(paddle.y) + "\n")
    
    toPredict = df.append({'x':ball.x, 'y':ball.y, 'vx': ball.velocity[0], 'vy':ball.velocity[1]}, ignore_index=True)
    shouldMove = clf.predict(toPredict)

    paddle.update(int(shouldMove))
    
    
    ball.update()
    #paddle.update()
    font = pygame.font.Font(None, 74)
    text = font.render(str(ball.SCORE), 1, fgColor)
    screen.blit(text, (WIDTH//2,10))
    pygame.display.flip()
    
    clock.tick(60)
pygame.quit()