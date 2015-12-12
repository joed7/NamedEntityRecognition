import os
import pickle
import numpy as np
import math


tags = ['B','I','O']            

def loadPickle(name):
    fileObject = open(name,'r')  
    b = pickle.load(fileObject)  
    return b

def tag(test):
    tagged_sent = []
    output = ''
    
    for each_sent in test:
        parsed_sent = []
        
        orig_sent = []
        
        for each_word in each_sent:
            word = each_word.split()[0]
            orig_sent.append(word)
            if word.lower() not in vocab:
                word="_rare_"
            parsed_sent.append(word)
        
        #tagged_sent.append(viterbi(parsed_sent))
        
        sent = viterbi(parsed_sent)
        for i,j in zip(orig_sent,sent):
            print i,j
            output = output +i +'\t'+j +'\n'
        output = output +'\n'
    
    f = open('../data/ouput.txt','w')
    f.write(output)
    f.flush()
    f.close()        
def viterbi(sentence):
    
    #print sentence

       
    log_fuc = np.vectorize(calculateLog)
    
    prob_mat = np.zeros( (len(tags),len(sentence))  )
    bp = np.chararray(  (len(tags),len(sentence))   )
    
    for (i1,word) in enumerate(sentence):
        for (i2,tag) in enumerate(tags):
            
            if i1 == 0:
                (prob,tag)=handleAny(word,tag,['<start>'],log_fuc(np.ones((len(tags)))))
            else:
                (prob,tag)=handleAny(word,tag,['B','I','O'], prob_mat[:,i1-1])    
            
            prob_mat[i2,i1]=prob
            bp[i2,i1]=tag    
    
       
    
    tagged = findBestAlignment(prob_mat, bp)   
    #print tagged
    assert len(sentence) == len(tagged)
    return tagged

    
     
def findBestAlignment(prob_mat,bp):
    assert  prob_mat.shape == bp.shape
    
    
    total_col = len(prob_mat[0])
    
    col_index = total_col-1
    
    fin_col = prob_mat[:,col_index]
    index = np.argmax(fin_col, axis=0)
    output_tags = []
    
    output_tags.insert(0,tags[index])

    prev_best_tag = bp[index][col_index]
    
    while prev_best_tag.find('<') == -1:
        output_tags.insert(0,prev_best_tag)
        col_index = col_index -1
        index = getTagIndex(prev_best_tag)
        prev_best_tag = bp[index][col_index]
        
    #print output_tags
    return output_tags

def getTagIndex(ch):
    for i,t in enumerate(tags):
        if t == ch:
            return i
                           
def calculateLog(val):
    if val ==0:
        return -1 * 10 ** 25
    else :
        return math.log(val)

def handleAny(word,cur_tag,tags,prob_matrix ):
    
    max_prob =-1* float('inf')
    
    
    emission = 1.0*emis_count[(word.lower(),cur_tag)]/counts[cur_tag]
    #best_tag='O'
    best_tag=''
    if emission > 0.0:
        best_tag = cur_tag
        
        
    for (i,prev_tag) in enumerate(tags):
        
        transition = 1.0 * transition_count[ (prev_tag,cur_tag) ]/counts[prev_tag]
        prev_prob_state = prob_matrix[i]
        
        prob =  calculateLog(emission) + calculateLog(transition) + prev_prob_state
        
        
        if prob > max_prob :
            max_prob = prob
            best_tag = prev_tag
    
    return (max_prob,best_tag)    
counts = loadPickle('../data/counts.pkl')
transition_count = loadPickle('../data/trans.pkl')
emis_count = loadPickle('../data/emiss.pkl')
vocab = loadPickle('../data/vocab.pkl')

test_set = loadPickle('../data/testing.pkl')
tag(test_set)