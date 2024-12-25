#!/usr/bin/env python3

"""
collapse_codebase.py

This script traverses multiple selected directories (including all subdirectories),
collects all files (both text and binary), and writes them into a single
.codebase.txt file using delimiters to denote folders and files.

Features:
- GUI-based multiple directory selection using built-in Tkinter dialogs.
- Supports nested directories and subdirectories.
- Handles both text and binary files by encoding binary content in Base64.

Usage:
    Double-click the script or run via command line:
        python collapse_codebase.py
"""

import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
import base64

def detect_delimiters():
    """
    Define the delimiters used in the codebase.txt file.
    """
    folder_delim = "### FOLDER:"
    file_delim = "### FILE:"
    binary_file_marker = "(binary content of the"
    return folder_delim, file_delim, binary_file_marker

def collapse_codebase_to_txt(output_file, target_dirs):
    """
    Traverse each selected directory and write their structure and contents
    into the output_file following the defined delimiters.
    """
    folder_delim, file_delim, binary_file_marker = detect_delimiters()

    with open(output_file, 'w', encoding='utf-8') as out:
        for target_dir in target_dirs:
            # Ensure the target_dir exists
            if not os.path.isdir(target_dir):
                print(f"Warning: '{target_dir}' is not a valid directory. Skipping.")
                continue

            # For each subdirectory and file in target_dir
            for root, dirs, files in os.walk(target_dir):
                # ------------------------------------------------
                # Compute relative path from the *parent* of target_dir
                # for nicer readability. You could do this differently
                # if you want a different naming scheme.
                # ------------------------------------------------
                parent_of_target = os.path.dirname(target_dir)
                relative_root = os.path.relpath(root, parent_of_target)

                # Always write a folder delimiter for every subdirectory
                out.write(f"{folder_delim} {relative_root}\n")
                print(f"Writing folder: {relative_root}")

                # Now iterate over all files in the current root
                for filename in files:
                    file_path = os.path.join(root, filename)
                    relative_file_path = os.path.join(relative_root, filename)

                    # Write file delimiter
                    out.write(f"{file_delim} {relative_file_path}\n")
                    print(f"Writing file: {relative_file_path}")

                    # Determine if the file is likely binary
                    binary_extensions = [
                        '.png', '.jpg', '.jpeg', '.gif', '.bmp', 
                        '.ico', '.pdf', '.zip', '.exe'
                    ]
                    _, ext = os.path.splitext(filename)
                    is_binary = ext.lower() in binary_extensions

                    if is_binary:
                        # Write binary file marker
                        out.write(f"{binary_file_marker} {filename})\n")

                        try:
                            with open(file_path, 'rb') as f:
                                binary_data = f.read()
                                encoded_data = base64.b64encode(binary_data).decode('utf-8')

                            # Write Base64 data in lines of 76 characters as per RFC 2045
                            for i in range(0, len(encoded_data), 76):
                                out.write(f"{encoded_data[i:i+76]}\n")
                        except Exception as e:
                            print(f"Error encoding binary file '{relative_file_path}': {e}")
                            out.write(f"# Error encoding binary file: {e}\n")
                    else:
                        # Write text file content
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content = f.readlines()
                                out.writelines(content)
                        except UnicodeDecodeError:
                            print(f"Warning: Skipping non-UTF-8 file: {relative_file_path}")
                            out.write("# Warning: Non-UTF-8 file skipped.\n")
                        except Exception as e:
                            print(f"Error reading file '{relative_file_path}': {e}")
                            out.write(f"# Error reading file: {e}\n")

                    # Add a newline for separation
                    out.write("\n")

def main():
    # Initialize Tkinter root
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    selected_dirs = []
    while True:
        # Prompt the user to select a directory
        directory = filedialog.askdirectory(
            title="Select a directory to collapse (Cancel to finish)"
        )
        if directory:
            if directory not in selected_dirs:
                selected_dirs.append(directory)
                messagebox.showinfo("Directory Selected", f"Added: {directory}")
            else:
                messagebox.showwarning(
                    "Duplicate Selection", f"Directory already selected:\n{directory}"
                )
        else:
            # User canceled the selection
            break

    if not selected_dirs:
        messagebox.showwarning(
            "No Directories Selected", 
            "No directories were selected. Exiting."
        )
        print("No directories selected; exiting.")
        sys.exit(1)

    # Ask the user for an output file path
    output_file = filedialog.asksaveasfilename(
        title="Save collapsed codebase as...",
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt")]
    )
    if not output_file:
        messagebox.showwarning(
            "No Output File", 
            "No output file selected. Exiting."
        )
        print("No output file selected; exiting.")
        sys.exit(1)

    # Confirm action
    confirm = messagebox.askyesno(
        "Confirm Collapse", 
        f"Are you sure you want to collapse the selected directories into:\n{output_file}"
    )
    if not confirm:
        print("Operation canceled by the user.")
        sys.exit(0)

    try:
        collapse_codebase_to_txt(output_file, selected_dirs)
        messagebox.showinfo(
            "Success", 
            f"Codebase collapsed into '{output_file}' successfully."
        )
        print(f"Codebase collapsed into '{output_file}' successfully.")
    except Exception as e:
        messagebox.showerror(
            "Error", 
            f"An error occurred during collapsing:\n{e}"
        )
        print(f"An error occurred during collapsing: {e}")

if __name__ == "__main__":
    main()
