import cv2
import mediapipe as mp
import time


class handDetector():
    def __init__(self,mode=False,maxHands=1,detectionCon=0.5,trackCon=0.5):
        self.mode=mode
        self.maxHands=maxHands
        self.detectionCon = detectionCon
        self.trackCon=trackCon

        self.mpHands = mp.solutions.hands
        self.hands=self.mpHands.Hands(self.mode,self.maxHands,self.detectionCon,self.trackCon)
        self.mpDraw =mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.predictions=self.hands.process(imgRGB)
        if self.predictions.multi_hand_landmarks:
            for handLms in self.predictions.multi_hand_landmarks:
                # print(self.predictions.multi_hand_landmarks)
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)

    def findPosition(self,img, handNo=0):
        self.lmList=[]
        if self.predictions.multi_hand_landmarks:
            myHand= self.predictions.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmList.append([id,cx,cy])
        return self.lmList

    def countTheFingersUp(self,img):
        tipIds = [4, 8, 12, 16, 20]
        self.fingers = []
        if len(self.lmList) != 0:
            if self.lmList[tipIds[0]][1] < self.lmList[tipIds[0] - 1][1]:
                self.fingers.append(1)
            else:
                self.fingers.append(0)
            for id in range(1, 5):
                if self.lmList[tipIds[id]][2] < self.lmList[tipIds[id] - 2][2]:
                    self.fingers.append(1)
                else:
                    self.fingers.append(0)
        return sum(self.fingers), self.fingers




def main():
    ptime = 0
    ctime = 0
    cap = cv2.VideoCapture(0)
    detector= handDetector()

    while True:
        ret, img = cap.read()

        if ret == False:
            break
        img = detector.findHands(img)
        lmList=detector.findPosition(img)
        print(lmList)

        ctime = time.time()
        fps = 1 / (ctime - ptime)
        ptime = ctime
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_ITALIC, 3, (255, 0, 255), 2)

        cv2.imshow("Hand", img)
        k = cv2.waitKey(1)

        if k == 27:
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()