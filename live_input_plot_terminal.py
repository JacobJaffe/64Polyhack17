import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import librosa,librosa.display
import time
import sys
import sounddevice as sd


def combine_frames(frames, num_frames):
    frame = frames[0]
    if (len(frames) < num_frames):
        num_frames = len(frames)
    for x in range(len(frames) - num_frames, len(frames)):
        frame = frame + frames[x]
    return frame

#TODO: this dosn't work but it usually does---- its just a random number can we please fix this
TIGHTNESS =  50

FORMAT = pyaudio.paInt16 # We use 16bit format per sample
CHANNELS = 1
CHUNK = 1024 # number of data points to read at a time
RATE = int(22050 / 2) # time resolution of the recording device (Hz)

p = pyaudio.PyAudio() # start the PyAudio class
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK) #uses default input device

frames = []
bpm_sum = 0
last_bpm = 100;
start_time = time.time()

# the magic
predicted_next_beat = None

# create a numpy array holding a single read of audio data
for i in range(250): #TODO: Make this keep playing untill something
    time_of_beat = None
    if(predicted_next_beat != None):
        if (time.time() - start_time > predicted_next_beat):
            time_of_beat = (time.time() - start_time)
            print("##################################################################" + str(time_of_beat))
            predicted_next_beat = None
    raw_bytes = stream.read(CHUNK)
    data = np.fromstring(raw_bytes,dtype=np.int16)
    frames.append(raw_bytes)
    if (len(sys.argv) > 1):
        peak=np.average(np.abs(data))*2
        bars="#"*int(50*peak/2**16)
        #print("%04d %05d %s"%(i,peak,bars))

        #determine the current bpm
        window = 0
        if (i <= 60):
            window = i
        else :
            window = 50
        last_few_frames = combine_frames(frames, window)
        x = np.fromstring(last_few_frames,np.int16)
        bpm = librosa.beat.tempo(x,sr=RATE,start_bpm=last_bpm)
        gtemp,beats = librosa.beat.beat_track(np.fromstring(combine_frames(frames, window * 2),np.int16),sr=RATE,units='time',start_bpm=bpm,tightness=TIGHTNESS)
        # for x in range(len(beats)):
        #     beats[x] = beats[x] + ((i - window) * float(CHUNK) / RATE)
        #print (beats)
        if (i > 10):
            bpm = min(bpm, old_bpm * 1.05)
            bpm = max(bpm, old_bpm * 0.95)
        #print("Calculated Time Elapsed: " + str(int(i * float(CHUNK) / RATE)))
        #print("Time Elapsed:            " + str(int(time.time() - start_time)))
        print("Bpm: " + str(int(gtemp)))
        if (len(beats) != 0):
            if(predicted_next_beat == None):
                if (time_of_beat == None):
                    time_of_beat = beats[-1]
                predicted_next_beat =  time_of_beat +  60 / bpm
        bpm_sum = bpm_sum + bpm
        old_bpm = bpm
    else :
        print(data)

# close the stream gracefully
stream.stop_stream()
stream.close()
p.terminate()

one_big_frame = combine_frames(frames, len(frames))

##########################################################


fig = plt.figure()
ax = fig.add_subplot(111)
x = np.fromstring(one_big_frame,np.int16)

temp = librosa.beat.tempo(x,sr=RATE)
gtemp,beats = librosa.beat.beat_track(x,sr=RATE,units='time',start_bpm=temp,tightness=TIGHTNESS)

librosa.display.waveplot(x,alpha=0.5)
plt.vlines(beats,ax.get_ylim()[0],ax.get_ylim()[1],color='r')
plt.title(str(np.around(temp))+" BPM, "+"Tightness: "+str(int(TIGHTNESS)))

print(beats)
print("Average bpm: " + str(int(bpm_sum / 250)))
plt.show()
