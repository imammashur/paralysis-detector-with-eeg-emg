import matplotlib.pyplot as plt
import matplotlib.animation as animation
import botbook_mcp3002 as mcp

x_len = 200         
y_range = [0, 1023]  

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = list(range(0, 200))
ys = [0] * x_len
ax.set_ylim(y_range)

line, = ax.plot(xs, ys)

plt.title('Data EMG')
plt.xlabel('Waktu')
plt.ylabel('Data')

sensor_emg = 0;

def animate(i, ys):
    sensor_emg = mcp.readAnalog()
    y = sensor_emg
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