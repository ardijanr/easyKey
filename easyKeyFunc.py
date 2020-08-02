



# skrive_filen2.close()
class DictObject:
    def __init__(self, dict_,keylist,skipped_lines=[]):
        self.dict=dict_
        self.keylist=keylist
        self.skipped_lines=skipped_lines


    def regen_keylist(self):
        self.keylist=[]
        for i in range(len(self.dict)):
            self.keylist.append(self.dict[i].key)


class TranslationValue:
    def __init__(self,key,translation):
        self.key=key
        self.translation=translation
        self.ignore=False

    def __str__(self):
        return('"'+self.key+'": "'+self.translation+'",\n' )


def generateDict(filepath):
    fileVar= open(filepath, "r")
    skipped_first=False
    skipping=True
    linje="a"


    # if (linje=="}\n" or linje=="{\n") and skipped_first==False:
    #     print(linje)
    #     linje=fileVar.readline()
    #     print(linje)
    #     skipped_first=True


    dictonairy=[]
    keylist=[]
    skipped_lines=[]
    linje=fileVar.readline()
    while linje!="":
        linje=fileVar.readline()

        if '{\n' in linje: #not working
            skipped_lines.append(linje)
            skipping=True


            while skipping:
                linje=fileVar.readline()
                skipped_lines.append(linje)

                if '},\n' in linje:
                    linje=fileVar.readline()
                    skipping=False
            #print(skipped_lines)


        linje=linje.replace("\n","")
        linje=linje.strip(',')
        lagre=linje.split(':',1)


        if len(lagre)>1:
            lagre[0]=lagre[0].strip()
            lagre[1]=lagre[1].strip()
            lagre[0]=lagre[0].strip('"')
            lagre[1]=lagre[1].strip('"')
            #print(lagre[0]+" "+lagre[1])

            dictonairy.append(TranslationValue(lagre[0],lagre[1]))
            keylist.append(lagre[0])

    fileVar.close()

    return DictObject(dictonairy,keylist,skipped_lines)


def keymissmatch_check(en,alt):
    missing_EN=[]
    missing_ALT=[]

    for i in range(len(en.dict)):
        if (en.dict[i].key in alt.keylist)==False and en.dict[i].ignore==False:
            #print(f"{en.dict[i]} NOT IN ALT DICTIONAIRY")
            missing_EN.append(en.dict[i])


    for i in range(len(alt.dict)):
        if (alt.dict[i].key in en.keylist)==False and alt.dict[i].ignore==False:
            #print(f"{alt.dict[i]} NOT IN EN DICTIONAIRY")
            missing_ALT.append(alt.dict[i])

    return (missing_EN,missing_ALT)

