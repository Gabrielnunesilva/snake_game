import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import os

# Caminho do arquivo
file_path = os.path.dirname(os.path.abspath(__file__)) + '\\scores.txt'

scores = []
steps = []
discard = 20000

def read_data():
    global scores, steps
    scores.clear()
    steps.clear()
    if not os.path.exists(file_path):
        print("Arquivo não encontrado.")
        return

    with open(file_path, "r") as file:
        line = file.read().strip()
        if line:
            entries = [entry.strip() for entry in line.split(",") if "/" in entry]
            for entry in entries:
                try:
                    x, y = map(int, entry.split("/"))
                    scores.append(x)
                    if y < discard:
                        steps.append(y)
                except ValueError:
                    continue

def plot_data(mode="scores"):
    ax_main.clear()

    if not scores or not steps:
        print("Nenhum dado válido encontrado.")
        return

    data = scores if mode == "scores" else steps
    ylabel = "Pontuação" if mode == "scores" else "Quantidade de Movimentos"
    title = "Evolução das Pontuações" if mode == "scores" else "Evolução dos Movimentos por Jogo"
    color = "blue" if mode == "scores" else "green"

    cumulative_avg = [sum(data[:i+1]) / (i+1) for i in range(len(data))]

    ax_main.bar(range(1, len(data) + 1), data, color=color, alpha=0.6, label=mode.capitalize())
    ax_main.plot(range(1, len(data) + 1), cumulative_avg, linestyle="--", color="red", label="Média acumulada")
    ax_main.set_title(title, fontsize=14)
    ax_main.set_xlabel("Episódios", fontsize=12)
    ax_main.set_ylabel(ylabel, fontsize=12)
    ax_main.grid(True, linestyle="--", alpha=0.6)
    ax_main.legend()
    plt.draw()

# Funções dos botões
def on_scores_clicked(event):
    plot_data("scores")

def on_steps_clicked(event):
    plot_data("steps")

# --- Configuração do layout ---
read_data()
fig, ax_main = plt.subplots(figsize=(13, 6))
plt.subplots_adjust(left=0.08, right=0.98, top=0.95, bottom=0.25)  # espaço extra inferior para os botões

# Criação dos botões horizontais (abaixo do eixo X)
ax_button_scores = fig.add_axes([0.1, 0.08, 0.1, 0.05])  # [esq, baixo, largura, altura]
ax_button_steps = fig.add_axes([0.22, 0.08, 0.1, 0.05])

btn_scores = Button(ax_button_scores, 'Pontuações')
btn_steps = Button(ax_button_steps, 'Movimentos')

btn_scores.on_clicked(on_scores_clicked)
btn_steps.on_clicked(on_steps_clicked)

# Primeiro gráfico
plot_data("scores")
plt.show()

