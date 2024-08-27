# import os

# # Directory containing the video files
# directory = '/Users/ericsheen/Desktop/DeepAI_Research/SSD_resized'  # Change this to your folder path

# # Output file to save the IDs
# output_file = './video_ids.txt'

# # List to store the extracted IDs
# video_ids = []

# # Iterate over all files in the directory
# for filename in os.listdir(directory):
#     if filename.endswith('.mp4'):
#         # Extract the ID from the filename
#         id_part = filename.split('_')[1]
#         video_ids.append(id_part)

# # Write the IDs to the output file
# with open(output_file, 'w') as f:
#     for video_id in video_ids:
#         f.write(f"{video_id}\n")

# # Print the number of IDs
# print(f"Number of video IDs: {len(video_ids)}")

import json

# Path to your JSON file
json_file = '/Users/ericsheen/Desktop/DeepAI_Research/SSD_resized/data_updated.json'  # Replace with the correct path

# Output file to save the IDs
output_file = 'video_json_ids.txt'

# Load the JSON data
with open(json_file, 'r') as f:
    data = json.load(f)

# List to store the extracted IDs
video_ids = []

# Iterate over each entry in the JSON data
for entry in data:
    # Extract the video filename
    video_filename = entry['video']
    
    # Add the extracted ID to the list
    video_ids.append(video_filename)

# Write the IDs to the output file
with open(output_file, 'w') as f:
    for video_id in video_ids:
        f.write(f"{video_id}\n")

# Print the number of IDs
print(f"Number of video IDs: {len(video_ids)}")
