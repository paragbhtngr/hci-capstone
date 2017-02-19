from psychopy import prefs
prefs.general['audioLib'] = ['pygame']
from psychopy import sound

tada = sound.Sound('dog.wav')
tada.play()