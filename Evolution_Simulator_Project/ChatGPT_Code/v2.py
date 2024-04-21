import random
import time
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

class Creature:
    def __init__(self, x, y, gender):
        self.x = x
        self.y = y
        self.health = 100
        self.gender = gender  # 'M' for male, 'F' for female

    def move(self, board):
        # Simple random walk logic, could be improved towards goal-oriented movement
        dx, dy = random.choice([(0, 1), (1, 0), (0, -1), (-1, 0)])
        new_x, new_y = (self.x + dx) % board.size, (self.y + dy) % board.size
        if board.grid[new_x][new_y] == '@':  # Eat food if on food spot
            self.health += 50
            board.food.remove((new_x, new_y))  # Remove food from list
        board.grid[self.x][self.y] = '*'
        self.x, self.y = new_x, new_y
        self.update_position(board)

    def update_health(self):
        self.health -= 1
        if self.health <= 0:
            return False
        return True

    def update_position(self, board):
        board.grid[self.x][self.y] = 'C' if self.gender == 'M' else 'c'

class Board:
    def __init__(self, size):
        self.size = size
        self.grid = [['*' for _ in range(size)] for _ in range(size)]
        self.creatures = []
        self.food = []

    def spawn_food(self):
        x, y = random.randint(0, self.size-1), random.randint(0, self.size-1)
        self.grid[x][y] = '@'
        self.food.append((x, y))

    def add_creature(self, creature):
        self.creatures.append(creature)
        creature.update_position(self)

    def print_board(self):
        clear_screen()
        for row in self.grid:
            print(''.join(row))
        print(f"Number of creatures: {len(self.creatures)}")

def main():
    board = Board(20)  # Reduced board size
    # Start with a few creatures
    for _ in range(5):
        gender = 'M' if random.choice([True, False]) else 'F'
        x, y = random.randint(0, 19), random.randint(0, 19)
        board.add_creature(Creature(x, y, gender))

    tick = 0
    try:
        while True:
            if tick % 5 == 0:  # Adjust food spawn rate for faster ticks
                board.spawn_food()
            for creature in list(board.creatures):  # Iterate over a copy to manage removals
                if not creature.update_health():
                    board.creatures.remove(creature)
                    board.grid[creature.x][creature.y] = '*'
                else:
                    creature.move(board)
            board.print_board()
            time.sleep(0.5)  # Adjusted for 2 ticks per second
            tick += 1
    except KeyboardInterrupt:
        print("Simulation stopped.")

if __name__ == "__main__":
    main()