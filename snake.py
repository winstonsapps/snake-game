#snake
from random import randint
import pygame, sys
pygame.init()

#setup
gridsizex = 30
gridsizey = 30
cellsize=30
screen = pygame.display.set_mode((gridsizex*cellsize, gridsizey*cellsize))
black = (0, 0, 0) #black background
white = (255,255,255) #white snake
red = (255, 0, 0) # red food
framereset = 6 # speed in frames
frame = 1 #resets when it reaches framereset
clock = pygame.time.Clock()
bigtext = pygame.font.Font('RobotoMono-Medium.ttf', 100) # adds font
smalltext = pygame.font.Font('RobotoMono-Medium.ttf', 20) # adds small font
highscore = 0
pygame.display.set_caption('Snake')
textoffset = 0
textoffset2 = 0
pause='pause'
lengthadd = 3
#player setup

score=0
playerdir = [0, 0] # x movement, y movement
oldplayerdir = None
player = pygame.Rect((gridsizex*cellsize)//2, (gridsizey*cellsize)//2, cellsize,cellsize)
playerlist = [player]
add = False
prevplayer = player
# food setup

food = pygame.Rect(randint(0, gridsizex-1)*cellsize, randint(0, gridsizey-1)*cellsize, cellsize,cellsize)
# main loop

def check_collision(rectlist, rect):
    return rect.collidelist(rectlist) > 0
    


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN: # turn but not the opposite direction that you are facing
            key = event.key
            if key == pygame.K_UP  and not playerdir == [0, 1]:
                playerdir = [0, -1] # 0 right 1 up
            elif key == pygame.K_DOWN and not playerdir == [0, -1]:
                playerdir = [0, 1] # 0 right 1 down
            elif key == pygame.K_LEFT and not playerdir == [1, 0]:
                playerdir = [-1, 0] # 1 left 1 up
            elif key == pygame.K_RIGHT and not playerdir == [-1, 0]:
                playerdir = [1, 0] # 1 right 0 up
            elif pause == 'pause' or pause=='dead':
                player.update((gridsizex*cellsize)//2, (gridsizey*cellsize)//2, cellsize,cellsize) #reset
                score=0
                playerdir = 0,0
                textoffset = 0
                textoffset2 = 0
                playerlist = [player]
                pause='unpause'

    if pause=='unpause':
        screen.fill(black)
        scoretext = 'score: %d' % score
        screen.blit(smalltext.render(scoretext, True, white), (0,0))

        for playerrect in playerlist:
            pygame.draw.rect(screen, white, playerrect)

        pygame.draw.rect(screen, red, food)
        if frame % framereset == 0 or not playerdir == oldplayerdir:

            frame = 1
            #insert generic movement here

            if player.x == food.x and player.y == food.y:
                while food.collidelist(playerlist) != -1:
                    food.x = randint(0, gridsizex-1)*cellsize
                    food.y = randint(0, gridsizey-1)*cellsize
                    for j in range(lengthadd):
                        playerlist.append(playerlist[len(playerlist) - 1].copy())
                    score+=1
            
            player.x += playerdir[0]*cellsize
            player.y += playerdir[1]*cellsize
            if check_collision(playerlist, player) and not (player.x == food.x and player.y == food.y):
                pause='dead'
            playerlist.append(player.copy())   
            playerlist.pop(0)


                

            oldplayerdir = playerdir
        
        


                

    elif pause == 'pause':
        screen.fill(black)
        screen.blit(bigtext.render('Snake',True, white), (7,7+textoffset))
        screen.blit(smalltext.render('Press any key',True, white), (7, 120+textoffset))
        if not textoffset+150 > gridsizey*cellsize :
            textoffset += 1
    
    if player.x > (gridsizex-1)*cellsize or player.y > (gridsizey-1)*cellsize or player.x < 0 or player.y < 0 or pause=='dead':
        pause = 'dead'

        screen.fill(black)
        screen.blit(bigtext.render('You Died!',True, white), (7,7+textoffset2)) # draw text
        screen.blit(smalltext.render('Press any key to continue',True, white), (7, 120+textoffset2))
        
        if score > highscore:
            highscore = score
        scoretext = 'score: %d, highscore: %d' % (score, highscore)
        screen.blit(smalltext.render(scoretext, True, white),  (7, 150+textoffset2))
        if not textoffset2+180 > gridsizey*cellsize:
            textoffset2 += 1


    
    frame+=1
    pygame.display.update()
    clock.tick(60)