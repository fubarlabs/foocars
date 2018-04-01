from PyQt4.QtCore import *
from PyQt4.QtGui import *


class fileSettingsDialog(QDialog):
    
    def __init__(self, filename, filedict, parent=None):
        super(fileSettingsDialog, self).__init__(parent)
        self.filedict=filedict
        self.filename=filename
        self.savename_edit=QLineEdit(filedict[filename]["save_name"])
        self.savename_label=QLabel("Save File Name:")
        self.save_checkbox=QCheckBox("Save File?")
        if filedict[filename]['save_toggle']==True:
            self.save_checkbox.setCheckState(Qt.Checked)
        self.appliedactionlist=QListWidget()
        self.unappliedactionlist=QListWidget()
        for a in filedict[filename]['applied_stack']:
            self.appliedactionlist.addItem(a.__str__())
        self.undoButton=QPushButton("undo")
        self.redoButton=QPushButton("redo")
        self.buttonbox=QDialogButtonBox(QDialogButtonBox.Ok|QDialogButtonBox.Cancel)
        layout=QGridLayout()
        layout.addWidget(self.appliedactionlist, 0, 0)
        layout.addWidget(self.unappliedactionlist, 0, 1)
        layout.addWidget(self.undoButton, 1, 0)
        layout.addWidget(self.redoButton, 1, 1)
        layout.addWidget(self.savename_label, 2, 1)
        layout.addWidget(self.savename_edit, 2, 2)
        layout.addWidget(self.save_checkbox, 3, 2)
        layout.addWidget(self.buttonbox, 4, 2)
        self.setLayout(layout)
        self.connect(self.buttonbox, SIGNAL("accepted()"), self, SLOT("accept()"))
        self.connect(self.buttonbox, SIGNAL("rejected()"), self, SLOT("reject()"))
        self.connect(self.undoButton, SIGNAL("clicked()"), self.undo)
        self.connect(self.redoButton, SIGNAL("clicked()"), self.redo)
        self.num_undos=0

    def undo(self):
        if self.num_undos<len(self.filedict[self.filename]['applied_stack']):
            self.num_undos=self.num_undos+1
            item=self.appliedactionlist.takeItem(0)
            self.unappliedactionlist.addItem(item)

    def redo(self):
        if self.num_undos>0:
            self.num_undos=self.num_undos-1
            item=self.unappliedactionlist.takeItem(self.unappliedactionlist.count()-1)
            self.appliedactionlist.insertItem(0, item)
        
    
    def accept(self):
        self.savename=str(self.savename_edit.text())
        if self.savename[0:4]!='imgs':
            QMessageBox.warning(self, "Bad Save Name", "The saved file name must begin with 'imgs'.")
            return 
        self.info=dict([("save_toggle", self.save_checkbox.isChecked()), ("savename",  self.savename),
            ("undo_number", self.num_undos)])
        QDialog.accept(self)

    def getInfo(self):
        return self.info



