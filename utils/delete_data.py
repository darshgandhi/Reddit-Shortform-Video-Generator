from pathlib import Path
import shutil

def empty_folders(path):
    folder = Path(path)
    for item in folder.iterdir():
        if item.is_file() or item.is_symlink():
            item.unlink()
        elif item.is_dir():
            shutil.rmtree(item)

empty_folders('./data/audio')
empty_folders('./data/screenshots')
empty_folders('./data/subtitles')
empty_folders('./data/video')