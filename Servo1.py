import RPi.GPIO as GPIO    #Importamos la libreria RPi.GPIO
import time                #Importamos time para poder usar time.sleep

class servo():

    def __init__(self):

        GPIO.setmode(GPIO.BOARD)   #Ponemos la Raspberry en modo BOARD
        GPIO.setup(21,GPIO.OUT)    #Ponemos el pin 21 como salida
	self.p = GPIO.PWM(21,50)        #Ponemos el pin 21 en modo PWM y enviamos 50 pulsos por segundo
	self.p.start(7.5)               

    def scan(self):
	k=0.4335
	j=2.5

	while True: 
	    try:                 
	        while  j<=11.17:
		    j=j+k
	            self.p.ChangeDutyCycle(j)    
        	    time.sleep(0.5)           
		    print j
     	            j=2.5
