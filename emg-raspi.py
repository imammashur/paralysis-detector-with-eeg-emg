# Install dulu ini di terminal :
# sudo apt-get install python-dev python-pip
# sudo pip install python
# sudo mod probe spi_bcm2708
# sudo pip install spidev
# echo spi_bcm2708 | sudo tee -a /etc/modules

import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Parameter-Parameter
x_len = 200         # Panjang-x
y_range = [0, 5]  # Panjang-y

# Buat tempat plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = list(range(0, 200))
ys = [0] * x_len
ax.set_ylim(y_range)


# Buat blank line.
line, = ax.plot(xs, ys)

# Buat label
plt.title('EMG Dengan Raspberry Pi')
plt.xlabel('Waktu')
plt.ylabel('Tegangan Sensor')

def read(adc_channel=0, spi_channel=0):
    spi = spidev.SpiDev()
    spi.open(0, spi_channel)
    spi.max_speed_hz = 1200000 # 1.2 MHz
    cmd = 128
    if adc_channel:
        cmd += 32
    reply_bytes = spi.xfer2([cmd, 0])
    reply_bitstring = ''.join(bitstring(n) for n in reply_bytes)
    reply = reply_bitstring[5:15]
    spi.close()
    return int(reply, 2) / 2**10

# Fungsi yang dipanggil secara periodik
def animate(i, ys):    
    teg = round(read(), 2)
    ys.append(teg)
    ys = ys[-x_len:]
    line.set_ydata(ys)
    return line,


	
# Atur pemanggilan
ani = animation.FuncAnimation(fig,
    animate,
    fargs=(ys,),
    interval=50,
    blit=True)
	
plt.show()