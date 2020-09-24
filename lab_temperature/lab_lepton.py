# -*- coding: utf-8 -*-
"""
Created on Wed Oct 10 19:43:05 2018
@author: Johan Odelius, Luleå University of Technology
"""

import numpy as np
#from pylepton import Lepton
from Lepton3 import Lepton3
import matplotlib.pyplot as plt

ambient_temperature = 20.3 #
    
# Pixel size
Image_Pixels = [120,160]
    
##To take a picture
with Lepton3("/dev/spidev0.1") as l:
    thermal_image,_ = l.capture()
    
n = thermal_image.shape[0]-np.prod(Image_Pixels)
#thermal_image_matrix = np.random.randint(0, high=8191, size=(60,80)) 
thermal_image_matrix = np.reshape(thermal_image[n:],Image_Pixels)

temperature_matrix = (0.026*(thermal_image_matrix - [8192])) + ambient_temperature

plt.imshow(temperature_matrix)
#plt.imsave('name.png', thermal_image_matrix)
plt.show()