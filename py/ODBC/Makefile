#

ALL: ;

build:
	pyinstaller --onefile --icon=app.ico db_monitor.py
    
build_d:
	pyinstaller --onefile db_monitor.py
    
mon:
	nodemon --exec "c:/python27/python.exe" db_monitor


.PHONY: build