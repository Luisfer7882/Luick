from Servo1 import servo
from lidar_lite import Lidar_Lite

lidar=Lidar_Lite()
connected = lidar.connect(1)
print "connected"

if connected <= -1:
    print "Not Connected"
else:
  while True:
    print lidar.getDistance()
    print lidar.getVelocity()

    myservo=servo()
    myservo.scan()

