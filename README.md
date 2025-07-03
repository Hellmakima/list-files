# LSD: `ls` detailed

## Overview

`lsd` is a Python-based tool to recursively list the contents of directories in a structured tree format. It mimics the behavior of Linux's `tree` command but is implemented entirely in Python and shows all sub-directories and files.

## Features

* Lists files and directories in a neat tree format.
* Accepts relative or absolute path; defaults to current directory.
* Supports multiple `--include` and `--exclude` filters to show/hide files or folders by pattern.
* Limits maximum recursion depth (`-d` / `--max-depth`).
* Limits max number of subitems per directory (`-m` / `--max-items`).
* Gracefully falls back to ASCII when console can’t display Unicode; suggests using `-o` flag for UTF-8 output.
* Optionally outputs to file with UTF-8 encoding.
* Lightweight, no external dependencies beyond Python 3.6+.

## Requirements

* Python 3.6 or later.

## Usage Instructions

### Option 1: Direct Download and Use

1. **Download the `lsd.exe` file**:

   * Save it to a folder of your choice.

2. **Add the executable to your PATH**:

   * **On Windows**:

     * Place `lsd.exe` in a directory already in your PATH (e.g., `C:\Windows\System32`) or create a new directory (e.g., `C:\tools`), move `lsd.exe` there, and add this directory to your PATH environment variable.
     * To add directory to PATH:

       * Open `System Properties` > `Environment Variables`.
       * Under `System Variables`, select `Path`, click `Edit`, then add the new directory.

   * **On Linux/MacOS**:

     * Build your own executable with PyInstaller (see below).

3. **Run the tool**:

   ```bash
   lsd <directory>
   ```

   * If no directory is specified, the current directory will be listed.

### Option 2: Build Your Own Executable

1. **Install PyInstaller**:

   ```bash
   pip install pyinstaller
   ```

2. **Edit `lsd.py` as needed**, e.g., add colors or tweak options.

3. **Build executable**:

   ```bash
   pyinstaller --onefile lsd.py
   ```

4. **Find your executable**:

   * It will be in the `dist/` folder.

5. **Add executable to your PATH**:

   * Move `lsd.exe` (Windows) or `lsd` (Linux/MacOS) to a directory in your PATH.

6. **Run the executable**:

   ```bash
   lsd <directory>
   ```

## Command Line Options

* `-d`, `--max-depth <int>`: Limit recursion depth.
* `-m`, `--max-items <int>`: Limit max subitems per directory.
* `-i`, `--include <pattern>`: Show only files matching any of the include patterns (can be used multiple times).
* `-x`, `--exclude <pattern>`: Exclude files or folders matching any of these patterns (can be used multiple times).
* `-o`, `--output <file>`: Write output to UTF-8 encoded file instead of console.
* `-h`, `--help`, `/?`: Show help message.

## Examples

### List current directory

```bash
lsd .
```

### List up to 2 levels deep

```bash
lsd -d 2
```

### Show only files in `homework` directory and exclude `.txt` files

```bash
lsd -i homework -x txt
```

### Limit to 5 items per directory

```bash
lsd -m 5
```

### Output to a file

```bash
lsd -o output.txt
```

## Notes

* Unicode tree characters fall back to ASCII if your console can’t display them.
* For full Unicode output, use `-o` to write to a file.
* Always verify the executable or build your own for security.
* Requires Python 3.6+. IDK I use 3.13

## License

Provided "as is" without warranty. Use at your own risk.
