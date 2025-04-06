import os
import sys
import gzip
import math

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
            #print(f"File is likely compressed: {file_type}")
            return True

    #print("File does not appear to be compressed.")
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
        #print(f"Error testing compression ratio: {e}")
        return None

def analyze_file(file_path, target_ratio):
    """Checks if a file is compressed and whether it should be compressed further."""
    #print(f"\nAnalyzing: {file_path}")
    if not os.path.isfile(file_path):
        print("Error: File not found.")
        return

    compressed = is_compressed(file_path)
    entropy = calculate_entropy(file_path)
    compression_ratio = test_compression_ratio(file_path)

    #print(f"Shannon Entropy: {entropy:.2f} bits/byte (Max: 8.0)")
    #print(f"Estimated Compression Ratio (Gzip): {compression_ratio:.2f}")

    if compression_ratio > target_ratio and entropy > 7.5:
        #print("File is already well compressed. Further compression won't help.")
        print(0)
    elif compression_ratio < target_ratio:
        #print("This file can likely be compressed further.")
        print(1)
    else:
        #print("The file might be compressible, but gains will be small.")
        x=1

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python identifier.py <file_path> <ratio>")
        sys.exit(1)

    file_path = sys.argv[1]
    ratio = float(sys.argv[2]) / 100
    analyze_file(file_path, ratio)