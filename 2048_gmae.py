import pygame, random, os, math

pygame.init()

# ---------------- WINDOW ----------------
W, H = 520, 720
screen = pygame.display.set_mode((W, H), pygame.RESIZABLE)
pygame.display.set_caption("2048")
clock = pygame.time.Clock()

GRID = 4
PAD = 12
BEST_FILE = "best_score.txt"

# ---------------- COLORS ----------------
BG_TOP = (18, 35, 70)
BG_BOTTOM = (28, 95, 85)

GRID_BG = (18, 45, 70)
EMPTY = (205, 220, 215)

BOX_BG = (30, 75, 120)
BOX_SHADOW = (10, 30, 60)

BEST_GLOW = (120, 220, 255)

BTN_BG = (45, 140, 160)
BTN_HOVER = (65, 170, 185)

# 🎨 ATTRACTIVE COLORS FOR 2 & 4
TILE_COLORS = {
    2:(235, 220, 180),     # warm cream-gold
    4:(180, 215, 225),     # soft teal-blue
    8:(185,220,160), 16:(150,205,120),
    32:(115,190,145), 64:(80,170,170),
    128:(80,150,200), 256:(60,135,195),
    512:(25,150,195), 1024:(10,120,190),
    2048:(0,105,175)
}

TEXT_DARK = (30, 45, 60)
WHITE = (245,250,250)

FONT = pygame.font.SysFont("arialrounded", 26, True)
BIG = pygame.font.SysFont("arialrounded", 52, True)
SMALL = pygame.font.SysFont("arialrounded", 14, True)

# ---------------- UTILS ----------------
def gradient():
    for y in range(H):
        t = y / H
        r = BG_TOP[0] + (BG_BOTTOM[0]-BG_TOP[0]) * t
        g = BG_TOP[1] + (BG_BOTTOM[1]-BG_TOP[1]) * t
        b = BG_TOP[2] + (BG_BOTTOM[2]-BG_TOP[2]) * t
        pygame.draw.line(screen, (int(r),int(g),int(b)), (0,y),(W,y))

def load_best():
    return int(open(BEST_FILE).read()) if os.path.exists(BEST_FILE) else 0

def save_best(v):
    open(BEST_FILE,"w").write(str(v))

# ---------------- ANIMATION STATE ----------------
score_scale = 1.0
best_glow_phase = 0.0

# ---------------- UI BOX ----------------
def draw_box(x, y, w, h, title, value, scale=1.0, glow=False):
    box_rect = pygame.Rect(x, y, w, h)
    box_rect.center = (x + w//2, y + h//2)
    box_rect.width = int(w * scale)
    box_rect.height = int(h * scale)

    shadow = pygame.Rect(box_rect.x, box_rect.y+6, box_rect.w, box_rect.h)
    pygame.draw.rect(screen, BOX_SHADOW, shadow, border_radius=22)
    pygame.draw.rect(screen, BOX_BG, box_rect, border_radius=22)

    if glow:
        glow_surf = pygame.Surface((box_rect.w+12, box_rect.h+12), pygame.SRCALPHA)
        alpha = int(80 + 50 * math.sin(best_glow_phase))
        pygame.draw.rect(glow_surf, (*BEST_GLOW, alpha),
                         glow_surf.get_rect(), border_radius=26)
        screen.blit(glow_surf, (box_rect.x-6, box_rect.y-6))

    screen.blit(
        SMALL.render(title, True, (180,225,245)),
        SMALL.render(title, True, (180,225,245)).get_rect(
            center=(box_rect.centerx, box_rect.y + 18)
        )
    )

    screen.blit(
        FONT.render(str(value), True, WHITE),
        FONT.render(str(value), True, WHITE).get_rect(
            center=(box_rect.centerx, box_rect.y + box_rect.h//2 + 12)
        )
    )

# ---------------- TILE ----------------
class Tile:
    def __init__(self, value, r, c):
        self.value = value
        self.r, self.c = r, c
        self.x = self.tx = 0
        self.y = self.ty = 0
        self.size = 0
        self.scale = 0
        self.spawn = True
        self.pulse = 0

    def move_to(self, x, y):
        self.tx, self.ty = x, y

    def merge(self):
        self.pulse = 0.35

    def update(self):
        self.x += (self.tx - self.x) * 0.35
        self.y += (self.ty - self.y) * 0.35

        if self.spawn:
            self.scale += (1-self.scale)*0.35
            if self.scale > 0.99:
                self.scale = 1
                self.spawn = False
        elif self.pulse > 0:
            self.scale = 1 + self.pulse
            self.pulse *= 0.55
        else:
            self.scale += (1-self.scale)*0.2

    def draw(self):
        s = self.size * self.scale
        rect = pygame.Rect(
            self.x + (self.size-s)/2,
            self.y + (self.size-s)/2,
            s, s
        )
        pygame.draw.rect(screen, TILE_COLORS[self.value], rect, border_radius=16)
        font = FONT if self.value < 1024 else pygame.font.SysFont("arialrounded", 22, True)
        txt = font.render(str(self.value), True, TEXT_DARK)
        screen.blit(txt, txt.get_rect(center=rect.center))

# ---------------- GAME ----------------
class Game:
    def __init__(self):
        self.best = load_best()
        self.restart()

    def restart(self):
        self.score = 0
        self.grid = [[0]*GRID for _ in range(GRID)]
        self.tiles = {}
        self.over = False
        self.spawn()
        self.spawn()

    def spawn(self):
        empty = [(r,c) for r in range(GRID) for c in range(GRID) if self.grid[r][c]==0]
        if not empty: return
        r,c = random.choice(empty)
        val = random.choice([2,4])
        self.grid[r][c] = val
        self.tiles[(r,c)] = Tile(val, r, c)

    def move(self, dx, dy):
        global score_scale
        moved = False
        merged = set()

        order = [(r,c) for r in range(GRID) for c in range(GRID)]
        if dx == 1: order.sort(key=lambda x:-x[1])
        if dy == 1: order.sort(key=lambda x:-x[0])

        for r,c in order:
            if self.grid[r][c] == 0: continue
            nr,nc = r+dy,c+dx
            if 0<=nr<GRID and 0<=nc<GRID:
                if self.grid[nr][nc] == 0:
                    self.grid[nr][nc] = self.grid[r][c]
                    self.grid[r][c] = 0
                    self.tiles[(nr,nc)] = self.tiles.pop((r,c))
                    moved = True
                elif self.grid[nr][nc] == self.grid[r][c] and (nr,nc) not in merged:
                    self.grid[nr][nc] *= 2
                    self.grid[r][c] = 0
                    self.tiles[(nr,nc)].value *= 2
                    self.tiles[(nr,nc)].merge()
                    self.tiles.pop((r,c))
                    merged.add((nr,nc))
                    self.score += self.grid[nr][nc]
                    score_scale = 1.25
                    self.best = max(self.best, self.score)
                    save_best(self.best)
                    moved = True

        if moved:
            self.spawn()
            self.check_over()

    def check_over(self):
        for r in range(GRID):
            for c in range(GRID):
                if self.grid[r][c] == 0:
                    return
                for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                    nr,nc = r+dy,c+dx
                    if 0<=nr<GRID and 0<=nc<GRID and self.grid[nr][nc]==self.grid[r][c]:
                        return
        self.over = True

    def draw(self):
        size = min(W-80, H-260)//GRID
        board_width = size*GRID + PAD*(GRID-1)
        sx = (W - board_width)//2
        sy = 190

        pygame.draw.rect(screen, GRID_BG,
            (sx-16,sy-16,board_width+32,board_width+32),
            border_radius=26)

        for r in range(GRID):
            for c in range(GRID):
                x = sx+c*(size+PAD)
                y = sy+r*(size+PAD)
                pygame.draw.rect(screen, EMPTY, (x,y,size,size), border_radius=16)
                if (r,c) in self.tiles:
                    t = self.tiles[(r,c)]
                    t.size = size
                    t.move_to(x,y)
                    t.update()
                    t.draw()

# ---------------- MAIN LOOP ----------------
game = Game()
restart_btn = pygame.Rect(0,0,180,48)

running = True
while running:
    W,H = screen.get_size()
    gradient()

    score_scale += (1 - score_scale) * 0.15
    best_glow_phase += 0.08

    screen.blit(BIG.render("2048", True, WHITE), (30,25))
    draw_box(190, 30, 120, 60, "SCORE", game.score, scale=score_scale)
    draw_box(320, 30, 150, 60, "BEST", game.best, glow=True)

    game.draw()

    if game.over:
        overlay = pygame.Surface((W,H), pygame.SRCALPHA)
        overlay.fill((0,0,0,160))
        screen.blit(overlay,(0,0))

        screen.blit(
            BIG.render("GAME OVER", True, WHITE),
            BIG.render("GAME OVER", True, WHITE).get_rect(center=(W//2, H//2-90))
        )

        restart_btn.center = (W//2, H//2+30)
        hover = restart_btn.collidepoint(pygame.mouse.get_pos())
        pygame.draw.rect(screen, BTN_HOVER if hover else BTN_BG,
                         restart_btn, border_radius=32)

        screen.blit(
            FONT.render("RESTART", True, WHITE),
            FONT.render("RESTART", True, WHITE).get_rect(center=restart_btn.center)
        )

    pygame.display.flip()
    clock.tick(60)

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN and not game.over:
            if e.key == pygame.K_LEFT: game.move(-1,0)
            if e.key == pygame.K_RIGHT: game.move(1,0)
            if e.key == pygame.K_UP: game.move(0,-1)
            if e.key == pygame.K_DOWN: game.move(0,1)
        if e.type == pygame.MOUSEBUTTONDOWN and game.over:
            if restart_btn.collidepoint(e.pos):
                game.restart()

pygame.quit()
