#import sys
#sys.path.insert(1, '/Users/caitlin/Documents/Math/PIC16B/pic16bproject')
#pde-simulation==0.0.1
from pde-simulation==0.0.1 import transport_equation as te
#from pde_simulation import wave_equation as we
#from pde_simulation import heat_equation as he
#from pde_simulation import burgers as be
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['animation.ffmpeg_path'] = '/Users/caitlin/opt/anaconda3/bin/ffmpeg'
import matplotlib.animation as animation
from matplotlib import colors
from matplotlib import rc
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
rc('text', usetex=True)
def f(x):
    return np.exp(-200*(x-0.25)**2)
def sine(x):
    return np.sin(2*x*np.pi)
def Gaussian_2d(x,y):
	return 0.8*np.exp(-700*((x-1)**2+(y-0)**2))+0.8*np.exp(-700*((x-0)**2+(y-1)**2))
te.solution(f,"animation")
#we.solution(sine,1,"3d")
#we.solution(Gaussian_2d,2)
#be.solution("shock")