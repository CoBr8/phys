
import sys
import requests as req
import collections as co
import string
rPun = string.punctuation.replace("'", '')
import operator as op

def countWords(strname):
    ## empty defaultdict
    ct = co.defaultdict(int)
    ## will be a list of every object in strname
    ## once split along the spaces
    strname = strname.replace('\r\n', ' ')
    strname = strname.lower()
    for c in rPun:
        strname = strname.replace(c, ' ')
    ln = strname.split(' ')
    for w in ln:
        if w!='':
            ct[w]+=1
    return(ct)

def countWPW(wpstring):
    romstr = req.get(wpstring).content.decode("utf-8")
    return(countWords(romstr))

## argv variable list of all the strings on the command line
out = countWPW(sys.argv[1])
out2 = sorted(out.items(), key=op.itemgetter(1))
print(out2[-10:])
