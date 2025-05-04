# main.py
import argparse
from rich.console import Console
from rich.table import Table
from file import *

def format_usage_bar(percent):
    total_slots = 20
    filled = int((percent / 100) * total_slots)
    bar = "#" * filled + "." * (total_slots - filled)
    return f"[{bar}] {percent:.1f}%"

def truncate_middle(text, max_len=30):
    if len(text) <= max_len:
        return text
    half = (max_len - 3) // 2
    return text[:half] + "..." + text[-half:]

def main():
    parser = argparse.ArgumentParser(prog='py-organize')
    parser.add_argument('-p', '--path', required=True, help="Path to directory to scan") 
    args = parser.parse_args()

    directory = args.path
    files = get_all_files(directory)
    result = process(files)

    console = Console()
    table = Table(show_header=True, header_style="bold magenta")

    table.add_column("D", justify="center")
    table.add_column("File Name", style="cyan", no_wrap=True)
    table.add_column("Type", style="green")
    table.add_column("Size (MB)", justify="right")
    table.add_column("% Usage", justify="left")
    table.add_column("Hash", style="yellow")
    table.add_column("Last Accessed", style="dim", justify="right")

    for f in result:
        size_mb = f["size"] / (1024 * 1024)
        usage_bar = format_usage_bar(f["usage_percent"])
        file_name_display = truncate_middle(f["file_name"], max_len=30)
        file_hash_display = f["hash"] if f["hash"] else "-"

        table.add_row(
            str(f["dflag"]),
            file_name_display,
            f["type"],
            f"{size_mb:.2f}",
            usage_bar,
            file_hash_display,
            f["last_accessed"],
        )

    console.print(table)

if __name__ == "__main__":
    main()
