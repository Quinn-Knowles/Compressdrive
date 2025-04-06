import os
import sys
import subprocess

"""
Input: target file directory
Option: target ratio
Output: _
Script goal 1: run all compression scripts from resources folder on all "leaf" files in the target directory.
Script goal 2: keep the smallest version of all leaf files.
Script goal 3: if ratio is provided only keep leaf files under that ratio.
Script goal 4: if a file is under the target ratio, keep the result that's smallest.
"""

def process_file(file_path):
    """Process a single file to compress and compare sizes."""
    deflate = ["resources/deflate.py" , ".deflate.7z"]
    PPMD = ["resources/ppmd.py" , ".ppmd.7z"]
    mx9 = ["resources/mx9.py" , ".mx9.7z"]
    windows = ["resources/windows.py", ".win.zip"]
    """lzma = ["resources/lzma.py", ".xz"]"""
    algorithms = [deflate, PPMD, mx9, windows]
    
    
    original_size = os.path.getsize(file_path)
    open(file_path + ".7z", 'a').close()
    best = original_size
    for algorithm in algorithms:
        subprocess.run([sys.executable, algorithm[0], file_path])
        if os.path.getsize(file_path + algorithm[1]) < best:
            os.remove(file_path + ".7z")
            os.rename(file_path +algorithm[1], file_path + ".7z")
            best = os.path.getsize(file_path + ".7z")
        else:
            os.remove(file_path +algorithm[1])
    if best != original_size:
        os.remove(file_path)
    else:
        os.remove(file_path + ".7z")

def process_file_by_ratio(file_path, ratio):
    """Process a single file and keep compressed versions under the target ratio."""
    deflate = ["resources/deflate.py", ".deflate.7z"]
    PPMD = ["resources/ppmd.py", ".ppmd.7z"]
    mx9 = ["resources/mx9.py", ".mx9.7z"]
    windows = ["resources/windows.py", ".win.zip"]
    algorithms = [deflate, PPMD, mx9, windows]

    original_size = os.path.getsize(file_path)
    target_size = original_size * (ratio / 100)

    open(file_path + ".7z", 'a').close()
    best = original_size

    for algorithm in algorithms:
        subprocess.run([sys.executable, algorithm[0], file_path])
        compressed_path = file_path + algorithm[1]
        compressed_size = os.path.getsize(compressed_path)

        if compressed_size < best and compressed_size <= target_size:
            os.remove(file_path + ".7z")
            os.rename(compressed_path, file_path + ".7z")
            best = os.path.getsize(file_path + ".7z")
        else:
            os.remove(compressed_path)

    # If no compressed file met the ratio, remove placeholder
    if best == original_size:
        os.remove(file_path + ".7z")
    
   
    


def process_directory(directory, ratio):
    """Recursively process all files in the given directory."""
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if(ratio == None):
                process_file(file_path)
            else: 
                process_file_by_ratio(file_path, ratio)

if __name__ == "__main__":
    if len(sys.argv) not in [2, 3]:
        print("Usage: python script.py <directory> [<Ratio>]")
        sys.exit(1)
    
    directory = sys.argv[1]
    if not os.path.isdir(directory):
        print("Error: Provided path is not a directory.")
        sys.exit(1)
    
    ratio = None
    if len(sys.argv) == 3:
        ratio = float(sys.argv[2])
        if not (0 < ratio <= 100):
            print("Error: Ratio should be between 0 and 100.")
            sys.exit(1)
    
    process_directory(directory, ratio)
