import time 
import botbook_mcp3002 as mcp
import matplotlib.pyplot as plt
import matplotlib.animation as animation

x_len = 200         
y_range = [0, 5]  

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = list(range(0, 200))
ys = [0] * x_len
ax.set_ylim(y_range)

line, = ax.plot(xs, ys)

plt.title('Pembacaan EMG pada Raspberry Pi')
plt.xlabel('Sampel')
plt.ylabel('Tegangan')

def readsensor():
	global sensor_emg
	sensor_emg = mcp.readAnalog()

def animate(i, ys):
    nilaix = sensor_emg
    ys.append(nilaix)
    ys = ys[-x_len:]
    line.set_ydata(ys)
    return line,

ani = animation.FuncAnimation(fig,
    animate,
    fargs=(ys,),
    interval=50,
    blit=True)
	
plt.show()