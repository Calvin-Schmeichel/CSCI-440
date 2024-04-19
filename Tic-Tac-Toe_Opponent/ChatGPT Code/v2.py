import tkinter as tk
import random

def check_winner():
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] != None:
            return board[row][0]
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != None:
            return board[0][col]
    if board[0][0] == board[1][1] == board[2][2] != None:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != None:
        return board[2][0]
    if all(all(row) for row in board):
        return 'Draw'
    return None

def on_click(row, col):
    global player, winner
    if board[row][col] is None and winner is None:
        board[row][col] = player
        if player == 'X':
            buttons[row][col].config(text='X', fg='blue')
            player = 'O'
        else:
            buttons[row][col].config(text='O', fg='red')
            player = 'X'
        winner = check_winner()
        if winner:
            label.config(text=f'{winner} wins!')
        elif player == 'O':
            ai_move()

def ai_move():
    global player, winner
    if winner is None:
        move = find_winning_move('O')
        if move:
            row, col = move
        else:
            empty_cells = [(r, c) for r in range(3) for c in range(3) if board[r][c] is None]
            if empty_cells:
                row, col = random.choice(empty_cells)
        board[row][col] = 'O'
        buttons[row][col].config(text='O', fg='red')
        winner = check_winner()
        if winner:
            label.config(text=f'{winner} wins!')
        player = 'X'

def find_winning_move(player):
    for r in range(3):
        for c in range(3):
            if board[r][c] is None:
                board[r][c] = player
                if check_winner() == player:
                    board[r][c] = None
                    return (r, c)
                board[r][c] = None
    return None

def reset_game():
    global board, winner, player
    board = [[None]*3 for _ in range(3)]
    for row in range(3):
        for col in range(3):
            buttons[row][col].config(text='', fg='black')
    winner = None
    player = random.choice(['X', 'O'])  # Randomly choose who starts
    if player == 'O':
        ai_move()  # If AI starts, make the first move
    label.config(text=f"Player {player}'s turn")

app = tk.Tk()
app.title('Tic Tac Toe')
player = 'X'  # Default start player, will be reset immediately
winner = None
board = [[None]*3 for _ in range(3)]

buttons = [[None]*3 for _ in range(3)]
for row in range(3):
    for col in range(3):
        button = tk.Button(app, text='', font=('normal', 40), width=5, height=2,
                           command=lambda r=row, c=col: on_click(r, c))
        button.grid(row=row, column=col)
        buttons[row][col] = button

reset_button = tk.Button(app, text='Reset', command=reset_game)
reset_button.grid(row=3, column=1)

label = tk.Label(app, text="Player X's turn")
label.grid(row=3, column=0, columnspan=3)

reset_game()  # Initialize game with random starter
app.mainloop()
