# import time
#
# ctime=time.time()
# print(ctime)
# import threading
# import time





#---------------------------------------------
# def a():
#     print("Function a is running at time: " + str(int(time.time())) + " seconds.")
# def b():
#     print("Function b is running at time: " + str(int(time.time())) + " seconds.")
#
# threading.Thread(target=a).start()
# threading.Thread(target=b).start()



#----------------------------

from queue import Queue
from threading import Thread


# A thread that produces data
# def producer(out_q):
#     while True:
#         # Produce some data
#         ...
#         out_q.put(data)
#
#
# # A thread that consumes data
# def consumer(in_q):
#     while True:
#         # Get some data
#         data = in_q.get()
#         # Process the data
#         ...
#
#
# # Create the shared queue and launch both threads
# q = Queue()
# t1 = Thread(target=consumer, args=(q,))
# t2 = Thread(target=producer, args=(q,))
# t1.start()
# t2.start()

#-----------------------------------------------
# import tkinter
# from PIL import Image, ImageTk
# import cv2
# import numpy as np
#
# # Load an color image
# img = cv2.imread('images/logo.PNG')
#
# #Rearrang the color channel
# b,g,r = cv2.split(img)
# img = cv2.merge((r,g,b))
#
# # A root window for displaying objects
# root = tkinter.Tk()
#
# # Convert the Image object into a TkPhoto object
# im = Image.fromarray(img)
# imgtk = ImageTk.PhotoImage(image=im)
#
# # Put it in the display window
# tkinter.Label(root, image=imgtk).pack()
#
# root.mainloop() # Start the GUI


#--------------------------------------------------
from tkinter import *
import cv2
from PIL import Image, ImageTk
import threading


def video_loop():
    success, img = camera.read(0)  # Read from the camera
    if success:
        cv2image = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)  # Convert colors from BGR to RGBA
        current_image = Image.fromarray(cv2image)  # Convert an image into an Image object
        imgtk = ImageTk.PhotoImage(image=current_image)
        panel.imgtk = imgtk
        panel.config(image=imgtk)
        root.after(1, video_loop)


camera = cv2.VideoCapture(0)  # camera

root = Tk()
root.geometry('600x400')
root.title("opencv + tkinter")

panel = Label(root)  # initialize image panel
panel.pack(padx=10, pady=10)
root.config(cursor="arrow")


threading.Thread(target=video_loop).start()
threading.Thread(target=root.mainloop()).start()
# When everything is done, turn off the camera and release the share of resources
camera.release()
# cv2.destroyAllWindows()