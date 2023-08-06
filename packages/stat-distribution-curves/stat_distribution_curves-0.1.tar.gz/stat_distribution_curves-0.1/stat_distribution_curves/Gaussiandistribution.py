import math
import matplotlib.pyplot as plt
from .Generaldistribution import Distribution

class Gaussian(Distribution):
	"""Gaussian distribution class for calculating and visualizing Gaussian distributions

	Attributes:
		mean (float) representing the mean value of the distribution
		stdev (float) is the standard deviation of the distribution
		data_list (list of floats) is the data extracted from file
	"""
	def __init__(self, mu=0, sigma=1):
		Distribution.__init__(self, mu, sigma)

	def pdf(self, x):
		"""Method to calculate probability densities for the gaussian distribution

		Args:
			x (float): point for calculating the probability density function

		Returns:
			float: probability density function output

		"""
		power = -(x-self.mean)**2/(2*self.stdev**2)
		base = 1/(math.sqrt(2*math.pi*self.stdev**2))

		return base*math.exp(power)

	def plot_histogram_pdf(self, n_spaces=50):
		"""Method to plot the normalized histogram of data and 
		probability density function along the same axis
		
		Args:
			n_spaces (int): number of data points

		Returns:
			list: x values for the pdf plot
			list: y values for the pdf plot

		"""
		mu = self.mean
		sigma = self.stdev

		min_range = min(self.data)
		max_range = max(self.data)

		interval = (max_range - min_range)/n_spaces

		x = []
		y = []

		for i in range(n_spaces):
			temp = i*interval + min_range
			x.append(temp)
			y.append(self.pdf(temp))

		fig, axes = plt.subplots(2, sharex=True)
		fig.subplots_adjust(hspace=0.5)
		axes[0].hist(self.data, density=True)
		axes[0].set_title('Normed histogram of Data')
		axes[0].set_ylabel('Density')

		axes[1].plot(x,y)
		axes[1].set_title('Normal Distribution of \n sample mean and standard distribution')
		axes[1].set_ylabel('Density')
		plt.show()

		return x,y


	def __add__(self, other):
		"""Magic method to add two gaussian distributions
		Args:
			other (Gaussian): Gaussian instance to add current instance to

		Returns:
			Gaussian: Gaussian distribution 

		"""
		result = Gaussian()
		result.mean = self.mean + other.mean
		result.stdev = math.sqrt(self.stdev**2 + other.stdev**2)

		return result

	def __repr__(self):
		"""Magic method to output characteristics of Gaussian instance

		Args:
			None

		Returns:
			string: characteristics of Gaussian instance

		"""
		return 'mean: {0}, stdev: {1}'.format(self.mean, self.stdev)
