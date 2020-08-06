# coding: UTF-8



### import
import sys
sys.path.append('/usr/local/lib/python3.7/site-packages')
import sys
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
import random
from spectrum import *
import serial
from tqdm import tqdm
from scipy import integrate



### replace this port name by yours!
portName = "/dev/tty.SLAB_USBtoUART"    
baudrate = 115200
ser = serial.Serial(portName,baudrate)



### create empty array
sub = np.zeros(0)



### progressbar
p = 100
pbar = tqdm(total=p)

n = 0
while n <= p:
    value = ser.readline() 
    sub = np.append(sub,int(value))
    if sub[n] < 400 or sub[n] > 2000:
        print(u'センサーが上手くデータを取れてません')
    n += 1
    pbar.update(1)

# print(sub)
pbar.close()



### Test Data
# d = np.array([875, 849, 848, 1700, 841, 861, 855, 865, 860, 876, 882, 874, 865, 879, 862, 916, 881, 875, 885, 878, 859, 897, 880, 845, 901, 1759, 898, 900, 857, 881, 868, 856, 880, 863, 856, 880, 878, 844, 877, 864, 843, 858, 878, 865, 855, 879, 917, 882, 938, 884, 975, 926, 914, 942, 961, 915, 942, 901, 920, 920, 881, 940, 925, 875, 1777, 879, 891, 910, 865, 898, 921, 922, 914, 923, 901, 883, 933, 484, 399, 1798, 926, 877, 921, 977, 898, 923, 939, 945, 920, 954, 948, 998, 975, 901, 942, 945, 915, 1815, 864, 918])



### input sensor data
d = sub



### set up pyqtgraph
app = QtGui.QApplication([])

win = pg.GraphicsWindow(title="HRVモニター")
win.resize(1000,600)
win.setWindowTitle('pyqtgraph example: Plotting')

pg.setConfigOptions(antialias=True)

p6 = win.addPlot(title="パワースペクトル")
p5 = win.addPlot(title="RR間隔")

p6.setXRange(0, 0.4)
# p6.setYRange(0,30)
curve = p6.plot(pen='y')
curve2 = p5.plot(pen='y')
data = d
ptr = 0



### calculate power spectrum
AR, P, k  = arburg(data, 8)
BBB = arma2psd(AR,sides='centerdc')
PSD = BBB[2048:4096]
y = 10*log10(PSD/max(PSD))

p = np.linspace(0.05, 0.15,768-256)
h = np.linspace(0.05, 0.15,2048-768)



### loop the pyqtgraph
def update():
    global curve, data, ptr, p6, PSD, y, BBB, AR, P, k, p, h
    plus = 65
    curve.setData(linspace(0, 0.4,len(PSD)),y+plus)
    if ptr == 0:
        p6.enableAutoRange('y', True)  ## stop auto-scaling after the first data set is plotted
    ptr += 1
    data = np.roll(data,-1)
    value = ser.readline() 
    data[-1:] = int(value)
    curve2.setData(data)
    AR, P, k  = arburg(data, 8)
    BBB = arma2psd(AR,sides='centerdc')
    PSD = BBB[2048:4096]
    y = 10*log10(PSD/max(PSD))
    LFrange = y[256:768]
    LF = integrate.simps(LFrange+plus, p)
    print('LF:',LF)
    HFrange = y[768:2048]
    HF = integrate.simps(HFrange+plus, h)
    print('HF:',HF)
    print('LF/HF:',LF/HF)
    QtGui.QApplication.processEvents()

timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(10)



### Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()




    
