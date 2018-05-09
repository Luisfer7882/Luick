import smbus
import time

class Lidar_Lite():
  def __init__(self):
    self.address = 0x62
    self.distWriteReg = 0x00
    self.distWriteVal = 0x04
    self.distReadReg1 = 0x01
    self.distReadReg2 = 0x10
    self.velWriteReg = 0x04
    self.velWriteVal = 0x08
    self.velReadReg = 0x09
    self.reg = {
        "ACQ_COMMAND":      0x00, # Device command
        "STATUS":           0x01, # System status
        "SIG_COUNT_VAL":    0x02, # Maximum acquisition count
        "ACQ_CONFIG_REG":   0x04, # Acquisition mode control
        "VELOCITY":         0x09, # Velocity measurement output
        "PEAK_CORR":        0x0c, # Peak value in correlation record
        "NOISE_PEAK":       0x0d, # Correlation record noise floor
        "SIGNAL_STRENGTH":  0x0e, # Received signal strength
        "FULL_DELAY_HIGH":  0x0f, # Distance measurement high byte
        "FULL_DELAY_LOW":   0x10, # Distance measurement low byte
        "OUTER_LOOP_COUNT": 0x11, # Burst measurement count control
        "REF_COUNT_VAL":    0x12, # Reference acquisition count
        "LAST_DELAY_HIGH":  0x14, # Previous distance measurement high byte
        "LAST_DELAY_LOW":   0x15, # Previous distance measurement low byte
        "UNIT_ID_HIGH":     0x16, # Serial number high byte
        "UNIT_ID_LOW":      0x17, # Serial number low byte
        "I2C_ID_HIGH":      0x18, # Write serial number high byte for I2C address unlock
        "I2C_ID_LOW":       0x19, # Write serial number low byte for I2C address unlock
        "I2C_SEC_ADDR":     0x1a, # Write new I2C address after unlock
        "THRESHOLD_BYPASS": 0x1c, # Peak detection threshold bypass
        "I2C_CONFIG":       0x1e, # Default address response control
        "COMMAND":          0x40, # State command
        "MEASURE_DELAY":    0x45, # Delay between automatic measurements
        "PEAK_BCK":         0x4c, # Second largest peak value in correlation record
        "CORR_DATA":        0x52, # Correlation record data low byte
        "CORR_DATA_SIGN":   0x53, # Correlation record data high byte
        "ACQ_SETTINGS":     0x5d, # Correlation record memory bank select
        "POWER_CONTROL":    0x65, # Power state control
        "FULL_DELAY":       0x0f,
        "LAST_DELAY":       0x14,
        "UNIT_ID":          0x16,
        "I2C_ID":           0x18,
    }

  def connect(self, bus):
    try:
      self.bus = smbus.SMBus(bus)
      time.sleep(0.5)
      return 0
    except:
      return -1

  def writeAndWait(self, register, value):
    self.bus.write_byte_data(self.address, register, value);
    time.sleep(1)

  def readAndWait(self, register):
    res = self.bus.read_byte_data(self.address, register)
    time.sleep(1)
    return res

  def read_reg(self, reg):
    """Reads a specified register from the LiDAR

    Args:
        reg (string): the name of the register (contained in self.reg)
    Returns:
        byte: the value of the register (8 bits)
    """
    return self.bus.read_byte_data(self.address, self.reg[reg])

  def read_reg2(self, reg):
        """Reads 2 registers from the LiDAR

        Args:
            reg (string): the name of the first register (contained in self.reg)

        Returns:
            byte: the value of both registers (16 bits)
        """
        high_byte = self.bus.read_byte_data(self.address, self.reg[reg])
        low_byte = self.bus.read_byte_data(self.address, self.reg[reg] + 1)
        return (high_byte << 8) + low_byte

  def write_reg(self, reg, val):
        """Writes a specified value into a specified register

        Args:
            reg (string): the name of the register (contained in self.reg)
            val (byte): the value to write to the register (8 bits)
        """
        self.bus.write_byte_data(self.address, self.reg[reg], val)

  def wait_until_not_busy(self):
    """Waits until the LiDAR-Lite is ready for a new command
    """
    status = 1
    while status != 0:
        status = self.read_reg("STATUS") & 0b1

  def getDistance(self):
    self.write_reg("ACQ_COMMAND", 0x04)    
    self.wait_until_not_busy()
    return self.read_reg2("FULL_DELAY")

  def getVelocity(self):
    self.writeAndWait(self.distWriteReg, self.distWriteVal)
    self.writeAndWait(self.velWriteReg, self.velWriteVal)
    vel = self.readAndWait(self.velReadReg)
    return self.signedInt(vel)

  def signedInt(self, value):
    if value > 127:
      return (256-value) * (-1)
    else:
      return value


