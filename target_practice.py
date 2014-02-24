import sys
import os
import time
import shutil
import argparse
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

cwd = None
cwd_len = None
abs_path = None
extensions = None

STARTC = '\033[91m'
ENDC = '\033[0m'

class FsHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return
        dot_idx = event.src_path.rfind('.')
        if dot_idx == -1 or event.src_path[dot_idx:].lower() not in extensions:
            return
        print("File modified: " + event.src_path)
        rel_path = event.src_path[cwd_len:]
        new_path = os.path.join(abs_path, rel_path)
        if not os.path.isfile(new_path):
            print("No version found in source. Skipping.")
            return

        try:
            shutil.copyfile(event.src_path, new_path)
            print("Successfully copied to: " + new_path)
        except Exception:
            sys.stderr.write("Failed to copy file.\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            description='Watch jsp files in current "watch" directory and copy them to target.')
    parser.add_argument('target', help='The target directory', action="store")
    parser.add_argument('-e', '--extension', help='Comma separated ext list.', default='jsp')
    parser.add_argument('-w', '--watch', action='store', default=os.getcwd(),
            help="The directory to watch (defaults to cwd).")
    args = parser.parse_args()

    cwd = os.path.abspath(args.watch)
    abs_path = os.path.abspath(args.target)
    extensions = ['.' + x.lower() for x in args.extension.split(',')]
    if not os.path.isdir(abs_path):
        sys.stderr.write("Target is not a directory.\n")
        sys.exit(1)
    if not os.path.isdir(cwd):
        sys.stderr.write("Watch is not a directory.\n")
        sys.exit(1)
    cwd_len = len(cwd) + 1
    event_handler = FsHandler()
    observer = Observer()
    print(STARTC+"Watching: " + cwd)
    print("Target: " + abs_path)
    print("Extensions: " + str(extensions)+ENDC)
    observer.schedule(event_handler, path=cwd, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
