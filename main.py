import transliterate as translate
import re
lang= 'sr'

def isUnicode(chr):
    try:
        chr.encode().decode('unicode_escape')
    except:
        return False
    return True

def formatOutStr(stri):
    outStr= ''
    i= 0
    while i < len(stri):
        chr= stri[i]
        if chr is '\n' or chr is '\t' or chr is '\\':
            outStr+= chr
            i+=1
            continue
        chr= str(chr.encode('unicode_escape'))
        bsPos= re.search(r"[\\]", chr)
        if bsPos is not None:
            if chr[bsPos.end()+1] is not "\\":
                outStr+= chr[bsPos.end():-1]
            else:
                outStr+= '\\'
        else:
            aPos= re.search(r"[']",chr)
            outStr+= chr[aPos.end():aPos.end()+1]
        i+=1
    return outStr


def convertLine(line,lang):
    trLine= ''
    i= 0
    while i < len(line):
        if line[i] == '\\' and i+6 < len(line):
            if isUnicode(line[i:i+6]) and line[i] is not line[i+1]:
                trLine+= line[i:i+6].encode().decode('unicode_escape')
                i+= 6
                continue

        trLine+= line[i]
        i+=1
    srStr= translate.translit(trLine,lang)
    return formatOutStr(srStr)

infile= open('messages_sr.properties','r')
outFile= open('testout_sr_cir_properties','w')

comFlag= False #Kontrolise razmak izmedju redova
for line in infile:
    print(str(line.encode()))
    if re.search(r"^#.*", line) is not None:
        outFile.write(line) #Uklanja razmak izmedju 2 linije istog komentara
        comFlag= True
        continue
    pos = re.search(r"[=]", line)
    if pos is not None:
        outFile.write(line[0:pos.end()])
        outFile.write(convertLine(line[pos.end():-1], lang))
        outFile.write('\n')
    else:
        outFile.write(convertLine(line,lang))

infile.close()
outFile.close()
