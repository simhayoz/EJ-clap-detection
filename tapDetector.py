import struct
import math

INITIAL_TAP_THRESHOLD = 0.30
SHORT_NORMALIZE = (1.0/32768.0)

def get_rms( block ):
    # RMS amplitude is defined as the square root of the 
    # mean over time of the square of the amplitude.
    # so we need to convert this string of bytes into 
    # a string of 16-bit samples...

    # we will get one short out for each 
    # two chars in the string.
    count = len(block)/2
    format = "%dh"%(count)
    shorts = struct.unpack( format, block )

    # iterate over the block.
    sum_squares = 0.0
    for sample in shorts:
        # sample is a signed short in +/- 32768. 
        # normalize it to 1.0
        n = sample * SHORT_NORMALIZE
        sum_squares += n*n
    
    return math.sqrt( sum_squares / count )

class TapDetector(object):
    def __init__(self, input_block_time):
        self.input_block_time = input_block_time
        self.tap_threshold = INITIAL_TAP_THRESHOLD
        self.noisycount = 0.15/self.input_block_time+1 
        self.quietcount = 0
        self.tap_list = []

    def tapDetected(self, time_info): #DETECTED
        self.tap_list.append(time_info)

    def analyse(self, block, time_info):
        amplitude = get_rms(block)
        if amplitude > self.tap_threshold:
            # noisy block
            self.quietcount = 0
            self.noisycount += 1
        else:            
            # quiet block.

            if 1 <= self.noisycount <= 0.15/self.input_block_time:
                self.tapDetected(time_info)
            self.noisycount = 0
            self.quietcount += 1