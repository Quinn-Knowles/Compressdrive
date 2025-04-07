import os
import sys
import subprocess


def compress_with_7zip(filepath):
    output_file = filepath + ".mx9.7z"
    # Run 7zip with mx9
    cmd = ['7z', 'a', output_file, filepath, '-mx9']
    subprocess.run(cmd)
    
    
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python mx9.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    compress_with_7zip(file_path)
