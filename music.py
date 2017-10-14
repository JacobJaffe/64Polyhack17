

import numpy as np
import matplotlib.pyplot as plt
import sklearn
import librosa,librosa.display

plt.rcParams['figure.figsize'] = (14,5)

#fname = '58bpm.wav'
fname = 'classic_rock_beat.wav'
#fname = 'conga_groove.wav'
#fname = '125_bounce.wav'
#fname = 'prelude_cmaj.wav'
#fname = 'simple_loop.wav'
#fname = 'simple_piano.wav'

#fname = 'c_strum.wav'
#fname = 'clarinet_c6.wav'
#fname = 'oboe_c6.wav'

x,sr = librosa.load('audio/'+fname)
t = np.linspace(0,x.size/sr,x.size)

#ipd.Audio(x,rate=sr)

def getTight():
    return 20*np.random.randn()+50

tight = getTight()
temp = librosa.beat.tempo(x,sr)

gtemp,beats = librosa.beat.beat_track(x,sr,units='time',start_bpm=temp,tightness=tight)

librosa.display.waveplot(x,alpha=0.5)
plt.vlines(beats,-1,1,color='r')
plt.ylim(-1,1)
plt.title(str(np.around(gtemp))+" BPM, "+"Tightness: "+str(int(tight)))


clicks = librosa.clicks(beats,sr=sr,length=x.size,click_freq=700)
#ipd.Audio(x+clicks,rate=sr)

plt.show()

