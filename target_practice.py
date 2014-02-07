import sys
import os
import time
import shutil
import argparse
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

cwd = os.getcwd()
cwd_len = len(cwd) + 1
abs_path = None
extensions = None

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
            print("Successfully copied " + new_path)
        except Exception:
            sys.stderr.write("Failed to copy file.\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            description='Watch jsp files in current target directory and copy them to source.')
    parser.add_argument('source', help='The source directory', action="store")

    # TODO: needs validation
    parser.add_argument('-e', '--extension', help='Comma separated ext list.', default='jsp')

    args = parser.parse_args()
    abs_path = os.path.abspath(args.source)
    extensions = ['.' + x.lower() for x in args.extension.split(',')]
    if not os.path.isdir(abs_path):
        sys.stderr.write("Source is not a directory.\n")
        sys.exit(1)
    event_handler = FsHandler()
    observer = Observer()
    print("Watching: " + cwd)
    print("Source: " + abs_path)
    print("Extensions: " + str(extensions))
    observer.schedule(event_handler, path=cwd, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
