Author= "Hassan Alhuzali"
Created_at= "3/27/2016"
import json


def extract_business_review():
    #extracts business_id and its associated reviews in order to bewritten into a file, taking its business_id as the filename
    Ei=0
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

def read_directory(dirname):
    #reads files inside the given directory
    i=0
    for fname in os.listdir(dirname):
        print (fname)
        i+=1
        try:
            for line in open(os.path.join(dirname, fname)):
                line
        except UnicodeDecodeError:
            continue 
    print ("The number of files in this directory is:", i)

def main():
    print("...Filtering the data...")
    
    extract_business_review()
        
if __name__=="__main__":
    #called the main function
    main()
