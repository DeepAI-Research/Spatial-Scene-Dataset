import os
import json

# Paths
json_file_path = '/Users/ericsheen/Desktop/DeepAI_Research/Spatial-Scene-Dataset-Real/data_updated.json'
video_directory = '/Users/ericsheen/Desktop/DeepAI_Research/Spatial-Scene-Dataset-Real'

# Load the JSON data
with open(json_file_path, 'r') as file:
    data = json.load(file)

# Process each entry in the JSON file
for index, item in enumerate(data):
    # Generate a new filename with leading zeros
    new_filename = f"{index:05d}"
    
    # Original video filename (without extension)
    original_filename = item["video"].split('.')[0]
    
    # Full paths to the original and new video files
    original_video_path = os.path.join(video_directory, f"{original_filename}.mp4")
    new_video_path = os.path.join(video_directory, f"{new_filename}.mp4")
    
    # Rename the video file
    os.rename(original_video_path, new_video_path)
    
    # Update the JSON entry with the new filename (without .mp4)
    item["video"] = new_filename

# Save the updated JSON data back to the file
with open(json_file_path, 'w') as file:
    json.dump(data, file, indent=4)

print(f"Video files renamed and JSON updated successfully.")


# import os
# import json

# # Paths
# json_file_path = '/Users/ericsheen/Desktop/DeepAI_Research/Filtered-Synthetic-Scene-Spatial/captions.json'
# video_directory = '/Users/ericsheen/Desktop/DeepAI_Research/Filtered-Synthetic-Scene-Spatial'

# # Load the JSON data
# with open(json_file_path, 'r') as file:
#     data = json.load(file)

# # Set the starting number (e.g., 7949 will make the first video 07950)
# start_number = 7949

# # Process each entry in the JSON file starting from the specified start_number + 1
# for index, item in enumerate(data, start=start_number + 1):
#     # Generate a new filename with leading zeros
#     new_filename = f"{index:05d}"
    
#     # Original video filename (without extension)
#     original_filename = item["video"].split('.')[0]
    
#     # Full paths to the original and new video files
#     original_video_path = os.path.join(video_directory, f"{original_filename}.mp4")
#     new_video_path = os.path.join(video_directory, f"{new_filename}.mp4")
    
#     # Rename the video file
#     if os.path.exists(original_video_path):
#         os.rename(original_video_path, new_video_path)
#         print(f"Renamed: {original_video_path} -> {new_video_path}")
#     else:
#         print(f"File not found: {original_video_path}")
    
#     # Update the JSON entry with the new filename (without .mp4)
#     item["video"] = new_filename

# # Save the updated JSON data back to the same file
# with open(json_file_path, 'w') as file:
#     json.dump(data, file, indent=4)

# print(f"Video files renamed and JSON updated successfully.")
