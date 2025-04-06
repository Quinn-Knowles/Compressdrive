import os
import sys
import subprocess


def compress_with_windows(filepath):
    output_file = filepath + ".win.zip"
    
    # Run 7zip with DEFLATE
    cmd = ['powershell', '-Command', f'Compress-Archive -Path "{filepath}" -DestinationPath "{output_file}"']
    subprocess.run(cmd)
    
    
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python windows.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    compress_with_windows(file_path)

