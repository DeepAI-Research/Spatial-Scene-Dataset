import os
import shutil

def copy_videos(src_folder, dst_folder):
    # Ensure the destination folder exists
    if not os.path.exists(dst_folder):
        os.makedirs(dst_folder)
    
    # Video file extensions to consider
    video_extensions = ('.mp4', '.avi', '.mkv', '.mov', '.flv', '.wmv', '.mpeg', '.mpg')
    
    # Iterate over all files in the source folder
    for filename in os.listdir(src_folder):
        src_file = os.path.join(src_folder, filename)
        dst_file = os.path.join(dst_folder, filename)
        
        # Check if the item is a video file
        if os.path.isfile(src_file) and filename.lower().endswith(video_extensions):
            shutil.copy2(src_file, dst_file)  # copy2 preserves metadata like timestamps
            print(f"Copied {filename} to {dst_folder}")

# Define the source and destination folders
source_folder = '/Users/ericsheen/Desktop/DeepAI_Research/SSD/processed_final'
destination_folder = '/Users/ericsheen/Desktop/DeepAI_Research/SpatialSceneDataset'

# Call the function to copy the video files
copy_videos(source_folder, destination_folder)
