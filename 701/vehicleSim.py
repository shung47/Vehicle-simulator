#!/usr/bin/python
import paho.mqtt.client as mqtt
import random
import uuid
import sys, time

broker_address="203.101.224.102"
broker_port = "1883" 
numVeh =  6

client = mqtt.Client("P1") #create new instance
client.connect(broker_address) #connect to broker

#along george street
#starting George/Alice: -27.474777, 153.027274
#finish George/Roma: 	-27.466914, 153.019646
vehUUID = []
vehX = []
vehY = []
vehVel = []
vehPosErr = []

for count in range(0,100):
    vehUUID=(1,2,3,4,5,6)
    #vehUUID.append(uuid.uuid4())
#   print vehUUID[count]

counter = 0;
try:
    while True:      
#       for simTime in xrange(0,10000):
        time_now = time.time()

        if counter == 0:
            for veh in range(0, numVeh):# number of vehicles            
                vehX.insert(veh, 200)
                vehY.insert(veh, 200)
                vehVel.insert(veh, 5)
                vehPosErr.insert(veh, 0)

                topic = "VSA/vehSim/"+str(vehUUID[veh])
                message = str(time_now) + ',' + str(vehUUID[veh]) + ',' + str(vehX[veh]) + ',' + str(vehY[veh]) + ',' + str(vehVel[veh])+ ',' + str(vehPosErr[veh])
                client.publish(topic,message) #publish
                print(message)
        

        #print(topic)
        #print(message)
        #print(counter)
        #counter = counter + 1
        time.sleep(1)
    
except KeyboardInterrupt: 		# catches the ctrl-c command, which breaks the loop above
    print("Vehicle Simulation Stopped")

