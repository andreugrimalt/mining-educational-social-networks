# This script remove the duplicates from the activities array

from bson import *
from pymongo import *
import time
from datetime import timedelta

# Connect to mongo query router
clir = MongoClient("localhost:27026")
ir = clir.research

# Find all the actors
Actors=ir.Actors.find()

# iterate through actors
for actor in Actors:
	# for each actor make an empty array
	tempActivities=[]
	# for each actor activity
	for activity in actor["activities"]:	
		# put the activity in the tempActivities if it's not there
		if activity not in tempActivities:
			tempActivities.append(activity['ts'])
		# if it is there, then remove from the database
		elif activity in tempActivities:
			#print activity
			# remove from the database
			ir.Actors.update({'_id':actor["_id"]},{'$pull':{'activities':activity}})
	print "checked ",len(actor["activities"]), "activities"