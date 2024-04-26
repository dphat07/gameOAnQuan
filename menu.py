import pygame,sys
import random
import copy
from Button import Button

#initialize pygame
pygame.init()

#constraint variables
SCREENWIDTH = 1280
SCREENHEIGHT = 720

timer = 0
time_lock = 8000

selected_btn_index_Up = []
selected_btn_index = []
list_btn = []
list_data = []

indexRandom = 0

turn = -1 # Human play

isEatLeft = False
isEatRight = False
isSave = False

scorePlayer = 0
scoreComputer = 0
scorePlayer1 = 0
scorePlayer2 = 0
score = 0

color = "#d7fcd4"
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

font = pygame.font.SysFont("font.ttf",30)
bigfont = pygame.font.SysFont("font.ttf",50)


SCREEN = pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))
pygame.display.set_caption("Game Ô Ăn Quan")

#background 
background = pygame.image.load("background.png")
def display_background():
    SCREEN.blit(background,(0,0))

#font word
def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("font.ttf", size)

#button_play_computer
scale = 0.8
playImg = pygame.image.load("rect.png")
playImg = pygame.transform.scale(playImg,(playImg.get_width()*3.4*scale,playImg.get_height()*scale))
playX = 640
playY = 300

#button_play_human
scale = 0.8
playhumanImg = pygame.image.load("rect.png")
playhumanImg = pygame.transform.scale(playhumanImg,(playhumanImg.get_width()*2.5*scale,playhumanImg.get_height()*scale))
playhumanX = 640
playhumanY = 400

#button_guide
scale = 0.8
guideImg = pygame.image.load("rect.png")
guideImg = pygame.transform.scale(guideImg,(guideImg.get_width()*scale,guideImg.get_height()*scale))
guideX = 640
guideY = 500

#button_quit
scale = 0.8
quitImg = pygame.image.load("rect.png")
quitImg = pygame.transform.scale(quitImg,(quitImg.get_width()*scale,quitImg.get_height()*scale))
quitX = 640
quitY = 600


def draw_button(x, y, width, height, color):
    pygame.draw.rect(SCREEN, color, (x, y, width, height))

def CheckEmptyHuman(scorePlayer):
    flag = True
    for i in range(11,6,-1):
        if (list_btn[i][2] != 0):                    
            flag = False

    if (flag == True):
        for i in range (11,6,-1):
            list_btn[i][2] = 1
        scorePlayer -= 5
    return flag

def spreadTroopsHuman(): # Rải quân cho Human
    for i in range(11,6,-1):
        x_pos_init = list_btn[i][0] 
        y_pos_init = list_btn[i][1] 
        pygame.draw.circle(SCREEN,BLACK,[x_pos_init, y_pos_init],1)

def CheckEmptyComputer(scoreComputer): # Kiểm tra các ô quân của Human hết hay chưa
    flag = True
    for i in range(1,6):
        if (list_btn[i][2] != 0):                    
            flag = False
    if (flag == True):
        for i in range (1,6):
            list_btn[i][2] = 1
        scoreComputer -= 5
    return flag

def spreadTroopsComputer(): # Rải quân cho Computer
    for i in range(1,6):
        x_pos_init = list_btn[i][0] 
        y_pos_init = list_btn[i][1] 
        pygame.draw.circle(SCREEN,BLACK,[x_pos_init, y_pos_init],1)

def Victory(scorePlayer,scoreComputer): # Xem ai Win Game
        if (list_btn[0][2] == 0 and list_btn[6][2] == 0 and isEatLeft == True and isEatRight == True):
            if scorePlayer > scoreComputer:
                print ("Player Win")    
            elif(scorePlayer < scoreComputer):
                print ("Computer Win")
            else:
                print("Draw")
            return True
        if CheckEmptyHuman(scorePlayer) == True:
            spreadTroopsHuman()
        if CheckEmptyComputer(scoreComputer) == True:
            spreadTroopsComputer()
        return False

def VictoryHuman(scorePlayer,scoreComputer): # Xem ai Win Game
        if (list_btn[0][2] == 0 and list_btn[6][2] == 0 and isEatLeft == True and isEatRight == True):
            if scorePlayer > scoreComputer:
                print ("Player 2 Win")    
            elif(scorePlayer < scoreComputer):
                print ("Player 1 Win")
            else:
                print("Draw")
            return True
        if CheckEmptyHuman(scorePlayer) == True:
            spreadTroopsHuman()
        if CheckEmptyComputer(scoreComputer) == True:
            spreadTroopsComputer()
        return False

def minimax():
  
    score = 0
    diem = 0
  
    step_tang = 1
  
    for i in range (1,6):
        list_test = copy.deepcopy(list_btn)
        if  (list_test[i][2] > 0):
            count = list_test[i][2]
            list_test[i][2] = 0
            index = i
            while count != 0: 
                index = (index + step_tang) % len(list_test)
                list_test[index][2] += 1
                count -=1
                if (count == 0 and (index + step_tang) % len(list_test) != 0 and (index + step_tang) % len(list_test) !=6):
                    getScore = True
                    while getScore == True:                    
                        next = (index + step_tang) % len(list_test)
                        if (list_test[next][2] != 0):
                            count = list_test[next][2]
                            list_test[next][2] = 0
                            index = next
                            getScore = False
                        else:
                            nextOfNext = (next + step_tang) % len(list_test)
                            if (list_test[nextOfNext][2] == 0):
                                getScore = False
                            else:
                                score += list_test[nextOfNext][2]
                                if nextOfNext == 0:
                                    score += 10
                                   
                                if nextOfNext == 6:
                                    score += 10
                                list_test[nextOfNext][2] = 0
                                                                  
                                break
                if count == 0:
                    diem += score
                    data_tuple = (i, step_tang, score)      
                    list_data.append(data_tuple)
        else:
            data_tuple = (i, 0, 0)    
            list_data.append(data_tuple)

def minimax_nguoc():
   
    score = 0
    diem = 0
   
    step_giam = -1

    for i in range (5,0,-1): 
        list_test_nguoc =copy.deepcopy(list_btn)
        if  (list_test_nguoc[i][2] > 0):
            count = list_test_nguoc[i][2]
            list_test_nguoc[i][2] = 0
            index = i
            while count != 0: 
                index = (index + step_giam) % len(list_test_nguoc)
                list_test_nguoc[index][2] += 1
                count -=1
                if (count == 0 and (index + step_giam) % len(list_test_nguoc) != 0 and (index + step_giam) % len(list_test_nguoc) !=6):
                    getScore = True
                    while getScore == True:
                        
                        next = (index + step_giam) % len(list_test_nguoc)
                        if (list_test_nguoc[next][2] != 0):
                            count = list_test_nguoc[next][2]
                            list_test_nguoc[next][2] = 0
                            index = next
                            getScore = False
                        else:
                            nextOfNext = (next + step_giam) % len(list_test_nguoc)
                            if (list_test_nguoc[nextOfNext][2] == 0):
                                getScore = False
                            else:
                                score += list_test_nguoc[nextOfNext][2]
                                if nextOfNext == 0:
                                    score += 10
                                 
                                if nextOfNext == 6:
                                    score += 10
                                list_test_nguoc[nextOfNext][2] = 0
                                              
                        
                                break
                if count == 0:
                    diem += score
                    data_tuple = (i, step_giam, score)      
                    list_data.append(data_tuple)  
        else:
            data_tuple = (i, 0, 0)    
            list_data.append(data_tuple)

def RouteComputer():
    index = list_data[0][0]
    dir = list_data[0][1]
    max = list_data[0][2]
    for i in range (len(list_data)):
        if (list_data[i][2] >= max and list_data[i][1] != 0):
            max = list_data[i][2]
            index = list_data[i][0]
            dir = list_data[i][1]
    print (list_data)
    print (index)
    print (dir)
    return [index, dir]

def randomIndexComputer ():
    index = 0
    count = 0
    list_data = []
    
    for i in range (1,6):
        if (list_btn[i][2] > 0):
            list_data.append(i)
    if (len(list_data) > 0):
        return random.choice(list_data)
    
    else:
        return 0
   
def DrawGame():
    global isSave
    global isEatLeft
    global isEatRight

    buttonX_Up = 350
    buttonY_Up = 220
    
    buttonX_Down = 870
    buttonY_Down = 350
    
    buttonX_Left = 240
    buttonY_Left = 250

    buttonX_Right = 1010
    buttonY_Right = 250

    for i in range (12):
        
        
        # draw_button(buttonX_Up, buttonY_Up , 120, 120, GREEN)         
        draw_button(buttonX_Down, buttonY_Down , 120, 120, GREEN)

        rectLeft=pygame.draw.rect(SCREEN,color,(220,220,120,250),border_top_left_radius=50,border_bottom_left_radius=50)
        rectRight=pygame.draw.rect(SCREEN,color,(1000,220,120,250),border_top_right_radius=50,border_bottom_right_radius=50)

        if (len(selected_btn_index) != 0 and selected_btn_index[0][0] == buttonX_Down and selected_btn_index[0][1] == buttonY_Down):                   
            draw_button(buttonX_Down, buttonY_Down , 120, 120, RED)
            
    
        if (len(selected_btn_index_Up) != 0 and selected_btn_index_Up[0][0] == buttonX_Up and selected_btn_index_Up[0][1] == buttonY_Up):                   
            draw_button(buttonX_Up, buttonY_Up, 120, 120, BLUE)

        if (indexRandom > 0):
            draw_button(220 + indexRandom * 130, 220 , 120, 120, RED)
              

        if (i  == 0):
            if (isSave == False):
                list_btn.append([buttonX_Left,buttonY_Left,0])
            
        if (i in range (1,6)):
            draw_button(buttonX_Up, buttonY_Up , 120, 120, GREEN)   
            if (i != 0 and isSave == False):
                list_btn.append([buttonX_Up,buttonY_Up,5])
            buttonX_Up += 130

        if (i == 6):
            if (isSave ==  False):
                list_btn.append([buttonX_Right,buttonY_Right,0])
        
        if (i in range(11,6,-1)):
            if (i != 0 and isSave == False):
                list_btn.append([buttonX_Down,buttonY_Down,5])
            buttonX_Down -= 130
            

    #Draw Circle Up
    
    for i in range(len(list_btn)):
        if (i in range (1,6)):
            x_pos_init = list_btn[i][0] + 20
            y_pos_init = list_btn[i][1] + 10
            for j in range (list_btn[i][2]):
                x_pos = x_pos_init + (j % 5) * 20 
                if j % 5 == 0 and j != 0:
                    y_pos_init += 20
                y_pos = y_pos_init
                pygame.draw.circle(SCREEN,BLACK,[x_pos, y_pos],5)

    # Draw Circle Down
    for i in range (len(list_btn)):
        if(i in range(11,6,-1)):
            x_pos_init = list_btn[i][0] + 20
            y_pos_init = list_btn[i][1] + 10
            for j in range (list_btn[i][2]):
                x_pos = x_pos_init + (j % 5) * 20 
                if j % 5 == 0 and j != 0:
                    y_pos_init += 20

                y_pos = y_pos_init
                pygame.draw.circle(SCREEN,BLACK,[x_pos, y_pos],5)

    # Draw O Quan Trai
    x_pos_init = list_btn[0][0] 
    y_pos_init = list_btn[0][1]
    for i in range (list_btn[0][2]):
        x_pos_init += 15 + (i % 5)
        if i % 5 == 0 and i != 0:
                y_pos_init += 20
                x_pos_init =  list_btn[0][0] 
        pygame.draw.circle(SCREEN,BLACK,[x_pos_init, y_pos_init],5)
    if (isEatLeft == False):
        pygame.draw.circle(SCREEN,BLUE,(240,400),15)
    

    # Draw O Quan Phai
    x_pos_init = list_btn[6][0] 
    y_pos_init = list_btn[6][1]
    for i in range (list_btn[6][2]):
        x_pos_init += 15 + (i % 5)
        if i % 5 == 0 and i != 0:
                y_pos_init += 20
                x_pos_init =  list_btn[6][0] 
        pygame.draw.circle(SCREEN,BLACK,[x_pos_init, y_pos_init],5)
    if (isEatRight == False):
        pygame.draw.circle(SCREEN,BLUE,(1100,400),15)

     
def ShowScore():
    global scorePlayer
    global scoreComputer
    name_computer = bigfont.render("COMPUTER",True,WHITE)
    SCREEN.blit (name_computer,(20,20))
    score_word = font.render("Score x  " + str(scoreComputer),True,WHITE)
    SCREEN.blit (score_word,(20,55))

    name_player = bigfont.render("PLAYER",True,WHITE)
    SCREEN.blit (name_player,(20,600))
    score_word = font.render("Score x  " + str(scorePlayer),True,WHITE)
    SCREEN.blit (score_word,(20,635))

def ShowScoreHuman():
    global scorePlayer1
    global scorePlayer2
    name_human1 = bigfont.render("PLAYER 1",True,WHITE)
    SCREEN.blit (name_human1,(20,20))
    score_word = font.render("Score x  " + str(scorePlayer1),True,WHITE)
    SCREEN.blit (score_word,(20,55))

    name_human2 = bigfont.render("PLAYER 2",True,WHITE)
    SCREEN.blit (name_human2,(20,600))
    score_word = font.render("Score x  " + str(scorePlayer2),True,WHITE)
    SCREEN.blit (score_word,(20,635))
    
def playComputer():
    global scorePlayer
    global scoreComputer
    score = 0
    global indexRandom
    global isSave 
    global isEatLeft 
    global isEatRight
    global list_data
    turn = -1
    while True:
        PLAYCOMPUTER_MOUSE_POS = pygame.mouse.get_pos()
        display_background()

        #ArrowLeft
        arrowLeftIMG = pygame.image.load("left.png")
        arrowLeftIMG=pygame.transform.scale(arrowLeftIMG,(150,150))
        arrowLeftX_Down = 520
        arrowLeftY_Down = 480
        button_rect_Left = pygame.Rect(arrowLeftX_Down, arrowLeftY_Down, 150, 150)
        
        #ArrowRight
        arrowRightIMG = pygame.image.load("right.png")
        arrowRightIMG=pygame.transform.scale(arrowRightIMG,(150,150))
        arrowRightX_Down = 680
        arrowRightY_Down = 480
        button_rect_Right = pygame.Rect(arrowRightX_Down, arrowRightY_Down, 150, 150)
       
        DrawGame()
        ShowScore()

        PLAYCOMPUTER_BACK = Button(image=None, pos=(1225, 700), text_input="BACK", font=get_font(20), base_color="White", hovering_color="Green")
        PLAYCOMPUTER_BACK .changeColor(PLAYCOMPUTER_MOUSE_POS)
        PLAYCOMPUTER_BACK .update(SCREEN)
        pygame.display.update
        
        step = 0
        index = 0

        # if (turn == 1):
        #     minimax()
        #     minimax_nguoc()
        #     predict = RouteComputer()
            # selected_btn_index.append(list_btn[predict[0]])
            # step = predict[1]
            # print (predict)

        if (isSave == False):
            isSave = True

        if len(selected_btn_index) != 0:
            SCREEN.blit(arrowLeftIMG,(arrowLeftX_Down,arrowLeftY_Down))
            SCREEN.blit(arrowRightIMG,(arrowRightX_Down,arrowRightY_Down))
            for event in pygame.event.get():   
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if button_rect_Left.collidepoint(mouse_pos):   
                        step = -1 * turn
                    if button_rect_Right.collidepoint(mouse_pos):  
                        step = 1 * turn
                    if (step != 0): 
                        for i in range (len(list_btn)):
                            if selected_btn_index[0] == list_btn[i]:
                                count = list_btn[i][2]
                                list_btn[i][2] = 0
                                index = i
                                while count != 0: 
                                    index = (index + step) % len(list_btn)
                                    # print (index)
                                    list_btn[index][2] += 1
                                    count -=1
                                    if (count == 0 and (index + step) % len(list_btn) != 0 and (index + step) % len(list_btn) !=6):
                                        getScore = True
                                        while getScore == True:
                                            next = (index + step) % len(list_btn)
                                            if (list_btn[next][2] != 0):
                                                count = list_btn[next][2]
                                                list_btn[next][2] = 0
                                                index = next
                                                getScore = False
                                            else:
                                                nextOfNext = (next + step) % len(list_btn)
                                                if (list_btn[nextOfNext][2] == 0):
                                                    getScore = False
                                                else:
                                                    score += list_btn[nextOfNext][2]
                                                    if nextOfNext == 0 and isEatLeft == False:
                                                        score += 10
                                                        isEatLeft = True
                                                    if nextOfNext == 6 and isEatRight == False:
                                                        score += 10
                                                        isEatRight = True
                                                    list_btn[nextOfNext][2] = 0
                                                    if turn == -1:
                                                        scorePlayer += score
                                                    else:
                                                        scoreComputer += score
                                                    score = 0
                                                    break
                                    if Victory(scorePlayer,scoreComputer) == True:
                                        turn = 0

                                    if count == 0 and turn == -1: 
                                        turn = 1
                                        # index = randomIndexComputer()
                                        minimax()
                                        minimax_nguoc()
                                        predict = RouteComputer()
                                        index =  predict[0]
                                        print ("Index" + str(index))
                                        selected_btn_index[0] = list_btn[index]
                                        indexRandom = index
                                        if (index > 0 ):
                                            count = list_btn[index][2]
                                        # step = random.choice([1,-1])
                                        step = predict[1]
                                        # step = RouteComputer
                                        print ("Step" + str(step))
                                        DrawGame()
                                        ShowScore()
                                        pygame.display.update()
                                        pygame.time.wait(3000)
                                        indexRandom = 0
                                        list_btn[index][2] = 0
                                        list_data = []

                             
                                  
                                turn = turn * (-1)
                                selected_btn_index.pop()
                                print (selected_btn_index)

                                break
            
        for event in pygame.event.get():   
            if event.type == pygame.MOUSEBUTTONDOWN:
                            mouse_pos = pygame.mouse.get_pos()
                            for i in range(len(list_btn)):
                                button_rect = pygame.Rect(list_btn[i][0], list_btn[i][1], 120, 120)        
            # Check if the mouse click is within the button area
                                if button_rect.collidepoint(mouse_pos):
                                    if (len(selected_btn_index) == 0):
                                        selected_btn_index.append(list_btn[i])                          
                                    else:
                                        if selected_btn_index[0][0] == list_btn[i][0] and selected_btn_index[0][1] == list_btn[i][1]:
                                            selected_btn_index.pop()
                                        else:
                                            selected_btn_index[0] = list_btn[i]
                                    break
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAYCOMPUTER_BACK.checkForInput(PLAYCOMPUTER_MOUSE_POS):
                    main_menu()
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
        pygame.display.update()  
                      
def playHuman():
    
    score = 0
    global indexRandom
    global isSave 
    global isEatLeft 
    global isEatRight
    global list_data
    global scorePlayer1
    global scorePlayer2
    turn = -1
    while True:
        PLAYCOMPUTER_MOUSE_POS = pygame.mouse.get_pos()
        display_background()

        #ArrowLeft
        arrowLeftIMG = pygame.image.load("left.png")
        arrowLeftIMG=pygame.transform.scale(arrowLeftIMG,(150,150))
        arrowLeftX_Down = 520
        arrowLeftY_Down = 480
        button_rect_Left = pygame.Rect(arrowLeftX_Down, arrowLeftY_Down, 150, 150)
        
        #ArrowRight
        arrowRightIMG = pygame.image.load("right.png")
        arrowRightIMG=pygame.transform.scale(arrowRightIMG,(150,150))
        arrowRightX_Down = 680
        arrowRightY_Down = 480
        button_rect_Right = pygame.Rect(arrowRightX_Down, arrowRightY_Down, 150, 150)
       
        DrawGame()
        ShowScoreHuman()

        PLAYCOMPUTER_BACK = Button(image=None, pos=(1225, 700), text_input="BACK", font=get_font(20), base_color="White", hovering_color="Green")
        PLAYCOMPUTER_BACK .changeColor(PLAYCOMPUTER_MOUSE_POS)
        PLAYCOMPUTER_BACK .update(SCREEN)
        pygame.display.update
        
        step = 0
        index = 0

    

        if (isSave == False):
            isSave = True

        if len(selected_btn_index) != 0:
            SCREEN.blit(arrowLeftIMG,(arrowLeftX_Down,arrowLeftY_Down))
            SCREEN.blit(arrowRightIMG,(arrowRightX_Down,arrowRightY_Down))
            for event in pygame.event.get():   
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if button_rect_Left.collidepoint(mouse_pos):   
                        step = -1 * turn
                    if button_rect_Right.collidepoint(mouse_pos):  
                        step = 1 * turn
                    if (step != 0): 
                        for i in range (len(list_btn)):
                            if selected_btn_index[0] == list_btn[i]:
                                count = list_btn[i][2]
                                list_btn[i][2] = 0
                                index = i
                                while count != 0: 
                                    index = (index + step) % len(list_btn)
                                    # print (index)
                                    list_btn[index][2] += 1
                                    count -=1
                                    if (count == 0 and (index + step) % len(list_btn) != 0 and (index + step) % len(list_btn) !=6):
                                        getScore = True
                                        while getScore == True:
                                            next = (index + step) % len(list_btn)
                                            if (list_btn[next][2] != 0):
                                                count = list_btn[next][2]
                                                list_btn[next][2] = 0
                                                index = next
                                                getScore = False
                                            else:
                                                nextOfNext = (next + step) % len(list_btn)
                                                if (list_btn[nextOfNext][2] == 0):
                                                    getScore = False
                                                else:
                                                    score += list_btn[nextOfNext][2]
                                                    if nextOfNext == 0 and isEatLeft == False:
                                                        score += 10
                                                        isEatLeft = True
                                                    if nextOfNext == 6 and isEatRight == False:
                                                        score += 10
                                                        isEatRight = True
                                                    list_btn[nextOfNext][2] = 0
                                                    if turn == -1:
                                                        scorePlayer2 += score
                                                    else:
                                                        scorePlayer1 += score
                                                    score = 0
                                                    break

                                    if VictoryHuman(scorePlayer2,scorePlayer1) == True:
                                        turn = 0

                                    if count == 0 and turn == -1: 
                                         if len(selected_btn_index) != 0:
                                        #  if len(selected_btn_index_Up) != 0:
                                            SCREEN.blit(arrowLeftIMG,(arrowLeftX_Down,arrowLeftY_Down))
                                            SCREEN.blit(arrowRightIMG,(arrowRightX_Down,arrowRightY_Down))
                                            for event in pygame.event.get():   
                                                if event.type == pygame.MOUSEBUTTONDOWN:
                                                    mouse_pos = pygame.mouse.get_pos()
                                                    if button_rect_Left.collidepoint(mouse_pos):   
                                                        step = -1 * turn
                                                    if button_rect_Right.collidepoint(mouse_pos):  
                                                        step = 1 * turn
                                                    if (step != 0): 
                                                        for i in range (len(list_btn)):
                                                            if selected_btn_index[0] == list_btn[i]:
                                                            # if selected_btn_index_Up[0] == list_btn[i]:
                                                                count = list_btn[i][2]
                                                                list_btn[i][2] = 0
                                                                index = i
                                                                while count != 0: 
                                                                    index = (index + step) % len(list_btn)
                                                                    # print (index)
                                                                    list_btn[index][2] += 1
                                                                    count -=1
                                                                    if (count == 0 and (index + step) % len(list_btn) != 0 and (index + step) % len(list_btn) !=6):
                                                                        getScore = True
                                                                        while getScore == True:
                                                                            next = (index + step) % len(list_btn)
                                                                            if (list_btn[next][2] != 0):
                                                                                count = list_btn[next][2]
                                                                                list_btn[next][2] = 0
                                                                                index = next
                                                                                getScore = False
                                                                            else:
                                                                                nextOfNext = (next + step) % len(list_btn)
                                                                                if (list_btn[nextOfNext][2] == 0):
                                                                                    getScore = False
                                                                                else:
                                                                                    score += list_btn[nextOfNext][2]
                                                                                    if nextOfNext == 0 and isEatLeft == False:
                                                                                        score += 10
                                                                                        isEatLeft = True
                                                                                    if nextOfNext == 6 and isEatRight == False:
                                                                                        score += 10
                                                                                        isEatRight = True
                                                                                    list_btn[nextOfNext][2] = 0
                                                                                    if turn == -1:
                                                                                        scorePlayer2 += score
                                                                                    else:
                                                                                        scorePlayer1 += score
                                                                                    score = 0
                                                                                    break
                                                                        

                                turn = turn * (-1)
                                selected_btn_index.pop()
                                # selected_btn_index_Up.pop()
                                break
            
        for event in pygame.event.get():   
            if event.type == pygame.MOUSEBUTTONDOWN:
                            mouse_pos = pygame.mouse.get_pos()
                            for i in range (len(list_btn)):
                                button_rect = pygame.Rect(list_btn[i][0], list_btn[i][1], 120, 120) # Check if the mouse click is within the button area
                                if button_rect.collidepoint(mouse_pos):
                                    if (len(selected_btn_index) == 0):
                                        selected_btn_index.append(list_btn[i])                          
                                    else:
                                        if selected_btn_index[0][0] == list_btn[i][0] and selected_btn_index[0][1] == list_btn[i][1]:
                                            selected_btn_index.pop()
                                        else:
                                            selected_btn_index[0] = list_btn[i]
                                    break

                            # for i in range(len(list_btn)):
                            #     button_rect = pygame.Rect(list_btn[i][0], list_btn[i][1], 120, 120) # Check if the mouse click is within the button area
                            #     if button_rect.collidepoint(mouse_pos):
                            #         if (len(selected_btn_index_Up) == 0):
                            #             selected_btn_index_Up.append(list_btn[i])                          
                                     
                            #         else:
                            #             if selected_btn_index_Up[0][0] == list_btn[i][0] and selected_btn_index_Up[0][1] == list_btn[i][1]:
                            #                 selected_btn_index_Up.pop()
                            #             else:
                            #                 selected_btn_index_Up[0] = list_btn[i]
                            #         break

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAYCOMPUTER_BACK.checkForInput(PLAYCOMPUTER_MOUSE_POS):
                    main_menu()
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
        pygame.display.update()  

def guide():
     while True:

        GUIDE_MOUSE_POS = pygame.mouse.get_pos()
        display_background()
        # SCREEN.fill("white")

        OPTIONS_TEXT = get_font(20).render("This is the GUIDE screen.", True, WHITE)
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 70))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)
       # Define your text for each line
        line1 = "Nguoi choi chon mot trong nam o, de bat dau tro choi chon mot o tuy thich."
        line2 = "Nhan <- -> de chon huong di."
        line3 = "Tro choi ket thuc khi 2 ben o QUAN trong."

        # Render each line separately
        text_surface1 = font.render(line1, True, WHITE)
        text_surface2 = font.render(line2, True, WHITE)
        text_surface3 = font.render(line3, True, WHITE)

        # Blit each text surface to your display surface at desired positions
        SCREEN.blit(text_surface1, (200, 200))
        SCREEN.blit(text_surface2, (200, 220))
        SCREEN.blit(text_surface3, (200, 240))

        # Update the display
        # pygame.display.update()

        OPTIONS_BACK = Button(image=None, pos=(1225, 700),text_input="BACK", font=get_font(20), base_color=WHITE, hovering_color="Green")
        OPTIONS_BACK.changeColor(GUIDE_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(GUIDE_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def main_menu():
    running = True
    while running:
        display_background()

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        Game_Title = get_font(70).render("Game Ô Ăn Quan", True, "#b68f40")
        Game_Rect = Game_Title.get_rect(center=(640, 200))


        PLAY_BUTTON = Button(image=playImg, pos=(playX,playY),text_input="Play Vs Computer", font=get_font(55), base_color="#d7fcd4", hovering_color="White")
        PLAY_BUTTON_HUMAN = Button(image=playhumanImg, pos=(playhumanX,playhumanY),text_input="Play Vs Human", font=get_font(55), base_color="#d7fcd4", hovering_color="White")
        GUIDE_BUTTON = Button(image=guideImg, pos=(guideX, guideY),text_input="Guide", font=get_font(55), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=quitImg, pos=(quitX, quitY),  text_input="Quit", font=get_font(55), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)
        SCREEN.blit(Game_Title,Game_Rect)

        for button in [PLAY_BUTTON,PLAY_BUTTON_HUMAN,GUIDE_BUTTON,QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                # pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    playComputer()
                if PLAY_BUTTON_HUMAN.checkForInput(MENU_MOUSE_POS):
                    playHuman()
                if GUIDE_BUTTON.checkForInput(MENU_MOUSE_POS):
                    guide()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()