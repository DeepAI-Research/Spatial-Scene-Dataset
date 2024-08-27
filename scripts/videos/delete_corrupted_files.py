import subprocess
import os

# Directory containing the MP4 files
directory = '/Users/ericsheen/Desktop/DeepAI_Research/SSD/VidOR/video/0001'

# FFmpeg command to check video integrity
def check_video(file_path):
    command = ['ffmpeg', '-v', 'error', '-i', file_path, '-f', 'null', '-']
    result = subprocess.run(command, stderr=subprocess.PIPE, text=True)
    return result.returncode == 0

# Loop through each file in the directory
for filename in os.listdir(directory):
    if filename.endswith('.mp4'):
        file_path = os.path.join(directory, filename)
        
        # Check video integrity using FFmpeg
        if check_video(file_path):
            print(f"{filename} is valid.")
        else:
            print(f"Cannot process {filename}. Deleting...")
            os.remove(file_path)
