class Board:
    '''Class representing the Tic-Tac-Toe board'''
    BOARD_SIDE = 3
    EMPTY_SYMBOL = " "

    def __init__(self):
        '''Initialize blank board'''
        self.play_area = [[self.EMPTY_SYMBOL for _ in range(self.BOARD_SIDE)]
                          for _ in range(self.BOARD_SIDE)]

    def printBoard(self):
        '''Print the current board state'''
        header_line = "|R\\C| "
        for col_number in range(self.BOARD_SIDE):
            header_line += str(col_number) + " | "
        print(header_line)
        separator = "-" * len(header_line)
        print(separator)
        for r in range(self.BOARD_SIDE):
            row_str = "| " + str(r) + " | "
            for c in range(self.BOARD_SIDE):
                row_str += self.play_area[r][c] + " | "
            print(row_str)
            print(separator)


class Game:
    '''Class managing the Tic-Tac-Toe game logic'''
    def __init__(self):
        '''Initialize game with empty board and starting player'''
        self.board = Board()
        self.turn = 'X'

    def switchPlayer(self):
        '''Switch current player'''
        self.turn = 'O' if self.turn == 'X' else 'X'

    def validateEntry(self, row, col):
        '''Returns True if row and col are valid AND cell is empty'''
        if row < 0 or row >= self.board.BOARD_SIDE:
            return False
        if col < 0 or col >= self.board.BOARD_SIDE:
            return False
        if self.board.play_area[row][col] != self.board.EMPTY_SYMBOL:
            return False
        return True

    def checkFull(self):
        '''Returns True if no empty spot'''
        for r in range(self.board.BOARD_SIDE):
            for c in range(self.board.BOARD_SIDE):
                if self.board.play_area[r][c] == self.board.EMPTY_SYMBOL:
                    return False
        return True

    def checkWin(self, mark):
        '''Returns True if the given mark has won'''
        b = self.board.play_area
        S = self.board.BOARD_SIDE
        for r in range(S):
            if all(b[r][c] == mark for c in range(S)):
                return True
        for c in range(S):
            if all(b[r][c] == mark for r in range(S)):
                return True
        if all(b[i][i] == mark for i in range(S)):
            return True
        if all(b[i][S - 1 - i] == mark for i in range(S)):
            return True
        return False


    def minimaxMove(self):
        '''Determine the best move for 'O' using a simple strategy'''
        # Try to win
        for r in range(self.board.BOARD_SIDE):
            for c in range(self.board.BOARD_SIDE):
                if self.board.play_area[r][c] == self.board.EMPTY_SYMBOL:
                    self.board.play_area[r][c] = 'O'
                    if self.checkWin('O'):
                        return (r, c)
                    self.board.play_area[r][c] = self.board.EMPTY_SYMBOL

        # Block X if about to win
        for r in range(self.board.BOARD_SIDE):
            for c in range(self.board.BOARD_SIDE):
                if self.board.play_area[r][c] == self.board.EMPTY_SYMBOL:
                    self.board.play_area[r][c] = 'X'
                    if self.checkWin('X'):
                        self.board.play_area[r][c] = self.board.EMPTY_SYMBOL
                        return (r, c)
                    self.board.play_area[r][c] = self.board.EMPTY_SYMBOL

        # Otherwise, pick first empty cell
        for r in range(self.board.BOARD_SIDE):
            for c in range(self.board.BOARD_SIDE):
                if self.board.play_area[r][c] == self.board.EMPTY_SYMBOL:
                    return (r, c)
        return (-1, -1)  # fallback if board full


    def playGame(self):
        '''Main game loop'''
        print("New Game: X (You) goes first.\n")
        self.board.printBoard()

        while True:
            if self.turn == 'X':
                entry = input("\nYour turn (X). Enter row,col: ")
                try:
                    row_str, col_str = entry.split(',')
                    row = int(row_str.strip())
                    col = int(col_str.strip())
                except:
                    print("Invalid input. Try again.")
                    continue

                if not self.validateEntry(row, col):
                    print("Invalid move. Try again.")
                    continue

                self.board.play_area[row][col] = 'X'

            else:
                print("\nComputer (O) is thinking...")
                r, c = self.minimaxMove()
                self.board.play_area[r][c] = 'O'

            self.board.printBoard()

            if self.checkWin(self.turn):
                print(f"\n{self.turn} WINS!")
                break
            if self.checkFull():
                print("\nDRAW! NOBODY WINS!")
                break

            self.switchPlayer()

        reply = input("\nPlay again? (y/n): ")
        if reply.lower() == 'y':
            self.__init__()
            self.playGame()
        else:
            print("Thanks for playing!")


if __name__ == "__main__":
    '''Main function to start the game'''
    game = Game()
    game.playGame()
