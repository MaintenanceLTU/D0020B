import LIS33HH
import numpy as np
import queue
import matplotlib.pyplot as plt
import matplotlib.animation as anim

LIS33HH.power("normal")
LIS33HH.rang("12g")
LIS33HH.BDU("block")

fig, (ax_X, ax_Y, ax_Z) = plt.subplots(ncols = 1, nrows = 3, figsize = [14.5, 5.6])

ax_X.set_ylim(-1.5, 1.5)
ax_X.set_title("Accel X")

ax_Y.set_ylim(-1.5, 1.5)
ax_Y.set_title("Accel Y")

ax_Z.set_ylim(-1.5, 1.5)
ax_Z.set_title("Accel Z")

x = np.arange(0, 100)
X = np.zeros(len(x))
Y = np.zeros(len(x))
Z = np.zeros(len(x))
      
line_X, = ax_X.plot(x, X)
line_Y, = ax_Y.plot(x, Y)
line_Z, = ax_Z.plot(x, Y)

def init():
    line_X.set_ydata([np.nan]*len(x))
    line_Y.set_ydata([np.nan]*len(x))
    line_Z.set_ydata([np.nan]*len(x))
    
    return line_X, line_Y, line_Z

def animate(i):
    global X, Y, Z 
    
    acc = LIS33HH.get_res("all")
       
    X = np.delete(X, 0, 0)
    X = np.append(X, [acc["X"]], 0)
    line_X.set_ydata(X)

    Y = np.delete(Y, 0, 0)
    Y = np.append(Y, [acc["Y"]], 0)
    line_Y.set_ydata(Y)

    Z = np.delete(Z, 0, 0)
    Z = np.append(Z, [acc["Z"]], 0)
    line_Z.set_ydata(Z)

    
    return line_X, line_Y, line_Z

try:
    ani = anim.FuncAnimation(fig, animate, interval = 20, init_func=init, blit=True,
                         save_count=50)
    plt.show()
       
except KeyboardInterrupt:

    pls.close()
    
    print("Goodbye")   


