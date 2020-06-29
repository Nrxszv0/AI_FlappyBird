import neat
import os
import random
import time
import pygame

pygame.font.init()

WIN_WIDTH = 500
WIN_HEIGHT = 800

GEN = 0

BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))) , pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))

STAT_FONT = pygame.font.SysFont("comicsans", 50)
class Bird:
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]

    def jump(self):
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y
    
    def move(self):
        self.tick_count += 1
        displacement = self.vel * self.tick_count + 1.5 * self.tick_count**2

        if displacement >= 16:
            displacement = 16
        if displacement < 0 :
            displacement-=2

        self.y = self.y + displacement

        if displacement < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL
    
    def draw(self, win):
        self.img_count +=1
        
        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME * 2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME * 3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME * 4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME * 4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        if self.tilt <= -80:
            self.img = self.IMGS[1] 
            self.img_count = self.ANIMATION_TIME*2

        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft = (self.x, self.y)).center)           
        win.blit(rotated_image, new_rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)

class Pipe:
    GAP = 200 #Space between pipes
    VEL = 5 #speed pipes move to bird

    def __init__(self,x):
        self.x = x
        self.height = 0

        self.top = 0 #Where top part of pipe is drawn
        self.bottom = 0 #Where bottom part of pipe is drawn
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True) #Flipping pipe so it lookes upside down. # the top pipe is flipped
        self.PIPE_BOTTOM = PIPE_IMG #Bottom pipe image does not need to be flipped

        self.passed = False #Check if the bird has passed the pipe
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 450) #Random height between 50 and 450
        self.top = self.height - self.PIPE_TOP.get_height() #Figure out top left position. Probably drawing in a negative location
        self.bottom = self.height + self.GAP #Adds gap position to the height. 
    
    def move(self):
        self.x -= self.VEL

    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))#Draws top pipe at the x and top coordinates
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom)) #Draws bottom pipe at the x and bottom coordinates

    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (self.x - bird.x, self.top - round(bird.y)) # cant have decimal numbers so bird is rounded. 
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y)) #no dedimals 
        #Offsets are how far away the top left corners are from each other

        b_point = bird_mask.overlap(bottom_mask, bottom_offset) # Check if masks collide. Find point of collision. If they don't collide then the overlap function will return none.
        t_point = bird_mask.overlap(top_mask, top_offset)

        if t_point or b_point:
            #return true if bird collided with either tube
            return True 
        
        return False

class Base:
    VEL = 5 #Needs to be the same as the pipe so it doesn't look like they are moving at different speeds
    WIDTH = BASE_IMG.get_width() #Gets width of base image
    IMG = BASE_IMG

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH
    
    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL
        #Moves the two bases at two velocities to the left.

        if self.x1 + self.WIDTH < 0:
            #Checks if the first base has gone of the screen and when it does it brings it behind the second base 
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            #Checks if the second base has gone of the screen and when it does it brings it behind the first base 
            self.x2 = self.x1 + self.WIDTH
    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y)) #Draws first base
        win.blit(self.IMG, (self.x2, self.y)) #Draws second base

def draw_window(win, birds, pipes, base, score, gen):
    win.blit(BG_IMG, (0,0))

    for pipe in pipes:
        pipe.draw(win)

    text = STAT_FONT.render("Score: "+ str(score), 1, (255,255,255))
    win.blit(text,(WIN_WIDTH - 10 - text.get_width(), 10)) #Will always fit on screen. Drawn  10 pixels large

    text = STAT_FONT.render("Generation: "+ str(gen), 1, (255,255,255))
    win.blit(text,(10, 10)) #Drawn at 10,10 Drawn  10 pixels large

    base.draw(win)

    for bird in birds:
        bird.draw(win)
    pygame.display.update()

def main(genomes, config):
    global GEN
    GEN += 1
    nets = [] #neural networks tracking
    ge = [] #genome tracking
    birds =[] 
    #genomes is a tupple with a genome id. Ex. (1, genome object) only care about genome object
    for _,g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        birds.append(Bird(230, 350))
        g.fitness = 0
        ge.append(g)
        

    base = Base(730)
    pipes = [Pipe(600)]
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()

    score = 0

    run = True
    while run:
        clock.tick(30) # ticks 30 times per second. 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        # bird.move()
        pipe_ind = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                #if first pipe is passed then focus on second pipe
                pipe_ind = 1
        else:
            #if no birds left stop running
            run = False
            break
        
        for x, bird in enumerate(birds):
            bird.move()
            ge[x].fitness += 0.1 #every second it gets one fitness point. Encourage survival

            output = nets[x].activate((bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom))) #creates output determined by bird's y position, bird's distance to top pipe, and birds distance to bottom pipe.
            #output is a list. There is only one output for this program but other programs could have more in the list
            if output[0] > 0.5:
                bird.jump() #bird will jump if output is greater than .5
        add_pipe = False
        rem =[] #list of pipes to remove
        for pipe in pipes:
            for x, bird in enumerate(birds):
                if pipe.collide(bird):
                    #if bird collides
                    ge[x].fitness -=1 # Every time bird hits pipe 1 fitness is removed
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x) #removes bird from lists
            
                if not pipe.passed and pipe.x < bird.x:
                    #Check if bird passed the pipe
                    pipe.passed = True
                    add_pipe = True

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                #If the pipe is totally off the screen
                rem.append(pipe) #Adds pipe to the remove list for removal

            pipe.move()

        if add_pipe:
            score +=1 # adds score
            for g in ge:
                g.fitness += 5
            pipes.append(Pipe(600)) #Adds a pipe to the pipes list with x position of 700. I need to add variables 
        for r in rem:
            pipes.remove(r) #removes pipe. might need to be random
        
        for x, bird in enumerate(birds):
            if bird.y + bird.img.get_height() > 730 or bird.y <0:
                #if bird hits the ground or flies off the screen
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)

        

        base.move()
        draw_window(win, birds, pipes, base, score, GEN)

def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path) # tell properties that are being set.
    
    pop = neat.Population(config) #Generate population based on config file

    pop.add_reporter(neat.StdOutReporter(True)) #Gives stats about populations
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats) #give output for last 3 lines

    winner = pop.run(main,50) #fitness function , generations


if __name__ =="__main__":
    local_dir = os.path.dirname(__file__) # give path to current directory. Used for loading config file
    config_path = os.path.join(local_dir, "config-feedforward.txt")#Find absolute path to file
    run(config_path)