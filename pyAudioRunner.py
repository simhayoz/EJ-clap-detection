import numpy as np
import pyaudio
import wave
import time
import xlsxwriter
import os
from tapDetector import TapDetector

FRAME_PER_SECOND = 1024
class PyAudioRunner(object):
    def __init__(self, audio_file, app):
        self.audio_file = audio_file
        self.app = app
        self.stream = None

    def waitStream(self):
        if self.stream.is_active():
            # time.sleep(0.1)
            self.app.setLabel("duration", self.getTime(int(self.t.current_time)) + "/" + self.getTime(int(self.wf.getnframes() / float(self.wf.getframerate()))))
            self.app.after(100, self.waitStream)
        else:
            print("list tap time: " + str(self.t.tap_list))
            self.stream.stop_stream()
            self.stream.close()
            self.wf.close()
            self.p.terminate()
            self.writeToXlsx()

    def writeToXlsx(self):
        if not os.path.exists("result"):
            os.makedirs("result")
        name = self.app.getEntry("Nom")
        workbook = xlsxwriter.Workbook("result/" + name + ".xlsx")
        worksheet = workbook.add_worksheet() 
        worksheet.write("A1", name)
        index = 2
        for tapTime in self.t.tap_list:
            worksheet.write("A"+str(index), tapTime)
            index += 1
        workbook.close() 
        self.app.setLabel("write", "result/" + name + ".xlsx enregistré avec " + str(len(self.t.tap_list)) + " claps")
    
    def getTime(self, total):
        if total > 60:
            minutes = total % 60
            seconds = total / 60
        else:
            minutes = 0
            seconds = total
        return '{:02d}'.format(minutes) + ":" + '{:02d}'.format(seconds)

    def run(self):
        self.wf = wave.open(self.audio_file, 'rb')

        self.p = pyaudio.PyAudio()
        self.t = TapDetector(FRAME_PER_SECOND/self.wf.getframerate(), self.app)

        def callback(in_data, frame_count, time_info, status):
            data = self.wf.readframes(frame_count)
            self.t.analyse(in_data, frame_count/self.wf.getframerate())
            return (data, pyaudio.paContinue)
            

        self.stream = self.p.open(format=self.p.get_format_from_width(self.wf.getsampwidth()),
                        channels=self.wf.getnchannels(),
                        rate=self.wf.getframerate(),
                        output=True,
                        input=True,
                        stream_callback=callback)

        self.stream.start_stream()

        # self.app.registerEvent(self.waitStream)
        self.waitStream()

        