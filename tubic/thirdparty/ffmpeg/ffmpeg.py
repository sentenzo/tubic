import subprocess
import os

from tubic.misc import fix_path

location = fix_path("tubic/thirdparty/ffmpeg/bin/ffmpeg.exe")


def ffmpeg__to_mp3(
    from_file: str,
    bitrate: int = 192,
):
    # ffmpeg -i input.wav -vn -ar 44100 -ac 2 -b:a 192k output.mp3
    f_root, f_ext = os.path.splitext(from_file)
    if f_ext == ".mp3":
        return from_file
    to_file = os.path.join(f_root, ".mp3")

    ffmpeg_args = location
    ffmpeg_args.extend(["-i", from_file])
    ffmpeg_args.extend(["-b:a", f"{bitrate}k"])
    ffmpeg_args.append(to_file)
    subprocess.run(ffmpeg_args)

    return to_file
