

# tubic
<div align="center">

![Screenshot](tubic.webp)

</div>
A simple lightweight portable single-file program to download videos from YouTube.

---

Why making another YouTube downloader, when we already have `%YOUR_FAVORITE_APP_NAME%`, which is a lot better, than this stuff will ever be?

Well...

~~Just for fun~~

~~Because I can~~

I've been trying out several tools of that kind, and each one of them had some flaw critical for me. Such as:
 
 - overweight — installing TarTube once took me something about half an hour
 - console-only — so I was unable to recomend it to my elderly relatives and non-IT friends
 - comercial
 - server-side component — so at some point you find your tool turned into a pumpkin because the servers are down (that's exactly what happaned with me once)
 - overly complex GUI (again elderly relatives won't appriciate)

I feel an unfulfilled demand for a very simple tool, which would:
- -be able to download both video and audio by a YouTube link
- -have a simple GUI (the less buttons — the better)
- -be portable (ideally: packed in a single executable)

The features I (subjectively) consider redundant:
- sequential download from a list of links
- post-processing (`video: 1080p → 780p` or `audio: 320 kbps → 96 kbps`)
- converting formats (`mp4 → mkv` or `webm → mp3`) 

So that's how I've decided to make this stuff.

It uses [yt-dlp](https://github.com/yt-dlp/yt-dlp) (and utilizes probably less then 5% of it's full functionality). 

The UI is implemented with [PyQt6](https://pypi.org/project/PyQt6/).

The application is packed in a single executable file with no dependencies (thanks to [`pyinstaller`](https://pypi.org/project/pyinstaller/)).

The target OS is currently Windows ≥ 10. Though, there's no OS-dependent features or libs used, so you're free to try and build it on Linux.

--- 

## Building

### Software requirements
- [**python3.10**](https://www.python.org/downloads/)

- [**make**](https://en.wikipedia.org/wiki/Make_(software)) tool — for build-automation. To install it on Windows, one can try [`GNU make 4.3`](https://community.chocolatey.org/packages/make)  package from the [Chocolatey](https://github.com/chocolatey/choco) package manager.

- [**Poetry**](https://python-poetry.org/) — to administer Python depandancies.

- **Qt Designer** — to edit `*.ui` files (to draw windows and GUI elements in WYSIWYG editor). Versions `5.*` and `6.*` are equaly suitable. To install it there are several options:
    - a [third party standalone installer](https://build-system.fman.io/qt-designer-download)
    - a [PySide6 pip package](https://pypi.org/project/PySide6/) (`pip install PySide6` or `poetry add -D PySide6`, and then run `pyside6-designer`)
    - the [official site](https://www.qt.io/) — ironicaly, not the best way, cause it is not destrebuted separately from all the over Qt tools and requites registration

### First run
In the project directory execute:

```bash
poetry install
```
\- to download all the Python packages required. 

That's all.

### GUI editing

Qt Designer related files can be found at `tubic/qt_wrap/ui`.

### Basic `make` tergets
- `make test` — run unit tests
- `make runpy` — run app with Python
- `make build` — create an executable in a `bin` folder
---

## License

- Current repository is licensed under [MIT License](https://github.com/sentenzo/tubic/blob/master/LICENSE)
- The icons for this application were taken from paomedia's [small-n-flat](https://github.com/paomedia/small-n-flat) set and licensed under [CC0 1.0 Universal](https://github.com/paomedia/small-n-flat/blob/master/LICENSE)
