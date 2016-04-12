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
	star=seperateReview[0]
	review=seperateReview[1].strip()
	if star not in wordsFreqDict:
		wordsFreqDict[star]= {}
	tokenizedWords=word_tokenize(review)
	postaggedWords=nltk.pos_tag(tokenizedWords)
	nouns=['NN','NNS','NNP','NNPS']
	for tup in postaggedWords:
		#tup=list(tup)
		if tup[1] in nouns:
			if _3prevTup[1] in nouns and _2prevTup[1] in nouns and prevTup[1] in nouns: # for 4-grams
				ngram=str(_3prevTup[0])+" "+str(_2prevTup[0])+" "+str(prevTup[0])+" "+str(tup[0])
				n_1gram=str(_3prevTup[0])+" "+str(_2prevTup[0])+" "+str(prevTup[0])
				n_1gram=n_1gram.lower()
				wordsFreqDict=addToDict(wordsFreqDict,star,ngram)
				try:
					wordsFreqDict[star][n_1gram]-=1
				except KeyError:  #code for ignoring higher n grams
					continue
			elif _2prevTup[1] in nouns and prevTup[1] in nouns:  # for 3-gram
				ngram=str(_2prevTup[0])+" "+str(prevTup[0])+" "+str(tup[0])
				n_1gram=str(_2prevTup[0])+" "+str(prevTup[0])
				n_1gram=n_1gram.lower()
				wordsFreqDict=addToDict(wordsFreqDict,star,ngram)
				wordsFreqDict[star][n_1gram]-=1
			elif prevTup[1] in nouns: # for 2-gram
				ngram=str(prevTup[0])+" "+str(tup[0])
				n_1gram=str(prevTup[0])
				n_1gram=n_1gram.lower()
				wordsFreqDict=addToDict(wordsFreqDict,star,ngram)
				wordsFreqDict[star][n_1gram]-=1
			else:
				_1gram.append(str(tup[0])) #for 1-gram
				wordsFreqDict=addToDict(wordsFreqDict,star,str(tup[0]))
		_3prevTup=_2prevTup
		_2prevTup=prevTup
		prevTup=tup
minsupport=2 #to eliminate items with support <=1
#wordFrequencyDict={[key1][key2]: value for key1,key2,value in wordsFreqDict.items() if value>minsupport}
print wordsFreqDict['1']
print wordsFreqDict.keys()
f.close()

	#adj,Noun(JJ NN)
	#