from tkinter import *
from tkinter.scrolledtext import *

import sqlite3
from utils import *
import copy
import time
import math
import random
DEPTH = 6
class Checkers:
    def __init__(self):
        self.cb = \
        [
        [0,1,0,1,0,1,0,1],
        [1,0,1,0,1,0,1,0],
        [0,1,0,1,0,1,0,1],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [2,0,2,0,2,0,2,0],
        [0,2,0,2,0,2,0,2],
        [2,0,2,0,2,0,2,0],
        ]

        self.turn = 2
        self.forwarding = False
        self.forwardCell = (-1,-1)
        self.winner = None
    def takeTurn(self):
        if (self.turn == 1):
            self.turn = 2
        else:
            self.turn = 1

        self.checkWin()

    def getAllMoves(self):
        totalMoves = []
        player = self.turn
        i = 0
        while (i < 8):
            j = 0
            while (j < 8): 
                totalMoves += self.listMoves(player, i, j)
                j += 1
            i += 1
        return totalMoves
    def getAllJumps(self):
        totalMoves = []
        player = self.turn
        i = 0
        while (i < 8):
            j = 0
            while (j < 8): 
                totalMoves += self.listJumps(player, i, j)
                j += 1
            i += 1
        return totalMoves

    def makeMove(self,x,y,newx, newy,app):
        player = self.turn

        moves = []
        totaljumps = []

        # If forwarding, enumerate only viable jumps of a specific cell else enumerate all possible jumps and moves
        if (not self.forwarding):
            moves += self.listMoves(player,x,y)
            
            i = 0
            while (i < 8):
                j = 0
                while (j < 8): 
                    totaljumps += self.listJumps(player,i,j)
                    j += 1
                i += 1

        else:
            totaljumps += self.listJumps(player,self.forwardCell[0],self.forwardCell[1])
        print("Possible jumps:",totaljumps)
        print("Attempting move:",(x,y,newx,newy))
        piece = self.cb[x][y]

        cell = None
        jumpOccured = False

        # Check if jump is present, if so must take this over all else
        if (length(totaljumps) == 0):
            if (x,y,newx, newy) in moves:
                self.cb[x][y] = 0
                self.cb[newx][newy] = piece
                res = self.promoteToKing(newx, newy)
                if (res):
                    app.logMessage("("+NumberToName(self.turn)+")"+":"+"Cell ("+str(newx)+','+str(newy)+") promoted to king!")
                cell = (newx, newy)
            else:
                app.logMessage("("+NumberToName(self.turn)+")"+":"+"GAME VIOLATION: Invalid move!")
                return None
        else:
            if (x,y,newx, newy) in totaljumps:
                self.cb[x][y] = 0
                self.cb[newx][newy] = piece
                self.cb[x + (newx-x)//2][y + (newy-y)//2] = 0
                app.logMessage("("+NumberToName(self.turn)+")"+":"+"Cell ("+str(x + (newx-x)//2)+','+str(y + (newy-y)//2)+") captured!")
                res = self.promoteToKing(newx, newy)
                if (res):
                    app.logMessage("("+NumberToName(self.turn)+")"+":"+"Cell ("+str(newx)+','+str(newy)+") promoted to king!")
                cell = (newx, newy)
                jumpOccured = True

            else:
                app.logMessage("("+NumberToName(self.turn)+")"+":"+"GAME VIOLATION: Must take jump!")
                return None
        # If we just did a jump and we can do another jump with the same piece, we will enable forwarding for this piece only
        if (cell and jumpOccured and length(self.listJumps(player,cell[0],cell[1])) > 0):
            self.forwardCell = cell
            app.logMessage("("+NumberToName(self.turn)+")"+":"+"Entering forwarding state!")
        elif cell:
            app.logMessage("("+NumberToName(self.turn)+")"+":" + str((x,y)) + "->" + str((newx,newy)))
            self.forwarding = False
            self.forwardCell = (-1,-1)
            
            self.takeTurn()
            app.logMessage("It is now "+NumberToName(self.turn)+"'s turn!")
        return cell

    def makeMoveSilent(self,x,y,newx, newy):
        player = self.turn

        moves = []
        totaljumps = []

        # If forwarding, enumerate only viable jumps of a specific cell else enumerate all possible jumps and moves
        if (not self.forwarding):
            moves += self.listMoves(player,x,y)
            
            i = 0
            while (i < 8):
                j = 0
                while (j < 8): 
                    totaljumps += self.listJumps(player,i,j)
                    j += 1
                i += 1

        else:
            totaljumps += self.listJumps(player,self.forwardCell[0],self.forwardCell[1])
        print("Possible jumps:",totaljumps)
        print("Attempting move:",(x,y,newx,newy))
        piece = self.cb[x][y]

        cell = None
        jumpOccured = False

        # Check if jump is present, if so must take this over all else
        if (length(totaljumps) == 0):
            if (x,y,newx, newy) in moves:
                self.cb[x][y] = 0
                self.cb[newx][newy] = piece
                res = self.promoteToKing(newx, newy)

                cell = (newx, newy)
            else:
                return None
        else:
            if (x,y,newx, newy) in totaljumps:
                self.cb[x][y] = 0
                self.cb[newx][newy] = piece
                self.cb[x + (newx-x)//2][y + (newy-y)//2] = 0
                res = self.promoteToKing(newx, newy)

                cell = (newx, newy)
                jumpOccured = True

            else:
                return None
        # If we just did a jump and we can do another jump with the same piece, we will enable forwarding for this piece only
        if (cell and jumpOccured and length(self.listJumps(player,cell[0],cell[1])) > 0):
            self.forwardCell = cell
        elif cell:
            self.forwarding = False
            self.forwardCell = (-1,-1)
            
            self.takeTurn()
        return cell
    def listMoves(self,player,x,y):
        moves = []
        piece = self.cb[x][y]
        if (piece not in (player,player+2)):
            return moves
        if (piece == 3 or piece == 4):
            if (x-1 >= 0):
                if (y-1 >= 0 and self.cb[x-1][y-1] == 0 ):
                    moves += [((x,y,x-1,y-1))]
                if (y+1 < 8 and self.cb[x-1][y+1] == 0):
                    moves += [(x,y,x-1,y+1)]
            if (x + 1 < 8):
                if (y-1 >= 0 and self.cb[x+1][y-1] == 0):
                    moves += [(x,y,x+1,y-1)]
                if (y+1 < 8 and self.cb[x+1][y+1] == 0):
                    moves += [(x,y,x+1,y+1)]  
        if (piece == 2):
            if (x - 1 >= 0 ):
                if (y-1 >= 0 and self.cb[x-1][y-1] == 0 ):
                    moves += [(x,y,x-1,y-1)]
                if (y+1 < 8 and self.cb[x-1][y+1] == 0):
                    moves += [(x,y,x-1,y+1)]
        if (piece == 1):
            if (x + 1 < 8):
                if (y-1 >= 0 and self.cb[x+1][y-1] == 0):
                    moves += [(x,y,x+1,y-1)]
                if (y+1 < 8 and self.cb[x+1][y+1] == 0):
                    moves += [(x,y,x+1,y+1)]       
        return moves
    def listJumps(self,player,x,y):
        jumps = []
        piece = self.cb[x][y]

        if (piece not in (player,player+2)):
            return jumps

        if (piece == 3 or piece == 4):
            if (x-2 >= 0):
                if (y-2 >= 0 and ( (piece == 3 and self.cb[x-1][y-1] in (2,4)) or (piece == 4 and self.cb[x-1][y-1] in (1,3)) ) and self.cb[x-2][y-2] == 0 ):
                    jumps += [(x,y,x-2,y-2)]
                if (y+2 < 8 and ( (piece == 3 and self.cb[x-1][y+1] in (2,4)) or (piece == 4 and self.cb[x-1][y+1] in (1,3)) ) and self.cb[x-2][y+2] == 0):
                    jumps += [(x,y,x-2,y+2)]
            if (x+2 < 8):
                if (y-2 >= 0 and ( (piece == 3 and self.cb[x+1][y-1] in (2,4)) or (piece == 4 and self.cb[x+1][y-1] in (1,3))) and self.cb[x+2][y-2] == 0):
                    jumps += [(x,y,x+2,y-2)]
                if (y+2 < 8 and ( (piece == 3 and self.cb[x+1][y+1] in (2,4)) or (piece == 4 and self.cb[x+1][y+1] in (1,3)) ) and self.cb[x+2][y+2] == 0):
                    jumps += [(x,y,x+2,y+2)]
        if (piece == 2):
            if (x - 2 >= 0):
                if (y-2 >= 0 and self.cb[x-1][y-1] in (1,3) and self.cb[x-2][y-2] == 0 ):
                    jumps += [(x,y,x-2,y-2)]
                if (y+2 < 8 and self.cb[x-1][y+1] in (1,3) and self.cb[x-2][y+2] == 0):
                    jumps += [(x,y,x-2,y+2)]
        if (piece == 1):
            if (x + 2 < 8):
                if (y-2 >= 0 and self.cb[x+1][y-1] in (2,4) and self.cb[x+2][y-2] == 0):
                    jumps += [(x,y,x+2,y-2)]
                if (y+2 < 8 and self.cb[x+1][y+1] in (2,4) and self.cb[x+2][y+2] == 0):
                    jumps += [(x,y,x+2,y+2)]

        return jumps

    def promoteToKing(self,newx, newy):
        # If far end reached, convert to king
        if (newx == 0 and self.cb[newx][newy] == 2):
            self.cb[newx][newy] = 4
            return True
        elif (newx == 7 and self.cb[newx][newy] == 1):
            self.cb[newx][newy] = 3
            return True
        return False
    def countPieces(self):
        scores = {'red':0,'black':0}
        i = 0
        while i < 8:
            j = 0
            while j < 8:
                if (self.cb[i][j] in (2,4)):
                    scores['red'] += 1
                elif (self.cb[i][j] in (1,3)):
                    scores['black'] += 1
                j += 1
            i += 1
        return scores
    def checkWin(self):
        # If no piece left or legal moves exhausted, announce winner
        d = self.countPieces()

        if (d['red'] == 0):
            self.winner = "Black"
        if (d['black'] == 0):
            self.winner = "Red"

        totalMoves = []
        i = 0
        while i < 8:
            j = 0
            while j < 8:
                totalMoves += self.listMoves(self.turn,i,j)
                totalMoves += self.listJumps(self.turn,i,j)
                j += 1
            i += 1
        if (length(totalMoves) == 0):
            print("No more legal moves left!")
            if (self.turn == 1):
                self.winner = "Red"
            else:
                self.black = "Black"

        return None


def calculate_heuristics(instance):
        board = instance.cb
        black = 1
        red = 2
        kingblack = 3
        kingred = 4

        h1 = 0
        h2 = 0
        hrand = random.randint(0,99) # Randomization component
        for i in range(8):
            for j in range(8):
                if (board[i][j] == black):
                    h1 -= 3
                    h2 -= (i-0)
                elif (board[i][j] == kingblack):
                    h1 -= 5
                elif (board[i][j] == red):
                    h1 += 3
                    h2 += (7-i)
                elif (board[i][j] == kingred):
                    h1 += 5
        score = h1*10000+h2*100+hrand
        print("Heuristic:",score)
        return score
        


def doAlphaBetaSearch(instance, levels, alpha, beta):
    #if (instance.winner == "Black"):
    #    return (-99999999+cur_depth)
    #if (instance.winner == "Red"):
    #    return (99999999-cur_depth)
    
    if (levels == 0 or instance.winner != None):
        return calculate_heuristics(instance)
    moves = instance.getAllMoves()
    jumps = instance.getAllJumps()
    best_move = None
    old_counts = instance.countPieces()
    best_score = 0
    if (instance.turn == 1):
        best_score = math.inf
    else:
        best_score = -math.inf
    if len(jumps) != 0:
        for jump in jumps:
            new_instance = copy.deepcopy(instance)
            new_instance.makeMoveSilent(jump[0],jump[1],jump[2],jump[3])
            # Black's turn
            if (instance.turn == 1):
                score = doAlphaBetaSearch(new_instance, levels-1,alpha,beta)

                best_score = min(score, best_score)
                beta = min(beta, best_score)
                if (beta <= alpha):
                    print("pruning")
                    break
            else:
            # Red's turn
                score = doAlphaBetaSearch(new_instance, levels-1,alpha,beta)
                best_score = max(score, best_score)
                alpha = max(alpha, best_score)
                if (beta <= alpha):
                    print("pruning")
                    break
    else:
        for move in moves:
            new_instance = copy.deepcopy(instance)
            new_instance.makeMoveSilent(move[0],move[1],move[2],move[3])
            if (instance.turn == 1):
                score = doAlphaBetaSearch(new_instance, levels-1,alpha,beta)

                best_score = min(score, best_score)
                beta = min(beta, best_score)
                if (beta <= alpha):
                    print("pruning")
                    break
            else:
                score = doAlphaBetaSearch(new_instance, levels-1,alpha,beta)
                best_score = max(score, best_score)
                alpha = max(alpha, best_score)
                if (beta <= alpha):
                    print("pruning")
                    break
    return best_score

def getBestMoveBlack(instance, levels):
    #if (instance.winner == "Black"):
    #    return (-99999999+cur_depth)
    #if (instance.winner == "Red"):
    #    return (99999999-cur_depth)
    
    if (levels == 0):
        return calculate_heuristics(instance)
    moves = instance.getAllMoves()
    jumps = instance.getAllJumps()

    best_score = math.inf
    best_move = None
    if len(jumps) != 0:
        for move in jumps:
            new_instance = copy.deepcopy(instance)
            new_instance.makeMoveSilent(move[0],move[1],move[2],move[3])
            score = min(best_score,doAlphaBetaSearch(new_instance,levels-1,-math.inf,math.inf))
            if (score < best_score):
                best_move = move
                best_score = score
    else:
        for move in moves:
            new_instance = copy.deepcopy(instance)
            new_instance.makeMoveSilent(move[0],move[1],move[2],move[3])
            score = min(best_score, doAlphaBetaSearch(new_instance,levels-1,-math.inf,math.inf))
            if (score < best_score):
                best_move = move
                best_score = score
    return (best_move, best_score)
class CheckerApp:
    def __init__(self):

        self.checkers = Checkers()
        self.trail = [[0 for _ in range(8)] for _ in range(8)]
        self.selectCell = (-1,-1)        
        self.db = sqlite3.connect("sessionLog.db")
        try:
            self.db.execute("create table if not exists sessions(id integer primary key autoincrement, \
             start_time datetime default current_timestamp, end_time datetime, winner varchar(5), reason varchar(10))")
            cur = self.db.execute("insert into sessions(end_time,winner,reason) values(?,?,?)",(None,None,None))
        except:
            print("[WARN] Error in initialized database!")
            return

        self.currentrowid = cur.lastrowid

        print("Inserting new row ID:",self.currentrowid)
        self.win = Tk()
        self.win.title("Checkers - AP Project")
        self.win.geometry("500x600")
        self.buttons = []
        self.buttonFrame = Frame(self.win)

        self.label = Label(self.win,text="Turn: Red")
        self.scoreLabel = Label(self.win,text="")
        self.text_area = ScrolledText(self.win,
                            width = 75, 
                            height = 6, 
                            font = ("Times New Roman",
                                    10))
        self.historyButton = Button(self.win, text="Dump DB History",command=self.dumpLog)        
        fillFunc = (lambda: 'black' if (toggle == 0) else  'red')
        
        superToggle = 0
        i = 0
        while i < 8:
            j = 0
            toggle = superToggle
            while j < 8:
                self.addButton(' ', lambda:self.addNumber(0),i,j)
                if (toggle == 0):
                    self.buttons[i*8 + j]['bg'] = 'red'
                else:
                    self.buttons[i*8+j]['bg'] = 'black'
                toggle ^= 1
                j += 1
            i += 1
            superToggle ^= 1
        
        self.buttonFrame.pack()
        self.label.pack()
        self.scoreLabel.pack()
        self.text_area.pack()
        self.historyButton.pack()
        self.refreshBoard()
        self.refreshPieceCount()
        self.win.mainloop()

    def addButton(self,text, cmd,i,j):
        b = Button(self.buttonFrame,text =text,command = lambda:self.selectCells(i,j),width=4,height=2,font = 'Helvetica 10')
        b.grid(row=i, column = j)
        self.buttons += [b]       

    def logMessage(self,message):
        self.text_area.insert(END, message + '\n')
        self.text_area.see("end")

    def selectCells(self,i,j):
        if (self.checkers.turn != 2):
            return
        if (self.selectCell == (-1,-1)):
            self.logMessage("Cell selected:"+'('+str(i)+','+str(j)+')')
            self.selectCell = (i,j)
            self.buttons[i*8+j]['font'] = 'Helvetica 10 underline'
        else:
            res = self.checkers.makeMove(self.selectCell[0],self.selectCell[1],i,j,self)
            if (self.checkers.turn == 1 and self.checkers.winner is None):
                self.win.after(2000,lambda: self.AIMove())
            if (res is None):
                self.buttons[self.selectCell[0]*8+self.selectCell[1]]['font'] = 'Helvetica 10'
                self.selectCell = (-1,-1)
                return
            else:
                self.buttons[self.selectCell[0]*8+self.selectCell[1]]['font'] = 'Helvetica 10'
                self.selectCell = (-1,-1)
            self.refreshBoard()
            self.refreshPieceCount()


    def AIMove(self):
        self.trail = [[0 for _ in range(8)] for _ in range(8)]
        while (self.checkers.turn == 1 and self.checkers.winner is None):
            (best_move, best_score) = getBestMoveBlack(self.checkers, DEPTH)
            self.logMessage("Computer making move:"+str(best_move)+"with score"+str(best_score))
            self.checkers.makeMove(best_move[0],best_move[1],best_move[2],best_move[3],self)
            self.trail[best_move[0]][best_move[1]] = 1
            self.trail[best_move[2]][best_move[3]] = 2

        self.refreshBoard()
        self.refreshPieceCount()
    def refreshBoard(self):
        for i in range(8):
            for j in range(8):
                piece = self.checkers.cb[i][j]
                prefix = ''
                if (self.trail[i][j] == 2):
                    prefix = '-'
                if piece == 2:
                    self.buttons[i*8+j]['fg'] = 'red'
                    self.buttons[i*8+j]['text'] = 'O'
                elif piece == 1:
                    self.buttons[i*8+j]['fg'] = 'black'
                    self.buttons[i*8+j]['text'] = prefix+'O'+prefix
                elif piece == 4:
                    self.buttons[i*8+j]['fg'] = 'red'
                    self.buttons[i*8+j]['text'] = 'Q'
                elif piece == 3:
                    self.buttons[i*8+j]['fg'] = 'black'
                    self.buttons[i*8+j]['text'] = prefix+'Q'+prefix
                elif self.trail[i][j] == 1:
                    self.buttons[i*8+j]['fg'] = 'brown'
                    self.buttons[i*8+j]['text'] = 'o'              
                else:
                    self.buttons[i*8+j]['text'] = ' '
        if self.checkers.winner is not None:
            self.label['text'] = "Winner: " + self.checkers.winner
            self.logMessage("Winner: "+self.checkers.winner)
        else:
            if (self.checkers.turn == 1):
                self.label['text'] = "Turn: Black"
            elif (self.checkers.turn == 2):
                self.label['text'] = "Turn: Red"
    def refreshPieceCount(self):
        pieceCount = self.checkers.countPieces()
        self.scoreLabel['text'] = "Red:" + str(pieceCount['red']) + "       " + "Black: " + str(pieceCount['black'])



    def __del__(self):
        self.db.execute("update  sessions set end_time = current_timestamp where id=?",(self.currentrowid,))
        if (self.checkers.winner):
            print("Game ended! Saving to DB")
            self.db.execute("update  sessions set winner = ? where id=?",(self.checkers.winner,self.currentrowid))
            self.db.execute("update  sessions set reason = ? where id=?",("FINISH",self.currentrowid))
        else:
            print("Game forfeit! Saving to DB")
            self.db.execute("update  sessions set reason = ? where id=?",("FORFEIT",self.currentrowid))

        self.db.commit()
        print("Current DB history:")
        cursor = self.db.execute("select * from sessions")
        for row in cursor:
            print(row)
        print("Ending checkers session")

        
    def dumpLog(self):
        cursor = self.db.execute("select * from sessions")
        self.logMessage("History: ")
        for row in cursor:
            self.logMessage(str(row))
c = CheckerApp()
