import os
import sys
import subprocess
import time

def log_compression_data(file_path, original_size, algorithm_data, header=False):
    """Logs the compression results to a file called output.txt."""
    file_name = os.path.basename(file_path)  # Extract the file name from the full path
    with open("logs/output.txt", "a") as log_file:
        if header:
            # Write headers once
            log_file.write(f"file name, original_size, ")
            header_str = ", ".join([f"{data['compressed_size']}, {data['compression_ratio']}, {data['time_taken']}" for data in algorithm_data])
            log_file.write(header_str + "\n")
        else:
            # Write the data for a specific file
            log_file.write(f"{file_name}, {original_size}, ")
            data_str = ", ".join([f"{data['compressed_size']}, {data['compression_ratio']:.4f}, {data['time_taken']:.4f}" for data in algorithm_data])
            log_file.write(data_str + "\n")

def process_file(file_path):
    """Process a single file to compress and compare sizes, then log results."""
    deflate = ["resources/deflate.py", ".deflate.7z"]
    PPMD = ["resources/ppmd.py", ".ppmd.7z"]
    mx9 = ["resources/mx9.py", ".mx9.7z"]
    windows = ["resources/windows.py", ".win.zip"]
    algorithms = [deflate, PPMD, mx9, windows]
    
    original_size = os.path.getsize(file_path)
    algorithm_data = []
        
    for algorithm in algorithms:
        start_time = time.time()
        subprocess.run([sys.executable, algorithm[0], file_path])
        end_time = time.time()
        
        compressed_path = file_path + algorithm[1]
        if os.path.exists(compressed_path):
            compressed_size = os.path.getsize(compressed_path)
            compression_ratio = compressed_size / original_size
            time_taken = end_time - start_time

            algorithm_data.append({
                'compressed_size': compressed_size,
                'compression_ratio': compression_ratio,
                'time_taken': time_taken
            })

            # Clean up after each compression algorithm
            os.remove(compressed_path)

    # Log all algorithm results
    log_compression_data(file_path, original_size, algorithm_data)

def process_directory(directory):
    """Recursively process all files in the given directory."""
    header_data = [
        {'compressed_size': "deflate size", 'compression_ratio': "deflate ratio", 'time_taken': "deflate time taken"},
        {'compressed_size': "ppmd size", 'compression_ratio': "ppmd ratio", 'time_taken': "ppmd time taken"},
        {'compressed_size': "mx9 size", 'compression_ratio': "mx9 ratio", 'time_taken': "mx9 time taken"},
        {'compressed_size': "win size", 'compression_ratio': "win ratio", 'time_taken': "win time taken"}
    ]

    # Write header once before processing files
    log_compression_data("file name", "original_size", header_data, header=True)

    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            process_file(file_path)

if __name__ == "__main__":
    if len(sys.argv) not in [2, 3]:
        print("Usage: python script.py <directory> [<Ratio>]")
        sys.exit(1)
    
    directory = sys.argv[1]
    if not os.path.isdir(directory):
        print("Error: Provided path is not a directory.")
        sys.exit(1)
    
    process_directory(directory)
