from os import path

from invoke import Collection

from utils.modules import import_modules


namespace = Collection(*import_modules(path.join(path.dirname(__file__), "src", "tasks")))

