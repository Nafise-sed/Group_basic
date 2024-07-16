import numpy as np
from astropy import constants as c
from astropy import units as u

class Apophis(object):

	def __init__(self, G=c.G, apo_mass=2.699e10*u.kg,sol_mass=c.M_sun,
			     v = 34.44*u.km/u.s, n = 365 ):
		# Editable parameters
		self.G = G
		self.a_mass =  apo_mass
		self.sol_mass = sol_mass
		self.v = v
		self.n = n

		# Apophis starting position
		self.x = 0.75 * c.au.to(u.km)
		self.y = 0
	
	def get_position(self):
		pass
		#TODO get_position function

	
