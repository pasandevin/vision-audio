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
def producer(out_q):
    while True:
        # Produce some data
        ...
        out_q.put(data)


# A thread that consumes data
def consumer(in_q):
    while True:
        # Get some data
        data = in_q.get()
        # Process the data
        ...


# Create the shared queue and launch both threads
q = Queue()
t1 = Thread(target=consumer, args=(q,))
t2 = Thread(target=producer, args=(q,))
t1.start()
t2.start()