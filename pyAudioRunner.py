import numpy as np
import pyaudio
import wave
import time
from tapDetector import TapDetector

FRAME_PER_SECOND = 1024
class PyAudioRunner(object):
    def __init__(self, audio_file, app):
        self.audio_file = audio_file
        self.app = app

    def waitStream(self):
        if self.stream.is_active():
            time.sleep(0.1)
        else:
            print("list tap time: " + t.tap_list)

            self.stream.stop_stream()
            self.stream.close()
            wf.close()

            p.terminate()

    def run(self):
        wf = wave.open(self.audio_file, 'rb')

        self.app.setLabel("duration", str(wf.getnframes() / float(wf.getframerate())))

        p = pyaudio.PyAudio()
        t = TapDetector(FRAME_PER_SECOND/wf.getframerate())

        def callback(in_data, frame_count, time_info, status):
            data = wf.readframes(frame_count)
            t.analyse(in_data, frame_count/wf.getframerate())
            return (data, pyaudio.paContinue)
            

        self.stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True,
                        input=True,
                        stream_callback=callback)

        self.stream.start_stream()

        self.app.registerEvent(self.waitStream)

        