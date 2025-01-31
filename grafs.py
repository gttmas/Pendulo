import matplotlib
matplotlib.use('TkAgg')  # Força o uso do backend TkAgg
import matplotlib.pyplot as plt
import numpy as np

def grafPosicaoxTempo (centers, L, fator, x_central):

    #Gráficos reais

    coordinates_X = []
    coordinates_Y = []
    time = []
    i = 0

    for sublist in centers:
        coordinates_X.append((sublist[0]-x_central)*fator)
        coordinates_Y.append(sublist[1]*fator)
        time.append(i/60)
        i+=1

    plt.plot(time, coordinates_X, marker='o')  # 'o' coloca marcadores nos pontos
    plt.savefig('graficox.png', format='png')
    print("Gráfico salvo como 'graficox.png'.")

    plt.clf()

    plt.plot(time, coordinates_Y, marker='o')
    plt.savefig('graficoy.png', format='png')
    print("Gráfico salvo como 'graficoy.png'.")

    plt.clf()

    #Gráfico ideal

    x0 = centers[0][0] - x_central
    ang_0 = np.arcsin(x0*fator*0.01/L)
    g = 9.81  
    omega = np.sqrt(g / L) 

    ideal_position_X = [L* 100 * np.sin(ang_0 * np.cos(omega * t)) for t in time]
    plt.plot(time, ideal_position_X, label='Ideal - X', linestyle='--')

    plt.savefig('grafico_ideal.png', format='png')
    print("Gráfico da situação ideal salvo como 'grafico_ideal.png'.")


def tabelaTempoxPosicao(centers, fator, x_central):
    tabela = []
    i = 0

    for sublist in centers:
        if i % 59 == 0:
            tabela.append([i/59, (sublist[0]-x_central)*fator, sublist[1]*fator])
        i+=1

    cabecalhos = ["Tempo", "X", "Y"]

    # Criar a figura e os eixos
    fig, ax = plt.subplots(figsize=(16,8))

    # Remover os eixos 
    ax.axis('tight')
    ax.axis('off')

    # Adiciona a tabela na figura e ajustaa a posição e o tamanho
    table_data = np.array(tabela)
    table = ax.table(cellText=table_data, colLabels=cabecalhos, loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1, 1.2)

    # Salvar como uma imagem
    plt.savefig('tabela.png', format='png')

    # Fechar a figura
    plt.close()

    print("Tabela salva como 'tabela.png'.")