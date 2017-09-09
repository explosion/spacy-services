from __future__ import unicode_literals

import os

pos_dictionnary = {'ADJ':'a','ADV':'r','NOUN':'n','SYM':'v', 'AUX':'v'}
VerbesTernesList = ['être', 'faire', 'avoir']

from .FrenchLefffLemmatizer import FrenchLefffLemmatizer

'''
create the lemmztizer for french
'''
Lemmatizer = FrenchLefffLemmatizer.FrenchLefffLemmatizer(os.path.dirname(__file__)+'/FrenchLefffLemmatizer/lefff-3.4.mlex/lefff-3.4.mlex',os.path.dirname(__file__)+'/FrenchLefffLemmatizer/lefff-3.4.mlex/lefff-3.4-addition.mlex')

class Mot:
    pos_dictionnary = {'ADJ':'a','ADV':'r','NOUN':'n','SYM':'v', 'AUX':'v'}


    def __init__(self, word):
        self.text = word.text
        self.tag = word.tag
        self.tag_ = word.tag_
        self.pos = word.pos
        self.pos_ = word.pos_
        self.i = word.i
        self.idx = word.idx

        if word.pos_ in pos_dictionnary:
            self.lemma_ = Lemmatizer.lemmatize(word.text,pos_dictionnary[word.pos_])
        else:
            self.lemma_ = word.text

def VerbesTernes(doc):
    '''
    return "verbes ternes" (weak terms) of the text. In french.
    parameter:
      - doc : a doc item from spacy.

    it returns the list of weak terms:
      (text of the word, lemma, position of the 1rst char, pos of the last char.)
    '''
    VerbeList = []

    for word in doc:
        mot = Mot(word)
        '''
        note: the POS in spacy 1.9 is not working correctly in french, for
        verbs. Instead of 'VERB', they are tagged 'SYM'.
        '''
        if mot.pos_ == 'SYM' and mot.lemma_ in VerbesTernesList:
            wordstart = mot.idx
            wordend = wordstart + len(mot.text)
            VerbeList.append((mot.text, mot.lemma_, wordstart,wordend))

    return VerbeList

def GetSynonyms(word, number = 10):
    '''
    retrieve synonyms of words (from spaCy model)
    parameter:
     - word : a word item from spaCy.
     - number : the number of synonyms to retrieve.
    it returns a list of synonyms.
    '''
    queries = [w for w in word.vocab if w.is_lower == word.is_lower and w.prob >= -15]
    by_similarity = sorted(queries, key=lambda w: word.similarity(w), reverse=True)
    return by_similarity[:number]

def Repetitions(doc,espace=20, synonyms=False):
    '''
    return the list of repetitions in the text. In french.
    parameter:
      - doc : a doc item from spacy.
      - espace : the number of words between two identical lemmas to be tagged
      as repetition.

    it returns the list of repetitions:
      (lemma of the word, pos of the word, pos of the 1rst char, pos of the last char.)
    '''
    WordList=[]
    RepetitionsList=[]
    TaggedRepetitionsList=[]

    print('repetitions')
    for word in doc:
        mot = Mot(word)
        if mot.pos_ in ['ADJ', 'NOUN', 'SYM']:
            syn = []
            if synonyms == True:
                syn = [w.lower_ for w in GetSynonyms(word)]
            #add list of words: lemma, position of the word, starting char, ending char, synonyms.
            WordList.append((mot.lemma_, mot.i, mot.idx, mot.idx + len(mot.text), syn))

    for i in range(len(WordList)):
        for j in range(len(WordList)-i-1):
            if WordList[i][0] == WordList[j+i+1][0]:
                RepetitionsList.append((WordList[i][0],WordList[i][1],WordList[i][2],WordList[i][3],WordList[j+i+1][1],WordList[j+i+1][2],WordList[j+i+1][3],WordList[i][4]))

    for rep in RepetitionsList:
        if rep[4]-rep[1]<espace:
            TaggedRepetitionsList.append((rep[0],rep[2],rep[3],rep[7]))
            TaggedRepetitionsList.append((rep[0],rep[5],rep[6],rep[7]))

    return TaggedRepetitionsList

def Passive(doc):
    '''
    return the list of passive verbs in the text. In french.
    parameter:
      - doc : a doc item from spacy.

    it returns the list of repetitions:
      (text of the verb, pos of the 1rst char, pos of the last char.)
    '''
    PassiveList = []

    participe = passive = False
    startchar = endchar = 0
    startword = endword = doc[0]

    for word in doc:
        mot = Mot(word)

        if mot.lemma_ == "être" and mot.pos_ == "AUX":
            participe = True
            startchar = mot.idx
            startword = mot.i

        elif participe == True and mot.pos_ == "SYM":
            endchar = mot.idx + len(mot.text)
            endword = mot.i
            PassiveList.append((doc.text[startchar:endchar],startchar,endchar))
            participe = False

        else:
            participe = False


    return PassiveList

def BigSentences(doc, size=25):
    '''
    return the list of big phrases in the text. In french.
    parameter:
      - doc : a doc item from spacy.
      - size : number of words in the sentence to be tagged as big.

    it returns the list of big phrase:
      (text of the sentence, pos of the 1rst char, pos of the last char.)
    '''
    PointList = [(0,-1)]
    BigSentencesList = []
    for word in doc:
        mot = Mot(word)
        if mot.text in [".", "!", "?"]:
            PointList.append((mot.i, mot.idx+1))

    for i in range(len(PointList)-1):
        if PointList[i+1][0]-PointList[i][0]>size:
            startchar = PointList[i][1]+1
            endchar = PointList[i+1][1]
            BigSentencesList.append((doc.text[startchar:endchar],startchar,endchar))

    return BigSentencesList

def SansVerbe(doc):
    '''
    return the list of phrases without verbs in the text. In french.
    parameter:
      - doc : a doc item from spacy.

    it returns the list of phrases without verbs:
      (text of the sentence, pos of the 1rst char, pos of the last char.)
    '''
    SentencesList = []
    SansVerbeList = []

    phrase = []

    PointList = [(0,-1)]
    BigSentencesList = []
    for word in doc:
        mot = Mot(word)
        if mot.text not in [".", "?", "!"]:
            phrase.append((mot.text, mot.idx, mot.pos_))
        else:
            phrase.append((mot.text, mot.idx, mot.pos_))
            SentencesList.append(phrase)
            phrase = []

    for sent in SentencesList:
        sansverbe=True
        for word in sent:
            if word[2] in ["SYM", 'AUX']:
                sansverbe = False
        if sansverbe == True:
            startchar = sent[0][1]
            endchar = sent[-1][1]+1
            SansVerbeList.append((doc.text[startchar:endchar],startchar,endchar))
        sansverbe = False

    return SansVerbeList

'''
commented below. Uncomment to call Parse and Entities classes.
'''
# class Parse(object):
#     def __init__(self, nlp, text, collapse_punctuation, collapse_phrases):
#         self.doc = nlp(text)
#         if collapse_punctuation:
#             spans = []
#             for word in self.doc[:-1]:
#                 if word.is_punct:
#                     continue
#                 if not word.nbor(1).is_punct:
#                     continue
#                 start = word.i
#                 end = word.i + 1
#                 while end < len(self.doc) and self.doc[end].is_punct:
#                     end += 1
#                 span = self.doc[start : end]
#                 spans.append(
#                     (span.start_char, span.end_char, word.tag_, word.lemma_, word.ent_type_)
#                 )
#             for span_props in spans:
#                 self.doc.merge(*span_props)
#
#         if collapse_phrases:
#             for np in list(self.doc.noun_chunks):
#                 np.merge(np.root.tag_, np.root.lemma_, np.root.ent_type_)
#
#     def to_json(self):
#         words = [{'text': w.text, 'tag': w.tag_} for w in self.doc]
#         arcs = []
#         for word in self.doc:
#             if word.i < word.head.i:
#                 arcs.append(
#                     {
#                         'start': word.i,
#                         'end': word.head.i,
#                         'label': word.dep_,
#                         'dir': 'left'
#                     })
#             elif word.i > word.head.i:
#                 arcs.append(
#                     {
#                         'start': word.head.i,
#                         'end': word.i,
#                         'label': word.dep_,
#                         'dir': 'right'
#                     })
#         return {'words': words, 'arcs': arcs}
#
# class Entities(object):
#     def __init__(self, nlp, text):
#         self.doc = nlp(text)
#
#     def to_json(self):
#         return [{'start': ent.start_char, 'end': ent.end_char, 'type': ent.label_}
#                 for ent in self.doc.ents]

class Annotations(object):
    def __init__(self, nlp, text):
        self.doc = nlp(text)
        self.BigSentencesList = BigSentences(self.doc)
        self.VerbesTernesList = VerbesTernes(self.doc)
        self.PassiveList = Passive(self.doc)
        self.RepetitionsList = Repetitions(self.doc, synonyms = False)
        self.SansVerbeList = SansVerbe(self.doc)

    def getStartKey(self, item):
        return item['start']

    def to_json(self):
        returnjson = []
        #for bigsent in self.BigSentencesList:
        #    returnjson.append({'start': bigsent[1], 'end': bigsent[2], 'type': 'longuephrase'})
        for verbe in self.VerbesTernesList:
            returnjson.append({'start': verbe[2], 'end': verbe[3], 'type': 'terne'})
        for passive in self.PassiveList:
            returnjson.append({'start': passive[1], 'end': passive[2], 'type': 'passive'})
        for repetition in self.RepetitionsList:
            returnjson.append({'start': repetition[1], 'end': repetition[2], 'synonyms': repetition[3],'type': 'repetition'})
        for sansverbe in self.SansVerbeList:
            returnjson.append({'start': sansverbe[1], 'end': sansverbe[2], 'type': 'sansverbe'})
        returnjson = sorted(returnjson, key = self.getStartKey)

        #remove duplicates in returnjson
        cleanlist = []
        for i in returnjson:
            if i not in cleanlist:
                cleanlist.append(i)
        returnjson = cleanlist

        print(returnjson)
        return returnjson
