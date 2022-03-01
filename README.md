# qt5simplebar

A simple dock with menu and calendar.

Free to use and modify.

This program needs:
- python3
- pyqt5
- python3-xdg
- Xorg
- stalonetray (optional - not integrated in the program)

Some options can be changed in the cfg.py config file.

The file 'delete_me' in the bookmarks folder must be deleted before launching the program.

The pictures below are self-explanatory. The calendar applet can read calendar ics files, and update its content. Double click on an calendar event lauch a program, if setted in the config file; an argument in the form yyyymmdd (e.g. 20220301) will be passed to the program. Single click on the month label in the calendar to select today. The menu applet shows all the applications installed or added by the user. Right click on the program to add it as bookmark. Right click on the bookmark to remove it. Type in something in the bottom for searching an installed program. The bar has its menu for reloading (changements in the config are taken into accout) and exiting.

With compositing on:
![My image](https://github.com/frank038/qt5simplebar/blob/main/screenshot1.png)

With no compositing and in reverse order:
![My image](https://github.com/frank038/qt5simplebar/blob/main/screenshot2.png)

With Stalonetray:
![My image](https://github.com/frank038/qt5simplebar/blob/main/screenshot3.png)
