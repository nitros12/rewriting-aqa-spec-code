from .vec2d import Vec2D
from .piece import *

class Move(object):
    '''Represents a piece moving from one location to the other

    Attributes
    ----------

    piece : piece.Piece
        The piece object being moved

    board : board.GameBoard
        Board piece is being moved on

    start : vec2d.Vec2D
        Starting position of piece

    end : vec2d.Vec2D
        Ending position of piece


    '''
    def __init__(self, piece, board, start, end):
        self.piece = piece
        self.board = board
        self.start = start
        self.end = end

    def __str__(self):
        return "Move: (piece: {0.piece}, board: {0.board}, start: {0.start}, end: {0.end} (valid: {0.valid_bool}, take: {0.taken}))".format(self)

    @property
    def valid(self):
        return self.piece.validate_move(self.board, self)

    @property
    def valid_bool(self):
        """Like move.valid, but designed for when you need boolean output (no exceptions)"""
        return bool(self.piece.validate_move(self.board, self))

    @property
    def taken(self):
        """returns:
        chess_game.take if can take validly"""
        try:
            return self.piece.test_take(self.board, self) if self.valid else False
        except Exception as e:
            return False

    def run_move(self):
        if self.valid:
            self.piece.location = self.end

class GameState(object):
    '''Stores current game state'''
    def __init__(self):
        self.turn = teams.white
        self.white_takes = 0
        self.black_takes = 0
        self.turns = 0
        self.in_check = {teams.white:False, teams.black:False}

    def __str__(self):
        return "game_state: (Turn: {0.turn}, white_takes: {0.white_takes}, black_takes: {0.black_takes}, Turns completed: {0.turns})".format(self)

    def swap_turn(self):
        self.turn = {"W":"B", "B":"W"}[self.turn]

    def inc_turns(self):
        self.turns += 1

    def add_take(self):
        if self.turn == "W":
            self.white_takes  += 1
        else:
            self.black_takes += 1


class GameBoard(object):
    '''holds game objects
    game is run from here



    Attributes
    ----------

    name : str
        name of board

    game_size_x game_size_y : int
        dimentions of game board'''
    def __init__(self, name: str, game_size_x, game_size_y):
        self.name = name
        self.pieces = []
        self.state = GameState()
        self.game_size = Vec2D(game_size_x, game_size_y)

    def __str__(self):
        return "Board: (name: {0.name}, state: {0.state}, pieces: {1})".format(self, ', '.join([str(i) for i in self.pieces]))

    def set_pieces(self, pieces):
        self.pieces = pieces

    def add_pieces(self, *pieces):
        for piece in pieces:
            self.pieces.append(piece)

    def remove_piece(self, piece):
        self.pieces.remove(piece)

    def check_pieces(self, *locations):
        return list(filter(lambda x: x.check_self_locations(*locations), self.pieces))

    def find_piece(self, location):
        pieces = self.check_pieces(location)
        if len(pieces) > 1:
            raise Exception("multiple pieces occupy same location: {0}: [{1}]".format(location, ', '.join(pieces)))
        elif pieces:
            return pieces[0]
        else:
            return

    def find_by_type(self, piece_type):
        return list(filter(lambda x: x.test_self_type(piece_type), self.pieces))

    def find_by_owner(self, owner, invert=False):
        return list(filter(lambda x: invert ^ x.test_owner(owner), self.pieces))
        # getting in the cheeky xor operator

    def construct_move(self, piece, start, end):
        return Move(piece, self, start, end)

    def run_take(self, take):
        print("took piece: {}".format(take.taken))
        self.state.add_take()
        self.remove_piece(take.taken)

    def test_win(self):
        windict = {teams.white:False, teams.black:False}
        for i in self.find_by_type(piece.King):
            for j in self.find_by_owner(i.owner, invert=True):
                testing_move = self.construct_move(j, piece.location, i.location)
                if testing_move.valid:
                    windict[j.owner] = True



    def run_game(self):
        '''Run one game move'''
        while True:
            while True:
                if not self.state.in_check[self.state.turn]:
                    start = wait_for_valid("Piece to move (in format: x,y): ", lambda x: len(x.split(",")) == 2,
                                       lambda x: Vec2D(*[int(i.strip()) for i in x.split(",")]))
                                       # grab piece
                    piece = self.find_piece(start)
                else:
                    piece = self.find_by_type(piece.King)[0]
                    print("{} is in check, so their king at {} was automatically selected".format(piece.owner, piece.location))
                if not piece:
                    print("there was no piece there, please enter a valid piece!")
                elif not piece.test_owner(self.state.turn):
                    print("You cannot move a piece that is owned by an enemy")
                else:
                    break
            print("picked piece: {}".format(piece))
            end = wait_for_valid("Place to move to: (in format x,y): ", lambda x: len(x.split(",")) == 2,
                                 lambda x: Vec2D(*[int(i.strip()) for i in x.split(",")]))
            move_piece = self.construct_move(piece, start, end)
            print(move_piece)
            if move_piece.valid:
                    break
            elif isinstance(move_piece.valid, piece.GameException):
                print(move_piece.valid)
            elif isinstance(move_piece.valid, piece.KingInCheck):
                print("{0.king} King is in check from piece: {0.taker}, {0.king.owner} must move the king their turn!".format(move_piece.valid))
                self.state.in_check[move_piece.king.owner] = True
        if move_piece.taken:
            self.run_take(move_piece.taken)
        move_piece.run_move()
        self.state.inc_turns()
        self.state.swap_turn()

    def check_board(self):
        return True, ''  # Todo: work on this

    def game_iter(self):
        while True:
            self.run_game()
            state, msg = self.check_board()
            if not state:
                print(msg)





def wait_for_valid(question :str, test=(lambda x: x), formatter=(lambda x: x)):
    temp = ""
    while not test(temp):
        temp = input(question)
    return formatter(temp)
