import os

EXCLUDED_FOLDERS = {"node_modules", "__pycache__", ".venv", ".git", "tree.py", ".gitignore", "utils"}

def display_tree(start_path=".", prefix=""):
    """Recursively prints the directory tree structure, excluding specified folders."""
    try:
        entries = [e for e in os.listdir(start_path) if e not in EXCLUDED_FOLDERS]
    except PermissionError:
        return

    entries.sort()
    entries_count = len(entries)

    for index, entry in enumerate(entries):
        path = os.path.join(start_path, entry)
        is_last = index == entries_count - 1
        connector = "└── " if is_last else "├── "

        print(prefix + connector + entry)

        if os.path.isdir(path):
            extension = "    " if is_last else "│   "
            display_tree(path, prefix + extension)

if __name__ == "__main__":
    print(".")  # Root directory indicator
    display_tree(".")
