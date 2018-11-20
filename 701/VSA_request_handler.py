#!/usr/bin/python
import sys, time, math
import paho.mqtt.client as mqtt
import pygame
import array
import json

pygame.init()

display_width = 1024
display_height = 682

white = (255,255,255)
green = (0,255,0)
red = (255,0,0)
yellow=(255,255,0)
gray=(150,150,150)
carlist=[(0,0),(0,0),(0,0),(0,0),(0,0)]
vehList=[(0,0),(0,0),(0,0),(0,0),(0,0)]

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Vehicle Simulation')
clock=pygame.time.Clock()
mapImg=pygame.image.load('map.jpg')
gameDisplay.blit(mapImg,(0,0))

def background():
        gameDisplay.blit(mapImg,(0,0))

def car(carx,cary):
        pygame.draw.circle(gameDisplay, green,(carx,cary),10)


def speed_detect(x1,y1,x2,y2):
        v=math.sqrt((x2-x1)*(x2-x1)+(y2-y1)*(y2-y1))
        return v

def text_objects(text, font):
        textSurface=font.render(text, True, white)
        return textSurface, textSurface.get_rect()

def time_display(text):
        largeText=pygame.font.Font('freesansbold.ttf',50)
        TextSurf, TextRect=text_objects(text,largeText)
        TextRect.center=(100,100)
        gameDisplay.blit(TextSurf, TextRect)

def speed_display(text):
        largeText=pygame.font.Font('freesansbold.ttf',50)
        TextSurf, TextRect=text_objects(text,largeText)
        TextRect.center=(100,140)
        gameDisplay.blit(TextSurf, TextRect)


def display(x,y,x0,y0):
 
        car(x,y)
        timeOri=0
        time1=timeOri
        time=pygame.time.get_ticks()
        time1=int(time)
        t1=str(time1/1000)
        if time1>timeOri:
                speed1=speed_detect(x,y,x0,y0)
                               
        #time_display(t1)
        print("Speed:"+str(speed1))
        v1=str(speed1)
        speed_display(v1)
        #if car1_startx > display_width:
        #        car1_startx=0
        #        car1_starty=650
        pygame.display.update()
        clock.tick()
        

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker: "+str(broker_address))
        global Connected
        Connected = True                #Signal connection 
    else:
         print("Connection failed")

def on_message_sims(mqttc, obj, msg):
    payload = str(msg.payload.decode("utf-8"))
    timestamp, vehUUID, vehLat, vehLon, vehVel, vehPosErr= payload.split(',')

    global vehUUIDList
    global msgList
    global vehList

    if vehList==[]:
            vehList=msgList
    
    a=int(vehUUID)
    b=int(vehLat)
    c=int(vehLon)
    #vehList[a]=b
    #vehList.insert(a,(b,c))
    
  
    idx = -1
    try:
        # replace message payload if vehUUID is already in the list
        idx = vehUUIDList.index(vehUUID)
        msgList[idx]=(b,c)
        display(b,c,vehList[idx][0],vehList[idx][1])
        vehList=msgList
        print(idx,msgList[idx])
        
        
    except ValueError:
        # add vehicle UUID and message to the list
        vehUUIDList.append(vehUUID)
        msgList.append(msg.payload)

        

def on_message_reqs(mqttc, obj, msg):
    # This callback will only be called for messages with topics that match
    # VSA/request/nearbyVeh/reqs/#
    # return result to 
    # VSA/request/nearbyVeh/return/#
    #print("Request: " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    try:
        vehID,reqRad,reqVeh,reqTime = msg.payload.split(',')
        returnTopic = "VSA/request/nearbyVeh/return/"+str(vehID)
    
        #print json.dumps(msgList)
        print(returnTopic)
        client.publish(returnTopic, json.dumps(msgList))
        #client.publish(returnTopic, "testing")
    except ValueError:
        print("request error: ensure it's in the format of vehID,reqRad,reqVeh,reqTime")

    # Find vehicles within xx radius of the user request and timestamp no more than 5 seconds
    # to be done

def on_message(mqttc, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))


timeStampList = []
vehUUIDList = []
vehLatList = []
vehLonList = []
vehVelList = []
vehPosErrList = []
vehUUID= []
vehList = []
msgList = []

Connected = False   #global variable for the state of the connection

broker_address="203.101.224.102"
broker_port = "1883" 
user = "yourUser"                    #Connection username
password = "yourPassword"            #Connection password
 
print("creating new instance")
client = mqtt.Client()               #create new instance
#client.username_pw_set(user, password=password)    #set username and password
client.on_connect= on_connect                      #attach function to callback
client.message_callback_add("VSA/vehSim/#", on_message_sims)
client.message_callback_add("VSA/request/nearbyVeh/reqs/#", on_message_reqs)

client.on_message= on_message                      #attach function to callback

print("connecting to broker")
client.connect(broker_address, int(broker_port))          #connect to broker
client.subscribe("VSA/vehSim/#")

client.loop_start()        #start the loop

while Connected != True:    #Wait for connection
    time.sleep(0.1)
    
 
print("Subscribing to every topic under ","VSA/#")

try:
    while True:
 
        time.sleep(1)
        

        
 
except KeyboardInterrupt: 		# catches the ctrl-c command, which breaks the loop above
    print("Vehicle Simulation Stopped")
    client.disconnect()
    client.loop_stop() #stop the loop

