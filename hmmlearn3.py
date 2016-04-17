import sys
from collections import defaultdict
import pickle
import json

def main():
    taglist = list()
    uniquetags = list()
    rootDict = defaultdict(dict)    #this contains tag to word mapping with number of occurrences of the word
    tagsDict = defaultdict(dict)    #this contains transition values
    tagsCounter = dict()
    emmitTagCounter = dict()
    
    uniquetags.append('S0')         #initialize start of sentence tag
    
    filename = sys.argv[1]
    
    with open(filename,'r',encoding='utf-8') as infile:
        for line in infile:
            currentTag = 'S0'
            prevTag = 'S0'

            if 'S0' not in tagsCounter:
                tagsCounter['S0'] = 1
            else:
                tagsCounter['S0'] += 1
                
            if 'S0' not in emmitTagCounter:
                emmitTagCounter['S0'] = 1
            else:
                emmitTagCounter['S0'] += 1
            
            words = line.split()
            taglist.append('S0')
            for word in words:
                token = word[:-3]   #this gives the word
                tag = word[-2:] #this gives the POS tag
                
                #Logic for word to tag mapping
                if token not in rootDict:     
                    rootDict[token][tag] = 1
                elif tag in rootDict[token]:
                    rootDict[token][tag] += 1
                else:
                    rootDict[token][tag] = 1
                
                #Update the emission tags counter
                
                if tag not in emmitTagCounter:
                    emmitTagCounter[tag] = 1
                else:
                    emmitTagCounter[tag] += 1
                
                #Logic for transition probability dict
                prevTag = currentTag;
                currentTag = tag;
                
                if prevTag not in tagsDict:
                    tagsDict[prevTag][currentTag] = 1
                elif currentTag in tagsDict[prevTag]:
                    tagsDict[prevTag][currentTag] += 1
                else:
                    tagsDict[prevTag][currentTag] = 1
                
                #Update the tags counter
                
                if tag not in tagsCounter:
                    tagsCounter[tag] = 1
                else:
                    tagsCounter[tag] += 1
                
                #maintain a list of tags
                taglist.append(tag)
                
                #add to uniquetags list
                if tag not in uniquetags:       
                    uniquetags.append(tag)
                    
            lst = line[len(line.strip())-2:];
            
            if lst.rstrip('\n') in tagsCounter:
                tagsCounter[lst.rstrip('\n')] -= 1
                
#     print("Unique tags are ::",uniquetags)
#     print(rootDict)
#     print(tagsDict)
#     print(emmitTagCounter)
    
    ####### Transition Probability Calculation #######
    for eachTag in uniquetags:
        for thisTag in uniquetags:
            if thisTag not in tagsDict[eachTag] and thisTag is not 'S0':
                tagsDict[eachTag][thisTag]=0 
      
    totalTags = len(uniquetags) - 1     # one less because S0   
    
    for eachTag in uniquetags:
        for transitionTag in tagsDict[eachTag]:
            tagsDict[eachTag][transitionTag] = round((tagsDict[eachTag][transitionTag] + 1) / (tagsCounter[eachTag] + totalTags),6)
      
    ######## End of Transition Probability Calculation = tagsDict (Fix FF/end of line cases) #######
    
    ######## Emission Probability Calculation #######
    for eachTag in rootDict:
        for innerTag in rootDict[eachTag]:
            rootDict[eachTag][innerTag] = round(rootDict[eachTag][innerTag] / emmitTagCounter[innerTag],6) 
    
    dataDumpDir = {"TransitionProb":tagsDict,"EmissionProb":rootDict}
    
    with open('hmmmodel.txt', 'w',encoding='utf8') as fp:
        json.dump(dataDumpDir, fp, ensure_ascii=False)

if __name__ == "__main__":main()