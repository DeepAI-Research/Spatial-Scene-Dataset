import os
import subprocess
import argparse

def convert_avi_to_mp4(avi_file_path, output_name):
    try:
        command = [
            'ffmpeg',
            '-i', avi_file_path,
            '-ac', '2',
            '-b:v', '2000k',
            '-c:a', 'aac',
            '-c:v', 'libx264',
            '-b:a', '160k',
            '-vprofile', 'high',
            '-bf', '0',
            '-strict', 'experimental',
            '-f', 'mp4',
            f'{output_name}.mp4'
        ]
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error converting {avi_file_path}: {e}")
        return False

def convert_videos_in_folder(folder_path, output_folder):
    if not os.path.isdir(folder_path):
        print(f"Error: The directory {folder_path} does not exist.")
        return

    for root, _, files in os.walk(folder_path):
        avi_files = [f for f in files if f.endswith('.avi')]

        if not avi_files:
            continue

        for avi_file in avi_files:
            avi_file_path = os.path.join(root, avi_file)
            # Preserve the directory structure in the output folder
            relative_path = os.path.relpath(root, folder_path)
            output_subfolder = os.path.join(output_folder, relative_path)
            if not os.path.exists(output_subfolder):
                os.makedirs(output_subfolder)
            output_name = os.path.join(output_subfolder, os.path.splitext(avi_file)[0])  # Strip the '.avi' extension
            if convert_avi_to_mp4(avi_file_path, output_name):
                print(f"Converted {avi_file} to {output_name}.mp4")
            else:
                print(f"Failed to convert {avi_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert AVI files to MP4 in a specified folder.")
    parser.add_argument("folder_path", nargs='?', default='/Users/ericsheen/Desktop/DeepAI_Research/SSD/UCF-101', 
                        help="Path to the folder containing AVI files (default: ./test_videos)")
    parser.add_argument("output_folder", nargs='?', default='/Users/ericsheen/Desktop/DeepAI_Research/SSD/output/', 
                        help="Path to the folder where MP4 files will be saved (default: ./output_videos)")
    args = parser.parse_args()

    convert_videos_in_folder(args.folder_path, args.output_folder)
