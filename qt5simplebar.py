#!/usr/bin/env python3
#### v 1.3
from PyQt5 import QtCore, QtGui, QtWidgets
import sys, os, time
from shutil import which as sh_which
from Xlib.display import Display
from Xlib import X
import datetime
from cfg import *
sys.path.append("modules")
from pop_menu import getMenu

# width and height of the program
WINW = 0
WINH = 0

################
# load the database
fopen = calendar_file

class sEvent:
    SUMMARY=None
    DTSTART=None

list_events_all = []
#
def get_events():
    _events = None
    if os.path.exists(fopen):
        try:
            with open(fopen, "r") as f:
                _events = f.readlines()
        except:
            pass
    else:
        return
    
    if _events is None:
        return
    if _events == []:
        return
    #
    s_event = None
    for el in _events:
        
        if el.strip("\n") == "BEGIN:VEVENT":
            s_event = sEvent()
            
        elif el.strip("\n")[0:8] == "SUMMARY:":
            s_event.SUMMARY = el.strip("\n")[8:]
        
        elif el.strip("\n")[0:8] == "DTSTART:":
            s_event.DTSTART = el.strip("\n")[8:]
        
        elif el.strip("\n") == "END:VEVENT":
            list_events_all.append(s_event)
            s_event = None
        
        elif el.strip("\n") == "END:VCALENDAR":
            s_event = None
            break
    
get_events()

#### main application categories
Development = []
Education = []
Game = []
Graphics = []
Multimedia = []
Network = []
Office = []
Settings = []
System = []
Utility = []
Missed = []

# extended categories
development_extended_categories = ["Building","Debugger","IDE","GUIDesigner",
                                  "Profiling","RevisionControl","Translation",
                                  "Database","WebDevelopment"]

office_extended_categories = ["Calendar","ContanctManagement","Office",
                             "Dictionary","Chart","Email","Finance","FlowChart",
                             "PDA","ProjectManagement","Presentation","Spreadsheet",
                             "WordProcessor","Engineering"]

graphics_extended_categories = ["2DGraphics","VectorGraphics","RasterGraphics",
                               "3DGraphics","Scanning","OCR","Photography",
                               "Publishing","Viewer"]

utility_extended_categories = ["TextTools","TelephonyTools","Compression",
                              "FileTools","Calculator","Clock","TextEditor",
                              "Documentation"]

settings_extended_categories = ["DesktopSettings","HardwareSettings",
                               "Printing","PackageManager","Security",
                               "Accessibility"]

network_extended_categories = ["Dialup","InstantMessaging","Chat","IIRCClient",
                              "FileTransfer","HamRadio","News","P2P","RemoteAccess",
                              "Telephony","VideoConference","WebBrowser"]

# added "Audio" and "Video" main categories
audiovideo_extended_categories = ["Audio","Video","Midi","Mixer","Sequencer","Tuner","TV",
                                 "AudioVideoEditing","Player","Recorder",
                                 "DiscBurning"]

game_extended_categories = ["ActionGame","AdventureGame","ArcadeGame",
                           "BoardGame","BlockGame","CardGame","KidsGame",
                           "LogicGame","RolePlaying","Simulation","SportGame",
                           "StrategyGame","Amusement","Emulator"]

education_extended_categories = ["Art","Construction","Music","Languages",
                                "Science","ArtificialIntelligence","Astronomy",
                                "Biology","Chemistry","ComputerScience","DataVisualization",
                                "Economy","Electricity","Geography","Geology","Geoscience",
                                "History","ImageProcessing","Literature","Math","NumericAnalysis",
                                "MedicalSoftware","Physics","Robots","Sports","ParallelComputing",
                                "Electronics"]

system_extended_categories = ["FileManager","TerminalEmulator","FileSystem",
                             "Monitor","Core"]

# populate the menu
def on_pop_menu(app_dirs_user, app_dirs_system):
    #
    menu = getMenu(app_dirs_user, app_dirs_system).retList()[0]
    for el in menu:
        cat = el[2]
        if cat == "AudioVideo" or cat in audiovideo_extended_categories:
            # label - executable - icon
            Multimedia.append([el[0],el[4],el[5],el[6]])
        elif cat == "Development" or cat in development_extended_categories:
            Development.append([el[0],el[4],el[5],el[6]])
        elif cat == "Education" or cat in education_extended_categories:
            Education.append([el[0],el[4],el[5],el[6]])
        elif cat == "Game" or cat in game_extended_categories:
            Game.append([el[0],el[4],el[5],el[6]])
        elif cat == "Graphics" or cat in graphics_extended_categories:
            Graphics.append([el[0],el[4],el[5],el[6]])
        elif cat == "Network" or cat in network_extended_categories:
            Network.append([el[0],el[4],el[5],el[6]])
        elif cat == "Office" or cat in office_extended_categories:
            Office.append([el[0],el[4],el[5],el[6]])
        elif cat == "Settings" or cat in settings_extended_categories:
            Settings.append([el[0],el[4],el[5],el[6]])
        elif cat == "System" or cat in system_extended_categories:
            System.append([el[0],el[4],el[5],el[6]])
        elif cat == "Utility" or cat in utility_extended_categories:
            Utility.append([el[0],el[4],el[5],el[6]])
        else:
            Missed.append([el[0],el[4],el[5],el[6]])

# the dirs of the application files
app_dirs_user = [os.path.expanduser("~")+"/.local/share/applications"]
app_dirs_system = ["/usr/share/applications", "/usr/local/share/applications"]

on_pop_menu(app_dirs_user, app_dirs_system)

#############

class showDialog(QtWidgets.QDialog):
    def __init__(self, dtype, lcontent, parent):
        super().__init__(parent)
        
        self.setWindowTitle("Info")
        
        if dtype == 1:
            QBtn = QtWidgets.QDialogButtonBox.Ok
        elif dtype == 2:
            QBtn = QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel

        self.buttonBox = QtWidgets.QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QtWidgets.QVBoxLayout()
        message = QtWidgets.QLabel(lcontent)
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)
        
        # geometry of the main window
        qr = self.frameGeometry()
        # center point of screen
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        # move rectangle's center point to screen's center point
        qr.moveCenter(cp)
        # top left of rectangle becomes top left of window centering it
        self.move(qr.topLeft())


# main class
class MainWin(QtWidgets.QMainWindow):
    
    def __init__(self, parent=None):
        super(MainWin, self).__init__(parent)
        self.setWindowTitle("qt5simplebar")
        ######## top container
        self.gbox = QtWidgets.QGridLayout()
        self.gbox.setContentsMargins(0,0,0,0)
        self.widget = QtWidgets.QWidget()
        self.widget.setContentsMargins(0, 0, 0, 0)
        self.widget.setLayout(self.gbox)
        self.setCentralWidget(self.widget)
        ####### 
        self.abox = QtWidgets.QHBoxLayout()
        self.abox.setContentsMargins(10,0,0,0)
        self.gbox.addLayout(self.abox, 0,0)
        
        self.mbutton = QtWidgets.QPushButton(self, flat=True)
        self.mbutton.setIcon(QtGui.QIcon("icons/menu.png"))
        self.btn_style_sheet(self.mbutton)
        self.mbutton.clicked.connect(self.on_click)
        ###### 
        self.cbox = QtWidgets.QHBoxLayout()
        self.cbox.setContentsMargins(0,0,0,0)
        self.gbox.addLayout(self.cbox, 0,5)
        self.tlabel = QtWidgets.QLabel("")
        tfont = QtGui.QFont()
        if calendar_label_font:
            tfont.setFamily(calendar_label_font)
        tfont.setPointSize(calendar_label_font_size)
        tfont.setWeight(calendar_label_font_weight)
        tfont.setItalic(calendar_label_font_italic)
        self.tlabel.setFont(tfont)
        if calendar_label_font_color:
            self.tlabel.setStyleSheet("color: {}".format(calendar_label_font_color))
        self.tlabel.setAlignment(QtCore.Qt.AlignCenter)
        self.cbox.addWidget(self.tlabel)
        #
        cur_time = QtCore.QTime.currentTime().toString('hh:mm')
        self.tlabel.setText(cur_time)
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_label)
        timer.start(60 * 1000)
        
        self.tlabel.setContentsMargins(0,0,0,0)
        self.tlabel.mousePressEvent = self.on_tlabel
        ######### box di destra
        self.zbox = QtWidgets.QHBoxLayout()
        self.zbox.setContentsMargins(0,0,10,0)
        orSpacer2 = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum) 
        self.zbox.addItem(orSpacer2)
        self.gbox.addLayout(self.zbox, 0,10)
        self.ebutton = QtWidgets.QPushButton(self, flat=True)
        self.ebutton.setIcon(QtGui.QIcon("icons/user.png"))
        self.ebutton.clicked.connect(self.on_close)
        # set the style
        self.btn_style_sheet(self.ebutton)
        #
        if menu_left:
            self.abox.addWidget(self.mbutton)
            orSpacer1 = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum) 
            self.abox.addItem(orSpacer1)
            self.zbox.addWidget(self.ebutton)
        else:
            self.abox.addWidget(self.ebutton)
            orSpacer1 = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum) 
            self.abox.addItem(orSpacer1)
            self.zbox.addWidget(self.mbutton)
        
        # for the calendar window
        self.cw_is_shown = None
        # for the menu window
        self.mw_is_shown = None
        # for the exit window
        self.cwin_is_shown = None
        #
        # calendar list events
        self.list_events = list_events_all
    
    # close all the menu if the bar is selected
    def mousePressEvent(self, event):
        ## for the calendar window
        if self.cw_is_shown:
            self.cw_is_shown.close()
            self.cw_is_shown = None
        # for the menu window
        if self.mw_is_shown:
            self.mw_is_shown.close()
            self.mw_is_shown = None
        # for the exit window
        if self.cwin_is_shown:
            self.cwin_is_shown.close()
            self.cwin_is_shown = None
    
    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        pix = QtGui.QPixmap("icons/left.png")
        painter.drawPixmap(0,0, pix)
        pix = QtGui.QPixmap("icons/right.png")
        painter.drawPixmap(WINW-10,0, pix)
        painter.end()
    
    
    # label time    
    def update_label(self):
        cur_time = QtCore.QTime.currentTime().toString('hh:mm')
        self.tlabel.setText(cur_time)
    
    # click on tlabel
    def on_tlabel(self, e):
        if self.cw_is_shown is not None:
            self.cw_is_shown.close()
            self.cw_is_shown = None
            return
        cw = calendarWin(self)
        cw.show()
        self.cw_is_shown = cw
    
    # style sheet for buttons
    def btn_style_sheet(self, w):
        w.setStyleSheet(""" QPushButton { 
                                        padding: 0px;
                                        border-color: black;
                                        border-style: outset;
                                        border-width: 0px;
                                        }
                                        
                                        QPushButton:hover {
                                            background-color: rgb(190,190,190);
                                        }
                                        
                                        QPushButton:pressed {
                                            background-color: rgb(190,190,190);     
                                        }
                                    """)
    
    def contextMenuEvent(self, event):
        contextMenu = QtWidgets.QMenu(self)
        reloadAct = contextMenu.addAction("Reload")
        quitAct = contextMenu.addAction("Quit")
        action = contextMenu.exec_(self.mapToGlobal(event.pos()))
        if action == quitAct:
            self.close()
        elif action == reloadAct:
            self.restart()
            
    def restart(self):
        QtCore.QCoreApplication.quit()
        status = QtCore.QProcess.startDetached(sys.executable, sys.argv)
    
    # click on mbutton
    def on_click(self):
        sender_button = self.sender()
        #
        if self.mw_is_shown is not None:
            self.mw_is_shown.close()
            self.mw_is_shown = None
            return
        mw = menuWin(self)
        self.mw_is_shown = mw
    
    #
    def on_close(self):
        if self.cwin_is_shown:
            self.cwin_is_shown.close()
            self.cwin_is_shown = None
            return
        cwin = closeWin(self)
        self.cwin_is_shown = cwin
    

# menu
class menuWin(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(menuWin, self).__init__(parent)
        self.window = window
        # self.setWindowFlags(self.windowFlags() | QtCore.Qt.FramelessWindowHint | QtCore.Qt.Tool | QtCore.Qt.WindowDoesNotAcceptFocus)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.FramelessWindowHint | QtCore.Qt.Window | QtCore.Qt.WindowStaysOnTopHint)
        ####### 
        self.mainBox = QtWidgets.QHBoxLayout()
        self.setLayout(self.mainBox)
        #
        win_height = self.window.size().height()
        sw = menu_width
        sh = 200
        if menu_left:
            sx = 0
        else:
            sx = WINW-sw
        if with_compositor:
            sy = win_height
        else:
            sy = win_height + 2
        if menu_left:
            sx += 2
        else:
            sx -= 2
        self.setGeometry(sx,sy,sw,sh)
        #
        self.hbox = QtWidgets.QHBoxLayout()
        # 
        if with_compositor:
            self.frame=QtWidgets.QFrame(self)
            self.frame.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
            self.mainBox.addWidget(self.frame)
            self.frame.setStyleSheet("background: palette(window); border-radius:{}px".format(border_radius))
            self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
            #
            if menu_left:
                self.mainBox.setContentsMargins(2,2,10,10)
                shadow_effect = QtWidgets.QGraphicsDropShadowEffect(
                        blurRadius=blur_radius,
                        offset=QtCore.QPointF(5, 5)
                    )
            else:
                self.mainBox.setContentsMargins(10,2,2,10)
                shadow_effect = QtWidgets.QGraphicsDropShadowEffect(
                        blurRadius=blur_radius,
                        offset=QtCore.QPointF(-5, 5)
                    )
            self.setGraphicsEffect(shadow_effect)
            #
            self.frame.setLayout(self.hbox)
        else:
            self.mainBox.setContentsMargins(2,2,2,2)
            self.mainBox.addLayout(self.hbox)
        
        ##### left box
        self.lbox = QtWidgets.QVBoxLayout()
        self.lbox.setContentsMargins(0,0,0,0)
        self.hbox.addLayout(self.lbox)
        #
        self.listWidget = QtWidgets.QListWidget(self)
        self.lbox.addWidget(self.listWidget)
        hpalette = self.palette().highlight().color().name()
        csaa = ("QListWidget::item:hover {")
        csab = ("background-color: {};".format(hpalette))
        csac = ("}")
        csa = csaa+csab+csac
        self.listWidget.setStyleSheet(csa)
        ###########
        cssa = ("QScrollBar:vertical {"
    "border: 0px solid #999999;"
    "background:white;"
    "width:8px;"
    "margin: 0px 0px 0px 0px;"
"}"
"QScrollBar::handle:vertical {")       
        cssb = ("min-height: 0px;"
    "border: 0px solid red;"
    "border-radius: 4px;"
    "background-color: {};".format(scroll_handle_col))
        cssc = ("}"
"QScrollBar::add-line:vertical {"       
    "height: 0px;"
    "subcontrol-position: bottom;"
    "subcontrol-origin: margin;"
"}"
"QScrollBar::sub-line:vertical {"
    "height: 0 px;"
    "subcontrol-position: top;"
    "subcontrol-origin: margin;"
"}")
        css = cssa+cssb+cssc
        self.listWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.listWidget.verticalScrollBar().setStyleSheet(css)
        ###########
        self.line_edit = QtWidgets.QLineEdit("")
        self.line_edit.setFrame(True)
        self.line_edit.setStyleSheet("background: white")
        self.line_edit.textChanged.connect(self.on_line_edit)
        self.lbox.addWidget(self.line_edit)
        
        ##### right box
        self.rbox = QtWidgets.QVBoxLayout()
        self.rbox.setContentsMargins(0,0,0,0)
        self.hbox.addLayout(self.rbox)
        #
        self.pref = QtWidgets.QPushButton("Bookmarks")
        self.pref.setIcon(QtGui.QIcon("icons/bookmark.svg"))
        self.pref.setFlat(True)
        ##########
        hpalette = self.palette().mid().color().name()
        csaa = ("QPushButton::hover:!pressed { border: none;")
        csab = ("background-color: {};".format(hpalette))
        csac = ("border-radius: 3px;}")
        csa = csaa+csab+csac
        self.pref.setStyleSheet(csa)
        ###########
        self.pref.clicked.connect(self.on_pref_clicked)
        self.rbox.addWidget(self.pref, alignment=QtCore.Qt.AlignLeft)
        #
        sepLine = QtWidgets.QFrame()
        sepLine.setFrameShape(QtWidgets.QFrame.HLine)
        sepLine.setFrameShadow(QtWidgets.QFrame.Plain)
        self.rbox.addWidget(sepLine)
        #
        self.rboxBtn = QtWidgets.QVBoxLayout()
        self.rboxBtn.setContentsMargins(0,0,0,0)
        self.rbox.addLayout(self.rboxBtn)
        #
        self.populate_menu()
        #
        self.rbox.addStretch(1)
        #
        self.show()
        #
        if self.window.cw_is_shown:
            self.window.cw_is_shown.close()
            self.window.cw_is_shown = None
        if self.window.cwin_is_shown:
            self.window.cwin_is_shown.close()
            self.window.cwin_is_shown = None
        #
        self.emulate_clicked(self.pref, 100)
        #
        self.listWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.listWidget.customContextMenuRequested.connect(self.itemClicked)
        # which button has been pressed
        self.itemBookmark = 1

    #
    def itemClicked(self, QPos):
        item_idx = self.listWidget.indexAt(QPos)
        _item = self.listWidget.itemFromIndex(item_idx)
        if _item == None:
            self.listWidget.clearSelection()
            self.listWidget.clearFocus()
            return
        if self.itemBookmark:
            self.listItemRightClickedToRemove(QPos)
        else:
            self.listItemRightClicked(QPos)
    
    def emulate_clicked(self, button, ms):
        QtCore.QTimer.singleShot(ms, button.clicked.emit)
    
    #
    def on_line_edit(self, text):
        self.listWidget.clear()
        self.search_program(text)
        
    
    # seeking in the program lists
    def search_program(self, text):
        if len(text) > 2:
            self.listWidget.clear()
            app_list = ["Development", "Education","Game",
                        "Graphics", "Multimedia", "Network",
                        "Office","Settings","System","Utility", "Missed"]
            #
            for ell in app_list:
                if globals()[ell] == []:
                    continue
                for el in globals()[ell]:
                    if (text.casefold() in el[1].casefold()) or (text.casefold() in el[3].casefold()):
                        exe_path = sh_which(el[1].split(" ")[0])
                        file_info = QtCore.QFileInfo(exe_path)
                        if file_info.exists():
                            icon = QtGui.QIcon.fromTheme(el[2])
                            if not icon.name():
                                icon = QtGui.QIcon("icons/none.svg")
                            litem = QtWidgets.QListWidgetItem(icon, el[0])
                            # set the exec name as property
                            litem.exec_n = el[1]
                            litem.setToolTip(el[3])
                            self.listWidget.addItem(litem)
                            self.listWidget.itemClicked.connect(self.listwidgetclicked)
        else:
            self.listWidget.clear()
    
    def populate_menu(self):
        # remove all widgets
        for i in reversed(range(self.rboxBtn.count())): 
            self.rboxBtn.itemAt(i).widget().deleteLater()
        #
        app_list = ["Development", "Education","Game",
                    "Graphics", "Multimedia", "Network",
                    "Office","Settings","System","Utility", "Missed"]
        for el in app_list:
            if globals()[el] == []:
                continue
            btn = QtWidgets.QPushButton(el)
            btn.setIcon(QtGui.QIcon("icons/{}".format(el+".svg")))
            btn.setFlat(True)
            ##########
            hpalette = self.palette().mid().color().name()
            csaa = ("QPushButton::hover:!pressed { border: none;")
            csab = ("background-color: {};".format(hpalette))
            csac = ("border-radius: 3px;}")
            csa = csaa+csab+csac
            btn.setStyleSheet(csa)
            ##########
            self.rboxBtn.addWidget(btn, alignment=QtCore.Qt.AlignLeft)
            btn.clicked.connect(self.on_btn_clicked)
            
    
    # category button clicked
    def on_btn_clicked(self):
        self.itemBookmark = 0
        cat_name = self.sender().text()
        cat_list = globals()[cat_name]
        self.listWidget.clear()
        for el in cat_list:
            # 0 name - 1 executable - 2 icon - 3 comment
            exe_path = sh_which(el[1].split(" ")[0])
            file_info = QtCore.QFileInfo(exe_path)
            if file_info.exists():
                # set the full path first
                if os.path.exists(el[2]):
                    icon = QtGui.QIcon(el[2])
                else:
                    icon = QtGui.QIcon.fromTheme(el[2])
                    if not icon.name():
                        icon = QtGui.QIcon("icons/none.svg")
                litem = QtWidgets.QListWidgetItem(icon, el[0])
                # set the exec name as property
                litem.exec_n = el[1]
                litem.setToolTip(el[3])
                self.listWidget.addItem(litem)
                self.listWidget.itemClicked.connect(self.listwidgetclicked)
                #
        self.listWidget.scrollToTop()
    
    # add the bookmark
    def listItemRightClicked(self, QPos):
        self.listMenu= QtWidgets.QMenu()
        item_b = self.listMenu.addAction("Add to bookmark")
        action = self.listMenu.exec_(self.listWidget.mapToGlobal(QPos))
        if action == item_b:
            item_idx = self.listWidget.indexAt(QPos)
            _item = self.listWidget.itemFromIndex(item_idx)
            # check if a bookmark is already present
            pret = 1
            pret = self.check_bookmarks(_item)
            if pret == 1:
                #
                new_book = str(int(time.time()))
                icon_name = _item.icon().name()
                # da fare: trovare path tra le liste dei programmi
                if not icon_name:
                    icon_name = "none"
                # ICON - NAME - EXEC - TOOLTIP
                new_book_content = """{0}
{1}
{2}
{3}""".format(icon_name,_item.text(),_item.exec_n,_item.toolTip() or _item.text())
                with open(os.path.join("bookmarks", new_book), "w") as fbook:
                    fbook.write(new_book_content)
        self.listWidget.clearSelection()
        self.listWidget.clearFocus()
    
    #
    def check_bookmarks(self, _item):
        if _item == None:
            return 1
        list_prog = os.listdir("bookmarks")
        if not list_prog:
            return 1
        for el in list_prog:
            cnt = []
            file_to_read = os.path.join("bookmarks", el)
            with open(file_to_read, "r") as f:
                cnt = f.readlines()
            #
            if cnt[2].strip("\n") == _item.exec_n:
                return 3
            else:
                return 1
    
    # execute the program from the menu
    def listwidgetclicked(self, item):
        self.p = QtCore.QProcess()
        self.p.start(str(item.exec_n))
        # close the menu window
        if self.window.mw_is_shown is not None:
            self.window.mw_is_shown.close()
            self.window.mw_is_shown = None
    
    # the bookmark button
    def on_pref_clicked(self):
        self.itemBookmark = 1
        self.listWidget.clear()
        bookmark_files = os.listdir("bookmarks")
        prog_list = []
        for bb in bookmark_files:
            with open(os.path.join("bookmarks",bb), "r") as fbook:
                cnt = fbook.readlines()
                # add the filename
                cnt.append(bb)
                prog_list.append(cnt)
        # populate listWidget
        for el in prog_list:
            ICON = el[0].strip("\n")
            NAME = el[1].strip("\n")
            EXEC = el[2].strip("\n")
            TOOLTIP = el[3].strip("\n")
            FILENAME = el[4].strip("\n")
            #
            exe_path = sh_which(EXEC.split(" ")[0])
            file_info = QtCore.QFileInfo(exe_path)
            if file_info.exists():
                if os.path.exists(ICON):
                    icon = QtGui.QIcon(ICON)
                else:
                    icon = QtGui.QIcon.fromTheme(ICON)
                    if not icon.name():
                        icon = QtGui.QIcon("icons/none.svg")
                litem = QtWidgets.QListWidgetItem(icon, NAME)
                litem.exec_n = EXEC
                litem.setToolTip(TOOLTIP)
                litem.file_name = FILENAME
                self.listWidget.addItem(litem)
                self.listWidget.itemClicked.connect(self.listwidgetclicked)
                #
        self.listWidget.sortItems(QtCore.Qt.AscendingOrder)
    
    #
    def listItemRightClickedToRemove(self, QPos):
        self.listMenuR= QtWidgets.QMenu()
        item_b = self.listMenuR.addAction("Remove from bookmark")
        action = self.listMenuR.exec_(self.listWidget.mapToGlobal(QPos))
        if action == item_b:
            item_idx = self.listWidget.indexAt(QPos)
            item_row = item_idx.row()
            item_removed = self.listWidget.takeItem(item_row)
            #
            try:
                os.remove(os.path.join("bookmarks", item_removed.file_name))
            except:
                pass
        self.listWidget.clearSelection()
        self.listWidget.clearFocus()


# popup per calendar
class calendarWin(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(calendarWin, self).__init__(parent)
        self.window = window
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.FramelessWindowHint | QtCore.Qt.Tool | QtCore.Qt.WindowDoesNotAcceptFocus)
        ####### box 
        mainBox = QtWidgets.QHBoxLayout()
        self.setLayout(mainBox)
        ## 
        self.hbox = QtWidgets.QHBoxLayout()
        if with_compositor:
            self.frame=QtWidgets.QFrame(self)
            mainBox.addWidget(self.frame)
            self.frame.setLayout(self.hbox)
            self.hbox.setContentsMargins(10,10,10,10)
            mainBox.setContentsMargins(10,2,10,10)
            self.frame.setStyleSheet("background: palette(window); border-radius:{}px".format(border_radius))
            self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
            #
            shadow_effect = QtWidgets.QGraphicsDropShadowEffect(
                    blurRadius=blur_radius,
                    offset=QtCore.QPointF(5, 5)
                )
            self.setGraphicsEffect(shadow_effect)
        else:
            mainBox.addLayout(self.hbox)
            self.hbox.setContentsMargins(2,2,2,2)
            mainBox.setContentsMargins(0,0,0,0)
        
        #### 
        self.vbox_1 = QtWidgets.QVBoxLayout()
        self.vbox_1.setContentsMargins(0,0,0,0)
        self.hbox.addLayout(self.vbox_1)
        #
        self.scroll = QtWidgets.QScrollArea()
        self.widget = QtWidgets.QWidget()
        self.vbox = QtWidgets.QVBoxLayout()
        self.widget.setLayout(self.vbox)
        # 
        self.ldatebox = QtWidgets.QHBoxLayout()
        self.ldatebox.setContentsMargins(0,0,0,0)
        self.vbox_1.addLayout(self.ldatebox)
        #
        tomonth = datetime.datetime.now().strftime("%B")
        toyear = str(datetime.datetime.now().year)
        #
        self.mlabel = QtWidgets.QLabel(tomonth+" "+toyear)
        self.mlabel.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.mlabel.setAlignment(QtCore.Qt.AlignCenter)
        self.mlabel.mousePressEvent = self.go_today 
        #
        self.pmonth = QtWidgets.QPushButton()
        self.pmonth.setIcon(QtGui.QIcon("icons/go-prev.png"))
        #
        self.nmonth = QtWidgets.QPushButton()
        self.nmonth.setIcon(QtGui.QIcon("icons/go-next.png"))
        #
        self.pmonth.clicked.connect(self.on_prev_month)
        self.nmonth.clicked.connect(self.on_next_month)
        #
        self.ldatebox.addWidget(self.pmonth)
        self.ldatebox.addWidget(self.mlabel)
        self.ldatebox.addWidget(self.nmonth)
        #
        self.scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setFixedWidth(appointment_window_size)
        self.scroll.setWidget(self.widget)
        cssa = ("QScrollBar:vertical {"
    "border: 0px solid #999999;"
    "background:white;"
    "width:8px;"
    "margin: 0px 0px 0px 0px;"
"}"
"QScrollBar::handle:vertical {")       
        cssb = ("min-height: 0px;"
    "border: 0px solid red;"
    "border-radius: 4px;"
    "background-color: {};".format(scroll_handle_col))
        cssc = ("}"
"QScrollBar::add-line:vertical {"       
    "height: 0px;"
    "subcontrol-position: bottom;"
    "subcontrol-origin: margin;"
"}"
"QScrollBar::sub-line:vertical {"
    "height: 0 px;"
    "subcontrol-position: top;"
    "subcontrol-origin: margin;"
"}")
        css = cssa+cssb+cssc
        self.scroll.setStyleSheet(css)
        #
        self.vbox_1.addWidget(self.scroll)
        
        ################ the calendar
        thisMonth = QtCore.QDate().currentDate().month()
        thisYear = QtCore.QDate().currentDate().year()
        l_e = []
        # 
        for ev in self.window.list_events:
            tdata = ev.DTSTART
            ttime = ("{}:{}".format(tdata[9:11], tdata[11:13]))
            tdate = QtCore.QDate.fromString(ev.DTSTART[0:8], 'yyyyMMdd')
            l_e.append((tdate, ttime+" "+ev.SUMMARY))
        #
        l_e.sort()
        ###
        self.calendar = Calendar(self, l_e, self.vbox)
        self.calendar.setContentsMargins(0,0,0,0)
        self.calendar.setNavigationBarVisible(False)
        self.calendar.setVerticalHeaderFormat(QtWidgets.QCalendarWidget.NoVerticalHeader)
        self.hbox.addWidget(self.calendar)
        self.show()
        #
        if self.window.mw_is_shown:
            self.window.mw_is_shown.close()
            self.window.mw_is_shown = None
        if self.window.cwin_is_shown:
            self.window.cwin_is_shown.close()
            self.window.cwin_is_shown = None
        #
        cwWidth = self.width()
        cwHeight = self.height()
        cwX = (WINW-cwWidth)/2
        win_height = self.window.size().height()
        cwY = win_height
        if not with_compositor:
            cwY += 2
        self.setGeometry(cwX, cwY, -1,-1)
        
    #
    def go_today(self, e):
        to_day = QtCore.QDate().currentDate()
        self.calendar.setSelectedDate(to_day)
    #
    def on_prev_month(self):
        thisMonth = QtCore.QDate().currentDate().month()
        thisYear = QtCore.QDate().currentDate().year()
        selectedDate = self.calendar.selectedDate()
        selectedMonth = selectedDate.month()
        selectedYear = selectedDate.year()
        thisDay = 1
        if selectedMonth == 1:
            selectedYear -= 1
            selectedMonth = 13
        if (thisMonth == selectedMonth - 1) and (thisYear == selectedYear):
            thisDay = QtCore.QDate().currentDate().day()
        #
        self.calendar.setSelectedDate(QtCore.QDate(selectedYear, selectedMonth-1, thisDay))
        #
        nmonth2 = datetime.datetime.strptime(str(selectedMonth-1), '%m')
        nmonth = nmonth2.strftime('%B')
        self.mlabel.setText(str(nmonth)+" "+str(selectedYear))
    # 
    def on_next_month(self):
        thisMonth = QtCore.QDate().currentDate().month()
        thisYear = QtCore.QDate().currentDate().year()
        selectedDate = self.calendar.selectedDate()
        selectedMonth = selectedDate.month()
        selectedYear = selectedDate.year()
        thisDay = 1
        if selectedMonth == 12:
            selectedYear += 1
            selectedMonth = 0
        if (thisMonth == selectedMonth+1) and (thisYear == selectedYear):
            thisDay = QtCore.QDate().currentDate().day()
        #
        self.calendar.setSelectedDate(QtCore.QDate(selectedYear, selectedMonth+1, thisDay))
        #
        nmonth2 = datetime.datetime.strptime(str(selectedMonth+1), '%m')
        nmonth = nmonth2.strftime('%B')
        self.mlabel.setText(str(nmonth)+" "+str(selectedYear))
        #
        
class ClickLabel(QtWidgets.QLabel):
    clicked = QtCore.pyqtSignal()
    
    def mouseDoubleClickEvent(self, event):
        self.clicked.emit()
        QtWidgets.QLabel.mousePressEvent(self, event)      

# 
class Calendar(QtWidgets.QCalendarWidget):
  
    # constructor
    def __init__(self, parent=None, c_dict=None, vbox=None):
        super(Calendar, self).__init__(parent)
        self.events = c_dict
        self.cvbox = vbox
        self.color3 = QtGui.QColor(calendar_appointment_day_color)
        # day in the month
        self.clicked.connect(self.showDate)
        # year or month changed by user
        self.currentPageChanged.connect(self.pageChanded)
        # today
        c_today = self.selectedDate()
        self.popCalEv(c_today)
        #
        self.vw = self.findChild(QtWidgets.QTableView)
        self.vw.viewport().installEventFilter(self)
        #
    
    #
    def popCalEv(self, date):
        # remove all the existent widgets
        for i in reversed(range(self.cvbox.count())): 
            w = self.cvbox.itemAt(i).widget()
            if w is not None:
                w.deleteLater()
        #
        self.cvbox.addStretch()
        self.events_date = []
        for item in self.events:
            self.events_date.append(item[0])
            if item[0] == date:
                label = ClickLabel()
                label.setText(appointment_char+" "+item[1])
                label.setWordWrap(True)
                label.setStyleSheet("""
                      border: 3px solid;                                                                                                            
                      border-radius: 18%;
                      border-color: {};                                                                                                                
                      """.format(appointment_border_color)) 
                self.cvbox.addWidget(label)
    
    # day of the month changed by user
    def showDate(self, date):
        self.popCalEv(date)
    
    def pageChanded(self, year, month):
        date = self.selectedDate()
        self.popCalEv(date)
    
    def paintCell(self, painter, rect, date):
        super().paintCell(painter, rect, date)
        if date in self.events_date:
            psize = 20
            startPoint = QtCore.QPoint(rect.x()+rect.width(), rect.y()+rect.height()-psize)
            controlPoint1 = QtCore.QPoint(rect.x()+rect.width(), rect.y()+rect.height())
            controlPoint2 = QtCore.QPoint(rect.x()+rect.width()-psize, rect.y()+rect.height())
            endPoint = QtCore.QPoint(rect.x(), rect.y())
            #
            path = QtGui.QPainterPath(startPoint)
            path.lineTo(controlPoint1)
            path.lineTo(controlPoint2)
            painter.fillPath(path, self.color3)


#
class closeWin(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(closeWin, self).__init__(parent)
        self.window = window
        #
        # self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint | QtCore.Qt.Tool)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.FramelessWindowHint | QtCore.Qt.Tool | QtCore.Qt.WindowDoesNotAcceptFocus)
        #
        self.hbox = QtWidgets.QVBoxLayout()
        self.setLayout(self.hbox)
        ####### main box
        self.mbox = QtWidgets.QVBoxLayout()
        if with_compositor:
            self.frame = QtWidgets.QFrame(self)
            self.hbox.addWidget(self.frame)
            self.frame.setLayout(self.mbox)
            self.hbox.setContentsMargins(10, 2, 2, 10)
            self.mbox.setContentsMargins(10, 2, 10, 10)
            self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
            self.frame.setStyleSheet("background: palette(window); border-radius:{}px".format(border_radius))
            #
            if menu_left:
                shadow_effect = QtWidgets.QGraphicsDropShadowEffect(
                        blurRadius=blur_radius,
                        offset=QtCore.QPointF(-5, 5)
                    )
            else:
                self.hbox.setContentsMargins(2, 2, 10, 10)
                shadow_effect = QtWidgets.QGraphicsDropShadowEffect(
                        blurRadius=blur_radius,
                        offset=QtCore.QPointF(5, 5)
                    )
            self.setGraphicsEffect(shadow_effect)
        else:
            self.hbox.addLayout(self.mbox)
            self.hbox.setContentsMargins(2, 2, 2, 2)
            self.mbox.setContentsMargins(0, 0, 0, 0)
        #
        shut_icon = QtGui.QIcon("icons/system-shutdown.svg")
        self.shut = QtWidgets.QPushButton(shut_icon, "Shutdown")
        self.shut.clicked.connect(self.on_shut)
        self.mbox.addWidget(self.shut)
        self.shut.setDefault(True)
        #
        rest_icon = QtGui.QIcon("icons/system-restart.svg")
        self.rest = QtWidgets.QPushButton(rest_icon, "Restart")
        self.rest.clicked.connect(self.on_rest)
        self.mbox.addWidget(self.rest)
        #
        if logout_command:
            rest_logo = QtGui.QIcon("icons/system-logout.svg")
            self.logo = QtWidgets.QPushButton(rest_logo, "Logout")
            self.logo.clicked.connect(self.on_logo)
            self.mbox.addWidget(self.logo)
        #
        if self.window.cw_is_shown:
            self.window.cw_is_shown.close()
            self.window.cw_is_shown = None
        if self.window.mw_is_shown:
            self.window.mw_is_shown.close()
            self.window.mw_is_shown = None
        
        self.show()
        #
        sw = self.size().width()
        sh = self.size().height()
        win_width = WINW
        win_height = self.window.size().height()
        sy = win_height
        if menu_left:
            sx = win_width - sw
        else:
            sx = 0
        if not with_compositor:
            sy += 2
            if menu_left:
                sx -= 2
            else:
                sx += 2
        self.setGeometry(sx, sy, sw, sh)
    
    def process_finished(self):
        self.process = None
    
    #
    def on_shut(self):
        self.close()
        self.window.cwin_is_shown = None
        dlg = showDialog(2, "Shutdown?", self)
        result = dlg.exec_()
        ret = 0
        if result == QtWidgets.QDialog.Accepted:
            ret = 1
            dlg.close()
        else:
            dlg.close()
        #
        if ret:
            self.process = QtCore.QProcess()
            self.process.finished.connect(self.process_finished)
            self.process.start(shutdown_command)
    
    #
    def on_rest(self):
        self.close()
        self.window.cwin_is_shown = None
        dlg = showDialog(2, "Restart?", self)
        result = dlg.exec_()
        ret = 0
        if result == QtWidgets.QDialog.Accepted:
            ret = 1
            dlg.close()
        else:
            dlg.close()
        #
        if ret:
            self.process = QtCore.QProcess()
            self.process.finished.connect(self.process_finished)
            self.process.start(shutdown_command)
    
    #
    def on_logo(self):
        self.close()
        self.window.cwin_is_shown = None
        dlg = showDialog(2, "Logout?", self)
        result = dlg.exec_()
        ret = 0
        if result == QtWidgets.QDialog.Accepted:
            ret = 1
            dlg.close()
        else:
            dlg.close()
        #
        if ret:
            self.process = QtCore.QProcess()
            self.process.finished.connect(self.process_finished)
            self.process.start(shutdown_command)


################
if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    window = MainWin()
    ####
    screen = app.primaryScreen()
    size = screen.size()
    ####
    WINW = size.width()
    WINH = bar_size
    window.setGeometry(0, 0, WINW, WINH)
    window.setAttribute(QtCore.Qt.WA_X11NetWmWindowTypeDock)
    window.setWindowFlags(window.windowFlags() | QtCore.Qt.WindowDoesNotAcceptFocus)
    window.show()
    # the main window height (depending also on font size)
    WINH = window.size().height()
    windowID = int(window.winId())
    _display = Display()
    _window = _display.create_resource_object('window', windowID)
    x = 0
    _window.change_property(_display.intern_atom('_NET_WM_STRUT_PARTIAL'),
                           _display.intern_atom('CARDINAL'), 32,
                           [0, 0, WINH, 0, 0, 0, 0, 0, x, x+WINW-1, 0, 0],
                           X.PropModeReplace)
    #
    _display.sync()
    # set new style globally
    if theme_style:
        s = QtWidgets.QStyleFactory.create(theme_style)
        app.setStyle(s)
    # set the icon style globally
    if icon_theme:
        QtGui.QIcon.setThemeName(icon_theme)
    #
    def directory_changed(edir):
        #
        global Development
        Development = []
        global Education
        Education = []
        global Game
        Game = []
        global Graphics
        Graphics = []
        global Multimedia
        Multimedia = []
        global Network
        Network = []
        global Office
        Office = []
        global Settings
        Settings = []
        global System
        System = []
        global Utility
        Utility = []
        global Missed
        Missed = []
        #
        on_pop_menu(app_dirs_system, app_dirs_user)
    
    # check for changes in the application directories
    fPath = app_dirs_system + app_dirs_user
    fileSystemWatcher = QtCore.QFileSystemWatcher(fPath)
    fileSystemWatcher.directoryChanged.connect(directory_changed)
    
    def file_changed(efile):
        get_events()
    
    # check for changes in the calendar file
    if os.path.exists(fopen):
        epath = QtCore.QFileInfo(QtCore.QFile(fopen)).absoluteFilePath()
        fileSystemWatcher.addPath(epath)
        fileSystemWatcher.fileChanged.connect(file_changed)
    #
    ##### stalonetray
    if use_stalonetray:
        tray = "stalonetray"
        hpalette = window.palette().window().color().name()
        if WINH < int(tray_icon_size):
            tray_icon_size = str(bar_size)
            tray_y_offset = 0
        elif WINH > int(tray_icon_size):
            tray_icon_size = str(tray_icon_size)
            tray_y_offset = int((int(WINH) - int(tray_icon_size)) / 2)
        else:
            tray_y_offset = 0
            tray_icon_size = str(tray_icon_size)
        p = QtCore.QProcess()
        #
        def start_tray():
            try:
                p.start(tray, ["--skip-taskbar", "-geometry", "+{}+{}".format(WINW-tray_offset, tray_y_offset), "--icon-size", tray_icon_size, "--sticky", "--grow-gravity", "E", "--icon-gravity", "W", "--window-layer", "top", "--background", hpalette])
            except Exception as E:
                dlg = showDialog(1, "Something happend with the tray.\n{}".format(str(E)), window)
                result = dlg.exec_()
                dlg.close()
        start_tray()
        ret = app.exec_()
        p.terminate()
        time.sleep(0.5)
        sys.exit(ret)
    else:
        sys.exit(app.exec_())
    
###################
