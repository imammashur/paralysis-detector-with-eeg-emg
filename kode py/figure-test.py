import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random

# Batas
x_len = 200         
y_range = [10, 40]  

# Buat figure
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = list(range(0, 200))
ys = [0] * x_len
ax.set_ylim(y_range)


# Buat blank line
line, = ax.plot(xs, ys)

# Label
plt.title('Tes Grafik')
plt.xlabel('Samples')
plt.ylabel('Nilai')

# Animasi
def animate(i, ys):

    # Ambil nilai x
    nilaix = random.randint(10,40)

    # Tambah ke y
    ys.append(nilaix)

    # Batas nilai y
    ys = ys[-x_len:]

    # Update nilai
    line.set_ydata(ys)

    return line,

# Buat plot
ani = animation.FuncAnimation(fig,
    animate,
    fargs=(ys,),
    interval=50,
    blit=True)
	
plt.show()