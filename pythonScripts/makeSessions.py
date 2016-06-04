# Extract the sessions for each users and put them into an array in the Actors collection

from bson import *
from pymongo import *
import time
from datetime import timedelta

# Music Circle database
cli = MongoClient("localhost:27017")
db = cli.musiccircle
# Research database
clir = MongoClient("localhost:27026")
ir = clir.research

# Find all users with uploads and activities
actors=ir.Actors.find({"$and":[{"activities.at":{"$eq":0}},{"activities.at":{"$eq":6}}]},timeout=False)
# To keep track of the progress (script takes a while to execute)
totalActors=actors.count()
n=0
# For each actor find all the sessions that correspond to the actor
for actor in actors:
	print totalActors-n," left"
	sessions=db.Session.find({'user_id':actor['_id']})
	# For all the sessions found, put them into the right actor in the Actors collection inside a new field called sessions
	for session in sessions:
		ir.Actors.update({'_id':actor['_id']},{'$push':{'sessions':session}})



