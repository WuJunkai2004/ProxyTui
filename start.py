#qqq#!/usr/bin/python3

import sys

from src import app
from src import lang

if(__name__ == "__main__" and len(sys.argv) == 1):
    exit(app.ClashUI().run())

if(len(sys.argv) == 2):
    exit(app.command(sys.argv[1]))

print(lang.get("help"))
exit(1)