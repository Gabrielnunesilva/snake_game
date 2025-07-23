import gymnasium as gym
from gymnasium import spaces
import numpy as np
from snake_game import reset_game, snake_action, render_game, get_game_state, SCREEN_WIDTH, SCREEN_HEIGHT, SCORE_HEIGHT, SNAKE_SIZE
import pygame
import math

# scores_path = os.path.dirname(os.path.abspath(__file__)) + '\\scores.txt'
scores_path = r"C:\Portable\snake_game_new\scores.txt"
#scores_path = "scores.txt"

class SnakeEnv(gym.Env):
    def __init__(self, render_mode=True):
        super(SnakeEnv, self).__init__()
        self.render_mode = render_mode

        self.action_space = spaces.Discrete(2)  # 0 = seguir, 1 = virar
        self.observation_space = spaces.Box(low=np.array([0, 0, 0, 0, 0, 0, -1.0, -1.0]),
                                            high=np.array([1, 1, 1, 1, 1, 1, 1.0, 1.0]),
                                            dtype=np.float32)
        MAX_STEPS = (SCREEN_WIDTH / 20) * ((SCREEN_HEIGHT - SCORE_HEIGHT) / 20)
        self.max_steps_without_food = MAX_STEPS 
        self.steps_without_food = 0
        self.episode_steps = 0


        self.max_cols = int(SCREEN_WIDTH / SNAKE_SIZE)
        self.max_rows = int((SCREEN_HEIGHT - SCORE_HEIGHT) / SNAKE_SIZE)

    def reset(self, seed=None, **kwargs):
        super().reset(seed=seed)
        self.steps_without_food = 0
        self.episode_steps = 0
        state = reset_game()
        return self._get_observation(state), {}

    def step(self, action):
        prev_state = get_game_state()
        prev_distance = self._calculate_distance_to_food(prev_state)

        row = (prev_state['snake_position'][1] - SCORE_HEIGHT) // SNAKE_SIZE
        col = prev_state['snake_position'][0] // SNAKE_SIZE
        suggested_dirs = self._map_sugest(row, col)
        current_dir = prev_state['snake_direction']

        # Se houver duas sugestões, remover a que está bloqueada
        if len(suggested_dirs) == 2:
            dir1, dir2 = suggested_dirs
            blocked1 = self._is_blocked(prev_state, dir1)
            blocked2 = self._is_blocked(prev_state, dir2)

            if blocked1 and not blocked2:
                suggested_dirs = [dir2]
            elif blocked2 and not blocked1:
                suggested_dirs = [dir1]

        if not suggested_dirs:
            chosen_dir = current_dir
        elif action == 0:
            chosen_dir = suggested_dirs[0]
        elif action == 1 and len(suggested_dirs) > 1:
            chosen_dir = suggested_dirs[1]
        else:
            chosen_dir = suggested_dirs[0]

        # Converter direção absoluta para ação relativa
        directions = ["UP", "RIGHT", "DOWN", "LEFT"]
        idx_current = directions.index(current_dir)
        idx_chosen = directions.index(chosen_dir)
        diff = (idx_chosen - idx_current) % 4

        if diff == 0:
            rel_action = 0  # frente
        elif diff == 1:
            rel_action = 2  # direita
        elif diff == 3:
            rel_action = 1  # esquerda
        else:
            return self._get_observation(prev_state), -10, True, False, {}

        state, reward, done = snake_action(rel_action)

        current_distance = self._calculate_distance_to_food(state)
        distance_change = prev_distance - current_distance
        reward += distance_change * 4

        if self.steps_without_food > 50:
            reward -= 0.01 * (self.steps_without_food - 50)

        self.steps_without_food += 1
        self.episode_steps += 1

        if reward >= 10:
            self.steps_without_food = 0

        if self.steps_without_food >= self.max_steps_without_food:
            done = True
            reward -= 100

        if done:
            with open(scores_path, "a") as file:
                file.write(f"{state['score']}/{self.episode_steps},")
            self.episode_steps = 0

        return self._get_observation(state), reward, done, False, {}

    def render(self, mode="human"):
        if self.render_mode:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            render_game()

    def _get_observation(self, state):
        snake_x, snake_y = state['snake_position']
        food_x, food_y = state['food_position']
        body = state['snake_body']
        direction = state["snake_direction"]
        SNAKE_SIZE = state['snake_size']

        def get_relative_positions(direction):
            if direction == "UP":
                return (0, -SNAKE_SIZE), (-SNAKE_SIZE, 0), (SNAKE_SIZE, 0)
            elif direction == "DOWN":
                return (0, SNAKE_SIZE), (SNAKE_SIZE, 0), (-SNAKE_SIZE, 0)
            elif direction == "LEFT":
                return (-SNAKE_SIZE, 0), (0, SNAKE_SIZE), (0, -SNAKE_SIZE)
            elif direction == "RIGHT":
                return (SNAKE_SIZE, 0), (0, -SNAKE_SIZE), (0, SNAKE_SIZE)

        front, left, right = get_relative_positions(direction)

        def danger_at(offset):
            x, y = snake_x + offset[0], snake_y + offset[1]
            return (
                x < 0 or x >= SCREEN_WIDTH or
                y < SCORE_HEIGHT or y >= SCREEN_HEIGHT or
                [x, y] in body
            )

        danger_front = danger_at(front)
        danger_left = danger_at(left)
        danger_right = danger_at(right)

        food_dx = food_x - snake_x
        food_dy = food_y - snake_y

        food_front = 1 if (front[0] * food_dx + front[1] * food_dy) > 0 else 0
        food_left  = 1 if (left[0]  * food_dx + left[1]  * food_dy) > 0 else 0
        food_right = 1 if (right[0] * food_dx + right[1] * food_dy) > 0 else 0
        dx = np.clip((food_x - snake_x) / SCREEN_WIDTH, -1.0, 1.0)
        dy = np.clip((food_y - snake_y) / SCREEN_HEIGHT, -1.0, 1.0)

        return np.array([
            int(danger_front), int(danger_left), int(danger_right),
            food_front, food_left, food_right, dx, dy
        ], dtype=np.float32)

    def _calculate_distance_to_food(self, state):
        sx, sy = state['snake_position']
        fx, fy = state['food_position']
        return math.sqrt((sx - fx) ** 2 + (sy - fy) ** 2)

    def _map_sugest(self, row, col):
        if row == 0 and col == 0:
            return ['DOWN']
        elif row == self.max_rows - 1 and col == 0:
            return ['RIGHT']
        elif row == 0 and col == self.max_cols - 1:
            return ['LEFT']
        elif row == self.max_rows - 1 and col == self.max_cols - 1:
            return ['UP']
        elif row == 0 and (col % 2 == 1):
            return ['LEFT']
        elif row == 0 and (col % 2 == 0):
            return ['LEFT', 'DOWN']
        elif row == self.max_rows - 1 and (col % 2 == 0):
            return ['RIGHT']
        elif row == self.max_rows - 1 and (col % 2 == 1):
            return ['RIGHT', 'UP']
        elif (row % 2 == 0) and col == 0:
            return ['DOWN']
        elif (row % 2 == 1) and col == 0:
            return ['RIGHT', 'DOWN']
        elif (row % 2 == 0) and col == self.max_cols - 1:
            return ['LEFT', 'UP']
        elif (row % 2 == 1) and col == self.max_cols - 1:
            return ['UP']
        elif (row % 2 == 1) and (col % 2 == 1):
            return ['RIGHT', 'UP']
        elif (row % 2 == 1) and (col % 2 == 0):
            return ['RIGHT', 'DOWN']
        elif (row % 2 == 0) and (col % 2 == 1):
            return ['LEFT', 'UP']
        elif (row % 2 == 0) and (col % 2 == 0):
            return ['LEFT', 'DOWN']
        else:
            return []

    def _is_blocked(self, state, direction):
        snake_x, snake_y = state['snake_position']
        body = state['snake_body']
        size = state['snake_size']

        if direction == "UP":
            x, y = snake_x, snake_y - size
        elif direction == "DOWN":
            x, y = snake_x, snake_y + size
        elif direction == "LEFT":
            x, y = snake_x - size, snake_y
        elif direction == "RIGHT":
            x, y = snake_x + size, snake_y
        return [x, y] in body
