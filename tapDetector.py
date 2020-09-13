import struct
import math

INITIAL_TAP_THRESHOLD = 0.30
SHORT_NORMALIZE = (1.0/32768.0)

def get_rms(block):
    count = len(block)/2
    format = "%dh"%(count)
    shorts = struct.unpack(format, block)
    sum_squares = 0.0
    for sample in shorts:
        n = sample * SHORT_NORMALIZE
        sum_squares += n*n
    
    return math.sqrt( sum_squares / count )

class TapDetector(object):
    def __init__(self, input_block_time, app):
        self.input_block_time = input_block_time
        self.tap_threshold = INITIAL_TAP_THRESHOLD
        self.current_time = 0
        self.noisycount = 0.15/self.input_block_time+1 
        self.quietcount = 0
        self.tap_list = []
        self.app = app

    def tapDetected(self, time_info):
        print("tap: " + str(self.current_time))
        self.app.setLabel("state", "clap: " + str(self.current_time))
        self.tap_list.append(self.current_time)

    def analyse(self, block, time_info):
        self.current_time += time_info
        # if self.current_time - math.floor(self.current_time) < 0.025:
        #     print(math.floor(self.current_time))
        amplitude = get_rms(block)
        if amplitude > self.tap_threshold:
            self.quietcount = 0
            self.noisycount += 1
        else:            
            if 1 <= self.noisycount <= 0.15/self.input_block_time:
                self.tapDetected(time_info)
            self.noisycount = 0
            self.quietcount += 1