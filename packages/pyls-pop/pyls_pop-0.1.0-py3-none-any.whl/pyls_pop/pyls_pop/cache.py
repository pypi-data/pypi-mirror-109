"""
Manage the pop-tree cache
"""
import json
import pathlib
import pickle
import sys
import tempfile
import filelock
import threading


def __init__(hub):
    tempdir = pathlib.Path(tempfile.gettempdir(), "pyls_pop")
    tempdir.mkdir(exist_ok=True, parents=True)
    hub.pyls_pop.cache.LOCK = filelock.FileLock(str(tempdir / ".lock"))
    hub.pyls_pop.cache.EVENT = FileEvent(tempdir / ".event")
    hub.pyls_pop.cache.FILE = tempdir / "cache.pickle"


class FileEvent(threading.Event):
    def __init__(self, f: pathlib.Path):
        self.file = f
        threading.Event.__init__(self)

    @property
    def _flag(self):
        return self.file.exists()

    @_flag.setter
    def _flag(self, value: bool):
        if value:
            self.file.touch(exist_ok=True)
        else:
            try:
                self.file.unlink()
            except FileNotFoundError:
                ...


async def create(hub):
    # Only one create should run at a time
    with hub.pyls_pop.cache.LOCK:
        if hub.pyls_pop.cache.check():
            hub.pyls_pop.cache.EVENT.set()
            return
        # Cache needs to be updated
        hub.pyls_pop.cache.EVENT.clear()
        tree = await hub.tree.init.traverse()
        refs = hub.tree.ref.list(tree)
        refs = json.loads(hub.output.json.display(refs))
        with hub.pyls_pop.cache.FILE.open("wb+") as fh:
            pickle.dump({"refs": refs, "path": sys.path}, fh)
        hub.pyls_pop.cache.EVENT.set()


def check(hub) -> bool:
    """
    See if the cache is up-to-date
    """
    # Check if cache doesn't exist
    if not hub.pyls_pop.cache.FILE.exists():
        return False
    # Check if dependencies have changed
    with hub.pyls_pop.cache.FILE.open("rb") as fh:
        try:
            data = pickle.load(fh)
            if data.get("path") != sys.path:
                return False
            return True
        except EOFError:
            return False
    # Check if current line has added a function to a pop project in the environment


def get(hub):
    """
    Read the cache and return the json results of pop-tree
    """
    if not hub.pyls_pop.cache.EVENT.wait(timeout=5):
        return {}
    with hub.pyls_pop.cache.FILE.open("rb") as fh:
        data = pickle.load(fh)

    return data.get("refs")


def clear(hub):
    """
    Remove the cache
    """
    with hub.pyls_pop.cache.LOCK:
        hub.pyls_pop.cache.FILE.unlink(missing_ok=True)
        hub.pyls_pop.cache.EVENT.clear()
