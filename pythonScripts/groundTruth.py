from numpy import genfromtxt
from bson import *
from pymongo import *
import time
from datetime import timedelta
import numpy as np
import sys
import json
from pymongo.errors import InvalidOperation
import operator
import matplotlib.pyplot as plt
import pylab as p
import math
import os
from sklearn.cluster import KMeans
from sklearn import datasets, linear_model
import random


clir = MongoClient("localhost:27026")
ir = clir.research


def generateCummulativeListFromFeatureVectorsBySession(json_data):
	featureListFromFile = json.load(json_data)
	cummulative=[]

	for actor in featureListFromFile['features']:
		actorId=actor['actor_id']
		uploads=0
		region_block=0
		my_tracks=0
		community_tracks=0
		play=0
		allActivities=0

		for featureVector in actor['featureVectors']:
			uploads=uploads+featureVector[0]
			region_block=region_block+featureVector[1]
			my_tracks=my_tracks+featureVector[2]
			community_tracks=community_tracks+featureVector[3]
			play=play+featureVector[4]
			allActivities=allActivities+featureVector[0]+featureVector[1]+featureVector[2]+featureVector[3]+featureVector[4]
		cummulative.append({'actor_id':actorId,'features':[uploads,region_block,my_tracks,community_tracks,play,allActivities]})

	return cummulative

def generatePlot():
	cummulativeList=generateCummulativeListFromFeatureVectorsBySession(open('histogramFeatureVectors.json'))

	y=[]
	grades=[]
	for actor in cummulativeList:
		grade=ir.ActorsGrade.find_one({'id':ObjectId(actor['actor_id'])})
		if grade != None:
			# uploads
			#y.append(actor['features'][0])

			# region block
			#y.append(actor['features'][1])

			# my tracks
			#y.append(actor['features'][2])

			# community tracks
			#y.append(actor['features'][3])

			# play
			#y.append(actor['features'][4])

			# all activities
			y.append(actor['features'][5])
			grades.append(grade['grade'])

	
	regr = linear_model.LinearRegression()
	regr.fit(grades, y)
	# The coefficients
	print('Coefficients: \n', regr.coef_)
	print('R^2', regr.score(grades,y))

	plt.xlabel('Grades')
	plt.ylabel('Number of activities')
	plt.plot(grades,y,'o')
	plt.savefig('allActivities.png')
	plt.show()
	

generatePlot()