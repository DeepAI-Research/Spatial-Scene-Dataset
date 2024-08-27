import os
import shutil

def copy_videos_with_rename(src_folder, dest_folder, video_extensions=None):
    if video_extensions is None:
        video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv']

    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    for root, _, files in os.walk(src_folder):
        for file in files:
            if any(file.lower().endswith(ext) for ext in video_extensions):
                source_path = os.path.join(root, file)
                # Extract relevant parts of the path to rename the file
                relative_path = os.path.relpath(root, src_folder)
                path_parts = relative_path.split(os.sep)

                # Determine the new file name based on the parent folder structure
                if "UCF-101" in path_parts:
                    # UCF-101 specific renaming
                    new_name = f"{path_parts[0]}-{file}"
                else:
                    # VidOR specific renaming
                    new_name = "-".join(path_parts) + f"-{file}"

                destination_path = os.path.join(dest_folder, new_name)

                print(f"Copying {source_path} to {destination_path}")
                shutil.copy2(source_path, destination_path)

if __name__ == "__main__":
    src_folder = "/Users/ericsheen/Desktop/DeepAI_Research/SSD/processed_cut"
    dest_folder = "/Users/ericsheen/Desktop/DeepAI_Research/SSD/processed_final"

    copy_videos_with_rename(src_folder, dest_folder)
