from pyAudioRunner import PyAudioRunner
from appJar import gui
import sys
import time

if __name__ == "__main__":
    app = gui("Clap detection", "600x300")
    app.addLabel("title", "Clap detection")
    app.addLabelEntry("Nom")
    app.setFocus("Nom")
    app.addEmptyLabel("state")
    app.addEmptyLabel("duration")
    app.addEmptyLabel("write")

    counter = 3

    p = PyAudioRunner("audio.wav", app)

    def resetCountdown():
        global counter
        counter = 3

    def countdown():
        global counter
        if counter > 0:
            app.setLabel("state", "Commence dans " + str(counter))
            counter -= 1
            app.after(1000, countdown)
        elif counter == 0:
            app.setLabel("state", "Début")

    def press(button):
        if button == "Fermer":
            p.stream.stop_stream()
            p.stream.close()
            app.stop()
        else:
            resetCountdown()
            countdown()
            app.setLabel("write", "")
            app.setLabel("duration", "")
            app.after(3000, p.run)

    app.addButtons(["Commencer", "Fermer"], press)

    app.go()