from tkinter import *
from tkinter.scrolledtext import *

import sqlite3

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
        self.selected = (-1,-1)
        self.forwarding = False
        self.forwardCell = (-1,-1)
        self.winner = None
    def takeTurn(self):
        if (self.turn == 1):
            self.turn = 2
        else:
            self.turn = 1

        self.checkWin()


    def makeMove(self,x,y,newx, newy,app):
        player = self.turn

        moves = []
        totaljumps = []

        if (not self.forwarding):
            moves += self.listMoves(player,x,y)
            
            for i in range(8):
                for j in range(8): 
                    totaljumps += self.listJumps(player,i,j)

        else:
            totaljumps += self.listJumps(player,self.forwardCell[0],self.forwardCell[1])
        print("Possible jumps:",totaljumps)
        print("Attempting move:",(x,y,newx,newy))
        piece = self.cb[x][y]

        cell = None
        jumpOccured = False
        if (len(totaljumps) == 0):
            if (x,y,newx, newy) in moves:
                self.cb[x][y] = 0
                self.cb[newx][newy] = piece
                res = self.promoteToKing(newx, newy)
                if (res):
                    app.logMessage("Cell ("+str(i)+','+str(j)+") promoted to king!")
                cell = (newx, newy)
            else:
                app.logMessage("GAME VIOLATION: Invalid move!")
        else:
            if (x,y,newx, newy) in totaljumps:
                self.cb[x][y] = 0
                self.cb[newx][newy] = piece
                self.cb[x + (newx-x)//2][y + (newy-y)//2] = 0
                res = self.promoteToKing(newx, newy)
                if (res):
                    app.logMessage("Cell ("+str(i)+','+str(j)+") promoted to king!")
                cell = (newx, newy)
            else:
                app.logMessage("GAME VIOLATION: Must take jump!")
        
        if (cell and len(self.listJumps(player,cell[0],self.cell[1])) > 0):
            self.forwardCell = cell
            app.logMessage("Entering forwarding state!")
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
                    moves.append((x,y,x-1,y-1))
                if (y+1 < 8 and self.cb[x-1][y+1] == 0):
                    moves.append((x,y,x-1,y+1))
            if (x + 1 < 8):
                if (y-1 >= 0 and self.cb[x+1][y-1] == 0):
                    moves.append((x,y,x+1,y-1))
                if (y+1 < 8 and self.cb[x+1][y+1] == 0):
                    moves.append((x,y,x+1,y+1))  
        if (piece == 2):
            if (x - 1 >= 0 ):
                if (y-1 >= 0 and self.cb[x-1][y-1] == 0 ):
                    moves.append((x,y,x-1,y-1))
                if (y+1 < 8 and self.cb[x-1][y+1] == 0):
                    moves.append((x,y,x-1,y+1))
        if (piece == 1):
            if (x + 1 < 8):
                if (y-1 >= 0 and self.cb[x+1][y-1] == 0):
                    moves.append((x,y,x+1,y-1))
                if (y+1 < 8 and self.cb[x+1][y+1] == 0):
                    moves.append((x,y,x+1,y+1))       
        return moves
    def listJumps(self,player,x,y):
        jumps = []
        piece = self.cb[x][y]

        if (piece not in (player,player+2)):
            return jumps

        if (piece == 3 or piece == 4):
            if (x-1 >= 0):
                if (y-2 >= 0 and ( (piece == 3 and self.cb[x-1][y-1] in (2,4)) or (piece == 4 and self.cb[x-1][y-1] in (1,3)) ) and self.cb[x-2][y-2] == 0 ):
                    jumps.append((x,y,x-2,y-2))
                if (y+2 < 8 and ( (piece == 3 and self.cb[x-1][y+1] in (2,4)) or (piece == 4 and self.cb[x-1][y+1] in (1,3)) ) and self.cb[x-2][y+2] == 0):
                    jumps.append((x,y,x-2,y+2))
            if (x+1 < 8):
                if (y-2 >= 0 and ( (piece == 3 and self.cb[x+1][y-1] in (2,4)) or (piece == 4 and self.cb[x+1][y-1] in (1,3))) and self.cb[x+2][y-2] == 0):
                    jumps.append((x,y,x+2,y-2))
                if (y+2 < 8 and ( (piece == 3 and self.cb[x+1][y+1] in (2,4)) or (piece == 4 and self.cb[x+1][y+1] in (1,3)) ) and self.cb[x+2][y+2] == 0):
                    jumps.append((x,y,x+2,y+2))
        if (piece == 2):
            if (x - 2 >= 0):
                if (y-2 >= 0 and self.cb[x-1][y-1] in (1,3) and self.cb[x-2][y-2] == 0 ):
                    jumps.append((x,y,x-2,y-2))
                if (y+2 < 8 and self.cb[x-1][y+1] in (1,3) and self.cb[x-2][y+2] == 0):
                    jumps.append((x,y,x-2,y+2))
        if (piece == 1):
            if (x + 2 < 8):
                if (y-2 >= 0 and self.cb[x+1][y-1] in (2,4) and self.cb[x+2][y-2] == 0):
                    jumps.append((x,y,x+2,y-2))
                if (y+2 < 8 and self.cb[x+1][y+1] in (2,4) and self.cb[x+2][y+2] == 0):
                    jumps.append((x,y,x+2,y+2))

        return jumps

    def promoteToKing(self,newx, newy):

        if (newx == 0 and self.cb[newx][newy] == 2):
            self.cb[newx][newy] = 4
            return True
        elif (newx == 7 and self.cb[newx][newy] == 1):
            self.cb[newx][newy] = 3
            return True
        return False
    def countPieces(self):
        scores = {'red':0,'black':0}
        for i in range(8):
            for j in range(8):
                if (self.cb[i][j] in (2,4)):
                    scores['red'] += 1
                elif (self.cb[i][j] in (1,3)):
                    scores['black'] += 1
        return scores
    def checkWin(self):
        d = self.countPieces()

        if (d['red'] == 0):
            self.winner = "Black"
        if (d['black'] == 0):
            self.winner = "Red"

        totalMoves = []
        for i in range(8):
            for j in range(8):
                totalMoves += self.listMoves(self.turn,i,j)
                totalMoves += self.listJumps(self.turn,i,j)

        if (len(totalMoves) == 0):
            print("No more legal moves left!")
            if (self.turn == 1):
                self.winner = "Red"
            else:
                self.black = "Black"

        return None
class CheckerApp:
    def __init__(self):

        self.checkers = Checkers()
        self.selectCell = (-1,-1)        
        self.db = sqlite3.connect("sessionLog.db")
        try:
            self.db.execute("create table if not exists sessions(id integer primary key autoincrement, start_time datetime default current_timestamp, end_time datetime, winner varchar(5), reason varchar(10))")
            cur = self.db.execute("insert into sessions(end_time,winner,reason) values(?,?,?)",(None,None,None))
        except:
            print("[WARN] Error in initialized database!")

        self.currentrowid = cur.lastrowid

        print("Inserting new row ID:",self.currentrowid)
        win = Tk()
        win.geometry("500x500")
        self.buttons = []
        self.buttonFrame = Frame(win)

        self.label = Label(win,text="Turn: {}".format(2))
        self.scoreLabel = Label(win,text="")
        self.text_area = ScrolledText(win,
                            width = 50, 
                            height = 6, 
                            font = ("Times New Roman",
                                    10))
        
        fillFunc = (lambda: 'black' if (toggle == 0) else  'red')
        
        superToggle = 0
        for i in range(8):
            toggle = superToggle
            for j in range(8):
                self.addButton(' ', lambda:self.addNumber(0),i,j)
                if (toggle == 0):
                    self.buttons[i*8 + j]['bg'] = 'red'
                else:
                    self.buttons[i*8+j]['bg'] = 'black'
                toggle ^= 1
            superToggle ^= 1
        self.buttonFrame.pack()
        self.label.pack()
        self.scoreLabel.pack()
        self.text_area.pack()
        self.refreshBoard()
        win.mainloop()

    def addButton(self,text, cmd,i,j):
        b = Button(self.buttonFrame,text =text,command = lambda:self.selectCells(i,j),width=4,height=2)
        b.grid(row=i, column = j)
        self.buttons.append(b)       

    def logMessage(self,message):
        self.text_area.insert(END, message + '\n')
        self.text_area.see("end")

    def selectCells(self,i,j):
        if (self.selectCell == (-1,-1)):
            self.logMessage("Cell selected:"+'('+str(i)+','+str(j)+')')
            self.selectCell = (i,j)
        else:
            res = self.checkers.makeMove(self.selectCell[0],self.selectCell[1],i,j,self)


            if (res is None):
                self.selectCell = (-1,-1)
                self.logMessage("Move failed!")
                return
            else:
                
                self.selectCell = (-1,-1)
                self.logMessage("Move success, switching turns")
                
            
            self.refreshBoard()
            self.refreshPieceCount()

    def refreshBoard(self):
        for i in range(8):
            for j in range(8):
                piece = self.checkers.cb[i][j]
                if piece == 2:
                    self.buttons[i*8+j]['fg'] = 'red'
                    self.buttons[i*8+j]['text'] = 'O'
                elif piece == 1:
                    self.buttons[i*8+j]['fg'] = 'white'
                    self.buttons[i*8+j]['text'] = 'O'
                elif piece == 4:
                    self.buttons[i*8+j]['fg'] = 'red'
                    self.buttons[i*8+j]['text'] = 'Q'
                elif piece == 3:
                    self.buttons[i*8+j]['fg'] = 'white'
                    self.buttons[i*8+j]['text'] = 'Q'               
                else:
                    self.buttons[i*8+j]['text'] = ' '
        if self.checkers.winner is not None:
            self.label['text'] = "Winner: " + self.checkers.winner
            self.logMessage("Winner: "+self.checkers.winner)
        else:
            self.label['text'] = "Turn: {}".format(self.checkers.turn)
    def refreshPieceCount(self):
        pieceCount = self.checkers.countPieces()
        self.scoreLabel['text'] = "Red: {}, Black: {}".format(pieceCount['red'],pieceCount['black'])



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
        print("Ending checkers session")

        
c = CheckerApp()
