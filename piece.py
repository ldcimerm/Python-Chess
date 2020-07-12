import board
import player

class Piece:
    '''this is the abstract base class for all types of pieces: Pawns, Knights, Queens etc...
    '''
    def __init__(self,name,row,col,isDead):
        self.name = name
        self.row = row
        self.col = col
        self.isDead = isDead


    def validMove(self,theBoard): #will return a 3-element list where first element is the updated game board. Also performs the actual move
        pass                      # second element is the piece that was in the square the piece moved onto
                                  # third element is the moving piece or the promoted piece(pawns only)


    def checkingKing(self,theBoard,Player1,Player2):
        pass


    def draw(self):
        print(self.name,end = "")


    def listofValidMoves(self,theBoard):
        pass


    def horizontalPath(self,theBoard,row,col): #returns whether there is a clear horizontal path from this piece to the piece at (row,col)
        if(row != self.row):
            return False
        if col > self.col: #the player wishes to move onto a square that is to the right of its current pos
            colCounter = self.col+1
            while colCounter != col:
                if theBoard.gameBoard[row][colCounter].name != "---":
                    return False
                else:
                    colCounter += 1
            return True
        else:
            colCounter = self.col - 1
            while colCounter != col:
                if theBoard.gameBoard[row][colCounter].name != "---":
                    return False
                else:
                    colCounter -= 1
            return True


    def verticalPath(self,theBoard,row,col): #returns whether there is a clear horizontal path from this piece to the piece at (row,col)
         if(col != self.col):
             return False
         if row > self.row: #the player wishes to move onto a square that is to the right of its current pos
             rowCounter = self.row+1
             while rowCounter != row:
                 if theBoard.gameBoard[rowCounter][col].name != "---":
                     return False
                 else:
                     rowCounter += 1
             return True
         else:
            rowCounter = self.row - 1
            while rowCounter != row:
                if theBoard.gameBoard[rowCounter][col].name != "---":
                     return False
                else:
                     rowCounter -= 1
            return True




    def diagonalPath(self,theBoard,row,col):
        if(abs(self.row-row) != abs(self.col-col)): #if this isn't true the coordinates are not diagonally aligned
            return False
        if(col > self.col): #the desired square is to the right of the moving piece
            if(row > self.row): #the desired square is SE of the moving piece
                rowCounter = self.row+1
                colCounter = self.col+1
                while rowCounter != row and colCounter != col:
                    if(theBoard.gameBoard[rowCounter][colCounter].name != "---"):
                        return False
                    else:
                        rowCounter += 1
                        colCounter += 1
                return True
            else: #the desired square is NE of the moving piece
                rowCounter = self.row-1
                colCounter = self.col+1
                while rowCounter != row and colCounter != col:
                    if(theBoard.gameBoard[rowCounter][colCounter].name != "---"):
                        return False
                    else:
                        rowCounter -= 1
                        colCounter += 1
                return True
        else:
            if(row > self.row): #the desired square is SW
                rowCounter = self.row+1
                colCounter = self.col-1
                while rowCounter != row and colCounter != col:
                    if(theBoard.gameBoard[rowCounter][colCounter].name != "---"):
                        return False
                    else:
                        rowCounter += 1
                        colCounter -= 1
                return True
            else: #the desired square is NW of the moving piece
                rowCounter = self.row-1
                colCounter = self.col-1
                while rowCounter != row and colCounter != col:
                    if(theBoard.gameBoard[rowCounter][colCounter].name != "---"):
                        return False
                    else:
                        rowCounter -= 1
                        colCounter -= 1
                return True
                

        
                






#------------------------------EmptySquare------------------------------------------------------------------------------------------
class EmptySquare(Piece):

    def validMove(self,theBoard): #does nothing
        x = 5




#-------------------------------BishopSubclass-------------------------------------------------------------------------------------
class Bishop(Piece):

    def validMove(self,theBoard):
        theCoords = input("Please enter the coordinates of the square you wish to move onto using the form row,col")
        row = -1
        col = -1
        #we first get the coordinates of the place on the board that the player wishes to move to
        if len(theCoords) ==3 and theCoords[0].isdigit() and theCoords[1] == "," and theCoords[2].isdigit():
            row = int(theCoords[0])
            col = int(theCoords[2])
        else:
            raise(AssertionError) 

        assert(row >= 0 and row <= 7 and col >=0 and col <= 7) #making sure the coordinates are squares on the board
        assert(not (row == self.row and col == self.col)) #making sure the square is not the current square
        assert(theBoard.gameBoard[row][col].name[0] != self.name[0]) #making sure the desired square is either holding an opponent's piece or is empty
        assert(theBoard.gameBoard[row][col].name[2] != "G") #making sure the desired square does not hold a king
        
        currSpace = self.row * 8 + self.col
        desiredSpace = row * 8 + col #checking the square entered is diagonal from current square
        if(not (currSpace % 9 == desiredSpace % 9) and not (currSpace % 7 == desiredSpace % 7)): 
            raise(AssertionError)

        if(not self.diagonalPath(theBoard,row,col)):
            raise(AssertionError)

        #by this point we know we can perform the move
        newBoard = theBoard
        oldPiece = newBoard.gameBoard[row][col] #the piece that will be getting deleted
        newBoard.gameBoard[self.row][self.col] = EmptySquare("---",self.row,self.col,True) #set the square of the current piece to be empty
        self.row = row #updating the row of moving piece
        self.col = col #updating the col of moving piece
        newBoard.gameBoard[oldPiece.row][oldPiece.col] = self #setting the board to be the moved
        return [newBoard,oldPiece,self]
        



    def checkingKing(self,theBoard,otherPlayer): #tells whether or not this piece is checking the opponent's king
        if(self.isDead):
            return False
        if(theBoard.p1Turn):
            p2KingCoords = otherPlayer.getKingCoords()
            if(self.diagonalPath(theBoard,p2KingCoords[0],p2KingCoords[1])):
                return True
            else:
                return False
        else:
            p1KingCoords = otherPlayer.getKingCoords()
            if(self.diagonalPath(theBoard,p1KingCoords[0],p1KingCoords[1])):
                return True
            else:
                return False



    def listofValidMoves(self,theBoard):
        nameChar = self.name[0]
        validMoves = []
        
        for row in range(0,8):
            for col in range(0,8):
                if(not(self.col == col and self.row == row) and theBoard.gameBoard[row][col].name[0] != nameChar):
                    if( self.diagonalPath(theBoard,row,col)):
                        validMoves.append([row,col])
        return validMoves






#--------------------------------------KingSubclass---------------------------------------------------
class King(Piece):

    def validMove(self,theBoard):
        theCoords = input("Please enter the coordinates of the square you wish to move onto using the form row,col")
        row = -1
        col = -1
        #we first get the coordinates of the place on the board that the player wishes to move to
        if len(theCoords) ==3 and theCoords[0].isdigit() and theCoords[1] == "," and theCoords[2].isdigit():
            row = int(theCoords[0])
            col = int(theCoords[2])
        else:
            raise(AssertionError) 

        assert(row >= 0 and row <= 7 and col >=0 and col <= 7) #making sure the coordinates are squares on the board
        assert(not (row == self.row and col == self.col)) #making sure the square is not the current square
        assert(theBoard.gameBoard[row][col].name[0] != self.name[0]) #making sure the desired square is either holding an opponent's piece or is empty
        assert(theBoard.gameBoard[row][col].name[2] != "G") #making sure the desired square does not hold a king

        assert(abs(row-self.row) == 1 and abs(col-self.col)) #making sure the move is one square in some direction

        #need to check that king is not moving into check


        #by this point we know we can perform the move
        newBoard = theBoard
        oldPiece = newBoard.gameBoard[row][col] #the piece that will be getting deleted
        newBoard.gameBoard[self.row][self.col] = EmptySquare("---",self.row,self.col) #set the square of the current piece to be empty
        self.row = row #updating the row of moving piece
        self.col = col #updating the col of moving piece
        newBoard.gameBoard[oldPiece.row][oldPiece.col] = self #setting the board to be the moved
        return [newBoard,oldPiece,self]


    def checkingKing(self,theBoard,otherPlayer):
        return False


    def listofValidMoves(self,theBoard): 
        nameChar = self.name[0]
        validMoves = []
        if(self.col - 1 >= 0):
            if(theBoard.gameBoard[self.row][self.col-1].name[0] != nameChar):
                validMoves.append([self.row,self.col-1])
            if(self.row+1 <= 7 and theBoard.gameBoard[self.row+1][self.col-1] != nameChar):
                validMoves.append([self.row+1,self.col-1])
            if(self.row - 1 >= 0 and theBoard.gameBoard[self.row-1][self.col-1] != nameChar):
                validMoves.append([self.row-1,self.col-1])
        if(self.row+1 <= 7 and theBoard.gameBoard[self.row+1,self.col] != nameChar):
            validMoves.append([self.row+1,self.col])
        if(self.row - 1 >= 0 and theBoard.gameBoard[self.row-1][self.col] != nameChar):
            validMoves.append([self.row-1,self.col])
        if(self.col + 1 <= 7):
            if(theBoard.gameBoard[self.row][self.col+1].name[0] != nameChar):
                validMoves.append([self.row,self.col+1])
            if(self.row+1 <= 7 and theBoard.gameBoard[self.row+1][self.col+1] != nameChar):
                validMoves.append([self.row+1,self.col+1])
            if(self.row - 1 >= 0 and theBoard.gameBoard[self.row-1][self.col+1] != nameChar):
                validMoves.append([self.row-1,self.col+1])
        print(validMoves)
        return validMoves



#-----------------KnightSubclass--------------------------------------------------------
class Knight(Piece):

    def validMove(self,theBoard):
        theCoords = input("Please enter the coordinates of the square you wish to move onto using the form row,col")
        row = -1
        col = -1
        #we first get the coordinates of the place on the board that the player wishes to move to
        if len(theCoords) ==3 and theCoords[0].isdigit() and theCoords[1] == "," and theCoords[2].isdigit():
            row = int(theCoords[0])
            col = int(theCoords[2])
        else:
            raise(AssertionError) 

        assert(row >= 0 and row <= 7 and col >=0 and col <= 7) #making sure the coordinates are squares on the board
        assert(not (row == self.row and col == self.col)) #making sure the square is not the current square
        assert(theBoard.gameBoard[row][col].name[0] != self.name[0]) #making sure the desired square is either holding an opponent's piece or is empty
        assert(theBoard.gameBoard[row][col].name[2] != "G") #making sure the desired square does not hold a king

        if row == self.row - 1 and col - 2 == self.col:
            pass
        elif row == self.row - 1 and col + 2 == self.col:
            pass
        elif row == self.row + 1 and col - 2 == self.col:
            pass
        elif row == self.row + 1 and col + 2 == self.col:
            pass
        elif row == self.row - 2 and col - 1 == self.col:
            pass
        elif row == self.row - 2 and col + 1 == self.col:
            pass
        elif row == self.row + 2 and col - 1 == self.col:
            pass
        elif row == self.row + 2 and col + 1 == self.col:
            pass
        else:
            raise(AssertionError)

        #by this point we know we can perform the move
        newBoard = theBoard
        oldPiece = newBoard.gameBoard[row][col] #the piece that will be getting deleted
        newBoard.gameBoard[self.row][self.col] = EmptySquare("---",self.row,self.col,True) #set the square of the current piece to be empty
        self.row = row #updating the row of moving piece
        self.col = col #updating the col of moving piece
        newBoard.gameBoard[oldPiece.row][oldPiece.col] = self #setting the board to be the moved
        return [newBoard,oldPiece,self]



    def checkingKing(self,theBoard,otherPlayer): #tells whether or not this piece is checking the opponent's king
        if(self.isDead):
            return False
        if(theBoard.p1Turn):
            p2KingCoords = otherPlayer.getKingCoords()
            if(abs(p2KingCoords[0]-self.row) == 2 and abs(p2KingCoords[1]-self.col) == 1):
                return True
            elif (abs(p2KingCoords[0]-self.row) == 1 and abs(p2KingCoords[1]-self.col) == 2):
                return True
            else:
                return False

        else:
            p1KingCoords = otherPlayer.getKingCoords()
            if(abs(p1KingCoords[0]-self.row) == 2 and abs(p1KingCoords[1]-self.col) == 1):
                return True
            elif (abs(p1KingCoords[0]-self.row) == 1 and abs(p1KingCoords[1]-self.col) == 2):
                return True
            else:
                return False


    def listofValidMoves(self,theBoard):
        nameChar = self.name[0]
        validMoves = []
        if self.row - 1 >= 0 and self.col - 2 >=0 and theBoard.gameBoard[self.row-1][self.col-2].name[0] != nameChar:
            validMoves.append([self.row-1,self.col-2])
        if self.row - 1 >= 0 and self.col + 2 <=7 and theBoard.gameBoard[self.row-1][self.col+2].name[0] != nameChar:
            validMoves.append([self.row-1,self.col+2])
        if self.row + 1 <= 7 and self.col - 2 >= 0 and theBoard.gameBoard[self.row+1][self.col-2].name[0] != nameChar:
            validMoves.append([self.row+1,self.col-2])
        if self.row + 1 <= 7  and self.col + 2  <= 7 and theBoard.gameBoard[self.row+1][self.col-2].name[0] != nameChar:
            validMoves.append([self.row+1,self.col-2])
        if self.row - 2 >= 0 and self.col - 1 >= 0 and theBoard.gameBoard[self.row-2][self.col-1].name[0] != nameChar :
            validMoves.append([self.row-2,self.col-1])
        if self.row - 2 >= 0 and self.col + 1 <= 7 and theBoard.gameBoard[self.row-2][self.col+1].name[0] != nameChar:
            validMoves.append([self.row-2,self.col+1])
        if self.row + 2 <= 7 and self.col-1 >= 0 and theBoard.gameBoard[self.row+2][self.col-1].name[0] != nameChar:
            validMoves.append([self.row+2,self.col-1])
        if self.row + 2 <= 7 and self.col+1 <= 7 and theBoard.gameBoard[self.row+2][self.col+1].name[0] != nameChar:
            validMoves.append([self.row+2,self.col+1])
        return validMoves






#---------------------------------------------PawnSubclass------------------------------------------
class Pawn(Piece):

    def __init__(self,name,row,col,isDead): #different constructor for a pawn then a basic piece
        self.name = name
        self.row = row
        self.col = col
        self.isDead = isDead
        self.firstMove = True #pawn can move two up on first move



    def validMove(self,theBoard):
        theCoords = input("Please enter the coordinates of the square you wish to move onto using the form row,col")
        row = -1
        col = -1
        #we first get the coordinates of the place on the board that the player wishes to move to
        if len(theCoords) ==3 and theCoords[0].isdigit() and theCoords[1] == "," and theCoords[2].isdigit():
            row = int(theCoords[0])
            col = int(theCoords[2])
        else:
            raise(AssertionError) 

        assert(row >= 0 and row <= 7 and col >=0 and col <= 7) #making sure the coordinates are squares on the board
        assert(not (row == self.row and col == self.col)) #making sure the square is not the current square
        assert(theBoard.gameBoard[row][col].name[0] != self.name[0]) #making sure the desired square is either holding an opponent's piece or is empty
        assert(theBoard.gameBoard[row][col].name[2] != "G") #making sure the desired square does not hold a king

        if(theBoard.p1Turn): #making sure that pawn is moving forward
            assert(row == self.row + 1 or row == self.row + 2)
            if(col != self.col): #the pawn is moving diagonally
                assert(col == self.col + 1 or col == self.col - 1)
                assert(theBoard.gameBoard[row][col].name != "---" and theBoard.gameBoard[row][col].name[0] != self.name[0])
            elif row == self.row + 2:
                assert(col == self.col)
                assert(self.firstMove)
                assert(theBoard.gameBoard[row][col].name == "---")
            else:
                assert(col == self.col)
                assert(theBoard.gameBoard[row][col].name == "---")
        else:
            assert(row == self.row - 1 or row == self.row - 2)
            if(col != self.col): #the pawn is moving diagonally
                assert(col == self.col + 1 or col == self.col - 1)
                assert(theBoard.gameBoard[row][col].name != "---" and theBoard.gameBoard[row][col].name[0] != self.name[0])
            elif row == self.row - 2:
                assert(col == self.col)
                assert(self.firstMove)
                assert(theBoard.gameBoard[row][col].name == "---")
            else:
                assert(col == self.col)
                assert(theBoard.gameBoard[row][col].name == "---")


        newPiece = self
        if((theBoard.p1Turn and row == 7) or (not theBoard.p1Turn and row == 0)): #assuming you can have a max of one extra of each piece
            print("You have successfully promoted a pawn!")
            print("You must now choose what to the pawn to")
            desiredPromotion = input("Enter R for Rook, K for Knight, B for Bishop, Q for Queen")
            if(desiredPromotion == "Q"):
                newPiece = Queen(self.name[0]+"Q"+"2",row,col,False)
            elif(desiredPromotion == "R"):
                newPiece = Rook(self.name[0]+"R"+"3",row,col,False)
            elif(desiredPromotion == "K"):
                newPiece = Knight(self.name[0]+"K"+"3",row,col,False)
            else:
                newPiece = Bishop(self.name[0]+"B"+"3",row,col,False)

        if(row == self.row + 2 or row == self.row - 2):
            self.firstMove == False


        newBoard = theBoard
        oldPiece = newBoard.gameBoard[row][col] #the piece that will be getting deleted
        newBoard.gameBoard[self.row][self.col] = EmptySquare("---",self.row,self.col,True) #set the square of the current piece to be empty
        self.row = row #updating the row of moving piece
        self.col = col #updating the col of moving piece
        newBoard.gameBoard[oldPiece.row][oldPiece.col] = self #setting the board to be the moved
        return [newBoard,oldPiece,newPiece]



    def checkingKing(self,theBoard,otherPlayer): #tells whether or not this piece is checking the opponent's king
        if(self.isDead):
            return False
        if(theBoard.p1Turn):
            p2KingCoords = otherPlayer.getKingCoords()
            if(self.diagonalPath(theBoard,p2KingCoords[0],p2KingCoords[1])):
                return True
            else:
                return False

        else:
            p1KingCoords = otherPlayer.getKingCoords()
            if(self.diagonalPath(theBoard,p1KingCoords[0],p1KingCoords[1])):
                return True
            else:
                return False




    def listofValidMoves(self,theBoard):
        row = self.row
        col = self.col
        nameChar = self.name[0]
        validMoves = []
        if(theBoard.p1Turn):
            if(theBoard.gameBoard[row+1][col].name[0] != nameChar):
                validMoves.append([row+1,col])
            if(theBoard.gameBoard[row+2][col].name[0] != nameChar and self.firstMove):
                validMoves.append([row+2,col])
            if(col - 1 >= 0 and theBoard.gameBoard[row+1][col-1].name[0] != nameChar and theBoard.gameBoard[row+1][col-1].name != "---"):
                validMoves.append([row+1,col-1])
            if(col+1 <= 7 and theBoard.gameBoard[row+1][col+1].name[0] != nameChar and theBoard.gameBoard[row+1][col+1].name != "---"):
                validMoves.append([row+1,col-1])
        else:
            if(theBoard.gameBoard[row-1][col].name[0] != nameChar):
                validMoves.append([row-1,col])
            if(theBoard.gameBoard[row-2][col].name[0] != nameChar and self.firstMove):
                validMoves.append([row-2,col])
            if(col - 1 >= 0 and theBoard.gameBoard[row-1][col-1].name[0] != nameChar and theBoard.gameBoard[row-1][col-1].name != "---"):
                validMoves.append([row+1,col-1])
            if(col+1 <= 7 and theBoard.gameBoard[row-1][col+1].name[0] != nameChar and theBoard.gameBoard[row-1][col+1].name != "---"):
                validMoves.append([row-1,col-1])
        
        return validMoves

        
#----------------------------------QueenSubclass---------------------------------------------
class Queen(Piece):

    def validMove(self,theBoard):
        theCoords = input("Please enter the coordinates of the square you wish to move onto using the form row,col")
        row = -1
        col = -1
        #we first get the coordinates of the place on the board that the player wishes to move to
        if len(theCoords) ==3 and theCoords[0].isdigit() and theCoords[1] == "," and theCoords[2].isdigit():
            row = int(theCoords[0])
            col = int(theCoords[2])
        else:
            raise(AssertionError) 

        assert(row >= 0 and row <= 7 and col >=0 and col <= 7) #making sure the coordinates are squares on the board
        assert(not (row == self.row and col == self.col)) #making sure the square is not the current square
        assert(theBoard.gameBoard[row][col].name[0] != self.name[0]) #making sure the desired square is either holding an opponent's piece or is empty
        assert(theBoard.gameBoard[row][col].name[2] != "G") #making sure the desired square does not hold a king


        if row == self.row: #there could be a potential horizontal path
            if(self.horizontalPath(theBoard,row,col)):
                pass
            else:
                raise(AssertionError)
        
        elif col == self.col: #there is a potential vertical path
            if(self.verticalPath(theBoard,row,col)):
                pass
            else:
                print("fuckoff")
                raise(AssertionError)

        else: #there is a potential diagonal path
            currSpace = self.row * 8 + self.col
            desiredSpace = row * 8 + col #checking the square entered is diagonal from current square
            if(not (currSpace % 9 == desiredSpace % 9) and not (currSpace % 7 == desiredSpace % 7)): 
                raise(AssertionError)

            elif(not self.diagonalPath(theBoard,row,col)):
                raise(AssertionError)

        #by this point we know we can perform the move
        newBoard = theBoard
        oldPiece = newBoard.gameBoard[row][col] #the piece that will be getting deleted
        newBoard.gameBoard[self.row][self.col] = EmptySquare("---",self.row,self.col,True) #set the square of the current piece to be empty
        self.row = row #updating the row of moving piece
        self.col = col #updating the col of moving piece
        newBoard.gameBoard[oldPiece.row][oldPiece.col] = self #setting the board to be the moved
        return [newBoard,oldPiece,self]



    def checkingKing(self,theBoard,otherPlayer): #tells whether or not this piece is checking the opponent's king
        if(self.isDead):
            return False
        if(theBoard.p1Turn):
            p2KingCoords = otherPlayer.getKingCoords()
            if(self.diagonalPath(theBoard,p2KingCoords[0],p2KingCoords[1])):
                return True
            elif(self.horizontalPath(theBoard,p2KingCoords[0],p2KingCoords[1])):
                return True
            elif(self.verticalPath(theBoard,p2KingCoords[0],p2KingCoords[1])):
                return True
            else:
                return False
        else:
            p1KingCoords = otherPlayer.getKingCoords()
            if(self.diagonalPath(theBoard,p1KingCoords[0],p1KingCoords[1])):
                return True
            elif(self.horizontalPath(theBoard,p1KingCoords[0],p1KingCoords[1])):
                return True
            elif(self.verticalPath(theBoard,p1KingCoords[0],p1KingCoords[1])):
                return True
            else:
                return False



    def listofValidMoves(self,theBoard):
        nameChar = self.name[0]
        validMoves = []
        
        for row in range(0,8):
            for col in range(0,8):
                if(not(self.col == col and self.row == row) and theBoard.gameBoard[row][col].name[0] != nameChar):
                    if(self.horizontalPath(theBoard,row,col) or self.verticalPath(theBoard,row,col) or self.diagonalPath(theBoard,row,col)):
                        validMoves.append([row,col])
        return validMoves



#---------------------------------------RookSubclass------------------------------------------------
class Rook(Piece):


    def validMove(self,theBoard):
        theCoords = input("Please enter the coordinates of the square you wish to move onto using the form row,col")
        row = -1
        col = -1
        #we first get the coordinates of the place on the board that the player wishes to move to
        if len(theCoords) ==3 and theCoords[0].isdigit() and theCoords[1] == "," and theCoords[2].isdigit():
            row = int(theCoords[0])
            col = int(theCoords[2])
        else:
            raise(AssertionError) 

        assert(row >= 0 and row <= 7 and col >=0 and col <= 7) #making sure the coordinates are squares on the board
        assert(not (row == self.row and col == self.col)) #making sure the square is not the current square
        assert(row == self.row or col == self.col) #making sure the desired square is either horizontal or vertical from current square
        assert(theBoard.gameBoard[row][col].name[0] != self.name[0]) #making sure the desired square is either holding an opponent's piece or is empty
        assert(theBoard.gameBoard[row][col].name[2] != "G") #making sure the desired square does not hold a king
        
        if(row == self.row):
            if(not self.horizontalPath(theBoard,row,col)):
                raise(AssertionError)
        if(col == self.col):
            if(not self.verticalPath(theBoard,row,col)):
                raise (AssertionError)

        #by this point we know we can perform the move
        newBoard = theBoard
        oldPiece = newBoard.gameBoard[row][col] #the piece that will be getting deleted
        newBoard.gameBoard[self.row][self.col] = EmptySquare("---",self.row,self.col,True) #set the square of the current piece to be empty
        self.row = row #updating the row of moving piece
        self.col = col #updating the col of moving piece
        newBoard.gameBoard[oldPiece.row][oldPiece.col] = self #setting the board to be the moved
        return [newBoard,oldPiece,self]




    def checkingKing(self,theBoard,otherPlayer): #tells whether or not this piece is checking the opponent's king
        if(self.isDead):
            return False
        if(theBoard.p1Turn):
            p2KingCoords = otherPlayer.getKingCoords()
            if(self.horizontalPath(theBoard,p2KingCoords[0],p2KingCoords[1])):
                return True
            elif(self.verticalPath(theBoard,p2KingCoords[0],p2KingCoords[1])):
                return True
            else:
                return False
        else:
            p1KingCoords = otherPlayer.getKingCoords()
            if(self.horizontalPath(theBoard,p1KingCoords[0],p1KingCoords[1])):
                return True
            elif(self.verticalPath(theBoard,p1KingCoords[0],p1KingCoords[1])):
                return True
            else:
                return False



    def listofValidMoves(self,theBoard):
        nameChar = self.name[0]
        validMoves = []
        
        for row in range(0,8):
            for col in range(0,8):
                if(not(self.col == col and self.row == row) and theBoard.gameBoard[row][col].name[0] != nameChar):
                    if(self.verticalPath(theBoard,row,col) or self.horizontalPath(theBoard,row,col)):
                        validMoves.append([row,col])
        return validMoves
            

