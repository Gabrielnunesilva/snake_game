import pygame
import random # type: ignore
import time
import os

# Inicialização do Pygame e Definição de variaveis
pygame.init()
GREEN, WHITE, BLACK, RED, GREY = (34, 177, 76), (255, 255, 255), (0, 0, 0), (255, 0, 0), (200, 200, 200)
SCREEN_WIDTH, SCREEN_HEIGHT, SCORE_HEIGHT, SCREEN_TITLE = 400, 450, 50, "Jogo da Cobrinha" 
max_score = (SCREEN_WIDTH / 20) * ((SCREEN_HEIGHT - SCORE_HEIGHT) / 20) - 1
SNAKE_SIZE, snake_position = 20, [100, 120]
assert SCREEN_WIDTH % SNAKE_SIZE == 0, "Largura incompatível com snake size"
assert (SCREEN_HEIGHT - SCORE_HEIGHT) % SNAKE_SIZE == 0, "Altura incompatível com snake size"

score = 0
render = True

# Variáveis de tempo para evitar mudanças rápidas de direção
last_direction_change_time = time.time()
direction_change_delay = 0.10  # Tempo em segundos entre mudanças de direção

def draw_score():
    font = pygame.font.SysFont("Arial", 24)
    score_text = font.render(f"Pontuação: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

def food_create():
    while True:
        food_position_x = random.randint(0, (SCREEN_WIDTH - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE
        food_position_y = random.randint(0, (SCREEN_HEIGHT - SCORE_HEIGHT - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE + SCORE_HEIGHT
        food_position = [food_position_x, food_position_y]
        
        # Garantir que a comida não saia dos limites ou na posição da cobra
        if food_position[1] < SCREEN_HEIGHT and food_position[0] < SCREEN_WIDTH:
            if food_position not in snake_body:
                return food_position
            
def reset_game():
    global snake_position, snake_body, score, snake_direction, food_position, SNAKE_SIZE
    snake_position = [100, 50]
    snake_body = [list(snake_position)]
    score = 0
    snake_direction = "LEFT"
    food_position = food_create()
    return get_game_state()

def get_game_state():
    return{
        'snake_position': snake_position,
        'snake_direction': snake_direction,
        'snake_body':   snake_body,
        'snake_size': SNAKE_SIZE,
        'score': score,
        'food_position': food_position
    }

def render_game():
    global render, screen
    if render:
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(SCREEN_TITLE)
        render = False

    clock = pygame.time.Clock()
    # Preenche a tela com a cor branca   
    screen.fill(WHITE)
    # Cria a cobra, comida e score
    pygame.draw.rect(screen, GREEN, pygame.Rect(snake_position[0], snake_position[1], SNAKE_SIZE, SNAKE_SIZE))
    pygame.draw.rect(screen, RED, pygame.Rect(food_position[0], food_position[1], SNAKE_SIZE, SNAKE_SIZE))
    pygame.draw.rect(screen, GREY , (0, 0, SCREEN_WIDTH, SCORE_HEIGHT))

    # renderizar setinhas
    from snake_env import SnakeEnv
    env_temp = SnakeEnv(render_mode=False)
    for row in range(env_temp.max_rows):
        for col in range(env_temp.max_cols):
            sugest = env_temp._map_sugest(row, col)
            x = col * SNAKE_SIZE
            y = row * SNAKE_SIZE + SCORE_HEIGHT
            for i, dir in enumerate(sugest):
                color = GREY if i == 0 else GREY  # seta principal = cinza, alternativa = cinza
                draw_arrow(screen, x, y, dir, color=color, size=5)

    # Desenhar o corpo da cobra
    for pos in snake_body:
        pygame.draw.rect(screen, GREEN, pygame.Rect(pos[0], pos[1], SNAKE_SIZE, SNAKE_SIZE))

    draw_score()  # Desenha a pontuação
    clock.tick(15)
    pygame.display.flip()  # Atualiza a tela

def draw_arrow(surface, x, y, direction, color=BLACK, size=6):
    """
    Desenha uma seta apontando na direção correta (UP, DOWN, LEFT, RIGHT),
    centralizada dentro da célula (x, y), com tamanho e cor definidos.
    """
    center_x = x + SNAKE_SIZE // 2
    center_y = y + SNAKE_SIZE // 2

    if direction == "UP":
        points = [
            (center_x, center_y - size),  # topo (ponta)
            (center_x - size, center_y + size),  # base esquerda
            (center_x + size, center_y + size)   # base direita
        ]
    elif direction == "DOWN":
        points = [
            (center_x, center_y + size),  # base
            (center_x - size, center_y - size),
            (center_x + size, center_y - size)
        ]
    elif direction == "LEFT":
        points = [
            (center_x - size, center_y),
            (center_x + size, center_y - size),
            (center_x + size, center_y + size)
        ]
    elif direction == "RIGHT":
        points = [
            (center_x + size, center_y),
            (center_x - size, center_y - size),
            (center_x - size, center_y + size)
        ]

    pygame.draw.polygon(surface, color, points)



def snake_action(action_relative):
    global snake_direction, score, food_position

    new_direction = relative_to_absolute(action_relative, snake_direction)

    # Evita voltar diretamente
    opposite = {"UP": "DOWN", "DOWN": "UP", "LEFT": "RIGHT", "RIGHT": "LEFT"}
    if new_direction != opposite[snake_direction]:
        snake_direction = new_direction

        # Movimento
        if snake_direction == "UP":
            snake_position[1] -= SNAKE_SIZE
        elif snake_direction == "DOWN":
            snake_position[1] += SNAKE_SIZE
        elif snake_direction == "LEFT":
            snake_position[0] -= SNAKE_SIZE
        elif snake_direction == "RIGHT":
            snake_position[0] += SNAKE_SIZE

        # Verifica colisões
        done = False
        reward = -0.1
        if (snake_position[0] < 0 or snake_position[0] >= SCREEN_WIDTH or 
            snake_position[1] < SCORE_HEIGHT or snake_position[1] >= SCREEN_HEIGHT or 
            snake_position in snake_body[1:]):
            reward = -100
            done = True
        else:
            snake_body.insert(0, list(snake_position))
            if snake_position == food_position:
                reward = 50
                score += 1
                if score == int(max_score):
                    #print("Venceu o Jogo !")
                    done = True
                else:
                    food_position = food_create()
            else:
                snake_body.pop()
    else:
        reward = -5 
        done = False

    return get_game_state(), reward, done


def relative_to_absolute(action_relative, current_direction):
    directions = ["UP", "RIGHT", "DOWN", "LEFT"]
    idx = directions.index(current_direction)

    # Ação relativa: 0 = frente, 1 = esquerda, 2 = direita
    if action_relative == 1:  # virar à esquerda
        idx = (idx - 1) % 4
    elif action_relative == 2:  # virar à direita
        idx = (idx + 1) % 4
    # se for 0, mantém a direção

    return directions[idx]




