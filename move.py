import time
from dronekit import connect, VehicleMode, LocationGlobalRelative, Command, LocationGlobal
from pymavlink import mavutil
import Tkinter as tk

class move():

  def set_velocity_body(vehicle, vx, vy, vz):
    msg = vehicle.message_factory.set_position_target_local_ned_encode(
            0,
            0, 0,
            mavutil.mavlink.MAV_FRAME_BODY_NED,
            0b0000111111000111, #-- BITMASK -> Consider only the velocities
            0, 0, 0,        #-- POSITION
            vx, vy, vz,     #-- VELOCITY
            0, 0, 0,        #-- ACCELERATIONS
            0, 0)
    vehicle.send_mavlink(msg)
    vehicle.flush()
#In this part we are making sure the drone is ready to arm before proceeding to the next instructions
  def arm_and_takeoff(TargetAltitude):

	print ("Executin Takeoff")
	while not drone.is_armable: 
		print ("Vehicle is not armable, waiting...")
		time.sleep(1)
        print("Ready to arm")
	drone.mode = VehicleMode("GUIDED")	
	drone.armed = True
#It assures the drone is armed before proceeding to next instructions
	while not drone.armed: 
		print ("Waiting for arming...")
        time.sleep(1)
        print("Ready for takeoff, taking off...")
	drone.simple_takeoff(TargetAltitude)
#The altitude sensor is not 100% precise, so this makes that the drone reaches ALMOST the altitude we want it to reach.
	while True:
		Altitude = drone.location.global_relative_frame.alt
		print("Altitude: ", Altitude)
		time.sleep(1)
		if Altitude >=TargetAltitude * 0.95:
			print ("Altitude reached")
        break
  def key(event):
    if event.char == event.keysym:
        if event.keysym == 'r': #this enable the letter "r" to open the Tk thing to move the drone with the keys
            drone.mode = VehicleMode("RTL")          
	else: 
        	if event.keysym == 'Up':
           		set_velocity_body(drone,5,0,0)
        	elif event.keysym == 'Down':
           		set_velocity_body(drone,-5,0,0)
        	elif event.keysym == 'Left':
           		set_velocity_body(drone,0,-5,0)
        	elif event.keysym == 'Right':
			set_velocity_body(drone,0,5,0)
