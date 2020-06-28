import pygame
import neat
import time
import os
import random

WIN_WIDTH = 600
WIN_HEIGHT = 800

BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))

class Bird:
    IMGS = BIRD_IMGS #Used for cycling through images
    MAX_ROTATION = 25 #Max rotation for bird
    ROT_VEL = 20 # How fast bird is rotating
    ANIMATION_TIME = 5 

    def __init__(self, x, y):
        self.x = x
        self.y = y #x and y are starting position
        self.tilt = 0 #How much image has tilted
        self.tick_count = 0 #Figure out physics for jumping and falling
        self.vel = 0 #Velocity
        self.height = self.y #Need for tilting and moving bird
        self.img_count = 0 #Determine which image is shown. Used for animaiting
        self.img = self.IMGS[0]
    
    def jump(self):
        #Function is used for jumping
        self.vel = -10.5 #Moves bird up
        self.tick_count = 0 #Keep track of when bird jumped
        self.height = self.y #Keep track of where bird jumped from

    def move(self):
        self.tick_count +=1 #Frame went by; tick happened
        d = self.vel*self.tick_count + 1.5 * self.tick_count**2 #Displacement formula 
        # Move right after jump: Velocity(-10.5) * time(tick_count(1)) + 1.5* time(tick_count(1))^2 || time^2 = 1 = 1^2 = 1
        #-10.5 + 1.5 = -9
        #Creates ark as it jumps.
        if d >= 16:
            #Terminal velocity
            d = 16 #Stop acceleration 
        if d < 0:
            d -=2 #if moving up. Move up a little bit more.
        self.y = self.y + d

        if d < 0 or self.y < self.height + 50:
            #tilt bird upwards
            #Record where bird jumped. If bird jumped above 50 still look like its jumping up
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
            else:
                #If not moving upwards and  don't want to tilt the bird upwards
                #Tilt downwwards
                if self.tilt > -90:
                    self.tilt -=self.ROT_VEL
                    #Allow bird to gradually rotate to 90 degress                    
        def draw(self, win):
            self.img_count += 1 #Need to record how many times has flap been shown

            if self.img_count < self.ANIMATION_TIME:
                # if less than 5 show first image
                self.img = self.IMGS[0]
            elif self.img_count < self.ANIMATION_TIME*2:
                #if less than 10 show second flappy bird
                self.img = self.IMGS[1]
            elif self.img_count < self.ANIMATION_TIME*3:
                #if less than 15 show last image
                self.img = self.IMGS[2]
            elif self.img_count < self.ANIMATION_TIME*4:
                #if less than 20 show second image
                self.img = self.IMGS[1]
            elif self.img_count < self.ANIMATION_TIME*4 + 1:
                #if less than 20 restart and show first image
                self.img = self.IMGS[0]
                self.img_count = 0
            #Loop checks what image to show to make the bird flap based on current image count

            if self.tilt <= -80:
                self.img =self.IMGS[1] #If the bird is titlted and looking down then do not cycle through and keep image constant
                self.img_count = self.ANIMATION_TIME*2 #Sets img count to 10 so it will not skip a frame.

            rotated_image = pygame.transform.rotate(self.img, self.tilt)  #rotate img for us
            new_rect = rotated_image.get_rect(center=self.img.get_rect)(topleft = (self.x, self.y).center) #Rotate around center center

            win.blit(rotated_image, new_rect.topleft) #How to rotate image

            def get_mask(self):
                return pygame.mask.from_surface(self.img)

def draw_window(win, bird):
    win.blit(BG_IMG, (0,0)) #blit means draw, 0,0 = top left corner
    bird.draw(win)
    pygame.display.update()

def main():
    bird = Bird(200,200) #takes starting position
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    
    run = True
    while run:
        for event in pygame.event.get():
            #When event happens check what it is. Event could be a mouse click
            if event.type == pygame.QUIT:
                run = False #If red X is clicked then stop running 

        draw_window(win, bird)
    
    pygame.quit() #Quit game
    quit() #quit program

main()