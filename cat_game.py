
import pygame
import random
import math

pygame.init()

WIDTH, HEIGHT = 900, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Virtual Cat Simulator")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 28)

WHITE=(255,255,255)
GRAY=(210,210,210)
GREEN=(80,200,120)
YELLOW=(255,210,80)
RED=(220,80,80)
BLUE=(80,140,255)
PURPLE=(170,120,255)

class Cat:
    def __init__(self):
        self.x = WIDTH//2
        self.y = HEIGHT//2
        self.size = 45
        self.dragging=False
        self.mood="happy"
        self.annoyance=0
        self.energy=100
        self.target=None
        self.color=GREEN
        self.tail_angle=0

    def rect(self):
        return pygame.Rect(self.x-self.size,self.y-self.size,self.size*2,self.size*2)

    def update(self,toy):
        if self.annoyance < 3:
            self.mood="happy"
            self.color=GREEN
        elif self.annoyance < 6:
            self.mood="annoyed"
            self.color=YELLOW
        else:
            self.mood="angry"
            self.color=RED

        if not self.dragging:
            self.chase_toy(toy)

        self.tail_angle += 0.1

    def chase_toy(self,toy):
        dx=toy.x-self.x
        dy=toy.y-self.y
        dist=math.hypot(dx,dy)

        if dist<200:
            if dist>5:
                self.x += dx*0.02
                self.y += dy*0.02

    def draw(self,screen):

        pygame.draw.circle(screen,self.color,(int(self.x),int(self.y)),self.size)

        ear1=[(self.x-20,self.y-25),(self.x-5,self.y-55),(self.x+5,self.y-25)]
        ear2=[(self.x+20,self.y-25),(self.x+5,self.y-55),(self.x-5,self.y-25)]

        pygame.draw.polygon(screen,self.color,ear1)
        pygame.draw.polygon(screen,self.color,ear2)

        pygame.draw.circle(screen,(0,0,0),(int(self.x-12),int(self.y-5)),4)
        pygame.draw.circle(screen,(0,0,0),(int(self.x+12),int(self.y-5)),4)

        tail_x=self.x+math.cos(self.tail_angle)*40
        tail_y=self.y+math.sin(self.tail_angle)*10

        pygame.draw.line(screen,self.color,(self.x,self.y),(tail_x,tail_y),6)


class Toy:
    def __init__(self):
        self.x=random.randint(100,800)
        self.y=random.randint(150,600)
        self.size=12
        self.color=BLUE

    def draw(self,screen):
        pygame.draw.circle(screen,self.color,(int(self.x),int(self.y)),self.size)

class Button:
    def __init__(self,text,x,y,w,h):
        self.rect=pygame.Rect(x,y,w,h)
        self.text=text

    def draw(self,screen):
        pygame.draw.rect(screen,GRAY,self.rect)
        label=font.render(self.text,True,(0,0,0))
        screen.blit(label,(self.rect.x+10,self.rect.y+8))

cat=Cat()
toy=Toy()

feed_button=Button("Feed",20,20,100,35)
toy_button=Button("New Toy",20,65,100,35)
adopt_button=Button("Adopt Cat",20,110,120,35)

running=True

while running:

    screen.fill(WHITE)

    for event in pygame.event.get():

        if event.type==pygame.QUIT:
            running=False

        if event.type==pygame.MOUSEBUTTONDOWN:
            mouse=pygame.mouse.get_pos()

            if cat.rect().collidepoint(mouse):
                cat.dragging=True
                cat.annoyance+=1

            if feed_button.rect.collidepoint(mouse):
                cat.annoyance=max(0,cat.annoyance-3)
                cat.energy=min(100,cat.energy+10)

            if toy_button.rect.collidepoint(mouse):
                toy=Toy()

            if adopt_button.rect.collidepoint(mouse):
                cat=Cat()

        if event.type==pygame.MOUSEBUTTONUP:
            cat.dragging=False

        if event.type==pygame.MOUSEMOTION and cat.dragging:
            cat.x,cat.y=pygame.mouse.get_pos()

    cat.update(toy)

    toy.draw(screen)
    cat.draw(screen)

    feed_button.draw(screen)
    toy_button.draw(screen)
    adopt_button.draw(screen)

    mood_text=font.render("Mood: "+cat.mood,True,(0,0,0))
    energy_text=font.render("Energy: "+str(cat.energy),True,(0,0,0))

    screen.blit(mood_text,(20,170))
    screen.blit(energy_text,(20,200))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
