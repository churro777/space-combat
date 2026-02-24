GRID_SIZE = 100
TILE_SIZE = 7
SIDEBAR_WIDTH = 260
WINDOW_WIDTH = GRID_SIZE * TILE_SIZE + SIDEBAR_WIDTH
WINDOW_HEIGHT = GRID_SIZE * TILE_SIZE
FPS = 60
TICK_RATE = 10       # ticks per second
MOVE_COOLDOWN = 2    # ticks (~0.2s, 5 moves/sec)
FIRE_COOLDOWN = 5    # ticks (~0.5s)
SCAN_COOLDOWN = 10   # ticks (~1.0s)
SCAN_MAX_AGE = 100   # ticks (~10s) before breadcrumbs expire
EXPLOSION_DURATION = 15  # ticks (~1.5s)

C_SPEED = 2          # tiles per tick (lightspeed)
SHIP_SPEED = 1       # tiles per tick (0.5c)

# 8 directions: name -> (dx, dy)
DIRECTIONS = {
    "N":  (0, -1),
    "NE": (1, -1),
    "E":  (1, 0),
    "SE": (1, 1),
    "S":  (0, 1),
    "SW": (-1, 1),
    "W":  (-1, 0),
    "NW": (-1, -1),
}

# Colors
COLOR_BG        = (10, 10, 30)
COLOR_GRID      = (30, 30, 60)
COLOR_PLAYER    = (0, 200, 255)
COLOR_ENEMY     = (255, 60, 60)
COLOR_LASER_P   = (0, 255, 200)
COLOR_LASER_E   = (255, 100, 100)
COLOR_SCAN_OUT  = (80, 80, 200)
COLOR_SCAN_RET  = (200, 200, 60)
COLOR_SCAN_MARK = (255, 200, 0)
COLOR_HUD_BG    = (20, 20, 40)
COLOR_HUD_TEXT  = (200, 200, 200)
COLOR_BTN       = (50, 50, 90)
COLOR_BTN_HOVER = (70, 70, 120)
COLOR_BTN_SEL   = (90, 90, 180)
COLOR_WHITE     = (255, 255, 255)
