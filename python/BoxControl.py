#!/usr/bin/env python

#-------------------------------------
#Qendy Qeeper Team.
#Part of 2017 HaQathon at Qwilt.
#Written by YaelY, GaliC SagiR, RoyR
#----------------------------------

import time
import RPi.GPIO as GPIO
import sys
from  pygame import mixer
from os import listdir
from random import randrange
from datetime import date
import datetime
import json
import os

class DataMap(object):
    
    def __init__(self):
        
        self.usersDataDict = {}
        self.usersDataDict["lastUpdate"] = None
        self.usersDataDict["admin"] = "admin"
        self.usersDataDict["userNames"] = {}
        
    def init(self):
        
        # Create files if does not exist
        file = open('/var/www/html/data.txt', 'a+')
        file.close()
        
        file = open('/var/www/html/timedata.txt', 'a+')
        file.close()
        
        if os.stat('/var/www/html/timedata.txt').st_size == 0:
            self.usersDataDict["lastUpdate"] = datetime.datetime.now()
            
            with open('/var/www/html/timedata.txt', 'w') as outfile:
                outfile.write(str(self.usersDataDict["lastUpdate"]))
                outfile.close()
        
        else:
            with open('/var/www/html/timedata.txt', 'r') as outfile:
                self.usersDataDict["lastUpdate"] = datetime.datetime.strptime(outfile.read(), '%Y-%m-%d %H:%M:%S.%f')
                outfile.close()
        
        if os.stat('/var/www/html/data.txt').st_size == 0:
            return
        
        with open('/var/www/html/data.txt', 'r') as outfile:
            self.usersDataDict["userNames"] = json.loads(outfile.read())
            outfile.close()
            
    def addData(self, userName, passWord, timesToOpen):
        #list include password, total allowed and current allowed
	print userName 
        self.usersDataDict["userNames"][userName] = [passWord, int(timesToOpen), int(timesToOpen)]
        print "before open data.txt" 
        with open('/var/www/html/data.txt', 'w') as outfile:
            print "In file open"
            json.dump(self.usersDataDict["userNames"], outfile)
	    print self.usersDataDict["userNames"]
        
    def isValidUser(self, userName, passWord):
        print self.usersDataDict["userNames"]
        if userName in self.usersDataDict["userNames"]:
            userDetails = self.usersDataDict["userNames"][userName]
            if userDetails[0] == passWord:
                print " true"
                return True
        return False
    
    def checkIfTimesLeftAndDecreseTime(self, userName):
        userList = self.usersDataDict["userNames"][userName]
        print userList[2]
        if userList[2] > 0:
            self.usersDataDict["userNames"][userName][2] = userList[2] - 1
            print self.usersDataDict["userNames"][userName][2]
         
            with open('/var/www/html/data.txt', 'w') as outfile:
                json.dump(self.usersDataDict["userNames"], outfile)
                outfile.close()
            return True
        return False
    
    def getLastUpdateTime(self):
        
        return self.usersDataDict["lastUpdate"]
        
    def updateTime(self):
        
        self.usersDataDict["lastUpdate"] = datetime.datetime.now()
            
        with open('/var/www/html/timedata.txt', 'w') as outfile:
            outfile.write(str(self.usersDataDict["lastUpdate"]))
            outfile.close()
        
        allUsers = self.usersDataDict["userNames"]
        for user in allUsers:
            allUsers[user][2] = allUsers[user][1]
        
        with open('/var/www/html/data.txt', 'w+') as outfile:
            json.dump(self.usersDataDict["userNames"], outfile)
            outfile.close()
            
    def getTimesLeft(self, userName):
        
        userData = self.usersDataDict["userNames"][userName]
        return userData[2]


class BoxControl(object):

	def __init__(self):
		self.datamap = DataMap()
		self.datamap.init()
		self.port1 = 36 #change GPIO to your desired ports.
		self.port2 = 40 

	def callOpenBox(self,user,password):
		self.update()
		print user
		print password
		if self.datamap.isValidUser(user,password):
			timesLeft = self.datamap.getTimesLeft(user)
			print "play sound"
			print timesLeft
			self.playSound(timesLeft)
			if self.datamap.checkIfTimesLeftAndDecreseTime(user):
				time.sleep(0.5)
				self.openBox()
				print "on"
                        while mixer.music.get_busy() == True:
                            continue

			

	def update(self):
		now = datetime.datetime.now()
		last = self.datamap.getLastUpdateTime()
		delta = now - last
		print "update %s days ago" %(delta.days)
		if delta.days >= 1:
			self.datamap.updateTime()

	def openBox(self):
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(self.port1,GPIO.OUT)
		GPIO.setup(self.port2,GPIO.OUT)
		GPIO.output(self.port1,1)
		GPIO.output(self.port2,1)
		time.sleep(5)	
		GPIO.output(self.port1,0)
		GPIO.output(self.port2,0)
		GPIO.cleanup()

	def addUser(self,adminPass,user,password,timesToOpen):
		if adminPass=="admin":
			print "add user admin"
			self.datamap.addData(user,password,timesToOpen)
	
	def playSound(self,timesLeft=2):
		#we used the ~/Music/open to put verious sounds and random between them every time you open the box with 2 or more allocationes left
        mixer.init()
		musicDir = "/home/pi/Music/open/"
		if timesLeft == 0:
			sound = "/home/pi/Music/no_more_candy.mp3"
		elif timesLeft == 1:
			sound = "/home/pi/Music/last_qandy.mp3"
		else:
			sound = musicDir + listdir(musicDir)[randrange(0,len(listdir(musicDir)))]
		print sound
		mixer.music.load(sound)
		mixer.music.play()


if __name__ == "__main__":
	print "!entered main loop"
	box = BoxControl()
	#box.openBox()
	#open user pass
	if len(sys.argv)==4: 
		box.callOpenBox(sys.argv[2],sys.argv[3])	
	 #add adminPass user pass timesToOpen
	if len(sys.argv)==6:
		print sys.argv[2]
		box.addUser(sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])	
				
	mixer.quit()

		  	
	