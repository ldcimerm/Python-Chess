
import piece
import player

class Board:
    ''' this class will hold the actual game Board which is implemented
    as a list of list of piece objects
    '''
    
    def __init__(self,Player1,Player2): #the constructor
        self.gameBoard = [[],[],[],[],[],[],[],[]]
        for p in Player1.myPieces: #initializing player1's pieces on the board
            if p.row == 0:
                self.gameBoard[0].append(p)
            else:
                self.gameBoard[1].append(p)
        
        for row in range(2,6): #intializing all of the empty squares
            for col in range(0,8):
                self.gameBoard[row].append(piece.EmptySquare("---",row,col,True))

        for p in Player2.myPieces:
            if p.row == 6:
                self.gameBoard[6].append(p)
            else:
                self.gameBoard[7].append(p)

        self.p1Turn = True


    def draw(self): #this method will print the board to the screen by calling each piece object's draw method
        print("  0   1   2   3   4   5   6   7")
        rowCounter = 0
        for row in self.gameBoard:
            print("---------------------------------")
            print("|",end="")
            for square in row:
                square.draw()
                print("|",end="")
            print("   {}".format(rowCounter))
            rowCounter += 1
        print("---------------------------------")

    


