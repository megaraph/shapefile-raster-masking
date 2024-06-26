import time
from config import OUT_DIR_PATH, OUT_EXT

def rename_files():
    # List all files in output masked directory
    masked_files = [file for file in OUT_DIR_PATH.iterdir() if file.is_file and file.suffix.lower() == OUT_EXT]

    for index, file in enumerate(masked_files):
        # Define the new filename path 1.png, 2.png, ... *.png
        new_name = f"{index + 1}{file.suffix}"
        new_file = file.with_name(new_name)

        # Rename the file
        file.rename(new_file)
        print(f"Renamed {file} to {new_file}")
    
    return len(masked_files)


if __name__ == "__main__":
    start_time = time.time()
    rename_count = rename_files()
    end_time = time.time()

    elapsed_time = end_time - start_time
    print(f"\nRenamed {rename_count} files in {elapsed_time:.2f} seconds")
