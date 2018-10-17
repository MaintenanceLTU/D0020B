"""
Created on Wed Oct 10 20:12:15 2018

@author: Johan Odelius, Luleå University of Technology
"""

import time
import smbus
import requests


Number_of_Measurements = 20

DEVICE_LABEL = "rpi-melexis"  # Put your device label here 
VARIABLE_OBJ_TEMP = "temberature_object"  # Put your first variable label here
VARIABLE_AMB_TEMP = "temberature_ambient"  # Put your second variable label here
TOKEN = ""  # Put your TOKEN here

url = "http://things.ubidots.com"
url = "{}/api/v1.6/devices/{}".format(url, DEVICE_LABEL)
headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}


class MLX90614():
                 
            MLX90614_RAWIR1=0x04
            MLX90614_RAWIR2=0x05
            MLX90614_TA=0x06
            MLX90614_TOBJ1=0x07
            MLX90614_TOBJ2=0x08
                 
            MLX90614_TOMAX=0x20
            MLX90614_TOMIN=0x21
            MLX90614_PWMCTRL=0x22
            MLX90614_TARANGE=0x23
            MLX90614_EMISS=0x24
            MLX90614_CONFIG=0x25
            MLX90614_ADDR=0x0E
            MLX90614_ID1=0x3C
            MLX90614_ID2=0x3D
            MLX90614_ID3=0x3E
            MLX90614_ID4=0x3F
                 
            def __init__(self, address=0x5a, bus_num=1):
                    self.bus_num = bus_num
                    self.address = address
                    self.bus = smbus.SMBus(bus=bus_num)
                         
            def read_reg(self, reg_addr):
                    return self.bus.read_word_data(self.address, reg_addr)
                         
            def data_to_temp(self, data):
                    temp = (data*0.02) - 273.15
                    return temp
                         
            def get_amb_temp(self):
                    data = self.read_reg(self.MLX90614_TA)
                    return self.data_to_temp(data)
                         
            def get_obj_temp(self):
                    data = self.read_reg(self.MLX90614_TOBJ1)
                    return self.data_to_temp(data)

def posixtime(t=time.time()):
    return int(t*1e3)
    
sensor = MLX90614()   
for measurement in range(Number_of_Measurements):
    #For the melexis sensor          
        if __name__ == "__main__":
            
            TEMPOBJ = sensor.get_obj_temp()
            TEMPAMB = sensor.get_amb_temp ()
            TIME = time.time()

            print("Ambient temperature %.1f°C" % TEMPAMB)
            print("Object temperature %.1f°C" % TEMPOBJ)
            print("The current local date time is ",time.ctime(TIME))                
            
            
            #package to post
            tposix = posixtime(TIME)
            pkg = {
                    VARIABLE_OBJ_TEMP: {'value': TEMPOBJ,'timestamp':tposix},
                    VARIABLE_AMB_TEMP: {'value': TEMPAMB,'timestamp':tposix}
            }
            req = requests.post(url=url, headers=headers, json=pkg)
            time.sleep(1)
