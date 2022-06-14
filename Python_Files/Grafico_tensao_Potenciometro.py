import serial
from threading import Thread
from time import sleep
import matplotlib.pyplot as plt
from matplotlib import animation
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
                        tensao = ((5.0*dados_float)/4095.0)
                        fila.append(tensao)
                    else:
                        fila.pop(0)
                        # print(fila)
                        print(f"Leitura: {tensao} | type: {type(tensao)}")
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
new_thread = Thread(target=ler_dados)
new_thread.daemon = True
new_thread.start()

sleep(2.0)
# Configuração do Matplotlib para plotagem do Gráfico.
fig, ax = plt.subplots(figsize=(7, 5))
plt.subplots_adjust(bottom=0.105, top=0.935, 
                    right=0.965, left=0.075)
x_data = np.linspace(0, 49, 50)
ln, = plt.plot(x_data, x_data, lw=0.9)
plt.axhline(0, color='gray', lw=1)
plt.axvline(0, color='gray', lw=1)
plt.xlabel("Tempo (s)", color='gray', fontdict={'fontsize': 12, 'fontweight': 'medium'})
plt.ylabel("Tensão (V)", color='gray', fontdict={'fontsize': 12, 'fontweight': 'medium'})

# Inicializa as configurações no gráfico quando inicializa a plotagem dinâmica.
def init():
    ax.set_ylim(-0.5, 5.5)
    ax.set_title("Potenciômetro", color='gray', fontdict={'fontsize': 20, 'fontweight': 'medium'})
    return ln,

# Atualiza o gráfico, é passado como parâmetro para a Classe FuncAnimation.
def update(filaup):
    ln.set_data(x_data, fila[:50])
    return ln,

# Gerencia a Plotagem dinâmica do Gráfico.
anima = animation.FuncAnimation(fig, update, init_func=init, interval=30)
plt.show()
sys.exit()

