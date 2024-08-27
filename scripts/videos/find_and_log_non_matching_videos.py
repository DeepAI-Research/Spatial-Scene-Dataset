import os
from get_vid_res import get_video_resolution_and_size

def find_videos_with_different_resolution(root_dir, target_resolution, batch_size=100):
    non_matching_videos = []
    batch_count = 0
    total_videos = 0
    total_non_matching = 0
    
    for root, dirs, files in os.walk(root_dir):
        print(f"Scanning directory: {root}")  # Debug statement
        for file in files:
            if file.lower().endswith(('.mp4', '.mkv', '.avi', '.mov')):
                file_path = os.path.join(root, file)
                print(f"Processing file: {file_path}")  # Debug statement
                resolution, size = get_video_resolution_and_size(file_path)
                print(f"Resolution obtained: {resolution}")  # Debug statement
                total_videos += 1
                if resolution:
                    if resolution != target_resolution:
                        print(f"Non-matching video: {file_path}")  # Debug statement
                        non_matching_videos.append(file_path)
                        total_non_matching += 1
                        # Write to file in batches
                        batch_count += 1
                        if batch_count >= batch_size:
                            write_results_to_file(output_file, non_matching_videos, total_videos, total_non_matching)
                            non_matching_videos.clear()  # Clear the list after writing
                            batch_count = 0
                else:
                    print(f"Could not determine resolution for: {file_path}")  # Debug statement
    
    # Write any remaining results that didn't reach the batch size
    if non_matching_videos:
        write_results_to_file(output_file, non_matching_videos, total_videos, total_non_matching)
    
    print(f"Total videos processed: {total_videos}")  # Debug statement
    print(f"Total non-matching videos found: {total_non_matching}")  # Debug statement
    return total_videos, total_non_matching

def write_results_to_file(file_path, video_list, total_videos, total_non_matching):
    print(f"Writing results to: {file_path}")  # Debug statement
    try:
        # Read existing content
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                lines = f.readlines()
        else:
            lines = []

        # Update header with updated counts
        header = [
            f"Total videos processed: {total_videos}\n",
            f"Total non-matching videos: {total_non_matching}\n"
        ]

        # Write updated header and append new content
        with open(file_path, 'w') as f:
            f.writelines(header)
            if len(lines) > 2:
                f.writelines(lines[2:])  # Skip the old header

        # Append non-matching videos
        with open(file_path, 'a') as f:
            for video in video_list:
                f.write(f"{video}\n")
        
        print("File writing successful!")  # Debug statement
    except Exception as e:
        print(f"Error writing to file: {e}")

if __name__ == "__main__":
    root_directory = "/Users/ericsheen/Desktop/DeepAI_Research/SSD/VidOR/"
    target_resolution = "720x480"
    output_file = "/Users/ericsheen/Desktop/DeepAI_Research/Spatial-Scene-Dataset/output/non_matching_videos.txt"  # Ensure this path is correct
    
    print("Starting the search...")  # Debug statement
    total_videos, total_non_matching = find_videos_with_different_resolution(root_directory, target_resolution)
    
    print(f"Videos not matching the resolution {target_resolution} have been written to {output_file}.")