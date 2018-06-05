import os
import sys
import glob
import numpy as np
import scipy.misc
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from actionclasses import deleteAction
from actionclasses import tagAction
from filehopper import filehopper
from filesettings import fileSettingsDialog

#Please don't read this code, it's terrible. I'll try to fix it later, I promise.
# --Jenny

#datadir="test_data"

class ImagePlayer(QMainWindow):

    def __init__(self, parent=None):
        super(ImagePlayer, self).__init__(parent)
#-------main image widget------------------------
        self.image_label=QLabel()
        self.image_label.setText("Please choose a directory to load")
        self.image_label.setMinimumSize(400, 300)
        self.image_label.setAlignment(Qt.AlignCenter)
#-------video playback toolbar-------------------
        self.create_actions()
        self.framelabel=QLabel()
        self.speedlabel=QLabel()
        self.speedlabel.setText("1x playback")
        #add actions and widgets to toolbar
        self.video_bar=QToolBar()
        self.video_bar.addAction(self.prev_frame10x_act)
        self.video_bar.addAction(self.prev_frame_act)
        self.video_bar.addAction(self.play_act)
        self.video_bar.addAction(self.pause_act)
        self.video_bar.addAction(self.next_frame_act)
        self.video_bar.addAction(self.next_frame10x_act)
        self.video_bar.addAction(self.speed_down_act)
        self.video_bar.addWidget(self.speedlabel)
        self.video_bar.addAction(self.speed_up_act)
        self.video_bar.addWidget(self.framelabel)
#-------Frame edit toolbar-----------------------
        self.tagselect=QComboBox()
        self.tagmanagerbutton=QPushButton("tag manager")
        self.lbracketframelabel=QLabel()
        self.rbracketframelabel=QLabel()
        self.edit_bar=QToolBar()
        self.edit_bar.addAction(self.undo_act)
        self.edit_bar.addAction(self.redo_act)
        self.edit_bar.addAction(self.lbracket_act)
        self.edit_bar.addWidget(self.lbracketframelabel)
        self.edit_bar.addAction(self.delete_act)
        self.edit_bar.addAction(self.tag_act)
        self.edit_bar.addWidget(self.rbracketframelabel)
        self.edit_bar.addAction(self.rbracket_act)
        self.edit_bar.addWidget(self.tagselect)
        self.edit_bar.addWidget(self.tagmanagerbutton)
        #set main widget layout, contains image label and video toolbar
        layout=QVBoxLayout()
        layout.addWidget(self.edit_bar)
        layout.addWidget(self.image_label)
        layout.addWidget(self.video_bar)
        #setup main widget in main window
        centralWidget=QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)
#-------Create Dock widget-----------------------
        list_dock_widget=QDockWidget("list", self)
        list_dock_widget.setObjectName("listDockWidget")
        list_dock_widget.setAllowedAreas(Qt.LeftDockWidgetArea|Qt.RightDockWidgetArea)
        #Create list widget for file names to go in dock
        self.file_list=QListWidget()
        self.file_list.setMinimumWidth(400)
        self.autoplaycheckbox=QCheckBox("continuous play")
        self.save_all_button=QPushButton("Toggle Save All")
        self.file_settings_button=QPushButton("Open File Settings")
        layout=QVBoxLayout()
        layout.addWidget(self.file_list)
        layout.addWidget(self.autoplaycheckbox)
        layout.addWidget(self.save_all_button)
        layout.addWidget(self.file_settings_button)
        dockWidget=QWidget()
        dockWidget=QWidget()
        dockWidget.setLayout(layout)
        list_dock_widget.setWidget(dockWidget)
        self.file_list.itemDoubleClicked.connect(self.load_selected_file)
        self.save_all_button.clicked.connect(self.toggle_save_all)
        self.file_settings_button.clicked.connect(self.open_file_settings)
        #add dock to main window
        self.addDockWidget(Qt.LeftDockWidgetArea, list_dock_widget)
#-------setup timer for video playback-----------
        self.timer=QTimer()
        self.timer.timeout.connect(self.next_img)
        self.timer.setInterval(25)
        self.timer_intervals=[250, 125, 50, 25, 12, 5]
#-------Create MenuBar with Load/Save------------
        filemenu=self.menuBar().addMenu("File")
        filemenu.addAction(self.open_act)
        filemenu.addAction(self.save_dir_act)
        filemenu.addAction(self.save_act)
#-------Load data, initial image, start----------
        self.savedir=None
        #self.load_directory()
        #self.update_image(0)
        self.setWindowTitle("Data Curator")
        self.show()

    def create_actions(self):
        #Create all the actions needed for video playback
        self.play_act=QAction(QIcon("play.png"), "Play", self)
        self.play_act.triggered.connect(self.play)
        self.pause_act=QAction(QIcon("pause.png"), "Pause", self)
        self.pause_act.triggered.connect(self.pause)
        self.next_frame_act=QAction(QIcon("rarrow.png"), "Forward", self)
        self.next_frame_act.triggered.connect(self.next_img)
        self.prev_frame_act=QAction(QIcon("larrow.png"), "Back", self)
        self.prev_frame_act.triggered.connect( self.prev_img)
        self.next_frame10x_act=QAction(QIcon("rarrows.png"), "Forward", self)
        self.next_frame10x_act.triggered.connect(self.next_img)
        self.prev_frame10x_act=QAction(QIcon("larrows.png"), "Back", self)
        self.prev_frame10x_act.triggered.connect(self.prev_img)
        self.speed_up_act=QAction(QIcon("uarrow.png"), "Speed Up", self)
        self.speed_up_act.triggered.connect( self.speed_up)
        self.speed_down_act=QAction(QIcon("darrow.png"), "Speed Down", self)
        self.speed_down_act.triggered.connect(self.speed_down)
        #Create all actions needed for editing
        self.delete_act=QAction(QIcon("close.png"), "Delete selection", self)
        self.delete_act.triggered.connect( self.deleteframes)
        self.tag_act=QAction(QIcon("flag.png"), "Tag selection", self)
        self.tag_act.triggered.connect(self.tagframes) #TODO
        self.lbracket_act=QAction(QIcon("lbracket.png"), "begin selection", self)
        self.lbracket_act.triggered.connect(self.bracketframes) 
        self.rbracket_act=QAction(QIcon("rbracket.png"), "end selection", self)
        self.rbracket_act.triggered.connect(self.bracketframes) 
        self.undo_act=QAction(QIcon("larrow.png"), "undo edit", self)
        self.undo_act.triggered.connect( self.undo) 
        self.redo_act=QAction(QIcon("rarrow.png"), "redo edit", self)
        self.redo_act.triggered.connect(self.redo) 
        #Create Actions for loading/saving
        self.open_act=QAction("Open Directory", self)
        self.open_act.triggered.connect(self.open_directory) 
        self.save_dir_act=QAction("Choose Save Directory", self)
        self.save_dir_act.triggered.connect(self.select_save_dir) #TODO
        self.save_act=QAction("Save File Changes", self)
        self.save_act.triggered.connect(self.save_files) #TODO

    def open_directory(self):
        self.loaddir=QFileDialog.getExistingDirectory(self)
        self.load_directory(self.loaddir)

    def select_save_dir(self):
        self.savedir=QFileDialog.getExistingDirectory(self)

    def save_files(self):
        if self.savedir is None:
            QMessageBox.warning(self, "save name error", "You must select a save directory")
        else:
            for img, comm in zip(self.img_files, self.comm_files):
                if self.file_dict[img]['save_toggle']==True:
                    save_indices=self.file_dict[img]['frames']
                    img_data=np.load(img)['arr_0']
                    comm_data=self.commdata[comm][save_indices, :]
                    save_imgs=img_data[save_indices, :, :, :]
                    np.savez(self.savedir+'/'+self.file_dict[img]['save_name'], save_imgs)
                    np.savez(self.savedir+'/'+(self.file_dict[img]['save_name']).replace('imgs', 'commands'), comm_data)



    def load_directory(self, datadir):
        #load in list of files in the data directory
        self.img_files=glob.glob(os.path.join(datadir, "imgs*.npz"))
        self.comm_files=glob.glob(os.path.join(datadir, "commands*.npz"))
        self.img_files.sort()
        self.comm_files.sort()
        self.commdata={}
        self.file_dict={}
        idx=0
        for f1, f2 in zip(self.img_files, self.comm_files):
            comm_data=np.load(f2)['arr_0']
            self.commdata[f2]=comm_data
            self.file_dict[f1]=dict([('frames', [i for i in range(0, comm_data.shape[0])]), 
                ('applied_stack', []), ('tag_dict', dict()), ('len', comm_data.shape[0]), 
                ('save_name', os.path.basename(f1)), ('save_toggle', False)]) 
            self.file_list.addItem(f1)
            self.file_list.item(idx).setBackground(QColor(255, 200, 200))
            idx=idx+1
        #load in first file:
        self.n_files=len(self.img_files)
        self.file_list.setCurrentRow(0)
        self.current_filename=self.file_list.currentItem().text()
        self.raw_frames=self.load_data(self.img_files[0])
        self.hopper=filehopper(self.img_files, self.file_dict)
        self.left_bracket=(None, None) #tuples to hold filename, frame number
        self.right_bracket=(None, None)
        self.global_undo_stack=[]
        self.global_redo_stack=[]
        self.update_image(0)

    def load_selected_file(self, selected):
        #load in new file selected from list. 
        #this should only be called by the listwidget
        self.current_filename=selected.text()
        self.file_list.setCurrentItem(selected)
        self.hopper.setIndex(0, self.img_files.index(self.current_filename))
        self.load_file(self.current_filename, 0)
        #self.raw_frames=self.load_data(selected.text())
        #update image window, start from first frame:
        #self.update_image(0)

    def load_file(self, filename, framenum=None):
        #this file is called by methods
        fileidx=self.img_files.index(filename)
        self.file_list.setCurrentRow(fileidx)
        self.current_filename=filename
        self.raw_frames=self.load_data(filename)
        if framenum!=None:
            self.update_image(framenum)

    def load_data(self, filename):
        np_images=(np.load(filename)['arr_0'])
        big_np=[scipy.misc.imresize(i, 4.0, interp='nearest') for i in np_images]
        self.image_shape=big_np[0].shape
        raw_frames=[i.tobytes() for i in big_np]
        return raw_frames

    def toggle_save_all(self):
        idx=0
        for f in self.file_dict.keys():
            self.file_dict[f]['save_toggle']=True
            self.file_list.item(idx).setBackground(QColor(200, 255, 200))
            idx=idx+1

    def open_file_settings(self):
        filename=self.file_list.currentItem().text()
        filedialog=fileSettingsDialog(filename, self.file_dict, self)
        if filedialog.exec_():
            self.global_redo_stack=[]
            info=filedialog.getInfo()
            self.file_dict[filename]['save_name']=info['savename']
            self.file_dict[filename]['save_toggle']=info['save_toggle']
            for u in range(0, info['undo_number']):
                act=self.file_dict[filename]['applied_stack'][-1].undo()
                for i in range(len(self.global_undo_stack)-1, -1, -1):
                    for j in range(len(self.global_undo_stack[i])-1, -1, -1):
                        if self.global_undo_stack[i][j] is act:
                            self.global_undo_stack[i].pop(j)
                    if self.global_undo_stack[i]==[]:
                        self.global_undo_stack.pop(i)
            if self.file_dict[filename]['save_toggle']==True:
                self.file_list.currentItem().setBackground(QColor(200, 255, 200))
            else:
                self.file_list.currentItem().setBackground(QColor(255, 200, 200))
            if filename==self.current_filename:
                self.hopper.setIndex(0) #TODO FIXME this will definitely cause an error eventually
                self.update_image(0)

    def next_img(self):
        #display next image, or 10 images ahead if called by 10x skip action
        if self.sender()==self.next_frame10x_act:
            self.hopper.jumpAhead(10, self.autoplaycheckbox.isChecked())
        else:
            self.hopper.next(self.autoplaycheckbox.isChecked())
        idx, filename=self.hopper.getState()
        if self.current_filename!=filename:
            self.load_file(filename)
        self.update_image(idx)
           
    def prev_img(self):
        #display previous image, or 10 images back if called by 10x skip action
        if self.sender()==self.prev_frame10x_act:
            self.hopper.jumpBack(10, self.autoplaycheckbox.isChecked())
        else:
            self.hopper.prev(self.autoplaycheckbox.isChecked())
        idx, filename=self.hopper.getState()
        if self.current_filename!=filename:
            self.load_file(filename)
        self.update_image(idx)

    def deleteframes(self):
        fstartindex=self.img_files.index(self.left_bracket[0])
        fstopindex=self.img_files.index(self.right_bracket[0])
        if fstartindex>fstopindex:
            QMessageBox.warning(self, "Bracketing Error", "The right bracket must come after the left bracket")
            return 
        if self.left_bracket[0]==self.right_bracket[0] and self.left_bracket[1]>self.right_bracket[1]:
            QMessageBox.warning(self, "Bracketing Error", "The right bracket must come after the left bracket")
            return
        ###Fucky stuff here:
        self.hopper.setIndex(self.left_bracket[1], self.img_files.index(self.left_bracket[0]))
        self.hopper.prev(self.autoplaycheckbox.isChecked())
        if fstartindex==fstopindex:
            #create a new delete action with the range and the dict object for the file
            delaction=deleteAction(self.left_bracket[1], self.right_bracket[1], self.file_dict[self.left_bracket[0]])
            delaction.apply()
            self.global_undo_stack.append([delaction])
        elif (fstopindex-fstartindex)==1:
            #we begin a delete action in one file and end it in the next file
            bdelaction=deleteAction(self.left_bracket[1], self.file_dict[self.left_bracket[0]]['len']-1, self.file_dict[self.left_bracket[0]])
            edelaction=deleteAction(0, self.right_bracket[1], self.file_dict[self.right_bracket[0]])
            bdelaction.apply()
            edelaction.apply()
            self.global_undo_stack.append([bdelaction, edelaction])
        else:
            #delete action spans multiple files, deleting at least one entirely
            bdelaction=deleteAction(self.left_bracket[1], self.file_dict[self.left_bracket[0]]['len']-1, self.file_dict[self.left_bracket[0]])
            edelaction=deleteAction(0, self.right_bracket[1], self.file_dict[self.right_bracket[0]])
            actionlist=[]
            for i in range(fstartindex+1, fstopindex):
                ndeleteaction=deleteAction(0, self.file_dict[self.img_files[i]]['len']-1, self.file_dict[self.img_files[i]])
                actionlist.append(ndeleteaction)
            bdelaction.apply()
            for a in actionlist:
                a.apply()
            edelaction.apply()
            actionlist.append(edelaction)
            actionlist.insert(0, bdelaction)
            self.global_undo_stack.append(actionlist)
        idx, filename=self.hopper.getState()
        if filename!=self.current_filename:
            self.load_file(filename, idx)
        else:
            self.update_image(idx)
        self.global_redo_stack=[]

    def tagframes(self):
        if self.img_files.index(self.left_bracket[0])>self.img_files.index(self.right_bracket[0]):
            QMessageBox.warning(self, "Bracketing Error", "The right bracket must come after the left bracket")
            return 
        if self.left_bracket[0]==self.right_bracket[0] and self.left_bracket[1]>self.right_bracket[1]:
            QMessageBox.warning(self, "Bracketing Error", "The right bracket must come after the left bracket")
            return
        self.global_redo_stack=[]

    def bracketframes(self):
        if self.sender()==self.lbracket_act:
            self.left_bracket=(self.current_filename, self.index)
            self.lbracketframelabel.setText("{0}, frame {1}".format(os.path.basename(self.current_filename), self.index))
        elif self.sender()==self.rbracket_act:
            self.right_bracket=(self.current_filename, self.index)
            self.rbracketframelabel.setText("{0}, frame {1}".format(os.path.basename(self.current_filename), self.index))

    def undo(self):
        if self.global_undo_stack!=[]: 
            #TODO FIXME this hopper stuff is stupid, should check to see if number of frames changes after undo
            self.hopper.prev(self.autoplaycheckbox.isChecked()) 
            actionlist=self.global_undo_stack.pop()
            for i in actionlist:
                i.undo()
            self.global_redo_stack.append(actionlist)
            self.hopper.next(self.autoplaycheckbox.isChecked())
            idx, filename=self.hopper.getState()
            if filename!=self.current_filename:
                self.load_file(filename, idx)
            else:
                self.update_image(idx)

    def redo(self):
        if self.global_redo_stack!=[]: 
            self.hopper.prev(self.autoplaycheckbox.isChecked())
            actionlist=self.global_redo_stack.pop()
            for i in actionlist:
                i.apply()
            self.global_undo_stack.append(actionlist)
            self.hopper.next(self.autoplaycheckbox.isChecked())
            idx, filename=self.hopper.getState()
            if filename!=self.current_filename:
                self.load_file(filename, idx)
            else:
                self.update_image(idx)

    def play(self):
        #starts timer to repeatedly call next_img, playing video
        self.timer.start()

    def pause(self):
        #stops timer to repeatedly call next_img, pausing video
        self.timer.stop()

    def speed_up(self):
        #increase playback speed by decreasing timer interval, calling next_img more often
        speed_idx=self.timer_intervals.index(self.timer.interval())
        if speed_idx<(len(self.timer_intervals)-1):
            self.timer.setInterval(self.timer_intervals[speed_idx+1])
            self.speedlabel.setText("{0}x playback".format(100.0/self.timer_intervals[speed_idx+1]))

    def speed_down(self):
        #decrease playback speed by increasing timer interval, calling next_img less often
        speed_idx=self.timer_intervals.index(self.timer.interval())
        if speed_idx>0:
            self.timer.setInterval(self.timer_intervals[speed_idx-1])
            self.speedlabel.setText("{0}x playback".format(100.0/self.timer_intervals[speed_idx-1]))

    def update_image(self, n):
        #set current frame index to n, and update image window
        fileframes=self.file_dict[self.current_filename]['len']
        self.index=n
        frame_num=self.file_dict[self.current_filename]['frames'][n]
        self.framelabel.setText("Frame {0}/{1}".format(self.index+1, fileframes))
        qimg=QImage(self.raw_frames[frame_num], self.image_shape[1], self.image_shape[0], self.image_shape[1]*3, QImage.Format_RGB888)
        self.image_label.setPixmap(QPixmap.fromImage(qimg))


app=QApplication(sys.argv)
nd=ImagePlayer()
app.exec_()

