__version__ = "1.2.0"
__annotations__ = {
    "author": "Sufiyan Attar",
    "email": "sufiyanhattar@gmail.com",
    "github": "https://github.com/Hellmakima/list-files"
}


from os import (
    path as os_path, 
    listdir as os_listdir, 
    remove as os_remove,
    stat as os_stat
)
from sys import stderr, exit as sys_exit
from argparse import ArgumentParser
from dataclasses import dataclass, field
from typing import List, Optional
from stat import filemode as stat_filemode

color_red: str = "\033[1;31m"
color_green: str = "\033[1;32m"
color_blue: str = "\033[1;34m"
color_yellow: str = "\033[1;33m"
color_gray: str = "\033[1;30m"
color_reset: str = "\033[0m"

@dataclass
class DirectoryLister:
    _warned_encoding: bool = False
    directories_only: bool = False
    exclude_patterns: List[str] = field(default_factory=list)
    gitignore_patterns: List[tuple] = field(default_factory=list)
    gitignore: bool = False
    include_patterns: List[str] = field(default_factory=list)
    list_details: bool = False
    no_color: bool = False
    output_file: Optional[str] = None
    relative_path: str = ""
    show_size: bool = False

    def __post_init__(self):
        if self.no_color:
            global color_red, color_green, color_blue, color_yellow, color_gray, color_reset
            color_red = ""
            color_green = ""
            color_blue = ""
            color_yellow = ""
            color_gray = ""
            color_reset = ""


    def should_include(self, path):
        """Apply excludes to everything; apply includes to files only."""
        file_relative_path = os_path.relpath(path, self.relative_path)

        if self.directories_only and os_path.isfile(path):
            return False
        if any(p in file_relative_path for p in self.exclude_patterns):
            return False

        # Apply regex-based gitignore
        include = True
        for base_dir, patterns in self.gitignore_patterns:
            rel_to_git_dir = os_path.relpath(path, base_dir)
            for pat in patterns:
                if pat in rel_to_git_dir:
                    return False

        # Apply include patterns only to files
        if self.include_patterns and not os_path.isdir(path):
            include = include and any(p in file_relative_path for p in self.include_patterns)

        return include

    
    def _format_size(self, size):
        for unit in ['B', 'KiB', 'MiB', 'GiB', 'TiB']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} PB"


    def _format_details(self, path):
        mtime = os_path.getmtime(path)
        formatted_time = formatter(mtime).strftime("%m/%d/%Y %H:%M")

        # File size
        size = self._format_size(os_path.getsize(path))

        # Get file mode
        mode = stat_filemode(os_stat(path).st_mode)

        return f"({formatted_time}) {size} {mode}"
        

    def _add_gitignore_patterns(self, directory):
        gitignore_path = os_path.join(directory, '.gitignore')
        patterns = []

        try:
            with open(gitignore_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#') or line.startswith('!'):
                        continue  # ignore comments and negation lines

                    # Remove * and / characters
                    cleaned = line.replace('*', '').replace('/', '')

                    if cleaned:  # skip empty lines after cleaning
                        patterns.append(cleaned)
        except Exception:
            pass

        return directory, patterns


    def list_files(self, directory, prefix='', level=0, max_depth=None, max_items=None):
        """Pretty tree printer that never mis-draws branches."""
        if max_depth is not None and level >= max_depth:
            return

        # Get filtered items
        try:
            all_items = sorted(os_listdir(directory))
        except PermissionError:
            self._print(f"{prefix}└── [Permission Denied]")
            return
        
        found_gitignore = False
        if self.gitignore:
            # see if .gitignore exists
            if os_path.exists(os_path.join(directory, '.gitignore')):
                found_gitignore = True
                gitignore_pattern = self._add_gitignore_patterns(directory)
                self.gitignore_patterns.append(gitignore_pattern)

        # Filter with include/exclude
        all_items = [i for i in all_items if self.should_include(os_path.abspath(os_path.join(directory, i)))]

        # Separate dirs and files
        dirs = [i for i in all_items if os_path.isdir(os_path.join(directory, i))]
        files = [] if self.directories_only else [i for i in all_items if not i in dirs]

        # Apply max_items limit prioritizing directories
        if max_items is not None:
            dirs = dirs[:max_items]
            if not self.directories_only:
                remaining = max_items - len(dirs)
                files = files[:remaining] if remaining > 0 else []
        items = dirs + files

        # Items hidden due to max_items
        truncated = len(all_items) - len(items)

        # Loop through (dirs first, then files) in display order
        for idx, name in enumerate(items):
            is_last = (idx == len(items) - 1) and (truncated == 0)
            connector = '└── ' if is_last else '├── '
            full_path = os_path.join(directory, name)
            display = f"{prefix}{connector}{name}/" if os_path.isdir(full_path) else f"{prefix}{connector}{name}" 
            if os_path.isfile(full_path):
                if self.show_size and not self.list_details:
                    display += f" {self._format_size(os_path.getsize(full_path))}"
                if self.list_details:
                    display += f" {self._format_details(full_path)}"

            self._print(display)

            if os_path.isdir(full_path):
                new_prefix = prefix + ('    ' if is_last else '│   ')
                self.list_files(full_path, new_prefix, level + 1,
                                max_depth, max_items)

        # Show "... (N more)" if anything was skipped
        if truncated:
            self._print(f"{prefix}└── ... ({truncated} more)")
        
        # remove gitignore patterns added in this call
        if found_gitignore:
            self.gitignore_patterns.pop()


    def _ascii_fallback(self, s: str) -> str:
        """Replace U-lines with ASCII twins."""
        return (s.replace('│', '|')
                .replace('├', '|')
                .replace('└', '\\')
                .replace('──', '--'))


    def _print(self, text):
        """Print with optional color and output file handling."""
        if self.output_file:
            with open(self.output_file, 'a', encoding='utf-8') as f:
                f.write(text + '\n')
            return
        try:
            if "─ ." in text: # hidden files (grey)
                text = text.replace("─ .", f"─ {color_gray}.") + color_reset
            if text.endswith('/'): # directories
                text = text.replace("─ ", f"─ {color_green}").replace("/", f"{color_reset}/")
            print(text)
        except UnicodeEncodeError:               # CP-1252 
            if not self._warned_encoding:
                stderr.write("Using ASCII fallback. Consider -o <file> for full UTF-8 output.\n")
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
  -g, --gitignore              Ignore .gitignore patterns.
  -i, --include PATTERN        Only show paths that include this pattern.
  -l, --list                   Show file details such as size, date and permissions.
  -m, --max-items MAX_ITEMS    Maximum number of subitems to display per directory.
  -nc, --no-color              Disable color output.
  -o, --output FILE            Write output to specified file instead of console.
  -r, --directories            Only show directories.
  -s, --size                   Display file size.
  -t, --time                   Display execution time.
  -v, --version                Display version.
  -x, --exclude PATTERN        Exclude paths that contain this pattern.
  -h, --help                   Display this help message.

github: https://github.com/Hellmakima/list-files
"""
    print(help_text)

if __name__ == "__main__":
    # Argument parsing
    parser = ArgumentParser(add_help=False)
    parser.add_argument("directory", nargs="?", default=".", help="Root directory to list.")
    parser.add_argument("-d", "--max-depth", type=int, help="Maximum depth for recursion.")
    parser.add_argument("-g", "--gitignore", action="store_true", help="Ignore .gitignore patterns")
    parser.add_argument("-i", "--include", action='append', help="Only include paths that contain these patterns")
    parser.add_argument("-l", "--list", action="store_true", help="Show file details such as size, date and permissions.")
    parser.add_argument("-m", "--max-items", type=int, help="Maximum number of subitems per directory.")
    parser.add_argument("-nc", "--no-color", action="store_true", help="Disable color output")
    parser.add_argument("-o", "--output", help="Write output to specified file.")
    parser.add_argument("-r", "--directories", action="store_true", help="Only list directories.")
    parser.add_argument("-s", "--size", action="store_true", help="Display file size.")
    parser.add_argument("-t", "--time", action="store_true", help="Display execution time")
    parser.add_argument("-v", "--version", action="store_true", help="Display version")
    parser.add_argument("-x", "--exclude", action='append', help="Exclude paths that contain these patterns")
    parser.add_argument("-h", "--help", action="store_true", help="Display help.")

    args = parser.parse_args()

    if args.time:
        import time
        start_time = time.time()

    # Handle help option
    if args.help:
        display_help()
        sys_exit(0)
    
    if args.version:
        print(f"lsd version 0.2.0")
        sys_exit(0)
    
    if args.list:
        from datetime import datetime
        formatter = datetime.fromtimestamp

    # Validate directory
    directory = args.directory
    if not os_path.exists(directory):
        print(f"Error: Couldn't find '{directory}'.")
        sys_exit(1)

    # Clear output file if it exists
    if args.output and os_path.exists(args.output):
        open(args.output, 'w').close()

    exclude_patterns = args.exclude if args.exclude else []
    if args.gitignore:
        exclude_patterns.append('.git')
    
    # Create lister with patterns
    lister = DirectoryLister(
        include_patterns=args.include if args.include else [],
        exclude_patterns=exclude_patterns,
        directories_only=args.directories,
        show_size=args.size,
        relative_path=directory,
        gitignore=args.gitignore,
        list_details=args.list,
        no_color=args.no_color,
        output_file=args.output
    )

    # List files with options
    try:
        lister.list_files(
            directory=directory,
            max_depth=args.max_depth,
            max_items=args.max_items,
        )

    except KeyboardInterrupt:
        print('...INTR')
        sys_exit(0)

    except Exception as e:
        print(f"{color_red}Error occured: {color_reset} {color_yellow}{e}{color_reset}\a")
        print_stacktrace = input("Want to print stacktrace(y/n)")
        if print_stacktrace.lower() == 'y':
            import traceback
            print(traceback.format_exc())
            print(f"Please report this issue at {color_blue}https://github.com/Hellmakima/list-files/issues{color_reset}")
    
    if args.time:
        end_time = time.time()
        elapsed = end_time - start_time
        print(f"\nExecution time: {color_green}{elapsed:.3f} seconds{color_reset}")
