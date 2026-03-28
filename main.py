import pygame
import sys

#CONSTANTS
W, H = 400, 500
GRAVITY = 0.45
FLAP = -8
BIRD_X = 80
BIRD_R = 16
FPS = 60

COLORS = [
    (127, 119, 221) #purple
]

def darken(color, amount = 40):
    return tuple(max(0, c - amount) for c in color)

class Bird:
    def __init__(self):
        self.y = H//2
        self.vy = 0
        self.color = COLORS[0]
        self.wing_phase = 0


def main():
    pygame.init()
    screen = pygame.display.set_mode((W,H))
    pygame.display.set_caption("FLAPPY BIRD")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("sans-sherif", 15)

    bird = Bird()
    state = "idle"

if __name__ == "__main__":
    main()