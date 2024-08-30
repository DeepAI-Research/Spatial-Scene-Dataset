import os
import json
import shutil


# Paths
json_file_path = '/Users/ericsheen/Desktop/DeepAI_Research/Spatial-Scene-Dataset-Real/data_updated.json'
videos_folder_path = '/Users/ericsheen/Desktop/DeepAI_Research/Spatial-Scene-Dataset-Real'
output_videos_folder = '/Users/ericsheen/Desktop/DeepAI_Research/SSD-CogVideo-Format/videos'
output_labels_folder = '/Users/ericsheen/Desktop/DeepAI_Research/SSD-CogVideo-Format/labels'

# Create output directories if they don't exist
os.makedirs(output_videos_folder, exist_ok=True)
os.makedirs(output_labels_folder, exist_ok=True)

# Load JSON data
with open(json_file_path, 'r') as json_file:
    data = json.load(json_file)

# Process each entry in the JSON
for entry in data:
    video_name = entry['video']
    caption = entry['caption']
    
    # Paths for the new video and label files
    video_src_path = os.path.join(videos_folder_path, f'{video_name}.mp4')
    video_dst_path = os.path.join(output_videos_folder, f'{video_name}.mp4')
    label_dst_path = os.path.join(output_labels_folder, f'{video_name}.txt')
    
    # Copy video to the new directory
    if os.path.exists(video_src_path):
        shutil.copy(video_src_path, video_dst_path)
    else:
        print(f"Warning: {video_src_path} does not exist.")
    
    # Write caption to the corresponding text file
    with open(label_dst_path, 'w') as label_file:
        label_file.write(caption)

print("Reorganization complete!")
