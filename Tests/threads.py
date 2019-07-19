import logging
import threading
import time

serialThread = False

def thread_function(name):
    global serialThread
    serialThread=True
    logging.info("Thread %s: starting", name)
    counter=1
    while serialThread:
        logging.info("Thread %s: counter %s", name,counter)
        time.sleep(.5)
        counter+=1

    logging.info("Thread %s: finishing", name)

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    logging.info("Main    : before creating thread")
    x = threading.Thread(target=thread_function, args=(1,))
    logging.info("Main    : before running thread")

    x.start()
    logging.info("Main    : wait for the thread to finish")
    logging.info("Main    : all done")

    time.sleep(5)
    serialThread = False