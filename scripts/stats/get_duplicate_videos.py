import os
from collections import defaultdict

# Path to the directory containing the videos
video_directory = '/Users/ericsheen/Desktop/DeepAI_Research/Spatial-Scene-Synthetic-Dataset'
output_file = './duplicate_videos.txt'

# Step 1: Create a dictionary to store video filenames and their full paths
video_files = defaultdict(list)

# Step 2: Traverse the video directory and populate the dictionary
for root, _, files in os.walk(video_directory):
    for file_name in files:
        if file_name.endswith('.mp4'):
            full_path = os.path.join(root, file_name)
            video_files[file_name].append(full_path)

# Step 3: Identify duplicate filenames
duplicates = {file_name: paths for file_name, paths in video_files.items() if len(paths) > 1}

# Step 4: Write duplicate video filenames and their paths to a text file
with open(output_file, 'w') as file:
    for file_name, paths in duplicates.items():
        file.write(f"Duplicate filename: {file_name}\n")
        for path in paths:
            file.write(f" - {path}\n")
        file.write("\n")

if duplicates:
    print(f"Duplicate video filenames have been saved to {output_file}")
else:
    print("No duplicate video filenames found.")
