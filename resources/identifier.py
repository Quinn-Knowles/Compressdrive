import os
import sys
#unused
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

COMPRESSED_EXTENSIONS = ['.zip', '.7z', '.rar', '.gz']

def get_file_signature(file_path, num_bytes=8):
    """Reads the first few bytes of a file to determine its magic number."""
    try:
        with open(file_path, 'rb') as f:
            return f.read(num_bytes)
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

def is_compressed(file_path):
    """Determines if a file is compressed based on its signature or extension."""
    if not os.path.isfile(file_path):
        print(f"File not found: {file_path}")
        return False

    file_extension = os.path.splitext(file_path)[1].lower()
    if file_extension in COMPRESSED_EXTENSIONS:
        print(f"File is compressed based on extension: {file_extension}")
        return True

    signature = get_file_signature(file_path)
    if not signature:
        return False

    for magic, file_type in COMPRESSED_SIGNATURES.items():
        if signature.startswith(magic):
            print(f"File is likely compressed as: {file_type}")
            return True

    print("File does not appear to be compressed.")
    return False

def analyze_file(file_path):
    """Checks if a file is compressed based on its signature or extension."""
    if not os.path.isfile(file_path):
        print("Error: File not found.")
        return

    compressed = is_compressed(file_path)
    if compressed:
        print(0)
    else:
        print(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python identifier.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    analyze_file(file_path)
