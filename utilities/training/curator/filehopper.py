class filehopper:
    def __init__(self, filelist, filedict):
        self.filelist=filelist
        self.filedict=filedict
        #assume start from first frame in dataset
        self.index=0
        self.fileindex=0
        self.activefile=self.filelist[self.fileindex] #gets filename
        self.numfiles=len(filelist)

    def getState(self):
        return (self.index, self.activefile)

    def setIndex(self, newIndex, newFileIndex=None):
        if newFileIndex==None:
            assert(newIndex<self.filedict[self.activefile]['len'])
            self.index=newIndex
        else:
            assert(newIndex<self.filedict[self.filelist[newFileIndex]]['len'])
            self.fileindex=newFileIndex
            self.activefile=self.filelist[self.fileindex]
            self.index=newIndex

    def next(self, continuous):
        if self.index+1==self.filedict[self.activefile]['len'] and continuous==True:
            fileoffset=1
            while self.filedict[self.filelist[(self.fileindex+fileoffset)%self.numfiles]]['len']==0:
                fileoffset=fileoffset+1
            self.fileindex=(self.fileindex+fileoffset)%self.numfiles
            self.activefile=self.filelist[self.fileindex]
            self.index=0
        else:
            self.index=(self.index+1)%self.filedict[self.activefile]['len']

    def prev(self, continuous):
        if self.index-1==-1 and continuous==True:
            fileoffset=1
            while self.filedict[self.filelist[(self.fileindex-fileoffset)%self.numfiles]]['len']==0:
                fileoffset=fileoffset+1
            self.fileindex=(self.fileindex-fileoffset)%self.numfiles
            self.activefile=self.filelist[self.fileindex]
            self.index=self.filedict[self.activefile]['len']-1
        else:
            self.index=(self.index-1)%self.filedict[self.activefile]['len']

    def jumpAhead(self, number, continuous):
        for i in range(0, number):
            self.next(continuous)

    def jumpBack(self, number, continuous):
        for i in range(0, number):
            self.prev(continuous)
'''
nlists=10
listdict={}
listlist=[]

for i in range(0, nlists):
    listname="list_{0:03d}".format(i)
    listlist.append(listname)
    listlen=int(30*random.random())
    listdict[listname]=dict([ ("len", listlen), ('data', [n for n in range(0, listlen)])])
listlist.sort()

for l in sorted(listdict.keys()):
    print("list {0}:".format(l))
    print("\tlength: {0}".format(listdict[l]["len"]))
    print("\tdata:", listdict[l]["data"])

fh=filehopper(listlist, listdict)
stride=10

for i in range(0, 40):
    fh.jumpAhead(stride, False)
    idx, activefile=fh.getState()
    print("{0} : {1}".format(activefile, idx))
'''
