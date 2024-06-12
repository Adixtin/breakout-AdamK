import os
import time
import sys
import keyboard

DT = 0.05
HIGH_SCORE_FILE = "highscores.txt"


class Map:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.cache = []

    def clear(self):
        self.cache = []
        self.cache.append(["■"] * (self.width + 2))
        for _ in range(self.height):
            self.cache.append(["■"] + [" "] * self.width + ["■"])
        self.cache.append(["■"] * (self.width + 2))

    def set_char(self, x, y, char):
        self.cache[y + 1][x + 1] = char

    def __repr__(self) -> str:
        return "\n".join("".join(row) for row in self.cache) + "\n"


class Ball:
    def __init__(self, posX, posY, speedX, speedY) -> None:
        self.speedX = speedX
        self.speedY = speedY
        self.posX = posX
        self.posY = posY

    def draw_on(self, map: Map):
        map.set_char(round(self.posX), round(self.posY), "⬤")

    def advance_position(self):
        self.posX += self.speedX * DT
        self.posY += self.speedY * DT

    def calculate_collision(self, map: Map, paddle, bricks, points):
        x_next = int(self.posX + self.speedX * DT)
        y_next = int(self.posY + self.speedY * DT)
        max_speed = 5

        if x_next >= map.width - 2 or x_next < 1:
            self.speedX *= -1
        if y_next < 0:
            self.speedY *= -1
        if y_next >= map.height - 1:
            print("Game Over")
            print(f"Final Score: {points}")
            update_high_scores(points)
            print_high_scores()
            sys.exit()

        if y_next == paddle.posY and paddle.posX <= x_next < paddle.posX + paddle.width:
            paddle_center = paddle.posX + paddle.width / 2
            relative_position = (
                self.posX - paddle_center) / (paddle.width / 2)
            self.speedX = relative_position * max_speed
            self.speedY *= -1

        for brick in bricks:
            if brick.collide_with_ball(self):
                points += 1
                break

        return points


class Paddle:
    def __init__(self, width, posX, posY) -> None:
        self.width = width
        self.posX = posX
        self.posY = posY

    def draw_on(self, map: Map):
        for i in range(self.width):
            map.set_char(self.posX + i, self.posY, "=")

    def move_left(self):
        if self.posX > 0:
            self.posX -= 1

    def move_right(self, map: Map):
        if self.posX + self.width < map.width:
            self.posX += 1


class Brick:
    def __init__(self, posX, posY) -> None:
        self.posX = posX
        self.posY = posY
        self.active = True

    def draw_on(self, map: Map):
        if self.active:
            # You can use a different character here
            map.set_char(self.posX, self.posY, "🝙")

    def collide_with_ball(self, ball: Ball):
        if not self.active:
            return False

        # Store y-coordinate before update (for bottom collision)
        ball_y = int(ball.posY)
        # Adjust tolerance for floating-point errors (optional)
        EPSILON = 0.001

        # Check all four sides of the brick for collision
        if (self.posX <= ball.posX < self.posX + 2 and (abs(ball_y - self.posY) < EPSILON or ball_y == self.posY)) or \
           (self.posX <= ball.posX < self.posX + 2 and self.posY + 1 == ball.posY) or \
           (self.posX == ball.posX and self.posY <= ball.posY < self.posY + 1) or \
           (self.posX + 1 == ball.posX and self.posY <= ball.posY < self.posY + 1):
            self.active = False
            # Optional: Reverse ball direction based on collision side
            if ball_y == self.posY:  # Top or bottom collision
                ball.speedY *= -1
            elif ball.posX == self.posX:  # Left collision
                ball.speedX *= -1
            elif ball.posX == self.posX + 1:  # Right collision
                ball.speedX *= -1
            return True
        return False


def read_high_scores():
    if not os.path.exists(HIGH_SCORE_FILE):
        return []
    with open(HIGH_SCORE_FILE, "r") as file:
        scores = file.readlines()
    return [int(score.strip()) for score in scores]


def write_high_scores(scores):
    with open(HIGH_SCORE_FILE, "w") as file:
        for score in scores:
            file.write(f"{score}\n")


def update_high_scores(new_score):
    scores = read_high_scores()
    scores.append(new_score)
    scores = sorted(scores, reverse=True)[:10]  # Keep only top 10 scores
    write_high_scores(scores)


def print_high_scores():
    scores = read_high_scores()
    print("High Scores:")
    for i, score in enumerate(scores, start=1):
        print(f"{i}. {score}")


def main():
    m = Map(30, 20)  # Map dimensions (width, height)
    b = Ball(15, 10, 8, 8)  # Ball starting position and speed
    p = Paddle(5, 12, 18)  # Paddle width, position

    bricks = [Brick(x, y) for x in range(2, 28, 2)
              for y in range(2, 6)]  # Create bricks

    start_time = time.time()
    points = 0

    try:
        while True:
            m.clear()
            points = b.calculate_collision(m, p, bricks, points)
            b.advance_position()
            b.draw_on(m)
            p.draw_on(m)
            for brick in bricks:
                brick.draw_on(m)
            elapsed_time = time.time() - start_time
            os.system("cls")  # Clear the terminal screen (optional)
            print(m)
            print(f"Time: {elapsed_time:.2f} seconds | Points: {points}")
            time.sleep(DT)

            if keyboard.is_pressed('a'):
                p.move_left()
            elif keyboard.is_pressed('d'):
                p.move_right(m)
            elif keyboard.is_pressed('q'):
                print("Game Quit (reverse.shell Hlib)")
                update_high_scores(points)
                print_high_scores()
                sys.exit()

    except KeyboardInterrupt:
        print("Game stopped.")
        print(f"Final Score: {points}")
        update_high_scores(points)
        print_high_scores()


if __name__ == "__main__":
    main()
