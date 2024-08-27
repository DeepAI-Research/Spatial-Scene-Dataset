import os
import json

# Path to the directory containing the videos
video_dir = "/Users/ericsheen/Desktop/DeepAI_Research/SSD"

# Path to the data.json file
data_json = "/Users/ericsheen/Desktop/DeepAI_Research/Spatial-Scene-Dataset/data/data.json"

# Path to the files containing the video paths
json_video_paths_file = "json_video_paths.txt"
dir_video_paths_file = "dir_video_paths.txt"
missing_videos_file = "missing_videos.txt"

# Load the data from the JSON file
with open(data_json, "r") as f:
    data = json.load(f)

# Write the video paths from the JSON data to a file
with open(json_video_paths_file, "w") as f:
    for item in data:
        f.write(item["video"] + "\n")

# Write the absolute video paths from the directory to a file
with open(dir_video_paths_file, "w") as f:
    for filename in os.listdir(video_dir):
        if filename.endswith(".mp4"):
            video_path = os.path.join(video_dir, filename)
            f.write(video_path + "\n")

# Read the video paths from the text files
with open(json_video_paths_file, "r") as f:
    json_video_paths = set(path.strip() for path in f.readlines())

with open(dir_video_paths_file, "r") as f:
    dir_video_paths = set(path.strip() for path in f.readlines())

# Find the missing video paths
json_missing_videos = dir_video_paths - json_video_paths
dir_missing_videos = json_video_paths - dir_video_paths

# Write the missing video paths to a file
with open(missing_videos_file, "w") as f:
    for path in json_missing_videos:
        f.write(path + "\n")
    for path in dir_missing_videos:
        f.write(path + "\n")

print("Video paths written to files.")