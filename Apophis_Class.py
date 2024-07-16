import numpy as np
from astropy import constants as c

class Apophis(object):

	def __init__(self, G=c.G, apo_mass=2.699e10,sol_mass=c.M_sun):
		self.G = G
		#TODO save other variables that are given to the class
