# 🐍 Snake Game com Inteligência Artificial (Reinforcement Learning)

Este projeto implementa o clássico **Jogo da Cobrinha** (Snake Game) controlado por uma **Inteligência Artificial** treinada com **Aprendizado por Reforço** usando a biblioteca [Stable-Baselines3](https://stable-baselines3.readthedocs.io/).

---

## 🚀 Funcionalidades

- 🎮 Implementação completa do jogo da cobrinha com **Pygame**.
- 🧠 Ambiente compatível com **Gymnasium** para treino de IA.
- 🤖 Treinamento usando **A2C** (Advantage Actor-Critic) — modelo facilmente adaptável para outros algoritmos como DQN, PPO, etc.
- 📊 Registro automático de **pontuação** e **número de movimentos** por jogo.
- 📈 Ferramenta gráfica para **visualização de desempenho** (pontuações e movimentos ao longo do treino).
- 🛠 Estrutura modular para facilitar ajustes e testes.

---

## 📂 Estrutura do Projeto

```
📁 snake_ai_project/
├── learning_data.py      # Visualização dos resultados de treino em gráficos
├── snake_env.py          # Definição do ambiente Gymnasium
├── snake_game.py         # Implementação do jogo com Pygame
├── train_snake.py        # Script para treino e visualização da IA
├── scores.txt            # Registro de pontuações e movimentos
└── snake_model.zip       # Modelo treinado (gerado após treino)
```

---

## 🖥 Ambiente e Tecnologias

- **Linguagem:** Python 3.8+
- **Bibliotecas:**
  - `pygame` 🎮 - motor gráfico do jogo
  - `gymnasium` 🏋️ - interface padrão de ambientes de RL
  - `stable-baselines3` 🤖 - algoritmos de aprendizado por reforço
  - `matplotlib` 📊 - visualização de dados
  - `numpy` 🔢 - cálculos numéricos

---

## 🧩 Componentes do Projeto

### 1️⃣ `snake_game.py`
- Contém toda a **lógica do jogo**.
- Implementa funções para:
  - Resetar o jogo (`reset_game`)
  - Renderizar o estado atual (`render_game`)
  - Processar ações (`snake_action`)
- Usa **coordenadas relativas** para ações (frente, esquerda, direita) em vez de direções absolutas.

### 2️⃣ `snake_env.py`
- Implementa a classe `SnakeEnv` compatível com **Gymnasium**.
- Define:
  - `observation_space` e `action_space`
  - Sistema de **recompensas** baseado em:
    - Comer comida 🍎 (+50)
    - Movimento seguro
    - Colisão (-100)
    - Proximidade da comida (recompensa/dedução proporcional)
- Registra pontuações e movimentos no arquivo `scores.txt`.

### 3️⃣ `learning_data.py`
- Lê `scores.txt` e plota gráficos interativos de:
  - 📈 Evolução da **pontuação**
  - 🏃 Evolução da **quantidade de movimentos**
- Possui botões para alternar entre os gráficos.

### 4️⃣ `train_snake.py`
- Configura e treina o modelo A2C.
- Opções para:
  - Treinar (`train()`)
  - Visualizar a IA jogando (`visual_gaming()`)
- Salva e carrega automaticamente o modelo em `snake_model.zip`.

---

## ⚙️ Como Executar

### 1️⃣ Clonar o repositório
```bash
git clone https://github.com/Gabrielnunesilva/snake_game.git
cd snake_game
```

### 2️⃣ Instalar dependências
```bash
pip install pygame gymnasium stable-baselines3 matplotlib numpy
```

### 3️⃣ Treinar o modelo
```bash
python train_snake.py
```

### 4️⃣ Visualizar resultados
```bash
python learning_data.py
```
---

## 🏆 Técnicas Utilizadas

- **Reinforcement Learning** com A2C
- Função de recompensa personalizada
- Observações otimizadas com:
  - Percepção de perigo nas 3 direções
  - Localização relativa da comida
  - Normalização das distâncias
- Sistema de **sugestão de movimentos** para otimizar ações

---

## 📌 Observações

- O ambiente foi projetado para permitir **substituição do algoritmo** de aprendizado facilmente.

---

## 📜 Licença
Este projeto é livre para uso acadêmico e pessoal. 😄


