import os
import sys
import subprocess


def compress_with_7zip(filepath):
    output_file = filepath + ".deflate.7z"
    
    # Run 7zip with DEFLATE
    cmd = ['7z', 'a', output_file, filepath, '-m1=Deflate']
    subprocess.run(cmd)
    
    size = os.path.getsize(output_file)
    
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python deflate_test.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    compress_with_7zip(file_path)
