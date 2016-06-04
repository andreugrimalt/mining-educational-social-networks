%pylab inline
%matplotlib inline
from bson import *
from pymongo import *
import time
from datetime import timedelta
from pylab import *

#source db 
#mongod --dbpath /Users/chris/expts/praise/dataAnalysis/mongo/db --fork --syslog
#mongod --dbpath /Users/matthew/Documents/PRAISE_local/data/musiccircle_latest/musiccircle
cli = MongoClient("localhost:27017")
db = cli.musiccircle

#target instance - intermediate representation
#mongod --port 27018 -dbpath /Users/chris/expts/praise/dataAnalysis/mongo/mus0IR --fork --syslog 
# mongod --port 27018 --dbpath /Users/matthew/Documents/PRAISE_local/data/musiccircle_latest/processedclir = MongoClient("localhost:27018")
#clir = MongoClient("localhost:27018")
#ir = clir.mus0IR

# Class that plots frequency of items in a collection vs time

class PlotItemsVsTime:
    
    def __init__(self,title,data,startDate,resolutionInDays,datefieldName):
        self.data = data.find().sort(datefieldName,1)
        self.title=title
        self.startDate=startDate
        self.resolutionInDays=resolutionInDays
        self.datefieldName=datefieldName
    
    def binData(self):
        mainList=[]
        tempList=[]
        self.startDate=self.startDate.replace(hour=0, minute=0, second=0, microsecond=0)
        deltaDays=self.resolutionInDays
        nextDate=self.startDate+timedelta(days=deltaDays)
        print "items in input collection",self.data.count()
        print "start date=",self.startDate
        for item in self.data:
            currentDate=item[self.datefieldName]
            if currentDate != None:
                if nextDate>=currentDate:
                    tempList.append(item)
                elif currentDate>=nextDate:
                        mainList.append({"date":self.startDate,"items":tempList})
                        self.startDate=currentDate.replace(hour=0, minute=0, second=0, microsecond=0)
                        nextDate=self.startDate+timedelta(days=deltaDays)
                        tempList=[]
                        #there is an item that will go in the next group, so add it now
                        tempList.append(item)
        mainList.append({"date":self.startDate,"items":tempList})
        print "end date",currentDate
        print "bins=",len(mainList)
        self.binList=mainList
        return mainList
    
    def countFreqOfBins(self):
        preparedList=[]
        count=0
        for i in self.binList:
            preparedList.append({"date":i["date"],"freq":len(i["items"])})
            count=count+len(i["items"])    
        print "total items=",count
        self.preparedList=preparedList
        return preparedList
    
    def checkForLostItems(self):
        count=0
        for item in self.preparedList:
            count=count+item["freq"]
        if count==self.data.count():
            print "data is OK"
        else:
            print "data might be wrong, diff=",count-self.data.count()
    
    def doThePlot(self):
        self.binData()
        self.countFreqOfBins()
        self.checkForLostItems()
        plt.figure(figsize=(12,6))
        plt.plot([element["date"] for element in self.preparedList],[element["freq"] for element in self.preparedList],"ro-")
        plt.title(self.title)
        plt.show()

# Uploads per day 
uploadsPerDay=PlotItemsVsTime("Uploads/day",db.AudioContent,datetime.datetime(2014, 6, 30, 13, 18, 42, 824000),1,"datetime")
uploadsPerDay.doThePlot()

# Sessions per day
sessionsPerDay=PlotItemsVsTime("Sessions/day",db.Session,datetime.datetime(2014, 6, 30, 13, 18, 42, 824000),1,"sessionStart")
sessionsPerDay.doThePlot()

# Views per day
viewsPerDay=PlotItemsVsTime("Views/day",db.MediaViewLog,datetime.datetime(2014, 6, 30, 15, 11, 32, 585000),1,"datetime")
viewsPerDay.doThePlot()

# Comments per day
commentsPerDay=PlotItemsVsTime("Comments/day",db.ActivityDefinition,datetime.datetime(2014, 6, 30, 19, 48, 45, 511000),1,"datetime")
commentsPerDay.doThePlot()

# Replies per day
repliesPerDay=PlotItemsVsTime("Replies/day",db.Activity,datetime.datetime(2014, 6, 30, 19, 48, 45, 511000),1,"datetime")
repliesPerDay.doThePlot()