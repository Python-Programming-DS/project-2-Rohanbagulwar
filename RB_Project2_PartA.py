class Board:
    ''' Tic-Tac-Toe Board Class '''
    BOARD_SIDE = 3
    EMPTY_SYMBOL = " "

    def __init__(self):
        ''' Initialize blank board '''
        # Initialize blank board
        self.play_area = [[self.EMPTY_SYMBOL for _ in range(self.BOARD_SIDE)]
                          for _ in range(self.BOARD_SIDE)]

    def printBoard(self):
        ''' Print the current state of the board '''
        # print column headers
        header_line = "|R\\C| "
        for col_number in range(self.BOARD_SIDE):
            header_line += str(col_number) + " | "
        print(header_line)

        separator = "-" * len(header_line)
        print(separator)

        # print each row
        for r in range(self.BOARD_SIDE):
            row_str = "| " + str(r) + " | "
            for c in range(self.BOARD_SIDE):
                row_str += self.play_area[r][c] + " | "
            print(row_str)
            print(separator)


class Game:
    ''' Tic-Tac-Toe Game Class '''
    def __init__(self):
        ''' Initialize game with board and starting player '''
        self.board = Board()
        self.turn = 'X'

    def switchPlayer(self):
        ''' Switch current player '''
        # Switch current player
        self.turn = 'O' if self.turn == 'X' else 'X'

    def validateEntry(self, row, col):
        ''' Validate if the move at (row, col) is valid '''
        # Returns True if row and col are valid AND cell is empty
        if row < 0 or row >= self.board.BOARD_SIDE:
            return False
        if col < 0 or col >= self.board.BOARD_SIDE:
            return False
        if self.board.play_area[row][col] != self.board.EMPTY_SYMBOL:
            return False
        return True

    def checkFull(self):
        ''' Check if the board is full '''
        # Returns True if no empty spot
        for r in range(self.board.BOARD_SIDE):
            for c in range(self.board.BOARD_SIDE):
                if self.board.play_area[r][c] == self.board.EMPTY_SYMBOL:
                    return False
        return True

    def checkWin(self):
        ''' Check if current player has won '''
        mark = self.turn
        SIDE = self.board.BOARD_SIDE
        b = self.board.play_area

        # Check rows
        for r in range(SIDE):
            if all(b[r][c] == mark for c in range(SIDE)):
                return True

        # Check columns
        for c in range(SIDE):
            if all(b[r][c] == mark for r in range(SIDE)):
                return True

        # Major diagonal
        if all(b[i][i] == mark for i in range(SIDE)):
            return True

        # Minor diagonal
        if all(b[i][SIDE - 1 - i] == mark for i in range(SIDE)):
            return True

        return False

    def checkEnd(self):
        ''' Check if the game has ended '''
        # Game ends if someone wins or board is full
        if self.checkWin():
            return True
        if self.checkFull():
            return True
        return False

    def playGame(self):
        ''' Main game loop '''
        print("New Game: X goes first.\n")
        self.board.printBoard()

        while True:
            print(f"\n{self.turn}'s turn.")
            entry = input("Enter row and column separated by comma (e.g. 1,2): ")

            try:
                row_str, col_str = entry.split(',')
                row = int(row_str.strip())
                col = int(col_str.strip())
            except:
                print("Invalid input. Try again.")
                continue

            if not self.validateEntry(row, col):
                print("Invalid move or cell already occupied. Try again.")
                continue

            # Place mark
            self.board.play_area[row][col] = self.turn
            self.board.printBoard()

            # Check if game ended
            if self.checkWin():
                print(f"\n{self.turn} IS THE WINNER!!!")
                break
            if self.checkFull():
                print("\nDRAW! NOBODY WINS!")
                break

            # Switch turn to next player
            self.switchPlayer()

        reply = input("\nAnother game? Enter Y/y to play again: ")
        if reply.lower() == 'y':
            self.__init__()
            self.playGame()
        else:
            print("Thank you for playing!")


if __name__ == "__main__":
    
    game = Game()
    game.playGame()
