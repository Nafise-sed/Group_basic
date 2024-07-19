import numpy as np
import matplotlib.pyplot as plt
from Apophis_Class import Apophis as A
from matplotlib import animation
from astropy import units as u
from astropy import constants as c

plt.rcParams['font.family'] = "serif"

# Create an Apophis object with a given velocity and increased iterations for better animation
apophis = A(v=30 * u.km/u.s, n=4000)  # v is the velocity in km/s, n is the number of iterations

# Conversion factor from meters to astronomical units (AU)
meters = 6.68459e-12

# Set up the figure and axis for the plot
fig, (ax, ax2) = plt.subplots(ncols=2, nrows=1, figsize=(12,5.5), gridspec_kw=dict(width_ratios=[1, 1.5], wspace=0.3), )
plt.suptitle('Asteroid Orbit Simulation', fontsize = 18)
ax.set_facecolor("k")
ax.set_xlim(-1 * c.au.to(u.m).value * meters, 3 * c.au.to(u.m).value * meters)
ax.set_ylim(-2 * c.au.to(u.m).value * meters, 2 * c.au.to(u.m).value * meters)
ax.set_aspect('equal')
ax.set_xlabel(r'$X$ (AU)')
ax.set_ylabel(r'$Y$ (AU)')

# --------------------------------------------------

# Create the Sun representation on the plot
sun, = ax.plot([0], [0], "y*", markersize=3.5, label='Sun')  # Sun is yellow and larger marker size

# Distances of planets in AU
distances = [0.39, 0.72, 1.00, 1.52, 5.20]

# Plot each circle
for distance in distances:
    circle = plt.Circle((0, 0), distance, linestyle='dashdot', edgecolor='white', fill=False, alpha=0.7)
    ax.add_patch(circle)

# Asteroid belt range in AU
asteroid_belt_min = 2.1
asteroid_belt_max = 3.3

# Generate random positions for the asteroid belt
asteroid_belt_radii = np.random.uniform(asteroid_belt_min, asteroid_belt_max, 1000)
asteroid_belt_angles = np.random.uniform(0, 2 * np.pi, 1000)
asteroid_belt_x = asteroid_belt_radii * np.cos(asteroid_belt_angles)
asteroid_belt_y = asteroid_belt_radii * np.sin(asteroid_belt_angles)

# Scatter plot for the asteroid belt
ax.scatter(asteroid_belt_x, asteroid_belt_y, s=1, color='grey', alpha=1)

# ---------------------------------------------------

# Create the asteroid representation on the plot
asteroid, = ax.plot([], [], marker = '.', color = 'deepskyblue', markersize = 3, label='Asteroid')  # Asteroid is blue

# Create the trajectory line for the asteroid
trajectory, = ax.plot([], [], ls = "-", color = "deepskyblue", alpha=0.8)

# Create the velocity plot on the secondary axis
vel, = ax2.plot([], [], 'k-')
ax2.set_xlabel(r'Time (days)')
ax2.set_ylabel('Inst. Velocity (km/s)')
ax2.set_xlim(0, 1000)
ax2.set_ylim(0, 400)
ax2.grid(ls='--', alpha=0.4)

# Add a legend to the plot
ax.legend(ncols = 2)

# Initialize the animation by setting empty data for asteroid, trajectory, and velocity
def init():
    """
    Initialize the animation.

    Returns:
        sun, asteroid, trajectory, vel: The initial plot elements.
    """
    asteroid.set_data([], [])
    trajectory.set_data([], [])
    vel.set_data([], [])
    return sun, asteroid, trajectory, vel

# Lists to store positions and velocities over time
positions_x = []
positions_y = []
g_vel = []
time = []

def update(frame):
    """
    Update function for the animation.

    Args:
        frame (int): The current frame number.

    Returns:
        sun, asteroid, trajectory, vel: The updated plot elements.
    """
    # Get the current position of the asteroid
    x, y = apophis.get_position()
    
    # Calculate the gravitational velocity at the current position
    v = apophis.calc_g_vel(np.sqrt((x * x) + (y * y)))

    # Convert positions to astronomical units (AU)
    x, y = x.value * meters, y.value * meters

    # Append the current velocity and time to their respective lists
    g_vel.append(v.value / 1000)
    time.append(frame)
    positions_x.append(x)
    positions_y.append(y)
    
    # Update the data for the asteroid and its trajectory
    asteroid.set_data([x], [y])  # Pass x and y as sequences
    trajectory.set_data(positions_x, positions_y)
    vel.set_data(time, g_vel)

    # Adjust the x-axis limits of the velocity plot if necessary
    _, xlim_max = ax2.get_xlim()
    if frame > xlim_max:
        xlim_max += 500
        ax2.set_xlim(0, xlim_max)

    return sun, asteroid, trajectory, vel

# Create the animation
ani = animation.FuncAnimation(fig, update, frames=range(apophis.n), init_func=init, blit=False, interval=50)

# Display the plot
plt.show()

