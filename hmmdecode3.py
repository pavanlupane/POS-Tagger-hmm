import json
import sys
from collections import defaultdict

def main():
    #Load the HMM model
    with open('hmmmodel.txt',encoding='utf-8') as model_file:    
        modelData = json.load(model_file)
        transitionProb = modelData["TransitionProb"]
        emissionProb = modelData["EmissionProb"]
        
        allPossibleTags = transitionProb.keys()     #all possible tags from the model
#         print(allPossibleTags)
        
    fout = open("hmmoutput.txt",'w',encoding='utf-8')    
       
    filename = sys.argv[1]
    with open(filename,'r',encoding='utf-8') as infile:
        for line in infile:
            probability = defaultdict(dict)
            backpointer = defaultdict(dict)
            
            words = line.split()    
            
            T = len(words)
            ##### Start of Viterbi #####
            
            ## Initialization at t=1 ##
            word = words[0]
            
            ##### If the word is seen #####
            if word in emissionProb:
                for eachTag in emissionProb[word]:
                    probability[eachTag][0] = transitionProb['S0'][eachTag] * emissionProb[word][eachTag]
                    backpointer[eachTag][0] = 'S0'
            ##### If the word is unseen #####
            else:
                for eachTag in allPossibleTags:
                    if eachTag != 'S0':
                        probability[eachTag][0] = transitionProb['S0'][eachTag]
                        backpointer[eachTag][0] = 'S0'
                               
            ## Recursion Step T=2 onwards ##
            itr = 1
            while(itr<T):
                word = words[itr]
                
                ### get the tags of previous word - Remember tags may have S0 so cover that case in conditions ###
                if words[itr-1] in emissionProb:
                    previousTagsList = emissionProb[words[itr-1]].keys()
                else:
                    previousTagsList = allPossibleTags

                ##### If the word is seen #####
                if word in emissionProb:
                    for eachTag in emissionProb[word]:
                        maxVal = -1000;
                        currentBackPtr = ''
                        for eachPrevTag in previousTagsList:
                            if eachPrevTag != 'S0':
                                probabilityVal = probability[eachPrevTag][itr-1] * transitionProb[eachPrevTag][eachTag] * emissionProb[word][eachTag]
                                if probabilityVal > maxVal:
                                    maxVal = probabilityVal
                                    currentBackPtr = eachPrevTag
                        
                        probability[eachTag][itr] = maxVal
                        backpointer[eachTag][itr] = currentBackPtr
                        
                ##### If the word is seen #####
                else:
                    for eachTag in allPossibleTags:
                        if eachTag != 'S0':
                            maxVal = -1000;
                            currentBackPtr = '' 
                            for eachPrevTag in previousTagsList:
                                if eachPrevTag != 'S0':
                                    probabilityVal = probability[eachPrevTag][itr-1] * transitionProb[eachPrevTag][eachTag]
                                    if probabilityVal > maxVal:
                                        maxVal = probabilityVal
                                        currentBackPtr = eachPrevTag
                            
                            probability[eachTag][itr] = maxVal
                            backpointer[eachTag][itr] = currentBackPtr
                 
                itr+=1
            
            ##### Termination Step #####
            posTags = list()
            
            maxProbableVal = -10000
            mostProbableState = ''
            for state in allPossibleTags:
                if (itr-1) in probability[state] and probability[state][itr-1] > maxProbableVal:
                    maxProbableVal = probability[state][itr-1]
                    mostProbableState = state

            posTags.append(mostProbableState)
            counter = itr-1;
            prevState = mostProbableState

            while(counter > 0):
                prevState = backpointer[prevState][counter]
                counter -= 1
                posTags.append(prevState)
            taggedLine = ''
            tagsLen = len(posTags)
            
            for word in words:
                taggedLine += word + '/' + posTags[tagsLen-1] + ' '
                tagsLen -= 1
                 
            fout.write(taggedLine.strip() + "\n")
    fout.close()        
        
if __name__ == "__main__":main()