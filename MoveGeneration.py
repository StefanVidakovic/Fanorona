from BoardContent import *
import copy
from test import *


#THIS FILE CONTAINS MOVE GENERATION, EVALUATIION AND MINIMAX WITH ALPHA BETA PRUNING.


def multicapture(newgraph,deltaxy,cappoint,opponent,withdraw=False):
    #Determines if a capture move can remove more than one pearl
    #and returns the appropriate board state. If a capture is made any
    #consecutive pieces along the same line and capture direction will be captured.
    dummygraph = BoardContent()
    dummygraph._board = newgraph._board.copy()
    if withdraw:
        nextpoint = (cappoint[0]-deltaxy[0],cappoint[1]-deltaxy[1])
    else:
        nextpoint = (cappoint[0]+deltaxy[0],cappoint[1]+deltaxy[1])
    dummygraph.add_piece_token(cappoint,0)
    if dummygraph.within_board(nextpoint) and dummygraph._board[nextpoint][0] == opponent:
        dummygraph.add_piece_token(nextpoint,0)

    else: return False
    if withdraw:
        nextpoint = (cappoint[0]-2*deltaxy[0],cappoint[1]-2*deltaxy[1])
    else:
        nextpoint = (cappoint[0]+2*deltaxy[0],cappoint[1]+2*deltaxy[1])

    if dummygraph.within_board(nextpoint) and dummygraph._board[nextpoint][0] == opponent:
        dummygraph.add_piece_token(nextpoint,0)

    return dummygraph


def approach(newgraph,move,deltaxy,opponent,old_move_locations=[]):
    #Determines whether a move is an approach capture and
    #returns the first piece to be captured.
    cappoint = (move[0]+deltaxy[0],move[1]+deltaxy[1])
    for moves in old_move_locations:
        if move == moves:
            return False
    if newgraph.within_board(cappoint) and newgraph._board[cappoint][0]==opponent:
        return cappoint
    else:
        return False
def withdraw(newgraph,move,deltaxy,opponent,old_move_locations=[]):
    #Determines whether a move is a withdraw capture and
    #returns the first piece to be captured.
    cappoint = (move[0]-2*deltaxy[0],move[1]-2*deltaxy[1])
    for moves in old_move_locations:
        if move == moves:
            return False
    if newgraph.within_board(cappoint) and newgraph._board[cappoint][0]==opponent:
        return cappoint
    else:
        return False

def consecutivecap(graph,v,caplist,opponent,traversed,linedict,decorate):
    #Performs a deapth first search recursively in order to find all possible
    #consecutive captures from an initial board state. Returns a list of
    #consecutive captures.
    traversed.append(v)
    for move in graph.open_neighbours(v):
        if move in traversed:
            continue
        Cgraph = copy.deepcopy(graph)
        Cgraph.pearl_update(move,v)
        Cdeltaxy = (move[0]-v[0],move[1]-v[1])
        Capproachpoint = approach(Cgraph,move,Cdeltaxy,opponent)
        Cwithdrawpoint = withdraw(Cgraph,move,Cdeltaxy,opponent)
        oldv = (v[0]-Cdeltaxy[0],v[1]-Cdeltaxy[1])
        oldmove = (move[0]-Cdeltaxy[0],move[1]-Cdeltaxy[1])
        if (oldv,oldmove) in linedict.keys():
            if linedict[(oldv,oldmove)] == Cdeltaxy:
                continue

        if Capproachpoint and Cwithdrawpoint:
            Cmulti = multicapture(Cgraph,Cdeltaxy,Capproachpoint,opponent)
            linedict[(v,move)] = Cdeltaxy
            if Cmulti:
                caplist.append(Cmulti)
                if len(caplist)==len(consecutivecap(Cmulti,move,caplist,opponent,traversed,linedict,decorate)):
                    decorate[Cmulti] = ("END",move)
                else:
                    decorate[Cmulti] = (None,move)
            else:
                Cgraph.add_piece_token(Capproachpoint,0)
                caplist.append(Cgraph)
                if len(caplist)==len(consecutivecap(Cgraph,move,caplist,opponent,traversed,linedict,decorate)):
                    decorate[Cgraph] = ("END",move)
                else:
                    decorate[Cgraph] = (None,move)
            Cgraph = copy.deepcopy(graph)
            Cgraph.pearl_update(move,v)

        elif Capproachpoint and not Cwithdrawpoint:
            Cmulti = multicapture(Cgraph,Cdeltaxy,Capproachpoint,opponent)
            linedict[(v,move)] = Cdeltaxy
            if Cmulti:
                caplist.append(Cmulti)
                temp = caplist
                if len(caplist)==len(consecutivecap(Cmulti,move,caplist,opponent,traversed,linedict,decorate)):

                    decorate[Cmulti] = ("END",move)
                else:
                    decorate[Cmulti] = (None,move)
            else:
                Cgraph.add_piece_token(Capproachpoint,0)
                caplist.append(Cgraph)
                if len(caplist)==len(consecutivecap(Cgraph,move,caplist,opponent,traversed,linedict,decorate)):
                    decorate[Cgraph] = ("END",move)
                else:
                    decorate[Cgraph] = (None,move)
            Cgraph = copy.deepcopy(graph)
            Cgraph.pearl_update(move,v)
        elif Cwithdrawpoint and not Capproachpoint:
            Cmulti = multicapture(Cgraph,Cdeltaxy,Cwithdrawpoint,opponent,True)
            if Cmulti:
                caplist.append(Cmulti)
                temp = caplist
                if len(caplist)==len(consecutivecap(Cmulti,move,caplist,opponent,traversed,linedict,decorate)):
                    decorate[Cmulti] = ("END",move)
                else:
                    decorate[Cmulti] = (None,move)
            else:
                Cgraph.add_piece_token(Cwithdrawpoint,0)
                caplist.append(Cgraph)
                if len(caplist)==len(consecutivecap(Cgraph,move,caplist,opponent,traversed,linedict,decorate)):
                    decorate[Cgraph] = ("END",move)
                else:
                    decorate[Cgraph] = (None,move)
            Cgraph = copy.deepcopy(graph)
            Cgraph.pearl_update(move,v)
    return caplist



def move_generator(boardgraph,pearl):
    #Generates a list of valid moves. Non-capture moves are not
    #returned if a capture is possible. Moves are represented as new board
    #graph states. Consecutive captures are stored as nested lists formatted
    #as follows: If a series of consecutive caps is represented by the list
    # [1,2,3,4,5], since it is valid to end at any capture point the list is
    # reformatted to be [1.[1,2],[1,2,3],[1,2,3,4],[1,2,3,4,5]]. This way
    #each possible move can be evaluated and the maximum consecutive cap
    #is always the last list element.
    capture_moves = []
    paika_moves = []
    capture_flag = False
    if pearl==boardgraph.WHITE:
        opponent = boardgraph.BLACK
    else:
        opponent = boardgraph.WHITE
    for v in boardgraph._board.keys():
        if boardgraph._board[v][0] != pearl:
            continue
        for move in boardgraph.open_neighbours(v):
            newgraph = copy.deepcopy(boardgraph)
            newgraph.pearl_update(move,v)
            deltaxy = (move[0]-v[0],move[1]-v[1])
            caplist = []
            traversed = []
            linedict = dict()
            outarr = []
            decorate = dict()
            approachpoint = approach(newgraph,move,deltaxy,opponent)
            withdrawpoint = withdraw(newgraph,move,deltaxy,opponent)
            traversed.append(v)

            if  approachpoint and withdrawpoint: #bi-directional move
                capture_flag = True
                multi = multicapture(newgraph,deltaxy,approachpoint,opponent)
                linedict[(v,move)] = deltaxy
                if multi:
                    capture_moves.append(multi)
                    caplist.append(multi)
                    if len(caplist) < len(consecutivecap(multi,move,caplist,opponent,traversed,linedict,decorate)):
                        outarr = formatlist(caplist,outarr,decorate)
                        capture_moves.append(outarr)

                else:
                    newgraph.add_piece_token(approachpoint,0)
                    capture_moves.append(newgraph)
                    caplist.append(newgraph)
                    if len(caplist) < len(consecutivecap(newgraph,move,caplist,opponent,traversed,linedict,decorate)):
                        outarr = formatlist(caplist,outarr,decorate)
                        capture_moves.append(outarr)


                newgraph = copy.deepcopy(boardgraph)
                newgraph.pearl_update(move,v)

            elif approachpoint and not withdrawpoint: #aproach move
                capture_flag = True
                multi = multicapture(newgraph,deltaxy,approachpoint,opponent,decorate)
                linedict[(v,move)] = deltaxy
                if multi:
                    capture_moves.append(multi)
                    caplist.append(multi)
                    if len(caplist) < len(consecutivecap(multi,move,caplist,opponent,traversed,linedict,decorate)):
                        outarr = formatlist(caplist,outarr,decorate)
                        capture_moves.append(outarr)
                else:
                    newgraph.add_piece_token(approachpoint,0)
                    capture_moves.append(newgraph)
                    caplist.append(newgraph)
                    if len(caplist) < len(consecutivecap(newgraph,move,caplist,opponent,traversed,linedict,decorate)):
                        outarr = formatlist(caplist,outarr,decorate)
                        capture_moves.append(outarr)

                newgraph = copy.deepcopy(boardgraph)
                newgraph.pearl_update(move,v)

            elif withdrawpoint and not approachpoint: #withdraw move
                capture_flag = True
                multi = multicapture(newgraph,deltaxy,withdrawpoint,opponent,True)
                if multi:
                    capture_moves.append(multi)
                    caplist.append(multi)
                    if len(caplist) < len(consecutivecap(multi,move,caplist,opponent,traversed,linedict,decorate)):
                        outarr = formatlist(caplist,outarr,decorate)
                        capture_moves.append(outarr)
                else:
                    newgraph.add_piece_token(withdrawpoint,0)
                    capture_moves.append(newgraph)
                    caplist.append(newgraph)
                    if len(caplist) < len(consecutivecap(newgraph,move,caplist,opponent,traversed,linedict,decorate)):
                        outarr = formatlist(caplist,outarr,decorate)
                        capture_moves.append(outarr)
                newgraph = copy.deepcopy(boardgraph)
                newgraph.pearl_update(move,v)

            else:
                paika_moves.append(newgraph)

    if capture_flag:
        return capture_moves,capture_flag
    else:
        return paika_moves,capture_flag



#The following two functions pertain to user interaction.
def check_move(boardgraph,pearl,old,new):
    move_list,capture_flag = move_generator(boardgraph,pearl)
    for graph in move_list:
        if type(graph)==list:
            continue
        if graph._board[old][0]==0 and graph._board[new][0]==pearl:
            return graph.remake_board_array(5,5),graph,capture_flag
    return False, boardgraph,capture_flag

def check_consecutive_move(boardgraph,new_y,new_x,capture_flag,old_move_locations=[],old_x=None,old_y=None):
        vertex = (new_x,new_y)
        old_vertex = (old_x,old_y)
        for moves in old_move_locations:
            print('old_move_locations',old_move_locations)
            print(new_x,new_y)
            if (new_x,new_y)== moves:
                print('repeat location!!!!!')
                return False, boardgraph,capture_flag
        if capture_flag == True:
            for move in boardgraph.open_neighbours(vertex):
                newgraph = copy.deepcopy(boardgraph)
                deltaxy = (move[0]-vertex[0],move[1]-vertex[1]) # move will be the empty coordinates
                appr = approach(newgraph,move,deltaxy,BoardContent.BLACK,old_move_locations)
                witd = withdraw(newgraph,move,deltaxy,BoardContent.BLACK,old_move_locations)
                if appr or witd:
                    return(True)
            return False

        else:
            return False



def evaluate_moves(move_list,pearl):
    #Assign value for each move (potential boardstate) based on
    #how many User pieces there are and how many AI pieces there are.
    #User win is automatically assigned a value of -25 and AI win
    #is an automatic 25. In other words, the AI is the maximizing
    #player and the User is the minimizing player.
    if pearl==BoardContent.WHITE:
        opponent = BoardContent.BLACK
    else:
        opponent = BoardContent.WHITE

    valdict = dict()
    value = 0
    for i in range(len(move_list)):
        graph=move_list[i]
        if type(graph)==list:
            index = i
            graph = graph[len(graph)-1]
            if type(graph)==list:
                graph = graph[len(graph)-1]
                if type(graph) == list:
                    graph = graph[len(graph)-1]
                    value = 0
                    opcount = 0
                    pcount = 0
                    for v in graph._board.keys():
                        if graph._board[v][0]==pearl:
                            pcount=+1
                        if graph._board[v][0]==opponent:
                            opcount+=1
                    if pcount==0:
                        valdict[graph] = (-25,index)
                    elif opcount==0:
                        valdict[graph] = (25,index)
                    else:
                        value = pcount-opcount
                        valdict[graph] = (value,index)
                value = 0
                opcount=0
                pcount=0
                for v in graph._board.keys():
                    if graph._board[v][0]==pearl:
                        pcount+=1
                    if graph._board[v][0]==opponent:
                        opcount+=1
                if pcount==0:
                    valdict[graph] = (-25,index)
                elif opcount==0:
                    valdict[graph] = (25,index)
                else:
                    value = pcount-opcount
                    valdict[graph] = (value,index)
            value = 0
            opcount = 0
            pcount = 0
            for v in graph._board.keys():
                if graph._board[v][0]==pearl:
                    pcount+=1
                if graph._board[v][0]==opponent:
                    opcount+=1
            if pcount==0:
                valdict[graph] = (-25,index)
            elif opcount==0:
                valdict[graph] = (25,index)
            else:
                value = pcount - opcount
                valdict[graph] = (value,index)
        else:
            value = 0
            opcount = 0
            pcount = 0
            for v in graph._board.keys():
                if graph._board[v][0]==pearl:
                    pcount+=1
                if graph._board[v][0]==opponent:
                    opcount+=1
            if pcount==0:
                valdict[graph] = (-25,None)
            elif opcount==0:
                valdict[graph] = (25,None)
            else:
                value = pcount - opcount
                valdict[graph] = (value,None)

    return valdict




def alphabeta(graph,depth,valdict,alpha,beta,maximizingP=True):
    #Minimax recursive algorithm with alpha beta pruning. Returns
    #a move that is the best choice.
    if (depth==0 or graph in valdict.keys() and valdict[graph][0]==25
            or graph in valdict.keys() and valdict[graph][0]==-25):
        return valdict[graph][0],graph
    if maximizingP:
        pearl = BoardContent.BLACK
    else:
        pearl = BoardContent.WHITE
    move_list,capture_flag = move_generator(graph,pearl)
    valdict = evaluate_moves(move_list,pearl)
    if maximizingP:
        bestValue = -25
        newgraph = graph
        for graph in valdict.keys():
            value,move = alphabeta(graph,depth-1,valdict,alpha,beta,False)
            if value >= bestValue:
                newgraph = graph
            alpha = max(alpha,value)
            if beta <= alpha:
                break
        return bestValue,newgraph
    else:
        bestValue = 25
        newgraph = graph
        for graph in valdict.keys():
            value,move = alphabeta(graph,depth-1,valdict,alpha,beta,True)
            if value <= bestValue:
                newgraph = graph
            beta = min(beta,value)
            if beta <= alpha:
                break
        return bestValue,newgraph
