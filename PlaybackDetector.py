import cv2
import time
import tkinter as tk
import HandTrackModule
import math
import numpy as np


#For main
import threading
import Player




class PlaybackDetector():
    def __init__(self,mode=False,maxHands=1,detectionCon=0.5,trackCon=0.5):
        self.handDetector=HandTrackModule.handDetector(mode,maxHands,detectionCon,trackCon)


        # #Intializing the Player
        # self.mPlayer= Player.Player()
        # self.root=tk.tK()
        # self.root.geometry('600x400')
        # self.root.wm_title('Player')
        # self.app= self.mPlayer(master=self.root)
        # self.app.mainloop()


    #----------------------------------------------

        def inplayer():

            self.root = tk.Tk()
            self.root.geometry('600x400')
            self.root.wm_title('Musicxy')
            self.app = Player.Player(master=self.root)

            self.app.mainloop()

        # getting Predictions
        def inpredict():
            self.ptime = 0
            self.ctime = 0
            self.cap = cv2.VideoCapture(0)
            # HandTrack= HandTrackModule.handDetector(detectionCon=0.6,trackCon=0.7)

            while True:
                self.ret, self.img = self.cap.read()
                self.img = cv2.flip(self.img, 1)

                # cv2.flip(img,0)
                if self.ret == False:
                    break

                self.detectionMode(self.img)
                self.ctime = time.time()
                self.fps = 1 / (self.ctime - self.ptime)
                self.ptime = self.ctime

                cv2.putText(self.img, str(int(self.fps)), (10, 70), cv2.FONT_ITALIC, 3, (255, 0, 255), 2)

                cv2.imshow("Hand", self.img)
                self.k = cv2.waitKey(1)

                if self.k == 27:
                    break

            cv2.destroyAllWindows()

        threading.Thread(target=inplayer).start()
        threading.Thread(target=inpredict).start()

#----------------------------------------------------------------





        self.timeMode={}
        self.mode="Pause"
        self.volmmode=False
        self.changeTrackMode=False





    def detectionMode(self,img):
        self.prevmode=self.mode



        # self.ctime=time.time()
        # print(self.now)
        self.handDetector.findHands(img)
        self.lmlist=self.handDetector.findPosition(img)

        if len(self.lmlist) != 0:
            self.idexfingerpos = self.lmlist[8]
            # self.timeMode[int(self.ctime)]=self.idexfingerpos
        # print(self.timeMode)
        # print('-----------------------')
        # print(lmList)


            self.fingercount, self.fingerlist = self.handDetector.countTheFingersUp(img)
            # print(self.fingerlist, self.fingercount)




            #For volume and changetrack modes
            if self.fingerlist == [1,1,0,0,0]:
                self.volmmode= True

            elif self.fingerlist==[0 , 1, 1, 1, 1]:
                self.changeTrackMode=True
            else:
                self.changeTrackMode=False
                self.volmmode = False

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


            # call change function for play pause
            elif self.prevmode!= self.mode and self.mode=='Play' and self.app.paused== True:    #For continue
                # print("play")
                self.app.pause_song()
            elif self.prevmode!= self.mode and self.mode=='Pause' and self.app.paused == False:      #For pause
                # print("pause")
                self.app.pause_song()

            # print(self.mode)
    def changeVol(self,img):
        # pass
        x1,y1= self.lmlist[4][1],self.lmlist[4][2]
        x2, y2 = self.lmlist[8][1], self.lmlist[8][2]
        cv2.line(img,(x1,y1),(x2,y2),(255,0,0),3)
        dist = math.hypot(x2 - x1, y2 - y1)
        # print(dist)
        vol=(np.interp(dist,[50,300],[0,10]))

        # self.volume = tk.DoubleVar(self.app)
        # print(tk.doubleVar(vol))
        # print(type(tk.getdouble(vol)))

        self.app.change_volume_vision(vol)








    def changeTrack(self):
        self.timeMode[round(float(time.time()),1)]= self.lmlist[4][2]
        try:

            if self.lmlist[4][2]>= self.timeMode[round(float(time.time()),1)-3]+100:
                print("HI")
            # print("changeTrack")
        except Exception as e:
            pass
            # print(e)
        # print("changeTrack")



def main():
    play=PlaybackDetector()


# def main():
#
#     def inplayer():
#
#         root = tk.Tk()
#         root.geometry('600x400')
#         root.wm_title('Musicxy')
#         app = Player.Player(master=root)
#
#         app.mainloop(app.play_song())
#
#
#
#     #getting Predictions
#     def inpredict():
#         ptime = 0
#         ctime = 0
#         cap = cv2.VideoCapture(0)
#         # HandTrack= HandTrackModule.handDetector(detectionCon=0.6,trackCon=0.7)
#         Modedetector= PlaybackDetector(detectionCon=0.6,trackCon=0.7)
#         while True:
#             ret, img = cap.read()
#             img = cv2.flip(img, 1)
#
#
#             # cv2.flip(img,0)
#             if ret == False:
#                 break
#
#             Modedetector.detectionMode(img)
#             ctime = time.time()
#             fps = 1 / (ctime - ptime)
#             ptime = ctime
#
#             cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_ITALIC, 3, (255, 0, 255), 2)
#
#             cv2.imshow("Hand", img)
#             k = cv2.waitKey(1)
#
#             if k == 27:
#                 break
#
#         cv2.destroyAllWindows()
#
#
#     threading.Thread(target=inplayer).start()
#     threading.Thread(target=inpredict).start()



# def main():
#     ptime = 0
#     ctime = 0
#     cap = cv2.VideoCapture(0)
#
#     detector= PlaybackDetector()
#     while True:
#         ret, img = cap.read()
#         img = cv2.flip(img, 1)
#
#         # cv2.flip(img,0)
#         if ret == False:
#             break
#
#         # detector.getPlaybackMode(img)
#
#         ctime = time.time()
#         fps = 1 / (ctime - ptime)
#         ptime = ctime
#
#         cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_ITALIC, 3, (255, 0, 255), 2)
#
#         cv2.imshow("Hand", img)
#         k = cv2.waitKey(1)
#
#         if k == 27:
#             break
#
#     cv2.destroyAllWindows()

if __name__ == "__main__":
    main()