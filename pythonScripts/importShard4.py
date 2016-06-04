from bson import *
from pymongo import *
import time
from datetime import timedelta
from pylab import *


import json
from pymongo.errors import InvalidOperation

#source db 
#mongod --dbpath /Users/chris/expts/praise/dataAnalysis/mongo/db --fork --syslog
#mongod --dbpath /Users/matthew/Documents/PRAISE_local/data/musiccircle_latest/musiccircle
cli = MongoClient("localhost:27017")
db = cli.musiccircle

#target instance - intermediate representation
#mongod --port 27018 -dbpath /Users/chris/expts/praise/dataAnalysis/mongo/mus0IR --fork --syslog 
# mongod --port 27018 --dbpath /Users/matthew/Documents/PRAISE_local/data/musiccircle_latest/processedclir = MongoClient("localhost:27018")
clir = MongoClient("localhost:27026")
ir = clir.research

# generate a list of dates
def dateListGenerator(start, end, delta):
    result=[]
    curr = start
    while curr < end:
        curr += delta
        result.append(curr)
        
    return result
datesList=dateListGenerator(datetime.datetime(2014, 7, 30, 00, 00, 00, 00),datetime.datetime(2014, 7, 31, 00, 00, 00, 00),timedelta(days=1))        
datesListLength=len(datesList)
prog=0

for date in datesList:
    prog=prog+1
    foundLogs=db.log.find({"$and":[
                    {"datetime":{"$gte":date}},
                    {"datetime":{"$lt":(date+timedelta(days=1))}}
                    ]
                  }
                 )
    print datesListLength-prog," left"
    
    for logChunk in foundLogs: 
        bulk = ir.Actors.initialize_ordered_bulk_op()
        activities=[]
        userFound=bulk.find({'_id':logChunk['uid']})
        for logEvent in json.loads(logChunk["text"]):
            if ObjectId.is_valid(logChunk["uid"]):
                if "id" in logEvent and "logtype" in logEvent:
                    tempActivity={'at':6, '_id':logEvent['id'], 'ts':datetime.datetime.fromtimestamp(logEvent['time']/1000.0), 'type':logEvent['type'], 'logtype':logEvent['logtype']}
                    if(tempActivity not in activities):                        
                        activities.append(tempActivity)
                        userFound.update({'$push':{'activities':tempActivity}})
        if(len(activities)>0):
            try:
                bulk.execute()
            except InvalidOperation as invOpt:
                pass