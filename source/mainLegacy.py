from parse import parse
from parse import PDFtoTXT
#from vectorize import vectorizePDFs
#from vectorize import machine
from RD import findRelevant

import os







#Write PDFS into CSV format
with open("../output/Full/%s.csv" % x, "w", encoding='utf8', errors='ignore') as f:
    f.write('ClassID,Desc\n')
    #replace d with x if wanting reduce format
    for key in d:
            f.write('%s,"%s"\n'%(key,d[key]))
    d.clear()




#Basic Relevancy Discover
# x = findRelevant(d)
# with open("../output/Reduced%s.csv" % school, "w", encoding='utf8', errors='ignore') as f:
#     f.write('ClassID,Desc\n')
#     #replace d with x if wanting reduce format
#     for key in x:
#         try:
#             f.write('%s,"%s"\n'%(key,x[key]))
#         except:
#             print(key)
