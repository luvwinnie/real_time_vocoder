from fbs_runtime.application_context import ApplicationContext
from PyQt5.QtWidgets import QMainWindow
from pyqtgraph.dockarea import DockArea, Dock
from pyqtgraph.Qt import QtCore
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
        d1 = Dock("Dock1", size=(500,300),closable=False)
        d6 = Dock("Dock6 (tabbed) - Plot", size=(500,200))
        parameter_widget = parameterWidget()
        parameter_widget2 = parameterWidget()
        parameter_widget.setObjectName("F0Slider")
        parameter_widget.setStyleSheet("""
            QSlider{
                background:red;
                size:100px;
            }
        """)
        spectogram_widget = SpectrogramWidget()
        wave_widget = WaveWidget()
        mic = MicrophoneRecorder(True,spectogram_widget.read_collected,wave_widget.read_collected)
        d1.addWidget(spectogram_widget)
        d1.addWidget(wave_widget)
        d6.addWidget(parameter_widget2)
        area.addDock(d1)
        area.addDock(d6,"right")

        interval = FS/CHUNKS
        t = QtCore.QTimer()
        t.timeout.connect(mic.read)
        t.start(interval/100000) #QTimer takes ms

        
        window.resize(1000,600)
        window.setCentralWidget(area)
        window.show()
        return self.app.exec_()                 # 3. End run() with this line

if __name__ == '__main__':
    appctxt = AppContext()                      # 4. Instantiate the subclass
    exit_code = appctxt.run()                   # 5. Invoke run()
    sys.exit(exit_code)