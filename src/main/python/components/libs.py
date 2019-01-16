import numpy as np
import pyaudio
import pyworld as pw
from .settings import *


class MicrophoneRecorder:
    def __init__(self, write_flag,*signal):
        self.signals = signal
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt16,
                            channels=1,
                            rate=FS,
                            input=True,
                            output=write_flag,
                            frames_per_buffer=CHUNKS,)
        self.write_flag = write_flag
    def read(self):
        data = self.stream.read(CHUNKS)
        y = np.frombuffer(data,"int16")
        # print("y_after",)
        before_shape = y.shape
        get_data = y.astype(np.float)  # WORLDはfloat前提のコードになっているのでfloat型にしておく
        _f0, t = pw.dio(get_data, FS)    # raw pitch extractor
        f0 = pw.stonemask(get_data, _f0, t, FS)  # pitch refinement
        sp = pw.cheaptrick(get_data, f0, t, FS)  # extract smoothed spectrogram
        ap = pw.d4c(get_data, f0, t, FS)         # extract aperiodicity
        y = pw.synthesize(f0*2, sp, ap, FS)
        y = np.asarray(y,dtype=np.float)
        # print("y_after",y.shape)
        y_new = y[0:before_shape[0]]
        y_new = np.asarray(y_new,dtype=np.int16)
        [signal.emit(y_new) for signal in self.signals]
        if self.write_flag:
            self.stream.write(y_new)

    def close(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

