Compress Drive
Quinn Knowles, Paige Schiele

CompressDrive

CompressDrive is a Python-based utility designed to compress files using various compression algorithms and (on request) log the results. It supports several compression algorithms and allows users to analyze the effectiveness of each algorithm by comparing the compression ratio, compressed size, and the time taken to perform the compression.
Features

    Supports multiple compression algorithms: Deflate, PPMD, MX9, and Windows Compression.

    Recursively processes all files in a specified directory.

    Logs the compression results (file name, original size, compression size, compression ratio, and time taken) to a file called output.txt.

    Can handle large numbers of files in a directory and supports clean-up of temporary compressed files.

Prerequisites

Before using this program, ensure that you have the following:

    Python 3.x: The program is written in Python, so you’ll need Python 3.x installed.

    Required Libraries: The program uses several Python libraries, including os, sys, subprocess, and time. These libraries come pre-installed with Python, so no additional installation is required.

    Compression Scripts: The program relies on external compression scripts, namely:
		7zip
		Python LZMA
        windows powershell (for Windows Compression)
		
Acknowledgments

    Thanks to the Python community for maintaining the standard library and making it easy to work with file systems, subprocesses, and logging.
