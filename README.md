# VisualGold [WIP]
### Simple Sound Visualizer
#### WORKS ONLY WITH Python3.6
#### Oscilloscope and Spectrum Analyser based on PyQtGraph
it will listen to "stereomix" you can find that in the soundsettings > recording
double click it and go to the listen tab, select your output device. then install the requirements:

you'll need PyQtGraph if you didn't already download and install it from http://www.pyqtgraph.org/

after, install all requirements with ```pip install -r requirements.txt```

if there are no errors you're good to go. otherwise:

if it fails at pyaudio (likely, if you are on windows) it's an easy fix: install and use pipwin:
```
pip install pipwin
pipwin install pyaudio
```

everything else should work OTB

start with: ```python main.py``` make sure you're running python3.6

by clicking on the "A" next to the graphs you can auto-adjust the range that's displayed

___

## Help
```
usage: main.py [-h] [-V] [-v] [-x]

VisualGold for Windows (Python3)

optional arguments:
  -h, --help     show this help message and exit
  -V, --version  Displays current version
  -v, --verbose  Sets logger level to show debug info
  -x, --xtreme   Sets logger level to show even more debug
  ```
