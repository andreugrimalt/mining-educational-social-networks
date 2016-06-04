import os      
import re
from pymongo import *
import numpy as np
import matplotlib.pyplot as plt
import pylab as p
import math
from bson import *
import pymysql

#source db 
#mongod --dbpath /Users/chris/expts/praise/dataAnalysis/mongo/db --fork --syslog
#mongod --dbpath /Users/matthew/Documents/PRAISE_local/data/musiccircle_latest/musiccircle
#cli = MongoClient("localhost:27017")
#db = cli.musiccircle

clir = MongoClient("localhost:27026")
ir = clir.research

mysqldb = pymysql.connect(db='coursera', user='root', passwd='root', host='localhost', port=8889	)

mysqldb.select_db('coursera')
mysql_cur = mysqldb.cursor()


def getSessionIdsFromDirectory(dir): 
	sessionIdsList=[]
	for subdir in os.walk(dir):
		for el in subdir[2]:
			if el=='fields.html':
				path=subdir[0]+'/'+el
				f = open(path, 'r')
				content = f.read()
				startSessionId='<title>'
				endSessionId='</title>'
				sessionId=re.search(re.escape(startSessionId)+"(.*?)"+re.escape(endSessionId),content).group(1)
				sessionId=sessionId.split('session_user_id: ')
				sessionId=sessionId[1].replace(')','')
				startMediaId='href="https://coursera.musiccircleproject.com/?media/'
				endMediaId='">'
				mediaId=re.search(re.escape(startMediaId)+"(.*?)"+re.escape(endMediaId),content)
				if mediaId!=None:
					mediaId=mediaId.group(1)
					mediaId=mediaId.split('" title="')
					#mediaIdsList.append(mediaId[0])
					sessionIdsList.append([{'sessionId':sessionId,'mediaId':mediaId[0]}])	
	return sessionIdsList


def getMCUserIds():
	data=[]
	for el in getSessionIdsFromDirectory('peer1'):
		oid=el[0]['mediaId']
		dataTemp={'sessionId':el[0]['sessionId'],'userId':oid}
		if ObjectId.is_valid(oid):
			userIdCursor=ir.Media.find({'_id':ObjectId(oid)})
			for i in userIdCursor:
				userId=i['owner']
				dataTemp['mcUserId']=userId
		data.append(dataTemp)
	return data

def linkMCUserIdsWithGrades():
	data=[]
	for el in getMCUserIds():
		dataTemp={'userId':el['userId']}
		query="SELECT normal_grade FROM course_grades WHERE session_user_id=\'"+str(el['sessionId'])+"\'"
		#query="select normal_grade from course_grades where session_user_id='3bb0d5a68482a648611c7533844c89ccf733ab1b'"
		#print query
		mysql_cur.execute(query)
		row=mysql_cur.fetchall()
		dataTemp['grade']=row[0]
		data.append(dataTemp)
		if 'mcUserId' in el:
			ir.ActorsGrade.insert({'id':ObjectId(el['mcUserId']),'grade':row[0]})
	#print data

def addActivitiesLength():
	for actor in ir.Actors.find():
		if 'activitiesLength' in actor:
			ir.ActorsGrade.update({'id':actor['_id']},{'$push':{'activitiesLength':actor['activitiesLength']}})

count=0
x=[]
y=[]
i=0
for actor in ir.ActorsGrade.find():
	if 'activitiesLength' in actor:
		a=actor['activitiesLength'][0][0]
		x.append(a)
		y.append(actor['grade'])
		i=i+1
plt.plot(y,x,'ro')
plt.show()
#linkMCUserIdsWithGrades()


