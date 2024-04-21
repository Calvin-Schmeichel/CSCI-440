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
        self.adjacent_ticks = {}  # Tracks ticks adjacent to other creatures for reproduction

    def move(self, board):
        # Random walk logic
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        random.shuffle(directions)
        for dx, dy in directions:
            new_x, new_y = (self.x + dx) % board.size, (self.y + dy) % board.size
            if board.grid[new_x][new_y] == '*':  # Move only if the spot is empty
                board.grid[self.x][self.y] = '*'
                self.x, self.y = new_x, new_y
                self.update_position(board)
                return
        self.update_position(board)  # Update position even if not moved

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
        if self.grid[x][y] == '*':  # Ensure food is placed on an empty spot
            self.grid[x][y] = '@'
            self.food.append((x, y))

    def add_creature(self, creature):
        self.creatures.append(creature)
        creature.update_position(self)

    def reproduce_creatures(self):
        pairs = []
        for creature in self.creatures:
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = (creature.x + dx) % self.size, (creature.y + dy) % self.size
                neighbor = next((c for c in self.creatures if c.x == nx and c.y == ny), None)
                if neighbor and creature.gender != neighbor.gender:
                    key = frozenset({creature, neighbor})
                    if key in creature.adjacent_ticks:
                        creature.adjacent_ticks[key] += 1
                    else:
                        creature.adjacent_ticks[key] = 1
                    if creature.adjacent_ticks[key] >= 1 and creature.health > 50 and neighbor.health > 50:  # They've been adjacent for at least one tick
                        pairs.append((creature, neighbor))
        for creature, neighbor in pairs:
            new_x, new_y = random.choice([(creature.x, creature.y), (neighbor.x, neighbor.y)])
            if self.grid[new_x][new_y] == '*':  # Only spawn if spot is empty
                new_gender = 'M' if random.choice([True, False]) else 'F'
                new_creature = Creature(new_x, new_y, new_gender)
                new_creature.health = 50
                self.add_creature(new_creature)
                creature.health -= 25
                neighbor.health -= 25

    def print_board(self):
        clear_screen()
        for row in self.grid:
            print(''.join(row))
        print(f"Number of creatures: {len(self.creatures)}")

def main():
    board = Board(20)
    for _ in range(5):
        gender = 'M' if random.choice([True, False]) else 'F'
        while True:
            x, y = random.randint(0, 19), random.randint(0, 19)
            if board.grid[x][y] == '*':
                board.add_creature(Creature(x, y, gender))
                break

    tick = 0
    try:
        while True:
            if tick % 5 == 0:
                board.spawn_food()
            board.reproduce_creatures()  # Check and handle reproduction
            for creature in list(board.creatures):
                if not creature.update_health():
                    board.creatures.remove(creature)
                    board.grid[creature.x][creature.y] = '*'
                else:
                    creature.move(board)
            board.print_board()
            time.sleep(0.5)
            tick += 1
    except KeyboardInterrupt:
        print("Simulation stopped.")

if __name__ == "__main__":
    main()
