import numpy as np
from sklearn.decomposition import PCA
import json
import matplotlib.pyplot as plt
import math
from sklearn.cluster import KMeans
from sklearn import metrics



pca = PCA(n_components=2)

def getJSONDataAsList(json_data):
	featureListFromFile = json.load(json_data)
	featureList=[]
	for actor in featureListFromFile['features']:
		for feature in actor['featureVectors']:
			featureList.append(feature)
	print "features list has = ",len(featureList)," values"
	return featureList

def getJSONData(json_data):
	return json.load(json_data)

def performPCA(featureList):
	pca.fit(featureList)
	print "variances = ",pca.explained_variance_ratio_
	transformedVectors=pca.transform(featureList)
	return transformedVectors

def normaliseList(featureList):
	featureListNorm=[]
	for feature in featureList:
		norm=math.sqrt(sum([j*j for j in feature]))
		if norm !=0:
			normalisedVector=[float(i)/math.sqrt(sum([j*j for j in feature])) for i in feature]
		else:
			normalisedVector=[0 for i in feature]
		featureListNorm.append(normalisedVector)
	return featureListNorm

def preapareForPlot(featureList):
	X=[x[0] for x in featureList]
	Y=[y[1] for y in featureList]
	return[X,Y]

def clusterKMeans(featureList,nClusters):
	k_means = KMeans(n_clusters=nClusters,init='random')
	k_means.fit(featureList)
	clusterClasses=[]
	for feature in featureList:
		cluster=k_means.predict(feature)
		for c in cluster:
			clusterClasses.append(c)
	return clusterClasses

def calculateGroundTruthClustering(json_data):
	featureListFromFile = json.load(json_data)
	groundTruthCuster=[]
	i=0
	for actor in featureListFromFile['features']:
		for feature in actor['featureVectors']:
			groundTruthCuster.append(i)
		i=i+1
	return groundTruthCuster

def compareClustering(groundTruth,modelCluster):
	print "adjusted random score (different from assigning random classes?)= ",metrics.adjusted_rand_score(groundTruthCustering,modelCluster)
	print "adjusted mutual Information based scores (tends to increase with number of clusters)= ",metrics.adjusted_mutual_info_score(groundTruthCustering,modelCluster)
	print "homogenity, completeness, v-measure scores = ",metrics.homogeneity_completeness_v_measure(groundTruthCustering,modelCluster)


figure=plt.figure()

featureList=getJSONDataAsList(open('histogramFeatureVectors.json'))
#normalise
normalisedList=normaliseList(featureList)

# plot first 2 components of normalised data
#doTheplot(normalisedList,'b')

#cluster featureList
print 'clustering'
#featureListClustering=clusterKMeans(featureList,len(featureList))

# feature clustering vs ground truth clustering
'''
print "cluster metrics for featureList"
groundTruthCustering=calculateGroundTruthClustering(open('histogramFeatureVectors.json'))
'''
#nUsers = len(json.load(open('histogramFeatureVectors.json'))['features'])
#plt.hist(groundTruthCustering,nUsers)
#plt.show()
#compareClustering(groundTruthCustering,featureListClustering)

#normalised feature clustering vs ground truth clustering
#print "cluster metrics for normalised feature list (I checked it's exactly the same as with non normlised)"
#compareClustering(normalisedList,featureListClustering)

# do PCA


print "PCA"
pcaFeatureList=performPCA(normalisedList)
print 'clustering....'
print len(pcaFeatureList)
'''
pcaClustering = clusterKMeans(pcaFeatureList,1332)
print 'comparing...'
compareClustering(pcaFeatureList,pcaClustering)

print 'making hist ...'
plt.hist(pcaClustering,len(pcaClustering))
plt.savefig('pcaClustering.png')
'''

featureListData=preapareForPlot(featureList)
featureListFigure = plt.figure(0)
ax1 = featureListFigure.add_subplot(111)
ax1.plot(featureListData[0], featureListData[1],'ro')
plt.savefig('pca2D.png')
'''
normFeatureListData=preapareForPlot(normalisedList)
normFeatureListFigure = plt.figure(1)
ax2 = normFeatureListFigure.add_subplot(111)
ax2.plot(normFeatureListData[0], normFeatureListData[1],'ro')
'''
plt.show()

'''
#doTheplot(pcaFeatureList,'r')





