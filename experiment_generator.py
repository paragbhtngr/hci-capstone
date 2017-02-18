import numpy as np
import random
from random import shuffle

BLOCKS = 6
TRIALS_PER_BLOCK = 24
DISTRACTIONS_PER_BLOCK = 4
VIBRATIONS_PER_TRIAL = 8


class Trial(object):
    """docstring for ClassName"""
    def __init__(self, target, distraction):
        super(Trial, self).__init__()
        self.vibrations, self.event = generate_trial(target)
        self.target = target
        self.isDistraction = distraction


class Block(object):
    """docstring for Block"""
    def __init__(self, train=False):
        super(Block, self).__init__()
        self.trials = []
        if not train:
            for i in xrange(DISTRACTIONS_PER_BLOCK):
                self.trials.append(Trial(i % 4, True))

            for i in xrange(TRIALS_PER_BLOCK - DISTRACTIONS_PER_BLOCK):
                self.trials.append(Trial(i % 4, False))
        else:
            for i in xrange(TRIALS_PER_BLOCK):
                self.trials.append(Trial(i % 4, False))

        shuffle(self.trials)

    def print_block(self):
        print "Printing Block:"
        for i in xrange(len(self.trials)):
            print "Trial", i, ":"
            print "\t", self.trials[i].vibrations,
            print "Target Finger:", self.trials[i].target,
            print "Event Position:", self.trials[i].event,
            print "is Distraction:", self.trials[i].isDistraction


def generate_trial_vibrations():
    numbers = np.zeros(VIBRATIONS_PER_TRIAL)
    for i in xrange(VIBRATIONS_PER_TRIAL):
        if i == 0:
            numbers[i] = int(np.random.randint(0, 3))
        else:
            oldrand = numbers[i - 1]
            adder = np.random.randint(0, 3) % 3
            numbers[i] = int((oldrand + adder + 1) % 4)
    return numbers


def generate_trial(target_finger):
    vibration = np.zeros(VIBRATIONS_PER_TRIAL)
    event = 0
    while True:
        vibration = generate_trial_vibrations()
        indices = [i + 3 for i, x in enumerate(vibration[3:]) if x == target_finger]
        # check target finger occurs in list and is not only the first one
        if len(indices) == 0:
            continue
        # otherwise this vibration pattern can be used
        event = random.choice(indices)
        break
    return(vibration, event)


def generate_experiment():
    blocks = []
    blocks.append(Block(train=True))
    for i in xrange(BLOCKS):
        blocks.append(Block())
    shuffle(blocks)
    return blocks


# block = Block()
# print block.trials[0].vibrations
# print block.trials[0].target
# print block.trials[0].event
# print block.trials[0].isDistraction
# block.print_block()
