import os
from pathlib import Path

FOLDER     = Path("/Users/ax/Downloads/Project Y")
PREFIX     = "Project Y"
# you can choose to rename only one type of files, or all files
EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".heic"}

images = [f for f in FOLDER.iterdir() if f.suffix.lower() in EXTENSIONS]

# sort the files in the list by their full path
images.sort()

for i, filepath in enumerate(images):
    new_name = PREFIX + "_" + str(i + 1).zfill(4) + filepath.suffix.lower()
    os.rename(filepath, FOLDER / new_name)
    print(str(filepath.name) + " -> " + new_name)
