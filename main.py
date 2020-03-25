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
                if i < len(line):
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
infile= open('messages_sr.properties','r')
outFile= open('testout.txt','w')

flag = True
beforHadEq= False
for line in infile:
    pos = re.search(r"[=]", line)
    if pos is not None:
        beforHadEq= True
        flag= False
        outFile.write(line[0:pos.end()])
        outFile.write(tranlateLine(line[pos.end():-1],lang))
        outFile.write('\n')
        if re.search(r'[\\]{1}$',line) is not None:
            flag= True
            beforHadEq= False

    elif flag:
        flag= False
        outFile.write(tranlateLine(line,lang) + '\n')
        if re.search(r'[\\]{1}$',line):
            flag= True
    elif beforHadEq:
        outFile.write('\n')



# line1= r"D\u017Eak" #OK
# line2= "Džak" #OK
# line3= r"D\\u017Eak"
# line4= "žakd"
# line5= r"\u0064\u017ED\\u017E"
# line6= "Sistem \u0107e generisati \u0161ifru i poslati je na va\u0161u \imejl adresu."

# line7= "Odaberi dodatne <br /> menad\u017Eere, ukoliko je \"
# line8= ' Test generator ne mo\u017Ee biti primenjen u granjanju \\'
# print(tranlateLine(line8 ,lang))

infile.close()
outFile.close()
