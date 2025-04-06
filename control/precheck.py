import os
import sys
import gzip
import math


"""
input: target file directory , target ratio
output: percent of files likely to compress

script goal 1: create an idea of how many files in target directory will compress below target 
"""


# Known file signatures for formats that include compression
COMPRESSED_SIGNATURES = {
    # Archive & Compression Formats
    b'\x50\x4B\x03\x04': 'ZIP / DOCX / XLSX / PPTX / JAR / APK',  
    b'\x1F\x8B': 'GZIP',
    b'\x42\x5A\x68': 'BZIP2',
    b'\x37\x7A\xBC\xAF\x27\x1C': '7Z',
    b'\x52\x61\x72\x21\x1A\x07\x00': 'RAR',
    b'\xFD\x37\x7A\x58\x5A\x00': 'XZ',

    # Image Formats with Compression
    b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A': 'PNG (lossless DEFLATE)',
    b'\xFF\xD8\xFF': 'JPEG (lossy DCT)',
    b'\x47\x49\x46\x38': 'GIF (LZW compression)',
    b'\x52\x49\x46\x46': 'WEBP or RIFF-based format',
    b'\x00\x00\x00\x0C\x6A\x50\x20\x20': 'JPEG2000',
    b'\x00\x00\x00\x1C\x66\x74\x79\x70': 'MP4 or QuickTime (compressed video)',

    # Video Formats
    b'\x1A\x45\xDF\xA3': 'MKV / WebM (can store compressed video)',
    b'\x00\x00\x01\xBA': 'MPEG-PS (potentially compressed)',
    b'\x00\x00\x01\xB3': 'MPEG Video',

    # Audio Formats
    b'\x49\x44\x33': 'MP3 (lossy compression)',
    b'OggS': 'OGG (Vorbis/Opus compressed audio)',
    b'fLaC': 'FLAC (lossless compression)',
    b'\xFF\xF1': 'AAC (lossy compression)',
    
    # Documents
    b'\x25\x50\x44\x46': 'PDF (compressed Flate/JPEG streams)',
    b'\x3C\x3F\x78\x6D\x6C': 'XML (could be inside ZIP-based format like DOCX)',
    
    # Executables & Virtual Disk Formats
    b'\x4D\x5A': 'EXE/DLL (some use UPX compression)',
    b'\x51\x46\x49': 'QCOW2 (compressed virtual disk)',
    b'\x52\x5A\x44\x31': 'VHDX (compressed virtual disk)'
}

def get_file_signature(file_path, num_bytes=8):
    """Reads the first few bytes of a file to determine its magic number."""
    try:
        with open(file_path, 'rb') as f:
            return f.read(num_bytes)
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

def is_compressed(file_path):
    """Determines if a file is compressed based on its signature."""
    if not os.path.isfile(file_path):
        print(f"File not found: {file_path}")
        return False

    # Read file signature
    signature = get_file_signature(file_path)
    if not signature:
        return False

    # Check if the signature matches any known compressed format
    for magic, file_type in COMPRESSED_SIGNATURES.items():
        if signature.startswith(magic):
            return True

    return False

def calculate_entropy(file_path):
    """Calculates Shannon entropy to determine randomness."""
    try:
        with open(file_path, 'rb') as f:
            data = f.read()

        if not data:
            return 0  # Empty file has zero entropy

        byte_counts = [0] * 256
        for byte in data:
            byte_counts[byte] += 1

        total_bytes = len(data)
        entropy = -sum((count / total_bytes) * math.log2(count / total_bytes) for count in byte_counts if count > 0)
        return entropy
    except Exception as e:
        print(f"Error calculating entropy: {e}")
        return None

def test_compression_ratio(file_path):
    """Attempts gzip compression to estimate how much smaller the file can get."""
    try:
        original_size = os.path.getsize(file_path)
        if original_size == 0:
            return 1.0  # Empty files are already "fully compressed"

        compressed_path = file_path + ".gz"
        with open(file_path, 'rb') as f_in, gzip.open(compressed_path, 'wb') as f_out:
            f_out.writelines(f_in)

        compressed_size = os.path.getsize(compressed_path)
        os.remove(compressed_path)  # Clean up temporary file

        compression_ratio = compressed_size / original_size
        return compression_ratio
    except Exception as e:
        return None

def process_directory(directory, target_ratio):
    """Recursively process all files in the given directory."""
    total_files = 0
    probable_success = 0
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            total_files += 1
            result = analyze_file(file_path, target_ratio)
            if result == 1:  # Assuming a successful return means a file with compression ratio below target
                probable_success += 1
    if total_files == 0:
        return 0
    return (probable_success / total_files) * 100


def analyze_file(file_path, target_ratio):
    """Checks if a file is compressed and whether it should be compressed further."""
    #print(f"\nAnalyzing: {file_path}")
    if not os.path.isfile(file_path):
        print("Error: File not found.")
        return 0  # Return 0 to handle error cases

    compressed = is_compressed(file_path)
    entropy = calculate_entropy(file_path)
    compression_ratio = test_compression_ratio(file_path)

    if compression_ratio is None:
        return 0  # If compression ratio cannot be calculated, return 0
    
    if compression_ratio > target_ratio and entropy > 7.5:
        return 0  # File is already well compressed
    elif compression_ratio < target_ratio:
        return 1  # File can likely be compressed further
    else:
        return -1  # File might be compressible, but gains will be small
        
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python identifier.py <directory_path> <target_ratio>")
        sys.exit(1)

    target_ratio = float(sys.argv[2]) / 100
    percentage = process_directory(sys.argv[1], target_ratio)
    print(f"{percentage:.2f}% of files are likely to compress below target.")
