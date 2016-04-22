#@author: Sameer Darekar
#@title: takes the popular business and creates json files for display

import nltk
from nltk import word_tokenize
import json 
import os
import sys


def addToDict(wordsFreqDict,star,ngram):
	ngram=ngram.lower()
	if ngram not in wordsFreqDict[star]:
		wordsFreqDict[star][ngram]=1
	else:
		wordsFreqDict[star][ngram]+=1
	return wordsFreqDict

def getUniqueKeys(wordFrequencyList):
	uniqueKeys=set()
	for dictionary in wordFrequencyList:
		keys=list(dictionary.keys())
		uniqueKeys.update(keys)
	return list(uniqueKeys)

def getWordsWithCondition(wordFrequencyList):
	"""2 conditions for selection Criteria:
	1. occurs in dictionaries of two stars atleast once
	2. if condition 1 not satisfied and appears only in one star dictionary it shd occur atleast twice
	"""
	uniqueKeys=getUniqueKeys(wordFrequencyList)
	#noOfDict_1=2 	#condition 1
	#noOfStars_1=1
	#noOfStars_2=2 	#condition 2	
	wordsWithCondition={}  #format [word,[dictCount]]
	dictCount=[]  #format [count in 1,count in 2,count in 3,count in 4,count in 5]
	for key in uniqueKeys:
         dictCount=[-1,-1,-1,-1,-1]
         noOfDict=0
         noOfStars=0
         for i in range(len(wordFrequencyList)):
             if key in wordFrequencyList[i]:
                   noOfDict+=1
                   dictCount[i]=wordFrequencyList[i][key]
                   noOfStars += wordFrequencyList[i][key]
             else:
                 dictCount[i]=0
                 
         if noOfStars >= 5 or (noOfDict < 3 and noOfStars > 1):
             wordsWithCondition[key]=dictCount
            
		
#          """if noOfDict>=noOfDict_1:  #checking for condition 1
#			count=0
#			for cnt in dictCount:
#				if cnt>=noOfStars_2:  #checking for condition 2
#					wordsWithCondition[key]=dictCount
#					break
#				if cnt>=1:
#					if count>=noOfStars_1:
#						wordsWithCondition[key]=dictCount
#						break
#					else:
#						count+=1"""
	return wordsWithCondition

def getRatioDict(wordsWithCondition):
	ratioDict={}
	for key in list(wordsWithCondition.keys()):
		ratioDict[key]=[float(x)/sum(wordsWithCondition[key]) for x in wordsWithCondition[key]]
	return ratioDict

def getOverAllPerformance(ratioDict):
    performanceDict = {}
    for key in list(ratioDict.keys()):
        if ratioDict[key][0] + ratioDict[key][1] > 0.49:
            performanceDict[key] = 'Bad'
        elif ratioDict[key][3] + ratioDict[key][4] > 0.75:
            performanceDict[key] = 'Good'
        else:
            performanceDict[key] = 'Average'
    return performanceDict

def createJson(wordFrequencyList,fileName):
    #pathForJsonFiles="C:\Users\samee\Desktop\ILS z 604\sentiProjMine\jsonFiles"  #path for JSON Files
    pathForJsonFiles= "/Users/naveenkumar2703/GitHub/Sentiment-Analysis/Data/json-files/"
    wordsWithCondition=getWordsWithCondition(wordFrequencyList)
    ratioDict=getRatioDict(wordsWithCondition)
    performanceDict = getOverAllPerformance(ratioDict)
    fileN=pathForJsonFiles+fileName[:-4]+".json"
    with open(fileN,'w') as fp:
        featuresArray = []
        for key in list(wordsWithCondition.keys()):
            d={'name':key,"performance":performanceDict[key],"star_1":wordsWithCondition[key][0],"star_2":wordsWithCondition[key][1],"star_3":wordsWithCondition[key][2],"star_4":wordsWithCondition[key][3],"star_5":wordsWithCondition[key][4]}
            featuresArray.append(d)
        md = {"features":featuresArray}
        json.dump(md,fp,sort_keys=True,indent=2)
        fp.close()
        print (".......json File %s created" % fileName[:-4])
    return 


	
#fileName="yTz8_GylkgCkuiBjSz8mIQ.txt"
print("Processing Popular Business")
#popularBusinessPath="C:\Users\samee\Desktop\ILS z 604\Senti Proj\Data\Popular business"
popularBusinessPath="/Users/naveenkumar2703/GitHub/Sentiment-Analysis/Data/Temp3/"
#path="C:\Users\samee\Desktop\ILS z 604\Senti Proj\Data\Popular business\yTz8_GylkgCkuiBjSz8mIQ.txt"  #Path for popular business
for fileName in os.listdir(popularBusinessPath):
    if not fileName.endswith(".txt"):
        continue
    sys.stdout.write("\r" + "processing with File %s " % fileName)
    sys.stdout.flush()
    path=popularBusinessPath+fileName
    f=open(path)
    _1gram=[]
    _2gram=[]
    _3gram=[]
    _2prevTup=("","")
    _3prevTup=("","")
    prevTup=("","")
    wordsFreqDict={}
    for line in f:
        seperateReview=line.split('\t')
        if len(seperateReview)<2:
            continue
        wordCount=[]
        star=seperateReview[0]
        review=seperateReview[1].strip()
        if star not in wordsFreqDict:
            wordsFreqDict[star]= {}
        tokenizedWords=word_tokenize(review)
		#todo convert it to singular word
        postaggedWords=nltk.pos_tag(tokenizedWords)
        nouns=['NN','NNS','NNP','NNPS']
        for tup in postaggedWords:
			#tup=list(tup)
            if tup[1] in nouns:
                if _3prevTup[1] in nouns and _2prevTup[1] in nouns and prevTup[1] in nouns: # for 4-grams
                    ngram=str(_3prevTup[0])+" "+str(_2prevTup[0])+" "+str(prevTup[0])+" "+str(tup[0])
                    n_1gram=str(_3prevTup[0])+" "+str(_2prevTup[0])+" "+str(prevTup[0])
                    n_1gram=n_1gram.lower()
                    if(ngram not in wordCount):
                        wordsFreqDict=addToDict(wordsFreqDict,star,ngram)
                        wordCount.append(ngram)
                        try:
                            wordsFreqDict[star][n_1gram]-=1
                        except KeyError:  #code for ignoring higher n grams
                            continue
                elif _2prevTup[1] in nouns and prevTup[1] in nouns:  # for 3-gram
                        ngram=str(_2prevTup[0])+" "+str(prevTup[0])+" "+str(tup[0])
                        n_1gram=str(_2prevTup[0])+" "+str(prevTup[0])
                        n_1gram=n_1gram.lower()
                        if(ngram not in wordCount):
                            wordsFreqDict=addToDict(wordsFreqDict,star,ngram)
                            wordCount.append(ngram)
                            try:
                                wordsFreqDict[star][n_1gram]-=1
                            except KeyError:  #code for ignoring higher n grams
                                continue
                elif prevTup[1] in nouns: # for 2-gram
                        ngram=str(prevTup[0])+" "+str(tup[0])
                        n_1gram=str(prevTup[0])
                        n_1gram=n_1gram.lower()
                        if(ngram not in wordCount):
                            wordsFreqDict=addToDict(wordsFreqDict,star,ngram)
                            wordCount.append(ngram)
                            try:
                                wordsFreqDict[star][n_1gram]-=1
                            except KeyError:  #code for ignoring higher n grams
                                continue
                else:
                        _1gram.append(str(tup[0])) #for 1-gram
                        if (str(tup[0]) not in wordCount):
                            wordsFreqDict=addToDict(wordsFreqDict,star,str(tup[0]))
                            wordCount.append(str(tup[0]))
            _3prevTup=_2prevTup
            _2prevTup=prevTup
            prevTup=tup
    minsupport=1 #to eliminate items with support <=1
    try:
        wordFrequencyDict1={key: value for key,value in wordsFreqDict['1'].items() if value>minsupport}
        wordFrequencyDict2={key: value for key,value in wordsFreqDict['2'].items() if value>minsupport}
        wordFrequencyDict3={key: value for key,value in wordsFreqDict['3'].items() if value>minsupport}
        wordFrequencyDict4={key: value for key,value in wordsFreqDict['4'].items() if value>minsupport}
        wordFrequencyDict5={key: value for key,value in wordsFreqDict['5'].items() if value>minsupport}
    except KeyError:  #code for ignoring higher n grams
        continue
    wordFrequencyList=[]


    wordFrequencyList.append(wordFrequencyDict1)
    wordFrequencyList.append(wordFrequencyDict2)
    wordFrequencyList.append(wordFrequencyDict3)
    wordFrequencyList.append(wordFrequencyDict4)
    wordFrequencyList.append(wordFrequencyDict5)

    #print(wordFrequencyList)
    createJson(wordFrequencyList,fileName)
	# for wordlist in wordFrequencyList:
	# 	print wordlist
    f.close()
