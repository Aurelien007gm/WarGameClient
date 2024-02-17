# main.py

from view import playerview  
import os
import sys

if __name__ == "__main__":
    script_folder = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(script_folder)
    playerview.main() 