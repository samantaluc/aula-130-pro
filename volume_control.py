import cv2
import mediapipe as mp
from pynput.keyboard import Key, Controller
import pyautogui

# Inicialização das bibliotecas
keyboard = Controller()
cap = cv2.VideoCapture(0)

# Configuração da janela de exibição
################# ADICIONE OS TRECHOS DE CÓDIGO AQUI

#################

# Tamanhos da janela
################# ADICIONE OS TRECHOS DE CÓDIGO AQUI

#################

# Inicialização do Mediapipe para detecção de mãos
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5)
tipIds = [4, 8, 12, 16, 20]
estado = None

###ATENÇÃO:  ELE IRÁ CONTAR OS DEDOS COM EXCESSÃO DO POLEGAR
def contarDedos(imagem, landmarks_mao, mao_numero=0):
    global estado
    if landmarks_mao:
        landmarks = landmarks_mao[mao_numero].landmark
        dedos = []

        for indice_lm in tipIds:
            y_ponta_dedo = landmarks[indice_lm].y
            y_base_dedo = landmarks[indice_lm - 2].y

            if indice_lm != 4:
                if y_ponta_dedo < y_base_dedo:
                    dedos.append(1)
                else:
                    dedos.append(0)

        totalDedos = dedos.count(1)

        # SE TENHO 4 DEDOS LEVANTADOS, MEU ESTADO É DE REPRODUÇÃO DO VÍDEO
        ################# ADICIONE OS TRECHOS DE CÓDIGO AQUI

        #################
        # SE ABAIXO TODOS MEUS DEDOS E MEU ESTADO ESTAVA EM REPRODUZIR, EU VOU PAUSAR E IDENTIFICAR COMO USA DA BARRA DE ESPAÇO
        ################# ADICIONE OS TRECHOS DE CÓDIGO AQUI

        #################

        x_ponta_dedo = landmarks[8].x * largura
        if totalDedos == 1:
            if x_ponta_dedo < largura - 400:
                print("Reproduzir Para Trás")
                keyboard.press(Key.left)
            if x_ponta_dedo > largura - 50:
                print("Reproduzir Para Frente")
                keyboard.press(Key.right)

        y_ponta_dedo = landmarks[8].y * altura
        if totalDedos == 2:
            if y_ponta_dedo < altura - 250:
                print("Aumentar volume")
                pyautogui.press("volumeup")
            if y_ponta_dedo > altura - 250:
                print("Diminuir volume")
                pyautogui.press("volumedown")

def desenharPontosMao(imagem, landmarks_mao):
    if landmarks_mao:
        for landmarks in landmarks_mao:
            mp_drawing.draw_landmarks(imagem, landmarks, mp_hands.HAND_CONNECTIONS)

while True:
    sucesso, imagem = cap.read()
    if not sucesso:
        break
    
    imagem = cv2.flip(imagem, 1)
    resultados = hands.process(imagem)
    landmarks_mao = resultados.multi_hand_landmarks
    
    desenharPontosMao(imagem, landmarks_mao)
    contarDedos(imagem, landmarks_mao)
    
    cv2.imshow("Controlador de Midia", imagem)

    tecla = cv2.waitKey(1)
    if tecla == 27:  # Tecla Esc para sair
        break

cap.release()
cv2.destroyAllWindows()
