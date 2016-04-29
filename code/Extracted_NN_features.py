Author= "Hassan Alhuzali"
Created_at= "4/9/2016"
import json
import nltk
from nltk import word_tokenize
import os

 
def extractBusinessIdReview():
    #extracts business_id and its associated reviews in order to bewritten into a file, taking its business_id as the filename
    i=0
    with open('yelp_academic_dataset_review.json') as file:
        for line in file:
            #i+=1
            try:
                extract=json.loads(line,encoding='ascii')
                bus_id=str(extract["business_id"])
                star= str(extract["stars"])
                review = str.replace(str(extract["text"]),"\n","")
                filename= bus_id
                with open(filename + ".txt",mode='a+') as file_write:
                    if bus_id in line:
                        file_write.write(star + '\t')
                        file_write.write(review)
                        file_write.write("\n")
            except UnicodeEncodeError:
                continue
                #if i==50:
                #break
    print("...Done...")


   
def extractedDictOfWordsFreq(srcFolder):
    """returns a dict that has key as(star) and value as(word:freq)
    
    str -> dict"""
    for fname in os.listdir(srcFolder):
        try:
            dict_words_freq={}
            for line in open(os.path.join(srcFolder, fname)):
                key=line.split()[0]
                if key not in dict_words_freq:
                    dict_words_freq[key]= {}
                text = word_tokenize(line)
                pos = nltk.pos_tag(text)
                for item in pos:
                    if item[1] in ['NN','NNS', 'NNP', 'NNPS']:
                        word= item[0].lower()
                        if word not in dict_words_freq[key]:
                            dict_words_freq[key][word] = 1
                        else:
                            dict_words_freq[key][word]+=1
            return dict_words_freq
        except UnicodeDecodeError:
            continue

def main():
    #Called the above functions
    print("...Filtering the data...")
    srcFolder = 'filePath'
    extractedDictOfWordsFreq(srcFolder)

    print("...Done...")
##    extractBusinessIdReview()   
if __name__=="__main__":
    #Called the main function
    main()
