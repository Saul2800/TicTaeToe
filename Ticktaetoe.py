#TicaTacToe
#Saul Arenas
#Python**Mediapipe**OpenCV

import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

class Game:    
    def __init__ (self):
        self.table = [[' ' for _ in range(3)] for _ in range(3)]
        self.marked_positions = {1: [], 2: []}
        self.markeds_positions = []
        self.current_color=(0,255,0)
        self.color2=(0,255,0)
        self.turn=0

    def table_show(self,frame):
        for i in range(3):
            for j in range(3):
                # SQUARE
                x1 = 100 + i * 100
                y1 = 100 + j * 100
                x2 = x1 + 100
                y2 = y1 + 100
                
                # DRAW SQUARE
                cv2.line(frame, (x1, y1), (x2, y1), (255, 255, 255), 5)  # LINE  X TOP
                cv2.line(frame, (x1, y2), (x2, y2), (255, 255, 255), 5)  # LINE X BOT
                cv2.line(frame, (x1, y1), (x1, y2), (255, 255, 255), 5)  # LINE Y LEFT
                cv2.line(frame, (x2, y1), (x2, y2), (255, 255, 255), 5)  # LINE Y RIGHT
                cv2.putText(frame, ' R to reset  ', (400, 400), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)
                cv2.putText(frame, ' Q to exit  ', (400, 450), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)

                '''
                # Center
                center_x = x1 + 50
                center_y = y1 + 50

                # Number
                number = i * 3 + j + 1
                print("X ",center_x,"Y ",center_y,"#",number)
                
                # Put number center
                cv2.putText(frame, str(number), (center_x - 10, center_y + 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                
                X  150 Y  150 # 1
                X  150 Y  250 # 2
                X  150 Y  350 # 3
                X  250 Y  150 # 4
                X  250 Y  250 # 5
                X  250 Y  350 # 6
                X  350 Y  150 # 7
                X  350 Y  250 # 8
                X  350 Y  350 # 9'
                '''
                
        return frame  
    
    def mark(self, frame, cordenada):
        mark=None
        if cordenada and len(cordenada) == 2:
            #Define all the square
            if 100 < cordenada[0] < 400 and 100 < cordenada[1] < 400:
            #Define each square
                if 100 < cordenada[0] < 200 and 100 < cordenada[1] < 200:
                    new_mark = (150, 150)
                    mark=1
                if 200 < cordenada[0] < 300 and 100 < cordenada[1] < 200:
                    new_mark = (250, 150)
                    mark=2
                if 300 < cordenada[0] < 400 and 100 < cordenada[1] < 200:
                    new_mark = (350, 150)
                    mark=3

                if 100 < cordenada[0] < 200 and 200 < cordenada[1] < 300:
                    new_mark = (150, 250)
                    mark=4
                if 200 < cordenada[0] < 300 and 200 < cordenada[1] < 300:
                    new_mark = (250, 250)
                    mark=5
                if 300 < cordenada[0] < 400 and 200 < cordenada[1] < 300:
                    new_mark = (350, 250)
                    mark=6

                if 100 < cordenada[0] < 200 and 300 < cordenada[1] < 400:
                    new_mark = (150, 350)
                    mark=7
                if 200 < cordenada[0] < 300 and 300 < cordenada[1] < 400:
                    new_mark = (250, 350)
                    mark=8
                if 300 < cordenada[0] < 400 and 300 < cordenada[1] < 400:
                    new_mark = (350, 350)
                    mark=9
                    
                if mark not in self.marked_positions[1] and mark not in self.marked_positions[2]:
                    player = 1 if self.turn % 2 == 0 else 2
                    self.current_color = (0, 255, 0) if player == 1 else (0, 0, 255)
                    self.color2 = (0, 0, 255) if player == 1 else (0, 255, 0)
                    self.marked_positions[player].append(mark)
                    self.markeds_positions.append((new_mark, self.current_color, self.color2))
                    self.turn += 1

        for pos, color, color2 in self.markeds_positions:
            cv2.circle(frame, pos, 10, color, -1)
            cv2.putText(frame, ' PLAY ', (450, 250), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color2, 2)
        
        self.check_winner(frame)
    
    def check_winner(self, frame):
        win_conditions = [
            [1, 2, 3], [4, 5, 6], [7, 8, 9],
            [1, 4, 7], [2, 5, 8], [3, 6, 9],
            [1, 5, 9], [3, 5, 7]
        ]
        pos_to_coords = {
            1: (150, 150), 2: (250, 150), 3: (350, 150),
            4: (150, 250), 5: (250, 250), 6: (350, 250),
            7: (150, 350), 8: (250, 350), 9: (350, 350)
        }
        for player in [1, 2]:
            for condition in win_conditions:
                if all(pos in self.marked_positions[player] for pos in condition):
                    winner_color = (0, 255, 0) if player == 1 else (0, 0, 255)
                    cv2.putText(frame, f' PLAYER {player} WINS! ', (150, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, winner_color, 3)
                    start, mid, end = [pos_to_coords[p] for p in condition]
                    cv2.line(frame, start, end, winner_color, 5)
                    return True
        return False

class Hands:
    def __init__(self):
        self.hands = mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.5
        )
        self.cordenada=[]

    def detect_hand_gesture(self, frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(frame_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                #mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # INDEX AND THUMB
                height, width, _ = frame.shape
                index = hand_landmarks.landmark[8]
                thumb = hand_landmarks.landmark[4]

                xi, yi = int(index.x * width), int(index.y * height)
                xt, yt = int(thumb.x * width), int(thumb.y * height)

                cv2.circle(frame, (xi, yi), 10, (0, 255, 0), -1)  # INDEX
                cv2.circle(frame, (xt, yt), 10, (0, 0, 255), -1)  # THUMB

                # DETECT IF THUMB AND INDEX TOUCH
                if abs(xt - xi) <= 10 and abs(yt - yi) <= 10:
                    cv2.circle(frame, (xi, yi), 40, (255, 255, 255), -1)
                    #print(f"Thumb: {xt, yt} | Index: {xi, yi}")
                    self.cordenada=[xi,yi]
                    #print(self.cordenada," CORDENDADA")
                    return self.cordenada


        return frame

#Open camera
cap = cv2.VideoCapture(0)
game = Game()
hand = Hands()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    frame = cv2.flip(frame, 1)
    game.table_show(frame)
    hand.detect_hand_gesture(frame)
    game.mark(frame, cordenada=hand.cordenada)

    cv2.imshow('Tic Tac Toe', frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('r'):
        game = Game()
        hand = Hands()
cap.release()
cv2.destroyAllWindows()