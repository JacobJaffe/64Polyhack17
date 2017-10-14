import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import pylab
import time
import pyqtgraph as pg
import sys


def combine_frames(frames):
    frame = frames[0]
    for x in range(1, len(frames)):
        frame = frame + frames[x]
    return frame

FORMAT = pyaudio.paInt16 # We use 16bit format per sample
CHANNELS = 1
CHUNK = 1024 # number of data points to read at a time
RATE = 44100 # time resolution of the recording device (Hz)

p = pyaudio.PyAudio() # start the PyAudio class
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK) #uses default input device

frames = []
# create a numpy array holding a single read of audio data
for i in range(100): #TODO: Make this keep playing untill something
    raw_bytes = stream.read(CHUNK)
    data = np.fromstring(raw_bytes,dtype=np.int16)
    frames.append(raw_bytes)
    if (len(sys.argv) > 1):
        peak=np.average(np.abs(data))*2
        bars="#"*int(50*peak/2**16)
        print("%04d %05d %s"%(i,peak,bars))
    else :
        print(data)

# close the stream gracefully
stream.stop_stream()
stream.close()
p.terminate()

one_big_frame = combine_frames(frames)


fig = plt.figure()
s = fig.add_subplot(111)
amplitude = np.fromstring(one_big_frame, np.int16)
s.plot(amplitude)
plt.show()
