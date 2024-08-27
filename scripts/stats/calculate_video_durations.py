import os
import subprocess
import json
from datetime import timedelta
from collections import defaultdict

def get_video_duration(file_path):
    cmd = [
        'ffprobe',
        '-v', 'quiet',
        '-print_format', 'json',
        '-show_format',
        '-show_streams',
        file_path
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        data = json.loads(result.stdout)
        return float(data['format']['duration'])
    except (subprocess.CalledProcessError, json.JSONDecodeError, KeyError):
        print(f"Error processing file: {file_path}")
        return 0

def is_video_file(filename):
    video_extensions = ('.avi', '.mp4', '.mov', '.mkv', '.wmv', '.flv', '.webm')
    return filename.lower().endswith(video_extensions)

def calculate_durations(root_directory):
    total_duration = 0
    total_video_count = 0
    subfolder_durations = defaultdict(lambda: {'duration': 0, 'count': 0})
    
    for dirpath, dirnames, filenames in os.walk(root_directory):
        for filename in filenames:
            if is_video_file(filename):
                file_path = os.path.join(dirpath, filename)
                duration = get_video_duration(file_path)
                
                relative_path = os.path.relpath(dirpath, root_directory)
                subfolder = relative_path.split(os.sep)[0] if relative_path != '.' else 'root'
                
                total_duration += duration
                total_video_count += 1
                subfolder_durations[subfolder]['duration'] += duration
                subfolder_durations[subfolder]['count'] += 1
                
                print(f"Processed: {os.path.join(relative_path, filename)} - Duration: {timedelta(seconds=int(duration))}")
    
    return total_duration, total_video_count, subfolder_durations

def format_duration(seconds):
    return str(timedelta(seconds=int(seconds)))

if __name__ == "__main__":
    ssd_path = os.path.expanduser("/Users/ericsheen/Desktop/DeepAI_Research/Spatial-Scene-Synthetic-Dataset")  # Adjust this path if needed
    
    if not os.path.exists(ssd_path):
        print(f"Error: The directory {ssd_path} does not exist.")
    else:
        total_duration, total_video_count, subfolder_durations = calculate_durations(ssd_path)
        
        print("\nSubfolder Durations:")
        for subfolder, data in subfolder_durations.items():
            print(f"Duration of videos in the {subfolder} folder: {format_duration(data['duration'])} (Video count: {data['count']})")
        
        print(f"\nTotal number of videos processed: {total_video_count}")
        print(f"Total duration across all folders: {format_duration(total_duration)}")
        print(f"Total duration in seconds: {total_duration:.2f}")