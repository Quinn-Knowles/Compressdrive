import os
import subprocess
import sys
import shutil

"""
input: target file directory
option: target ratio
output: _

script goal 1: run all compression scripts from resourcess folder on all folders in target directory.
???stretch??? script goal 2: if leaf files are present in target directory, compress them to a single file
script goal 3: if ratio is provided only keep leaf files under that ratio
script goal 4: if a file is under the target ratio, keep the result thats smallest. 
"""

def get_folder_size(folder_path):
    total_size = 0
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isfile(item_path):
            total_size += os.path.getsize(item_path)
        elif os.path.isdir(item_path):
            total_size += get_folder_size(item_path)
    return total_size
    
    

def process_folder(folder_path):
    """Compress a folder using multiple algorithms and keep the best result."""
    deflate = ["resources/deflate.py", ".deflate.7z"]
    PPMD = ["resources/ppmd.py", ".ppmd.7z"]
    mx9 = ["resources/mx9.py", ".mx9.7z"]
    windows = ["resources/windows.py", ".win.zip"]
    algorithms = [deflate, PPMD, mx9, windows]

    original_size = get_folder_size(folder_path)
    best = original_size
    best_output = None

    for algorithm in algorithms:
        subprocess.run([sys.executable, algorithm[0], folder_path])
        output_path = folder_path + algorithm[1]
        if os.path.exists(output_path):
            compressed_size = os.path.getsize(output_path)
            if compressed_size < best:
                if best_output and os.path.exists(best_output):
                    os.remove(best_output)
                best = compressed_size
                best_output = output_path
            else:
                os.remove(output_path)

    if best_output:
        # Rename best to .7z for consistency
        final_output = folder_path + ".7z"
        os.rename(best_output, final_output)
        try:
            shutil.rmtree(folder_path)
        except Exception as e:
            print(f"Could not delete folder: {folder_path} — {e}")
    else:
        print(f"No effective compression for: {folder_path}")
    


def process_directory(directory, ratio):
    """Process all top-level folders in the given directory."""
    for entry in os.listdir(directory):
        folder_path = os.path.join(directory, entry)
        if os.path.isdir(folder_path):
            if ratio is None:
                process_folder(folder_path)
            """else:
                process_file_by_ratio(folder_path, ratio)"""

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