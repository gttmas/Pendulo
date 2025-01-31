import cv2
import numpy as np
from grafs import grafPosicaoxTempo
from grafs import tabelaTempoxPosicao

# Caminhos para os arquivos de vídeo de entrada e saída
video_input_path = 'pendulo_video.mp4'  
video_output_path = 'output_video.mp4'  

# Abrir o arquivo de vídeo de entrada e verifica se foi aberto corretamente
cap = cv2.VideoCapture(video_input_path)
if not cap.isOpened():
    print("Erro ao abrir o vídeo!")
    exit()

# Obter as propriedades do vídeo de entrada
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  
fps = min(cap.get(cv2.CAP_PROP_FPS), 30)  # Ajustar FPS

fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec para .mp4
out = cv2.VideoWriter(video_output_path, fourcc, fps, (width, height))


lower_orange = np.array([0, 150, 150])  
upper_orange = np.array([20, 255, 255])

centers = [] # Lista para armazenar as coordenadas dos centros
L = 0.62
fator = 0.00375 # relação entre pixels e centímetros: 1 pixel = 0,00375 cm (calculado a partir do PPI)
X_central = 3840/2

while True:
    ret, frame = cap.read()  # Ler um frame do vídeo de entrada

    # Se não conseguir fim do vídeo
    if not ret:
        break

    # Converter o frame para o espaço de cor HSV
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Criar a máscara com base no intervalo de cor laranja
    mask = cv2.inRange(hsv_frame, lower_orange, upper_orange)

    # Refinar a máscara com operações morfológicas
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    # Encontrar contornos na máscara
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Desenhar os contornos encontrados no frame original
    for contour in contours:
        if cv2.contourArea(contour) > 500:  
            # Obter o retângulo delimitador ao redor do contorno
            x, y, w, h = cv2.boundingRect(contour)

            # Calcular e salvar as coordenadas do centro do retângulo
            center_x = x + w // 2
            center_y = y + h // 2

            centers.append([center_x, center_y])

            # Desenhar um retângulo em volta do objeto
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2) 
            
            cv2.circle(frame, (center_x, center_y), 5, (255, 0, 0), -1)  # "centro" do retângulo

    # Salvar o frame no vídeo de saída
    out.write(frame)

# Liberar os recursos
cap.release()
out.release()

print("Vídeo de saída salvo com sucesso!")

grafPosicaoxTempo(centers, L, fator, X_central)
tabelaTempoxPosicao(centers, fator, X_central)
