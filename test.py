import audio_helper

predictions[0] = 1

a = audio_helper.AudioFile("dog.wav")

if (predictions[0] == 1):
    while 1:
        a.start()
        sleep(0.5)
        msgbox("Critical Situation Detected!")


        msg ="Please choose an action?"
        title = "Critical Situation Detected!"
        choices = ["Ignore the Warning", "Contact Doctor", "Call Ambulance Service", "Call Hospital"]
        #choice = choicebox(msg, title, choices)
        choice = multchoicebox(msg, title, choices)

        a.stop()

        # note that we convert choice to string, in case
        # the user cancelled the choice, and we got None.
        msgbox("You chose: " + str(choice), "Action is in Progress")

        msg = "Do you want to continue?"
        title = "Please Confirm"
        if ccbox(msg, title):     # show a Continue/Cancel dialog
                        pass  # user chose Continue
        else:
                        sys.exit(0)           # user chose Cancel