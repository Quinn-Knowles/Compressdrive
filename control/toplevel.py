import os
import struct

# Dictionary of file signatures (magic numbers) for compressed file types
COMPRESSED_SIGNATURES = {
    b'\x50\x4B\x03\x04': 'ZIP',  # ZIP (PKZIP)
    b'\x1F\x8B': 'GZIP',  # GZIP
    b'\x42\x5A\x68': 'BZIP2',  # BZ2
    b'\x37\x7A\xBC\xAF\x27\x1C': '7Z',  # 7-Zip
    b'\x52\x61\x72\x21\x1A\x07\x00': 'RAR',  # RAR
    b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A': 'PNG',  # PNG (has internal compression)
    b'\x1A\x45\xDF\xA3': 'MKV/WebM',  # Matroska (potential compression)
    b'\x00\x00\x01\xBA': 'MPEG-PS',  # MPEG Program Stream
    b'\x00\x00\x01\xB3': 'MPEG Video',
    b'\x00\x00\x00\x18\x66\x74\x79\x70': 'MP4',  # MP4 (some contain compression)
}

# Extensions that often contain compression
COMPRESSED_EXTENSIONS = {'.zip', '.rar', '.7z', '.gz', '.bz2', '.xz', '.tar.gz', '.mkv', '.mp4', '.png'}

def get_file_signature(file_path, num_bytes=8):
    """Reads the first few bytes of the file to get the magic number."""
    try:
        with open(file_path, 'rb') as f:
            return f.read(num_bytes)
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

def is_compressed(file_path):
    """Determines if a file is compressed based on its signature and known compressed formats."""
    if not os.path.isfile(file_path):
        print(f"File not found: {file_path}")
        return False

    # Get the first few bytes (header)
    signature = get_file_signature(file_path)
    if not signature:
        return False

    # Check against known compressed file signatures
    for magic, file_type in COMPRESSED_SIGNATURES.items():
        if signature.startswith(magic):
            print(f"File matches known compressed format: {file_type}")
            return True

    # Check by extension (fallback)
    ext = os.path.splitext(file_path)[1].lower()
    if ext in COMPRESSED_EXTENSIONS:
        print(f"File extension suggests possible compression: {ext}")
        return True

    print("File does not appear to be compressed.")
    return False

# Example usage
if __name__ == "__main__":
    file_path = input("Enter file path: ").strip()
    if is_compressed(file_path):
        print("The file is compressed.")
    else:
        print("The file is not compressed.")
