
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

ENTRY_POINT = ./src/app.py

build:
	pyinstaller --workpath ./.pyinstaller/build --distpath ./bin --specpath ./.pyinstaller  --onefile $(ENTRY_POINT)

run:
	./bin/app

runpy:
	$(PYTHON) $(ENTRY_POINT)

clean:
	$(RM) $(call FixPath,./bin/*)
	$(RM) $(call FixPath,./.pyinstaller/*)
