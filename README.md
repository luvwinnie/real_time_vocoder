# Real-time vocoder

## Information

This is a real-time vocoder created with PyQtGraph and PyQt5.
The Vocoder algorithm is use with the WORLD python wrapper.

The right widget of GUI is used to modify f0 paramter by multiplying a constant value which use numerator constant `a` divided by denominator constant `b` which will be formula as below.
The Left widget is a view to plot the raw wave at the bottom with respective spectrogram at 
the top.

The program is built with [fman build system](https://build-system.fman.io/) package management system.

これはWORLD音声処理のアルゴリズム、pythonのwrapperを用いて、PyQtGraphまたはPyQt5でGUIを作成し、リアルタイムで音声を録音し、音声合成処理を行い、出力するソフトウェアである。以下のGUIのように左側は音声の生波形とそのスペクトラムをプロットするガジェットであり、右側のガジェットは基本周波数f0を調整するためのものである。f0を調整するためには定数を掛け算するが、その係数は分子(numerator)a割る分母(denominator)bで計算されます。式は以下の様になる。

<div align="center">
<img src="http://latex.codecogs.com/gif.latex?pitch%5C%20constant%20%3D%20%5Cfrac%7Ba%7D%7Bb%7D" width="150">
</div>

<div align="center">
<img width="912" alt="screen shot 2019-01-17 at 23 29 54" src="https://user-images.githubusercontent.com/13714992/51364147-7b1d5700-1b1e-11e9-8e55-2e14f818e122.png">
</div>

## Requirements
The software is tested in Ubuntu 18.04LTS and MacOS Mojave(10.14.2) with `python3`.
You need to install PyQt5, pyqtgraph, PyAudio, pyworld in order to run the program.
Install the required package with following command.

### Ubuntu
```
virtualenv --no-site-package real-time-vocoder
source real-time-vocoder/bin/activate
pip3 install --no-cache-dir -r requirements.txt
```

### MacOS Mojave(10.14.2)/XCode 10.1
```
virtualenv --no-site-package real-time-vocoder
source real-time-vocoder/bin/activate
export CC=clang;export CXX=clang++;
pip3 install --no-cache-dir -r requirements.txt
```
### Required Package

```
boto3==1.9.81
botocore==1.12.81
Cython==0.29.2
docutils==0.14
fbs==0.6.6
jmespath==0.9.3
numpy==1.16.0
PyAudio==0.2.11
PyQt5==5.11.3
PyQt5-sip==4.19.13
pyqtgraph==0.10.0
python-dateutil==2.7.5
pyworld==0.2.8
s3transfer==0.1.13
six==1.12.0
urllib3==1.24.1
```


## Run the Program
Change the directory to `real_time_vocoder` and run the below command.

以上のパッケージをインストールし終わりましたら、マイクとヘッドホンなどを接続し、以下のコマンドで実行する。

```sh
cd real_time_vocoder
fbs run
```

# <font color="red">CAUTION/注意</font>
<font color="red">
Please make sure you are plug in the headphone earphone to listen the sound. If you use the laptop speaker, it will cause the howling.

必ずヘッドホンやイヤホンを付けて聞いてください。ノートパソコンなどのスピーカで出力すると、
ハウンリングが起こります。
</font>
