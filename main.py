import pyaudio
import wave
import time
import sys
import numpy as np
import struct
import math
from tapDetector import TapDetector

FRAME_PER_SECOND = 1024

if len(sys.argv) < 2:
    print("Plays a wave file.\n\nUsage: %s filename.wav" % sys.argv[0])
    sys.exit(-1)

wf = wave.open(sys.argv[1], 'rb')

p = pyaudio.PyAudio()
t = TapDetector(FRAME_PER_SECOND/wf.getframerate())

def callback(in_data, frame_count, time_info, status):
    data = wf.readframes(frame_count)
    t.analyse(in_data, time.time() - start_time)
    return (data, pyaudio.paContinue)

stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True,
                input=True,
                stream_callback=callback)

stream.start_stream()
start_time = time.time()
print("start", start_time)

while stream.is_active():
    time.sleep(0.1)

print(t.tap_list)

stream.stop_stream()
stream.close()
wf.close()

p.terminate()