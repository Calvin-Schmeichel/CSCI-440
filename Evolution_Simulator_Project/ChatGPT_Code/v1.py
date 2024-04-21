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
        # Implement logic to move towards food or randomly
        pass

    def update_health(self):
        self.health -= 1
        if self.health <= 0:
            return False
        return True

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
        self.update_position(creature)

    def update_position(self, creature):
        self.grid[creature.x][creature.y] = 'C' if creature.gender == 'M' else 'c'

    def print_board(self):
        clear_screen()
        for row in self.grid:
            print(''.join(row))
        print(f"Number of creatures: {len(self.creatures)}")

def main():
    board = Board(100)
    # Start with a few creatures
    for _ in range(5):
        gender = 'M' if random.choice([True, False]) else 'F'
        x, y = random.randint(0, 99), random.randint(0, 99)
        board.add_creature(Creature(x, y, gender))

    tick = 0
    try:
        while True:
            if tick % 10 == 0:
                board.spawn_food()
            for creature in board.creatures:
                if not creature.update_health():
                    board.creatures.remove(creature)
                    board.grid[creature.x][creature.y] = '*'
                else:
                    creature.move(board)
            board.print_board()
            time.sleep(1)
            tick += 1
    except KeyboardInterrupt:
        print("Simulation stopped.")

if __name__ == "__main__":
    main()