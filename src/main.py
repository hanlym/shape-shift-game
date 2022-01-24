#whoops i forgot to write comments and am now too lazy to do that except for the funny ones
import pygame
import os
import random

pygame.init()

WIDTH, HEIGHT = 900, 500
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shapeshift")

pygame.font.init()
font = pygame.font.SysFont(None, 30)

class Player:
    def __init__(self):
        self.y = 190
        self.shape = 3
        self.score = 0
        self.hasShield = False
        self.hasAuto = True
        self.speed = 0

    def draw(self):
        playerIcon = pygame.image.load(os.path.join("assets", f"{str(self.shape)}.png"))
        playerIcon = pygame.transform.scale(playerIcon, (60, 60))
        window.blit(playerIcon, (125, self.y))

        if self.hasShield:
            shieldEffect = pygame.image.load(os.path.join("assets", "shield_effect.png"))
            shieldEffect = pygame.transform.scale(shieldEffect, (90, 90))
            window.blit(shieldEffect, (110, self.y-10))
        if self.hasAuto:
            autoEffect = pygame.image.load(os.path.join("assets", "autoswitch_effect.png"))
            shieldEffect = pygame.transform.scale(autoEffect, (100, 100))
            window.blit(shieldEffect, (105, self.y-15))

class EnemyLine:
    def __init__(self):
        self.x = 900
        self.shape = random.randint(3, 6)
        self.openSlot = random.randint(0, 3)
        self.speed = 5
        self.hasShield = random.randint(0, 100) % 3 == 0
        self.hasAuto = random.randint(0, 100) % 3 == 0 if not self.hasShield else False
    
    def regen(self):
        self.x = 900
        self.shape = random.randint(3, 6)
        self.openSlot = random.randint(0, 3)
        self.hasShield = random.randint(1, 20) == 1
        self.hasAuto = random.randint(0, 100) % 3 == 0 if not self.hasShield else False

    def draw(self):
        slots = [(self.x, 0), (self.x, 125), (self.x, 250), (self.x, 375)]
        if self.hasShield: 
            shieldSlot = slots[self.openSlot]
        elif self.hasAuto:
            autoSlot = slots[self.openSlot]

        del slots[self.openSlot]
        
        enemyIcon = pygame.image.load(os.path.join("assets", f"{str(self.shape)}.png"))
        window.blit(enemyIcon, slots[0])
        window.blit(enemyIcon, slots[1])
        window.blit(enemyIcon, slots[2])
        if self.hasShield:
            shieldIcon = pygame.image.load(os.path.join("assets", "shield.png"))
            window.blit(shieldIcon, shieldSlot)
        elif self.hasAuto:
            autoIcon = pygame.image.load(os.path.join("assets", "autoswitch.png"))
            autoIcon = pygame.transform.scale(autoIcon, (75, 75))
            window.blit(autoIcon, autoSlot)

        self.x -= self.speed

def drawWin(player):
    window.fill((0, 0, 0))
    playerScore = font.render(f"SCORE: {player.score}", True, (0, 255, 0))
    window.blit(playerScore, (25, 25))

def death(player):
    youDied = font.render("YOU DIED", True, (255, 0, 0))
    window.blit(youDied, (400, 200))
    drawEnd()
    
#end of game
def drawEnd():
    #haha butt funny
    againButt = font.render("Play again", True, (255, 255, 255))
    window.blit(againButt, (400, 225))
    quitButt = font.render("Quit", True, (255, 255, 255))
    window.blit(quitButt, (400, 250))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = pygame.mouse.get_pos()
                if 400 <= mouseX <= 500 and 225 <= mouseY <= 249:
                    main()
                elif 400<= mouseX <= 500 and 250 <= mouseY <= 275:
                    pygame.quit()
                    exit()

#heehee sloppy code time
def mainMenu():
    window.fill((0, 0, 0))
    titleFont = pygame.font.SysFont(None, 50)
    title = titleFont.render("SHAPE SHIFT", True, (255, 255, 255))
    window.blit(title, (325, 150))

    playButt = font.render("Play", True, (255, 255, 255))
    window.blit(playButt, (400, 225))
    quitButt = font.render("Quit", True, (255, 255, 255))
    window.blit(quitButt, (400, 250))

    pygame.display.update()

    #this makes an error i can't be bothered to fix so just make sure you play the game right and it'll be ok
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = pygame.mouse.get_pos()
                if 400 <= mouseX <= 500 and 225 <= mouseY <= 249:
                    main()
                elif 400<= mouseX <= 500 and 250 <= mouseY <= 275:
                    pygame.quit()
                    exit()

fps = 60
def main():
    clock = pygame.time.Clock()

    player = Player()
    enemy = EnemyLine()
    
    running = True
    autoSwitch = False
    while running:
        clock.tick(fps)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            if player.y > 0:
                player.y -= 5 + player.speed
            else:
                player.y += 5 + player.speed
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            if player.y < HEIGHT - 60:
                player.y += 5 + player.speed
            else:
                player.y -= 5 + player.speed

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_3:
                    player.shape = 3
                elif event.key == pygame.K_4:
                    player.shape = 4
                elif event.key == pygame.K_5:
                    player.shape = 5
                elif event.key == pygame.K_6:
                    player.shape = 6
                elif event.key == pygame.K_SPACE and player.hasAuto:
                    autoSwitch = True
                    autoCounter = 0
        
        drawWin(player)
        
        if 125 <= enemy.x <= 125+60:
            slotsY = [0, 125, 250, 375]
            if player.shape == enemy.shape and slotsY[enemy.openSlot] <= player.y+30 <= slotsY[enemy.openSlot] + 125:
                player.score += 1
                enemy.speed += 0.1
                player.speed += 0.01

                #powerup pickups
                if enemy.hasShield:
                    player.hasShield = True
                elif enemy.hasAuto:
                    player.hasAuto = True
            else:
                if player.hasShield:
                    player.hasShield = False
                    enemy.x -= 150
                else:
                    death(player)
        
        if enemy.x > -100:
            enemy.draw()
        else:
            enemy.regen()

        if autoSwitch and autoCounter <= 300:
            player.hasAuto = False
            player.shape = enemy.shape
            autoCounter += 1
        elif autoSwitch and autoCounter > 300:
            autoSwitch = False
        
        player.draw()
        
        pygame.display.update()
    
    pygame.quit()

if __name__ == "__main__":
    mainMenu()
