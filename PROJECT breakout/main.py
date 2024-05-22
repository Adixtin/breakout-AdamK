import os
import time

DT = 0.05


class Map:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

        self.cache: list[list[str]]

    def clear(self):
        self.cache = []

        char = "X"

        self.cache.append([char] * (self.y + 2))

        for _ in range(self.x):
            self.cache.append([char] + self.y * [" "] + [char])

        self.cache.append([char] * (self.y + 2))

    def set_char(self, x, y, char):
        self.cache[x + 1][y + 1] = char

    def __repr__(self) -> str:
        napis = ""
        for row in range(self.y + 2):
            row_napis = ""

            for column in range(self.x + 2):
                row_napis += self.cache[column][row]

            napis += row_napis + "\n"

        return napis


class Ball:
    def __init__(self) -> None:
        self.accY = 0

        self.speedX = 0
        self.speedY = 0

        self.posX = 0
        self.posY = 0

    def draw_on(self, map: Map):
        map.set_char(int(self.posX), int(self.posY), "O")

    def advance_position(self):
        self.speedY += self.accY * DT

        self.posX += self.speedX * DT
        self.posY += self.speedY * DT

    def calculate_collision(self, map: Map):
        has_collision = False

        x_za_chwilę = self.posX + self.speedX * DT
        if x_za_chwilę > map.x or x_za_chwilę < 0:
            self.speedX *= -1
            has_collision = True

        y_za_chwilę = self.posY + self.speedY * DT
        if y_za_chwilę > map.y or y_za_chwilę < 0:
            self.speedY *= -1
            has_collision = True

        return has_collision


m = Map(15, 15)
b = Ball()
b.accY = 10

while True:
    m.clear()

    if not b.calculate_collision(m):
        b.advance_position()
    b.draw_on(m)

    os.system("clear")
    print(m)

    time.sleep(DT)
