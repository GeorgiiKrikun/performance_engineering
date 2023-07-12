from time import sleep

event_1_happened, event_2_happened = False, False
callback1, callback2 = lambda: print("Event 1"), lambda: print("Event 2")


while True: 
    if event_1_happened: 
        callback1()
    elif event_2_happened:
        callback2()
    sleep_until_event_arrives()
