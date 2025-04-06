import os
import sys
import time
import subprocess
import deflate

def compress(filepath):
    level = 6  # Compression level (usually 1-12 for libdeflate)
    with open(filepath, "rb") as file:
        data = file.read()
    
    # DEFLATE compression (raw)
    compressed_deflate = deflate.deflate_compress(data, level)
    
    # zlib compression
    compressed_zlib = deflate.zlib_compress(data, level)

    # Write zlib-compressed data to a file
    out_path = filepath + ".zlib"
    with open(out_path, "wb") as file:
        file.write(compressed_zlib)
    
    print(f"Compressed (zlib) file written to: {out_path}")

def compress_with_7zip(filepath):
    start_time = time.time()
    output_file = filepath + ".deflate.7z"
    
    # Run 7zip with DEFLATE
    cmd = ['7z', 'a', output_file, filepath, '-m1=Deflate']
    subprocess.run(cmd)
    
    end_time = time.time()
    size = os.path.getsize(output_file)
    
    print(f"7-Zip Deflate compression finished.")
    print(f"Output file: {output_file}")
    print(f"Size: {size} bytes")
    print(f"Time taken: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python deflate_test.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    compress(file_path)
    compress_with_7zip(file_path)
