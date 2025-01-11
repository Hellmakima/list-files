# LSD: ls detailed

## Overview

`lsd` is a Python-based tool to recursively list the contents of directories in a structured tree format. It mimics the behavior of Linux's `tree` command but is implemented entirely in Python and shows all sub-directories and files.

## Features

- Lists files and directories in a tree format.
- Accepts a relative or absolute path as an argument, or defaults to the current directory if no argument is provided.
- Simple to use and lightweight.

## Requirements

- Python 3.6 or later.

## Usage Instructions

### Option 1: Direct Download and Use

1. **Download the ************`lsd.exe`************ file**:

   - Save it to a desired folder on your system.

2. **Add the script to your PATH**:

   - **On Windows**:
     1. Save `lsd.exe` to a directory already in your PATH (e.g., `C:\Windows\System32`) or create a new directory (e.g., `C:\tools`), move `lsd.exe` there, and add this directory to your PATH environment variable.
     2. To add a directory to PATH:
        - Open `System Properties` > `Environment Variables`.
        - Under `System Variables`, find `Path`, click `Edit`, and add the directory.
   - **On Linux/MacOS**:
     1. There is no steps, recompile it.

3. **Run the script**:

   ```bash
   lsd <directory>
   ```

   - If no directory is specified, the current directory will be listed.

### Option 2: Create Your Own Executable

1. **Install `pyinstaller`**:

   ```bash
   pip install pyinstaller
   ```

2. **Test and Tweak**:

   - Test to see if the file runs properly.
   - Edit the `lsd.py` file according to your needs.
   - Add color scheme if you want. (implement it yourself)
  
4. **Create an Executable**:

   ```bash
   pyinstaller --onefile lsd.py
   ```

5. **Locate the Executable**:

   - The executable will be located in the `dist/` folder.

6. **Add Executable to PATH**:

   - Move the generated `lsd.exe` (on Windows) or `lsd` (on Linux/MacOS) to a directory in your PATH.

7. **Run the Executable**:

   ```bash
   lsd <directory>
   ```

## Examples

### Example 1: Listing a Directory

```bash
lsd .
```

Output:

```
./
├── file1.txt
├── file2.py
└── subdir/
    ├── file3.md
    └── file4.jpg
```

### Example 2: Specifying a Directory

```bash
lsd some_folder
```

Output:

```
some_folder/
├── example1.txt
└── example2.txt
```

## Notes

- Ensure that Python is installed and accessible from your command line.
- The script handles errors like missing directories and provides meaningful error messages.
- This is not the surce code for the included exe file. please make sure it runs properly before making exe/out file.
- Don't trust `.exe` files online.

## License

This tool is provided "as is" without any guarantees. Use at your own risk.
