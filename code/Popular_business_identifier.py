"""@author:Naveen. This file simpy picks business that have atleast minNumberOfReviews from srcFolder to destFolder"""
from os import listdir
from os.path import isfile, join
import os
import shutil


srcFolder = '/Users/naveenkumar2703/GitHub/Sentiment-Analysis/Data/Very Popular business/'
destFolder = '/Users/naveenkumar2703/GitHub/Sentiment-Analysis/Data/Very Popular business 1/'
minNumberOfReviews = 300

def countNumberOfLines(fileName):
    file = open(fileName,'r')
    for numberOfLines,line in enumerate(file):
        pass
    return numberOfLines+1

def getPopularBusinessIds():
    popularBusiness = []

    for item in os.listdir(str(srcFolder)):
        if(item.endswith('.txt') and countNumberOfLines(str(srcFolder+item)) > (minNumberOfReviews-1)):
            popularBusiness.append(item)
    print(len(popularBusiness))
    return popularBusiness
           
           
def copyPopularBusiness():
    for item in getPopularBusinessIds():
        shutil.copy(str(srcFolder+item),destFolder)

           
copyPopularBusiness()

