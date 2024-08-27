import os

# Directory containing the folders
root_directory = '/Users/ericsheen/Desktop/DeepAI_Research/SSD/VidOR'
# Path to the output text file
output_file = '/Users/ericsheen/Desktop/DeepAI_Research/Spatial-Scene-Dataset/output/video_paths.txt'

# List of video file extensions to search for
video_extensions = ('.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv')

def find_video_files(directory):
    video_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(video_extensions):
                full_path = os.path.join(root, file)
                video_files.append(full_path)
    return video_files

def write_paths_in_batches(video_files, output_file, batch_size=100):
    with open(output_file, 'a') as f:
        for i in range(0, len(video_files), batch_size):
            batch = video_files[i:i + batch_size]
            f.write('\n'.join(batch) + '\n')

# Find all video files
video_files = find_video_files(root_directory)

# Write the paths to the text file in batches
write_paths_in_batches(video_files, output_file)

print(f"Paths of video files have been written to {output_file}")
