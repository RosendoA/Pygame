import pygame
pygame.init()

win = pygame.display.set_mode((500,500))
pygame.display.set_caption("No-Name")

x = 50
y = 300
width = 50
height = 50
vel = 7.5

ij = False
jc = 10

run = True

while run:
  pygame.time.delay(25)

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False

  keys = pygame.key.get_pressed()

  if keys[pygame.K_LEFT] and x > vel :
    x -= vel
  if keys[pygame.K_RIGHT] and x < 500 - vel - width :
    x += vel
  if not(ij):
    if keys[pygame.K_UP] and y > vel :
      y -= vel
    if keys[pygame.K_DOWN] and y < 500 - height - vel :
      y += vel
    if keys[pygame.K_SPACE]:
      ij = True

  else:
    if jc >= -10:
      y -= (jc * abs(jc)) * 0.5
    else:
      jct = 10
      ij = False

  win.fill((0,0,0))
  pygame.draw.rect(win, (255,0,0), (x, y, width, height))   
  pygame.display.update()


pygame.QUIT()