import pyxel
from time import sleep
from random import randint

WIDTH = 384
HEIGHT = 216

class SnakeCell():
    def __init__(self, direction, coordinates, sprite):
        self.direction = direction
        self.coordinates = coordinates
        self.sprite = sprite

class Game:
    def __init__(self):
        pyxel.init(WIDTH, HEIGHT, title="PySnake", fps=20)
        pyxel.load("src.pyxres")
        pyxel.fullscreen(True)

        self.food_coordinates = None
        self.food_sprite = None
        self.fullscreen = True

        self.reset()
        pyxel.run(self.update, self.draw)

    def reset(self):
        self.snake = [SnakeCell((1, 0), (6, 6), (24, 0)), SnakeCell((1, 0), (5, 6), (40, 0)), SnakeCell((1, 0), (4, 6), (40, 0))]
        self.score = 0
        self.death = False
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
            self.check_food()
            self.check_death()

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
            cell.sprite = self.sprite_snake(cell)

    def check_death(self):
        for cell in self.snake:
            if self.snake[0] != cell and self.snake[0].coordinates == cell.coordinates:
                self.kill_snake()

    def kill_snake(self):
        self.death = True
        self.snake[1].direction = self.snake[0].direction
        self.snake[1].sprite = self.sprite_snake(self.snake[0], dead=True)

    def feed_snake(self):
        self.snake.append(SnakeCell(self.snake[-1].direction, (self.snake[-1].coordinates[0] - self.snake[-1].direction[0], self.snake[-1].coordinates[1] - self.snake[-1].direction[1]), self.sprite_snake(self.snake[-1])))

    def sprite_snake(self, cell, dead=False):
        if cell == self.snake[0]:
            if dead:
                if cell.direction == (0, -1):
                    return (80, 0)
                elif cell.direction == (0, 1):
                    return (88, 0)
                elif cell.direction == (-1, 0):
                    return (96, 0)
                elif cell.direction == (1, 0):
                    return (104, 0)
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

    def generate_food(self):
        self.food_coordinates = (randint(0, 47), randint(0, 26))
        self.food_sprite = (randint(0, 3) * 8, 8)

    def check_food(self):
        for cell in self.snake:
            if cell.coordinates == self.food_coordinates:
                self.score += 1
                self.generate_food()
                self.feed_snake()
                break

    def draw(self):
        pyxel.cls(0)
        self.draw_food()
        self.draw_snake()
        pyxel.text(10, 10, f"Score is {self.score}", 7)

    def draw_snake(self):
        for cell in self.snake:
            pyxel.blt(cell.coordinates[0] * 8, cell.coordinates[1] * 8, 0, cell.sprite[0], cell.sprite[1], 8, 8)

    def draw_food(self):
        pyxel.blt(self.food_coordinates[0] * 8, self.food_coordinates[1] * 8, 0, self.food_sprite[0], self.food_sprite[1], 8, 8)

Game()
