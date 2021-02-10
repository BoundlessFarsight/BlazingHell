import numpy as np
import matplotlib.pylab as plt
import pandas as pd
from automata import Automaton
import random as rd

np.random.seed(0)

from matplotlib.animation import FuncAnimation
from matplotlib.colors import ListedColormap
from matplotlib.colors import BoundaryNorm

cmap = ListedColormap(['g', 'r', 'k'])
boundaries = [0, 1.5, 2.5, 4]
norm = BoundaryNorm(boundaries, cmap.N, clip=True)

# Credits for the perlin generator : https://stackoverflow.com/questions/42147776/producing-2d-perlin-noise-with-numpy

def perlin(x,y,seed=np.random.randint(10000000)):
    # permutation table
    np.random.seed(seed)
    p = np.arange(256,dtype=int)
    np.random.shuffle(p)
    p = np.stack([p,p]).flatten()
    # coordinates of the top-left
    xi = x.astype(int)
    yi = y.astype(int)
    # internal coordinates
    xf = x - xi
    yf = y - yi
    # fade factors
    u = fade(xf)
    v = fade(yf)
    # noise components
    n00 = gradient(p[p[xi]+yi],xf,yf)
    n01 = gradient(p[p[xi]+yi+1],xf,yf-1)
    n11 = gradient(p[p[xi+1]+yi+1],xf-1,yf-1)
    n10 = gradient(p[p[xi+1]+yi],xf-1,yf)
    # combine noises
    x1 = lerp(n00,n10,u)
    x2 = lerp(n01,n11,u) # FIX1: I was using n10 instead of n01
	 
# 	 MAKE RANDOM RANDOM AGAIN !
#   np.random.seed(int(rd.random()*10000))
	 
    return lerp(x1,x2,v) # FIX2: I also had to reverse x1 and x2 here

def lerp(a,b,x):
    "linear interpolation"
    return a + x * (b-a)

def fade(t):
    "6t^5 - 15t^4 + 10t^3"
    return 6 * t**5 - 15 * t**4 + 10 * t**3

def gradient(h,x,y):
    "grad converts h to the right gradient vector and return the dot product with (x,y)"
    vectors = np.array([[0,1],[0,-1],[1,0],[-1,0]])
    g = vectors[h%4]
    return g[:,:,0] * x + g[:,:,1] * y



# data returns n instances of fires computed with the parameter c_intercept, c_moisture

# firestart is fixed

# seed, moisture, value

def data(n, c_intercept, c_moisture, shape, firestart):
	
	df = pd.DataFrame(columns = ['seed', 'moisture', 'value'])
	
	x,y = shape
	lx = np.linspace(0,5,x,endpoint=False)
	ly = np.linspace(0,5,y,endpoint=False)
	X,Y = np.meshgrid(lx,ly)
	
	for k in range(n):
		moisture = perlin(X,Y,seed=k) + 0.5
		auto = Automaton(c_intercept, c_moisture, shape, firestart, moisture)
		value = auto.run()
		df.loc[k] = [k, moisture, value]
	
	return df

if __name__ == "__main__":
	x,y = 50,50
	lx = np.linspace(0,5,x,endpoint=False)
	ly = np.linspace(0,5,y,endpoint=False)
	X,Y = np.meshgrid(lx,ly)
	
	df = data(10, 0.5, -7, (x,y), (int(x/2),int(y/2)))
	
	#  I already tested and it works
	
	auto0 = Automaton(c_intercept = 0.5, c_moisture = -7, shape = (x,y), firestart = (int(x/2),int(y/2)), moisture = df.at[0, 'moisture'])
	auto1 = Automaton(c_intercept = 0.5, c_moisture = -7, shape = (x,y), firestart = (int(x/2),int(y/2)), moisture = df.at[1, 'moisture'])
	auto2 = Automaton(c_intercept = 0.5, c_moisture = -7, shape = (x,y), firestart = (int(x/2),int(y/2)), moisture = df.at[2, 'moisture'])
	auto3 = Automaton(c_intercept = 0.5, c_moisture = -7, shape = (x,y), firestart = (int(x/2),int(y/2)), moisture = df.at[3, 'moisture'])
	
	
	print(df.at[0,'value'])
	print(auto0.run())

# fig, ax = plt.subplots()
# im = ax.imshow(auto0.state_matrix(), cmap = cmap, norm = norm)
# def update(x):
# 	im.set_array(auto0.state_matrix())
# 	auto0.time_step()
# ani = FuncAnimation(fig, update, interval = 100)
	