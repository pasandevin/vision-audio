import time
import tkinter as tk
import HandTrackModule
import math
import Player
import cv2
import numpy as np
import threading


class PlaybackDetector():
    def __init__(self,mode=False,maxHands=1,detectionCon=0.5,trackCon=0.5):
        self.handDetector=HandTrackModule.handDetector(mode,maxHands,detectionCon,trackCon)
        self.timeMode={}
        self.mode="Pause"
        self.volmmode=False
        self.changeTrackMode=False
        self.changeTrackFlag=False
        self.trackChangeCount=0

        #Intialize Player: Thread1
        def inplayer():
            self.root = tk.Tk()
            self.root.geometry('600x400')
            self.root.wm_title('Vision_Player')
            self.app = Player.Player(master=self.root)
            self.app.mainloop()

        # getting Predictions: Thread2
        def inpredict():
            self.ptime = 0
            self.ctime = 0
            self.cap = cv2.VideoCapture(0)

            while True:
                self.ret, self.img = self.cap.read()
                self.img = cv2.flip(self.img, 1)
                if self.ret == False:
                    break

                #Calculate FrameRate
                self.detectionMode(self.img)
                self.ctime = time.time()
                self.fps = 1 / (self.ctime - self.ptime)
                self.ptime = self.ctime
                cv2.putText(self.img, str(int(self.fps)), (10, 70), cv2.FONT_ITALIC, 3, (255, 0, 255), 2)

                #Displaying Predictions
                cv2.imshow("Hand", self.img)
                self.k = cv2.waitKey(1)

                if self.k == 27:
                    break

            cv2.destroyAllWindows()

        #Multithreding
        threading.Thread(target=inplayer).start()
        threading.Thread(target=inpredict).start()

    def detectionMode(self,img):
        self.prevmode=self.mode
        self.handDetector.findHands(img)
        self.lmlist=self.handDetector.findPosition(img)

        if len(self.lmlist) != 0:
            self.fingercount, self.fingerlist = self.handDetector.countTheFingersUp(img)

            #For volume and changetrack modes
            if self.fingerlist == [1,1,0,0,0]:
                self.volmmode= True
            elif self.fingerlist==[0 , 1, 1, 1, 1]:
                self.changeTrackMode=True
            else:
                self.changeTrackMode=False
                self.volmmode = False
                self.trackChangeCount=0

            #For PlayPause
            if self.fingerlist == [1, 1, 1, 1, 1]:
                self.mode = "Play"
            elif self.fingerlist == [0,0,0,0,0]:
                self.mode= "Pause"
            # call volume function
            if self.volmmode== True:
                self.changeVol(img)

            # Call change track function
            elif self.changeTrackMode== True:
                self.changeTrack()

            # call function for play pause
            elif self.prevmode!= self.mode and self.mode=='Play' and self.app.paused== True:    #For continue
                self.app.pause_song()
            elif self.prevmode!= self.mode and self.mode=='Pause' and self.app.paused == False:      #For pause
                self.app.pause_song()

    def changeVol(self,img):
        x1,y1= self.lmlist[4][1],self.lmlist[4][2]
        x2, y2 = self.lmlist[8][1], self.lmlist[8][2]
        cv2.line(img,(x1,y1),(x2,y2),(255,0,0),3)
        dist = math.hypot(x2 - x1, y2 - y1)
        vol=(np.interp(dist,[50,300],[0,10]))
        self.app.change_volume_vision(vol)

    def changeTrack(self):
        self.timeMode[round(float(time.time()),1)]= self.lmlist[8][1]
        try:
            if len(self.timeMode)> 10:
                if self.lmlist[8][1]< self.timeMode[round(float(time.time()),1)-1]-150 and self.trackChangeCount==0:
                    self.app.prev_song()
                    self.trackChangeCount += 1
                elif self.lmlist[8][1]> self.timeMode[round(float(time.time()),1)-1]+150 and self.trackChangeCount==0:
                    self.app.next_song()
                    self.trackChangeCount += 1
        except Exception as e:
            pass

def main():
    play=PlaybackDetector()
if __name__ == "__main__":
    main()