import pygame
import random
from time import sleep

pygame.init()
WIDTH, HEIGHT = (288,576)
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")
CLOCK = pygame.time.Clock()
FPS = 60

WHITE = (255,255,255)

BACKGROUND = pygame.transform.scale(
             pygame.image.load("sprites/background.png"), (WIDTH, HEIGHT))

PIPE = pygame.transform.scale(
       pygame.image.load("sprites/pipe.png"), (52,250)
)

BASE = pygame.image.load("sprites/base.png")
BASE_X, BASE_Y = (0, HEIGHT-BASE.get_height())

def draw_window(pipes):
    WINDOW.blit(BACKGROUND, (0,0))

    for top_rect, bottom_rect in pipes:

        WINDOW.blit(PIPE, (top_rect.x, top_rect.y))
        WINDOW.blit(PIPE, (bottom_rect.x, bottom_rect.y))

    WINDOW.blit(BASE, (BASE_X, BASE_Y))
    pygame.display.flip()

def generate_pipes():
    pipes = []
    for _ in range(3):

        top_rect_height = random.randint(50,250)
        top = pygame.rect.Rect(0,-top_rect_height, 52, top_rect_height)

        bottom_rect_height = random.randint(50,250)
        bottom = pygame.rect.Rect(0,BASE_Y-bottom_rect_height, 52, bottom_rect_height)
        pipes.append((top,bottom))

    return pipes

def handle_pipe_movement(pipes):
    for top, bottom in pipes:
        top.x -= 1
        if top.x < 0:
            top.x = WIDTH
        bottom.x -= 1
        if bottom.x < 0:
            bottom.x = WIDTH


def main():
    running = True
    # pipe_rect = pygame.rect.Rect(144,BASE_Y-random.randint(50,250), 52, 250)
    pipes = generate_pipes()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        handle_pipe_movement(pipes)
        draw_window(pipes)   
        CLOCK.tick(FPS)
    
    pygame.quit()           

if __name__ == "__main__":
    main()