import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

frame_count = 0

try:
    with mp_hands.Hands(min_detection_confidence=0.7) as hands:
        while True:
            success, frame = cap.read()
            if not success:
                print("Erro ao capturar a imagem")
                break

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = hands.process(frame_rgb)

            if result.multi_hand_landmarks:
                for hand_landmarks in result.multi_hand_landmarks:
                    mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                    for id, lm in enumerate(hand_landmarks.landmark):
                        h, w, c = frame.shape
                        cx, cy = int(lm.x * w), int(lm.y * h)
                        if id == 8:
                            cv2.circle(frame, (cx, cy), 10, (255, 0, 255), cv2.FILLED)
                            print(f"Posição dedo indicador: x={cx} y={cy}")

            frame_count += 1
            if frame_count % 30 == 0:
                print(f"{frame_count} frames capturados e processados...")

            cv2.imshow("Mao", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

except KeyboardInterrupt:
    print("\nInterrompido pelo usuário.")

finally:
    print("Liberando recursos...")
    cap.release()
    cv2.destroyAllWindows()
