from smbus2  import SMBus as i2c

class reg_bit:
        def __init__(self, offset):

            if offset > 7 or offset < 0:
                raise ValueError("Bit offset must be between 0-7")

            self.offset = offset
            self.HIGH = (True<<self.offset)
            self.LOW = ~self.HIGH
        

class reg_mode:
        def __init__(self, setting):
                self.setting = setting

class register:
        def __init__(self, dev, bus, adress, rw):
                self.DEVICE = dev
                self.BUS = bus
                self.RW = rw
                self.ADRESS = adress
                self.modes = dict()
                self.bits = dict()
        

        def add_reg_bits(self, **kvargs):

                for name in kvargs:
                        if not(isinstance(kvargs[name], int)): raise Exception("Bit offset must be integer")
                        
                        self.bits[name] = reg_bit(kvargs[name])
                                    

        def add_mode(self, modeFam, modeName, **kvargs):

                if len(kvargs) == 0: raise Exception("No bits where assigned a state")

                if modeFam not in self.modes:
                        self.modes[modeFam] = dict()

                self.modes[modeFam][modeName] = reg_mode(kvargs)
      
           
        def set_mode(self, modeFam, mode):

                
                if mode not in self.modes[modeFam]: raise Exception("Unknown mode")
                if self.RW == "r": raise Exception("Register is read-only")
                
                with i2c(self.BUS) as bus:
                        reg_val = self.read()
                         
                        for modeBit in self.modes[modeFam][mode].setting:

                                if self.modes[modeFam][mode].setting[modeBit]:
                                        reg_val |= self.bits[modeBit].HIGH
                                        
                                elif not(self.modes[modeFam][mode].setting[modeBit]):
                                        reg_val &= self.bits[modeBit].LOW

                                else:
                                        raise Exception("Unexpected value")
                                
                        bus.write_byte_data(self.DEVICE, self.ADRESS, reg_val)
                        

        def read(self):
                with i2c(self.BUS) as bus:
                        reg = bus.read_byte_data(self.DEVICE, self.ADRESS)
                return reg
                
