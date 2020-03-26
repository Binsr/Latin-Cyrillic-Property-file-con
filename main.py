import transliterate as translate
import re
lang= 'sr'

#TEXT that you dont want to translate just put bettween < >

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

def convertLine(line,lang,firstLine):
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
    srStr= TagSafeTranslate(trLine,lang,firstLine)
    # srStr= translate.translit(trLine,lang)
    return formatOutStr(srStr)

def TagSafeTranslate(line,lang,firstLine): # 3- argument odstraniti u nekom trenutku(resava gubljenje \ na kraju reda koji sadrzo = i tag)
    pattern= re.compile(r"<.+?>")
    tagReg= pattern.finditer(line)
    add= ''
    if line[len(line)-1] is '\n': #Trebalo bi prepraviti u nekom trenutku
        add= '\n'

    outStr=''
    iter= 0
    tag= None
    for tag in tagReg:
        outStr+= translate.translit(line[iter:tag.start()],lang)
        outStr+= line[tag.start():tag.end()]
        iter= tag.end()
    if tag is None:
        return translate.translit(line,lang)
    outStr+= translate.translit(line[iter:-1], lang)
    if firstLine:
        outStr+= '\\'
    outStr+= add
    return outStr


infile= open('messages_sr.properties','r')
outFile= open('testout_sr_cir_properties','w')

comFlag= False #Kontrolise razmak izmedju komentara
for line in infile:
    if re.search(r"^#.*", line) is not None:
        outFile.write(line) #Uklanja razmak izmedju 2 linije istog komentara
        comFlag= True
        continue
    pos = re.search(r"[=]", line)
    if pos is not None:
        outFile.write(line[0:pos.end()])
        outFile.write(convertLine(line[pos.end():-1], lang,True))
        outFile.write('\n')
    else:
        outFile.write(convertLine(line,lang,False))

infile.close()
outFile.close()
