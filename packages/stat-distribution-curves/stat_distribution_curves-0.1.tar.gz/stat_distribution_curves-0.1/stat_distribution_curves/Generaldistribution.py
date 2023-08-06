import math
import matplotlib.pyplot as plt

class Distribution:
	def __init__(self, mu=0, sigma=1):
		self.mean = mu
		self.stdev = sigma
		self.data = []


	def calculate_mean(self):
		"""Method to calculate mean of some data

		Args:
			None

		Returns:
			float: mean of the data set

		"""
		return sum(self.data)/len(self.data)

	def calculate_stdev(self, sample=True):
		"""Method to calculate standard deviation of dataset

		Args:
			sample (bool): whether the data represents sample or population

		Returns:
			float: standard deviation of dataset

		"""
		sum_of_diffs = sum([(i-self.mean)**2 for i in self.data])

		if sample:
			return math.sqrt(sum_of_diffs/(len(self.data)-1))

		else:
			return math.sqrt(sum_of_diffs/len(self.data))
			

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

		self.mean = self.calculate_mean()

		self.stdev = self.calculate_stdev()

	def plot_histogram(self):
		"""Method to output a histogram of the instance variable data using matplotlib pyplot library

		Args:
			None

		Returns:
			None

		"""
		plt.hist(self.data)
		plt.ylabel('counts')
		plt.xlabel('data')
		plt.show()