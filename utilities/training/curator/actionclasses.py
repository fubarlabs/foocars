import os
import sys
import glob
import numpy as np

class deleteAction():
    def __init__(self, delstart, delstop, file_object):
        self.delstart=delstart
        self.delstop=delstop
        self.file_object=file_object
        self.applied=False

    def apply(self):
        self.removed_frames=[]
        for i in range(self.delstop, self.delstart-1, -1):
            #self.removed_frames.append((self.file_object['frames'][i], []))
            r_frame_tuple=(self.file_object['frames'][i], [])
            for k in self.file_object['tag_dict'].keys():
                if self.file_object['frames'][i] in self.file_object['tag_dict'][k]:
                    self.file_object['tag_dict'][k].remove(self.file_object['frames'][i])
                    r_frame_tuple[1].append(k)
            del self.file_object['frames'][i]
            self.removed_frames.append(r_frame_tuple)
        #self.removed_frames.sort()
        self.file_object['applied_stack'].append(self)
        self.applied=True
        self.file_object['len']=len(self.file_object['frames'])
        
    def undo(self):
        for i in self.removed_frames:
            if i[0] not in self.file_object['frames']:
                self.file_object['frames'].append(i[0])
            for t in i[1]:
                self.file_object['tag_dict'][t].append(i[0])
        for k in self.file_object['tag_dict'].keys():
            self.file_object['tag_dict'][k].sort()
        self.removed_frames=[]
        self.file_object['frames'].sort()
        self.file_object['applied_stack'].pop()
        self.applied=False
        self.file_object['len']=len(self.file_object['frames'])
        return self

    def __str__(self):
        if self.applied==True:
            return "Applied delete action: frames {0} to {1}".format(self.delstart, self.delstop)
        else:
            return "Unapplied delete action: frames {0} to {1}".format(self.delstart, self.delstop)


class tagAction():
    def __init__(self, tagstart, tagstop, file_object, tag):
        self.tagstart=tagstart
        self.tagstop=tagstop
        self.file_object=file_object
        self.tag=tag
        self.applied=False

    def apply(self):
        self.tagged_frames=[]
        if self.tag not in self.file_object['tag_dict'].keys():
            self.file_object['tag_dict'][self.tag]=[]
        for i in range(self.tagstart, self.tagstop+1):
            if self.file_object['frames'][i] not in self.file_object['tag_dict'][self.tag]:
                self.tagged_frames.append(self.file_object['frames'][i])
                self.file_object['tag_dict'][self.tag].append(self.file_object['frames'][i])
        self.file_object['tag_dict'][self.tag].sort()
        self.file_object['applied_stack'].append(self)
        self.applied=True

    def undo(self):
        for i in self.tagged_frames:
            if i in self.file_object['tag_dict'][self.tag]:
                self.file_object['tag_dict'][self.tag].remove(i)
        self.tagged_frames=[]
        self.file_object['applied_stack'].pop()
        self.applied=False
        return self

    def __str__(self):
        if self.applied==True:
            return "Applied tag '{0}' action: frames {1} to {2}".format(self.tag, self.tagstart, self.tagstop)
        else:
            return "Unapplied tag '{0}' action: frames {1} to {2}".format(self.tag, self.tagstart, self.tagstop)




