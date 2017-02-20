import threading
from threading import *
import sys
import termios
import os
import time
import itertools
import Queue as queue
import experiment_generator
import audio_helper
import motor_helper
from psychopy import visual, core, gui, data, event  # import some libraries from PsychoPy
from psychopy.tools.filetools import fromFile, toFile
from psychopy import prefs
prefs.general['audioLib'] = ['pygame']
from psychopy import sound


blocks = experiment_generator.generate_experiment(testing=True)
blocks[0].print_block()


def drawText(win, msg, text, time=0):
    msg.setText(text)
    win.flip()
    core.wait(time)


def updateTrial(win, blockTxt, trialTxt, bn, tn):
    blockStr = "Block " + str(bn)
    trialStr = "Trial " + str(tn)
    blockTxt.setText(blockStr)
    trialTxt.setText(trialStr)
    win.flip()


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


def keyboard_input(blocks, input_ready, vibration_ready, distraction_ready, input_complete, vibration_complete, distraction_complete):
    block_number = 0
    trial_number = 0

    # create a window
    win = visual.Window([800, 600], monitor="testMonitor", units="deg")

    blockTxt = visual.TextStim(win, text="", pos=(-3, 8))
    trialTxt = visual.TextStim(win, text="", pos=(3, 8))
    msg = visual.TextStim(win, text="")

    blockTxt.setAutoDraw(True)
    trialTxt.setAutoDraw(True)
    msg.setAutoDraw(True)

    clock = core.Clock()

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

            updateTrial(win, blockTxt, trialTxt, block_number + 1, trial_number + 1)

            input_complete.clear()
            # put the command in the queue so the other thread can read it
            #  don't forget to quit here as well, or you will have memory leaks

            drawText(win, msg, "Press Enter to start the experiment")

            while True:
                enter = event.getKeys(['return'])
                if len(enter) > 0:
                    drawText(win, msg, "Press Space when you feel the vibration")
                    time.sleep(3)
                    break
            
            input_ready.set()
            distraction_ready.wait()
            vibration_ready.wait()
            
            timeOfStart = clock.getTime()

            drawText(win, msg, "Press Space when you feel the vibration")

            while True:
                space = event.getKeys(['space'])
                if len(space) > 0:
                    break

            timeOfDetection = clock.getTime()

            print "Time Taken: ", timeOfDetection - timeOfStart, "\n\r",

            screen_lock.acquire()
            print "Vibration detected!"
            drawText(win, msg, "Which finger did you feel the vibration on?")
            finger = None
            while True:
                answer = event.getKeys(['f', 'g', 'h', 'j'])                     

                if len(answer) > 0:
                    drawText(win, msg, "Answer Recorded as " + answer[0])
                    break

            finger = answer[0]
            print finger
            print "You said finger: ", finger
            if char_to_finger(finger) == trial.target:
                print "You are correct!"
            else:
                print "Sorry, correct answer was ", trial.target
            screen_lock.release()

            print "exit keyboard"
            input_complete.set()
            distraction_complete.wait()
            vibration_complete.wait()

            input_ready.clear()
            
            trial_number += 1
        block_number += 1


def vibration(blocks, input_ready, vibration_ready, distraction_ready, input_complete, vibration_complete, distraction_complete):
    block_number = 0
    trial_number = 0

    motor_helper.start_motors()
    
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

            vibration_ready.set()
            distraction_ready.wait()
            input_ready.wait()

            vibration_number = 0
            for vibration in trial.vibrations:
                screen_lock.acquire()
                print "VIBRATION IN %d:" % int(vibration), "\r"
                if vibration_number == trial.event:
                    print "BZZZZZZ\n\r"
                    motor_helper.vibrate_motor(vibration_number, 100, 5)
                    time.sleep(5)
                else:
                    print "bzz\n\r"
                    motor_helper.vibrate_motor(vibration_number, 80, 1)
                    time.sleep(1)
                screen_lock.release()

                vibration_number += 1

            print "exit vibration\n\r",
            vibration_complete.set()
            distraction_complete.wait()
            input_complete.wait()

            vibration_ready.clear()
            
            trial_number += 1
        block_number += 1
        
    motor_helper.stop_motors()


def distraction(blocks, input_ready, vibration_ready, distraction_ready, input_complete, vibration_complete, distraction_complete):
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

            distraction_ready.set()
            vibration_ready.wait()
            input_ready.wait()
            
            if trial.isDistraction:
                distraction_event = trial.event - 3
                time.sleep(distraction_event * 0.125)
                print "GAAAAAAAAAAAAAAAAAAAAAAAAAAH\n\r",
                # tada = sound.Sound('dog.wav')
                # tada.play()
                os.system("omxplayer 'dog.wav'")

            print "exit distraction\n\r",
            distraction_complete.set()
            vibration_complete.wait()
            input_complete.wait()

            distraction_ready.clear()

            trial_number += 1
        block_number += 1


input_ready = threading.Event()
vibration_ready = threading.Event()
distraction_ready = threading.Event()
input_complete = threading.Event()
vibration_complete = threading.Event()
distraction_complete = threading.Event()

# start the threads
input_thread = threading.Thread(target=keyboard_input, args=(
    blocks, input_ready, vibration_ready, distraction_ready,
    input_complete, vibration_complete, distraction_complete))
vibration_thread = threading.Thread(target=vibration, args=(
    blocks, input_ready, vibration_ready, distraction_ready,
    input_complete, vibration_complete, distraction_complete))
distraction_thread = threading.Thread(target=distraction, args=(
    blocks, input_ready, vibration_ready, distraction_ready,
    input_complete, vibration_complete, distraction_complete))
screen_lock = Semaphore(value=1)


def run_experiment():
    input_thread.start()
    time.sleep(1)
    vibration_thread.start()
    distraction_thread.start()


# if __name__ == "__main__":
#     a.start()
#     time.sleep(0.5)
#     a.stop()     
#     run_experiment()

run_experiment()
