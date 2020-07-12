import player
import piece
import board


def main():
    print("Welcome to Python chess!")

    #we first get the names of the two players. 
    p1Name = input("Player 1, please enter your name")
    while(not p1Name[0].isalpha()):
        p1Name = input("That is an invalid name. Please give a proper name")

    p2Name = input("Player 2, please enter your name")
    while(not p2Name[0].isalpha() or p2Name == p1Name):
        p2Name = input("That is an invalid name. Please give a proper name")

    #the players are now being constructed and are set to have the correct pieces
    Player1 = player.Player(p1Name,True)
    Player2 = player.Player(p2Name,False)
    #the Board is initialized to have the correct pieces
    gameBoard = board.Board(Player1,Player2)
    print("Welcome to the game {0} and {1}. Let's get started".format(p1Name,p2Name))
    print("")
    print("")

    player1Turn = True

    while(True):
        gameBoard.draw()
        if(player1Turn):
            try:
                pieceToMove = input("{}, input the name of the piece you wish to move".format(p1Name))
                chosenPiece = Player1.choosePiece(pieceToMove)
                moveInfo = chosenPiece.validMove(gameBoard)
                gameBoard = moveInfo[0]
                Player2.removePiece(moveInfo[1])
                Player1.updateMyPieces(moveInfo[2])
                player1Turn = False
                gameBoard.p1Turn = False
                if(Player2.checkMate(gameBoard,Player1)):
                   print("{} wins the game".format(p1Name))
                   break
                if(Player2.kingInCheck(gameBoard,Player1)):
                    print("{}, your king is in check. You must deal with that".format(p2Name))
            except IndexError:
                print("That is not a valid move")
            except AssertionError:
                print("That is not a valid move")
        else:
            try:
                pieceToMove = input("{}, input the name of the piece you wish to move".format(p2Name))
                chosenPiece = Player2.choosePiece(pieceToMove)
                moveInfo = chosenPiece.validMove(gameBoard)
                gameBoard = moveInfo[0]
                Player1.removePiece(moveInfo[1])
                Player2.updateMyPieces(moveInfo[2])
                player1Turn = True
                gameBoard.p1Turn = True
                if(Player1.checkMate(gameBoard,Player2)):
                    print("{} wins the game".format(p2Name))
                    break
                elif(Player1.kingInCheck(gameBoard,Player2)):
                    print("{}, your king is in check. You must deal with that".format(p1Name))
            except IndexError:
                print("That is not a valid move")
            except AssertionError:
                print("That is not a valid move")