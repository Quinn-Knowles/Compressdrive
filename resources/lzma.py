import lzma
import sys
import os

def compress_with_lzma(filepath):
    output_file = filepath + ".xz"
    # Run py module LZMA
    with open(filepath, "rb") as f:
        data = f.read()
    with lzma.open(output_file, "w") as f:
        f.write(data)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python lzma.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]

    if not os.path.isfile(file_path):
        print("Error: Provided path is not a file.")
        sys.exit(1)

    compress_with_lzma(file_path)
