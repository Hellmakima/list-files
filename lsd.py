import os
import sys

def print_help():
    """Displays help information."""
    help_text = """
Usage: python lsd.py [DIRECTORY] [-n MAX_DEPTH]
<or>
Usage: lsd [DIRECTORY] [-n MAX_DEPTH]

Arguments:
  DIRECTORY       The root directory to list. Defaults to the current directory.
  -n MAX_DEPTH    Maximum recursion depth from the starting location. Default is infinite.
  -h, --help, /?  Display this help message.

Example:
  python lsd.py ../Downloads/test -n 2
  This will list files and directories up to 2 levels deep starting at ../Downloads/test.
  others:
      py lsd.py
      py lsd.py -n 1
      py lsd.py new
NOTE: replace "python lsd.py" with whatever you have named your exe file
"""
    print(help_text)

def list_files(directory, level=0, max_depth=None):
    """Recursively lists all files and directories up to a specified depth."""
    try:
        # Stop if maximum depth is reached
        if max_depth is not None and level >= max_depth:
            return

        # Formatting
        indent = '│   ' * level
        dir_prefix = '├── '
        file_prefix = '└── '

        # Separate directories and files
        dirs = []
        files = []
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            if os.path.isdir(item_path):
                dirs.append(item)
            else:
                files.append(item)

        # Sort directories and files
        dirs.sort()
        files.sort()

        # Print directories first
        for i, dir_name in enumerate(dirs):
            connector = file_prefix if i == len(dirs) - 1 and not files else dir_prefix
            print(f"{indent}{connector}{dir_name}/")
            # Recurse into the subdirectory
            list_files(os.path.join(directory, dir_name), level + 1, max_depth)

        # Print files
        for i, file_name in enumerate(files):
            connector = file_prefix if i == len(files) - 1 else dir_prefix
            print(f"{indent}{connector}{file_name}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    import argparse

    # Argument parsing
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("directory", nargs="?", default=".", help="Root directory to list.")
    parser.add_argument("-n", "--max-depth", type=int, help="Maximum depth for recursion.")
    parser.add_argument("-h", "--help", action="store_true", help="Display help.")

    args = parser.parse_args()

    # Handle help option
    if args.help or args.__dict__.get('/?'):
        print_help()
        sys.exit(0)

    # Validate directory
    directory = args.directory
    if not os.path.exists(directory):
        print(f"Error: The directory '{directory}' does not exist.")
        sys.exit(1)

    # List files with optional max depth
    list_files(directory, max_depth=args.max_depth)
