import matplotlib.pyplot as plt
import nltk
def plotgraph(tag_list):
    list =tag_list
    print list
    tagstring=' '.join(list)
    print tagstring
    fobj=open('tag.txt','w')
    fobj.write(tagstring)
    fobj.close()
    wordlist = tagstring.split()
    wordfreq = []
    for w in wordlist:
        wordfreq.append(wordlist.count(w))

#print("String\n" + wordstring +"\n")
#print("List\n" + str(wordlist) + "\n")
#print("Frequencies\n" + str(wordfreq) + "\n")
#print("Pairs\n" + str(zip(wordlist, wordfreq)))
    freq=zip(wordlist,wordfreq)
    print 'freq list',freq

    words = [('a',3),('b',4)]
    wordsdict = {}
    for w in freq:
        wordsdict[w[0]]=w[1]

    plt.bar(range(len(wordsdict)), wordsdict.values(), align='center')
    plt.xticks(range(len(wordsdict)), wordsdict.keys())

    plt.show()