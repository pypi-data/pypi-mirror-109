from os.path import dirname, join


def version() -> str:
    with open(join(dirname(__file__), "resources", "VERSION")) as f:
        return f.read().strip()


__version__ = version()
