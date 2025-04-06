import os
import sys
import subprocess

def process_directory(directory,ratio):
    """Recursively process all files in the given directory."""
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            result = subprocess.run([sys.executable, "resources/identifier.py", file_path, ratio])
            print(result)
            if result == 1:
                subprocess.run([sys.executable, "resources/deflate.py", file_path])

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