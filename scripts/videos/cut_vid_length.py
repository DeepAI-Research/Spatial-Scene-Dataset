# import os
# import subprocess
# import json

# def get_video_duration(file_path):
#     cmd = [
#         'ffprobe',
#         '-v', 'quiet',
#         '-print_format', 'json',
#         '-show_format',
#         '-show_streams',
#         file_path
#     ]
#     result = subprocess.run(cmd, capture_output=True, text=True)
#     data = json.loads(result.stdout)
#     return float(data['format']['duration'])

# def cut_video(input_file, output_file, max_duration):
#     cmd = [
#         'ffmpeg',
#         '-y',  # Overwrite without prompting
#         '-i', input_file,
#         '-t', str(max_duration),
#         '-c', 'copy',
#         output_file
#     ]
#     try:
#         subprocess.run(cmd, check=True)
#     except subprocess.CalledProcessError:
#         print(f"Failed to cut {input_file} directly. Re-encoding and trying again...")
#         re_encode_and_cut(input_file, output_file, max_duration)

# def re_encode_and_cut(input_file, output_file, max_duration):
#     temp_file = output_file + ".temp.mp4"
    
#     re_encode_cmd = [
#         'ffmpeg',
#         '-i', input_file,
#         '-vf', 'scale=trunc(iw/2)*2:trunc(ih/2)*2',  # Scale to ensure dimensions are divisible by 2
#         '-c:v', 'libx264',   # Re-encode video to H.264
#         '-c:a', 'aac',       # Re-encode audio to AAC
#         '-strict', 'experimental',  # Necessary for some versions of ffmpeg to use AAC
#         '-y',  # Overwrite temp file without prompting
#         temp_file
#     ]
    
#     try:
#         subprocess.run(re_encode_cmd, check=True)
#         final_cut_cmd = [
#             'ffmpeg',
#             '-y',
#             '-i', temp_file,
#             '-t', str(max_duration),
#             '-c', 'copy',
#             output_file
#         ]
#         subprocess.run(final_cut_cmd, check=True)
#     finally:
#         if os.path.exists(temp_file):
#             os.remove(temp_file)

# def process_videos(input_folder, output_folder, max_duration, min_threshold):
#     if not os.path.exists(output_folder):
#         os.makedirs(output_folder)

#     for root, _, files in os.walk(input_folder):
#         for filename in files:
#             if filename.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
#                 input_path = os.path.join(root, filename)
#                 relative_path = os.path.relpath(root, input_folder)
#                 output_dir = os.path.join(output_folder, relative_path)
                
#                 if not os.path.exists(output_dir):
#                     os.makedirs(output_dir)
                
#                 output_path = os.path.join(output_dir, f"cut_{filename}")

#                 duration = get_video_duration(input_path)

#                 if duration > max_duration:
#                     print(f"Cutting {filename} to {max_duration} seconds")
#                     cut_video(input_path, output_path, max_duration)
#                 elif min_threshold <= duration <= max_duration:
#                     print(f"{filename} is already shorter than {max_duration} seconds but longer than {min_threshold} seconds. Copying without cutting.")
#                     # Copy the video without cutting
#                     cmd = ['ffmpeg', '-y', '-i', input_path, '-c', 'copy', output_path]
#                     try:
#                         subprocess.run(cmd, check=True)
#                     except subprocess.CalledProcessError:
#                         print(f"Failed to copy {input_path}. Re-encoding and trying again...")
#                         re_encode_and_cut(input_path, output_path, max_duration)
#                 else:
#                     print(f"{filename} is shorter than {min_threshold} seconds. Skipping.")
#                     with open("skipped_videos.txt", "a") as file:
#                         file.write(f"{input_path}\n")

# if __name__ == "__main__":
#     input_folder = "/Users/ericsheen/Desktop/DeepAI_Research/SpatialSceneDatasetProcessed"
#     output_folder = "/Users/ericsheen/Desktop/DeepAI_Research/SSD"
#     max_duration = 6  # maximum duration in seconds
#     min_threshold = 5  # minimum threshold in seconds

#     process_videos(os.path.expanduser(input_folder), os.path.expanduser(output_folder), max_duration, min_threshold)

import os
import subprocess
import json

def get_video_duration(file_path):
    cmd = [
        'ffprobe',
        '-v', 'quiet',
        '-print_format', 'json',
        '-show_format',
        '-show_streams',
        file_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    data = json.loads(result.stdout)
    return float(data['format']['duration'])

def cut_video(input_file, output_file, max_duration):
    cmd = [
        'ffmpeg',
        '-y',  # Overwrite without prompting
        '-i', input_file,
        '-t', str(max_duration),
        '-c', 'copy',
        output_file
    ]
    try:
        subprocess.run(cmd, check=True)
        # Delete the original video if cutting was successful
        os.remove(input_file)
    except subprocess.CalledProcessError:
        print(f"Failed to cut {input_file} directly. Re-encoding and trying again...")
        re_encode_and_cut(input_file, output_file, max_duration)

def re_encode_and_cut(input_file, output_file, max_duration):
    temp_file = output_file + ".temp.mp4"
    
    re_encode_cmd = [
        'ffmpeg',
        '-i', input_file,
        '-vf', 'scale=trunc(iw/2)*2:trunc(ih/2)*2',  # Scale to ensure dimensions are divisible by 2
        '-c:v', 'libx264',   # Re-encode video to H.264
        '-c:a', 'aac',       # Re-encode audio to AAC
        '-strict', 'experimental',  # Necessary for some versions of ffmpeg to use AAC
        '-y',  # Overwrite temp file without prompting
        temp_file
    ]
    
    try:
        subprocess.run(re_encode_cmd, check=True)
        final_cut_cmd = [
            'ffmpeg',
            '-y',
            '-i', temp_file,
            '-t', str(max_duration),
            '-c', 'copy',
            output_file
        ]
        subprocess.run(final_cut_cmd, check=True)
        # Delete the original video if re-encoding and cutting was successful
        os.remove(input_file)
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)

def process_videos(input_folder, output_folder, max_duration):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for root, _, files in os.walk(input_folder):
        for filename in files:
            if filename.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
                input_path = os.path.join(root, filename)
                relative_path = os.path.relpath(root, input_folder)
                output_dir = os.path.join(output_folder, relative_path)
                
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                
                output_path = os.path.join(output_dir, f"cut_{filename}")

                duration = get_video_duration(input_path)

                if duration > max_duration:
                    print(f"Cutting {filename} to {max_duration} seconds")
                    cut_video(input_path, output_path, max_duration)
                else:
                    print(f"{filename} is shorter than {max_duration} seconds. Skipping.")
                    with open("skipped_videos.txt", "a") as file:
                        file.write(f"{input_path}\n")

if __name__ == "__main__":
    input_folder = "/Users/ericsheen/Desktop/DeepAI_Research/SSD"
    output_folder = "/Users/ericsheen/Desktop/DeepAI_Research/SSD_Cut_Part2"
    max_duration = 6  # maximum duration in seconds

    process_videos(os.path.expanduser(input_folder), os.path.expanduser(output_folder), max_duration)
