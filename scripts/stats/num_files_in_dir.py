import os

def num_files_in_dir(directory):
    count = 0
    for root, _, files in os.walk(directory):
        for file in files:
            count += 1
    return count

if __name__ == "__main__":
    directory = "/Users/ericsheen/Desktop/DeepAI_Research/SSD"
    print(f"Number of files in directory: {num_files_in_dir(directory)}")