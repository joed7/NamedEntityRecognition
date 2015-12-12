'''
for tag I count 24435
for tag B count 16637
for tag O count 345128

for tag_seq ('I', 'O') count 9622
for tag_seq ('<start>', 'B') count 749
for tag_seq ('<start>', 'O') count 13047
for tag_seq ('B', 'I') count 9633
for tag_seq ('I', 'I') count 14802
for tag_seq ('O', 'O') count 315457
for tag_seq ('O', 'B') count 15888
for tag_seq ('B', 'O') count 7002

[(('_rare_', 'O'), 25254), (('the', 'O'), 18048), (('.', 'O'), 15344), (('of', 'O'), 14711), ((',', 'O'), 12111)]

'''

from operator import itemgetter, attrgetter
import os
import pickle
from _collections import defaultdict
import re

data = '../data/train.txt'

tagCounts=defaultdict(int)
trans_prob=defaultdict(int)
emiss_prob = defaultdict(int)
vocab=defaultdict(int)

wc = defaultdict(int)

threshold = 4

all_num=r'^[0-9]+$'
all_caps=r'^[A-Z]+$'
punct=r'^[^a-zA-Z0-9]+$'
nums_caps=r'^[0-9]+[A-Z]+$'
caps_nums=r'^[A-Z]+[0-9]+$'
nums_smalls=r'^[0-9]+[a-z]+$'
small_nums=r'^[a-z]+[0-9]+$'
small_caps=r'^[a-z][A-Z]+$'
pattern_1=r'^[A-Z].*[0-9]$'
pattern_2=r'^[a-z].*[0-9]$'
pattern_3=r'^.*[A-Z]+$'
#capssmall=r'^[a-zA-Z]+$'
#aplhanumeic=r'^[a-A-Z0-9]+$'

def featureEngineering(word):
    if re.search(all_num,word):
        return 'allnum'
    if re.search(all_caps,word):
        return 'allcaps'
    if re.search(punct,word):
        return 'punct'
    if re.search(nums_caps,word):
        return 'nums_caps'
    if re.search(caps_nums,word):
        return 'caps_nums'
    if re.search(nums_smalls,word):
        return 'nums_smalls'
    if re.search(small_nums,word):
        return 'small_nums'
    if re.search(small_caps,word):
        return 'small_caps'
    if re.search(pattern_1,word):
        return 'pattern_1'        
    if re.search(pattern_2,word):
        return 'pattern_2'    
    if re.search(pattern_3,word):
        return 'pattern_3'
    return '_rare_'

def filter_rare_words():
    f = open(data)
    for i in f.readlines():
        i=i.strip()
        if len(i) == 0:
            continue

        (text,tag) = i.split()
        text = text.lower()
        wc[text] = wc[text] +1        
    rare_words={}
    
    f = open(data)
    
    for i in f.readlines():
        i=i.strip()
        if len(i) == 0:
            continue
        (text,tag) = i.split()
        ltext = text.lower()
        
        if wc[ltext] < threshold:
            rare_words[text]=1
        
    '''    
    for (k,v) in wc.items():
        if v < threshold:
            rare_words[k]=1
    '''            
    return rare_words        
    f.close()
    
def readData(rare_words):
    f = open(data)

    prev='<start>'
    
    for i in f.readlines():
        i=i.strip()
        if len(i) == 0:
            prev = '<start>'
            continue

        (text,tag) = i.split()
        
        
        if text in rare_words:
            text = featureEngineering(text)
        else:
            text = text.lower()
            vocab[text]=1
                
        word_seq = (text,tag) 
        emiss_prob[word_seq] = emiss_prob[word_seq]+ 1
        
        '''Handling tags
        '''
        
        tagCounts[tag] = tagCounts[tag] +1
       
        tag_seq = (prev,tag)
        trans_prob[tag_seq] = trans_prob[tag_seq] + 1
        
        prev = tag
    f.close()
    
def createPickle(name,dict):
    fileObject = open(name,'wb') 
    pickle.dump(dict,fileObject)   
    fileObject.close()    

rare_words = filter_rare_words()
#print rare_words.items()[0:5]
readData(rare_words)



count_start_tags = 0;
    
for (k,v) in trans_prob.items():
    if k[0].find('start') != -1:
        count_start_tags = count_start_tags+v
    print 'for tag_seq ' + str(k) + ' count '+ str(v)
    
tagCounts['<start>'] = count_start_tags

print ''

print 'printing tags'
for (k,v) in tagCounts.items():
    print 'for tag ' + k + ' count '+ str(v)
    
print ''

print ''
    
print sorted(emiss_prob.items(),key=(itemgetter(1)),reverse=True)[0:5]    
#print "('the','I')->"+str(emiss_prob[('the','I')])



createPickle('../data/counts.pkl', tagCounts)
createPickle('../data/trans.pkl', trans_prob)
createPickle('../data/emiss.pkl', emiss_prob)
createPickle('../data/vocab.pkl', vocab)


#f.close()
#r.close()
print('done')