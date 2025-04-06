import os
import struct



"""
input: target file directory
option: target ratio
output: _

script goal 1: run all compression scripts from resourcess folder on all folders in target directory.
??? script goal 2: if leaf files are present in target directory, compress them to a single file
script goal 3: if ratio is provided only keep leaf files under that ratio
script goal 4: if a file is under the target ratio, keep the result thats smallest. 
"""

def process_directory(directory,ratio):
    """Recursively process all files in the given directory."""
    print( os.walk(directory))
    
    
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <directory> <CompRatio>")
        sys.exit(1)
    
    directory = sys.argv[1]
    ratio = sys.argv[2]
    if not os.path.isdir(directory):
        print("Error: Provided path is not a directory.")
        sys.exit(1)
    
    process_directory(directory,ratio)