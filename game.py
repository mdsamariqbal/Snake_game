import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()
pygame.font.init()
pygame.display.set_caption("Snake Game")

# Global Constants
SNAKE_SIZE = 20
APPLE_SIZE = SNAKE_SIZE
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 10
gameClock = pygame.time.Clock()

# Direction constants
KEY = {"UP": 1, "DOWN": 2, "LEFT": 3, "RIGHT": 4}

# Colors
BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
GREEN = pygame.Color("green")
YELLOW = pygame.Color("yellow")
RED = pygame.Color("red")
ORANGE = pygame.Color("orange")

# Fonts
score_font = pygame.font.Font(None, 38)
score_numb_font = pygame.font.Font(None, 28)
game_over_font = pygame.font.Font(None, 48)
play_again_font = pygame.font.Font(None, 28)

# Set up screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

def checkCollision(posA, sizeA, posB, sizeB):
    x1 = posA.x if hasattr(posA, 'x') else posA
    y1 = posA.y if hasattr(posA, 'y') else posA
    x2 = posB.x if hasattr(posB, 'x') else posB
    y2 = posB.y if hasattr(posB, 'y') else posB
    
    return (
        x1 < x2 + sizeB and
        x1 + sizeA > x2 and
        y1 < y2 + sizeB and
        y1 + sizeA > y2
    )

class Segment:
    def __init__(self, x, y, direction=KEY["UP"], color=WHITE):
        self.x = x
        self.y = y
        self.direction = direction
        self.color = color

class Apple:
    def __init__(self, x, y, state=1):
        self.x = x
        self.y = y
        self.state = state
        self.color = ORANGE

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, APPLE_SIZE, APPLE_SIZE))

class Snake:
    def __init__(self, x, y):
        self.stack = [Segment(x, y)]
        self.direction = KEY["UP"]
        self.grow()
        self.grow()

    def move(self):
        for i in reversed(range(1, len(self.stack))):
            self.stack[i].x = self.stack[i - 1].x
            self.stack[i].y = self.stack[i - 1].y
            self.stack[i].direction = self.stack[i - 1].direction

        head = self.stack[0]
        if self.direction == KEY["UP"]:
            head.y = (head.y - SNAKE_SIZE) % SCREEN_HEIGHT
        elif self.direction == KEY["DOWN"]:
            head.y = (head.y + SNAKE_SIZE) % SCREEN_HEIGHT
        elif self.direction == KEY["LEFT"]:
            head.x = (head.x - SNAKE_SIZE) % SCREEN_WIDTH
        elif self.direction == KEY["RIGHT"]:
            head.x = (head.x + SNAKE_SIZE) % SCREEN_WIDTH

    def grow(self):
        tail = self.stack[-1]
        x, y = tail.x, tail.y
        if tail.direction == KEY["UP"]:
            y += SNAKE_SIZE
        elif tail.direction == KEY["DOWN"]:
            y -= SNAKE_SIZE
        elif tail.direction == KEY["LEFT"]:
            x += SNAKE_SIZE
        elif tail.direction == KEY["RIGHT"]:
            x -= SNAKE_SIZE
        self.stack.append(Segment(x, y, tail.direction, YELLOW))

    def draw(self, screen):
        for i, segment in enumerate(self.stack):
            color = GREEN if i == 0 else segment.color
            pygame.draw.rect(screen, color, (segment.x, segment.y, SNAKE_SIZE, SNAKE_SIZE))

    def getHead(self):
        return self.stack[0]

    def setDirection(self, direction):
        if (self.direction == KEY["UP"] and direction != KEY["DOWN"]) or \
           (self.direction == KEY["DOWN"] and direction != KEY["UP"]) or \
           (self.direction == KEY["LEFT"] and direction != KEY["RIGHT"]) or \
           (self.direction == KEY["RIGHT"] and direction != KEY["LEFT"]):
            self.direction = direction

    def checkSelfCollision(self):
        head = self.getHead()
        for segment in self.stack[1:]:
            if checkCollision(head, SNAKE_SIZE, segment, SNAKE_SIZE):
                return True
        return False

def getKey():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                return KEY["UP"]
            elif event.key == pygame.K_DOWN:
                return KEY["DOWN"]
            elif event.key == pygame.K_LEFT:
                return KEY["LEFT"]
            elif event.key == pygame.K_RIGHT:
                return KEY["RIGHT"]
            elif event.key == pygame.K_y:
                return "yes"
            elif event.key == pygame.K_n:
                return "no"
    return None

def endGame():
    message = game_over_font.render("Game Over", True, WHITE)
    message_play_again = play_again_font.render("Play Again? (Y/N)", True, GREEN)
    screen.blit(message, (300, 240))
    screen.blit(message_play_again, (332, 280))
    pygame.display.flip()

    while True:
        gameClock.tick(FPS)
        choice = getKey()
        if choice == "yes":
            main()
            break
        elif choice == "no" or choice == "exit":
            pygame.quit()
            sys.exit()

def drawScore(score):
    label = score_font.render("Score:", True, GREEN)
    value = score_numb_font.render(str(score), True, RED)
    screen.blit(label, (SCREEN_WIDTH - 150, 10))
    screen.blit(value, (SCREEN_WIDTH - 60, 14))

def main():
    score = 0
    snake = Snake(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    apples = [Apple(random.randint(0, (SCREEN_WIDTH - APPLE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE, 
                    random.randint(0, (SCREEN_HEIGHT - APPLE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE)]

    running = True
    while running:
        clock.tick(FPS)
        screen.fill(BLACK)

        key = getKey()
        if key in KEY.values():
            snake.setDirection(key)

        snake.move()

        head = snake.getHead()
        for apple in apples:
            if apple.state == 1 and checkCollision(head, SNAKE_SIZE, apple, APPLE_SIZE):
                apple.state = 0
                snake.grow()
                score += 10

        if snake.checkSelfCollision():
            endGame()

        for apple in apples:
            if apple.state == 1:
                apple.draw(screen)
            else:
                apple.x = random.randint(0, (SCREEN_WIDTH - APPLE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE
                apple.y = random.randint(0, (SCREEN_HEIGHT - APPLE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE
                apple.state = 1

        snake.draw(screen)
        drawScore(score)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()