import numpy as np
import pyaudio
import pyworld as pw
from .settings import *
from PyQt5.QtCore import QObject


class MicrophoneRecorder(QObject):
    def __init__(self, write_flag,*signal):
        super(MicrophoneRecorder,self).__init__()
        self.signals = signal
        self.p = pyaudio.PyAudio()

        self.stream = self.p.open(format=pyaudio.paInt16,
                            channels=1,
                            rate=FS,
                            input=True,
                            output=write_flag,
                            frames_per_buffer=CHUNKS)
        self.write_flag = write_flag
        self.f0_numerator_para = 1
        self.f0_denominator_para = 1
        self.f0_parameter = self.f0_numerator_para / self.f0_denominator_para

    def audio_synthesize(self,y):
        y = np.asarray(y,dtype=np.float)
        before_shape = y.shape
        # print("y_after",y.shape)
        _f0, t = pw.dio(y, FS)    # raw pitch extractor
        f0 = pw.stonemask(y, _f0, t, FS)  # pitch refinement
        sp = pw.cheaptrick(y, f0, t, FS)  # extract smoothed spectrogram
        ap = pw.d4c(y, f0, t, FS)         # extract aperiodicity
        data = pw.synthesize(f0*self.f0_parameter, sp, ap, FS)
        y_new = data[0:before_shape[0]]
        y_new = np.asarray(y_new,dtype=np.int16)
        return y_new

    def numeratorChanged(self,value):
        self.f0_numerator_para = value
        self.f0_parameter = self.f0_numerator_para / self.f0_denominator_para

    def denominatorChanged(self,value):
        self.f0_denominator_para = value
        self.f0_parameter = self.f0_numerator_para / self.f0_denominator_para

    def read(self):
        data = self.stream.read(CHUNKS)
        y = np.frombuffer(data,"int16")
        y_new = self.audio_synthesize(y)
        if self.write_flag:
            self.stream.write(y_new,CHUNKS)
        [signal.emit(y_new) for signal in self.signals]

    def close(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        # return 1

