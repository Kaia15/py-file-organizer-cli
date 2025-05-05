# Python File Organizer CLI
### Progress
![image](https://github.com/user-attachments/assets/a7174620-aaf5-455f-b15d-73941d759878)


## Setup
- git clone `https://github.com/Kaia15/py-file-organizer-cli.git`
- `pip install . ` to install all required packages
- `py-organize --path [dir]` to grab all the files you want to review and get the information

## Requirements
- Find all files with any extensions (.txt, .exe, .pdf, .png, etc) in the current parameter directory
- Raise `D = 1`-flag if there are any duplicated files and provide the sharing hash among those files
- Sort all files in descending order (memory-based)
- Calculate scores of each file to recommend deletion (free memory)
- Categorize files based on each type(extension)
- For some `installer` or `.exe`, find the corresponding applications with their setup program, if found, mark it red in the data table to **highly recommend delete**
- Utilize *multithreading* to process all files (will need a benchmark to compare later on)
- Optional: recursively walk through non-empty folders and apply the same thing as done with files
  
## Libraries
- `tqdm, os, multithreading, setuptools`
