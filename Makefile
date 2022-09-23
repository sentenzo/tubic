
# https://stackoverflow.com/a/4511164/2493536
ifdef OS # Windows
   PYTHON = python
   PATH_ARG_SEP=;
else
   ifeq ($(shell uname), Linux) # Linux
	  PYTHON = python3.10
	  PATH_ARG_SEP=:
   endif
endif


PACKAGE_NAME = tubic

all: build

pyui:
	poetry run python -m PyQt6.uic.pyuic \
	    -o ./$(PACKAGE_NAME)/qt_wrap/pyui/main_window.py \
	    -x ./$(PACKAGE_NAME)/qt_wrap/ui/main_window.ui

build: pyui
	poetry run pyinstaller \
	    --workpath ./.pyinstaller/build \
	    --distpath ./bin \
	    --specpath ./.pyinstaller \
	    --noconsole \
	    --onefile \
	    --name $(PACKAGE_NAME) \
	    --icon ../$(PACKAGE_NAME)/rec/ico/file-video.ico \
	    --add-data ../$(PACKAGE_NAME)/rec/ico/*$(PATH_ARG_SEP)./$(PACKAGE_NAME)/rec/ico \
		--add-data ../$(PACKAGE_NAME)/thirdparty/ffmpeg/bin/*$(PATH_ARG_SEP)./$(PACKAGE_NAME)/thirdparty/ffmpeg/bin \
		$(PACKAGE_NAME)/__main__.py

run:
	./bin/$(PACKAGE_NAME)

runpy: pyui
	poetry run python -m $(PACKAGE_NAME)

test: pyui
	poetry run python -m pytest -m "not slow" --verbosity=2 --showlocals --log-level=DEBUG

test-full: pyui
	poetry run python -m pytest --verbosity=2 --showlocals --log-level=DEBUG
