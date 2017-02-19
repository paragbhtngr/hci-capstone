from psychopy import prefs, core
prefs.general['audioLib'] = ['pygame']

from psychopy import sound

tada = sound.Sound('dog.wav')
tada.play()	
core.wait(tada.getDuration() + 0.5)
