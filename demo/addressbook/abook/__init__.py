import os
from os.path import expanduser

from . import config # relative import

storage_path = expanduser('~')
config.STORAGE_PATH = os.path.join(storage_path, '.contacts')
if not os.path.exists(config.STORAGE_PATH):
    os.mkdir(config.STORAGE_PATH)