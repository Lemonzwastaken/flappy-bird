import pygame
import sys
import random

# Constants
W, H = 400, 500
GRAVITY = 0.45
FLAP = -8
PIPE = -8
PIPE_W = 55
GAP = 200
MIN_GAP = 60
PIPE_SPEED = 2.4
BIRD_X = 80
BIRD_R = 16
FPS = 60
GAP_DRECREASE = 3

COLORS = [
    (127, 119, 221),
    (212, 83, 126),
    (29, 158, 117),
    (239, 159, 39),
    (216, 90, 48),
    (55, 138, 221),
    (99, 153, 34),
]

def rc():
    return random.choice(COLORS)

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

class Pipe:
    def __init__(self, x = None):
        self.x = x if x is not None else W + 10
        self.top = random.randint(60, H- GAP - 129)
        self.bot = self.top + GAP
        self.color = rc()
        self.scored = False

    def update(self):
        self.x -= PIPE_SPEED

    def draw(self, screen):
        pygame.draw.rect(screen, self.color,
            (self.x, 0, PIPE_W, self.top), border_radius=4)
        pygame.draw.rect(screen, darken(self.color),
            (self.x + PIPE_W - 6, 0, 6, self.top))
        pygame.draw.rect(screen, self.color,
            (self.x, self.bot, PIPE_W, H - self.bot), border_radius=4)
        pygame.draw.rect(screen, darken(self.color),
            (self.x + PIPE_W - 6, self.bot, 6, H - self.bot))

        
    def collides(self, bird_rect):
        top_rect = pygame.Rect(self.x + 4, 0, PIPE_W - 8, self.top)
        bot_rect = pygame.Rect(self.x + 4, self.bot, PIPE_W - 8, H-self.bot)
        return bird_rect.colliderect(top_rect) or bird_rect.colliderect(bot_rect)
    
    def off_screen(self):
        return self.x < -PIPE_W - 10


def new_game():
    global GAP
    GAP = 200
    bird = Bird()
    pipes = [Pipe(W + 60)]
    score = 0
    return bird, pipes, score


def main():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Flappy Birb")
    clock = pygame.time.Clock()
    font_hud = pygame.font.SysFont("sans-serif", 18)
    font_sm = pygame.font.SysFont("sans-serif", 15)
 
    bird, pipes, score = new_game()
    state = "idle"
 
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                if event.type == pygame.KEYDOWN and event.key != pygame.K_SPACE:
                    continue
                if state == "dead":
                    bird, pipes, score = new_game()
                    state = "idle"
                elif state == "idle":
                    state = "play"
                    bird.flap()
                else:
                    bird.flap()
 
        if state == "play":
            global GAP
            bird.update()
            for p in pipes:
                p.update()
            if pipes[-1].x < W - 200:
                pipes.append(Pipe())
            pipes = [p for p in pipes if not p.off_screen()]
 
            for p in pipes:
                if not p.scored and p.x + PIPE_W < BIRD_X:
                    p.scored = True
                    score += 1
                    print(score)
                    GAP = max(MIN_GAP, GAP - GAP_DRECREASE)
 
            bird_rect = bird.get_rect()
            if bird.y - BIRD_R < 0 or bird.y + BIRD_R > H:
                state = "dead"
            for p in pipes:
                if p.collides(bird_rect):
                    state = "dead"



        screen.fill((13, 13, 13))
        for p in pipes:
            p.draw(screen)
        bird.draw(screen)

        if state == "idle":
            msg = font_sm.render("Click or Space to start", True, (200,200,200))
            screen.blit(msg, (W//2 - msg.get_width() // 2, H // 2 + 30))

        if state == "dead":
            msg = font_sm.render("You died lol", True, (200,200,200))
            screen.blit(msg, (W//2 - msg.get_width() // 2, H // 2))
            
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()

