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
                        fila.append(dados_float)
                    else:
                        fila.pop(0)
                        # print(fila)
                        print(f"Leitura: {dados_float} | type: {type(dados_float)}")
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

new_thread = Thread(target=ler_dados)
new_thread.daemon = True
new_thread.start()

sleep(2)
fig, ax = plt.subplots(figsize=(7, 5))
plt.subplots_adjust(bottom=0.05, top=0.935, 
                    right=0.965, left=0.070)
x_data = np.linspace(0, 49, 50)
y_data = np.ones(50)
ln, = plt.plot(x_data, y_data, lw=0.9)

def init():
    ax.set_ylim(-400, 4400)
    ax.set_title("Potenciômetro", fontdict={'fontsize': 18, 'fontweight': 'medium'})
    return ln,

def Plot_Data(filaup):
    ln.set_data(x_data, fila[:50])
    return ln,

anima = animation.FuncAnimation(fig, Plot_Data, init_func=init, interval=30)
plt.show()
sys.exit()

