# LSD: `ls` detailed

Python-based recursive directory lister. Think `tree`, but all Python. Clean output. Filters. No external deps.

---

## Features

* Lists directories/files in a clean tree format.
* Supports relative or absolute paths.
* Includes/excludes files/folders by pattern (`--include`, `--exclude`).
* Limit recursion depth (`--max-depth`) or number of items per dir (`--max-items`).
* Optionally show only directories (`--directories`).
* UTF-8 tree output with ASCII fallback.
* Can write to a file (`--output`) with UTF-8 encoding.
* Lightweight: Python 3.6+, no external deps.

---

## Requirements

* Python 3.6+
  (You’re fine if you're on 3.13 or whatever.)

---

## Usage

### Run from source

```bash
python lsd.py [DIRECTORY] [OPTIONS]
```

If no directory is given, it uses the current one.

### Example commands

```bash
python lsd.py .
  # Show current directory recursively.

python lsd.py ../Downloads -d 2
  # Show up to 2 levels deep.

python lsd.py -i ".txt" -x "temp" -o output.txt
  # Include only .txt files, exclude anything with "temp", save to file.

python lsd.py -m 5 -r
  # Show only directories, max 5 per dir.
```

---

## CLI Options

```
Usage: python lsd.py [DIRECTORY] [OPTIONS]

Arguments:
  DIRECTORY                 The root directory to list. Defaults to the current directory.

Options:
  -d, --max-depth N        Limit recursion depth to N levels.
  -m, --max-items N        Limit max number of subitems per directory to N.
  -i, --include PATTERN    Show only files or folders matching this pattern. Can be used multiple times.
  -x, --exclude PATTERN    Exclude files or folders matching this pattern. Can be used multiple times.
  -r, --directories        Only show directories (no files).
  -o, --output FILE        Write output to FILE (UTF-8 encoded).
  -h, --help, /?           Show this help message and exit.
```

---

## Building Executable

If you want a standalone `.exe` or binary:

### 1. Install PyInstaller

```bash
pip install pyinstaller
```

### 2. Build

```bash
pyinstaller --onefile lsd.py
```

Output will be in `dist/lsd` (or `lsd.exe` on Windows).

### 3. Add to PATH

Move `lsd`/`lsd.exe` to a folder in your `PATH`.

* **Windows**:
  Use `C:\tools` or something, then add that folder to your PATH in System Properties.

* **Linux/macOS**:
  Drop it in `~/bin`, `/usr/local/bin`, etc.

---

## Unicode Output

* Tree uses Unicode chars (`├──`, `└──`, etc).
* Falls back to ASCII if console doesn't support it.
* To force full Unicode (e.g. in a file), use `-o`:

```bash
python lsd.py -o output.txt
```

---

## Security

* If using prebuilt `lsd.exe`, verify source.
* Or just build your own.

---

## License

MIT-ish. No warranty. Use at your own risk. You break it, you bought it.