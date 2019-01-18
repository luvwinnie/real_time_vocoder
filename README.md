# Real time vocoder

## Information

This is a real time vocoder created with PyQtGraph and PyQt5.
The Vocoder algorithm is use with the WORLD python wrapper.

The right widget of GUI is used to modify f0 paramter by multiplying a constant value which use numerator constant `a` divided by denominator constant `b` which will be ![constant equation](http://latex.codecogs.com/gif.latex?constant%20%3D%20%5Cfrac%7Ba%7D%7Bb%7D)
The Left widget is a view to plot the raw wave at the bottom with respective spectrogram at 
the top.

The program is built with ![fman build system](https://build-system.fman.io/) package management system.

<div align="center">
<img width="912" alt="screen shot 2019-01-17 at 23 29 54" src="https://user-images.githubusercontent.com/13714992/51364147-7b1d5700-1b1e-11e9-8e55-2e14f818e122.png">
</div>

## Requirements
You need to install PyQt5, pyqtgraph, PyAudio, pyworld in order to run the program.

```
PyAudio==0.2.11
pyqtgraph==0.10.0
PyQt5==5.11.3
PyQt5-sip==4.19.13
pyworld==0.2.8
fbs==0.6.5
```

## Run the Program
Change the directory to `real_time_vocoder` and run the below command.

```sh
fbs run
```

# <font color="red">CAUTION/注意</font>
<font color="red">
Please make sure you are plug in the headphone earphone to listen the sound. If you use the laptop speaker, it will cause the howling.

必ずヘッドホンやイヤホンを付けて聞いてください。ノートパソコンなどのスピーカで
ハウンリング
</font>
