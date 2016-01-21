import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import math

#convention: 2 particules a 2 dim, matrice
# |x1 x2|
# |y1 y2|


#definition de fonctions dfsdfsdfsdf

def E(x):
	if x < 0 :
		return np.exp(0.4/x)
	else:
		return 0

def Evect(x):
	return np.piecewise(x,[x<0,x>=0], [lambda x: np.exp(0.4/x),0]) 

#derivee de E
def dE(x):
	if x < 0 : 
		return -0.4/x**2*np.exp(0.4/x)
	else:
		return 0

def dEvect(x):
	return np.piecewise(x,[x<0,x>=0],[lambda x: -0.4/x**2*E(x),0])

#la fonction E(a-x)E(x-b) donne un "blip" sur [a;b]
def blip(a,b,x):
	return E(a-x)*E(x-b)

#derivee du blip
def dblip(a,b,x):
	return -dE(a-x)*E(x-b)+E(a-x)*dE(x-b)

#blip normalise, son max vaut 1
def blipn(a,b,x):
	return blip(a,b,x)*np.exp(1.6/(b-a))	

def dblipn(a,b,x):
	return dblip(a,b,x)*np.exp(1.6/(b-a))

#definition du potentiel, deux puits dont le recouvrement est defini par delta
def V(x,y,delta):
	return -(blipn(0,0.5+delta,x)*blipn(0,0.5+delta,y)+0.5*blipn(0.5-delta,1,x)*blipn(0.5-delta,1,y))

def gradV(x,y,delta):
	return -np.asarray([dblipn(0,0.5+delta,x)*blipn(0,0.5+delta,y)+0.5*dblipn(0.5-delta,1,x)*blipn(0.5-delta,1,y), \
		dblipn(0,0.5+delta,y)*blipn(0,0.5+delta,x)+0.5*dblipn(0.5-delta,1,y)*blipn(0.5-delta,1,x)])

def gen_part(beta,deltat,start,stop, delta=0.15):
	sigma=np.sqrt(2./beta)
	x0=np.asarray([np.random.uniform(),np.random.uniform()])
	path_x =[x0[0]]
	path_y =[x0[1]]
	x_t=x0
	for t in np.arange(start,stop,deltat):
		x_temp = x_t  - delta*gradV(x_t[0],x_t[1], delta) + sigma*np.sqrt(deltat)*np.random.normal(0,1,(2)) 
		x_temp = x_temp % 1 
		ratio = np.exp(-beta*(V(x_temp[0],x_temp[1],delta)-V(x_t[0],x_t[1],delta)))
		ptrans = min(1,ratio)
		temp = np.random.uniform()
		if temp<ptrans:
			x_t=x_temp
		path_x.append(x_t[0])
		path_y.append(x_t[1])
		print x_t[0],x_t[1]
	return path_x,path_y



# ax.plot_surface(x,y,z)

# ax.set_xlabel('x')
# ax.set_ylabel('y')
# ax.set_zlabel('z')

# plt.figure(2)
# plt.contour(x,y,z)
# plt.show()


delta = 0.15

beta = 10
deltat= 0.01
start = 0.
stop = 10.

path_x,path_y = gen_part(beta,deltat,start,stop)

fig = plt.figure(3)
plt.scatter(np.asarray(path_x),np.asarray(path_y))

fig = plt.figure(4)
plt.hist(path_x)

fig = plt.figure(5)
plt.plot(path_x)

plt.show()

print V(0.25,0.25,delta)