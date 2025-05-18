# /opt/navi-organizer/navi-organizer.py

import time
import shutil
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Directory to watch
WATCH_DIR = '/home/boba/Mainframe/drop'

# Define target directories
TARGETS = {
    # TEXT type format file extensions & locations
    '.txt': '/home/boba/Mainframe/navi/assets/documents',
    '.pdf': '/home/boba/Mainframe/navi/assets/documents',
    '.doc': '/home/boba/Mainframe/navi/assets/documents',
    '.docx': '/home/boba/Mainframe/navi/assets/documents',
    '.xls': '/home/boba/Mainframe/navi/assets/documents',
    '.xlsx': '/home/boba/Mainframe/navi/assets/documents',
    '.ppt': '/home/boba/Mainframe/navi/assets/documents',
    '.pptx': '/home/boba/Mainframe/navi/assets/documents',
    '.odt': '/home/boba/Mainframe/navi/assets/documents',
    '.ods': '/home/boba/Mainframe/navi/assets/documents',
    '.odp': '/home/boba/Mainframe/navi/assets/documents',
    '.pages': '/home/boba/Mainframe/navi/assets/documents',
    # CODE type format file extensions & locations
    '.py': '/home/boba/Mainframe/navi/assets/code',
    '.js': '/home/boba/Mainframe/navi/assets/code',
    '.html': '/home/boba/Mainframe/navi/assets/code',
    '.css': '/home/boba/Mainframe/navi/assets/code',
    '.java': '/home/boba/Mainframe/navi/assets/code',
    '.cpp': '/home/boba/Mainframe/navi/assets/code',
    '.c': '/home/boba/Mainframe/navi/assets/code',
    '.cs': '/home/boba/Mainframe/navi/assets/code',
    '.php': '/home/boba/Mainframe/navi/assets/code',
    '.rb': '/home/boba/Mainframe/navi/assets/code',
    '.go': '/home/boba/Mainframe/navi/assets/code',
    '.swift': '/home/boba/Mainframe/navi/assets/code',
    '.ts': '/home/boba/Mainframe/navi/assets/code',
    '.sh': '/home/boba/Mainframe/navi/assets/code',
    '.bat': '/home/boba/Mainframe/navi/assets/code',
    '.ps1': '/home/boba/Mainframe/navi/assets/code',
    '.sql': '/home/boba/Mainframe/navi/assets/code',
    '.json': '/home/boba/Mainframe/navi/assets/code',
    '.xml': '/home/boba/Mainframe/navi/assets/code',
    '.yaml': '/home/boba/Mainframe/navi/assets/code',
    '.yml': '/home/boba/Mainframe/navi/assets/code',
    '.toml': '/home/boba/Mainframe/navi/assets/code',
    '.md': '/home/boba/Mainframe/navi/assets/code',
    '.csv': '/home/boba/Mainframe/navi/assets/code',
    # IMAGE type format file extensions & locations
    '.mpg': '/home/boba/Mainframe/navi/assets/media/video',
    '.png': '/home/boba/Mainframe/navi/assets/media/images',
    '.jpg': '/home/boba/Mainframe/navi/assets/media/images',
    # ANIMATION type format file extensions & locations
    '.gif': '/home/boba/Mainframe/navi/assets/media/gif',
    # VIDEO type format file extensions & locations
    '.mp4': '/home/boba/Mainframe/navi/assets/media/video',
    '.avi': '/home/boba/Mainframe/navi/assets/media/video',
    '.mov': '/home/boba/Mainframe/navi/assets/media/video',
    '.mkv': '/home/boba/Mainframe/navi/assets/media/video',
    # SOUND type format file extensions & locations
    '.mp3': '/home/boba/Mainframe/navi/assets/media/audio',
    '.wav': '/home/boba/Mainframe/navi/assets/media/audio',
    '.flac': '/home/boba/Mainframe/navi/assets/media/audio',
    # COMPRESSED type format file extensions & locations
    '.zip': '/home/boba/Mainframe/navi/assets/compressed',
}

# Make sure that the target folders exist
for path in TARGETS.values():
    os.makedirs(path, exist_ok=True)


class NaviHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            filepath = event.src_path
            _, ext = os.path.splitext(filepath)
            ext = ext.lower()
            target_dir = TARGETS.get(ext)
            if target_dir:
                print(f"Detected {ext} file. Moving {filepath} -> {target_dir}")
                shutil.move(filepath, os.path.join(target_dir, os.path.basename(filepath)))
            else:
                print(f"Unknown file type: {filepath}. Ignoring.")


if __name__ == "__main__":
    print(f"Starting Navi-Organizer! Watching: {WATCH_DIR}")
    event_handler = NaviHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCH_DIR, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
