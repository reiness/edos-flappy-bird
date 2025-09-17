import pygame
import sys
import random
import sqlite3
import os

# --- Database Functions (Local) ---
def get_db_path():
    # Get the directory where the script/executable is running
    # This ensures the database is always next to the .exe
    application_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    return os.path.join(application_path, 'local_scores.db')

def init_local_db():
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            score INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def write_local_score(name, score):
    if not name: return
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()
    cursor.execute('INSERT INTO scores (name, score) VALUES (?, ?)', (name, int(score)))
    conn.commit()
    conn.close()

def read_local_scores():
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()
    cursor.execute('SELECT name, score FROM scores ORDER BY score DESC LIMIT 10')
    scores = cursor.fetchall()
    conn.close()
    return [{'name': name, 'score': score} for name, score in scores]

# --- Game Functions ---
def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 900))
    screen.blit(floor_surface, (floor_x_pos + SCREEN_WIDTH, 900))

def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = active_pipe_surface.get_rect(midtop=(700, random_pipe_pos))
    top_pipe = active_pipe_surface.get_rect(midbottom=(700, random_pipe_pos - 300))
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return [pipe for pipe in pipes if pipe.right > -50]

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 1024:
            screen.blit(active_pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(active_pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            hit_sound.play()
            return False
    if bird_rect.top <= -100 or bird_rect.bottom >= 900:
        hit_sound.play()
        return False
    return True

def rotate_bird(bird):
    return pygame.transform.rotozoom(bird, -bird_movement * 3, 1)

def bird_animation():
    new_bird = active_bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center=(100, bird_rect.centery))
    return new_bird, new_bird_rect

def score_display():
    score_text = f'Score: {int(score)}'
    score_surface = game_font.render(score_text, True, (255, 255, 255))
    score_rect = score_surface.get_rect(center=(SCREEN_WIDTH / 2, 100))
    screen.blit(score_surface, score_rect)

    if not game_active:
        high_score_text = f'High score: {int(high_score)}'
        high_score_surface = game_font.render(high_score_text, True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(SCREEN_WIDTH / 2, 850))
        screen.blit(high_score_surface, high_score_rect)

# --- Initialization ---
pygame.mixer.pre_init(frequency=44100, size=16, channels=1, buffer=512)
pygame.init()
init_local_db() # Ensure the local DB file and table exist on startup
SCREEN_WIDTH, SCREEN_HEIGHT = 576, 1024
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird by Pythia')
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.ttf', 35)
small_font = pygame.font.Font('04B_19.ttf', 25)

# --- Game State & Variables ---
game_active = False
score = 0
high_score = 0
pipe_list = []
player_name = ""
input_active = False
score_submitted = False
leaderboard_scores = read_local_scores()
gravity = 0.25
bird_movement = 0

# --- PRE-LOADING ALL ASSETS ---
bg_day = pygame.transform.scale2x(pygame.image.load('sprites/background-day.png').convert())
bg_night = pygame.transform.scale2x(pygame.image.load('sprites/background-night.png').convert())
backgrounds = {'day': bg_day, 'night': bg_night}
floor_surface = pygame.transform.scale2x(pygame.image.load('sprites/base.png').convert())
floor_x_pos = 0
bird_colors = ['red', 'blue', 'yellow']
birds = {color: [pygame.transform.scale2x(pygame.image.load(f'sprites/{color}bird-{flap}.png').convert_alpha()) for flap in ['downflap', 'midflap', 'upflap']] for color in bird_colors}
pipe_green = pygame.transform.scale2x(pygame.image.load('sprites/pipe-green.png'))
pipe_red = pygame.transform.scale2x(pygame.image.load('sprites/pipe-red.png'))
pipes = {'green': pipe_green, 'red': pipe_red}
pipe_height = [400, 600, 800]
game_over_surface = pygame.transform.scale2x(pygame.image.load('sprites/gameover.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 200))
message_surface = pygame.transform.scale2x(pygame.image.load('sprites/message.png').convert_alpha())
message_rect = message_surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50))
flap_sound = pygame.mixer.Sound('audio/wing.wav')
hit_sound = pygame.mixer.Sound('audio/hit.wav')
score_sound = pygame.mixer.Sound('audio/point.wav')

# --- ACTIVE ASSETS ---
active_bg = backgrounds['day']
active_bird_frames = birds['yellow']
active_pipe_surface = None
bird_index = 0
bird_surface = active_bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(100, SCREEN_HEIGHT / 2))

# --- Timed Events ---
SPAWNPIPE = pygame.USEREVENT
BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

# --- The Game Loop ---
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if game_active:
                if event.key == pygame.K_SPACE:
                    bird_movement = 0
                    bird_movement -= 10
                    flap_sound.play()
            else:
                if input_active:
                    if event.key == pygame.K_RETURN:
                        write_local_score(player_name, score)
                        input_active = False
                        score_submitted = True
                        leaderboard_scores = read_local_scores()
                    elif event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                    elif len(player_name) < 10:
                        player_name += event.unicode
                else:
                    if event.key == pygame.K_SPACE:
                        game_active = True
                        pipe_list.clear()
                        bird_movement = 0
                        score = 0
                        score_submitted = False
                        
                        chosen_bird_color = random.choice(bird_colors)
                        active_bird_frames = birds[chosen_bird_color]
                        chosen_theme = random.choice(['day', 'night'])
                        active_bg = backgrounds[chosen_theme]
                        if chosen_theme == 'day':
                            active_pipe_surface = pipes['green']
                        else:
                            active_pipe_surface = pipes['red']
                        
                        bird_rect = active_bird_frames[0].get_rect(center=(100, SCREEN_HEIGHT / 2))
                        pygame.time.set_timer(SPAWNPIPE, 1200)
                    elif event.key not in (pygame.K_SPACE, pygame.K_RETURN, pygame.K_BACKSPACE) and not score_submitted:
                        input_active = True
                        player_name = event.unicode

        if event.type == SPAWNPIPE and game_active:
            pipe_list.extend(create_pipe())
        if event.type == BIRDFLAP and game_active:
            bird_index = (bird_index + 1) % 3
            bird_surface, bird_rect = bird_animation()

    screen.blit(active_bg, (0, 0))
    if game_active:
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)
        
        if not check_collision(pipe_list):
            game_active = False
            pygame.time.set_timer(SPAWNPIPE, 0)
            leaderboard_scores = read_local_scores()

        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
        
        for pipe in pipe_list:
             if pipe.centerx == 100:
                score += 0.5
                score_sound.play()
        if score > high_score: high_score = score
    else: # Menu / Game Over Screen
        if score > 0:
            screen.blit(game_over_surface, game_over_rect)
            if input_active:
                prompt = small_font.render('Enter Name:', True, (255, 255, 255))
                screen.blit(prompt, (SCREEN_WIDTH/2 - prompt.get_width()/2, 450))
                input_box = pygame.Rect(SCREEN_WIDTH/2 - 150, 490, 300, 50)
                pygame.draw.rect(screen, (255, 255, 255), input_box, 2)
                name_surf = game_font.render(player_name, True, (255, 255, 255))
                screen.blit(name_surf, (input_box.x + 10, input_box.y + 5))
            else:
                if score_submitted:
                    prompt_text = 'Score Saved! Space to Play Again'
                else:
                    prompt_text = 'Space to Play, Type to Save'
                prompt = small_font.render(prompt_text, True, (255, 255, 255))
                screen.blit(prompt, (SCREEN_WIDTH/2 - prompt.get_width()/2, 450))
        else:
            screen.blit(message_surface, message_rect)
            screen.blit(active_bird_frames[bird_index], bird_rect)

        if leaderboard_scores:
            title = small_font.render('Leaderboard', True, (255, 255, 255))
            screen.blit(title, (SCREEN_WIDTH/2 - title.get_width()/2, 560))
            for i, record in enumerate(leaderboard_scores):
                col_width = SCREEN_WIDTH / 2
                x_offset = (i // 5) * col_width + 30
                y_offset = 600 + (i % 5) * 40
                pos_text = f"{i+1}."
                name_text = record['name'][:8]
                score_text = str(record['score'])
                pos_surf = small_font.render(pos_text, True, (255,255,255))
                name_surf = small_font.render(name_text, True, (255,255,255))
                score_surf = small_font.render(score_text, True, (255,255,255))
                screen.blit(pos_surf, (x_offset, y_offset))
                screen.blit(name_surf, (x_offset + 40, y_offset))
                screen.blit(score_surf, (x_offset + 200, y_offset))

    score_display()
    floor_x_pos -= 1
    if floor_x_pos <= -SCREEN_WIDTH: floor_x_pos = 0
    draw_floor()
    pygame.display.update()
    clock.tick(120)