import cv2
import time
import PlaybackDetector
import Player
import tkinter as tk
from tkinter import PhotoImage
# import HandTrackModule




# Intializing the Player
# img = PhotoImage(file='images/music.gif')
# next_ = PhotoImage(file = 'images/next.gif')
# prev = PhotoImage(file='images/previous.gif')
# play = PhotoImage(file='images/play.gif')
# pause = PhotoImage(file='images/pause.gif')
# mPlayer= Player.Player(img,next_,prev,play,pause)
# root = tk.Tk()
# root.geometry('600x400')
# root.wm_title('Musicxy')
#
#
#
# app = mPlayer(master=root)
# app.mainloop()



# #getting Predictions
# ptime = 0
# ctime = 0
# cap = cv2.VideoCapture(0)
# # HandTrack= HandTrackModule.handDetector(detectionCon=0.6,trackCon=0.7)
# Modedetector= PlaybackDetector.PlaybackDetector(detectionCon=0.6,trackCon=0.7)
# while True:
#     ret, img = cap.read()
#     img = cv2.flip(img, 1)
#
#
#     # cv2.flip(img,0)
#     if ret == False:
#         break
#
#     detectMode=Modedetector.detectionMode(img)
#     ctime = time.time()
#     fps = 1 / (ctime - ptime)
#     ptime = ctime
#
#     cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_ITALIC, 3, (255, 0, 255), 2)
#
#     cv2.imshow("Hand", img)
#     k = cv2.waitKey(1)
#
#     if k == 27:
#         break
#
# cv2.destroyAllWindows()