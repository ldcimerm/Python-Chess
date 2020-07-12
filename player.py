import board
import piece
import copy


#these are the pieces that each player will initially start each game with
p1InitializedPieces = [piece.Rook("R2",0,0,False),piece.Knight("K2",0,1,False),piece.Bishop("B2",0,2,False),piece.Queen("Q1",0,3,False),\
    piece.King("KG",0,4,False),piece.Bishop("B1",0,5,False), piece.Knight("K1",0,6,False),piece.Rook("R1",0,7,False), \
    piece.Pawn("P8",1,0,False),piece.Pawn("P7",1,1,False),piece.Pawn("P6",1,2,False),piece.Pawn("P5",1,3,False),piece.Pawn("P4",1,4,False), \
    piece.Pawn("P3",1,5,False),piece.Pawn("P2",1,6,False),piece.Pawn("P1",1,7,False)]

p2InitializedPieces = [piece.Pawn("P1",6,0,False),piece.Pawn("P2",6,1,False),piece.Pawn("P3",6,2,False),piece.Pawn("P4",6,3,False),piece.Pawn("P5",6,4,False), \
    piece.Pawn("P6",6,5,False),piece.Pawn("P7",6,6,False),piece.Pawn("P8",6,7,False), \
    piece.Rook("R1",7,0,False),piece.Knight("K1",7,1,False),piece.Bishop("B1",7,2,False),piece.King("KG",7,3,False),\
    piece.Queen("Q1",7,4,False),piece.Bishop("B2",7,5,False), piece.Knight("K2",7,6,False),piece.Rook("R2",7,7,False)]


class Player:
    '''Player objects will have a list of Piece objects that are owned by the player
    '''
    def __init__(self,name,isPlayer1): #constructor
        self.name = name
        self.isPlayer1 = isPlayer1
        playerId = name[0]
        if isPlayer1 == True:
            self.myPieces = p1InitializedPieces
        else:
            self.myPieces = p2InitializedPieces

        listLength = len(self.myPieces)
        counter = 0
        while counter != listLength: #add a identifier(playerName[0]) to each piece
            self.myPieces[counter].name = playerId + self.myPieces[counter].name
            counter += 1
            


    def addToMyPieces(self,piece): #adds a piece to the pieces that are owned by the player. Only useful when initializing game
        self.myPieces.append(piece)



    def choosePiece(self,pieceName): #finds the piece that a player wishes to move
        for p in self.myPieces:
            if(p.name == pieceName and not p.isDead):
                return p
        raise(IndexError)


    def updateMyPieces(self,newPiece): #updates a player's myPieces to hold the moved piece
        counter = 0
        while counter != len(self.myPieces):
            if self.myPieces[counter].name == newPiece.name:
                self.myPieces[counter] = newPiece
                break
            else:
                counter += 1


    def removePiece(self,pieceToRemove): #removes pieceToRemove from the player's myPieces by setting it to be dead
        counter = 0
        while counter != len(self.myPieces):
            if self.myPieces[counter].name == pieceToRemove:
                self.myPieces[counter].isDead = True
                break
            else:
                counter += 1



    def getKingCoords(self): #returns the coordinates of the king
        for p in self.myPieces:
            if(p.name[2] == "G"):
                return [p.row,p.col]


    
    def kingInCheck(self,theBoard,otherPlayer): #tells whether this player's king is in check
        for p in otherPlayer.myPieces: #it loops through the pieces in the other player's pieces and checks if any of those pieces
            if(p.checkingKing(theBoard,self)): #is checking their king
               return True
        return False




    def checkMate(self,theBoard,otherPlayer):
        if(not self.kingInCheck(theBoard,otherPlayer)): #if the king is not in check, no chance of checkmate
           return False
        for p in self.myPieces: #otherwise the player's king is in check
            if(not p.isDead):
                validMoves = p.listofValidMoves(theBoard) #then for each piece the player has access to, we get a list of possible places
                for coord in validMoves:                  #that it can move to
                    newBoard = copy.deepcopy(theBoard)
                    newBoard.gameBoard[p.row][p.col] = piece.EmptySquare("---",p.row,p.col,True)
                    newBoard.gameBoard[coord[0]][coord[1]] = p #then for each piece, we make the changes to the board and see if the king is still
                    newBoard.gameBoard[coord[0]][coord[1]].row == coord[0] #in check
                    newBoard.gameBoard[coord[0]][coord[1]].col == coord[1]
                    if(not self.kingInCheck(newBoard,otherPlayer)): #if there is a move that gets the king out of check, we are not in checkmate
                        return False
                #otherwise the king is in checkmate
        return True

