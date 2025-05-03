import os
from concurrent.futures import ThreadPoolExecutor

def get_all_files(directory):
    return [os.path.join(directory, f) for f in os.listdir(directory)
            if os.path.isfile(os.path.join(directory, f))]

def get_file_size(file_path):
    return (os.path.basename(file_path), os.path.getsize(file_path))