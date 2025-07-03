import os
import sys
import argparse
from contextlib import redirect_stdout

class DirectoryLister:
    def __init__(self, include_patterns=None, exclude_patterns=None):
        self.include_patterns = include_patterns or []
        self.exclude_patterns = exclude_patterns or []
        self._warned_encoding = False

    def should_include(self, path):
        """Apply excludes to everything; apply includes to files only."""
        if any(p in path for p in self.exclude_patterns):
            return False
        if self.include_patterns and not os.path.isdir(path):
            return any(p in path for p in self.include_patterns)
        return True

    def list_files(self, directory, prefix='', level=0,
                   max_depth=None, max_items=None, output_file=None):
        """Pretty tree printer that never mis-draws branches."""
        # Stop if depth exceeded
        if max_depth is not None and level >= max_depth:
            return

        # Get filtered items
        try:
            all_items = sorted(os.listdir(directory))
        except PermissionError:
            self._print(f"{prefix}└── [Permission Denied]", output_file)
            return

        # Filter with include/exclude
        all_items = [i for i in all_items if self.should_include(os.path.abspath(os.path.join(directory, i)))]

        # Separate dirs and files
        dirs = [i for i in all_items if os.path.isdir(os.path.join(directory, i))]
        files = [i for i in all_items if not os.path.isdir(os.path.join(directory, i))]

        # Apply max_items limit prioritizing directories
        if max_items is not None:
            dirs = dirs[:max_items]
            remaining = max_items - len(dirs)
            files = files[:remaining] if remaining > 0 else []
        items = dirs + files

        # Items hidden due to max_items
        truncated = len(all_items) - len(items)

        # Loop through (dirs first, then files) in display order
        for idx, name in enumerate(items):
            is_last = (idx == len(items) - 1) and (truncated == 0)
            connector = '└── ' if is_last else '├── '
            full_path = os.path.join(directory, name)
            display = f"{prefix}{connector}{name}/" if os.path.isdir(full_path) else f"{prefix}{connector}{name}"
            self._print(display, output_file)

            if os.path.isdir(full_path):
                new_prefix = prefix + ('    ' if is_last else '│   ')
                self.list_files(full_path, new_prefix, level + 1,
                                max_depth, max_items, output_file)

        # Show "... (N more)" if anything was skipped
        if truncated:
            self._print(f"{prefix}└── ... ({truncated} more)", output_file)

    def _ascii_fallback(self, s: str) -> str:
        """Replace U-lines with ASCII twins."""
        return (s.replace('│', '|')
                .replace('├', '|')
                .replace('└', '\\')
                .replace('──', '--'))

    def _print(self, text, output_file=None):
        if output_file:
            with open(output_file, 'a', encoding='utf-8') as f:
                f.write(text + '\n')
            return
        try:
            print(text)
        except UnicodeEncodeError:               # CP-1252 et al choke on box-chars
            if not self._warned_encoding:
                sys.stderr.write("Using ASCII fallback. Consider -o <file> for full UTF-8 output.\n")
                self._warned_encoding = True
            print(self._ascii_fallback(text))

def display_help():
    """Displays help information."""
    help_text = """
Usage: python lsd.py [DIRECTORY] [OPTIONS]

Arguments:
  DIRECTORY       The root directory to list. Defaults to the current directory.
  
Options:
  -d, --max-depth MAX_DEPTH    Maximum recursion depth from the starting location. Default is infinite.
  -m, --max-items MAX_ITEMS    Maximum number of subitems to display per directory.
  -i, --include PATTERN        Only show paths that include this pattern.
  -x, --exclude PATTERN        Exclude paths that contain this pattern.
  -o, --output FILE            Write output to specified file instead of console.
  -h, --help                   Display this help message.

Examples:
  python lsd.py ../Downloads/test -d 2
    List files and directories up to 2 levels deep starting at ../Downloads/test.
  
  python lsd.py -i ".txt" -x "temp" -o output.txt
    List all .txt files excluding "temp" and save to output.txt.
  
  python lsd.py -m 5 -o results.log
    List all files and directories (max 5 per dir) and save to results.log.
"""
    print(help_text)

if __name__ == "__main__":
    # Argument parsing
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("directory", nargs="?", default=".", help="Root directory to list.")
    parser.add_argument("-d", "--max-depth", type=int, help="Maximum depth for recursion.")
    parser.add_argument("-m", "--max-items", type=int, help="Maximum number of subitems per directory.")
    parser.add_argument("-i", "--include", action='append', help="Only include paths that contain these patterns")
    parser.add_argument("-x", "--exclude", action='append', help="Exclude paths that contain these patterns")
    parser.add_argument("-o", "--output", help="Write output to specified file.")
    parser.add_argument("-h", "--help", action="store_true", help="Display help.")

    args = parser.parse_args()

    # Handle help option
    if args.help:
        display_help()
        sys.exit(0)

    # Validate directory
    directory = args.directory
    if not os.path.exists(directory):
        print(f"Error: The directory '{directory}' does not exist.")
        sys.exit(1)

    # Clear output file if it exists
    if args.output and os.path.exists(args.output):
        try:
            os.remove(args.output)
        except Exception as e:
            print(f"Error clearing output file: {e}")
            sys.exit(1)

    # Create lister with patterns
    lister = DirectoryLister(
        include_patterns=args.include if args.include else [],
        exclude_patterns=args.exclude if args.exclude else []
    )

    # List files with options
    lister.list_files(
        directory=directory,
        max_depth=args.max_depth,
        max_items=args.max_items,
        output_file=args.output
    )
