import os

def list_all_subfolders(directory, output_file):
    with open(output_file, 'w') as file:
        for root, dirs, _ in os.walk(directory):
            # Get the relative path from the root directory
            rel_path = os.path.relpath(root, directory)
            indent_level = rel_path.count(os.sep)
            # Print each directory at the correct indentation level
            for dir in dirs:
                file.write(f"{'    ' * indent_level}{dir}\n")

# Replace 'your_directory_path' and 'output_file.txt' with your target directory path and desired output file name
list_all_subfolders('/Users/ericsheen/Desktop/DeepAI_Research/SSD/', 'all_subfolders_list.txt')
