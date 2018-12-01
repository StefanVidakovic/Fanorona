import pygame
import math
from BoardContent import *
from MoveGeneration import *
import copy
import random

#~~~~INITIALIZATIONS~~~~
pygame.init()
pygame.font.init()
arielLrg = pygame.font.SysFont("Times New Roman, Arial",60)
arielMed = pygame.font.SysFont("Times New Roman, Arial",40)
arielSmall = pygame.font.SysFont("Times New Roman, Arial",30)

#~~~~SETTING UP PROGRAM WINDOW SIZE, BOARD SIZE, FPS, SYSTEM CLOCK, ETC~~~~
window_width = 800
window_height = 800
GRID_WIDTH = 5
GRID_HEIGHT = 5
EMPTY      = 'EMPTY'  # nothing to draw on the grid
FPS = 60
gameDisplay = pygame.display.set_mode((window_width,window_height))
clock = pygame.time.Clock()
global USER_TURN
USER_TURN = True
#Create the window title
pygame.display.set_caption('Fanorona')

#~~~~WE DEFINE COLORS WITH THE RGB METHOD - (BACKLIGHT USED TO DISPLAY COLOR)~~~~

#monochromatic
BLACK = (0,0,0)
WHITE = (255,255,255)
#RGB
red =   (255,0,0)
green = (0,255,0)
blue =  (0,0,255)
#Other Triad Color Combinations from ADOBE CC
military_green  = (120,178,131)
off_purple      = (202,172,255)
light_green     = (146,255,167)
light_brown     = (204,173,138)
dark_brown      = (178,147,111)

#~~~~IMPORTING IMAGES AND GRAPHICS FOR GAMEPLAY~~~~
whitePearl =    pygame.image.load('white-pearl.png')
blackPearl =    pygame.image.load('black-pearl.png')
boardImage      =    pygame.image.load('FiveByFive.png')
selected_image = pygame.image.load('selected-pearl.png')
invalidPearl =  pygame.image.load('invalid-pearl.png')
# arrow_img_left = pygame.image.load('arrow_left.png')
# arrow_img_right = pygame.image.load('arrow_right.png')
gameIcon = pygame.image.load('ICON.png')
pygame.mouse.set_cursor
pygame.display.set_icon(gameIcon)


#~~~~BOARD CONTENT CLASS FOR COMMUNICATING BETWEEN GAMEPLAY FUNCTIONS~~~~


#Sets up the initial game board for beginning a new game, will work with any ODD sized game board
# returns board:[[2, 2, 2, 2, 2], [2, 2, 2, 2, 2], [2, 1, 0, 2, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1]]
'''
b b b b b
b b b b b
b w e b w
w w w w w
w w w w w
'''

def game_intro():

    intro = True

    while intro:
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill(WHITE)
        TITLE = arielLrg.render("FANORONA", True, BLACK)
        START = arielMed.render("Start Game", True, BLACK)
        QUIT = arielMed.render("Quit",True,BLACK)
        gameDisplay.blit(TITLE,(window_width/3.4,window_height/3))
        button("GO!",100,450,200,170,military_green,light_green,gameLoop)
        button("Quit",500,450,200,170,dark_brown,light_brown,quit)
        gameDisplay.blit(START,(110,500))
        gameDisplay.blit(QUIT,(560,500))

        pygame.display.update()
        clock.tick(15)

def outro():

    intro = True

    while intro:
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill(light_brown)
        TITLE = arielLrg.render("FANORONA", True, BLACK)
        START = arielMed.render("Play Again?", True, BLACK)
        QUIT = arielMed.render("Quit",True,BLACK)
        gameDisplay.blit(TITLE,(window_width/3.4,window_height/3))
        button("GO!",100,450,200,170,military_green,light_green,gameLoop)
        button("Quit",500,450,200,170,dark_brown,light_brown,quit)
        gameDisplay.blit(START,(110,500))
        gameDisplay.blit(QUIT,(560,500))

        pygame.display.update()
        clock.tick(15)

def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    print(click)
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac,(x,y,w,h))

        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(gameDisplay, ic,(x,y,w,h))

    # smallText = pygame.font.SysFont("arielLrgms",20)
    # textSurf, textRect = text_objects(msg, smallText)
    # textRect.center = ( (x+(w/2)), (y+(h/2)) )
    # gameDisplay.blit(textSurf, textRect)


def newGameBoard():
    width = 5
    height = 5
    board = [[BoardContent.EMPTY for i in range(width)] for j in range(height)]

    #first two rows black pearls
    for j in range(width):
        for i in range(height//2): # 5.0/2.0 = 2.5    5//2 = 2 (width-1)/2
            board[i][j]=BoardContent.BLACK

    #last two rows white pearls
    for j in range(width):
        for i in range(1+height//2, height):
            board[i][j]=BoardContent.WHITE
    #filling in middle row with alternating black/white and empty middle
    for j in range(width//2):
        i = height//2

        if j%2 == 0:
            board[i][j] = BoardContent.BLACK
            board[i][j + (width//2)+1] = BoardContent.BLACK
        elif j%2 == 1:
            board[i][j] = BoardContent.WHITE
            board[i][j + (width//2)+1] = BoardContent.WHITE

    return board

#checking the game board for empty spaces (BoardContent.EMPTY)
def checkEmpty(board):
    height = 5
    width = 5
    empty_pixel_array_x,empty_pixel_array_y = [],[]

    for j in range(width):
        for i in range(height):
            if board[i][j]==BoardContent.EMPTY:
                tempx,tempy = coordinateToPixel(i,j)
                empty_pixel_array_y.append(tempx)
                empty_pixel_array_x.append(tempy)
                print('')

    return(empty_pixel_array_x,empty_pixel_array_y)

#arguments: array x and y coordinates
def coordinateToPixel(x, y):
    distance_bt_points = 175
    original_displacement_x = 25
    original_displacement_y = 10

    coord_x = distance_bt_points*x + original_displacement_x
    coord_y = distance_bt_points*y + original_displacement_y

    return(coord_x,coord_y) #return the display x and y coordinates
    '''
    x:
    0 -> 10
    1 -> 185
    2 -> 360
    4 -> 710
    '''
#arguments: the display x and y coordinates
def pixelToCoordinate(coord_x,coord_y):
    distance_bt_points = 175
    original_displacement_x = 25
    original_displacement_y = 10

    x = round((coord_x - original_displacement_x)/distance_bt_points)
    y = round((coord_y - original_displacement_y)/distance_bt_points)
    return(x,y) #arguments: array x and y coordinate

#waiting for user to make a selection of either the peice they want or the empty space to move to.
def select_pearl(pixel_array_x,pixel_array_y):
    global USER_TURN
    selected_x,selected_y = None,None
    while(True):
        ev = pygame.event.get()
        min_x, min_y = [],[]
        for event in ev:
            #selecting the gamepeice we want
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                selected_x,selected_y = mouse[0],mouse[1]

                if selected_x >250 and selected_x < 550 and selected_y > 770:
                    print ('hitting end game ')
                    USER_TURN = False
                    return(None,None)
                else:
                    for i in range(len(pixel_array_x)):
                        min_x.append(abs(selected_x - pixel_array_x[i]))
                        min_y.append(abs(selected_y - pixel_array_y[i]))

                    old_x = min_x.index( min(min_x) )
                    old_y = min_y.index( min(min_y) )
                    selected_x,selected_y = pixel_array_x[min_x.index( min(min_x) )], pixel_array_y[min_y.index( min(min_y) )]
                    return(selected_x,selected_y)

def select_move(pixel_array_x,pixel_array_y,selected_x,selected_y,board_array,old_move_locationsArray,consecutive):
    #selecting the empty spot to move to, Pass in the empty pixel array
    currentx = selected_x
    currenty = selected_y
    while(True):
        ev = pygame.event.get()
        min_x, min_y = [],[]
        for event in ev:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                selected_x,selected_y = mouse[0],mouse[1]

                for i in range(len(pixel_array_x)):
                    min_x.append(abs(selected_x - pixel_array_x[i]))
                    min_y.append(abs(selected_y - pixel_array_y[i]))

                print(min_x,min_y)
                new_x = min_x.index( min(min_x) )
                new_y = min_y.index( min(min_y) )
                selected_x,selected_y = pixel_array_x[min_x.index( min(min_x) )], pixel_array_y[min_y.index( min(min_y) )]
                print('selected_x',selected_x,'selected_y',selected_y)
                print(abs(mouse[0]-currentx),abs(mouse[0]-selected_x))
                print((abs(mouse[1]-currenty)), abs(mouse[1]-selected_y))
                if consecutive == True:
                    button("END TURN",250,775,300,30,dark_brown,light_brown,end_Turn)
                    END_TURN = arielSmall.render("END TURN?",True,BLACK)
                    gameDisplay.blit(END_TURN,(325,770))
                    pygame.display.update()
                if (abs(mouse[0]-currentx)) <= abs(mouse[0]-selected_x) and (abs(mouse[1]-currenty)) <= abs(mouse[1]-selected_y):
                    print('do we go into deselect')
                    deselect = True
                    drawGameplay(boardImage,board_array,whitePearl,False,currentx,currenty,True) #removes green highlight from screen
                    return(None,None)
                elif (mouse[0]>250 and mouse[0]<550 and mouse[1]>770):
                    USER_TURN = False
                    return(False,False)
                for moves in old_move_locationsArray:
                    print('old_move_locations',old_move_locationsArray)
                    print('moves',moves)
                    print(selected_x,selected_y)
                    x,y = pixelToCoordinate(selected_x,selected_y)
                    if (x,y) == moves:
                        print('repeat location!!!!!')
                        gameDisplay.fill(light_brown)
                        drawGameplay(boardImage,board_array,whitePearl,False,currentx,currenty,True) #removes green highlight from screen
                        ERROR_INVALIDMOVE_PATH = arielLrg.render("INVALID MOVE!",True,BLACK)
                        INVALID_PATH = arielLrg.render("You cannot go where you've been!",True,BLACK)
                        gameDisplay.blit(ERROR_INVALIDMOVE_PATH,(150,100))
                        gameDisplay.blit(INVALID_PATH,(5,250))
                        pygame.display.update()
                        pygame.time.delay(2000)
                        gameDisplay.fill(light_brown)
                        drawGameplay(boardImage,board_array,whitePearl,False,currentx,currenty,True)
                        pygame.display.update()
                        return (None,None)

                return(selected_x,selected_y) #return new_x,new_y

def drawGameplay(board_image, board_array,selected_image,selected=False,selected_x=None,selected_y=None,deselected=False):
    gameDisplay.blit(board_image,(44,44)) #put board to approx middle of window

    pixel_array_y,pixel_array_x = [],[]
    for j in range(len(board_array)):
        for i in range(len(board_array[j])):
            y, x = coordinateToPixel(i, j)
            pixel_array_y.append(y)
            pixel_array_x.append(x)
            if board_array[i][j] == BoardContent.WHITE: # BoardContent
                gameDisplay.blit(whitePearl,(x,y))
            elif board_array[i][j] == BoardContent.BLACK:
                gameDisplay.blit(blackPearl,(x,y))

    if selected == True:
        #print('selected_x,selected_y',selected_x,selected_y)
        gameDisplay.blit(selected_image,(selected_x,selected_y))
        pygame.display.update()
        #select_move()
    elif deselected == True:
        #input normal white pearl and overwrite green
        gameDisplay.blit(selected_image,(selected_x,selected_y))
        pygame.display.update()
    return pixel_array_x, pixel_array_y

#~~~~MOVE CLASS FOR CHECKING PROPER USER MOVES~~~~
class InvalidMove(Exception):
    pass

def movePiece(board_array, old_x, old_y, new_x, new_y):

    # Edge cases:
    # trying to move more than one jump <--------------- todo
    # old_x, old_y point to an empty space
    # new_x, new_y point to a space with something already in it
    # when able to move diagonally <--------------- todo

    if board_array[new_y][new_x] != BoardContent.EMPTY or board_array[old_y][old_x] == BoardContent.EMPTY: # todo: handle other exceptions
        raise InvalidMove()

    board_array[new_y][new_x] = board_array[old_y][old_x]
    board_array[old_y][old_x] = BoardContent.EMPTY
    return board_array



def end_Turn():
    USER_TURN = False


def check_Result(board):
    height = 5
    width = 5
    temp_array_x,temp_array_y = [],[]
    countWhite=0
    countBlack=0
    for row in board:
        print(*row)
    print()
    for j in range(width):
        for i in range(height):
            if board[i][j] == BoardContent.WHITE:
                countWhite += 1
                print('white',countWhite)

    if countWhite == 0:
        return 'AI WINS'

    for j in range(width):
        for i in range(height):
            if board[i][j]==BoardContent.BLACK:
                countBlack += 1
                print('black count:',countBlack)
    if countBlack ==0:
        return 'USER WINS'

    return None


#~~~~MAIN GAME LOOP~~~~
def gameLoop():
    global USER_TURN
    gameExit = False
    old_move_locationsGraph = []
    old_move_locationsArray = []
    x = (window_width * 0.45)
    y = (window_height * 0.8)
    x_change = 0
    count =0
    consecutive = False
    gameDisplay.fill(light_brown)
    board_array = newGameBoard()
    boardgraph = BoardContent()
    boardgraph.make_board_graph(board_array,5,5)
    pixel_array_x,pixel_array_y = drawGameplay(boardImage,board_array,selected_image)
    pygame.display.update()

    #MAIN GAMEPLAY DECISION BETWEEN USER AND AI
    while not gameExit:

        result = check_Result(board_array)
        print('result',result)
        if result == 'AI WINS':
            gameDisplay.fill(light_brown)
            AIWINS = arielMed.render("Sorry, better luck next time!",True,BLACK)
            gameDisplay.blit(AIWINS,(200,400))
            pygame.display.update()
            pygame.time.delay(3000)
            outro()
        elif result == 'USER WINS':
            gameDisplay.fill(light_brown)
            USERWINS = arielMed.render("Wohoo! Is your name Elon Musk?",True,BLACK)
            gameDisplay.blit(USERWINS,(160,400))
            pygame.display.update()
            pygame.time.delay(3000)
            outro()
        else:
            pass


        if USER_TURN == True:
            userturn = arielMed.render("USER TURN",True,BLACK)
            gameDisplay.blit(userturn,(290,-5))
            pygame.display.update()
            if consecutive== True and new_x != None and new_y != None:
                selected_x,selected_y = coordinateToPixel(new_x,new_y)
                selected_x=selected_x-25+10
                selected_y=selected_y-10+25
                if count>1:
                    old_move_locationsGraph.append((new_y,new_x))
                    old_move_locationsArray.append((new_x,new_y))
            else:
                selected_x,selected_y = select_pearl(pixel_array_x,pixel_array_y) #user selected a pearl
            if selected_x == None and selected_y == None:
                gameDisplay.fill(light_brown)
                pixel_array_x,pixel_array_y = drawGameplay(boardImage,board_array,selected_image)
                pygame.display.update()
                pass
            else:
                pixel_array_x,pixel_array_y = drawGameplay(boardImage,board_array,selected_image,True,selected_x,selected_y)#printed the green selection from user to screen
                empty_pixel_array_x,empty_pixel_array_y = checkEmpty(board_array) # checked for empty spaces to move to
                new_x,new_y = select_move(empty_pixel_array_x,empty_pixel_array_y,selected_x,selected_y,board_array,old_move_locationsArray,consecutive)

                if new_x==False and new_y == False:
                    USER_TURN = False
                    consecutive = False
                    gameDisplay.fill(light_brown)
                    pixel_array_x,pixel_array_y = drawGameplay(boardImage,board_array,whitePearl)
                    pygame.display.update()
                elif new_x != None and new_y != None:
                    old_x, old_y = pixelToCoordinate(selected_x, selected_y)
                    new_x,new_y = pixelToCoordinate(new_x,new_y)

                    #CHECKING TO SEE IF THE MOVE IS VALID OR NOT
                    old_board_array = board_array #saving old board config incase move is false/invalid
                    board_array,boardgraph,capture_flag = check_move(boardgraph,1,(old_y,old_x),(new_y,new_x)) #boardgraph will be most recent graph of the game

                    if board_array == False:
                        board_array = old_board_array
                        gameDisplay.fill(light_brown)
                        pixel_array_x,pixel_array_y = drawGameplay(boardImage,board_array,selected_image,True,selected_x,selected_y)
                        ERROR_INVALIDMOVE = arielMed.render("INVALID MOVE, PLEASE TRY AGAIN",True,military_green)
                        gameDisplay.blit(ERROR_INVALIDMOVE,(70,-5))
                        pygame.display.update()
                        pygame.time.delay(2000)
                        gameDisplay.fill(light_brown)
                        pixel_array_x,pixel_array_y = drawGameplay(boardImage,board_array,selected_image,True,selected_x,selected_y)
                        drawGameplay(boardImage,board_array,whitePearl,False,selected_x,selected_y,True)
                        pygame.display.update()
                    else:
                        count += 1
                        if count==1:
                            old_move_locationsGraph.append((old_y,old_x))
                            old_move_locationsArray.append((old_x,old_y))
                        #fancy board array print
                        for row in board_array:
                            print(*row)
                        print()

                        originx,originy = new_x,new_y #making sure that the user doesnt return to original spot
                        pixel_array_x,pixel_array_y = drawGameplay(boardImage,board_array,selected_image,True,selected_x,selected_y)
                        gameDisplay.fill(light_brown)
                        pixel_array_x,pixel_array_y = drawGameplay(boardImage,board_array,selected_image)
                        pygame.display.update() # by default updates everyting in the window, but you can pass a single parameter to just update a single element
                        clock.tick(FPS) #THIS IS THE NUMBER OF FPS
                        consecutive = check_consecutive_move(boardgraph,new_x,new_y,capture_flag,old_move_locationsGraph)
                        print('this is consecutive',consecutive) #printing if there is a consecutive move or not
                        if consecutive == True:
                            button("END TURN",250,775,300,30,dark_brown,light_brown,end_Turn)
                            END_TURN = arielSmall.render("END TURN?",True,BLACK)
                            gameDisplay.blit(END_TURN,(325,770))
                            pygame.display.update()
                        else:
                            consecutive = False # shouldnt be needed?
                            USER_TURN = False


        else:
            #AI TURN
            count = 0
            old_move_locationsGraph=[]
            old_move_locationsArray=[]
            AI_TURN = arielMed.render("AI TURN",True,BLACK)
            gameDisplay.blit(AI_TURN,(325,-5))
            pygame.display.update()
            pygame.time.delay(2000)
            dummygraph = copy.deepcopy(boardgraph)
            move_list,capture_flag = move_generator(dummygraph,BoardContent.BLACK)
            valdict = dict()
            valdict1 = evaluate_moves(move_list,BoardContent.BLACK)
            dummygraph = copy.deepcopy(boardgraph)
            value,movegraph = alphabeta(dummygraph,17,valdict,-25,25,True)

            for i in move_list:
                if type(i)==list:
                    j = i[len(i)-1]
                    if type(j)==list:
                        k = j[len(j)-1]
                        if k==movegraph:
                            movegraph = j
                    movegraph=i

            if type(movegraph)==list:
                temp = movegraph[len(movegraph)-1]
                if type(temp)==list:
                    for i in range(len(temp)):
                        movegraph = temp[i]
                        print(movegraph)
                        board_array = movegraph.remake_board_array(5,5)
                        drawGameplay(boardImage,board_array,blackPearl)
                        gameDisplay.fill(light_brown)
                        pixel_array_x,pixel_array_y = drawGameplay(boardImage,board_array,blackPearl)
                        pygame.display.update()
                        pygame.time.delay(3000)
                else:
                    movegraph = temp
                    board_array = movegraph.remake_board_array(5,5)
                    drawGameplay(boardImage,board_array,blackPearl)
                    gameDisplay.fill(light_brown)
                    pixel_array_x,pixel_array_y = drawGameplay(boardImage,board_array,blackPearl)
                    pygame.display.update()
                    pygame.time.delay(3000)

            drawGameplay(boardImage,board_array,blackPearl)
            boardgraph = copy.deepcopy(movegraph)
            board_array = boardgraph.remake_board_array(5,5)
            gameDisplay.fill(light_brown)
            pixel_array_x,pixel_array_y = drawGameplay(boardImage,board_array,blackPearl)
            pygame.display.update()
            USER_TURN=True

game_intro()
gameLoop()
outro()
pygame.quit()
quit()
