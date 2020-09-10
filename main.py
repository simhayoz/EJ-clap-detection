from pyAudioRunner import PyAudioRunner
import xlsxwriter
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

    counter = 3

    p = PyAudioRunner("60BPM.wav", app)

    def countdown():
        global counter
        if counter > 0:
            app.setLabel("state", "Commence dans " + str(counter))
            counter -= 1

    def press(button):
        if button == "Annuler":
            print("goes here")
            p.stream.stop_stream()
            p.stream.close()
            app.stop()
        else:
            name = app.getEntry("Nom")
            app.registerEvent(countdown)
            p.run()

    app.addButtons(["Commencer", "Annuler"], press)

    # if len(sys.argv) < 2:
    #     print("Plays a wave file.\n\nUsage: %s filename.wav" % sys.argv[0])
    #     sys.exit(-1)

    app.go()

    workbook = xlsxwriter.Workbook(name + ".xlsx")
    worksheet = workbook.add_worksheet() 
    worksheet.write("A1", name)
    index = 2
    for tapTime in t.tap_list:
        worksheet.write("A"+str(index), tapTime)
        index += 1
    workbook.close() 