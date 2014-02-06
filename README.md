Quick thingy to watch and copy .jsp files to src/ as you're working on them in target/.

Could theoretically be used in reverse too.

installation:

`sudo easy_install watchdog`

usage:

`python target_practice.py ../src/`

(watches the current working directory recursively, first arg is where to copy to)

TODO: add ability to specify different extensions and the watcher directory
