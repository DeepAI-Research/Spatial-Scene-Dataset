import os

# Path to the directory containing the videos
video_directory = '/Users/ericsheen/Desktop/DeepAI_Research/SSD_resized'  # Update with your actual directory path

# Path to the text file containing the valid video IDs
txt_file_path = '/Users/ericsheen/Desktop/DeepAI_Research/Spatial-Scene-Dataset/scripts/video_json_ids.txt'  # Update with your actual text file path

# Read the valid video IDs from the text file
with open(txt_file_path, 'r') as file:
    valid_video_ids = {line.strip().split('.')[0] for line in file}

# Iterate through the videos in the directory
for video_file in os.listdir(video_directory):
    if video_file.endswith('.mp4'):
        # Extract the video ID from the file name
        video_id = video_file.split('_')[1]
        
        # Check if the video ID is not in the list of valid IDs
        if video_id not in valid_video_ids:
            # Construct the full path to the video file
            video_path = os.path.join(video_directory, video_file)
            
            # Delete the video file
            os.remove(video_path)
            print(f"Deleted: {video_path}")

# Output the length of the JSON file (number of valid video IDs)
print(f"Total valid video IDs in text file: {len(valid_video_ids)}")

# Output the number of videos in the folder
remaining_videos = [f for f in os.listdir(video_directory) if f.endswith('.mp4')]
print(f"Total videos remaining in the folder: {len(remaining_videos)}")

# Check if the counts match
if len(valid_video_ids) == len(remaining_videos):
    print("The number of valid video IDs matches the number of videos in the folder.")
else:
    print("Warning: The number of valid video IDs does not match the number of videos in the folder.")
