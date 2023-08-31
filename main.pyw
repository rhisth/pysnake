import pyxel
from time import sleep
from random import randint, choice

WIDTH = 384
HEIGHT = 216

class Object():
    def __init__(self, coordinates, sprite):
        self.coordinates = coordinates
        self.sprite = sprite

class SnakeCell():
    def __init__(self, coordinates, direction, sprite):
        Object.__init__(self, coordinates, sprite)
        self.direction = direction

class Game:
    def __init__(self):
        with open("assets/icon.txt") as file:
            icon = file.read().splitlines()
        pyxel.init(WIDTH, HEIGHT, title="PySnake", fps=10)
        pyxel.load("assets/src.pyxres")
        pyxel.icon(icon, 4)
        pyxel.fullscreen(True)

        self.fullscreen = True

        self.reset()
        self.feed_snake()
        self.feed_snake()
        pyxel.run(self.update, self.draw)

    def reset(self):
        self.snake = [SnakeCell((6, 6), (1, 0), (24, 0)), SnakeCell((5, 6), (1, 0), (40, 0)), SnakeCell((4, 6), (1, 0), (40, 0))]
        self.death = False
        self.food = Object(None, None)
        self.map_variant = randint(1, 2)
        self.score = 0
        self.generate_map()
        self.generate_walls()
        self.generate_food()

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if pyxel.btnp(pyxel.KEY_R):
            self.reset()

        if pyxel.btnp(pyxel.KEY_F11):
            self.fullscreen = not self.fullscreen
            pyxel.fullscreen(self.fullscreen)

        if not self.death:
            self.update_direction()
            self.update_snake()
            self.check_death()
            self.check_food()

    def update_direction(self):
        if pyxel.btnp(pyxel.KEY_UP):
            if self.snake[0].direction != (0, 1):
                self.snake[0].direction = (0, -1)
        elif pyxel.btnp(pyxel.KEY_DOWN):
            if self.snake[0].direction != (0, -1):
                self.snake[0].direction = (0, 1)
        elif pyxel.btnp(pyxel.KEY_LEFT):
            if self.snake[0].direction != (1, 0):
                self.snake[0].direction = (-1, 0)
        elif pyxel.btnp(pyxel.KEY_RIGHT):
            if self.snake[0].direction != (-1, 0):
                self.snake[0].direction = (1, 0)

    def update_snake(self):
        for cell in self.snake:
            cell.coordinates = ((cell.coordinates[0] + cell.direction[0]) % (WIDTH / 8), (cell.coordinates[1] + cell.direction[1]) % (HEIGHT / 8))

        last_direction = self.snake[0].direction
        for cell in self.snake:
            cell_direction = cell.direction
            cell.direction = last_direction
            last_direction = cell_direction

        for cell in self.snake:
            cell.sprite = self.get_sprite(cell)

        for index, cell in enumerate(self.snake[::-1]):
            if cell == self.snake[0]:
                continue
            next_cell = self.snake[::-1][index + 1]
            if cell.direction == (0, -1):
                if next_cell.direction == (1, 0):
                    next_cell.sprite = (80, 0)
                elif next_cell.direction == (-1, 0):
                    next_cell.sprite = (88, 0)
            elif cell.direction == (0, 1):
                if next_cell.direction == (1, 0):
                    next_cell.sprite = (96, 0)
                elif next_cell.direction == (-1, 0):
                    next_cell.sprite = (104, 0)
            elif cell.direction == (-1, 0):
                if next_cell.direction == (0, -1):
                    next_cell.sprite = (96, 0)
                elif next_cell.direction == (0, 1):
                    next_cell.sprite = (80, 0)
            elif cell.direction == (1, 0):
                if next_cell.direction == (0, -1):
                    next_cell.sprite = (104, 0)
                elif next_cell.direction == (0, 1):
                    next_cell.sprite = (88, 0)

    def check_death(self):
        for cell in self.snake:
            if self.snake[0] != cell and self.snake[0].coordinates == cell.coordinates:
                self.kill_snake()
                break

        for wall in self.walls:
            if self.snake[0].coordinates == wall.coordinates:
                self.kill_snake()
                break

    def check_food(self):
        if self.snake[0].coordinates == self.food.coordinates:
            self.score += 1
            self.generate_food()
            self.feed_snake()

    def kill_snake(self):
        self.death = True
        self.snake[1].direction = self.snake[0].direction
        self.snake[1].sprite = self.get_sprite(self.snake[0], dead=True)
        self.snake.pop(0)

    def feed_snake(self):
        coordinates = (self.snake[-1].coordinates[0] - self.snake[-1].direction[0], self.snake[-1].coordinates[1] - self.snake[-1].direction[1])
        direction = self.snake[-1].direction
        sprite = self.get_sprite(self.snake[-1])
        self.snake.append(SnakeCell(coordinates, direction, sprite))

    def get_sprite(self, cell, dead=False):
        if cell == self.snake[0]:
            if dead:
                if cell.direction == (0, -1):
                    return (48, 0)
                elif cell.direction == (0, 1):
                    return (56, 0)
                elif cell.direction == (-1, 0):
                    return (64, 0)
                elif cell.direction == (1, 0):
                    return (72, 0)
            else:
                if cell.direction == (0, -1):
                    return (0, 0)
                elif cell.direction == (0, 1):
                    return (8, 0)
                elif cell.direction == (-1, 0):
                    return (16, 0)
                elif cell.direction == (1, 0):
                    return (24, 0)
        else:
            if cell.direction == (0, 1) or cell.direction == (0, -1):
                return (32, 0)
            elif cell.direction == (1, 0) or cell.direction == (-1, 0):
                return (40, 0)

    def get_available_space(self):
        list = []
        for i in range(int(HEIGHT / 8)):
            for j in range(int(WIDTH / 8)):
                coordinates = (j, i)
                list.append(coordinates)
        for cell in self.snake:
            list.remove(cell.coordinates)
        for wall in self.walls:
            list.remove(wall.coordinates)
        return list

    def generate_map(self):
        self.map = []
        for i in range(int(HEIGHT / 8)):
            list = []
            for j in range(int(WIDTH / 8)):
                if randint(1, 10) < 10:
                    tile = (0, self.map_variant * 8)
                else:
                    tile = (randint(1, 3) * 8, self.map_variant * 8)
                list.append(tile)
            self.map.append(list)

    def generate_walls(self):
        self.walls = []
        space = self.get_available_space()
        for i in range(20):
            coordinates = choice(space)
            sprite = (randint(8, 11) * 8, self.map_variant * 8)
            self.walls.append(Object(coordinates, sprite))
            space.remove(coordinates)

    def generate_food(self):
        self.food.coordinates = choice(self.get_available_space())
        self.food.sprite = (randint(4, 7) * 8, self.map_variant * 8)

    def draw(self):
        pyxel.cls(0)
        self.draw_map()
        self.draw_food()
        self.draw_snake()
        self.draw_walls()
        self.draw_score()

    def draw_map(self):
        x = -1
        y = -1
        for list in self.map:
            y += 1
            for tile in list:
                x += 1
                pyxel.blt(x * 8, y * 8, 0, tile[0], tile[1], 8, 8)
            x = -1

    def draw_food(self):
        pyxel.blt(self.food.coordinates[0] * 8, self.food.coordinates[1] * 8, 0, self.food.sprite[0], self.food.sprite[1], 8, 8)

    def draw_snake(self):
        for cell in self.snake:
            pyxel.blt(cell.coordinates[0] * 8, cell.coordinates[1] * 8, 0, cell.sprite[0], cell.sprite[1], 8, 8)

    def draw_walls(self):
        for wall in self.walls:
            pyxel.blt(wall.coordinates[0] * 8, wall.coordinates[1] * 8, 0, wall.sprite[0], wall.sprite[1], 8, 8)

    def draw_score(self):
        pyxel.text(10, 10, f"Score is {self.score}", 0)

Game()
