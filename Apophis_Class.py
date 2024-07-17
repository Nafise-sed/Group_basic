import numpy as np
from astropy import constants as c
from astropy import units as u
import matplotlib.pyplot as plt

class Apophis(object):

	def __init__(self, G=c.G, apo_mass=2.699e10*u.kg,sol_mass=c.M_sun,
			     v = 34.44*u.km/u.s, n = 365 ):
		# Editable parameters
		self.G = G	# Gravitational constant
		self.a_mass =  apo_mass # asteroid mass
		self.sol_mass = sol_mass # solar mass
		self.v = v.to(u.m/u.s) # Starting velocity
		self.n = n # number of iterations

		# Apophis starting position and semi-major axis
		self.x = 0.75 * c.au.to(u.m)
		self.perx = 0.75 * c.au.to(u.m)
		self.y = 0 * u.m
		self.sma = 0.9225 * c.au.to(u.m)
	
	def get_position(self):
		
		radius = np.sqrt(self.x**2 + self.y**2)
		g_vel = self.calc_g_vel(radius)
		g_angle = np.arctan2(self.y,self.x)
		
		# Orbital velocity is always going to be perpendicular to gravitational velocity
		# Not sure how to easily translate the orbital velocity into x and y components
		orb_angle = (np.pi/2)*u.rad + g_angle # Does this work? At (x,y) = (1,0) orb_angle is 90. At (0,1) it's 180.
								# it's the opposite direction of where g_v WILL be pointed 90 degrees later

		# Break the velocities into x and y components
		g_vx = g_vel * np.cos(g_angle) 
		g_vy = g_vel * np.sin(g_angle) 

		#g_vx = (vel_rad * np.cos(g_angle)) - (vel_tan * np.sin(g_angle))
		#g_vy = (vel_rad * np.sin(g_angle)) + (vel_tan * np.cos(g_angle))

		o_vx = self.v * np.cos(orb_angle)
		o_vy = self.v * np.sin(orb_angle)

		# Calc distance traveled
		time = u.day.to(u.second)*u.second
		
		# Ensure gravity is always pulling the object towards the center
		if self.x > 0:
			g_dx = -g_vx * time
		else: g_dx = g_vx * time

		if self.y > 0:
			g_dy = -g_vy * time
		else: g_dy = g_vy * time
		
		o_dx = o_vx * time
		o_dy = o_vy * time

		self.x = self.x + o_dx + g_dx
		self.y = self.y + o_dy + g_dy
		#self.x = self.x + g_dx
		#self.y = self.y + g_dy
		
		print(g_vel)
		return(self.x,self.y)
		# Whatever calls get_position will need to return not just the x and y but also the 
		# step number for plotting
		# using self.x and self.y so that we can update the position with every iteration of get_position

	def calc_g_vel(self, radius):
		# We need a catch here for if the orbit becomes parabolic or hyperbolic
		# (2/radius - 1/self.sma) < 0)
		g_vel = (self.G * self.sol_mass * (2 / radius - 1 / self.sma)) ** 0.5
		#vel_tan = (self.v * self.perx)/self.x
		#vel_rad = np.sqrt(g_vel**2 - vel_tan**2)
		#return(g_vel, vel_tan, vel_rad)
		return(g_vel)
	
	def run_apophis(self):
		for i in range(self.n):
			x,y = self.get_position()
			plt.plot(x,y,color='blue',marker='o',markersize=5)
		plt.plot(0,0,color='yellow',marker='*',markersize=20)
		plt.show()

a = Apophis(n=100)
a.run_apophis()
