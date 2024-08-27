import os

# Path to the directory containing the videos
video_directory = '/Users/ericsheen/Desktop/DeepAI_Research/SSD_resized'  # Update with your actual directory path

# Iterate through each video in the directory
for video_file in os.listdir(video_directory):
    if video_file.endswith('.mp4'):
        # Extract the digits between the underscores and hyphens
        video_id = video_file.split('_')[1].split('-')[0]
        # Construct the new file name
        new_video_name = video_id + '.mp4'
        # Full paths to the original and new video files
        original_video_path = os.path.join(video_directory, video_file)
        new_video_path = os.path.join(video_directory, new_video_name)
        # Rename the video file
        os.rename(original_video_path, new_video_path)
        print(f"Renamed: {video_file} to {new_video_name}")

print("Video renaming completed.")
