import math
import matplotlib.pyplot as plt
from .Generaldistribution import Distribution

class Binomial(Distribution):
	"""Binomial distribution class for calculating and visualizing binomial distributions

	Attributes:
		mean (float) representing mean of the distribution
		stdev (float) representing standard deviation of distribution
		data (list of floats) is the data extracted from a file
	"""
	def __init__(self, mu=0.5, sigma=0, p=0.5):
		Distribution.__init__(self, mu, sigma)
		self.p = p

	def calculate_p(self):
		self.p = sum(self.data)/len(self.data)

	def calculate_mean(self):
		return self.p*len(self.data)

	def calculate_stdev(self):
		n = len(self.data)
		return math.sqrt(n*self.p*(1-self.p))


	def read_data_file(self, file_name, sample=True):
		"""Fetch data from the local repository

		Args:
			file_name (str): name of the file we want to read from

		Returns:
			None

		"""
		with open(file_name) as file:
			data_list = []
			line = file.readline()
			while line:
				data_list.append(int(line))
				line = file.readline()
		file.close()

		self.data = data_list

		self.calculate_p()

		self.mean = self.calculate_mean()

		self.stdev = self.calculate_stdev()

	def pdf(self, k):
		"""Method to calculate probability densities of the binomial distribution

		Args:
			x (float): point for which to calculate probability density

		Returns:
			float: probability density output at x
		"""
		n = len(self.data)
		n_fact = math.factorial(n)
		k_fact = math.factorial(k)
		n_k_fact = math.factorial(n-k)
		base = n_fact/(k_fact*n_k_fact)

		return base*(self.p**k)*(1-self.p)**(n-k)


	def plot_histogram_pdf(self):
		x = [k for k in range(len(self.data))]
		y = [self.pdf(k) for k in x]

		fig, ax = plt.subplots(2, sharex=False)
		fig.subplots_adjust(hspace=0.5)

		ax[0].hist(self.data, density=True)
		ax[0].set_title('normalzed distribution of data')
		ax[0].set_xlabel('data')
		ax[0].set_ylabel('Density')

		ax[1].plot(x,y)
		ax[1].set_title('Binomial eDistribution')
		ax[1].set_xlabel('k')
		ax[1].set_ylabel('Density')

		plt.show()

		return x,y

	def __add__(self, other):
		"""Magic method to add two binomial distributions

		Args:
			other (Bonomial): Binomial distribution to add current distribution to

		Returns:
			Binomial: Binomial distribution
		"""
		result = Binomial()
		n = len(self.data)+len(other.data)
		result.mean = n*self.p
		result.stdev = math.sqrt(n*self.p*(1-self.p))
		return result

	def __repr__(self):
		return "mean: {0}, stdev: {1}".format(self.mean, self.stdev)
