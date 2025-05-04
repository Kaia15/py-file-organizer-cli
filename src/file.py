# process.py
import os
import hashlib
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
import datetime
from tqdm import tqdm

def get_all_files(directory):
    files = []
    for f in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, f)):
            file_path = os.path.join(directory, f)
            file_name = os.path.basename(file_path)
            files.append((file_name, file_path))
    return files

def get_file_size(file_path):
    return os.path.getsize(file_path)

def hash_file(path):
    hasher = hashlib.md5()
    blocksize = 65536
    try:
        with open(path, 'rb') as afile:
            while chunk := afile.read(blocksize):
                hasher.update(chunk)
        return hasher.hexdigest()
    except Exception:
        return None

def categorize(filepath):
    file_categories = {
        'jpg': 'Images',
        'jpeg': 'Images',
        'png': 'Images',
        'pdf': 'Documents',
        'doc': 'Documents',
        'docx': 'Documents',
        'mp3': 'Audio',
        'wav': 'Audio',
        'mp4': 'Video',
        'mov': 'Video'
    }
    _, extension = os.path.splitext(filepath)
    return file_categories.get(extension[1:].lower(), "Other")

def process(files):
    def worker(file_tuple):
        filename, filepath = file_tuple
        try:
            filehash = hash_file(filepath)
            if filehash is None:
                return None
            filecategory = categorize(filepath)
            filesize = get_file_size(filepath)
            last_accessed = os.path.getatime(filepath)
            last_accessed_str = datetime.datetime.fromtimestamp(last_accessed).strftime('%Y-%m-%d %H:%M:%S')
            return filehash, {
                "file_name": filename,
                "type": filecategory,
                "size": filesize,
                "last_accessed": last_accessed_str
            }
        except Exception:
            return None

    duplicates = defaultdict(list)
    all_processed = []

    with ThreadPoolExecutor() as executor:
        for result in tqdm(executor.map(worker, files), total=len(files), desc="Processing files"):
            if result:
                filehash, file_info = result
                duplicates[filehash].append(file_info)

    for filehash, file_list in duplicates.items():
        for f in file_list:
            f["dflag"] = 1 if len(file_list) > 1 else 0
            f["hash"] = filehash if f["dflag"] == 1 else ""
            all_processed.append(f)

    total_size = sum(f["size"] for f in all_processed)
    for f in all_processed:
        f["usage_percent"] = round((f["size"] / total_size) * 100, 1) if total_size else 0.0

    return sorted(all_processed, key=lambda x: x["size"], reverse=True)
