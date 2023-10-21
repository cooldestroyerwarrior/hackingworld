import pygame
import neat
import time
import os
import random
import pickle
pygame.font.init()


win_width=570
win_height=800
floor=730

win= pygame.display.set_mode((win_width,win_height))
pygame.display.set_caption("Flappy Bird")

generation=0

bird_imgs=[pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird1.png"))),
          pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird2.png"))),
          pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird3.png")))
          ]

pipe_img=pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","pipe.png")))
base_img=pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","base.png")))
bg_img=pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bg.png")))

stat_font = pygame.font.SysFont("comicsans",50)
end_font = pygame.font.SysFont("comicsans",70)
draw_lines=False


class Bird:
    imgs=bird_imgs
    max_rotation=25
    rot_vel=20
    animation_time=5

    def __init__(self,x,y) -> None:
        self.x=x
        self.y=y
        self.tilt=0
        self.tick_count=0
        self.vel=0
        self.height=self.y
        self.img_count=0
        self.img=self.imgs[0]

    def jump(self):
        self.vel=-10.5
        self.tick_count=0
        self.height=self.y

    def move(self):
        self.tick_count+=1
        d=self.vel*self.tick_count+1.5*self.tick_count**2
        if d>=16:
            d=16
        if d<0:
            d-=2
        
        self.y=self.y+d
        if d<0 or self.y < self.height+50:
            if self.tilt < self.max_rotation:
                self.tilt=self.max_rotation
        else:
            if self.tilt> -90:
                self.tilt-=self.rot_vel   
    
    def draw(self,win):
        self.img_count+=1

        if self.img_count < self.animation_time:
            self.img = self.imgs[0]
        elif self.img_count < self.animation_time*2:
            self.img = self.imgs[1]
        elif self.img_count < self.animation_time*3:
            self.img = self.imgs[2]
        elif self.img_count < self.animation_time*4:
            self.img = self.imgs[1]
        elif self.img_count < self.animation_time*4+1:
            self.img = self.imgs[0]
            self.img_count=0

        if self.tilt<=-80:
            self.img=self.imgs[1]
            self.img_count=self.animation_time*2

        #will rotate the image about the center
        blitRotateCenter(win,self.img,(self.x,self.y),self.tilt)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)
    
class Pipe:
    gap=200
    vel=5

    def __init__(self,x):
        self.x=x
        self.height=0
        self.gap=200

        self.top=0
        self.bottom=0
        self.pipe_top=pygame.transform.flip(pipe_img, False, True)
        self.pipe_bottom=pipe_img

        self.passed=False
        self.set_height()
    
    def set_height(self):
        self.height=random.randrange(50,450)
        self.top=self.height-self.pipe_top.get_height()
        self.bottom=self.height+self.gap

    def move(self):
        self.x-=self.vel
    
    def draw(self,win):
        win.blit(self.pipe_top,(self.x,self.top))
        win.blit(self.pipe_bottom,(self.x,self.bottom))

    def collide(self,bird):
        bird_mask=bird.get_mask()
        top_mask = pygame.mask.from_surface(self.pipe_top)
        bottom_mask = pygame.mask.from_surface(self.pipe_bottom)

        top_offset = (self.x-bird.x,self.top-round(bird.y))
        bottom_offset=(self.x-bird.x,self.bottom-round(bird.y))

        b_point = bird_mask.overlap(bottom_mask,bottom_offset)
        t_point = bird_mask.overlap(top_mask,top_offset)

        if t_point or b_point:
            return True
        return False

class Base:
    vel=5
    width=base_img.get_width()
    img=base_img

    def __init__(self,y):
        self.y=y
        self.x1=0
        self.x2=self.width
    
    def move(self):
        self.x1 -= self.vel
        self.x2 -= self.vel

        if self.x1+self.width<0:
            self.x1=self.x2+self.width

        if self.x2+self.width<0:
            self.x2=self.x1+self.width
        
    def draw(self,win):
        win.blit(self.img,(self.x1,self.y))
        win.blit(self.img,(self.x2,self.y))

def blitRotateCenter(surf, image, topleft, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(topleft = topleft).center)

    surf.blit(rotated_image, new_rect.topleft)

def draw_window(win,birds,pipes,base,score,gen,pipe_ind):
    if gen == 0:
        gen = 1
    win.blit(bg_img, (0,0))

    for pipe in pipes:
        pipe.draw(win)

    base.draw(win)
    for bird in birds:
        # draw lines from bird to pipe
        if draw_lines:
            try:
                pygame.draw.line(win, (255,0,0), (bird.x+bird.img.get_width()/2, bird.y + bird.img.get_height()/2), (pipes[pipe_ind].x + pipes[pipe_ind].PIPE_TOP.get_width()/2, pipes[pipe_ind].height), 5)
                pygame.draw.line(win, (255,0,0), (bird.x+bird.img.get_width()/2, bird.y + bird.img.get_height()/2), (pipes[pipe_ind].x + pipes[pipe_ind].PIPE_BOTTOM.get_width()/2, pipes[pipe_ind].bottom), 5)
            except:
                pass
        # draw bird
        bird.draw(win)

    # score
    score_label = stat_font.render("Score: " + str(score),1,(255,255,255))
    win.blit(score_label, (win_width - score_label.get_width() - 15, 10))

    # generations
    score_label = stat_font.render("Gens: " + str(gen-1),1,(255,255,255))
    win.blit(score_label, (10, 10))

    # alive
    score_label = stat_font.render("Alive: " + str(len(birds)),1,(255,255,255))
    win.blit(score_label, (10, 50))

    pygame.display.update()



def eval_genomes(genomes,config):
    global generation,win
    generation+=1
    nets=[]
    ge=[]
    birds=[]

    for _,g in genomes:
        net=neat.nn.FeedForwardNetwork.create(g,config)
        nets.append(net)
        birds.append(Bird(230,350))
        g.fitness=0
        ge.append(g)


    base = Base(floor)
    pipes = [Pipe(700)]

    clock = pygame.time.Clock()

    score=0

    run=True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
                pygame.quit()
                quit()

        pipe_ind=0
        if len(birds)>0:
            if len(pipes)>1 and birds[0].x>pipes[0].x+pipes[0].pipe_top.get_width():
                pipe_ind=1
        else:
            run=False
            break

        for x,bird in enumerate(birds):
            bird.move()
            ge[x].fitness+=0.1
            output = nets[birds.index(bird)].activate((bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))
            if output[0]>0.5:
                bird.jump()

        base.move()

        #game
        rem=[]
        add_pipe=False
        for pipe in pipes:
            pipe.move()
            for x,bird in enumerate(birds):
                if pipe.collide(bird):
                    ge[x].fitness-=1
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)
            
            if pipe.x + pipe.pipe_top.get_width()<0:
                rem.append(pipe)

            if not pipe.passed and pipe.x < bird.x:
                pipe.passed=True
                add_pipe=True
            #pipe.move()
        
        if add_pipe:
            score+=1

        #for birds that will pass pipe will get extra score
            for g in ge:
                g.fitness+=5

            pipes.append(Pipe(win_width))

        for r in rem:
            pipes.remove(r)

        for x,bird in enumerate(birds):
            if bird.y + bird.img.get_height()-10>=floor or bird.y<-50:
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)

        #base.move()
        draw_window(win,birds,pipes,base,score,generation,pipe_ind)

    



def run(config_path):
    config=neat.config.Config(neat.DefaultGenome,neat.DefaultReproduction,
                       neat.DefaultSpeciesSet,neat.DefaultStagnation,
                       config_path)

    p=neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats=neat.StatisticsReporter()
    p.add_reporter(stats)

    winner=p.run(eval_genomes,50)

    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))

if __name__== "__main__":
    local_dir=os.path.dirname(__file__)
    config_path=os.path.join(local_dir,'config-feedforward.txt')
    run(config_path)