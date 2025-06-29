# Logic for the Smart Clean-up module
import os
import shutil
import hashlib

# --- Configuration for Temporary Files/Folders ---
TEMP_PATTERNS = {
    "extensions": [".tmp", ".temp", ".bak", ".log", ".chk", ".swp"],
    "files": ["thumbs.db", "desktop.ini"],
    "folders": ["__pycache__", ".pytest_cache", ".mypy_cache", "node_modules", "venv", ".venv"]
}

# --- Helper Functions ---

def get_file_hash(filepath, block_size=65536):
    """Calculates MD5 hash of a file."""
    hasher = hashlib.md5()
    try:
        with open(filepath, 'rb') as f:
            buf = f.read(block_size)
            while len(buf) > 0:
                hasher.update(buf)
                buf = f.read(block_size)
        return hasher.hexdigest()
    except Exception:
        return None # Handle cases where file might be inaccessible

def is_temporary(item_path, item_name, is_dir):
    """Checks if a file or folder is temporary based on TEMP_PATTERNS."""
    name_lower = item_name.lower()
    if is_dir:
        return name_lower in TEMP_PATTERNS["folders"]
    else:
        if name_lower in TEMP_PATTERNS["files"]:
            return True
        for ext in TEMP_PATTERNS["extensions"]:
            if name_lower.endswith(ext):
                return True
    return False

# --- Core Cleaning Functions ---

def find_duplicate_files(directories):
    """
    Scans directories to find duplicate files based on their content hash.
    Returns a dictionary where keys are hashes and values are lists of paths to duplicate files.
    """
    hashes = {}
    duplicates_found = {}
    for directory in directories:
        for dirpath, _, filenames in os.walk(directory):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                if not os.path.exists(filepath) or os.path.islink(filepath): # Skip broken links or non-existent files
                    continue
                file_hash = get_file_hash(filepath)
                if file_hash:
                    if file_hash in hashes:
                        if hashes[file_hash] not in duplicates_found.get(file_hash, []): # Ensure original is added once
                            duplicates_found.setdefault(file_hash, []).append(hashes[file_hash])
                        duplicates_found[file_hash].append(filepath)
                    else:
                        hashes[file_hash] = filepath
    # Filter out unique files, only keep entries with actual duplicates
    return {h: paths for h, paths in duplicates_found.items() if len(paths) > 1}


def remove_temporary_items(directories, dry_run=False, report=None):
    """Removes temporary files and folders."""
    if report is None:
        report = {"deleted_files": 0, "space_recovered": 0, "errors": [], "skipped": []}

    for directory in directories:
        for dirpath, dirnames, filenames in os.walk(directory, topdown=False): # topdown=False for easier dir removal
            # Remove temporary files
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                if is_temporary(filepath, filename, is_dir=False):
                    try:
                        file_size = os.path.getsize(filepath)
                        if not dry_run:
                            os.remove(filepath)
                        print(f"{'[DRY RUN] Would remove' if dry_run else 'Removed'} temporary file: {filepath}")
                        report["deleted_files"] += 1
                        report["space_recovered"] += file_size
                    except Exception as e:
                        error_msg = f"Error removing temporary file {filepath}: {e}"
                        print(error_msg)
                        report["errors"].append(error_msg)

            # Remove temporary directories (after files are processed)
            for dirname in dirnames:
                dir_to_check = os.path.join(dirpath, dirname)
                if is_temporary(dir_to_check, dirname, is_dir=True):
                    try:
                        # For dry run, we'd estimate size. For actual, shutil.rmtree handles size.
                        dir_size = 0
                        if dry_run:
                            for p, _, fnames in os.walk(dir_to_check):
                                for f in fnames:
                                    dir_size += os.path.getsize(os.path.join(p,f))

                        if not dry_run:
                             # Get size before deleting for the report
                            for p, _, fnames in os.walk(dir_to_check):
                                for f in fnames:
                                    report["space_recovered"] += os.path.getsize(os.path.join(p,f))
                            shutil.rmtree(dir_to_check)
                        else:
                            report["space_recovered"] += dir_size # Add estimated size for dry run

                        print(f"{'[DRY RUN] Would remove' if dry_run else 'Removed'} temporary directory: {dir_to_check}")
                        # Note: shutil.rmtree deletes multiple files, we count it as one "directory" operation here for simplicity in reporting deleted items.
                        # A more granular count would be complex if not actually deleting.
                        report["deleted_files"] += 1 # Counting the dir itself as one item
                    except Exception as e:
                        error_msg = f"Error removing temporary directory {dir_to_check}: {e}"
                        print(error_msg)
                        report["errors"].append(error_msg)
    return report


def remove_empty_folders(directories, dry_run=False, report=None):
    """Removes all empty folders within the specified directories."""
    if report is None:
        report = {"deleted_files": 0, "space_recovered": 0, "errors": [], "skipped": []}

    for directory in directories:
        for dirpath, dirnames, filenames in os.walk(directory, topdown=False): # Iterate bottom-up
            if not dirnames and not filenames: # Check if directory is empty
                # Ensure we don't delete the root directory being scanned unless it's explicitly targeted and empty
                if os.path.abspath(dirpath) == os.path.abspath(directory) and not os.listdir(dirpath):
                    pass # Handled by the initial call if the target dir itself is empty
                elif not os.listdir(dirpath): # Redundant check, but safe
                    try:
                        if not dry_run:
                            os.rmdir(dirpath)
                        print(f"{'[DRY RUN] Would remove' if dry_run else 'Removed'} empty directory: {dirpath}")
                        report["deleted_files"] += 1
                        # Space recovered from empty dirs is negligible/zero.
                    except OSError as e: # Catch OSError for non-empty or permission issues
                        error_msg = f"Error removing empty directory {dirpath}: {e}"
                        print(error_msg)
                        if "Directory not empty" not in str(e): # Avoid reporting "not empty" if it was just checked
                             report["errors"].append(error_msg)
                        else:
                            report["skipped"].append(f"Skipped non-empty (or became non-empty) directory: {dirpath}")
                    except Exception as e:
                        error_msg = f"Unexpected error removing empty directory {dirpath}: {e}"
                        print(error_msg)
                        report["errors"].append(error_msg)
    return report


# --- Main Cleaner Function ---

def clean_directories(directories, do_dupes, do_tmp, do_empty, dry_run):
    """
    Main function to orchestrate the cleaning process.
    """
    report = {"deleted_files": 0, "space_recovered": 0, "errors": [], "skipped": []}
    initial_cwd = os.getcwd()

    # Resolve relative paths to absolute paths for consistency
    abs_directories = [os.path.abspath(d) for d in directories]
    for d in abs_directories:
        if not os.path.isdir(d):
            print(f"Error: Directory '{d}' not found. Skipping.")
            report["errors"].append(f"Directory not found: {d}")
            return report # Or continue with other valid directories

    if do_dupes:
        print(f"\n--- {'[DRY RUN] ' if dry_run else ''}Finding Duplicate Files ---")
        duplicates = find_duplicate_files(abs_directories)
        if duplicates:
            print("Found the following duplicate sets:")
            for file_hash, paths in duplicates.items():
                print(f"  Hash: {file_hash}")
                print(f"    Original: {paths[0]}")
                for dup_path in paths[1:]:
                    print(f"    Duplicate: {dup_path}")
                    try:
                        file_size = os.path.getsize(dup_path)
                        if not dry_run:
                            os.remove(dup_path)
                        print(f"      {('[DRY RUN] Would delete' if dry_run else 'Deleted')}: {dup_path}")
                        report["deleted_files"] += 1
                        report["space_recovered"] += file_size
                    except Exception as e:
                        error_msg = f"Error deleting duplicate {dup_path}: {e}"
                        print(f"      {error_msg}")
                        report["errors"].append(error_msg)
        else:
            print("No duplicate files found.")

    if do_tmp:
        print(f"\n--- {'[DRY RUN] ' if dry_run else ''}Removing Temporary Files & Folders ---")
        report = remove_temporary_items(abs_directories, dry_run, report)

    if do_empty:
        print(f"\n--- {'[DRY RUN] ' if dry_run else ''}Removing Empty Folders ---")
        # Run multiple passes for empty folders, as removing some might make others empty
        for _ in range(3): # Arbitrary number of passes, usually 2-3 are enough
            prev_deleted_count = report["deleted_files"]
            report = remove_empty_folders(abs_directories, dry_run, report)
            if report["deleted_files"] == prev_deleted_count: # No change in this pass
                break

    # Final Report
    print("\n--- Cleaning Summary ---")
    if dry_run:
        print("*** DRY RUN MODE: No actual changes were made. ***")

    print(f"Files/folders that would be/were deleted: {report['deleted_files']}")
    space_mb = report['space_recovered'] / (1024 * 1024)
    print(f"Space that would be/was recovered: {report['space_recovered']} bytes ({space_mb:.2f} MB)")

    if report["errors"]:
        print("\nErrors encountered:")
        for err in report["errors"]:
            print(f"  - {err}")
    if report["skipped"]:
        print("\nItems skipped (e.g., became non-empty before deletion):")
        for skip in report["skipped"]:
            print(f"  - {skip}")

    os.chdir(initial_cwd) # Restore original CWD
    return report


if __name__ == '__main__':
    # --- Test Environment Setup ---
    print("Setting up test environment for cleaner.py...")
    test_dir_base = "sta_cleaner_test_area"
    os.makedirs(test_dir_base, exist_ok=True)

    # Dir 1: Mixed content
    dir1 = os.path.join(test_dir_base, "test_dir1")
    os.makedirs(dir1, exist_ok=True)
    os.makedirs(os.path.join(dir1, "__pycache__"), exist_ok=True) # Temp folder
    os.makedirs(os.path.join(dir1, "empty_folder_to_delete"), exist_ok=True) # Empty folder
    os.makedirs(os.path.join(dir1, "folder_with_stuff"), exist_ok=True)

    with open(os.path.join(dir1, "file1.txt"), "w") as f: f.write("This is file1.")
    with open(os.path.join(dir1, "file2.tmp"), "w") as f: f.write("This is a temp file.") # Temp file
    with open(os.path.join(dir1, "duplicate_me.txt"), "w") as f: f.write("I am a duplicate.")
    with open(os.path.join(dir1, "folder_with_stuff", "another_file.txt"), "w") as f: f.write("Content.")

    # Dir 2: More duplicates and temp files
    dir2 = os.path.join(test_dir_base, "test_dir2")
    os.makedirs(dir2, exist_ok=True)
    os.makedirs(os.path.join(dir2, "subfolder", "another_empty_one"), exist_ok=True) # Nested empty

    with open(os.path.join(dir2, "file3.log"), "w") as f: f.write("This is a log file.") # Temp file
    with open(os.path.join(dir2, "duplicate_me_too.txt"), "w") as f: f.write("I am a duplicate.") # Duplicate of file_in_dir1/duplicate_me.txt
    with open(os.path.join(dir2, "subfolder", "original.txt"), "w") as f: f.write("Original content for a duplicate test.")
    with open(os.path.join(dir2, "subfolder", "copy_of_original.txt"), "w") as f: f.write("Original content for a duplicate test.") # Duplicate within same subfolder

    print(f"Test environment created in ./{test_dir_base}")
    print("--- Running Cleaner (Dry Run) ---")
    clean_directories([dir1, dir2], do_dupes=True, do_tmp=True, do_empty=True, dry_run=True)

    print("\n--- Running Cleaner (Actual Run) ---")
    # input("Press Enter to proceed with actual cleaning (will delete files in test_dir)...") # For manual testing
    clean_directories([dir1, dir2], do_dupes=True, do_tmp=True, do_empty=True, dry_run=False)

    print(f"\n--- Verifying Cleanup ---")
    print(f"Contents of {dir1} after clean:")
    if os.path.exists(dir1): print(os.listdir(dir1))
    else: print(f"{dir1} was removed (or should be empty and removed if it was a target and became empty).")

    print(f"Contents of {dir2} after clean:")
    if os.path.exists(dir2): print(os.listdir(dir2))
    else: print(f"{dir2} was removed.")

    # Clean up the test environment
    # input(f"Press Enter to delete the test directory '{test_dir_base}'...")
    try:
        shutil.rmtree(test_dir_base)
        print(f"\nTest environment '{test_dir_base}' removed.")
    except Exception as e:
        print(f"Error removing test environment '{test_dir_base}': {e}")

    # Example of cleaning current directory (use with caution)
    # print("\n--- Running Cleaner on Current Directory (Dry Run) ---")
    # clean_directories(['.'], do_dupes=True, do_tmp=True, do_empty=True, dry_run=True)
