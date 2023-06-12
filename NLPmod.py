import pandas as pd
import numpy as np
from nltk.tokenize import word_tokenize
from nltk import pos_tag
import heapq
import re
import upsetplot


def wordnetPOS(pos): # translates full description of POS to necessary chunk
    if pos.startswith('J'): # letter J at start for adjective
        return 'a'
    elif pos.startswith('V'): # Letter V at start for verb
        return 'v'
    elif pos.startswith('N'): # Letter N at start for noun
        return 'n'
    elif pos.startswith('R'): # Letter R at start for adverb
        return 'r'
    elif pos.startswith('S'):
        return 's'
    else: # default all other words to noun.
        return 'n'

def tokenizerREG(state,lemmatizer,stopset = {}) : # function for removing unnecessary text elements.
    state = str(state).lower() # remove all capitalization
    state = re.sub(r'\W',' ',state) # removes punctuation
    state = re.sub(r'\s+',' ',state) # removes excess spacing  
    tokens = word_tokenize(state) # tokenize each sentence into word lists
    ltokens = [lemmatizer.lemmatize(token) for token in tokens if token] # lemmatize tokens
    sltokens = [token for token in ltokens if token not in stopset] # discard pointless stopwords
    return sltokens    

def tokenizerPOS(state,lemmatizer,stopset = {}) : # function for removing unnecessary text elements.
    state = str(state).lower() # remove all capitalization
    state = re.sub(r'\W',' ',state) # removes punctuation
    state = re.sub(r'\s+',' ',state) # removes excess spacing  
    tokens = word_tokenize(state) # tokenize each sentence into word lists
    taggedTokens = pos_tag(tokens) # add the part of speech portion
    ltokens = [lemmatizer.lemmatize(token, wordnetPOS(pos)) for token,pos in taggedTokens if token] # lemmatize tokens
    sltokens = [token for token in ltokens if token not in stopset] # discard pointless stopwords
    return sltokens

def negatList() : # returns list of negative words
    return ["hadn't", "t", "didn't", "hadn", "shouldn", "doesn't", "weren't", "mustn't", "couldn't", 
         "won't", "don", "haven't", "aren't", "wouldn", "shan't", "mustn", "haven", "no", "ain", "shouldn't", 
         "nor", "hasn't", "don't", "hasn", "shan", "didn", "mightn't", "wasn't", "isn't", "wasn", "won", "doesn", 
         "needn't", "not", "mightn", "couldn", "wouldn't", "needn", "aren"]


def ngramsappend(tokenlist, gramsize, omit): # this function takes a list of tokens and returns it with ngrams appended.
    ngram = [] # begin with an empty list 
    for n in gramsize :
        scrangram = zip(*[tokenlist[i:] for i in range(n)]) # create an iterable of tuples that are made of adjacent word pairs
        ngram += [" ".join(grampieces) for grampieces in scrangram] # convert tuple into a specialized list item built using
    if omit : # are we replacing the original tokens?
        return ngram # return just the new list.
    else : # TYPICALLY, we would want both. 
        return tokenlist + ngram # return the concatenated list.


def wordfreq(tlist) : # generates a word frequency table from a list of tokens.
    freqtab = {} # begin with an empty dictionary
    for tokens in tlist : # look at each list of tokens belonging to your list
        for token in tokens : # Look at each component token
            if token not in freqtab.keys() : # if it is not YET part of the frequency table
                freqtab[token] = 0 # add it in and point it towards 0.
            freqtab[token] += 1 # increment frequency of word by 1.
    return freqtab # return dictionary of word frequencies


def repbank(freqtab,thresh=1) : # using a frequency table, partitions words into common/rare.
    comflag = [freqtab[word] > thresh for word in freqtab] # flag words that appear more than 'thresh' times
    comsize = np.sum(comflag) # sum over all flags raised for size.
    comwords = heapq.nlargest(comsize,freqtab,key=freqtab.get) # gather all words that do so
    rarwords = [word for word in freqtab if word not in comwords] # all other words are rare
    return comwords, rarwords # return the bank of rare and common words as separate lists.


def vectorizer(tokens, comwords) : # converts list of tokens in to fixed length vector 
    vector = [int(word in tokens) for word in comwords] # 1 (bool true) on certain entries, else 0
    return vector # return completed vector.


def pab(ldamodel,size = 5) :
    topics = ldamodel.print_topics(num_words = size)
    for topic in topics : 
        print(topic)


def dmanip1(ldamodel, comm, corpus) : # generates specialized topic dataframe from LDAmodel
    labs = {"topic":[], "% cont":[]} # pre-make some new labels for another dataframe
    dftopics = pd.DataFrame(labs) # initialize the dataframe using the labels.

    for i, row_list in enumerate(ldamodel[corpus]): # enumerate over the corpus
        row = row_list[0] if ldamodel.per_word_topics else row_list # Adjust based on boolean variable that is always false
        row = sorted(row, key=lambda x: (x[1]), reverse=True) # Sort topics in row based on weighting percentages
        for j, (topnum, proptop) in enumerate(row): # Get the Dominant topic, Perc Contribution for each document
            if j == 0:  # => dominant topic
                scrarow = pd.DataFrame({
                    "topic" : [int(topnum)], # identify topic number
                    "% cont" : [round(proptop,4)] # identify percent contribution
                })
                dftopics = pd.concat([dftopics,scrarow], axis = 0, ignore_index=True) # concatenate df together
            else: # are we looking at some other topic
                break # get out of there!
    dftopics['raw'] = comm # create another column for initial comments
    return dftopics # return completed dataframe 


def dmanip2(df, notops) : 
    topicsort = [] # empty list for topics
    labs = {"% cont":[], "raw":[]} # labels for iterated dataframes
    for i in range(notops) :
        topicsort.append(pd.DataFrame(labs))

    for i, row in df.iterrows() :
        scrarow = pd.DataFrame({
            "raw" : [row["raw"]], # re-input the initial text
            "% cont" : [row["% cont"]], # identify percent contribution
        })
        topicsort[int(row["topic"])] = pd.concat([topicsort[int(row["topic"])],scrarow], ignore_index = True)

    for i in range(notops) :
        topicsort[i].sort_values("% cont", ascending = False, inplace = True)
        print(f"\n{topicsort[i]}\n")        
    return topicsort