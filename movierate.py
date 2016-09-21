
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
        """
        Create dictionary of movies as keys and dictionary as value
        That dictionary contains users as keys and ratings as values
        """
        self.dictionary = {}
        for i in range(len(self.movie)):
            if self.movie[i] in self.dictionary:
                vectors = self.dictionary[self.movie[i]]
                vectors[self.user[i]] = self.rating[i]
                self.dictionary[self.movie[i]] = vectors
            else:
                newMovie = dict([(self.user[i], self.rating[i])])
                self.dictionary[self.movie[i]] = newMovie
        return self.dictionary

    def makeCluster(self):
        """Create random sparse vectors as centroids
        adds movies to centroid membership lists based on distance from centroid
        Recalculate the centroid after every new addition"""
        for i in range(self.k):
            #vector of length total users, pick random number 1-5
            self.centroids.append(np.random.uniform(low=1,high=5,size=len(self.user)))
            memberList = []
            self.membership.append(memberList)
        self.centroids = np.round(self.centroids)

        for movie in self.dictionary.keys():
            #Finds the index of the closest centroid
            closest = np.argmin(self.calculateDistance(self.dictionary[movie]))
            newVector = []
            newVector.append(movie)
            #Add the movie to the list of members of the closest centroid
            self.membership[closest].append(newVector)
            self.recalculateCentroid(self.membership[closest], closest)

    def calculateDistance(self, movieDictionary):
        '''Uses Euclidean distance to match ratings between users
        Returns list of distances between user ratings centroids'''
        distList = []
        for centroid in self.centroids:
            total = 0
            for user in movieDictionary.keys():
                total += (centroid[user]-movieDictionary[user])**2
            distList.append(total)
        return distList

    def recalculateCentroid(self, memList, index):
        '''Sums up all the ratings for that user, divides by number of members'''
        newCentroid = np.zeros(len(self.user))
        for i in range(len(memList)):
            for j in range(len(memList[i])):
                movie = memList[i][j]
                for user in self.dictionary[movie].keys():
                    newCentroid[user] += self.dictionary[movie][user]
        newCentroid = np.round(newCentroid/len(memList))
        self.centroids[index] = newCentroid

    def getInfo(self):
        '''Print out closest members to each centroid'''
        for i in range(len(self.membership)):
            print "Cluster %d" %i
            lyst = self.centroidDist(self.membership[i], i)
            sort = lyst.sort()
            for j in range(10):
                dist, movie = lyst[j]
                print int(movie)


    def centroidDist(self, movieList, centroidInd):
        '''Euclidean distance of member movie from its centroid'''
        distList = []
        for mem in movieList:
            total = 0
            for key in self.dictionary[mem[0]].keys():
                total += (self.centroids[centroidInd][key]-self.dictionary[mem[0]][key])**2
            distList.append((total, mem[0]))
        return distList




if __name__ == "__main__":
    cluster = K_Means(5)
    u,m,r = cluster.loadData()
    collection = cluster.makeDictionary()
    cluster.makeCluster()
    cluster.getInfo()
