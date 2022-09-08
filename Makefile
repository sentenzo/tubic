
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
	    --add-data ../$(PACKAGE_NAME)/rec/ico/*;./$(PACKAGE_NAME)/rec/ico \
		$(PACKAGE_NAME)/__main__.py

run:
	./bin/$(PACKAGE_NAME)

runpy: pyui
	poetry run python -m $(PACKAGE_NAME)

clean:
	$(RM) $(call FixPath,./bin/*)
	$(RM) $(call FixPath,./.pyinstaller/*)

test: pyui
	poetry run python -m pytest -m "not slow" --verbosity=2 --showlocals --log-level=DEBUG

test-full: pyui
	poetry run python -m pytest --verbosity=2 --showlocals --log-level=DEBUG