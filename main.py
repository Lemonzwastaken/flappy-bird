import pygame
import sys
import random
import sys
import json
import os


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
SAVE_FILE = "flappy_score.json"


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

def draw_text_centered(screen, font, text, y, color = (255,255,255)):
    surf = font.render(text, True, color)
    screen.blit(surf, (W//2 - surf.get_width() // 2, y))


#LOAD AND SAVE FILE
def load_best():
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r") as f:
                data = json.load(f)
                return data.get("best", 0)
        except(json.JSONDecodeError, KeyError):
            return 0
    return 0

def save_best(best):
    with open(SAVE_FILE, "w") as f:
        json.dump({"best": best}, f)


#BIRB
class Bird:
    def __init__(self):
        self.y = H // 2
        self.vy = 0
        self.color = COLORS[0]
        self.wing_phase = 0

        self.dead = False
        self.death_timer = 0
        self.death_flash = 0
        self.death_x = float(BIRD_X)


    def flap(self):
        self.vy = FLAP 

    def update(self):
        self.vy += GRAVITY * 1.4
        self.y += self.vy
        self.wing_phase += 0.25

    def die(self):
        if not self.dead:
            self.dead = True
            self.death_timer = 0
            self.death_flash = 8
            self.vy = FLAP * 0.6

    def update_death(self):
        self.vy += GRAVITY
        self.y += self.vy * 1.4
        self.death_x -= 1.2
        self.wing_phase += 0.1
        if self.death_flash> 0:
            self.death_flash -= 1
        self.death_timer += 1

    def death_done(self):
        return self.y - BIRD_R > H

    def draw(self, screen):

        color = (255,255,255) if self.death_flash > 0 else self.color
        bx = int(self.death_x) if self.dead else BIRD_X
#
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

#GAME OVER LOL
def draw_game_over(screen, font_big, font_sm, score, best):
    overlay = pygame.Surface((W, H), pygame.SRCALPHA)
    overlay.fill((13, 13, 13, 160))
    screen.blit(overlay, (0, 0))
 
    card_w, card_h = 280, 170
    card_x, card_y = W // 2 - card_w // 2, H // 2 - card_h // 2
    pygame.draw.rect(screen, (30, 30, 30), (card_x, card_y, card_w, card_h), border_radius=12)
    pygame.draw.rect(screen, (60, 60, 60), (card_x, card_y, card_w, card_h), width=1, border_radius=12)

    draw_text_centered(screen, font_big, "GAME OVER", card_y + 24)
    draw_text_centered(screen, font_sm, f"Score: {score}", card_y + 72, (180,180,180))

    new_best = score >= best and score > 0
    best_color = (239, 159, 39) if new_best else (180,180,180)
    best_label = (f"Best:   {best} (NEW!!!)" if new_best else f"Best:   {best}")
    
    draw_text_centered(screen, font_sm, best_label, card_y + 98, best_color)
    draw_text_centered(screen, font_sm, "Click or Space to retry", card_y + 140, (120, 120, 120))
 

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

    font_big = pygame.font.SysFont("sans-serif", 28)
    font_hud = pygame.font.SysFont("sans-serif", 18)
    font_sm = pygame.font.SysFont("sans-serif", 15)
    
    best = load_best()

    bird, pipes, score = new_game()
 
    #STATES = IDLE/PLAYING/DYING/DEAD
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
                elif state == "play":
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
                    if score > best:
                        best = score
                        save_best(score)
                    

 
            bird_rect = bird.get_rect()
            hit = bird.y - BIRD_R < 0 or bird.y + BIRD_R > H
            hit = hit or any(p.collides(bird_rect) for p in pipes)
        if hit:
                bird.die()
                state = "dying"
            
        elif state == "dying":
            bird.update_death()
            if bird.death_done():
                state = "dead"  

        screen.fill((13, 13, 13))
        for p in pipes:
            p.draw(screen)
        bird.draw(screen)

        hud = font_hud.render(f"Score: {score}     Best: {best}", True, (180,180,180))
        screen.blit(hud, (10,10))

        if state == "idle":
            overlay = pygame.Surface((W, H), pygame.SRCALPHA)
            overlay.fill((13, 13, 13, 100))
            screen.blit(overlay, (0, 0))
            draw_text_centered(screen, font_big, "Flappy Birb", H // 2 - 20)
            draw_text_centered(screen, font_sm, "Click or Space to start", H // 2 + 16, (180,180,180))


        if state == "dead":
            draw_game_over(screen, font_big, font_sm, score, best)
            
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()

