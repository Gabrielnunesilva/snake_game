import gymnasium as gym
from stable_baselines3 import DQN 
from stable_baselines3 import A2C
from snake_env import SnakeEnv  
from stable_baselines3.common.env_checker import check_env
import os

# Cria ambiente e verifica a compatibilidade
env = SnakeEnv(render_mode=False)
check_env(env, warn=True)

#project_path = os.path.dirname(os.path.abspath(__file__)) + '\\snake_model.zip'
project_path = r"C:\Portable\snake_game_new\snake_model.zip"
#project_path = "snake_model.zip"

if os.path.exists(project_path):
    model = A2C.load(project_path, env=env)
    print("Modelo Carregado >> ", project_path)
else:
# Define o modelo DQN com a política e parametros de aprendizado
    model = A2C("MlpPolicy", env,
            verbose=0,
            learning_rate=0.001,
            n_steps=20,
            gamma=0.99,
            gae_lambda=0.95,
            ent_coef=0.01,
            )
    print("Criando novo modelo >> ", project_path)
    model.save(project_path)


# Define a quantidade de passos que o agente dará para o treino e inicia o treino
TIMESTEPS = 300000

def train():
    print("Treino Iniciado")
    model.learn(total_timesteps=TIMESTEPS, reset_num_timesteps=False)
    model.save(project_path)
    print("Treinamento concluído e modelo salvo!")

def visual_gaming(max_games):
# Treinamento e prática com visualização
    print("Jogos Visuais Iniciados")
    for i in range(0, max_games):
        obs, _ = env.reset()

        # Visualizar a IA jogando uma partida
        done = False
        env.render_mode = True # Define se vai renderizar
        while not done:
            action, _ = model.predict(obs, deterministic=False)
            obs, reward, done, truncated, info = env.step(action)
            env.render()
    print("Jogos Visuais finalizados")

option = 2

for i in range(1,50):
    print(f"Loop {i}")
    if option == 1:
        train()
    elif option == 2:
        visual_gaming(1)
    else:
        train()