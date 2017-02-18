from psychopy import visual, core, gui, data, event  # import some libraries from PsychoPy
from psychopy.tools.filetools import fromFile, toFile

# create a window
win = visual.Window([800, 600], monitor="testMonitor", units="deg")

blockNum = 1
trialNum = 1

blockStr = "Block " + str(blockNum)
trialStr = "Trial " + str(trialNum)

blockTxt = visual.TextStim(win, text=(blockStr), pos=(-3, 8))
trialTxt = visual.TextStim(win, text=(trialStr), pos=(3, 8))
msg = visual.TextStim(win, text="")

blockTxt.setAutoDraw(True)
trialTxt.setAutoDraw(True)
msg.setAutoDraw(True)

clock = core.Clock()


def drawText(text, time=1):
	msg.setText(text)
	win.flip()
	core.wait(time)


def updateTrial():
	blockStr = "Block " + str(blockNum)
	trialStr = "Trial " + str(trialNum)
	blockTxt.setText(blockStr)
	trialTxt.setText(trialStr)
	win.flip()


# draw the stimuli and update the window
while True:  # this creates a never-ending loop
	drawText(clock.getTime(), time=0.01)
	q = event.getKeys(['q'])
	space = event.getKeys(['space'])
	if len(q) > 0: 
		print "quitting..."
		break
	event.clearEvents()

	if len(space) > 0:
		trialNum += 1
		updateTrial()
		print trialStr


# cleanup
win.close()
core.quit()
