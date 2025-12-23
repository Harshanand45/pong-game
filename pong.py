import pygame, sys
pygame.init()
def draw_start_screen():
    screen.fill(BLACK)

    title = big_font.render("PONG", True, WHITE)
    screen.blit(title, (WIDTH//2 - 70, 80))

    lines = [
        "Press 1 : Two Player",
        "Press 2 : Player vs AI",
        "",
        "Controls:",
        "Player 1 : W (Up) | S (Down)",
        "Player 2 : UP (Up) | DOWN (Down)",
        "Start Game : P",
        "Restart : R",
        "",
        "First to 5 points wins"
    ]

    y = 170
    for line in lines:
        text = font.render(line, True, WHITE)
        screen.blit(text, (WIDTH//2 - 200, y))
        y += 30

# ---------------- SETTINGS ----------------
WIDTH, HEIGHT = 900, 500
BLACK = (0,0,0)
WHITE = (255,255,255)
WIN_SCORE = 5

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PONG")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)
big_font = pygame.font.SysFont(None, 60)

# ---------------- BALL ----------------
class Ball:
    def __init__(self, x, y, r):
        self.r = r
        self.reset(x, y)

    def reset(self, x, y):
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0

    def start(self):
        self.dx = 6
        self.dy = 3

    def move(self):
        self.x += self.dx
        self.y += self.dy

    def draw(self):
        pygame.draw.circle(screen, WHITE, (self.x, self.y), self.r)

    def bounce_x(self):
        self.dx = -self.dx * 1.05

    def bounce_y(self):
        self.dy = -self.dy

# ---------------- PADDLE ----------------
class Paddle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 15
        self.h = 120
        self.speed = 8
        self.state = "stop"

    def move(self):
        if self.state == "up":
            self.y -= self.speed
        elif self.state == "down":
            self.y += self.speed
        self.y = max(0, min(HEIGHT - self.h, self.y))

    def ai_move(self, ball):
        if ball.y < self.y + self.h//2:
            self.y -= 6
        elif ball.y > self.y + self.h//2:
            self.y += 6
        self.y = max(0, min(HEIGHT - self.h, self.y))

    def draw(self):
        pygame.draw.rect(screen, WHITE, (self.x, self.y, self.w, self.h))

# ---------------- COLLISION ----------------
def paddle_hit(ball, paddle):
    return (
        ball.x - ball.r <= paddle.x + paddle.w and
        ball.x + ball.r >= paddle.x and
        ball.y + ball.r >= paddle.y and
        ball.y - ball.r <= paddle.y + paddle.h
    )

# ---------------- DRAW ----------------
def draw_center():
    screen.fill(BLACK)
    pygame.draw.line(screen, WHITE, (WIDTH//2,0), (WIDTH//2,HEIGHT), 3)

def draw_score(s1, s2):
    t1 = font.render(str(s1), True, WHITE)
    t2 = font.render(str(s2), True, WHITE)
    screen.blit(t1, (WIDTH//2 - 60, 20))
    screen.blit(t2, (WIDTH//2 + 40, 20))

# ---------------- GAME OBJECTS ----------------
ball = Ball(WIDTH//2, HEIGHT//2, 12)
p1 = Paddle(20, HEIGHT//2 - 60)
p2 = Paddle(WIDTH - 35, HEIGHT//2 - 60)

score1 = 0
score2 = 0
playing = False
mode = None
game_over = False

# ---------------- MAIN LOOP ----------------
while True:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if mode is None:
                if event.key == pygame.K_1:
                    mode = "PVP"
                if event.key == pygame.K_2:
                    mode = "AI"

            if event.key == pygame.K_p and not game_over:
                ball.start()
                playing = True

            if event.key == pygame.K_r:
                score1 = score2 = 0
                ball.reset(WIDTH//2, HEIGHT//2)
                game_over = False
                playing = False

            if event.key == pygame.K_w:
                p1.state = "up"
            if event.key == pygame.K_s:
                p1.state = "down"
            if event.key == pygame.K_UP:
                p2.state = "up"
            if event.key == pygame.K_DOWN:
                p2.state = "down"

        if event.type == pygame.KEYUP:
            p1.state = "stop"
            p2.state = "stop"

    # ---------------- MENU ----------------
    if mode is None:
      draw_start_screen()
      pygame.display.update()
      continue

    draw_center()

    if playing and not game_over:
        ball.move()

        if ball.y - ball.r <= 0 or ball.y + ball.r >= HEIGHT:
            ball.bounce_y()

        if paddle_hit(ball, p1) and ball.dx < 0:
            ball.bounce_x()
        if paddle_hit(ball, p2) and ball.dx > 0:
            ball.bounce_x()

        if ball.x < 0:
            score2 += 1
            ball.reset(WIDTH//2, HEIGHT//2)
            playing = False

        if ball.x > WIDTH:
            score1 += 1
            ball.reset(WIDTH//2, HEIGHT//2)
            playing = False

        if score1 == WIN_SCORE or score2 == WIN_SCORE:
            game_over = True

    p1.move()
    if mode == "AI":
        p2.ai_move(ball)
    else:
        p2.move()

    p1.draw()
    p2.draw()
    ball.draw()
    draw_score(score1, score2)

    if game_over:
        text = "Player 1 Wins!" if score1 == WIN_SCORE else "Player 2 Wins!"
        screen.blit(big_font.render(text, True, WHITE), (WIDTH//2-150, HEIGHT//2-30))
        screen.blit(font.render("Press R to Restart", True, WHITE), (WIDTH//2-120, HEIGHT//2+30))

    pygame.display.update()
