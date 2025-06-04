#!/usr/bin/env python3
from pathlib import Path
import sys

def rename_and_flatten(base_dir):
    """
    For each file under base_dir:
      1. Build a prefix: base_dir name + any sub-dirs, joined by underscores
      2. Rename the file to prefix_originalname
      3. Move it into base_dir's parent directory
    """
    base = Path(base_dir)
    if not base.is_dir():
        print(f"Error: {base!r} is not a directory.", file=sys.stderr)
        sys.exit(1)

    target_dir = base.parent
    for file_path in base.rglob('*'):
        if not file_path.is_file():
            continue

        # Compute the components: always include base.name, then any subdirs
        rel_parent = file_path.parent.relative_to(base)
        if rel_parent == Path('.'):
            components = [base.name]
        else:
            components = [base.name, *rel_parent.parts]

        prefix = '_'.join(components) + '_'
        new_name = prefix + file_path.name
        new_path = base / new_name

        # Skip if target already exists
        if new_path.exists():
            print(f"Skipping '{file_path}': '{new_name}' already exists in {target_dir}.", file=sys.stderr)
            continue

        # This both renames and moves the file
        file_path.rename(new_path)
        print(f"Moved & renamed:\n  {file_path}\n→ {new_path}")





from pathlib import Path
import shutil

def remove_hidden(path: Path):
    """Remove hidden files and directories recursively."""
    for item in path.rglob('*'):
        if item.name.startswith('.'):
            if item.is_dir():
                shutil.rmtree(item)
                print(f"Removed hidden directory: {item}")
            elif item.is_file():
                item.unlink()
                print(f"Removed hidden file: {item}")

def flatten_and_copy_files(base_dir):
    base_path = Path(base_dir).resolve()

    # Remove hidden files and directories first
    remove_hidden(base_path)

    # Create destination flat directory
    flat_dir = base_path.parent / f"{base_path.name}_flat"
    flat_dir.mkdir(exist_ok=True)

    for file_path in base_path.rglob('*'):
        if file_path.is_file():
            relative_parts = file_path.relative_to(base_path).parts
            new_name = f"{base_path.name}_" + '_'.join(relative_parts)
            destination = flat_dir / new_name

            shutil.copy2(file_path, destination)
            print(f"Copied: {file_path} -> {destination}")


# Example usage
# flatten_and_copy_files('/path/to/your/base_dir')  # Replace with your actual base directory



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} /path/to/base_directory", file=sys.stderr)
        sys.exit(1)
    flatten_and_copy_files(sys.argv[1])
