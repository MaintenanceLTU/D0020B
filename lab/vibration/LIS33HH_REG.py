import registerframework as rf

DEVADRESS = 0x19
BUS = 1

CTRL_REG1 = rf.register(DEVADRESS, BUS, 0x20, "rw")
CTRL_REG1.add_reg_bits(PM2 = 7, PM1 = 6, PM0 = 5, DR1 = 4, DR0 = 3, Z_enable = 2, Y_enable = 1, X_enable = 0,)
CTRL_REG1.add_mode("power", "off", PM2 =0, PM1 = 0, PM0 = 0)
CTRL_REG1.add_mode("power", "normal", PM2 = 0, PM1 = 0, PM0 = 1)
CTRL_REG1.add_mode("power", "low1", PM2 = 0, PM1 = 1, PM0 = 0)
CTRL_REG1.add_mode("power", "low2", PM2 = 0, PM1 = 1, PM0 = 1)
CTRL_REG1.add_mode("power", "low3", PM2 = 1, PM1 = 0, PM0 = 0)
CTRL_REG1.add_mode("power", "low4", PM2 = 1, PM1 = 0, PM0 = 1)
CTRL_REG1.add_mode("power", "low5", PM2 = 1, PM1 = 1, PM0 = 0)

CTRL_REG2 = rf.register(DEVADRESS, BUS, 0x21, "rw")
CTRL_REG2.add_reg_bits(BOOT = 7, HPM1 = 6, HPM0 = 5, FDS = 4, HPen2 = 3, HPen1 = 2, HPCF1 = 1, HPCF = 0)
CTRL_REG2.add_mode("BOOT", "BOOT", BOOT = 1)
CTRL_REG2.add_mode("filter", "HP1", HPM1 = 0, HPM0 = 0)
CTRL_REG2.add_mode("filter", "HP2", HPM1 = 0, HPM0 = 1)
CTRL_REG2.add_mode("filter", "HP3", HPM1 = 1, HPM0 = 0)

CTRL_REG3 = rf.register(DEVADRESS, BUS, 0x22, "rw")
CTRL_REG3.add_reg_bits(IHL = 7, PP_OD = 6, LIR2 = 5, I2_CFG1 = 4, I2_CFG0 = 3, LIR1 = 2, I1_CFG1 = 1, I1_CFG0 = 0)

CTRL_REG4 = rf.register(DEVADRESS, BUS, 0x23, "rw")
CTRL_REG4.add_reg_bits(BDU = 7, BLE = 6, FS1 = 5, FS0 = 4, STs = 3, ST = 1, SIM = 0)
CTRL_REG4.add_mode("sens", "6g", FS1 = 0, FS0 = 0)
CTRL_REG4.add_mode("sens", "12g", FS1 = 0, FS0 = 1)
CTRL_REG4.add_mode("sens", "24g", FS1 = 1, FS0 = 1)
CTRL_REG4.add_mode("BDU", "block", BDU = 1)
CTRL_REG4.add_mode("BDU", "cont", BDU = 0)

CTRL_REG5 = rf.register(DEVADRESS, BUS, 0x24, "rw")
CTRL_REG5.add_reg_bits(TurnOn1 = 1, TurnOn0 = 0)
CTRL_REG5.add_mode("StW", "enable", TurnOn1 = 0, TurnOn0 = 0)
CTRL_REG5.add_mode("StW", "disable", TurnOn1 = 1, TurnOn0 = 1)

HP_FILTER_RESET = rf.register(DEVADRESS, BUS, 0x25, "r")

REFERENCE = rf.register(DEVADRESS, BUS, 0x26, "rw")

STATUS_REG = rf.register(DEVADRESS, BUS, 0x27, "rw")
STATUS_REG.add_reg_bits(ZYXOR = 7, ZOR = 6, YOR = 5, XOR = 4, ZYXDA = 3, ZDA = 2, YDA = 1, XDA = 0)

OUT_X_L = rf.register(DEVADRESS, BUS, 0x28, "r")
OUT_X_H = rf.register(DEVADRESS, BUS, 0x29, "r")
OUT_Y_L = rf.register(DEVADRESS, BUS, 0x2A, "r")
OUT_Y_H = rf.register(DEVADRESS, BUS, 0x2B, "r")
OUT_Z_L = rf.register(DEVADRESS, BUS, 0x2C, "r")
OUT_Z_H = rf.register(DEVADRESS, BUS, 0x2D, "r")

INT1_CFG = rf.register(DEVADRESS, BUS, 0x30, "rw")
INT1_CFG.add_reg_bits(AOI = 7, SIXD = 6, ZHIE = 5, ZLIE = 4, YHIE = 3, YLIE = 2, XHIE = 1, XLIE = 0)
INT1_CFG.add_mode("intSrcCfg", "OR", AOI = 0, SIXD = 0)
INT1_CFG.add_mode("intSrcCfg","6mov", AOI = 0, SIXD = 1)
INT1_CFG.add_mode("intSrcCfg","AND", AOI = 1, SIXD = 0)
INT1_CFG.add_mode("intSrcCfg","6pos", AOI = 1, SIXD = 1)

INT1_SRC = rf.register(DEVADRESS, BUS, 0x31, "r")
INT1_SRC.add_reg_bits(IA = 6, ZH = 5, ZL = 4, YH = 3, YL = 2, XH = 1, XL = 0)

INT1_THS = rf.register(DEVADRESS, BUS, 0x32, "rw")
INT1_DURATION = rf.register(DEVADRESS, BUS, 0x33, "rw")

INT2_CFG = rf.register(DEVADRESS, BUS, 0x34, "rw")
INT2_CFG.add_reg_bits(AOI = 7, SIXD = 6, ZHIE = 5, ZLIE = 4, YHIE = 3, YLIE = 2, XHIE = 1, XLIE = 0)
INT2_CFG.add_mode("intSrcCfg","OR", AOI = 0, SIXD = 0)
INT2_CFG.add_mode("intSrcCfg","6mov", AOI = 0, SIXD = 1)
INT2_CFG.add_mode("int1SrcCfg","AND", AOI = 1, SIXD = 0)
INT2_CFG.add_mode("int1SrcCfg","6pos", AOI = 1, SIXD = 1)

INT2_SRC = rf.register(DEVADRESS, BUS, 0x31, "r")
INT2_SRC.add_reg_bits(IA = 6, ZH = 5, ZL = 4, YH = 3, YL = 2, XH = 1, XL = 0)

INT2_THS = rf.register(DEVADRESS, BUS, 0x32, "rw")
INT2_DURATION = rf.register(DEVADRESS, BUS, 0x33, "rw")

