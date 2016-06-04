# All the code by Chris Kiffer

%pylab inline
from pymongo import *
from bson import *
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

class mediaFormats:
    VIDEO = 0
    AUDIO = 1

class Activities:
    UPLOADED = 0
    VIEWED = 1
    COMMENTED = 2
    REPLIED = 3
    LOGGEDIN=4
    PLAY=5

def importCourseraData():
    actorIdx = 0 #numerical id
    ignoreTheseUsers = [ObjectId('53b16012a66e44472a7e7d72'),ObjectId('53b160c4a66e444cbca4c2f4'),ObjectId('53b16feba66e444dff9c7c8e')]
    users = db.PraiseUser.find({'_id':{'$nin':ignoreTheseUsers}})
    #ir.Actors.remove({})
    for u in users:
        ir.Actors.insert({'_id':u['_id'],"name":u['display_name'], 'activities':[], 'idx':actorIdx })
        actorIdx = actorIdx + 1
    print "imported actors"
    
    media = db.AudioContent.find({'PraiseUser_id':{'$nin':ignoreTheseUsers}})
    ir.Media.remove({})
    for m in media:
        ir.Media.insert({"_id":m['_id'], 'owner':m['PraiseUser_id'], 'fmt':mediaFormats.VIDEO,'title':m['title'], 'ts':m['datetime']})
        uploadActivity = {'at':Activities.UPLOADED, 'ts':m['datetime'], 'id':m['_id']}
        ir.Actors.update({'_id':m['PraiseUser_id']}, {'$push':{'activities':uploadActivity}})
    print "imported media"
    
    comments = db.ActivityDefinition.find({'PraiseUser_id':{'$nin':ignoreTheseUsers}})
    for cm in comments:
        commentActivity = {'at':Activities.COMMENTED, '_id':cm['_id'], 'ts':cm['datetime'], 'media_id':cm['AudioContent_id'], 'text':cm['title']}
        ir.Actors.update({'_id':cm['PraiseUser_id']}, {'$push':{'activities':commentActivity}})
    print "imported comments"

    replies = db.Activity.find({'PraiseUser_id':{'$nin':ignoreTheseUsers}})
    for rp in replies:
        replyActivity = {'at':Activities.REPLIED, '_id':rp['_id'], 'ts':rp['datetime'], 'cmt_id':rp['ActivityDefinition_id'], 'text':rp['content']}
        ir.Actors.update({'_id':cm['PraiseUser_id']}, {'$push':{'activities':replyActivity}})
    print "imported replies"

    mvlog = db.MediaViewLog.find({'PraiseUser_id':{'$nin':ignoreTheseUsers}})
    for item in mvlog:
        viewActivity = {'at':Activities.VIEWED, 'ts':item['datetime'], 'id':item['AudioContent_id']}
        ir.Actors.update({'_id':item['PraiseUser_id']}, {'$push':{'activities':viewActivity}})
    print "Imported media view log"
    
    sessions = db.Session.find({'user_id':{'$nin':ignoreTheseUsers}})
    for item in sessions:
         loginActivity = {'at':Activities.LOGGEDIN, 'ts':item['sessionStart']}
         ir.Actors.update({'_id':item['user_id']}, {'$push':{'activities':loginActivity}})
    print "Imported sessions"
    
        
importCourseraData()
print "import complete!"