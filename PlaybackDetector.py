import time
import tkinter as tk
import HandTrackModule
import math
import Player
import cv2
import numpy as np
import threading
import os


class PlaybackDetector():
    def __init__(self,mode=False,maxHands=1,detectionCon=0.5,trackCon=0.5):
        self.handDetector=HandTrackModule.handDetector(mode,maxHands,detectionCon,trackCon)
        self.fingertipindex=[4,8,12,16,20]
        self.timeMode={}
        self.mode="Pause"
        self.volmmode=False
        self.changeTrackMode=False
        self.changeTrackFlag=False

        #Intialize Player: Thread1
        def inplayer():
            self.root = tk.Tk()
            self.root.geometry('600x400')
            self.root.wm_title('Vison Audio')
            self.app = Player.Player(master=self.root)
            self.app.mainloop()

        # getting Predictions: Thread2
        def inpredict():
            ptime = 0
            cap = cv2.VideoCapture(0)

            while True:
                ret, self.img = cap.read()
                self.img = cv2.flip(self.img, 1)
                self.img = cv2.resize(self.img, (640,480), interpolation=cv2.INTER_AREA)
                # print(self.img.shape)
                if ret == False:
                    break

                #Calculate FrameRate
                self.detect(self.img)
                self.ctime = time.time()
                fps = 1 / (self.ctime - ptime)
                ptime = self.ctime
                cv2.putText(self.img, "framerate: "+str(int(fps)), (440, 120), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,255,255), 2)


                #Displaying Predictions
                cv2.imshow("Gesture Detection", self.img)
                k = cv2.waitKey(1)

                if k == 27:
                    break

            cv2.destroyAllWindows()
            cap.release()

        #Multithreding
        threading.Thread(target=inplayer).start()
        threading.Thread(target=inpredict).start()

    def detect(self,img):
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
                self.changeTrackFlag=False

            #For PlayPause
            if self.fingerlist == [1, 1, 1, 1, 1]:
                self.mode = "Play"
                #Visualizations
                cv2.rectangle(img, (0, 0), (img.shape[1], 80), (255, 0, 0), -1)
                cv2.putText(img, "Playing: ", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 72, 255), 2)
                cv2.putText(img, os.path.basename(self.app.playlist[self.app.current]), (70, 60), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,255,0), 2)


            elif self.fingerlist == [0,0,0,0,0]:
                self.mode= "Pause"
                #Visualizations
                cv2.rectangle(img, (0, 0), (img.shape[1], 80), (255, 0, 0), -1)
                cv2.putText(img, "Paused", (180, 60), cv2.FONT_HERSHEY_TRIPLEX, 2, (0, 0, 255), 5)
                for id in self.fingertipindex:
                    cv2.circle(self.img,(self.lmlist[id][1],self.lmlist[id][2]),4,(0,0,255),-1)


            # call volume function
            if self.volmmode== True:
                self.changeVol(img)

            # Call change track function
            elif self.changeTrackMode== True:
                cv2.rectangle(img, (0, 0), (img.shape[1], 80), (255, 0, 0), -1)
                cv2.putText(img, "Change Track", (100,60), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 5)
                p11 = (80, 20)
                p12 = (50, 40)
                p13 = (80, 60)
                cv2.line(img, p11, p12, (0, 0, 255), 3)
                cv2.line(img, p12, p13, (0, 0, 255), 3)
                cv2.line(img, p13, p11, (0, 0, 255), 3)
                p21 = (545, 20)
                p22 = (575, 40)
                p23 = (545, 60)
                cv2.line(img, p21, p22, (0, 0, 255), 3)
                cv2.line(img, p22, p23, (0, 0, 255), 3)
                cv2.line(img, p23, p21, (0, 0, 255), 3)
                for id in self.fingertipindex[1:]:
                    cv2.circle(self.img,(self.lmlist[id][1],self.lmlist[id][2]),4,(0,0,255),-1)
                self.changeTrack()

            # call function for play pause
            else:
                self.checkplaypause()
    def checkplaypause(self):
        if self.prevmode!= self.mode and self.mode=='Play' and self.app.paused== True:    #For continue
            self.app.pause_song()
        elif self.prevmode!= self.mode and self.mode=='Pause' and self.app.paused == False:      #For pause
            self.app.pause_song()

    def changeVol(self,img):
        x1,y1= self.lmlist[4][1],self.lmlist[4][2]
        x2, y2 = self.lmlist[8][1], self.lmlist[8][2]


        dist = math.hypot(x2 - x1, y2 - y1)
        lowerdist=50
        maxdist=280
        vol=np.interp(dist,[lowerdist,maxdist],[0,10])
        self.app.change_volume_vision(vol)

        # Visualizations
        cv2.rectangle(img, (0, 0), (img.shape[1], 80),(255,0,0) , -1)
        cv2.putText(img,"Change Volume",(60,60),cv2.FONT_HERSHEY_TRIPLEX,2,(0, 72, 255),5)
        cv2.line(img, (x1, y1), (x2, y2), (0, 72, 255), 6)
        cv2.circle(img, (x1, y1), 6, (0, 0, 255), -1)
        cv2.circle(img, (x2, y2), 6, (0, 0, 255), -1)

        scaleforrec = np.interp(dist, [lowerdist,maxdist], [400,120])
        # print(scale)
        if vol < 8:
            cv2.rectangle(self.img, (20, 120), (60, 400), (0, 255, 0), 2)
            cv2.rectangle(self.img, (20, 400), (60, int(scaleforrec)), (0, 255, 0), -1)
            cv2.putText(self.img, "Volume", (10, 430), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,255,0), 2)
            cv2.putText(self.img, str(round(vol*10))+"%", (20, 110), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 0), 2)
            # print("<0.8")
        elif vol >= 8:
            cv2.rectangle(self.img, (20, 120), (60, 400), (0, 0,255), 2)
            cv2.rectangle(self.img, (20, 400), (60, int(scaleforrec)), (0 ,0, 255), -1)
            cv2.putText(self.img, "Volume", (10, 430), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,(0, 0, 255), 2)
            cv2.putText(self.img, str(round(vol*10))+"%", (20, 110), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), 2)
            # print(">0.8")


    def changeTrack(self):
        self.timeMode[round(float(time.time()),1)]= self.lmlist[8][1]
        try:
            if len(self.timeMode)> 10:
                if self.lmlist[8][1]< self.timeMode[round(float(time.time()),1)-1]-150 and self.changeTrackFlag==False:
                    self.app.prev_song()
                    self.changeTrackFlag=True
                elif self.lmlist[8][1]> self.timeMode[round(float(time.time()),1)-1]+150 and self.changeTrackFlag==False:
                    self.app.next_song()
                    self.changeTrackFlag =True
        except Exception as e:
            pass

def main():
    play=PlaybackDetector()
if __name__ == "__main__":
    main()