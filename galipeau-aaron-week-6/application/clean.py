import os
import shutil

# Collect all `__pycache__` directories
def collect_pycache_dirs(root_dir):
    pycache_dirs = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if '__pycache__' in dirnames:
            pycache_dirs.append(os.path.join(dirpath, '__pycache__'))
    return pycache_dirs

# Display directories and prompt for confirmation
def confirm_deletion(pycache_dirs):
    print("The following __pycache__ directories will be deleted:\n")
    for path in pycache_dirs:
        print(f" - {path}")
    
    confirmation = input("\nDo you want to proceed with deletion? (y/n): ").strip().lower()
    return confirmation == 'y'

# Delete directories
def delete_pycache_dirs(pycache_dirs):
    for path in pycache_dirs:
        shutil.rmtree(path)
        print(f"Deleted: {path}")

# Main function
def clean_pycache(root_dir):
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