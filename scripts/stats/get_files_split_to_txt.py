import os

def get_video_paths(directory):
    video_paths = []
    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
                video_paths.append(os.path.join(root, filename))
    return video_paths

def split_paths(paths):
    half = len(paths) // 2
    return paths[:half], paths[half:]

def write_paths_to_files(paths1, paths2, file1, file2):
    with open(file1, 'w') as f1, open(file2, 'w') as f2:
        f1.write('\n'.join(paths1))
        f2.write('\n'.join(paths2))

if __name__ == "__main__":
    directory = "/Users/ericsheen/Desktop/DeepAI_Research/SSD_Cut"
    file1 = "/Users/ericsheen/Desktop/DeepAI_Research/Spatial-Scene-Dataset/label/video_paths_part1.txt"
    file2 = "/Users/ericsheen/Desktop/DeepAI_Research/Spatial-Scene-Dataset/label/video_paths_part2.txt"

    video_paths = get_video_paths(os.path.expanduser(directory))
    paths_part1, paths_part2 = split_paths(video_paths)
    write_paths_to_files(paths_part1, paths_part2, file1, file2)
