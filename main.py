import transliterate as tr
import re

def isUnicode(chr):
    try:
        chr.encode().decode('unicode_escape')
    except:
        return False
    return True

def tranlateLine(line,lang):
        trLine=''
        i=0
        j= i+1
        doubleChrs = {'D': 'ž', 'L': 'j', 'N': 'j', 'l': 'j', 'd': 'ž', 'n': 'j'}
        while i < len(line):
            chr1= ''
            chr2= ''
            if line[i] == '\\':
                if isUnicode(line[i:i+6]) and line[i] is not line[i+1]:
                    chr1= line[i:i+6].encode().decode('unicode_escape')
                    i+= 5
                    j= i+1
                    if j < len(line):
                        chr2= line[j]

            if j < len(line):
                if line[j] == '\\':
                    if isUnicode(line[j:j+6]):
                        chr2= line[j:j+6].encode().decode('unicode_escape')
                        j+=6
                        if chr1 is '':
                            chr1= line[i]
            if chr1 is '' and chr2 is '':
                chr1= line[i]
                if j < len(line):
                    chr2= line[j]
            #Pokrivene situacije \uxxxChar Char\uxxx \uxxx\uxxx \\ \\uxxx \Char CharChar...
            if chr1 in doubleChrs.keys():
                if doubleChrs[chr1] == chr2:
                    trLine+= tr.translit(chr1+chr2,lang)
                    if i - j < -1:
                        i= j
                    else:
                        i= j+1
                    j=i+1
                    continue
            trLine+= tr.translit(chr1,lang)
            i+=1
            j= i+1
            continue
        return trLine

lang= 'sr'
infile= open('test.txt','r')
outFile= open('testout.txt','w')

for line in infile:
    pos = re.search(r"[=]", line)
    if pos is not None:
        outFile.write(line[0:pos.end()])
        outFile.write(tranlateLine(line[pos.end():-1],lang))
    else:
        outFile.write(line)
    outFile.write('\n')




# line1= r"D\u017Eak" #OK
# line2= "Džak" #OK
# line3= r"D\\u017Eak"
# line4= "žakd"
# line5= r"D\\u017ED\\u017E"
# print(tranlateLine(line5 ,lang))

infile.close()
outFile.close()
