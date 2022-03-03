import pygame
import glob
import random
pygame.init()

win = pygame.display.set_mode((500,500))

pygame.display.set_caption("GAME")


def loadImages(folderName,flip,x_size,y_size):
  fileList=glob.glob(folderName+"/*")
  output=[]
  for i in range(len(fileList)):
    output.append(pygame.image.load(fileList[i]))
    output[i]=pygame.transform.scale(output[i],(x_size, y_size))
  
  if flip==1:
    for i in range(len(output)):
      output[i]=pygame.transform.flip(output[i],True,False)

  return output
  

wr=loadImages('saitama_walk',0,64,64)
wl=loadImages('saitama_walk',1,64,64)

bg = pygame.image.load('Game/ship1.png')


bgx = 0
xpos = 0

char = pygame.image.load('saitama_walk/R01.png')

score = 0

bulletSound = pygame.mixer.Sound("Game/bullet.mp3")
hitSound = pygame.mixer.Sound("Game/hit.mp3")

music = pygame.mixer.music.load("Game/music.mp3")

clock = pygame.time.Clock()

class player(object):
  def __init__(self,x,y,width,height):
    self.x = x
    self.y = y
    self.width = width
    self.height = height
    self.vel = 5
    self.ij = False
    self.left = False
    self.right = False
    self.wc = 0
    self.jc = 9
    self.standing = True
    self.hitbox = (self.x + 15, self.y + 11, 35, 60)

  def draw(self, win):
    if self.wc + 1 >= 27:
      self.wc = 0
      
    if not(self.standing):
      if self.left:
        win.blit(wl[self.wc//3], (self.x,self.y))
        self.wc += 1
      elif self.right:
        win.blit(wr[self.wc//3], (self.x,self.y))
        self.wc += 1

    else:
      if self.right:
        win.blit(wr[0], (self.x, self.y))
      else:
        win.blit(wl[0], (self.x, self.y))
    self.hitbox = (self.x + 15, self.y + 2, 35, 60)
    pygame.draw.rect(win, (255,0,0), self.hitbox,2)

  def hit(self):
    self.x = 60
    self.y = 400
    self.wc = 0
    font1 = pygame.font.SysFont('comicsans', 100)
    text = font1.render('-5', 1, (255,0,0))
    win.blit(text, (250 - (text.get_width()/2),200))
    pygame.display.update()
    i = 0
    while i < 300:
      pygame.time.delay(10)
      i += 1
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          i = 301
          pygame.quit()

class projectile(object):
  def __init__(self,x,y,radius,color,facing):
    self.x = x
    self.y = y
    self.radius = radius
    self.color = color
    self.vel = 8 * facing

  def draw(self,win):
    pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


class lordboros(object):
  rw=loadImages('Enemy',0,64,64)
  lw=loadImages('Enemy',1,64,64)

  def __init__(self, x, y, width, height, end):
    self.x = x
    self.y = y
    self.width = width
    self.height = height
    self.end = end
    self.path = [self.x, self.end]
    self.wc = 0
    self.vel = 4
    self.hitbox = (self.x + 17, self.y + 2, 31, 57)
    self.health = 10
    self.visible = True

  def draw(self, win):
    self.move()
    if self.visible:
      if self.wc + 1 >= 11:
        self.wc = 0

      if self.vel > 0:
        win.blit(self.rw[self.wc//3], (self.x,self.y))
        self.wc += 1
      else:
        win.blit(self.lw[self.wc//3], (self.x,self.y))
        self.wc += 1

      pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
      pygame.draw.rect(win, (0,128,0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.health)), 10))
      self.hitbox = (self.x + 17, self.y + 2, 31, 57)
      
  def move(self):
    if self.vel > 0:
      if self.x + self.vel < self.path[1]:
        self.x += self.vel
      else:
        self.vel = self.vel * -1
        self.wc = 0
    else:
      if self.x - self.vel > self.path[0]:
        self.x += self.vel
      else:
        self.vel = self.vel * -1
        self.wc = 0

  def hit(self):
    if self.health > 0:
      self.health -= 0.33
    else:
      self.visible = False
    print('hit')

def rgw():
  win.blit(bg, (bgx,0))
  text = font.render('Score: ' + str(score), 1, (0,0,0))
  win.blit(text, (390, 10))
  man.draw(win)
  Boros.draw(win)
  for bullet in bullets:
    bullet.draw(win)

  pygame.display.update()

font = pygame.font.SysFont('comicsans', 30, True)
man = player(50, 400, 64,64)
Boros = lordboros(90, 400, 64, 64, 400)
sLoop = 0
bullets = []
run = True
scroll = True

while run:
  clock.tick(27)

  if man.hitbox[1] < Boros.hitbox[1] + Boros.hitbox[3] and man.hitbox[1] + man.hitbox[3] > Boros.hitbox[1]:
    if man.hitbox[0] + man.hitbox[2] > Boros.hitbox[0] and man.hitbox[0] < Boros.hitbox[0] + Boros.hitbox[2]:
      man.hit()
      score -= 0.5

  if sLoop > 0:
    sLoop += 1
  if sLoop > 3:
    sLoop = 0

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False

  for bullet in bullets:
    if bullet.y - bullet.radius < Boros.hitbox[1] + Boros.hitbox[3] and bullet.y + bullet.radius > Boros.hitbox[1]:
      if bullet.x + bullet.radius > Boros.hitbox[0] and bullet.x - bullet.radius < Boros.hitbox[0] + Boros.hitbox[2]: 
        hitSound.play()
        Boros.hit()
        score += 1
        bullets.pop(bullets.index(bullet))

    if bullet.x < 500 and bullet.x > 0:
      bullet.x += bullet.vel
    else:
      bullets.pop(bullets.index(bullet))

  keys = pygame.key.get_pressed()

  if keys[pygame.K_SPACE] and sLoop == 0:
    if man.left:
      facing = -1
    else :
      facing = 1
          
    if len(bullets) < 5:
      bullets.append(projectile(round(man.x + man.width //2), round(man.y + man.height//2), 6, (0,0,0), facing))

    sLoop = 1
  if keys[pygame.K_LEFT] and man.x > man.vel:
    if not scroll:
      man.x -= man.vel
    
    man.left = True
    man.right =  False
    man.standing = False
    

    if xpos>5:
      xpos -= 5
      bgx += 5
      Boros.x += 5

  elif keys[pygame.K_RIGHT] and man.x < 500 - man.width - man.vel:  
    if not scroll:
      man.x += man.vel
    man.left = False
    man.right = True
    man.standing = False

    

    if xpos<=2200:
      xpos += 5
      bgx -= 5
      Boros.x -= 5
     
  else:
    man.standing = True
    man.wc = 0
      
  if not(man.ij):
    if keys[pygame.K_UP]:
      man.ij = True
      man.right = False
      man.left = False
      man.standing = False
      man.wc = 0
  else:
    if man.jc >= -9:
      neg = 1
      if man.jc < 0:
        neg = -1
      man.y -= (man.jc ** 2) * 0.5 * neg
      man.jc -= 1
    else:
      man.ij = False
      man.jc = 9
          
  rgw()

pygame.quit()