"""
This script provides functionality to clean up `__pycache__` directories within a specified root directory.

Functions:
    collect_pycache_dirs(root_dir)
    confirm_deletion(pycache_dirs)
    delete_pycache_dirs(pycache_dirs)
    clean_pycache(root_dir)

Usage:
    Run this script directly to clean up `__pycache__` directories within the current directory:
        python clean.py
"""
import os
import shutil

# Collect all `__pycache__` directories
def collect_pycache_dirs(root_dir):
    """
    Collects all directories named '__pycache__' within a given root directory.

    This function walks through the directory tree starting from the specified 
    root directory and collects the paths of all directories named '__pycache__'.

    Args:
        root_dir (str): The root directory to start the search from.

    Returns:
        list: A list of paths to '__pycache__' directories found within the root directory.
    """
    pycache_dirs = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if '__pycache__' in dirnames:
            pycache_dirs.append(os.path.join(dirpath, '__pycache__'))
    return pycache_dirs

# Display directories and prompt for confirmation
def confirm_deletion(pycache_dirs):
    """
    Prompts the user to confirm the deletion of specified __pycache__ directories.
    Args:
        pycache_dirs (list of str): A list of paths to __pycache__ directories to be deleted.
    Returns:
        bool: True if the user confirms the deletion (inputs 'y'), False otherwise.
    """
    print("The following __pycache__ directories will be deleted:\n")
    for path in pycache_dirs:
        print(f" - {path}")
    
    confirmation = input("\nDo you want to proceed with deletion? (y/n): ").strip().lower()
    return confirmation == 'y'

# Delete directories
def delete_pycache_dirs(pycache_dirs):
    """
    Deletes the specified list of __pycache__ directories.

    Args:
        pycache_dirs (list of str): A list of paths to the __pycache__ directories to be deleted.

    Returns:
        None

    Example:
        delete_pycache_dirs(['/path/to/__pycache__', '/another/path/to/__pycache__'])
    """
    for path in pycache_dirs:
        shutil.rmtree(path)
        print(f"Deleted: {path}")

# Main function
def clean_pycache(root_dir):
    """
    Cleans up all __pycache__ directories within the specified root directory.
    This function searches for all __pycache__ directories within the given 
    root directory, confirms with the user if they want to delete them, and 
    then deletes them if confirmed.
    Args:
        root_dir (str): The root directory to search for __pycache__ directories.
    Returns:
        None
    """
    pycache_dirs = collect_pycache_dirs(root_dir)
    
    if not pycache_dirs:
        print("No __pycache__ directories found.")
        return
    
    if confirm_deletion(pycache_dirs):
        delete_pycache_dirs(pycache_dirs)
        print("Cleanup completed.")
    else:
        print("Cleanup aborted.")

# Usage
if __name__ == '__main__':
    clean_pycache(".")