from fbs_runtime.application_context import ApplicationContext
from PyQt5.QtWidgets import QMainWindow
from pyqtgraph.dockarea import DockArea, Dock
from pyqtgraph.Qt import QtCore, QtGui
from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout)
from PyQt5.QtCore import Qt
# from components.parameterControllerWidget import parameterWidget
from components.widgets import parameterWidget, SpectrogramWidget, WaveWidget
from components.libs import MicrophoneRecorder
import sys
from components.settings import *

class AppContext(ApplicationContext):           # 1. Subclass ApplicationContext
    def run(self):                              # 2. Implement run()
        window = QMainWindow()
        version = self.build_settings['version']
        window.setWindowTitle("real_time_vocoder.py v" + version)
        area = DockArea()
        d1 = Dock("Plot Widget", size=(800,200),closable=False)
        d2 = Dock("Parameter Widget", size=(200,200),closable=False)
        # parameter_widget2 = parameterWidget()
        # parameter_widget.setObjectName("F0Slider")
        # parameter_widget.setStyleSheet("""
        #     QSlider{
        #         background:red;
        #         size:100px;
        #     }
        # """)
        self.spectogram_widget = SpectrogramWidget()
        self.wave_widget = WaveWidget()
        self.mic = MicrophoneRecorder(False,self.spectogram_widget.read_collected,self.wave_widget.read_collected)

        #　コントロールのレイアウト設定
        self.createParamterWidget()

        d1.addWidget(self.spectogram_widget)
        d1.addWidget(self.wave_widget)
        d2.addWidget(self.mainControl)
        area.addDock(d1)
        area.addDock(d2,"right")


        interval = CHUNKS/FS
        t = QtCore.QTimer()
        t.timeout.connect(self.mic.read)
        t.start(interval/1000) #QTimer takes ms
        window.resize(800,400)
        window.setCentralWidget(area)
        window.show()
        self.app.aboutToQuit.connect(self.mic.close)
        return self.app.exec_()                 # 3. End run() with this line

    def changedValue(self,value):
            self.pitch_constant.setText("Pitch Constant:{}".format(self.mic.f0_parameter))

    def createParamterWidget(self):
        self.mainControl = QtGui.QWidget()
        self.mainControl.setStyleSheet("""
            background:black;
            color:white;
        """)
        # main = QGridLayout()
        main = QVBoxLayout()
        main.addStretch(1)
        vbox1 = QHBoxLayout()
        vbox1.addStretch(1)
        self.pitch_constant = QtGui.QLabel("Pitch Constant:1")
        vbox1.addWidget(self.pitch_constant)
        vbox1.addStretch(1)
        # vbox1.setAlignment(Qt.AlignCenter)
        vbox2 = QHBoxLayout()
        vbox2.addStretch(1)
        vbox3 = QHBoxLayout()
        vbox3.addStretch(1)
        main.addLayout(vbox1)
        main.addLayout(vbox2)
        main.addLayout(vbox3)
        numeratorLabel = QtGui.QLabel("Numerator")
        numeratorSlider = parameterWidget(1,1000)
        numeratorSlider.setStyleSheet("""
            QSlider{
                background:gray;
            }
        """)
        denominatorLabel = QtGui.QLabel("Denominator")
        denominatorSlider = parameterWidget(1,1000)
        denominatorSlider.setStyleSheet("""
            QSlider{
                background:gray;
            }
        """)
        numeratorSlider.slider.valueChanged.connect(self.mic.numeratorChanged)
        numeratorSlider.slider.valueChanged.connect(self.changedValue)
        denominatorSlider.slider.valueChanged.connect(self.mic.denominatorChanged)
        denominatorSlider.slider.valueChanged.connect(self.changedValue)

        vbox2.addWidget(numeratorLabel)
        vbox2.addStretch(1)
        vbox2.addWidget(denominatorLabel)
        vbox2.addStretch(1)
        vbox2.setAlignment(Qt.AlignHCenter)
        vbox3.addWidget(numeratorSlider)
        vbox2.addStretch(1)
        vbox3.addWidget(denominatorSlider)
        vbox3.addStretch(1)
        vbox3.setAlignment(Qt.AlignHCenter)
        vbox3.addStretch(1)
        main.addStretch(1)
        main.setAlignment(Qt.AlignHCenter)
        self.mainControl.setLayout(main)

if __name__ == '__main__':
    appctxt = AppContext()                      # 4. Instantiate the subclass
    exit_code = appctxt.run()                   # 5. Invoke run()
    sys.exit(exit_code)