import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import librosa,librosa.display
import time
import sys


def combine_frames(frames):
    frame = frames[0]
    for x in range(1, len(frames)):
        frame = frame + frames[x]
    return frame

FORMAT = pyaudio.paInt16 # We use 16bit format per sample
CHANNELS = 1
CHUNK = 1024 # number of data points to read at a time
RATE = 22050 # time resolution of the recording device (Hz)

p = pyaudio.PyAudio() # start the PyAudio class
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK) #uses default input device

frames = []
# create a numpy array holding a single read of audio data
for i in range(200): #TODO: Make this keep playing untill something
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

##########################################################


fig = plt.figure()
ax = fig.add_subplot(111)
x = np.fromstring(one_big_frame,np.int16)
sr = RATE

def getTight():
    return 20*np.random.randn()+50

tight = getTight()
temp = librosa.beat.tempo(x,sr=sr)
gtemp,beats = librosa.beat.beat_track(x,sr=sr,units='time',start_bpm=temp,tightness=tight)


librosa.display.waveplot(x,alpha=0.5)
plt.vlines(beats,ax.get_ylim()[0],ax.get_ylim()[1],color='r')
plt.title(str(np.around(temp))+" BPM, "+"Tightness: "+str(int(tight)))

print(beats)

plt.show()
