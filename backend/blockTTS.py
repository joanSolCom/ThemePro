
from embeddings import Embeddings


class BlockTTS():

    def __init__(self, corefs, iT, model, sents):
        self.corefs = corefs
        print(corefs)
        self.iT = iT
        self.embeddings = Embeddings(model)
        self.sents = sents
        self.them = self.getThem(iT.levels)
        self.maxchars = 420
        self.thresh = 0.6
        self.buildBlocks()

    
    def getThem(self, levels):

        thems = []

        for sentIdx, lvl in enumerate(levels):
            them = lvl[0]
            dthem = {}
            for start, end, themLabel in them:
                substr = " ".join(self.sents[sentIdx][start-1:end])
                dthem[themLabel] = substr
            
            dthem["fullsent"] = " ".join(self.sents[sentIdx])
            thems.append(dthem)

        return thems


    def check_corefs(self, lastThem, currentThem):
        
        for corefList in self.corefs:
            foundTc = False
            foundTl = False
            foundRl = False
            for corefElem in corefList:
                if "T1" in lastThem:
                    if corefElem in lastThem["T1"].lower():
                        foundTl = True
                        print("found in last theme", corefElem)
                if "T1" in currentThem:
                    if corefElem in currentThem["T1"].lower():
                        foundTc = True
                        print("found in current theme", corefElem)
                if "R1" in lastThem:
                    if corefElem in lastThem["R1"].lower():
                        fountRl = True
                        print("found in last rheme", corefElem)

            if foundTl and foundTc:
                return True
            elif foundTc and foundRl:
                return True

        return False

    def check_sim(self, lastThem, currentThem):
        
        vectorTl = None
        vectorTc = None
        vectorRl = None
        if "T1" in lastThem:
            tokens = lastThem["T1"].split()
            if len(tokens) > 1:
                vectorTl = self.embeddings.getMsgVector(lastThem["T1"])
                
        if "T1" in currentThem:
            tokens = currentThem["T1"].split()
            if len(tokens) > 1:
                vectorTc = self.embeddings.getMsgVector(currentThem["T1"])
                
        if "R1" in lastThem:
            tokens = lastThem["R1"].split()
            if len(tokens) > 1:
                vectorRl = self.embeddings.getMsgVector(lastThem["R1"])
                
                
        if vectorTc and vectorTl:
            sim = self.embeddings.distance(vectorTc, vectorTl)
            print(currentThem["T1"],"|||",lastThem["T1"], sim)
            if sim < self.thresh:
                return True

        if vectorTc and vectorRl:
            sim = self.embeddings.distance(vectorTc, vectorRl)
            print(currentThem["T1"],"|||", lastThem["R1"], sim)
            if sim < self.thresh:
                return True
        
        return False

    def string_match(self, lastThem, currentThem):
        if "T1" in currentThem:
            if currentThem["T1"].lower() in lastThem["fullsent"].lower():
                return True

        return False

    def need_to_merge(self, lastThem, currentThem):
        if self.string_match(lastThem, currentThem):
            return True
        elif self.check_corefs(lastThem, currentThem):
            return True
        elif self.check_sim(lastThem, currentThem):
            return True
        else:
            return False


    def buildBlocks(self):
        length = 0
        blocks = []
        currentBlock = []
        lastThem = None

        for themDict in self.them:
            print("currentBlock", currentBlock)
            print("blocks",blocks)

            if lastThem:
                if len(themDict["fullsent"]) >= self.maxchars:
                    print("sentence is too large, we skip this one")
                
                else:
                    if length + len(themDict["fullsent"]) < self.maxchars:
                        
                        if self.need_to_merge(lastThem, themDict):
                            print("-------------we merge------------")
                            currentBlock.append(themDict["fullsent"])
                            length = length + len(themDict["fullsent"])
                        
                        else:
                            print("---------creating new block---------")
                            if currentBlock:
                                blocks.append(currentBlock)
                                currentBlock = []
            
                            currentBlock.append(themDict["fullsent"])
                            length = len(themDict["fullsent"])

                    else:
                        print("char limit reached. current size: ", length, "with new sent", length + len(themDict["fullsent"]))
                        blocks.append(currentBlock)
                        currentBlock = []
                        currentBlock.append(themDict["fullsent"])
                        length = len(themDict["fullsent"])
            else:
                currentBlock.append(themDict["fullsent"])
                length = length + len(themDict["fullsent"])

            lastThem = themDict
        
        blocks.append(currentBlock)
        print(blocks)
        self.blocks = blocks



