
# https://stackoverflow.com/a/4511164/2493536
# ifdef OS
#    RM = Remove-Item -Recurse -Force -LiteralPath 
#    RD = rd
#    FixPath = $(subst /,\,$1)
# else
#    ifeq ($(shell uname), Linux)
#       RM = rm -rf
# 	  FixPath = $1
#    endif
# endif

build:
	pyinstaller --workpath ./.pyinstaller/build --distpath ./bin --specpath ./.pyinstaller  --onefile ./app.py

run:
	./bin/app.exe

# clean:
# 	$(RM) "bin"
# 	$(RM) ./.pyinstaller