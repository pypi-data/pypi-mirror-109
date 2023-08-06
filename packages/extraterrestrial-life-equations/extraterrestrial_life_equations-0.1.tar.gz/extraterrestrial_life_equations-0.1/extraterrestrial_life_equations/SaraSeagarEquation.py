import math

class SSEquation:
	""" Revised Drake equation that focuses on the search 
	for planets with biosignature gases by Sara Seagar
	Attributes:
		NumberPlanets (int) representing the number of planets with detectable signs of life
		NumberStars (int) representing the number of stars observed
		FractionStarsQuiet (float) representing the fraction of stars that are quiet
		FractionRocky (float) representing the fraction of stars with rocky planets in the habitable zone
		FractionRockyObserved (float) representing the fraction of those planets that can be observed
		FractionPlanetsLife (float) representing the fraction the fraction that have life
		FractionPlanetsGas(float) representing the fraction on which life produces a detectable signature gas
	"""
	def __init__(self):
		option = 0
		while True:
			print('Choose an option to calculate the number of planets with detectable signs of life: ')   
			print('[0] Defalut values')
			print('[1] Choose your own values')
			option = int(input())
			if option==0:
				self.NumberStars = 30000
				self.FractionStarsQuiet = 0.15
				self.FractionRocky = 0.15
				self.FractionRockyObserved = 0.15
				self.FractionPlanetsLife = 0.15
				self.FractionPlanetsGas = 0.15
				self.calculate()
				self.data()
				break
			elif option == 1:
				self.own_values()
				self.calculate()
				self.data()
				break
			else:
				print('Please choose a correct option')
				print('--------------------------------------------')
	def data(self):
		print('--------------------------------------------')
		print('Number of stars observed: {}'.format(self.NumberStars))		
		print('Fraction of stars that are quiet: {}'.format(self.FractionStarsQuiet))
		print('Fraction of stars with rocky planets in the habitable zone: {}'.format(self.FractionRocky))
		print('Fraction of those planets that can be observed: {}'.format(self.FractionRockyObserved))
		print('Fraction the fraction that have life: {}'.format(self.FractionPlanetsLife))
		print('Fraction on which life produces a detectable signature gas: {} '.format(self.FractionPlanetsGas))
		print('--------------------------------------------')
		print('Number of planets with detectable signs of life: {}'.format(self.NumberPlanets))   
	def own_values(self):
		print('Enter the number of stars observed (30000 by James Webb)')
		self.NumberStars = int(input())
		print('Enter the fraction of stars that are quiet')
		self.FractionStarsQuiet = float(input())
		print('Enter the fraction of stars with rocky planets in the habitable zone')
		self.FractionRocky = float(input())
		print('Enter the fraction of those planets that can be observed')
		self.FractionRockyObserved = float(input())
		print('Enter the fraction the fraction that have life')
		self.FractionPlanetsLife = float(input())
		print('Enter the fraction on which life produces a detectable signature gas')
		self.FractionPlanetsGas = float(input())
	def calculate(self):
		self.NumberPlanets = int(self.NumberStars * self.FractionStarsQuiet * self.FractionRocky * self.FractionRockyObserved * self.FractionPlanetsLife * self.FractionPlanetsGas)