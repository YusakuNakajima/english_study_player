import shutil

def clean_trailing_pipes(filename):
    """
    Removes trailing pipe characters from each line of a file.
    A backup of the original file is created with a .bak extension.
    """
    backup_filename = filename + '.bak'
    shutil.copy(filename, backup_filename)
    print(f"Backed up {filename} to {backup_filename}")

    with open(backup_filename, 'r', encoding='utf-8') as infile, open(filename, 'w', encoding='utf-8') as outfile:
        for line in infile:
            # rstrip('|') will remove trailing pipes and newlines
            # so we add the newline back.
            cleaned_line = line.rstrip('|') + '\n'
            outfile.write(cleaned_line)
    
    print(f"Cleaned {filename}")

if __name__ == "__main__":
    clean_trailing_pipes('vocabulary_data_all.csv')
