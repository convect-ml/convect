import sys
from convect import Sdk


def main():
    if sys.argv[0].endswith("convect") and sys.argv[1] == "hello" and len(sys.argv) == 2:
        Sdk("").hello()
    else:
        print("Invalid usage of convect. Try:\n\nconvect hello")
