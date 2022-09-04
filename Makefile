
# https://stackoverflow.com/a/4511164/2493536
ifdef OS # Windows
   RM = del /Q /S #Remove-Item -Recurse -Force -LiteralPath
   FixPath = $(subst /,\,$1)
   PYTHON = python
   EXT = .exe
else
   ifeq ($(shell uname), Linux) # Linux
      RM = rm -rf
	  FixPath = $1
	  PYTHON = python3.10
   endif
endif

# APP_FILE = app
APP_FILE = app_gui

APP_NAME = yt-dpl-qt6

ENTRY_POINT = ./src/$(APP_FILE).py

all: build

pyui:
	pyuic6 -o ./src/qt/pyui/main_window.py \
	       -x ./src/qt/ui/main_window.ui

build: pyui
	pyinstaller --workpath ./.pyinstaller/build \
	            --distpath ./bin \
	            --specpath ./.pyinstaller \
	            --noconsole \
	            --onefile \
	            --name $(APP_NAME) \
	            --icon ../rec/ico/file-video.ico \
	            --add-data ../rec/ico/*;./rec/ico \
	            $(ENTRY_POINT)

run:
	./bin/$(APP_NAME)

runpy: pyui
	$(PYTHON) $(ENTRY_POINT)

clean:
	$(RM) $(call FixPath,./bin/*)
	$(RM) $(call FixPath,./.pyinstaller/*)
