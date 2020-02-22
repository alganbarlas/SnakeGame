"""
PyGame ile Yılan oyunu
"""

import pygame, sys, time, random

#Pygame'yi initialised ediyoruz
check_error = pygame.init()

# Verebilecek hataları kontrol ediyoruz
if(check_error[1]>0):
    print("(-)Oyun Yüklenemedi. Bir daha deneyin ...")
    sys.exit(-1)
else:
    print("(+) Oyun başarıyla yüklendi !!")

# yılan hızının değişkeni
hiz = 17

# harita (bknz: play surface)
(width, height) = (900,530)
play_Surface = pygame.display.set_mode((width, height))
pygame.display.set_caption("Yılan Oyunu")

# Oyun renklerini belirliyoruz
red = pygame.Color(255,0,0) # Oyun bitiş mesajı
green = pygame.Color(0,255,0) # Yılan
blue = pygame.Color(0,0,255) # Yazılar
white = pygame.Color(255,255,255) # Skor
black = pygame.Color(0,0,0) # Arka plan
brown = pygame.Color(165,42,42) # Yemekler

# FPS Kontrolü yapıyoruz
fps_Controller = pygame.time.Clock()

# Yılana ait değişkenler burada
snake_Pos = [100,50]
snakeBody = [[100,50], [90,50], [80,50]]
# Yemlere ait değişkenler
food_Pos = [random.randrange(1,72)*10, random.randrange(1,46)*10]
foodSpawn = True # Bunu duruma göre değiştireceğiz

# yılan kontrolünü direk olmasa da bunlar üzerinden yapacağız
direction = "RIGHT"
changeTo = direction

score = 0 # Oyun skorunun saklı tutulduğu değişken

# İlk önce oyun bitiş fonksiyonunu oluşturuyoruz

def GameOver():
    myFont = pygame.font.SysFont('monospace',72) # Oyun bittiğindeki font
    overMessage = myFont.render('Oyun Bitti !',True,red)
    overRect = overMessage.get_rect()
    overRect.midtop = (370,15)
    play_Surface.blit(overMessage, overRect)
    # Buraya kadar bitiş ekranını ayarladık, şimdi skoru göstereceğiz
    ShowScore(0)
    pygame.display.flip()
    time.sleep(3)
    pygame.quit()
    sys.exit()

def ShowScore(choice=1): #Oyun skoru için bir fonksiyon oluşturduk
    scFont = pygame.font.SysFont('monospace', 30)
    scSurface = scFont.render('Skor: '+ str(score), True, white)
    scRect = scSurface.get_rect()

    if choice == 1:
        scRect.midtop=(80,10)
    else:
        scRect.midtop=(360,100)
    play_Surface.blit(scSurface,scRect)

# Bütün oyun mekanizması burası

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    # Tuş vuruşlarını yakalıyoruz
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == ord('w'):
                changeTo = 'UP'
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                changeTo = 'DOWN'
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                changeTo = 'LEFT'
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                changeTo = 'RIGHT'
            # Esc ile çıkış yapmak için
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

    # Yön doğrulama
    if changeTo=='RIGHT' and not direction=='LEFT':
        direction='RIGHT'
    if changeTo=='LEFT' and not direction=='RIGHT':
        direction='LEFT'
    if changeTo=='UP' and not direction=='DOWN':
        direction='UP'
    if changeTo=='DOWN' and not direction=='UP':
        direction='DOWN'

    # Yılanın pozisyonunu değiştirmek

    if direction=='RIGHT':
        snake_Pos[0] += 10
    if direction=='LEFT':
        snake_Pos[0] -= 10
    if direction=='UP':
        snake_Pos[1] -= 10
    if direction=='DOWN':
        snake_Pos[1] += 10

    # Yılan gövdesinin mekanizması

    snakeBody.insert(0, list(snake_Pos))
    if snake_Pos[0]==food_Pos[0] and snake_Pos[1]==food_Pos[1]:
            hiz += 1 # yılan hızını arttırır
            score += 1 # skoru bir arttırır
            foodSpawn = False
    else:
        snakeBody.pop()

    if not foodSpawn:
        foodPos = [random.randrange(1,(width//10))*10,random.randrange(1,height//10)*10]
    # Yani yemek yoksa ekranda verilen değerlerde yemek oluştur ve yemek olduğunu söyle
    foodSpawn = True

    # Yılanı çizelim
    play_Surface.fill(black)
    for pos in snakeBody:
        pygame.draw.rect(play_Surface,green, pygame.Rect(pos[0],pos[1],10,10))

    # Yemi çizelim
    pygame.draw.rect(play_Surface,red, pygame.Rect(food_Pos[0],food_Pos[1],10,10))

    # Sınırları belirleyelim

    if snake_Pos[0]>890 or snake_Pos[0]<0:
        time.sleep(1)
        GameOver()
    if snake_Pos[1]>530 or snake_Pos[1]<0:
        time.sleep(1)
        GameOver()

    ShowScore()
    pygame.display.flip()
    fps_Controller.tick(hiz)
