# Skeleton Program code for the AQA COMP1 Summer 2015 examination
# this code should be used in conjunction with the Preliminary Material
# written by the AQA COMP1 Programmer Team
# developed in the Python 3.4 programming environment

import sys
import re
from itertools import groupby

BOARDDIMENSION = 8

DEBUG = False  # enable debug printing


def generate_fen(board :list=list(), turn :str='W'):
    '''formats a board list into a Forsyth–Edwards Notation string, following the spec
    uses all sorts of black magic to make it work

    example:
        (the default board) -> \'genmsneg\\rrrrrrrr\\8\\8\\8\\8\\RRRRRRRR\\GENMSNEG\\W\''''
    def format_rank(rank :list):
        '''formats piece string into it's fen version

        example:
            BG -> g
            WR -> R

        input:
            rank: a row from the board'''
        return map(lambda x: x[1].__getattribute__({"B":"lower", "W":"upper"}[x[0]])() if str(x).isalpha() else None, rank)

    def collate_rank(rank :list):
        '''minimizes empty cells to their count, formats into a string

        example:
            ["R"," "," ","g"] -> R2g

        input:
            rank: formatted list of pieces (from format_rank function)'''
        string = [[k, list(g)] for k,g in groupby(format_rank(rank[1:]))]
        return str().join(map(lambda x: str(len(x[1])) if not x[0] else str().join(x[1]), string))

    return "{}\{}".format('\\'.join(list(map(collate_rank, board[1:]))), turn)

def decode_fen(fenStr :str=""):
    '''decodes a Forsyth–Edwards Notation sting into a 2d array'''
    def unpack_rank(rank :str):
        '''unpacks packed fen string into a list

        example:
            "R4g2" -> ["R"," "," "," "," ","g"," "," "]

        input:
            rank: packed fen string'''
        def format(x):
            return " "*int(x.group())
        return map(lambda x: x*2 if not x.isalpha() else x, re.sub(re.compile('\d'), format , rank))

    def format_rank(rank :str):
        '''formats a fen encoded list into a piece string version

        example:
            g -> BG
            R -> WR

        input:
            rank: fen encoded list'''
        return list(map(lambda x: "{}{}".format("b" if x.islower() else 'W', x).upper() if x.isalpha() else x, rank))

    def fix_list(array :list):
        '''helper function to format generated list into the type used by the game
        (empty row on top of board, and each row padded by an empty cell'''
        return [ ["  " for i in range(BOARDDIMENSION+1)], *list(map(lambda x: ["  "] + x, array))]


    validate = re.compile(r"([\w\d]+\\)+[WB]")

    if not re.match(validate, fenStr):
        return None, None
        # verify that the fen string is complete

    chain_funcs = lambda x: format_rank(unpack_rank(x))
    fen_list = fenStr.split("\\")
    return fix_list(map(chain_funcs, fen_list[:-1])), fen_list[-1]



def print_name(func):
    def callme(*args):
        if DEBUG:
            print('entering function: {0.__name__} with {1} params of type {2}'.format(
                func, len(args), [type(i) for i in args]), file=sys.stderr)
        values = func(*args)
        if DEBUG:
            print('exiting function: {0.__name__} with {1} params of type {2}'.format(
                func, len(args), [type(i) for i in args]), file=sys.stderr)
        return values
    return callme


def expand_arguments(func):
    def callme(*args):
        return func(*args+args) #works on my machine
    return callme


@print_name
def CreateBoard():
    '''generate a 2d array of length BOARDDIMENSION+1 and width BOARDDIMENSSION+1'''
    Board = [["  " for i in range(BOARDDIMENSION + 1)] for j in range(BOARDDIMENSION + 1)]
    return Board


@print_name
def DisplayWhoseTurnItIs(WhoseTurn):
    '''prints whose turn it is'''
    if WhoseTurn == "W":
        print("It is White's turn")
    else:
        print("It is Black's turn")


@print_name
def GetTypeOfGame():
    '''ask user for type of game'''
    TypeOfGame = input(
        "Do you want to play the sample game (enter Y for Yes)? ")
    return TypeOfGame


@print_name
def DisplayWinner(WhoseTurn):
    '''print winner of game'''
    if WhoseTurn == "W":
        print("Black's Sarrum has been captured.  White wins!")
    else:
        print("White's Sarrum has been captured.  Black wins!")


@print_name
def CheckIfGameWillBeWon(Board, FinishRank, FinishFile):
    '''determine if game is won'''
    if Board[FinishRank][FinishFile][1] == "S":
        return True
    else:
        return False


@print_name
def DisplayBoard(Board):
    '''print game board'''
    print()
    for RankNo in range(1, BOARDDIMENSION + 1):
        print("     _______________________")
        print(RankNo, end="   ")
        for FileNo in range(1, BOARDDIMENSION + 1):
            print("|" + Board[RankNo][FileNo], end="")
        print("|")
    print("     _______________________")
    print("\n      1  2  3  4  5  6  7  8\n\n")


@print_name
def CheckRedumMoveIsLegal(Board, StartRank, StartFile, FinishRank, FinishFile, ColourOfPiece):
    '''determine if a move is legal'''
    CheckRedumMoveIsLegal = False
    if ColourOfPiece == "W":
        if FinishRank == StartRank - 1:
            if FinishFile == StartFile and Board[FinishRank][FinishFile] == "  ":
                CheckRedumMoveIsLegal = True
            elif abs(FinishFile - StartFile) == 1 and Board[FinishRank][FinishFile][0] == "B":
                CheckRedumMoveIsLegal = True
    elif FinishRank == StartRank + 1:
        if FinishFile == StartFile and Board[FinishRank][FinishFile] == "  ":
            CheckRedumMoveIsLegal = True
        elif abs(FinishFile - StartFile) == 1 and Board[FinishRank][FinishFile][0] == "W":
            CheckRedumMoveIsLegal = True
    return CheckRedumMoveIsLegal


@print_name
def CheckSarrumMoveIsLegal(Board, StartRank, StartFile, FinishRank, FinishFile):
    '''determine if a move is legal'''
    CheckSarrumMoveIsLegal = False
    if abs(FinishFile - StartFile) <= 1 and abs(FinishRank - StartRank) <= 1:
        CheckSarrumMoveIsLegal = True
    return CheckSarrumMoveIsLegal


@print_name
def CheckGisgigirMoveIsLegal(Board, StartRank, StartFile, FinishRank, FinishFile):
    '''determine if a move is legal'''
    GisgigirMoveIsLegal = False
    RankDifference = FinishRank - StartRank
    FileDifference = FinishFile - StartFile
    if RankDifference == 0:
        if FileDifference >= 1:
            GisgigirMoveIsLegal = True
            for Count in range(1, FileDifference):
                if Board[StartRank][StartFile + Count] != "  ":
                    GisgigirMoveIsLegal = False
        elif FileDifference <= -1:
            GisgigirMoveIsLegal = True
            for Count in range(-1, FileDifference, -1):
                if Board[StartRank][StartFile + Count] != "  ":
                    GisgigirMoveIsLegal = False
    elif FileDifference == 0:
        if RankDifference >= 1:
            GisgigirMoveIsLegal = True
            for Count in range(1, RankDifference):
                if Board[StartRank + Count][StartFile] != "  ":
                    GisgigirMoveIsLegal = False
        elif RankDifference <= -1:
            GisgigirMoveIsLegal = True
            for Count in range(-1, RankDifference, -1):
                if Board[StartRank + Count][StartFile] != "  ":
                    GisgigirMoveIsLegal = False
    return GisgigirMoveIsLegal


@print_name
def CheckNabuMoveIsLegal(Board, StartRank, StartFile, FinishRank, FinishFile):
    '''determine if a move is legal'''
    CheckNabuMoveIsLegal = False
    if abs(FinishFile - StartFile) == 1 and abs(FinishRank - StartRank) == 1:
        CheckNabuMoveIsLegal = True
    return CheckNabuMoveIsLegal


@print_name
def CheckMarzazPaniMoveIsLegal(Board, StartRank, StartFile, FinishRank, FinishFile):
    '''determine if a move is lagal'''
    CheckMarzazPaniMoveIsLegal = False
    if (abs(FinishFile - StartFile) == 1 and abs(FinishRank - StartRank) == 0) or (abs(FinishFile - StartFile) == 0 and abs(FinishRank - StartRank) == 1):
        CheckMarzazPaniMoveIsLegal = True
    return CheckMarzazPaniMoveIsLegal


@print_name
def CheckEtluMoveIsLegal(Board, StartRank, StartFile, FinishRank, FinishFile):
    '''determine if a move is legal'''
    CheckEtluMoveIsLegal = False
    if (abs(FinishFile - StartFile) == 2 and abs(FinishRank - StartRank) == 0) or (abs(FinishFile - StartFile) == 0 and abs(FinishRank - StartRank) == 2):
        CheckEtluMoveIsLegal = True
    return CheckEtluMoveIsLegal


@print_name
@expand_arguments
def CheckMoveIsLegal(Board, StartRank, StartFile, FinishRank, FinishFile, WhoseTurn, *args):
    '''coordinator for legal move functions'''
    MoveIsLegal = True
    if (FinishFile == StartFile) and (FinishRank == StartRank):
        MoveIsLegal = False
    if not all(map(lambda x: x in range(1,BOARDDIMENSION+1), args[1:-1])):
        return False
    else:
        PieceType = Board[StartRank][StartFile][1]
        PieceColour = Board[StartRank][StartFile][0]
        if WhoseTurn == "W":
            if PieceColour != "W":
                MoveIsLegal = False
            if Board[FinishRank][FinishFile][0] == "W":
                MoveIsLegal = False
        else:
            if PieceColour != "B":
                MoveIsLegal = False
            if Board[FinishRank][FinishFile][0] == "B":
                MoveIsLegal = False
        if MoveIsLegal == True:
            if PieceType == "R":
                MoveIsLegal = CheckRedumMoveIsLegal(
                    Board, StartRank, StartFile, FinishRank, FinishFile, PieceColour)
            elif PieceType in "SK": # same legal moves
                MoveIsLegal = CheckSarrumMoveIsLegal(
                    Board, StartRank, StartFile, FinishRank, FinishFile)
            elif PieceType == "M":
                MoveIsLegal = CheckMarzazPaniMoveIsLegal(
                    Board, StartRank, StartFile, FinishRank, FinishFile)
            elif PieceType == "G":
                MoveIsLegal = CheckGisgigirMoveIsLegal(
                    Board, StartRank, StartFile, FinishRank, FinishFile)
            elif PieceType == "N":
                MoveIsLegal = CheckNabuMoveIsLegal(
                    Board, StartRank, StartFile, FinishRank, FinishFile)
            elif PieceType == "E":
                MoveIsLegal = CheckEtluMoveIsLegal(
                    Board, StartRank, StartFile, FinishRank, FinishFile)
    return MoveIsLegal


@print_name
def InitialiseBoard(Board, SampleGame):
    '''starts the board for the game'''
    if SampleGame == "Y":
        for RankNo in range(1, BOARDDIMENSION + 1):
            for FileNo in range(1, BOARDDIMENSION + 1):
                Board[RankNo][FileNo] = "  "
        Board[1][2] = "BG"
        Board[1][4] = "BS"
        Board[1][8] = "WG"
        Board[2][1] = "WR"
        Board[3][1] = "WS"
        Board[3][2] = "BE"
        Board[3][8] = "BE"
        Board[6][8] = "BR"
    else:
        for RankNo in range(1, BOARDDIMENSION + 1):
            for FileNo in range(1, BOARDDIMENSION + 1):
                if RankNo == 2:
                    Board[RankNo][FileNo] = "BR"
                elif RankNo == 7:
                    Board[RankNo][FileNo] = "WR"
                elif RankNo == 1 or RankNo == 8:
                    if RankNo == 1:
                        Board[RankNo][FileNo] = "B"
                    if RankNo == 8:
                        Board[RankNo][FileNo] = "W"
                    if FileNo == 1 or FileNo == 8:
                        Board[RankNo][FileNo] = Board[RankNo][FileNo] + "G"
                    elif FileNo == 2 or FileNo == 7:
                        Board[RankNo][FileNo] = Board[RankNo][FileNo] + "E"
                    elif FileNo == 3 or FileNo == 6:
                        Board[RankNo][FileNo] = Board[RankNo][FileNo] + "N"
                    elif FileNo == 4:
                        Board[RankNo][FileNo] = Board[RankNo][FileNo] + "M"
                    elif FileNo == 5:
                        Board[RankNo][FileNo] = Board[RankNo][FileNo] + "S"
                else:
                    Board[RankNo][FileNo] = "  "


@print_name
def GetMove(StartSquare, FinishSquare):
    '''asks user for input'''
    def try_int(x):
        try:
            return int(x)
        except:
            return 0

    StartSquare = try_int(
        input("Enter coordinates of square containing piece to move (file first): "))
    FinishSquare = try_int(
        input("Enter coordinates of square to move piece to (file first): "))
    return StartSquare, FinishSquare


@print_name
def MakeMove(Board, StartRank, StartFile, FinishRank, FinishFile, WhoseTurn):
    '''coordinator for move function'''
    if WhoseTurn == "W" and FinishRank == 1 and Board[StartRank][StartFile][1] == "R":
        Board[FinishRank][FinishFile] = "WK"
        Board[StartRank][StartFile] = "  "
    elif WhoseTurn == "B" and FinishRank == 8 and Board[StartRank][StartFile][1] == "R":
        Board[FinishRank][FinishFile] = "BM"
        Board[StartRank][StartFile] = "  "
    elif Board[StartRank][StartFile][1] == "K":
        # perform witch owner conversion
        Board[FinishRank][FinishFile] = "{0}{1}".format(Board[StartRank][StartFile][0],Board[FinishRank][FinishFile][1])
    else:
        Board[FinishRank][FinishFile] = Board[StartRank][StartFile]
        Board[StartRank][StartFile] = "  "


def run_test():
    myboard = CreateBoard()
    InitialiseBoard(myboard, "")

    fen = generate_fen(myboard)

    dec, turn = decode_fen(fen)

    assert dec == myboard # confirm that fen decodes correctly


if __name__ == "__main__":


    run_test()


    Board = CreateBoard()  # 0th index not used
    StartSquare = 0
    FinishSquare = 0
    PlayAgain = "Y"
    while PlayAgain == "Y":
        WhoseTurn = "W"
        GameOver = False
        SampleGame = str()
        while not SampleGame.isalpha():
            SampleGame = input("Do you wish to enter a fen string to start from? (Y/ N)")
        if SampleGame.lower().startswith("y"):
            fenStr = input("Please enter the fen string here:\n")
            Board, WhoseTurn = decode_fen(fenStr)
        else:
            SampleGame = str()
            while not SampleGame.isalpha():
                SampleGame = input("Do you want to play the sample game (enter Y for Yes)? ") # type: str
            SampleGame = SampleGame.upper()
            InitialiseBoard(Board, SampleGame)
        NoOfMoves = 0
        while not(GameOver):
            DisplayBoard(Board)
            DisplayWhoseTurnItIs(WhoseTurn)
            MoveIsLegal = False
            while not(MoveIsLegal):
                StartSquare, FinishSquare = GetMove(StartSquare, FinishSquare)
                StartRank = StartSquare % 10
                StartFile = StartSquare // 10
                FinishRank = FinishSquare % 10
                FinishFile = FinishSquare // 10
                MoveIsLegal = CheckMoveIsLegal(
                    Board, StartRank, StartFile, FinishRank, FinishFile, WhoseTurn)
                if not(MoveIsLegal):
                    print("That is not a legal move - please try again")
            NoOfMoves += 1

            GameOver = CheckIfGameWillBeWon(Board, FinishRank, FinishFile)
            MakeMove(Board, StartRank, StartFile,
                     FinishRank, FinishFile, WhoseTurn)

            print("The number of moves completed so far: {}".format(NoOfMoves))

            if GameOver:
                DisplayWinner(WhoseTurn)
            WhoseTurn = {"W":"B","B":"W"}[WhoseTurn]

            print("The current fen string is: {}".format(generate_fen(Board, WhoseTurn)))

        PlayAgain = str()
        while not PlayAgain.isalpha():
            PlayAgain = input("Do you want to play again (enter Y for Yes)? ") # type: str
        PlayAgain = PlayAgain.upper()
