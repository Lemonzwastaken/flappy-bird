import pygame
import sys

# Constants
W, H = 400, 500
GRAVITY = 0.45
FLAP = -8
BIRD_X = 80
BIRD_R = 16
FPS = 60

COLORS = [
    (127, 119, 221)  # purple
]

def darken(color, amount=40):
    return tuple(max(0, c - amount) for c in color)


class Bird:
    def __init__(self):
        self.y = H // 2
        self.vy = 0
        self.color = COLORS[0]
        self.wing_phase = 0

    def flap(self):
        self.vy = FLAP 

    def update(self):
        self.vy += GRAVITY
        self.y += self.vy
        self.wing_phase += 0.25

    def draw(self, screen):
        pygame.draw.ellipse(screen, self.color,
            (BIRD_X - BIRD_R, int(self.y) - BIRD_R - 3, BIRD_R * 2, (BIRD_R - 3) * 2))
        
        pygame.draw.ellipse(screen, (255, 255, 255),
            (BIRD_X + 2, int(self.y) - 9, 10, 8))
        
        pygame.draw.circle(screen, (30, 30, 30),
            (BIRD_X + 8, int(self.y) - 6), 3)
        
        beak = [(BIRD_X + 14, int(self.y) - 3),
                (BIRD_X + 22, int(self.y)),
                (BIRD_X + 14, int(self.y) + 3)]
        pygame.draw.polygon(screen, (239, 159, 39), beak)
        flap_offset = int(8 * abs(pygame.math.Vector2(1, 0).rotate(
            self.wing_phase * 57.3).y))
        wing_rect = (BIRD_X - BIRD_R - 4, int(self.y) + flap_offset - 5, 14, 8)
        pygame.draw.ellipse(screen, darken(self.color, 30), wing_rect)

    def get_rect(self): 
        return pygame.Rect(BIRD_X - BIRD_R + 4, int(self.y) - BIRD_R + 4,
                           (BIRD_R - 4) * 2, (BIRD_R - 4) * 2)


def main():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Flappy Bird")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("sans-serif", 15)

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

        if state == "play":
            bird.update()
            if bird.y - BIRD_R < 0 or bird.y + BIRD_R > H:
                bird.y =  H// 2
                bird.vy = 0
                state = "idle"


        screen.fill((13, 13, 13))
        bird.draw(screen)

        if state == "idle":
            msg = font.render("Click or Space to Start", True, (200, 200, 200))
            screen.blit(msg, (W // 2 - msg.get_width() // 2, H // 2 + 30))


        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()

