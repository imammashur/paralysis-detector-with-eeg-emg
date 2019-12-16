# Masuk di Raspberry pi lalu buka terminal, ketik :
# dmesg

# Dalam terminal, cari device identifier yaitu ttyUSB0 seperti ini :
# [   36.216956] usb 1-1.4: ch341-uart converter now attached to ttyUSB0

# install mathplotlib dengan cara ketik di termminal:
# sudo apt-get install python3-matplotlib
# cd ~
# git clone https://github.com/JoBergs/mindwave-python
# cd mindwave-python
# buat file text dgn nama: mindwave_LED.py
# isinya yaitu kode di bawah :

import mindwave, time
import matplotlib.pyplot as plt
import matplotlib.animation as animation

headset = mindwave.Headset('/dev/ttyUSB0', '0D1B')
time.sleep(2)

headset.connect()
print "Connecting..."

while headset.status != 'connected':
    time.sleep(0.5)
    if headset.status == 'standby':
        headset.connect()
        print "Retrying connect..."
print "Connected."

x_len = 200         
y_range = [0, 100]  

line, = ax.plot(xs, ys)

plt.title('Data EEG')
plt.xlabel('Waktu')
plt.ylabel('Data')

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = list(range(0, 200))
ys = [0] * x_len
ax.set_ylim(y_range)


def animate(i, ys):
    sensor_eeg = headset.attention + headset.meditation
    sensor_eeg = sensor_eeg / 2 
    y = sensor_eeg
    ys.append(y)
    ys = ys[-x_len:]
    line.set_ydata(ys)
    return line,

ani = animation.FuncAnimation(fig,
    animate,
    fargs=(ys,),
    interval=50,
    blit=True)
plt.show()