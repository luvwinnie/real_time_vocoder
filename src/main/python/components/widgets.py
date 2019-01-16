import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore

from PyQt5.QtWidgets import (QWidget, QSlider, QApplication, 
    QHBoxLayout, QVBoxLayout)

from PyQt5.QtCore import QObject, Qt, pyqtSignal,QSize


from .settings import *
   

class WaveWidget(pg.PlotWidget):
    read_collected = QtCore.pyqtSignal(np.ndarray)
    def __init__(self):
        super(WaveWidget, self).__init__()
        #プロット初期設定
        # self.enableMouse(False)
        self.plt = self.getPlotItem()
        self.plt.setMouseEnabled(x=False,y=False)
        self.plt.setYRange(-10000,10000)    #y軸の上限、下限の設定
        self.curve=self.plt.plot()  #プロットデータを入れる場所

        self.frameSize = 1024*8
        self.overLap = 0
        self.record = False
        self.read_collected.connect(self.update)
        # self.data_array = np.array([],dtype=np.int16)
        
    def update(self,chunk):
        self.curve.setData(chunk)   #プロットデータを格納
        # zcr = ZeroCR(chunk,self.frameSize,self.overLap)
        # zcr = int(zcr.mean())
        # self.data_array = np.concatenate(chunk)
        # print(self.data_array)


class parameterWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setRange(0, 50 )
        self.slider.resize(100,100)
        self.slider.setTickInterval(1)



class SpectrogramWidget(pg.PlotWidget):
    read_collected = QtCore.pyqtSignal(np.ndarray)
    def __init__(self):
        super(SpectrogramWidget, self).__init__()
        self.img = pg.ImageItem()
        self.addItem(self.img)
        self.getPlotItem().setMouseEnabled(x=False,y=False)

        self.img_array = np.zeros((250, int(CHUNKS/2+1)))

        # bipolar colormap
        pos = np.array([0., 1., 0.5, 0.25, 0.75])
        color = np.array([[0,255,255,255], [255,255,0,255], [0,0,0,255], (0, 0, 255, 255), (255, 0, 0, 255)], dtype=np.ubyte)
        cmap = pg.ColorMap(pos, color)
        lut = cmap.getLookupTable(0.0, 1.0, 256)

        # set colormap
        self.img.setLookupTable(lut)
        self.img.setLevels([-30,40])

        # setup the correct scaling for y-axis
        freq = np.arange((CHUNKS/2)+1)/(float(CHUNKS)/FS)
        yscale = 1.0/(self.img_array.shape[1]/freq[-1])
        self.img.scale((1./FS)*CHUNKS, yscale)

        self.setLabel('left', 'Frequency', units='Hz')

        # prepare window for later use
        self.win = np.hamming(CHUNKS)
        self.read_collected.connect(self.update)

    def update(self, chunk):
        # normalized, windowed frequencies in data chunk
        spec = np.fft.rfft(chunk*self.win) / CHUNKS
        # get magnitude
        psd = abs(spec)
        # convert to dB scale
        psd = 20 * np.log10(psd)

        # roll down one and replace leading edge with new data
        self.img_array = np.roll(self.img_array, -1, 0)
        self.img_array[-1:] = psd

        self.img.setImage(self.img_array, autoLevels=False)