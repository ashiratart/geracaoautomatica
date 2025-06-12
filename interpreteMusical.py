import simpleaudio as sa
import numpy as np

def play_note(frequency, duration=0.5):
    fs = 44100  # taxa de amostragem (samples por segundo)
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

def gerar_frequencias():
    notas_frequencias = atribuir_frequencias()
    ntpedida = "A6"  # Pode alterar para outra nota
    frequencia = notas_frequencias.get(ntpedida)
    if frequencia:
        play_note(frequencia)
        print(f"Tocando {ntpedida} com frequência {frequencia:.2f} Hz")
    else:
        print(f"Nota {ntpedida} não encontrada.")

gerar_frequencias()
