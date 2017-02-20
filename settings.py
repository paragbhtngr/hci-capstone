'''
This file sets up various variables values.
'''

'''
SS randomization restrictions

These trials cannot be in the first three trials or the last trial within each block, 
and each Surprise trial must be separated from another by at least two trials of other types. 
The first four Surprise trials must represent the four types of target-present trials 
(see breakdown of types below).
'''
NUM_TRIAL = 160 #number of trial per block
SS_NUM = 24 #number of SS per block
FIRST_SS = 3 #first SS appearance
LAST_SS = 1 #last SS appearance
SS_INT = 2 #SS intervals

PO_no = 50 #number of Probe only trials
PA_no = 36 #number of Probe absent trials
SS_no = 5 #number of SS trials
SO_no = 2 #number of SS only trials

PPT_ORDER = ['12', '16', '21', '9', '3', '22', '13', '10', '19', \
'6', '24', '18', '2', '20', '8', '23', '4', '15', '1', '7', '14', '17', '11', '5']

A_INST = u'Before starting the main experiment, you will work through three \
brief practice sessions. During this first practice session, you will be \
presented with trials that consist of a rapid series of tones. Your task is to \
determine whether a high-pitched tone (the probe) was present in the stream.\
\n\nAt the end of each trial, you will be prompted to respond using the keyboard mappings \
that are provided below. Press the "K" key now to hear the probe. \
The same probe will automatically play before each trial.\
\n\nPress the space bar to begin the practice trials.'

V_INST = u'During this second practice session, you will be presented with \
trials that consist of a sequence of rapidly changing letters.\
\n\nYour task is to determine whether an X (probe) was present or not. \
At the end of each trial, you will be prompted to respond using the keyboard \
mappings that are provided below. "Probe?" is cue to report the presence of the X. \
\n\nPress the space bar to begin the practice trials.'

AV_INST = u'During this third practice session, you will be presented with trials \
that consist of a rapid series of tones and a sequence of rapidly changing letters.\
\nYour task is to determine whether a probe was present or not. \
When the probe is present in a trial, it will either be a high-pitched tone OR X \
but NOT both. Therefore, you will be asked to determine whether the probe was auditory \
(i.e., a high-pitched tone) or visual (i.e., an X). At the end of each trial, you \
will be prompted to respond using the keyboard mappings that are provided below. \
"Probe?" is cue to report the presence and type of the probe.\
\nPress the space bar to begin the practice trials.'

E_INST = u'In each trial, a rapid series of tones and sequence of rapidly \
changing letters will be presented simultaneously.\
\nYour task is to determine whether a probe was present or not. \
When the probe is present in a trial, it will either be a high-pitched tone \
OR X but NOT both. Therefore, you will be asked to determine whether the \
probe was auditory (i.e., a high-pitched tone) or visual (i.e., an X). \
At the end of each trial, you will be prompted to respond using the keyboard \
mappings that are provided below. "Probe?" is cue to report the presence and type of the probe.\
\nPress the space bar to begin the experimental trials.'

BREAK = u'Now, you have completed half of the entire experiment.\
Please allow yourself to have a break.\
\nPress the space bar to resume the experiment.'