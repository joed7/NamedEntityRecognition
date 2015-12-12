from operator import itemgetter, attrgetter
import os
import pickle
from _collections import defaultdict

data = '../data/gene.train.txt'

train = '../data/train.txt'
test = '../data/test.txt'

sentences=[]

def readData():
    f = open(data)
    
    
    t_sent=[]
    c=0
    for i in f.readlines():   
        text = i.strip()
        
        if len(text) == 0:
            sentences.append(t_sent);
            t_sent = []
        else:
            t_sent.append(text)
    
    if len(t_sent) != 0:
        sentences.append(t_sent)
    print(len(sentences))      
    print(sentences[-1])          
    f.close()
    
def splitData():
    index = int(0.80 * len(sentences))
    
    training =   sentences[:index]
    testing =   sentences[index:]
    
    f = open(train,'w')
    
    for i,sent in enumerate(training):
        for k in sent:
            f.write(k+"\n")
        f.write('\n')    
    f.flush()
    
    f = open(test,'w')
    
    for i,sent in enumerate(testing):
        for k in sent:
            f.write(k+"\n")
        f.write(''+'\n')    
    f.flush()
    
    f.close()
    
    print (training[-1])    
    print (testing[-1])
    
    createPickle('../data/testing.pkl', testing)
    
def createPickle(name,lst):
    fileObject = open(name,'wb') 
    pickle.dump(lst,fileObject)   
    fileObject.close()    
    
        
readData()        
splitData()    