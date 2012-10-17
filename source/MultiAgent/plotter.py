import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as so

def func(x, a, b, c):
     return a * np.exp( -b * x ) + c

ydata = np.load( 'result.npy' )
xdata = np.array( range( len( ydata ) ) )

popt, pcov = so.curve_fit( func, xdata, ydata )

plt.plot( xdata, ydata )
plt.plot( xdata, func( xdata, popt[0], popt[1], popt[2] ) )
plt.show()

'''
x = np.linspace( 0, 4, 50 )
y = func( x, 2.5, 1.3, 0.5 )
yn = y + 0.2*np.random.normal( size = len(x) )
popt, pcov = so.curve_fit( func, x, yn )

plt.plot(x,y)
plt.plot(x,yn)
plt.plot(x,func( x, popt[0], popt[1], popt[2] ) )
plt.show()
'''