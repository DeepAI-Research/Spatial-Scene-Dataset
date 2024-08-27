import os

def delete_videos(removal_file):
    # Read the video paths from the removal file
    with open(removal_file, 'r') as f:
        video_paths = f.readlines()

    # Delete each video file
    for video_path in video_paths:
        video_path = video_path.strip()  # Remove any extra whitespace/newlines
        if os.path.exists(video_path):
            os.remove(video_path)
            print(f"Deleted: {video_path}")
        else:
            print(f"File not found, could not delete: {video_path}")

if __name__ == "__main__":
    removal_file = '/Users/ericsheen/Desktop/DeepAI_Research/Spatial-Scene-Dataset/scripts/skipped_videos.txt'  # Replace with your actual file path
    delete_videos(removal_file)
