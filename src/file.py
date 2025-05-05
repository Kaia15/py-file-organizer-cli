# process.py
import os
import hashlib
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
import datetime
from tqdm import tqdm
import time

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
        'mov': 'Video',
        'exe': 'Installer',
        'zip': 'Compressed Folder',
        'txt': 'Text',
        'ipynb': 'Jupyter Notebook'
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
            last_accessed = os.path.getmtime(filepath)
            last_accessed_str = datetime.datetime.fromtimestamp(last_accessed).strftime('%Y-%m-%d %H:%M:%S')
            return filehash, {
                "file_name": filename,
                "type": filecategory,
                "size": filesize,
                "path": filepath,
                "last_accessed": last_accessed_str
            }
        except Exception:
            return None

    def suggest_deletion(file, now=None):
        now = now or time.time()
        last_access_age_days = (now - os.path.getatime(file["path"])) / 86400

        score = 0

        # Duplicate files
        if file["dflag"] == 1:
            score += 3

        # Old files
        if last_access_age_days > 180:
            score += 2

        # Download or temp folders
        if "downloads" in file["path"].lower() or "temp" in file["path"].lower():
            score += 1

        # Small usage footprint
        if file["usage_percent"] > 5 or file["usage_percent"] < 0.5:
            score += 3

        # Bonus weights by type
        if file["type"] == "Installer" and "downloads" in file["path"].lower():
            score += 2
        elif file["type"] == "Compressed Folder":
            score += 2
        elif file["type"] == "Jupyter Notebook":
            score -= 2  # usually important
        elif file["type"] == "Text":
            score -= 1  # low priority to delete

        return {
            "suggest_delete": score >= 4,
            "deletion_score": score
        }

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
    now = time.time()
    for f in all_processed:
        f["usage_percent"] = round((f["size"] / total_size) * 100, 1) if total_size else 0.0
        suggestions = suggest_deletion(f, now)
        f.update(suggestions)
    return sorted(all_processed, key=lambda x: x["size"], reverse=True)
