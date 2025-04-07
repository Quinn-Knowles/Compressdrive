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




"""
Input: path to a 'leaf' node of a directory
output: most compressed file
script goal 1: go through all  listed algorithms
script goal 2: find smallest resulting file
script goal 3: remove other files 
"""
def process_file(file_path): 
    #define implemented algorithms
    deflate = ["resources/deflate.py" , ".deflate.7z"]
    PPMD = ["resources/ppmd.py" , ".ppmd.7z"]
    mx9 = ["resources/mx9.py" , ".mx9.7z"]
    windows = ["resources/windows.py", ".win.zip"]
    """lzma = ["resources/lzma.py", ".xz"]"""
    algorithms = [deflate, PPMD, mx9, windows]
    
    
    original_size = os.path.getsize(file_path) #get original file size
    open(file_path + ".7z", 'a').close()       #create a placeholder file for os.remove statements
    best = original_size                       #create tracker for goal file size
    
    
    for algorithm in algorithms: #iterate through algorithms, keep the best result
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


"""
Input: path to a 'leaf' node of a directory, target compression ratio 
output: most compressed file
script goal 1: go through all  listed algorithms
script goal 2: find smallest resulting file which meets ratio criteria 
script goal 3: remove other files 
"""
def process_file_by_ratio(file_path, ratio):
    #define implemented algorithms
    deflate = ["resources/deflate.py", ".deflate.7z"]
    PPMD = ["resources/ppmd.py", ".ppmd.7z"]
    mx9 = ["resources/mx9.py", ".mx9.7z"]
    windows = ["resources/windows.py", ".win.zip"]
    algorithms = [deflate, PPMD, mx9, windows]

    original_size = os.path.getsize(file_path)  #get original file size
    target_size = original_size * (ratio / 100) #get target size for later comparison 
    open(file_path + ".7z", 'a').close()        #create a placeholder file for os.remove statements
    best = original_size                        #create tracker for goal file size


    for algorithm in algorithms:                #iterate through algorithms, keep the best result
        subprocess.run([sys.executable, algorithm[0], file_path])
        compressed_path = file_path + algorithm[1]
        compressed_size = os.path.getsize(compressed_path)

        if compressed_size < best and compressed_size <= target_size: #if file meets standards
            os.remove(file_path + ".7z")
            os.rename(compressed_path, file_path + ".7z")
            best = os.path.getsize(file_path + ".7z")
        else:                                                         #else remove file
            os.remove(compressed_path)
    if best == original_size:
        os.remove(file_path + ".7z")


"""
Input: directory,  optional: [ratio] (else None)
output: -
script goal 1: pass individual files off to file process
"""
def process_directory(directory, ratio):
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if(ratio == None):                  #if user didn't enter ratio
                process_file(file_path)
                
            else:                               #else
                process_file_by_ratio(file_path, ratio)

if __name__ == "__main__":
    if len(sys.argv) not in [2, 3]: #handle no arguments, handle too many arguments (incorrect usage
        print("Usage: python script.py <directory> [<Ratio>]")
        sys.exit(1)
    
    directory = sys.argv[1]
    if not os.path.isdir(directory): #handle wrong argument
        print("Error: Provided path is not a directory.")
        sys.exit(1)
    
    ratio = None
    if len(sys.argv) == 3:
        ratio = float(sys.argv[2]) #handle wrong argument
        if not (0 < ratio <= 100):
            print("Error: Ratio should be between 0 and 100.")
            sys.exit(1)
    
    process_directory(directory, ratio) #run core functions
