# CompleteTech-LLC / CodePack

A pair of Python scripts designed to **collapse** entire directories (including nested subdirectories) into a single `.txt` codebase file and **expand** it back into the original folder structure. These scripts were developed to simplify transferring or archiving complete codebases in a single file while preserving directory structures and handling both text and binary files.

---

## Table of Contents
1. [Overview](#overview)
2. [Features](#features)
3. [Prerequisites](#prerequisites)
4. [Installation](#installation)
5. [Usage](#usage)
   1. [Collapse a Codebase](#collapse-a-codebase)
   2. [Expand a Codebase](#expand-a-codebase)
6. [Project Structure](#project-structure)
7. [Technical Notes](#technical-notes)
8. [Author and Contact](#author-and-contact)
9. [License](#license)

---

## Overview

The **CodePack** project consists of two Python scripts:
1. **`collapse_codebase.py`** – Collapses selected directories (with all subdirectories) into a single `.codebase.txt` file.
2. **`expand_codebase.py`** – Expands a `.codebase.txt` file back into its original folder and file structure.

Both scripts utilize Python’s **Tkinter** library to provide a graphical interface, making it user-friendly for those uncomfortable with command-line operations. This allows convenient multiple directory selection and file dialogs for both collapsing and expanding codebases.

---

## Features

- **GUI-driven directory selection**: Choose as many directories as needed via a Tkinter-based dialog.
- **Nested subdirectory support**: Recursively traverses directory trees to capture all contained files and subfolders.
- **Automatic handling of binary files**: Detects common binary file extensions (e.g., `.png`, `.jpg`, `.zip`) and safely encodes them in Base64 within the `.codebase.txt` file.
- **Prevent duplicates**: Each directory is only processed once, alerting you if the same directory is re-selected.
- **Restoration of original structure**: When expanding, directories are rebuilt and files (including binary) are restored to their original form.

---

## Prerequisites

1. **Python** (3.6+ recommended)
2. **Tkinter** – Typically included with standard Python installations on most platforms (Windows, macOS, and many Linux distros). 
3. **Base64** – Included in the Python standard library.

---

## Installation

1. **Clone or Download** this repository:
   ```bash
   git clone https://github.com/CompleteTech-LLC/CodePack.git
   ```
   Or download the ZIP file and extract its contents.

   Change directory into the repository:
   ```bash
   cd CodePack
   ```

2. (Optional) Create and activate a virtual environment for clean dependency management:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. No additional packages beyond the standard library are required.

---

## Usage

### Collapse a Codebase
1. Run the `collapse_codebase.py` script:
   ```bash
   python collapse_codebase.py
   ```
2. A file dialog will prompt you to select one or more directories to be collapsed:
   - After selecting each directory, click **OK**.
   - When finished, click **Cancel** to stop adding directories.
3. Next, select (or specify) the output `.txt` file where the collapsed codebase will be saved.
4. Confirm when prompted to finalize the collapse process.
5. Upon completion, a success message will appear, and you will find a `.txt` file containing all selected directories’ content.

### Expand a Codebase
1. Run the `expand_codebase.py` script:
   ```bash
   python expand_codebase.py
   ```
2. A file dialog will prompt you to select the `.txt` file containing the collapsed codebase.
3. Click **Open** to begin the expansion.
4. The script will recreate the folders and files (including binary files) in the current working directory.

---

## Project Structure

```lua
CodePack/
├── collapse_codebase.py
├── expand_codebase.py
└── README.md   <-- This documentation
```

- **collapse_codebase.py** – Script to gather directories, encode content (text or Base64 for binaries), and produce a single `.txt` file.
- **expand_codebase.py** – Script to parse the `.txt` file, rebuild directories, and decode files.

---

## Technical Notes

### Delimiters
The scripts use specific delimiters in the `.codebase.txt` file:

- `### FOLDER:` – Indicates the start of a new folder.
- `### FILE:` – Indicates the start of a new file within the current folder.
- `(binary content of the ...)` – Marks that the file to follow is binary data encoded in Base64.

### Binary vs. Text Detection
- By default, binary extensions are identified based on common file types (e.g., images, archives, executables).
- You can customize the `binary_extensions` list in both scripts if your project includes other types of binary files.

### Character Encoding
- Text files are read and written using UTF-8 encoding.
- If a file is incorrectly classified or unreadable in UTF-8, the script prints a warning and skips writing that file to the output.

### Base64 Limitations
- Large files might increase the `.codebase.txt` file size significantly.
- Ensure you have adequate disk space to accommodate the encoded data.

---

## Author and Contact

**Author**  
Timothy Gregg (CTO, CompleteTechLLC)

**Contact**  
Timothy.Gregg@complete.tech

Feel free to reach out for any inquiries, feature requests, or issues.

---

## License

This repository is licensed under the terms of the MIT License. Refer to the LICENSE file (if included) or the following excerpt:

```vbnet
MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy of this 
software and associated documentation files (the "Software"), to deal in the Software 
without restriction, including without limitation the rights to use, copy, modify, merge, 
publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons 
to whom the Software is furnished to do so, subject to the following conditions:

[ ... full text omitted for brevity ... ]
```
