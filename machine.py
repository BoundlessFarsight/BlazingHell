from automata import Automaton
from data_generator import data
import pandas as pd
import numpy as np
import random as rd
from time import time
import matplotlib.pyplot as plt

# Pour commencer, pour pas trop se prendre la tête, on va fixer firestart constamment à x_max/2, y_max/2

np.random.seed(1100)
# rd.seed(0)

class machine:
	
	def __init__(self, data, mb_size, c_intercept = 0, c_moisture = 0, h = 0.01, learning_rate = 0.000003):
		self.data = data
		self.mb_size = mb_size
		self.c_intercept = c_intercept
		self.c_moisture = c_moisture
		self.h = h
		self.learning_rate = learning_rate
	
	
# 	Computes the approximation of the gradient for the instance of data at index k
	
	def gradient(self, k):
		
		moisture = self.data.iloc[k]['moisture']
		value = self.data.iloc[k]['value']
		
		x,y = moisture.shape

# 		On calcule d'abord la prédiction sur le paramètre actuel			
		auto_0 = Automaton(self.c_intercept, self.c_moisture, shape = (x,y), firestart = (int(x/2), int(y/2)), moisture = moisture)
		c_0 = (auto_0.run() - value)**2
		
# 		Puis avec chacun des paramètres augmenté de self.h
# 		On peut ensuite calculer la dérivée partielle par rapport à chaque paramètre et actualiser le gradient

# 		c_intercept + h d'abord
		auto_i = Automaton(self.c_intercept + self.h, self.c_moisture, shape = (x,y), firestart = (int(x/2), int(y/2)), moisture = moisture)
		c_i = (auto_i.run() - value)**2			
		g_i = (c_i - c_0)/self.h
			
# 		c_moisture + h ensuite
		auto_m = Automaton(self.c_intercept, self.c_moisture + self.h, shape = (x,y), firestart = (int(x/2), int(y/2)), moisture = moisture)
		c_m = (auto_m.run() - value)**2			
		g_m = (c_m - c_0)/self.h
		
		return g_i, g_m


	
	def learn_step(self):
		
# 		First we get a subset of mb_size element of data
# 		We randomly select rows, and each row might get selected more than once
		
		n = len(self.data)
		l = [k for k in range(n)]
		ll = rd.choices(l, k = self.mb_size)
		
# 		The point of all this is to compute the gradient over the minibatch so we initiate a gradient and then average over all rows of the minibatch
		
		grad_intercept = 0
		grad_moisture = 0
		
		for k in ll:			
			g_i, g_m = self.gradient(k)
			
			grad_intercept += g_i
			grad_moisture += g_m
			
# 		Then we use the gradient by normalizing it and adding it to the parameter
			
		grad_intercept = (grad_intercept/self.mb_size)*self.learning_rate
		grad_moisture = (grad_moisture/self.mb_size)*self.learning_rate
		
		self.c_intercept -= grad_intercept
		self.c_moisture -= grad_moisture

	
	def learning(self,n):
		for k in range(n):
			self.learn_step()
	
	def predict(self, moisture, firestart = (25,25)):
		auto = Automaton(self.c_intercept, self.c_moisture, moisture.shape, firestart, moisture)
		return auto.run()


bigdata = data(10, 0.5, -7, shape = (50,50), firestart = (25,25))
daneel = machine(bigdata, mb_size = 10)


for k in range(50):
	daneel.learn_step()
	print(daneel.c_intercept)
	print(daneel.c_moisture)
	print()

