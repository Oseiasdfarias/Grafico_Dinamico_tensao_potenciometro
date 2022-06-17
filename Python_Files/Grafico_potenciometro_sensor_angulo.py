import serial
from threading import Thread
from time import sleep
import matplotlib.pyplot as plt
from matplotlib import animation, text
import numpy as np
import sys

plt.style.use("ggplot")

porta = "/dev/ttyUSB0"
baud_rate = 9600

fila = []
def ler_dados():
    global fila
    try:
        disp = serial.Serial(porta, baud_rate)
        while disp.is_open:
            try:
                dado = disp.readline()
                dados1 = str(dado.decode('utf8')).rstrip("\n")
                try:
                    dados_float = float(dados1)
                    if len(fila) <= 51:
                        graus = ((300.0*dados_float)/4095.0)
                        fila.append(graus)
                    else:
                        fila.pop(0)
                        print(f"Graus: {graus}°")
                except Exception as erro:
                    print(f"Erro: {erro}")
                sleep(0.03)
            except serial.SerialException:
                print("Erro de leitura ...")
                break
        if not disp.is_open:
            disp.close()
            print("Close ...")
    except serial.SerialException:
        print("Erro de conexão...")

# Thread responsável por rodar a função que se comunica com 
# o Esp32 e colhe os dados e os processa.
thread = Thread(target=ler_dados)
thread.daemon = True
thread.start()

sleep(2.0)
# Configuração do Matplotlib para plotagem do Gráfico.
fig, ax = plt.subplots(figsize=(8, 5))
plt.yticks(range(0, 301, 20), label="°")
plt.xticks(range(0, 51, 2))
plt.subplots_adjust(bottom=0.115, top=0.915, 
                    right=0.965, left=0.110)
x_data = np.linspace(0, 49, 50)
ln, = ax.plot(x_data, x_data, lw=1.2)
tx  = ax.text(45, int(fila[-1]+10), f"{fila[-1]}",
              color=[0.3,0.3,0.5],
              fontsize=12,
              fontweight="bold")

plt.axhline(0, color='dimgray', lw=1)
plt.axvline(0, color='dimgray', lw=1)
plt.xlabel("Tempo (s)", color='dimgray',
           fontdict={
               'fontsize': 12,
               'fontweight': 'medium'
           },
           fontweight="bold")
plt.ylabel("Ângulo (G°)", color='dimgray',
           fontdict={
               'fontsize': 12,
               'fontweight': 'medium'
           },
           fontweight="bold")

# Inicializa as configurações no gráfico quando inicializa a plotagem dinâmica.
def init():
    ax.set_ylim(-30, 330)
    ax.set_title("Sensor de Ângulo com Potenciômetro",
                 color='dimgray',
                 fontdict={
                     'fontsize': 18,
                     'fontweight': 'medium'},
                 fontweight="bold")
    tx.set_y(int(fila[-1])+10)
    tx.set_text(f"{fila[-1]}")
    return ln, tx

# Atualiza o gráfico, é passado como parâmetro para a Classe FuncAnimation.
def update(filaup):
    ln.set_data(x_data, fila[:50])
    ln.set_linestyle("-.")
    ln.set_marker(".")
    tx.set_y(int(fila[-1])+10)
    tx.set_text(f"{fila[-1]:.2f} °")
    return ln, tx

# Gerencia a Plotagem dinâmica do Gráfico.
anima = animation.FuncAnimation(fig,
                                update,
                                init_func=init,
                                interval=30)
plt.show()
sys.exit()

