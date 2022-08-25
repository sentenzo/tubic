build:
	pyinstaller --workpath .\.pyinstaller\build --distpath .\bin --specpath .\.pyinstaller  --onefile .\app.py
