import os
import json

def combine_json_files(directory, output_filename):
    combined_data = []
    file_count = 0
    total_json_length = 0

    # Iterate over all files in the directory
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.json'):
                filepath = os.path.join(root, filename)
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    combined_data.extend(data)
                    file_count += 1
                    total_json_length += len(data)

    # Write the combined data to the output file
    with open(output_filename, 'w') as outfile:
        json.dump(combined_data, outfile, indent=2)

    print(f"All JSON files have been combined and saved to {output_filename}.")
    print(f"Number of files processed: {file_count}")
    print(f"Total JSON length: {total_json_length}")

# Set the directory containing your JSON files
json_directory = '/Users/ericsheen/Desktop/DeepAI_Research/Spatial-Scene-Dataset/scripts/json'
output_file = './data.json'

# Combine the JSON files
combine_json_files(json_directory, output_file)