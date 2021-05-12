import sys
from convect import Sdk


def main():
    if sys.argv[0].endswith("convect") and sys.argv[1] == "ready" and len(sys.argv) == 2:
        Sdk("").ready()
    else:
        print("Invalid usage of convect. Try:\n\nconvect ready")
