#3/4/2024
#trying to make a little cube that can dash
import pygame
pygame.init

#Vars
#Dash input timers
L1 = 0
L2 = 0
R1 = 0
R2 = 0
#Dash Cooldown
dashCD = 10
#Jump Cooldown
jumpCD = 0
#game window
wdw = pygame.display.set_mode((700,400))   #look at
pygame.display.set_caption("dashy boi")
#starting coords
cy = 330
cx = 350
#cube size
cw = 10
ch = 10
#starting vel
vely = 0
vmax = 3
vmin = -3
vel = 0
#starting accel
accel = 0
#deccelerations
slow = 0.1
#blocked booleans, 0 is top, and it goes clockwise
blocked = [False,False,False,False]

#game start
run = True
while run:
    #refresh delay
    pygame.time.delay(10)

    #implements quiting the game  
    for event in pygame.event.get():    
        if event.type == pygame.QUIT: 
            run = False

    #wall detection
    if cx>700-cw:
        blocked[1] = True
    else:
        blocked[1] = False
    if cx<0:
        blocked[3] = True
    else:
        blocked[3] = False
    if cy>350:
        blocked[2] = True
    else:
        blocked[2] = False
    if cy < 0+ch:
        blocked[0] = True
    else:
        blocked[0] = False

    #starts detecting pressed keys
    keys = pygame.key.get_pressed()

    # if left arrow key is pressed
    if keys[pygame.K_LEFT] and blocked[3] == False:
        L2 = L1 
        L1 = pygame.time.get_ticks()
        accel = -0.1
        if 50 < (L1 - L2) < 200 and dashCD == 0: #the DASH
            cx = cx-10
            vel = -5
            dashCD = 20
          
    # if right arrow key is pressed 
    if keys[pygame.K_RIGHT] and blocked[1] == False:
        R2 = R1 
        R1 = pygame.time.get_ticks()
        accel = 0.1
        if 50 < (R1 - R2) < 200 and dashCD == 0: #the DASH
            cx = cx+10
            vel = 5
            dashCD = 20

    # if up arrow key is pressed 
    if keys[pygame.K_UP] and jumpCD == 0 and blocked[0] == False: 
        cy -= 5
        vely = -5


    #using accel & slow
    if blocked[2] == False:
        slow = 0.005
    elif keys[pygame.K_DOWN]:
        slow = 0.5
    else: 
        slow = 0.1

    if accel != 0 and ((not vel <= vmin and not vel >= vmax) or (accel*vel)< 0): 
        vel += accel
    else:
        #ground friction negative acceleration bs
        if vel > 0 or vel >= vmax:
            #this if acts as a hardstop for the slipping issue
            if vel < slow:
                vel = 0
            else:
                vel -= slow
        elif vel < 0 or vel <= vmin:
            #this if acts as a hardstop for the slipping issue
            if vel > -slow:
                vel = 0
            else:
                 vel += slow

    #using vel
    if (vel > 0 and blocked[1] == False) or (vel < 0 and blocked[3] == False):
        cx += vel
    if blocked[2] == False:
        cy += vely
        jumpCD = 1

    #reset accel & Cooldowns
    accel = 0
    if dashCD != 0:
        dashCD -= 1

    #gravity
    if blocked[2]== False:
        vely += 0.1
    else:
        vely = 0
        jumpCD = 0
    
    #unsticking/bouncing
    if cx <= 0:
        if vel <= -3:
            vel = vel*(-1/2)
        else:
            vel = 0
        cx = 1
    if blocked[2] == True:
        vely = 0
        cy = 350
    if cx >= 700 - cw:
        if vel >= 3:
            vel = vel*(-1/2)
        else:
            vel = 0
        cx = 699 - cw
    
    

    #make window black
    wdw.fill((0, 0, 0))
    #draw rectangle boi
    pygame.draw.rect(wdw, (0, 255, 255), (cx, cy, cw, ch))
    #refresh window
    pygame.display.update()
    print("Accel: ", accel, "Vel: " ,vel,"slow: ",slow)
pygame.quit()
