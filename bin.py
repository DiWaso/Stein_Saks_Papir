import pygame, random, math, sys
from pygame.locals import *
pygame.init()

WIDTH = 800
HEIGHT = 600
FELLES_STØRRELSE = 50
FPS = 60
clock = pygame.time.Clock()

win = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Rock, Paper, Scissors")
font = pygame.font.SysFont("arialblack", 50)

#Bilder
stein_bilde = pygame.image.load("pictures/stein.png").convert_alpha()
saks_bilde = pygame.image.load("pictures/saks.png").convert_alpha()
papir_bilde = pygame.image.load("pictures/papir.png").convert_alpha()
start_img = pygame.image.load("pictures/start.png").convert_alpha()
exit_img = pygame.image.load("pictures/exit.png").convert_alpha()
background_img = pygame.image.load("pictures/background.png").convert_alpha()
chooseBall_img = pygame.image.load("pictures/chooseBall_Background.png").convert_alpha()
play_img = pygame.image.load("pictures/playBackground.jpg").convert_alpha()
win_img = pygame.image.load("pictures/winBackground.png").convert_alpha()
left_arrow_img = pygame.image.load("pictures/arrow_left.png").convert_alpha()
right_arrow_img = pygame.image.load("pictures/arrow_right.png").convert_alpha()

#Bilder i riktig størrelse
scaled_stein = pygame.transform.scale(stein_bilde, (FELLES_STØRRELSE, FELLES_STØRRELSE))
scaled_saks = pygame.transform.scale(saks_bilde, (FELLES_STØRRELSE, FELLES_STØRRELSE))
scaled_papir = pygame.transform.scale(papir_bilde, (FELLES_STØRRELSE, FELLES_STØRRELSE))
scaled_background = pygame.transform.scale(background_img, (800, 600))
scaled_chooseBall = pygame.transform.scale(chooseBall_img, (800, 600))
scaled_play = pygame.transform.scale(play_img, (800, 600))
scaled_win = pygame.transform.scale(win_img, (800, 600))
scaled_left_arrow = pygame.transform.scale(left_arrow_img, (100, 100))
scaled_right_arrow = pygame.transform.scale(right_arrow_img, (100, 100))
antall_baller = 15

class Button:
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, screen):
        action = False
        #get mouse position
        pos = pygame.mouse.get_pos()

        #check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        #draw button on screen
        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action

#Kaller Button klassen
start_button = Button(125, 225, start_img, 1)
exit_button = Button((800 - exit_img.get_width() - 125), 225, exit_img, 1)

class Ball:
    def __init__(self, scaled_bilde, tracker, everyone):
        self.scaled_bilde = scaled_bilde
        self.tracker = tracker
        self.radius = FELLES_STØRRELSE // 2
        self.x_vel = 2
        self.y_vel = 2
        self.spawnBall(everyone)
    
    def spawnBall(self, everyone):
        while True:
            self.x = random.randint((self.radius + 5), (WIDTH - FELLES_STØRRELSE - 5))
            self.y = random.randint((self.radius + 5), (HEIGHT - FELLES_STØRRELSE - 5))
            for ball in everyone:
                if ball is self:
                    continue
                xAvstand2 = (self.x - ball.x)**2
                yAvstand2 = (self.y - ball.y)**2
                avstand = math.sqrt(xAvstand2 + yAvstand2)
                if avstand < self.radius + ball.radius:
                    break
            else:
                if self.x < self.radius or self.x > WIDTH - self.radius or self.y < self.radius or self.y > HEIGHT - self.radius:
                    continue
                else:
                    break

    def drawBall(self):
        win.blit(self.scaled_bilde, (self.x, self.y))

    def moveBall(self):
        self.x += self.x_vel
        if self.x <= 0:
            self.x_vel = -self.x_vel
        if self.x >= WIDTH - self.scaled_bilde.get_width():
            self.x_vel = -self.x_vel
            
        self.y += self.y_vel
        if self.y <= 0:
            self.y_vel = -self.y_vel
        if self.y >= HEIGHT - self.scaled_bilde.get_height():
            self.y_vel = -self.y_vel

def chaseBall(objekter):
    for i, objekt in enumerate(objekter):
        for j, objekt2 in enumerate(objekter[i+1:]):
            xAvstand2 = (objekt.x - objekt2.x)**2
            yAvstand2 = (objekt.y - objekt2.y)**2
            avstand = math.sqrt(xAvstand2 + yAvstand2)

            if avstand < objekt.radius + objekt2.radius:
                if objekt.tracker == "STEIN" and objekt2.tracker == "PAPIR":
                    objekt.scaled_bilde = pygame.transform.scale(papir_bilde, (FELLES_STØRRELSE, FELLES_STØRRELSE))
                    objekt.tracker = "PAPIR"
                    objekt.x_vel = -objekt.x_vel
                    objekt.y_vel = -objekt.y_vel
                    objekt2.x_vel = -objekt.x_vel
                    objekt2.y_vel = -objekt.y_vel
                elif objekt2.tracker == "STEIN" and objekt.tracker == "PAPIR":
                    objekt2.scaled_bilde = pygame.transform.scale(papir_bilde, (FELLES_STØRRELSE, FELLES_STØRRELSE))
                    objekt2.tracker = "PAPIR"
                    objekt.x_vel = -objekt.x_vel
                    objekt.y_vel = -objekt.y_vel
                    objekt2.x_vel = -objekt.x_vel
                    objekt2.y_vel = -objekt.y_vel

                if objekt.tracker == "SAKS" and objekt2.tracker == "STEIN":
                    objekt.scaled_bilde = pygame.transform.scale(stein_bilde, (FELLES_STØRRELSE, FELLES_STØRRELSE))
                    objekt.tracker = "STEIN"
                    objekt.x_vel = -objekt.x_vel
                    objekt.y_vel = -objekt.y_vel
                    objekt2.x_vel = -objekt.x_vel
                    objekt2.y_vel = -objekt.y_vel
                elif objekt2.tracker == "SAKS" and objekt.tracker == "STEIN":
                    objekt2.scaled_bilde = pygame.transform.scale(stein_bilde, (FELLES_STØRRELSE, FELLES_STØRRELSE))
                    objekt2.tracker = "STEIN"
                    objekt.x_vel = -objekt.x_vel
                    objekt.y_vel = -objekt.y_vel
                    objekt2.x_vel = -objekt.x_vel
                    objekt2.y_vel = -objekt.y_vel

                if objekt.tracker == "PAPIR" and objekt2.tracker == "SAKS":
                    objekt.scaled_bilde = pygame.transform.scale(saks_bilde, (FELLES_STØRRELSE, FELLES_STØRRELSE))
                    objekt.tracker = "SAKS"
                    objekt.x_vel = -objekt.x_vel
                    objekt.y_vel = -objekt.y_vel
                    objekt2.x_vel = -objekt.x_vel
                    objekt2.y_vel = -objekt.y_vel
                elif objekt2.tracker == "PAPIR" and objekt.tracker == "SAKS":
                    objekt2.scaled_bilde = pygame.transform.scale(saks_bilde, (FELLES_STØRRELSE, FELLES_STØRRELSE))
                    objekt2.tracker = "SAKS"
                    objekt.x_vel = -objekt.x_vel
                    objekt.y_vel = -objekt.y_vel
                    objekt2.x_vel = -objekt.x_vel
                    objekt2.y_vel = -objekt.y_vel
                print(f"{objekt.tracker} og {objekt2.tracker}")

def findWinner(objekter):
    ending_amount = antall_baller * 3
    stein_tracker = []
    saks_tracker = []
    papir_tracker = []

    for objekt in objekter:
        if objekt.tracker == "STEIN":
            stein_tracker.append(stein_bilde)
        if objekt.tracker == "SAKS":
            saks_tracker.append(saks_bilde)
        if objekt.tracker == "PAPIR":
            papir_tracker.append(papir_bilde)

    if len(stein_tracker) == ending_amount:
        winner(stein_tracker[0])
    if len(saks_tracker) == ending_amount:
        winner(saks_tracker[0])
    if len(papir_tracker) == ending_amount:
        winner(papir_tracker[0])

def drawGrid():
    blockSize = 25 #Set the size of the grid block
    for x in range(0, WIDTH, blockSize):
        for y in range(0, HEIGHT, blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            pygame.draw.rect(win, (255, 255, 255), rect, 1)

def draw_menu():
    img = font.render("Rock, Paper, Scissors", True, (255, 255, 255))

    win.blit(scaled_background, (0, 0))
    win.blit(img, ((WIDTH - img.get_width()) // 2, 50))

def main():
    run = True
    show_menu = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                sys.exit()
        
        clock.tick(FPS)

        if show_menu:
            draw_menu()
            start_clicked = start_button.draw(win)
            exit_clicked = exit_button.draw(win)
            if start_clicked:
                chooseBall()
                show_menu = False
            
            elif exit_clicked:
                pygame.quit()
                sys.exit()
        
        else:
            draw_menu()

        pygame.display.update()
    
    pygame.quit()

# def chooseBallDraw(screen, get_pressed, button):
#     run = True
#     pos = pygame.mouse.get_pos()

#     while run:
#         if button.rect.collidepoint(pos):
#             if pygame.mouse.get_pressed()[0] == 1:
#                 antall_baller += 1
            
#         if get_pressed[K_RETURN]:
#             return print(antall_baller)

#         screen.blit(button.image, (button.rect.x, button.rect.y))


def chooseBall():
    run = True
    antallBaller = 1
    img = font.render(str(antallBaller), True, (255, 255, 255))
    keypress = pygame.key.get_pressed()

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                sys.exit()

        #chooseBallDraw(win, keypress, left_button)
        win.blit(img, ((WIDTH - img.get_width()) // 2, 100))    

        pygame.display.update()
    pygame.quit()

def draw_play(stein, saks, papir):

    win.blit(scaled_play, (0, 0))
    drawGrid()

    for idx, val in enumerate(stein):
        val.drawBall()
        saks[idx].drawBall()
        papir[idx].drawBall()

def play():
    run = True
    
    everyone = []
    stein = [Ball(scaled_stein, "STEIN", everyone) for i in range(antall_baller)]
    everyone += stein
    saks = [Ball(scaled_saks, "SAKS", everyone) for i in range(antall_baller)] 
    everyone += saks
    papir = [Ball(scaled_papir, "PAPIR", everyone) for i in range(antall_baller)]
    everyone += papir
    random.shuffle(everyone)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                sys.exit()
        
        clock.tick(FPS)
        draw_play(stein, saks, papir)
        for idx, val in enumerate(stein):
            val.moveBall()
            saks[idx].moveBall()
            papir[idx].moveBall()

        chaseBall(everyone)
        findWinner(everyone)

        #pygame.event.wait()
        pygame.display.update()

    pygame.quit()

def winner(winner_bilde):
    run = True
    img = font.render("WINNER!", True, (255, 255, 255))
    img2 = font.render("Press SPACE to Continue", True, (255, 255, 255))
    vinner_bilde = pygame.transform.scale(winner_bilde, (250, 250))

    while run:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    main()
            if event.type == pygame.QUIT:
                run = False
                sys.exit()

        clock.tick(FPS)
        win.blit(scaled_win, (0, 0))

        win.blit(img, ((WIDTH - img.get_width()) // 2, 50))
        win.blit(img2, (67.5, (HEIGHT - 150)))
        win.blit(vinner_bilde, (((WIDTH - vinner_bilde.get_width()) // 2, (HEIGHT - vinner_bilde.get_height()) // 2)))
        
        pygame.display.update()
    
    pygame.quit()

if __name__ == '__main__':
    main()
