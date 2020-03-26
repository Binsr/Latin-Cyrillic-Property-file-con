import transliterate as tr
import re

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

lang= 'sr'
infile= open('messages_sr.properties','r')
outFile= open('testout_sr_cir_properties','w')

flag = True
beforHadEq= False
for line in infile:
    pos = re.search(r"[=]", line)
    if pos is not None:
        beforHadEq= True
        flag= False
        outFile.write(line[0:pos.end()])
        outFile.write(str((translateLine(line[pos.end():-1],lang)).encode('unicode_escape')))
        outFile.write('\n')
        if re.search(r'[\\]{1}$',line) is not None:
            flag= True
            beforHadEq= False

    elif flag:
        flag= False
        outFile.write(str((translateLine(line,lang)).encode('unicode_escape')))
        outFile.write('\n')
        if re.search(r'[\\]{1}$',line):
            flag= True
    elif beforHadEq:
        outFile.write('\n')

infile.close()
outFile.close()
