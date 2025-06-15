import simpleaudio as sa
import numpy as np
import cv2
import mediapipe as mp


def play_note(frequency, duration=0.5):
    fs = 44100
    t = np.linspace(0, duration, int(fs * duration), False)
    note = np.sin(frequency * t * 2 * np.pi)
    audio = note * (2**15 - 1) / np.max(np.abs(note))
    audio = audio.astype(np.int16)
    play_obj = sa.play_buffer(audio, 1, 2, fs)
    play_obj.wait_done()


def calcula_resultados():
    A = 440
    resultados = []
    for n in range(25):
        resultado = A * 2 ** (n / 12)
        resultados.append(resultado)
    return resultados


def atribuir_frequencias():
    frequencias = calcula_resultados()
    notas = [
        "A4", "A#4", "B4", "C5", "C#5", "D5", "D#5", "E5", "F5", "F#5", "G5", "G#5",
        "A5", "A#5", "B5", "C6", "C#6", "D6", "D#6", "E6", "F6", "F#6", "G6", "G#6",
        "A6"
    ]
    notas_frequencias = {nota: frequencias[i] for i, nota in enumerate(notas)}
    return notas_frequencias


def mapear_posicao_para_nota(x, largura_frame, notas_frequencias):
    num_teclas = len(notas_frequencias)
    intervalo = largura_frame // num_teclas
    indice_nota = min(x // intervalo, num_teclas - 1)
    nota = list(notas_frequencias.keys())[indice_nota]
    return nota, indice_nota, intervalo


def desenhar_teclado(frame, num_teclas, tecla_ativa):
    altura = frame.shape[0]
    largura = frame.shape[1]
    intervalo = largura // num_teclas

    for i in range(num_teclas):
        x_inicio = i * intervalo
        x_fim = x_inicio + intervalo

        if i == tecla_ativa:
            cor = (0, 255, 0)  # Verde para tecla ativa
        else:
            cor = (255, 255, 255)  # Branco para teclas inativas

        cv2.rectangle(frame, (x_inicio, altura - 100), (x_fim, altura), cor, -1)
        cv2.rectangle(frame, (x_inicio, altura - 100), (x_fim, altura), (0, 0, 0), 2)


def ver():
    mp_hands = mp.solutions.hands
    mp_draw = mp.solutions.drawing_utils
    notas_frequencias = atribuir_frequencias()
    nota_atual = None

    cap = cv2.VideoCapture(0)
    frame_count = 0
    num_teclas = len(notas_frequencias)

    try:
        with mp_hands.Hands(min_detection_confidence=0.7) as hands:
            while True:
                success, frame = cap.read()
                if not success:
                    print("Erro ao capturar a imagem")
                    break

                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                result = hands.process(frame_rgb)

                tecla_ativa = -1

                if result.multi_hand_landmarks:
                    for hand_landmarks in result.multi_hand_landmarks:
                        mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                        for id, lm in enumerate(hand_landmarks.landmark):
                            h, w, c = frame.shape
                            cx, cy = int(lm.x * w), int(lm.y * h)
                            if id == 8:  # Dedo indicador
                                cv2.circle(frame, (cx, cy), 10, (255, 0, 255), cv2.FILLED)

                                nota_detectada, indice_nota, intervalo = mapear_posicao_para_nota(cx, w, notas_frequencias)

                                if nota_detectada != nota_atual:
                                    frequencia = notas_frequencias[nota_detectada]
                                    print(f"Tocando {nota_detectada} ({frequencia:.2f} Hz)")
                                    play_note(frequencia, duration=0.3)
                                    nota_atual = nota_detectada

                                tecla_ativa = indice_nota

                desenhar_teclado(frame, num_teclas, tecla_ativa)

                frame_count += 1
                if frame_count % 30 == 0:
                    print(f"{frame_count} frames capturados e processados...")

                cv2.imshow("Teclado Musical - Pressione 'q' para sair", frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
    except KeyboardInterrupt:
        print("\nInterrompido pelo usuário.")
    finally:
        print("Liberando recursos...")
        cap.release()
        cv2.destroyAllWindows()


def main():
    print("Bem-vindo ao simulador musical com visão computacional!")
    print("\nEste teclado virtual responde à posição do seu dedo indicador.")
    print("Programa desenvolvido por: Acácio Mariano, estudante de Engenharia de Eletrônica, UniEnsino, 2025\n")
    print("Para iniciar, pressione 'i'.\n"
          "Para sair, pressione 's'.\n")
    while True:
        opcao = input("=> ").strip().lower()
        if opcao == 'i':
            ver()
        elif opcao == 's':
            print("Saindo do programa...")
            break
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()
