# Count the uploads and activities for each user

from bson import *
from pymongo import *
import time
from datetime import timedelta

# Connect to the research database
clir = MongoClient("localhost:27026")
ir = clir.research

# Find the actors that have activities and uploads
actors=ir.Actors.find({"$and":[{"activities.at":{"$eq":0}},{"activities.at":{"$eq":6}}]},timeout=False)
# Just to keep track of the progress (script takes a few seconds to execute)
totalActors=actors.count()
n=0
# For each actor, count the activities and uploads
for actor in actors:
	print totalActors-n," left"
	n=n+1
	uploadsAndActivities6=0
	for activity in actor['activities']:
		if activity['at']==0 or activity['at']==6:
			uploadsAndActivities6=uploadsAndActivities6+1
	# Add a field to the actor withe the total numper of activities and uploads
	ir.Actors.update({'_id':actor['_id']},{'$push':{'uploadsAndLogActivities':uploadsAndActivities6}})



