
import numpy as np
import random
import sys

class K_Means:

    def __init__(self, K):
        self.k = K
        self.centroids = []
        self.membership = []


    def loadData(self, filename='u.data'):
        mydata = np.genfromtxt(filename, skip_header=0)
        self.user = mydata[:,0]
        self.movie = mydata[:,1]
        self.rating = mydata[:,2]
        return self.user, self.movie, self.rating

    def makeDictionary(self):
        self.dictionary = {}
        for i in range(len(self.movie)):
            if self.movie[i] in self.dictionary:
                vectors = self.dictionary[self.movie[i]]
                vectors[self.user[i]] = self.rating[i]
                self.dictionary[self.movie[i]] = vectors
            else:
                newMovie = dict([(self.user[i], self.rating[i])])
                self.dictionary[self.movie[i]] = newMovie
        # print self.dictionary[1]
        return self.dictionary

    def makeCluster(self):
        #Create random clusters
        for i in range(self.k):
            #vector of length total users, pick random number 1-5
            self.centroids.append(np.random.uniform(low=1,high=5,size=len(self.user)))
            memberList = []
            self.membership.append(memberList)
        self.centroids = np.round(self.centroids)

        for movie in self.dictionary.keys():
            closest = np.argmin(self.calculateDistance(self.dictionary[movie]))
            # print closest
            # newVector = np.zeros(len(self.user))
            # for user in self.dictionary[movie].keys():
            #     # print type(self.dictionary[movie][user])
            #     newVector[user] = self.dictionary[movie][user]
            #     # print newVector[user]
            # newVector = newVector.tolist()
            newVector = []
            newVector.append(movie)
            # print len(newVector), len(self.user)
            self.membership[closest].append(newVector)
            # print type(self.membership[closest]), type(newVector)
            # print np.count_nonzero(self.membership[closest][0])
            self.recalculateCentroid(self.membership[closest], closest)


    def calculateDistance(self, movieDictionary):
        distList = []
        for centroid in self.centroids:
            total = 0
            for user in movieDictionary.keys():
                total += (centroid[user]-movieDictionary[user])**2
            distList.append(total)
        # print distList
        return distList

    def recalculateCentroid(self, memList, index):
        newCentroid = np.zeros(len(self.user))
        for i in range(len(memList)):
            for j in range(len(memList[i])):
                # newCentroid[j] += memList[i][j]
                movie = memList[i][j]
                for user in self.dictionary[movie].keys():
                    newCentroid[user] += self.dictionary[movie][user]
        # newCentroid = np.zeros(len(memList))
        newCentroid = np.round(newCentroid/len(memList))
        self.centroids[index] = newCentroid

    def getInfo(self):
        for i in range(len(self.membership)):
            print "New Cluster"
            for j in range(10):
                print self.membership[i][j]



if __name__ == "__main__":
    cluster = K_Means(5)
    u,m,r = cluster.loadData()
    collection = cluster.makeDictionary()
    cluster.makeCluster()
    cluster.getInfo()
