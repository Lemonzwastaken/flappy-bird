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

    def flap(self):
        self.vy = self.flap

    def update(self):
        self.vy += GRAVITY
        self.y += self.vy
        self.wing_phase += 0.25


def main():
    pygame.init()
    screen = pygame.display.set_mode((W,H))
    pygame.display.set_caption("FLAPPY BIRD")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("sans-sherif", 15)

    bird = Bird()
    state = "idle"

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                if event.type == pygame.KEYDOWN and event.key != pygame.K_SPACE:
                    continue

                if state == "idle":
                    state = "play"
                
                bird.flap()


    pygame.display.flip()
    clock.tick(FPS)

if __name__ == "__main__":
    main()