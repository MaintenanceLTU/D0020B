import LIS33HH
from time import sleep

LIS33HH.power("normal")
LIS33HH.rang("12g")
LIS33HH.BDU("block")

      

def get_acc():
    return LIS33HH.get_res("all")

try:
    while True:
        print(get_acc())
        sleep(1)
       
except KeyboardInterrupt:

    pls.close()
    
    print("Goodbye")   



