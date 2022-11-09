#!/usr/bin/env python3
#### v 0.7
from PyQt5 import QtCore, QtGui, QtWidgets
import sys, os
from cfg import DIALOGWIDTH


freedesktop_main_categories = ["AudioVideo","Development",
                              "Education","Game","Graphics","Network",
                              "Office","Settings","System","Utility"]

# the dir of the application desktop files
app_dir_user = os.path.expanduser("~")+"/.local/share/applications"

class appWin(QtWidgets.QWidget):
    def __init__(self, arg1=None):
        super(appWin, self).__init__()
        self.setWindowIcon(QtGui.QIcon("icons/menu.png"))
        self.setWindowTitle("Appmenu")
        self.file_name = arg1
        ####### box 
        self.mainBox = QtWidgets.QGridLayout()
        self.setLayout(self.mainBox)
        #### file name
        lbl_file_name = QtWidgets.QLabel("File name *")
        self.mainBox.addWidget(lbl_file_name, 0, 0)
        self.le_file_name = QtWidgets.QLineEdit()
        self.mainBox.addWidget(self.le_file_name, 0, 1, 1, 5)
        #### name
        lbl_name = QtWidgets.QLabel("Name *")
        self.mainBox.addWidget(lbl_name, 1, 0)
        self.le_name = QtWidgets.QLineEdit()
        self.mainBox.addWidget(self.le_name, 1, 1, 1, 5)
        #### generic name
        lbl_gen_name = QtWidgets.QLabel("Generic Name")
        self.mainBox.addWidget(lbl_gen_name, 2, 0)
        self.le_gen_name = QtWidgets.QLineEdit()
        self.mainBox.addWidget(self.le_gen_name, 2, 1, 1, 5)
        #### executable
        lbl_exec = QtWidgets.QPushButton("Executable *")
        self.mainBox.addWidget(lbl_exec, 3, 0)
        self.le_exec = QtWidgets.QLineEdit()
        self.mainBox.addWidget(self.le_exec, 3, 1, 1, 5)
        lbl_exec.clicked.connect(lambda:self.f_choose(self.le_exec, "All Files (*.*)"))
        #### try executable
        lbl_exec_try = QtWidgets.QPushButton("Try Executable")
        self.mainBox.addWidget(lbl_exec_try, 4, 0)
        self.le_exec_try = QtWidgets.QLineEdit()
        self.mainBox.addWidget(self.le_exec_try, 4, 1, 1, 5)
        lbl_exec_try.clicked.connect(lambda:self.f_choose(self.le_exec_try, "All Files (*.*)"))
        #### path
        lbl_path = QtWidgets.QPushButton("Path")
        self.mainBox.addWidget(lbl_path, 5, 0)
        self.le_path = QtWidgets.QLineEdit()
        self.mainBox.addWidget(self.le_path, 5, 1, 1, 5)
        lbl_path.clicked.connect(lambda:self.f_choose(self.le_path, "All Files (*.*)"))
        #### categories
        lbl_categ = QtWidgets.QLabel("Category *")
        self.mainBox.addWidget(lbl_categ, 6, 0)
        self.combo_categ = QtWidgets.QComboBox()
        self.mainBox.addWidget(self.combo_categ, 6, 1, 1, 5)
        self.combo_categ.addItems(freedesktop_main_categories)
        #### mimetypes
        lbl_mime = QtWidgets.QLabel("Mimetypes **")
        self.mainBox.addWidget(lbl_mime, 7, 0)
        self.le_mime = QtWidgets.QLineEdit()
        self.mainBox.addWidget(self.le_mime, 7, 1, 1, 5)
        #### keywords
        lbl_keys = QtWidgets.QLabel("Keywords **")
        self.mainBox.addWidget(lbl_keys, 8, 0)
        self.le_keys = QtWidgets.QLineEdit()
        self.mainBox.addWidget(self.le_keys, 8, 1, 1, 5)
        #### icon
        lbl_icon = QtWidgets.QPushButton("Icon")
        self.mainBox.addWidget(lbl_icon, 9, 0)
        self.le_icon = QtWidgets.QLineEdit()
        self.mainBox.addWidget(self.le_icon, 9, 1, 1, 5)
        lbl_icon.clicked.connect(lambda:self.f_choose(self.le_icon, "Icons (*.png *.svg *.xpm)"))
        #### comment
        lbl_comment = QtWidgets.QLabel("Comment")
        self.mainBox.addWidget(lbl_comment, 10, 0)
        self.le_comment = QtWidgets.QLineEdit()
        self.mainBox.addWidget(self.le_comment, 10, 1, 1, 5)
        ####
        lbl_optional = QtWidgets.QLabel("(* mandatory - ** optional and separate with a semicolon)")
        self.mainBox.addWidget(lbl_optional, 11, 0, 1, 6)
        #### check buttons
        hbox_chk_btn = QtWidgets.QHBoxLayout()
        self.mainBox.addLayout(hbox_chk_btn, 12, 0, 1, 6)
        self.chk_term = QtWidgets.QCheckBox("Run in Terminal")
        hbox_chk_btn.addWidget(self.chk_term)
        self.chk_disp = QtWidgets.QCheckBox("No Display")
        hbox_chk_btn.addWidget(self.chk_disp)
        self.chk_hidd = QtWidgets.QCheckBox("Hidden")
        hbox_chk_btn.addWidget(self.chk_hidd)
        #### buttons
        self.hbox_btn = QtWidgets.QHBoxLayout()
        self.mainBox.addLayout(self.hbox_btn, 13, 0, 1, 6)
        ## delete button
        self.del_btn = QtWidgets.QPushButton("Delete")
        self.del_btn.clicked.connect(self.f_delete)
        self.hbox_btn.addWidget(self.del_btn)
        ## accept button
        self.acpt_btn = QtWidgets.QPushButton("Accept")
        self.acpt_btn.clicked.connect(self.f_accept)
        self.hbox_btn.addWidget(self.acpt_btn)
        ## close button
        self.quit_btn = QtWidgets.QPushButton("Close")
        self.quit_btn.clicked.connect(self.f_close)
        self.hbox_btn.addWidget(self.quit_btn)
        #
        if arg1:
            self.f_modify()
        #
        self.show()
        
    def f_delete(self):
        if not self.le_file_name.text() or not self.le_name.text() or not self.le_exec.text():
            MyDialog("Info", "Nothing to do.", self)
            return
        #
        if os.path.dirname(self.file_name) == app_dir_user:
            #
            ret = MyDialog("Question", "Delete?", self)
            if ret.getValue() == 1:
                try:
                    os.remove(self.file_name)
                    self.close()
                except Exception as E:
                    MyDialog("Error", str(E), self)
                    return
        else:
            MyDialog("Info", "Cannot remove a system file.", self)
            return
    
    def f_accept(self):
        if not self.le_file_name.text() or not self.le_name.text() or not self.le_exec.text():
            MyDialog("Info", "Mandatory field(s) empty.", self)
            return
        #
        file_name = self.le_file_name.text()
        if not file_name.endswith(".desktop"):
            file_name += ".desktop"
        file_name_path = os.path.join(app_dir_user, file_name)
        if os.path.exists(file_name_path):
            ret = MyDialog("Question", "The desktop file already exists.\nDo you want to overwrite it?", self)
            if ret.getValue() == 0:
                return
        #
        f_content="""[Desktop Entry]
Type=Application
Version=1.0
Name={}
GenericName={}
Exec={}
TryExec={}
Path={}
Categories={};
MimeType={}
Keywords={}
Icon={}
Comment={}
Terminal={}
NoDisplay={}
Hidden={}
""".format(self.le_name.text(), self.le_gen_name.text(), self.le_exec.text(), self.le_exec_try.text(), self.le_path.text(), self.combo_categ.currentText(), self.le_mime.text(), self.le_keys.text(), self.le_icon.text(), self.le_comment.text(), str(self.chk_term.isChecked()).lower(), str(self.chk_disp.isChecked()).lower(), str(self.chk_hidd.isChecked()).lower())
        #
        try:
            ffile = open(file_name_path, "w")
            ffile.write(f_content)
            ffile.close()
            MyDialog("Info", "Done.", self)
        except Exception as E:
            MyDialog("Error", str(E), self)
        #
        self.file_name = file_name_path
        #
        self.le_file_name.setText(file_name)
        self.le_file_name.setEnabled(False)
    
    def f_modify(self):
        file_content = None
        with open(self.file_name, "r") as ffile:
            file_content = ffile.readlines()
        #
        self.le_file_name.setText(os.path.basename(self.file_name))
        self.le_file_name.setEnabled(False)
        #
        for el in file_content:
            if el[0:5] == "Name=":
                self.le_name.setText(el[5:].strip("\n"))
            elif el[0:12] == "GenericName=":
                self.le_gen_name.setText(el[12:].strip("\n"))
            elif el[0:5] == "Exec=":
                self.le_exec.setText(el[5:].strip("\n"))
            elif el[0:8] == "TryExec=":
                self.le_exec_try.setText(el[8:].strip("\n"))
            elif el[0:5] == "Path=":
                self.le_path.setText(el[5:].strip("\n"))
            elif el[0:11] == "Categories=":
                cat_name = el[11:].strip("\n").split(";")[0]
                if cat_name in freedesktop_main_categories:
                    cb_idx = self.combo_categ.findText(cat_name)
                    if cb_idx != -1:
                        self.combo_categ.setCurrentIndex(cb_idx)
            elif el[0:9] == "MimeType=":
                self.le_mime.setText(el[9:].strip("\n"))
            elif el[0:9] == "Keywords=":
                self.le_keys.setText(el[9:].strip("\n"))
            elif el[0:5] == "Icon=":
                self.le_icon.setText(el[5:].strip("\n"))
            elif el[0:8] == "Comment=":
                self.le_comment.setText(el[8:].strip("\n"))
            elif el[0:9] == "Terminal=":
                term_chk = el[9:].strip("\n")
                self.chk_term.setChecked(False if term_chk=="false" else True)
            elif el[0:10] == "NoDisplay=":
                nodisp_chk = el[10:].strip("\n")
                self.chk_disp.setChecked(False if nodisp_chk=="false" else True)
            elif el[0:7] == "Hidden=":
                hidd_chk = el[7:].strip("\n")
                self.chk_hidd.setChecked(False if hidd_chk=="false" else True)
    
    def f_close(self):
        ret = MyDialog("Question", "Close this program?", self)
        if ret.getValue() == 1:
            self.close()
    
    def f_choose(self, wgt, f_type):
        fileName = QtWidgets.QFileDialog.getOpenFileName(self,
            "Choose", os.path.expanduser("~"), f_type)
        if fileName[0]:
            wgt.setText(fileName[0])
        

#############

# args: type - message - parent
class MyDialog(QtWidgets.QMessageBox):
    def __init__(self, *args):
        super(MyDialog, self).__init__(args[-1])
        if args[0] == "Info":
            self.setIcon(QtWidgets.QMessageBox.Information)
            self.setStandardButtons(QtWidgets.QMessageBox.Ok)
        elif args[0] == "Error":
            self.setIcon(QtWidgets.QMessageBox.Critical)
            self.setStandardButtons(QtWidgets.QMessageBox.Ok)
        elif args[0] == "Question":
            self.setIcon(QtWidgets.QMessageBox.Question)
            self.setStandardButtons(QtWidgets.QMessageBox.Ok|QtWidgets.QMessageBox.Cancel)
        self.setWindowIcon(QtGui.QIcon("icons/dialog-red.svg"))
        self.setWindowTitle(args[0])
        self.resize(DIALOGWIDTH,50)
        self.setText(args[1])
        self.Value = None
        retval = self.exec_()
        #
        if retval == QtWidgets.QMessageBox.Ok:
            self.Value = 1
        elif retval == QtWidgets.QMessageBox.Cancel:
            self.Value = 0
    
    def getValue(self):
        return self.Value
    
    def event(self, e):
        result = QtWidgets.QMessageBox.event(self, e)
        #
        self.setMinimumHeight(0)
        self.setMaximumHeight(16777215)
        self.setMinimumWidth(0)
        self.setMaximumWidth(16777215)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        # 
        return result


################
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    if len(sys.argv) > 1:
        if sys.argv[1]:
            window = appWin(sys.argv[1])
    else:
        window = appWin()
    sys.exit(app.exec_())
