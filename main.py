import transliterate as tr
import re
lang= 'sr'

def isUnicode(chr):
    try:
        chr.encode().decode('unicode_escape')
    except:
        return False
    return True

def translateLine(line,lang):
    trLine= ''
    i= 0
    while i < len(line):
        if line[i] == '\\' and i < len(line):
            if isUnicode(line[i:i+6]) and line[i] is not line[i+1]:
                trLine+= line[i:i+6].encode().decode('unicode_escape')
                i+= 6
                continue

        trLine+= line[i]
        i+=1
    return tr.translit(trLine,lang)


infile= open('messages_sr.properties','r')
outFile= open('testout_sr_cir_properties','w')

flag= False #Kontrolise razmak izmedju redova
for line in infile:
    pos = re.search(r"[=]",line)
    if re.search(r"^#.*",line) is not None:
        outFile.write(translateLine(line,lang)) #Uklanja razmak izmedju 2 linije istog komentara
        comFlag= True
        continue

    if pos is not None:
        flag= True
        outFile.write(line[0:pos.end()])
        outFile.write(translateLine(line[pos.end():-1],lang) + '\n')
    elif re.search(r"^\s*$",line) is not None and len(line) > 0:
        if flag:
            outFile.write('\n')
        flag= False
        continue
    else:
        outFile.write(translateLine(line,lang)+ '\n')
        flag= False

    # if re.search(r'[\\]$',line) is None:
    #     outFile.write('\n')

infile.close()
outFile.close()
