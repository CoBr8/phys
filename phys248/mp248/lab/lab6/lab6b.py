import os as os
import collections as co
import operator as op
import sys
from termcolor import colored
def function(DN):
    fts=co.defaultdict(int)
    for dirName,subdirList, fileList in os.walk(DN):
        ft=[]
        for FN in fileList:
            fn=FN.split('.')
            if len(fn)>1:
                ft.append('.%s'%fn[-1])
            else:
                ft.append('None')
        for f in ft:
            fts['%s'%f]+=1
    return list(sorted(fts.items(),key=op.itemgetter(1)))
print('the ten most common filetypes are: ')
for i in function(str(sys.argv[1]))[:-20:-1]:
    print(colored(i[0],'green'),colored(i[1],'red'))
    