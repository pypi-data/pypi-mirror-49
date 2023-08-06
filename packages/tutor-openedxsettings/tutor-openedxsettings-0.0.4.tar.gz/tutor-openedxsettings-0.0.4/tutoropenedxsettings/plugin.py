import os
from glob import glob

HERE = os.path.abspath(os.path.dirname(__file__))

config = {
    "add": {
        "LMS": {},
        "CMS": {},
        "LMS_HOOK": [],
        "CMS_HOOK": [],
    },
}

templates = os.path.join(HERE, "templates")

hooks = {
    "init": ["lms", "cms"],
}


def patches():
    all_patches = {}
    for path in glob(os.path.join(HERE, "patches", "*")):
        with open(path) as patch_file:
            name = os.path.basename(path)
            content = patch_file.read()
            all_patches[name] = content
    return all_patches
