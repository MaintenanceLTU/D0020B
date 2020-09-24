import LIS33HH_REG as reg

bus = reg.BUS
dev = reg.DEVADRESS

def power(mode):
    reg.CTRL_REG1.set_mode("power", mode)


def rang(mode):
    reg.CTRL_REG4.set_mode("sens", mode)

        
def BDU(mode):
    reg.CTRL_REG4.set_mode("BDU", "block")

    
def get_res(self, form = "G", *axis):

    if len(axis) > 3: raise Exception("get_res axis arguments > 3")
    
    if isinstance(axis, str): axis = (axis, )
   
    res = {"X" : {"MSB" : reg.OUT_X_H.read(),
                  "LSB" : reg.OUT_X_L.read()
                  },
           
           "Y" : {"MSB" : reg.OUT_Y_H.read(),
                  "LSB" : reg.OUT_Y_L.read()
                  },
           
           "Z" : {"MSB" : reg.OUT_Z_H.read(),
                  "LSB" : reg.OUT_Z_L.read()
                  }
           }

    for axle in res:
        res[axle] = res[axle]["LSB"] | (res[axle]["MSB"]<<8)

        if res[axle] > 32767: res[axle] -= 65536
        
        res[axle] = ~res[axle]
                
        res[axle] = (2*float(12)*float(res[axle])/(2**16))

    return res          
