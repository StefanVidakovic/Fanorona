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
        # largeText = pygame.font.SysFont("arielLrgms",115)
        # TextSurf, TextRect = text_objects("Fanorona", largeText)
        # TextRect.center = ((display_width/2),(display_height/2))
        # gameDisplay.blit(TextSurf, TextRect)

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
        for i in range(height): # 5.0/2.0 = 2.5    5//2 = 2 (width-1)/2
            if board[i][j]==BoardContent.EMPTY:
                tempx,tempy = coordinateToPixel(i,j)
                empty_pixel_array_y.append(tempx)
                empty_pixel_array_x.append(tempy)
                print('')

    # x = [x for x in board if in x][0]
    # print 'The index is (%d,%d)'%(a.index(x),x.index(3))
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
    return(x,y) #arguments: array x and y coordinates

#waiting for user to make a selection of either the peice they want or the empty space to move to.
def select_pearl(pixel_array_x,pixel_array_y,consecutive=False,new_x=None,new_y=None):
    global USER_TURN
    selected_x,selected_y = None,None
    #print('this is pixel array',pixel_array_x,pixel_array_y)
    while(True):
        ev = pygame.event.get()
        min_x, min_y = [],[]
        #print(pixel_array_x,pixel_array_y)
        for event in ev:
            #selecting the gamepeice we want
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                #print('mouse coordinates',mouse[0],mouse[1])
                selected_x,selected_y = mouse[0],mouse[1]
                if consecutive == false:
                    if selected_x >250 and selected_x < 550 and selected_y > 770:
                        print ('hitting end game ')
                        #end turn is True
                        USER_TURN = False
                        return(None,None)
                    else:
                        for i in range(len(pixel_array_x)):
                            min_x.append(abs(selected_x - pixel_array_x[i]))
                            min_y.append(abs(selected_y - pixel_array_y[i]))

                        old_x = min_x.index( min(min_x) )
                        old_y = min_y.index( min(min_y) )
                        selected_x,selected_y = pixel_array_x[min_x.index( min(min_x) )], pixel_array_y[min_y.index( min(min_y) )]
                        #print('selectedx',selected_x)
                        #print('selectedy',selected_y)
                        return(selected_x,selected_y)
                else:
                    return(new_x,new_y)


def select_move(pixel_array_x,pixel_array_y,selected_x,selected_y,board_array):
    #selecting the empty spot to move to, Pass in the empty pixel array
    currentx = selected_x
    currenty = selected_y
    while(True):
        ev = pygame.event.get()
        min_x, min_y = [],[]
        #print(pixel_array_x,pixel_array_y)
        for event in ev:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                #print('mouse coordinates',mouse[0],mouse[1])
                selected_x,selected_y = mouse[0],mouse[1]

                for i in range(len(pixel_array_x)):
                    min_x.append(abs(selected_x - pixel_array_x[i]))
                    min_y.append(abs(selected_y - pixel_array_y[i]))

                print(min_x,min_y)
                new_x = min_x.index( min(min_x) )
                new_y = min_y.index( min(min_y) )
                #print('empty_pixel_array_x',pixel_array_x[min_x.index( min(min_x) )])
                #print('empty_pixel_array_y',pixel_array_y[min_y.index( min(min_y) )])
                selected_x,selected_y = pixel_array_x[min_x.index( min(min_x) )], pixel_array_y[min_y.index( min(min_y) )]
                print('selected_x',selected_x,'selected_y',selected_y)
                print(abs(mouse[0]-currentx),abs(mouse[0]-selected_x))
                print((abs(mouse[1]-currenty)), abs(mouse[1]-selected_y))
                if (abs(mouse[0]-currentx)) <= abs(mouse[0]-selected_x) and (abs(mouse[1]-currenty)) <= abs(mouse[1]-selected_y):
                    print('do we go into deselect')
                    deselect = True
                    drawGameplay(boardImage,board_array,whitePearl,False,currentx,currenty,True) #removes green highlight from screen
                    return(None,None)
                    # selected_x,selected_y = select_pearl(pixel_array_x,pixel_array_y)
                    # new_x,new_y = select_move(pixel_array_x,pixel_array_y,selected_x,selected_y)
                return(selected_x,selected_y) #return new_x,new_y

#                (board png  , board array,green pearl png, selected TorF,selectedx,selectedy)
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
    # exception(error):
    #           try:
    #           print('Invalid try again')
    #           continue


def delete_pearls():
    pass


def check_BI_DIRECTIONAL(arrow_img_left,arrow_img_right,board_array,old_x,old_y,new_x,new_y):
    # if board_array[new_x + 3*(new_x-old_x)][new_y + 3*(new_y-old_y)] == BoardContent.BLACK and board_array[new_x + 4*(new_x-old_x)][new_y + 4*(new_y-old_y)] == BoardContent.BLACK and board_array[new_x - 2*(new_x-old_x)][new_y + 4*(old_y-old_y)]:
    #print('This is a BI-DIRECTIONAL MOVE')
    #draw_Arrows(arrow_img_left,arrow_img_right,arrowx,arrowy)
    pass


def BI_DIRECTIONAL():
    pass

def end_Turn():
    USER_TURN = False

def draw_Arrows(arrow_img_left,arrow_img_right,new_x,new_y):
    gameDisplay.blit(arrow_img_left,(new_x-50,new_y-15))
    gameDisplay.blit(arrow_img_right,(new_x+50,new_y-15))
    pygame.display.update()



#~~~~MAIN GAME LOOP~~~~
def gameLoop():
    global USER_TURN
    gameExit = False
    x = (window_width * 0.45)
    y = (window_height * 0.8)
    x_change = 0
    gameDisplay.fill(light_brown)
    board_array = newGameBoard()
    boardgraph = BoardContent()
    boardgraph.make_board_graph(board_array,5,5)
    boardgraph.add_piece_token((1,2),0)
    boardgraph.remake_board_array(5,5)

    # old_boardgraph = copy.deepcopy(boardgraph)

    pixel_array_x,pixel_array_y = drawGameplay(boardImage,board_array,selected_image)
    pygame.display.update()
    count = 0
    consecutive = False
    #print(board_array)
    #print(boardgraph._board)

    #MAIN GAMEPLAY DECISION BETWEEN USER AND AI
    while not gameExit:
        print('this is user turn',USER_TURN)
        if USER_TURN == True:
            #if the move is not consecutive allow the user to select any pearl
            if consecutive == False:
                selected_x,selected_y = select_pearl(pixel_array_x,pixel_array_y) #user selected a pearl
                #print(selected_x,selected_y)

                #if end turn is initiated we must stop
                if selected_x == None and selected_y == None:
                    #end turn initiated
                    pass
            # if the move IS consecutive the same peice can only be selected.
            else:
                selected_x,selected_y = select_pearl(pixel_array_x,pixel_array_y,True,new_x,new_y) #user selected a pearl

                #if end turn is initiated we must stop
                if selected_x == None and selected_y == None:
                    #end turn initiated
                    pass
            else:
                pixel_array_x,pixel_array_y = drawGameplay(boardImage,board_array,selected_image,True,selected_x,selected_y)#printed the green selection from user to screen
                empty_pixel_array_x,empty_pixel_array_y = checkEmpty(board_array) # checked for empty spaces to move to
                new_x,new_y = select_move(empty_pixel_array_x,empty_pixel_array_y,selected_x,selected_y,board_array)
                print('this is newx,newy',new_x,new_y)
                count+=1
                print(count)

                #allows the user to deselect choice
                if new_x != None and new_y != None:
                    print('are we in here?')
                    print(count)
                    old_x, old_y = pixelToCoordinate(selected_x, selected_y)
                    # print('pixel coordinate versions(oldx,oldy):',old_x,old_y)
                    # print('pixel coordinate versions(newx,newy):'newx',new_x,'newy',new_y)

                    arrowx,arrowy = new_x,new_y
                    new_x,new_y = pixelToCoordinate(new_x,new_y)
                    #print('newx (board posistion)',new_x,'newy(boardposistion)',new_y)


                    #CHECKING TO SEE IF THE MOVE IS ALLOWED
                    old_board_array = board_array #saving old board config incase move is false/invalid
                    board_array,boardgraph = check_move(boardgraph,1,(old_y,old_x),(new_y,new_x)) #boardgraph will be most recent graph of the game

                    #if the move is not allowed
                    if board_array == False:
                        board_array = old_board_array
                        # boardgraph = old_boardgraph
                        ERROR_INVALIDMOVE = arielSmall.render("INVALID MOVE, PLEASE TRY AGAIN",True,light_green)
                        gameDisplay.blit(ERROR_INVALIDMOVE,(150,3))
                        pygame.display.update()
                        pygame.time.delay(1000)
                        gameDisplay.fill(light_brown)
                        pixel_array_x,pixel_array_y = drawGameplay(boardImage,board_array,selected_image,True,selected_x,selected_y)
                        drawGameplay(boardImage,board_array,whitePearl,False,selected_x,selected_y,True)
                        pygame.display.update()

                    #if the move is allowed
                    else:
                        for row in board_array:
                            print(*row)
                        print()

                        pixel_array_x,pixel_array_y = drawGameplay(boardImage,board_array,selected_image,True,selected_x,selected_y)
                        gameDisplay.fill(light_brown)
                        pixel_array_x,pixel_array_y = drawGameplay(boardImage,board_array,selected_image)
                        pygame.display.update() # by default updates everyting in the window, but you can pass a single parameter to just update a single element
                        clock.tick(FPS) #THIS IS THE NUMBER OF FPS
                        # print(board_array)
                        # print(boardgraph._board)
                        print('newx,y',new_x,new_y)
                        print(boardgraph._board)
                        consecutive = check_consecutive_move(boardgraph,new_x,new_y)
                        print('this is consecutive',consecutive)
                        if consecutive == True:
                            button("END TURN",250,775,300,30,dark_brown,light_brown,end_Turn)
                            END_TURN = arielSmall.render("END TURN?",True,BLACK)
                            gameDisplay.blit(END_TURN,(325,770))
                            pygame.display.update()
                        else:
                            USER_TURN = False
        else:
            print('ai turn')
            AI_TURN = arielMed.render("AI_TURN",True,BLACK)
            gameDisplay.blit(AI_TURN,(325,3))
            pygame.display.update()
            pygame.time.delay(1000)
            move_list = move_generator(boardgraph,BoardContent.BLACK)
            rand = random.randint(0, len(move_list)-1)
            newgraph = move_list[rand]
            print(board_array)
            if type(newgraph)==list:
                temp = newgraph[len(newgraph)-1]
                for i in range(len(temp)):
                    newgraph = temp[i]
                    # boardgraph = newgraph
                    board_array = newgraph.remake_board_array(5,5)
                    drawGameplay(boardImage,board_array,blackPearl)
                    gameDisplay.fill(light_brown)
                    pixel_array_x,pixel_array_y = drawGameplay(boardImage,board_array,blackPearl)
                    pygame.display.update()
                    pygame.time.delay(4000)
            # boardgraph = newgraph
            print('end of ai ')
            drawGameplay(boardImage,board_array,blackPearl)
            boardgraph = copy.deepcopy(newgraph)
            board_array = boardgraph.remake_board_array(5,5)
            gameDisplay.fill(light_brown)
            pixel_array_x,pixel_array_y = drawGameplay(boardImage,board_array,blackPearl)
            print('pixel aray x,y',pixel_array_x,pixel_array_y)
            pygame.display.update()
            USER_TURN=True
            print(board_array)

#like main():
print(pygame.font.get_fonts())
game_intro()
gameLoop()
pygame.quit()
quit()


#EXTRA SHIT I THATS USEFUL FOR REFERENCE BUT DOESNT BELONG ABOVE!!!!

# for event in pygame.event.get():
#     print(event)
#old_x, old_y, new_x, new_y = map(lambda n: int(n), input().split())
#movement stuff
#x = x+ x_change
'''
pixel translation bullshit
#     gameDisplay.blit(whitePearl,(10,725))  # 0, 4
#     gameDisplay.blit(whitePearl,(185,725)) # 1, 4
#     gameDisplay.blit(whitePearl,(360,725)) # 2, 4
#     gameDisplay.blit(whitePearl,(535,725)) # 3, 4
#     gameDisplay.blit(whitePearl,(710,725)) # 4, 4
#     gameDisplay.blit(whitePearl,(10,550))  # 0, 3
#     gameDisplay.blit(whitePearl,(185,550)) # 1, 3
#     gameDisplay.blit(whitePearl,(360,550)) # 2, 3
#     gameDisplay.blit(whitePearl,(535,550)) # 3, 3
#     gameDisplay.blit(whitePearl,(710,550)) # 4, 3

#     gameDisplay.blit(blackPearl,(10,25))   # 0, 0
#     gameDisplay.blit(blackPearl,(185,25))  # 1, 0
#     gameDisplay.blit(blackPearl,(360,25))    2,0
#     gameDisplay.blit(blackPearl,(535,25))    3,0
#     gameDisplay.blit(blackPearl,(710,25))    0,1
#     gameDisplay.blit(blackPearl,(10,200))     1,1
#     gameDisplay.blit(blackPearl,(185,200))   2,1
#     gameDisplay.blit(blackPearl,(360,200))       ,1
#     gameDisplay.blit(blackPearl,(535,200))
#     gameDisplay.blit(blackPearl,(710,200))
'''

# for event in pygame.event.get(): #pygame grabs events , wheres the mouse on the screen, are they pressing keys etc
#     print(event)
#     if event.type == pygame.QUIT: #if you hit the close button on the window pygame exits
#         gameExit = True
#     #button interaction examples not needed now but could be useful in future for pause/play functionality etc
#     print('why dont we get here?')
#     if event.type == pygame.KEYDOWN: # if key is pressed....what do we want to do?
#         print('how often do we come here?')
#         if event.key == pygame.K_e: # !!!!USE THIS TO END TURN AFTER NUMBER OF MOVES.
#             endTurn = True
#             print(endTurn)
#         elif event.key == pygame.K_RIGHT: # Right arrow key pressed
#             x_change = 5
#     if event.type == pygame.KEYUP: #if key is released... what do we want to do?
#         if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
#             x_change = 0
#     #print(event)
#

# board_array = movePiece(board_array, old_x, old_y,new_x,new_y)
# boardgraph.pearl_update((new_y,new_x),(old_y,old_x))
#check_BI_DIRECTIONAL(arrow_img_left,arrow_img_right,board_array,old_x,old_y,new_x,new_y)
#draw_Arrows(arrow_img_left,arrow_img_right,arrowx,arrowy)
