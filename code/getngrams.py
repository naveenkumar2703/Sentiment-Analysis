#@author: Sameer Darekar
#@title: Extract Noun ngrams till 4-grams

import nltk
from nltk import word_tokenize
import nltk.collocations

def addToDict(wordsFreqDict,star,ngram):
	ngram=ngram.lower()
	if ngram not in wordsFreqDict[star]:
		wordsFreqDict[star][ngram]=1
	else:
		wordsFreqDict[star][ngram]+=1
	return wordsFreqDict

path="C:\Users\samee\Desktop\ILS z 604\Senti Proj\Data\Popular business\yTz8_GylkgCkuiBjSz8mIQ.txt"
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
					wordsFreqDict[star][n_1gram]-=1
			elif prevTup[1] in nouns: # for 2-gram
				ngram=str(prevTup[0])+" "+str(tup[0])
				n_1gram=str(prevTup[0])
				n_1gram=n_1gram.lower()
				if(ngram not in wordCount):
					wordsFreqDict=addToDict(wordsFreqDict,star,ngram)
					wordCount.append(ngram)
					wordsFreqDict[star][n_1gram]-=1
			else:
				_1gram.append(str(tup[0])) #for 1-gram
				if (str(tup[0]) not in wordCount):
					wordsFreqDict=addToDict(wordsFreqDict,star,str(tup[0]))
					wordCount.append(str(tup[0]))
		_3prevTup=_2prevTup
		_2prevTup=prevTup
		prevTup=tup
minsupport=0 #to eliminate items with support <=1
wordFrequencyDict1={key: value for key,value in wordsFreqDict['1'].items() if value>minsupport}
wordFrequencyDict2={key: value for key,value in wordsFreqDict['2'].items() if value>minsupport}
wordFrequencyDict3={key: value for key,value in wordsFreqDict['3'].items() if value>minsupport}
wordFrequencyDict4={key: value for key,value in wordsFreqDict['4'].items() if value>minsupport}
wordFrequencyDict5={key: value for key,value in wordsFreqDict['5'].items() if value>minsupport}
wordFrequencyList=[]


wordFrequencyList.append(wordFrequencyDict1)
wordFrequencyList.append(wordFrequencyDict2)
wordFrequencyList.append(wordFrequencyDict3)
wordFrequencyList.append(wordFrequencyDict4)
wordFrequencyList.append(wordFrequencyDict5)
print (wordFrequencyList)
# for wordlist in wordFrequencyList:
# 	print wordlist
f.close()
