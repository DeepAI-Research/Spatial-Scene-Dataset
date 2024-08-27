import random

def select_videos_for_removal(input_file, output_file, removal_fraction=0.4):
    # Read the video paths from the input file
    with open(input_file, 'r') as f:
        video_paths = f.readlines()

    # Calculate the number of videos to remove
    num_to_remove = int(len(video_paths) * removal_fraction)

    # Randomly select the paths to remove
    videos_to_remove = random.sample(video_paths, num_to_remove)

    # Write the selected paths to the output file
    with open(output_file, 'w') as f:
        f.writelines(videos_to_remove)

    print(f"Selected {num_to_remove} videos for removal. Paths written to {output_file}.")

if __name__ == "__main__":
    input_file = '/Users/ericsheen/Desktop/DeepAI_Research/Spatial-Scene-Dataset/output/video_paths.txt'  # Replace with your actual file path
    output_file = 'videos_to_remove.txt'  # The file where paths to be removed will be written
    select_videos_for_removal(input_file, output_file)
