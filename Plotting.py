import numpy as np
import matplotlib.pyplot as plt
from Apophis_Class import Apophis as A
from matplotlib import animation
from astropy import units as u
from astropy import constants as c

temp = A()

print(temp.get_position())

# Set up the Apophis object
apophis = A(v=30 * u.km/u.s, n=5000)  # Increased iterations for better animation

meters = 6.68459e-12 # AU

# Set up the figure and axis
fig, (ax, ax2) = plt.subplots(ncols = 2, nrows = 1, figsize = (12,5), gridspec_kw=dict(width_ratios=[1, 1.5], wspace=0.3))
ax.set_xlim(-1 * c.au.to(u.m).value * meters, 3 * c.au.to(u.m).value * meters)
ax.set_ylim(-2 * c.au.to(u.m).value * meters, 2 * c.au.to(u.m).value * meters)
ax.set_aspect('equal')
ax.grid(True)
ax.set_title('Asteroid Orbit Simulation')
ax.set_xlabel('X Position (AU)')
ax.set_ylabel('Y Position (AU)')

# Create the Sun
sun, = ax.plot([0], [0], 'yo', markersize=4, label='Sun')  # Sun is yellow and larger marker size

# Create the asteroid
asteroid, = ax.plot([], [], 'bo', markersize=3, label='Asteroid')  # Asteroid is blue

# Create the trajectory line
trajectory, = ax.plot([], [], 'b-', alpha=0.5)

# Get the velocity
vel, = ax2.plot([], [], 'k-')

ax2.set_xlabel('Time')
ax2.set_ylabel('g_vel (km/s)')
# ax2.set_aspect('equal')
ax2.set_xlim(0, 1000)
ax2.set_ylim(0, 400)
ax2.grid(ls = '--', alpha = 0.4)

# Add a legend
ax.legend()

# Initialize the animation
def init():
    asteroid.set_data([], [])
    trajectory.set_data([], [])
    vel.set_data([], [])
    return sun, asteroid, trajectory, vel

# Update function for the animation
positions_x = []
positions_y = []
g_vel = []
time = []

def update(frame):
    x, y = apophis.get_position()
    v = apophis.calc_g_vel(np.sqrt( (x * x) + (y * y) ))

    x, y = x.value * meters, y.value * meters

    g_vel.append(v.value / 1000)
    time.append(frame)
    positions_x.append(x)
    positions_y.append(y)
    
    asteroid.set_data([x], [y])  # Pass x and y as sequences
    trajectory.set_data(positions_x, positions_y)
    vel.set_data(time, g_vel)

    _, xlim_max = ax2.get_xlim()
    if(frame > xlim_max):
        xlim_max += 500
        ax2.set_xlim(0, xlim_max)

    return sun, asteroid, trajectory, vel

# Create the animation
ani = animation.FuncAnimation(fig, update, frames = range(apophis.n), 
                              init_func=init, blit=False, interval=100)

plt.show()
