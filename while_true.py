from time import sleep
import signal

event_1_happened, event_2_happened = False, False
callback1, callback2 = lambda: print("Event 1"), lambda: print("Event 2")

def sigint_handler(signum, frame):
    global event_1_happened
    event_1_happened = True

signal.signal(signal.SIGTSTP, sigint_handler)

while True: 
    if event_1_happened: 
        callback1()
        event_1_happened = False
    elif event_2_happened:
        callback2()
        event_2_happened = False
    sleep_until_next_event_arrives()

