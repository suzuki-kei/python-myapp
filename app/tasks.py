import os, sys, importlib
import invoke

sys.path.append(os.path.join(os.path.dirname(__file__), "tasks"))

namespace = invoke.Collection(*map(importlib.import_module, (
    "app",
    "test",
    "version",
)))

