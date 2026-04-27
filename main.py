import pygame
import random
import sys

pygame.mixer.init()


WIDTH, HEIGHT = (288, 576)
CLOCK = pygame.time.Clock()
FPS = 60
GAMEOVER = pygame.USEREVENT
WHITE = (255, 255, 255)

WING_SOUND = pygame.mixer.Sound("audio/wing.wav")
DIE_SOUND = pygame.mixer.Sound("audio/die.wav")
HIT_SOUND = pygame.mixer.Sound("audio/hit.wav")
POINT_SOUND = pygame.mixer.Sound("audio/point.wav")

zero = pygame.image.load("sprites/0.png")
SCORE_SURFACES = {
    0: pygame.image.load("sprites/0.png"),
    1: pygame.image.load("sprites/1.png"),
    2: pygame.image.load("sprites/2.png"),
    3: pygame.image.load("sprites/3.png"),
    4: pygame.image.load("sprites/4.png"),
    5: pygame.image.load("sprites/5.png"),
    6: pygame.image.load("sprites/6.png"),
    7: pygame.image.load("sprites/7.png"),
    8: pygame.image.load("sprites/8.png"),
    9: pygame.image.load("sprites/9.png"),
}

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

GAME_START_MSG = pygame.transform.scale(
    (pygame.image.load("sprites/message.png")), (200, 500)
)

BACKGROUND = pygame.transform.scale(
    pygame.image.load("sprites/background.png"), (WIDTH, HEIGHT)
)

BIRD = pygame.transform.scale(pygame.image.load("sprites/bird.png"), (30, 30))

PIPE = pygame.transform.scale(pygame.image.load("sprites/pipe.png"), (52, 250))

BASE = pygame.image.load("sprites/base.png")

BASE_X, BASE_Y = (0, HEIGHT - BASE.get_height())


def game_start():

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return
        WINDOW.blit(BACKGROUND, (0, 0))
        WINDOW.blit(
            GAME_START_MSG,
            (
                WIDTH // 2 - GAME_START_MSG.get_width() // 2,
                HEIGHT // 2 - GAME_START_MSG.get_height() // 2,
            ),
        )
        pygame.display.flip()


def draw_window(pipes, bird_rect, points):
    WINDOW.blit(BACKGROUND, (0, 0))
    WINDOW.blit(BIRD, (bird_rect.x, bird_rect.y))
    for top, bottom in pipes:
        WINDOW.blit(pygame.transform.rotate(PIPE, 180), (top.x, top.y))
        WINDOW.blit(PIPE, (bottom.x, bottom.y))

    digits = []
    for digit in str(points):
        digits.append(int(digit))
    for index, digit in enumerate(digits):
        digit_surface = SCORE_SURFACES[digit]
        WINDOW.blit(
            digit_surface, (WIDTH // 2 + (index * digit_surface.get_width()), 100)
        )

    WINDOW.blit(BASE, (BASE_X, BASE_Y))
    pygame.display.flip()


def generate_pipe():
    top_rect_height = random.randint(50, 150)
    top = pygame.rect.Rect(500, -top_rect_height, 52, PIPE.get_height())

    bottom_rect_height = random.randint(50, 180)
    bottom = pygame.rect.Rect(500, BASE_Y - bottom_rect_height, 52, PIPE.get_height())

    return (top, bottom)


def handle_pipe_movement(pipes: list):
    for top, bottom in pipes:
        top.x -= 2
        bottom.x -= 2

    _top, _ = pipes[-1]
    if _top.x < 300:
        pipes.append(generate_pipe())
    if pipes[0][0].x < -PIPE.get_width():
        pipes.remove(pipes[0])


def handle_detection(
    bird_rect: pygame.rect.Rect, pipes: pygame.rect.Rect, base: pygame.rect.Rect
):
    if bird_rect.colliderect(base):
        pygame.event.post(pygame.event.Event(GAMEOVER))
        HIT_SOUND.play()
        return

    for top, bottom in pipes:
        if bird_rect.colliderect(top) or bird_rect.colliderect(bottom):
            pygame.event.post(pygame.event.Event(GAMEOVER))
            HIT_SOUND.play()
            return


def increase_point(bird_rect: pygame.rect.Rect, pipes, points):
    _, bottom = pipes[0]
    if bottom.x == bird_rect.x:
        points += 1
        POINT_SOUND.play()
    return points


def main():

    running = True
    points = 0
    BASE_RECT = pygame.rect.Rect(BASE_X, BASE_Y, BASE.get_width(), BASE.get_width())
    BIRD_RECT = BIRD.get_rect(top=100, left=100)
    pipes = []
    pipes.append(generate_pipe())
    while running:
        BIRD_RECT.y += 1.5

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    BIRD_RECT.y -= 41
                    WING_SOUND.play()

            if event.type == GAMEOVER:
                pygame.time.delay(4000)
                running = False
                break

        handle_detection(BIRD_RECT, pipes, BASE_RECT)
        points = increase_point(BIRD_RECT, pipes, points)
        handle_pipe_movement(pipes)
        draw_window(pipes, BIRD_RECT, points)
        CLOCK.tick(FPS)


if __name__ == "__main__":
    while True:
        pygame.init()
        game_start()
        main()
