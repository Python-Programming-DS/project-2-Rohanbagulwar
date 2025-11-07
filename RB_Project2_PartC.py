import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

#  Board Class 
class Board:

    BOARD_SIDE = 3
    EMPTY_SYMBOL = " "

    def __init__(self):
        ''' Initialize blank board '''
        self.play_area = [[self.EMPTY_SYMBOL for _ in range(self.BOARD_SIDE)]
                          for _ in range(self.BOARD_SIDE)]

    def printBoard(self):
        ''' Print the current state of the board '''
        # Print column headers
        header_line = "|R\\C| "
        for col_number in range(self.BOARD_SIDE):
            header_line += str(col_number) + " | "
        print(header_line)

        # Separator
        separator = "-" * len(header_line)
        print(separator)

        # Print rows with indices
        for row_number in range(self.BOARD_SIDE):
            line_print = "| " + str(row_number) + " | "
            for col_number in range(self.BOARD_SIDE):
                line_print += self.play_area[row_number][col_number] + " | "
            print(line_print)
            print(separator)


#  Game Class
class Game:

    def __init__(self, model):
        ''' Initialize game with board and ML model '''
        self.board = Board()
        self.turn = "X"  # Human goes first
        self.model = model  # ML model for AI moves

    def switchPlayer(self):
        ''' Switch current player '''
        self.turn = "O" if self.turn == "X" else "X"

    def validateEntry(self, row, col):
        ''' Validate if the move at (row, col) is valid '''
        if 0 <= row < self.board.BOARD_SIDE and 0 <= col < self.board.BOARD_SIDE:
            if self.board.play_area[row][col] == self.board.EMPTY_SYMBOL:
                return True
        return False

    def checkFull(self):
        ''' Check if the board is full '''
        for r in range(self.board.BOARD_SIDE):
            for c in range(self.board.BOARD_SIDE):
                if self.board.play_area[r][c] == self.board.EMPTY_SYMBOL:
                    return False
        return True

    def checkWin(self, mark):
        ''' Check if the current player with 'mark' has won '''
        b = self.board.play_area
        SIDE = self.board.BOARD_SIDE

        # Rows
        for r in range(SIDE):
            if all(b[r][c] == mark for c in range(SIDE)):
                return True

        # Columns
        for c in range(SIDE):
            if all(b[r][c] == mark for r in range(SIDE)):
                return True

        # Diagonals
        if all(b[i][i] == mark for i in range(SIDE)):
            return True
        if all(b[i][SIDE - 1 - i] == mark for i in range(SIDE)):
            return True

        return False

    # AI Move Using ML Model
    def aiMove(self):
        ''' AI makes a move based on the trained ML model '''
        # Convert board to ML input format: 1=X, -1=O, 0=empty
        flat_board = []
        for r in range(3):
            for c in range(3):
                if self.board.play_area[r][c] == "X":
                    flat_board.append(1)
                elif self.board.play_area[r][c] == "O":
                    flat_board.append(-1)
                else:
                    flat_board.append(0)

        # Predict best move index
        best_move_index = self.model.predict([flat_board])[0]
        row, col = divmod(best_move_index, 3)

        # Make sure the cell is empty (fallback if model predicts occupied cell)
        if self.board.play_area[row][col] == self.board.EMPTY_SYMBOL:
            self.board.play_area[row][col] = "O"
        else:
            for r in range(3):
                for c in range(3):
                    if self.board.play_area[r][c] == self.board.EMPTY_SYMBOL:
                        self.board.play_area[r][c] = "O"
                        return

    # Game Loop
    def playGame(self):
        ''' Main game loop '''
        print("New Game: X (You) goes first.\n")
        self.board.printBoard()

        while True:
            if self.turn == "X":
                # Human move
                user_move = input(
                    f"\n{self.turn}'s turn.\nEnter row,col (e.g. 1,2): "
                )
                try:
                    row_str, col_str = user_move.split(",")
                    row_input = int(row_str.strip())
                    col_input = int(col_str.strip())
                except:
                    print("Invalid input format. Try again.")
                    continue

                if not self.validateEntry(row_input, col_input):
                    print("Invalid move. Try again.")
                    continue

                self.board.play_area[row_input][col_input] = "X"

            else:
                # AI move
                print("\nComputer (O) is thinking...")
                self.aiMove()

            # Print board
            self.board.printBoard()

            # Check win/draw
            if self.checkWin(self.turn):
                print(f"\n{self.turn} IS THE WINNER!!!")
                break
            if self.checkFull():
                print("\nDRAW! NOBODY WINS!")
                break

            # Switch turn
            self.switchPlayer()

        reply = input("\nAnother game? Enter Y or y for yes.\n")
        if reply.lower() == "y":
            self.__init__(self.model)
            self.playGame()
        else:
            print("Thank you for playing!")


#  Main 
if __name__ == "__main__":
    ''' Main function to train model and start game '''
    # Load dataset
    data = pd.read_csv("tictac_single.txt", header=None, sep=" ")
    X = data.iloc[:, :9]
    y = data.iloc[:, 9]

    # Train model
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Start game
    game_instance = Game(model)
    game_instance.playGame()
