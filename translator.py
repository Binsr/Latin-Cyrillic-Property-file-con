import transliterate as translate
import re
#NE PROSLEDJUJ JEZIK PREPRAVI

class Translate:

    def __init__(self,fileIn, fileOut, language):
        self.fileIn= fileIn
        self.fileOut= fileOut
        self.language= language

    #TEXT in file that you dont want to translate just put bettween < >

    def isUnicode(self,chr):
        try:
            chr.encode().decode('unicode_escape')
        except:
            return False
        return True

    def formatOutStr(self,stri):
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

    def convertLine(self,line):
        convLine= ''
        i= 0
        while i < len(line):
            if line[i] == '\\' and i+6 < len(line):
                if self.isUnicode(line[i:i+6]) and line[i] is not line[i+1]:
                    convLine+= line[i:i+6].encode().decode('unicode_escape')
                    i+= 6
                    continue

            convLine+= line[i]
            i+=1
        return convLine
        # srStr= self.TagSafeTranslate(trLine,command,firstLine)
        # return self.formatOutStr(srStr)

    def tagSafeTranslate(self,line,isFirstLine): # 3- argument odstraniti u nekom trenutku(resava gubljenje \ na kraju reda koji sadrzo = i tag)
        pattern= re.compile(r"<.+?>")
        tagReg= pattern.finditer(line)
        add= ''
        if line[len(line)-1] is '\n': #Trebalo bi prepraviti u nekom trenutku
            add= '\n'

        outStr=''
        iter= 0
        tag= None
        for tag in tagReg:
            outStr+= translate.translit(line[iter:tag.start()], 'sr')
            outStr+= line[tag.start():tag.end()]
            iter= tag.end()
        if tag is None:
            return translate.translit(line, 'sr')
        outStr+= translate.translit(line[iter:-1], 'sr')
        if isFirstLine:
            outStr+= '\\'
        outStr+= add
        return outStr

    def lineTranslator(self,line,command,isFirstLine):
        convLine= self.convertLine(line)
        transLine= convLine

        if command == "Latin-to-Cirilic":
            transLine= self.tagSafeTranslate(transLine, isFirstLine)

        if command == "Translate-to-English":
            transLine= "English"


        return self.formatOutStr(transLine)


    def translate(self,command):
        infile= open(self.fileIn, 'r')
        outfile= open(self.fileOut, 'w')
        for line in infile:
            if re.search(r"^#.*", line) is not None:
                outfile.write(line) #Uklanja razmak izmedju 2 linije istog komentara
                continue
            pos = re.search(r"[=]", line)
            if pos is not None:
                outfile.write(line[0:pos.end()])
                outfile.write(self.lineTranslator(line[pos.end():-1], command, True))
                outfile.write('\n')
            else:
                outfile.write(self.lineTranslator(line,command, False))

        infile.close()
        outfile.close()