import threading
from threading import *
import sys
import termios
import os
import time
import itertools
import Queue as queue
import experiment_generator


class _GetchUnix:
    def __init__(self):
        import tty
        import sys

    def __call__(self):
        import sys
        import tty
        import termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


getch = _GetchUnix()

commands = queue.Queue(0)
blocks = experiment_generator.generate_experiment()


def char_to_finger(ch):
    ch.strip()
    ch = ch[0]
    if ch == 'f':
        return 0
    elif ch == 'g':
        return 1
    elif ch == 'h':
        return 2
    elif ch == 'j':
        return 3
    else:
        return -1


def keyboard_input(blocks, commands, timer_complete, input_complete, vibration_complete, distraction_complete):
    block_number = 0
    trial_number = 0

    for block in blocks:
        trial_number = 0

        screen_lock.acquire()
        print "-------------------------------------------------------------------------------\n\r",
        print "KEYBOARD INPUT: STARTING BLOCK", block_number, "\n\r",
        print "-------------------------------------------------------------------------------\n\r",
        screen_lock.release()

        for trial in block.trials:

            screen_lock.acquire()
            print "-------------------------------------------------------------------------------\n\r",
            print "KEYBOARD INPUT: STARTING TRIAL", trial_number, "\n\r",
            print "-------------------------------------------------------------------------------\n\r",
            screen_lock.release()

            input_complete.clear()
            # put the command in the queue so the other thread can read it
            #  don't forget to quit here as well, or you will have memory leaks
            while 1:
                command = getch()
                if command == " ":
                    break
                else:
                    command = ""
                    termios.tcflush(sys.stdin, termios.TCIOFLUSH)

            commands.put(command)

            if command == " ":
                screen_lock.acquire()
                print "Vibration detected!"
                while 1:
                    finger = raw_input("Which finger did you feel the vibration on?: ")
                    finger = finger.strip()
                    if len(finger) == 0:
                        print "ERROR: Please choose a finger"
                        continue
                    finger = finger[0].lower()
                    print finger
                    if (finger == "f") or (finger == "g") or (finger == "h") or (finger == "j"):
                        print "You said finger: ", finger
                        if char_to_finger(finger) == trial.target:
                            print "You are correct!"
                            break
                        else:
                            print "Sorry, correct answer was ", trial.target
                            break
                    else:
                        print "ERROR: Please enter f,g,h or j."
                screen_lock.release()

            time.sleep(1)
            raw_input("Press Enter to continue:")

            print "exit keyboard"
            input_complete.set()
            distraction_complete.wait()
            vibration_complete.wait()
            timer_complete.wait()

            trial_number += 1
        block_number += 1


def timer(blocks, commands, timer_complete, input_complete, vibration_complete, distraction_complete):
    block_number = 0
    trial_number = 0

    for block in blocks:
        trial_number = 0

        screen_lock.acquire()
        print "-------------------------------------------------------------------------------\n\r",
        print "TIMER INPUT: STARTING BLOCK", block_number, "\n\r",
        print "-------------------------------------------------------------------------------\n\r",
        screen_lock.release()

        for trial in block.trials:

            screen_lock.acquire()
            print "-------------------------------------------------------------------------------\n\r",
            print "TIMER INPUT: STARTING TRIAL", trial_number, "\n\r",
            print "-------------------------------------------------------------------------------\n\r",
            screen_lock.release()

            timer_complete.clear()

            start_time = time.clock()
            command = ""

            while 1:
                # parsing the command queue
                try:
                    # false means "do not block the thread if the queue is empty"
                    # a second parameter can set a millisecond time out
                    command = commands.get(False)
                except queue.Empty:
                    command = ""

                # behave according to the command
                if command == " ":
                    stop_time = time.clock()
                    time_taken = stop_time - start_time

                    screen_lock.acquire()
                    print "Time taken: ", time_taken
                    screen_lock.release()
                    break
            print "exit timer"

            timer_complete.set()
            distraction_complete.wait()
            vibration_complete.wait()
            input_complete.wait()

            trial_number += 1
        block_number += 1


def vibration(blocks, timer_complete, input_complete, vibration_complete, distraction_complete):
    block_number = 0
    trial_number = 0

    for block in blocks:
        trial_number = 0

        screen_lock.acquire()
        print "-------------------------------------------------------------------------------\n\r",
        print "VIBRATION INPUT: STARTING BLOCK", block_number, "\n\r",
        print "-------------------------------------------------------------------------------\n\r",
        screen_lock.release()

        for trial in block.trials:

            screen_lock.acquire()
            print "-------------------------------------------------------------------------------\n\r",
            print "VIBRATION INPUT: STARTING TRIAL", trial_number, "\n\r",
            print "-------------------------------------------------------------------------------\n\r",
            screen_lock.release()

            vibration_complete.clear()

            vibration_number = 0
            for vibration in trial.vibrations:
                screen_lock.acquire()
                print "VIBRATION IN %d:" % int(vibration), "\r"
                if vibration_number == trial.event:
                    print "BZZZZZZ\n\r"
                else:
                    print "bzz\n\r"
                screen_lock.release()

                time.sleep(0.2)
                vibration_number += 1

            print "exit vibration\n\r",
            vibration_complete.set()
            distraction_complete.wait()
            input_complete.wait()
            timer_complete.wait()

            trial_number += 1
        block_number += 1


def distraction(blocks, timer_complete, input_complete, vibration_complete, distraction_complete):
    block_number = 0
    trial_number = 0

    for block in blocks:
        trial_number = 0

        screen_lock.acquire()
        print "-------------------------------------------------------------------------------\n\r",
        print "DISTRACTION INPUT: STARTING BLOCK", block_number, "\n\r",
        print "-------------------------------------------------------------------------------\n\r",
        screen_lock.release()

        for trial in block.trials:

            screen_lock.acquire()
            print "-------------------------------------------------------------------------------\n\r",
            print "DISTRACTION INPUT: STARTING TRIAL", trial_number, "\n\r",
            print "-------------------------------------------------------------------------------\n\r",
            screen_lock.release()

            distraction_complete.clear()
            if trial.isDistraction:
                distraction_event = trial.event - 3
                time.sleep(distraction_event * 0.125)
                print "GAAAAAAAAAAAAAAAAAAAAAAAAAAH\n\r",

            print "exit distraction\n\r",
            distraction_complete.set()
            vibration_complete.wait()
            timer_complete.wait()
            input_complete.wait()

            trial_number += 1
        block_number += 1


timer_complete = threading.Event()
input_complete = threading.Event()
vibration_complete = threading.Event()
distraction_complete = threading.Event()

# start the threads
timer_thread = threading.Thread(target=timer, args=(blocks, commands, timer_complete, input_complete, vibration_complete, distraction_complete))
input_thread = threading.Thread(target=keyboard_input, args=(blocks, commands, timer_complete, input_complete, vibration_complete, distraction_complete))
vibration_thread = threading.Thread(target=vibration, args=(blocks, timer_complete, input_complete, vibration_complete, distraction_complete))
distraction_thread = threading.Thread(target=distraction, args=(blocks, timer_complete, input_complete, vibration_complete, distraction_complete))
screen_lock = Semaphore(value=1)


def run_experiment():
    timer_thread.start()
    input_thread.start()
    time.sleep(1)
    vibration_thread.start()
    distraction_thread.start()


if __name__ == "__main__":
    run_experiment()
