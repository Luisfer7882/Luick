from lidar_lite import Lidar_Lite
lidar = Lidar_Lite()
import time
connected = lidar.connect(1)

if connected < -1:
    print ("Not Connected")
else:
    print ("Connected")

while True:
    distance = lidar.getDistance()
    print("Distance to target = %s" % (distance))
    if int(distance) <= 80:
        print("Too Close!!! Back Off!!!")
    time.sleep(0.5)

