from file import *
from concurrent.futures import ThreadPoolExecutor
import argparse

def main():
    parser = argparse.ArgumentParser(prog='py-organize')
    parser.add_argument('-p', '--path') 
    args = parser.parse_args()

    directory = args.path

    files = get_all_files(directory)
    with ThreadPoolExecutor(max_workers=5) as executor:
        result = executor.map(get_file_size, files)
    for r in result:
        print(r)