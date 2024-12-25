#!/usr/bin/env python3

"""
expand_codebase.py

This script reads a single .txt file (UTF-8 encoded) from the local
file system that contains an entire codebase. The text file uses
delimiters such as "### FOLDER:" and "### FILE:" to denote folders
and files, respectively.

Features:
- GUI-based file selection for ease of use on Windows.
- Supports nested directories and subdirectories.
- Handles both text and binary files by encoding binary content in Base64.

Usage:
    Double-click the script or run via command line:
        python expand_codebase.py
"""

import os
import sys
import tkinter as tk
from tkinter import filedialog
import base64

def detect_delimiters():
    """
    Define the delimiters used in the codebase.txt file.
    """
    folder_delim = "### FOLDER:"
    file_delim = "### FILE:"
    binary_file_marker = "(binary content of the"
    return folder_delim, file_delim, binary_file_marker

def expand_codebase_from_txt(input_file):
    folder_delim, file_delim, binary_file_marker = detect_delimiters()

    current_folder_path = ""
    current_file_path = ""
    file_content_buffer = []
    is_binary = False

    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for idx, line in enumerate(lines):
        line_stripped = line.strip()

        # Check for folder delimiter
        if line_stripped.startswith(folder_delim):
            # Flush any ongoing file buffer
            if current_file_path and file_content_buffer:
                _write_file(current_file_path, file_content_buffer, is_binary)
                file_content_buffer = []
                current_file_path = ""
                is_binary = False

            # Parse folder name (can include nested paths)
            folder_name = line_stripped.replace(folder_delim, "").strip()
            current_folder_path = os.path.join(os.getcwd(), folder_name)

            # Create the folder, including any necessary subdirectories
            os.makedirs(current_folder_path, exist_ok=True)
            print(f"Created folder: {current_folder_path}")

        # Check for file delimiter
        elif line_stripped.startswith(file_delim):
            # Flush any ongoing file buffer
            if current_file_path and file_content_buffer:
                _write_file(current_file_path, file_content_buffer, is_binary)
                file_content_buffer = []
                is_binary = False

            # Parse file name
            file_name = line_stripped.replace(file_delim, "").strip()
            current_file_path = os.path.join(current_folder_path, file_name)

            # Determine if the file is binary based on its extension
            binary_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.ico', '.pdf', '.zip', '.exe']
            _, ext = os.path.splitext(file_name)
            is_binary = ext.lower() in binary_extensions

            print(f"Processing file: {current_file_path} (Binary: {is_binary})")

        else:
            # Check if the current line indicates binary content
            if is_binary and line_stripped.startswith(binary_file_marker):
                # The next lines contain Base64 encoded binary data
                # Continue reading until an empty line or next delimiter
                binary_data = []
                for binary_line in lines[idx + 1:]:
                    binary_line_stripped = binary_line.strip()
                    if binary_line_stripped.startswith(folder_delim) or binary_line_stripped.startswith(file_delim):
                        break
                    binary_data.append(binary_line)
                # Decode Base64 and write binary file
                _write_binary_file(current_file_path, binary_data)
                file_content_buffer = []
                is_binary = False
                break  # Exit since binary content is handled
            else:
                # Otherwise, treat as text content
                if current_file_path and not is_binary:
                    file_content_buffer.append(line)

    # Handle the last file if buffer is not empty
    if current_file_path and file_content_buffer:
        _write_file(current_file_path, file_content_buffer, is_binary)

def _write_file(filepath, content_lines, is_binary):
    """
    Writes the buffered content into the specified file in UTF-8 encoding.
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(content_lines)
    print(f"Created file: {filepath}")

def _write_binary_file(filepath, base64_lines):
    """
    Decodes Base64 encoded lines and writes binary content to the file.
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    base64_str = ''.join(base64_lines)
    binary_data = base64.b64decode(base64_str)
    with open(filepath, 'wb') as f:
        f.write(binary_data)
    print(f"Created binary file: {filepath}")

def main():
    # Initialize Tkinter root
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Open a file dialog to select the codebase.txt file
    input_file = filedialog.askopenfilename(
        title="Select the codebase.txt file",
        filetypes=[("Text Files", "*.txt")]
    )

    if not input_file:
        print("No file selected; exiting.")
        sys.exit(1)

    # Expand the codebase from the selected file
    expand_codebase_from_txt(input_file)
    print("Codebase expansion complete.")

if __name__ == "__main__":
    main()
