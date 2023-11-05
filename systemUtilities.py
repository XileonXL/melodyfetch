import os

def get_folders_in_current_dir():
    folders = [folder for folder in os.listdir() if os.path.isdir(folder)]
    return folders

def read_file(filename):
    lines = []
    with open(filename, 'r') as f:
        for line in f:
            lines.append(line.strip())
    return lines
