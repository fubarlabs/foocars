from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QListWidget


class HistoryDialog(QDialog):
    def __init__(self, undo_stack, redo_stack, parent=None):
        super(HistoryDialog, self).__init__(parent)

        self.setWindowTitle("Action History")

        self.undo_stack = undo_stack
        self.redo_stack = redo_stack

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.undo_list = QListWidget()
        self.redo_list = QListWidget()

        for action in self.undo_stack:
            self.undo_list.addItem(str(action)) # You might need to adjust this to display the action in a user-friendly format
        for action in self.redo_stack:
            self.redo_list.addItem(str(action))

        layout.addWidget(QLabel("Undo History:"))
        layout.addWidget(self.undo_list)
        layout.addWidget(QLabel("Redo History:"))
        layout.addWidget(self.redo_list)

        self.setLayout(layout)
