import tkinter as tk

class TicTacToe:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tic Tac Toe")
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'

        # Create buttons
        self.buttons = [[tk.Button(self.window, text='', command=lambda row=row, col=col: self.click(row, col), height=3, width=6) for col in range(3)] for row in range(3)]
        for row in range(3):
            for col in range(3):
                self.buttons[row][col].grid(row=row, column=col)

    def click(self, row, col):
        if self.board[row][col] == '' and not self.check_winner():
            self.buttons[row][col]['text'] = self.current_player
            self.board[row][col] = self.current_player
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            if self.check_winner():
                print(f"Player {self.check_winner()} wins!")

    def check_winner(self):
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != '':
                return self.board[i][0]
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != '':
                return self.board[0][i]
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != '':
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != '':
            return self.board[0][2]
        return None

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    game = TicTacToe()
    game.run()
