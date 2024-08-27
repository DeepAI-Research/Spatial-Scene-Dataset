import json

# Paths to your input files
json_file = './data.json'  # Replace with the path to your shorter JSON file
txt_file = '/Users/ericsheen/Desktop/DeepAI_Research/Spatial-Scene-Dataset/scripts/video_ids.txt'  # Replace with the path to your txt file containing valid IDs

# Output file
filtered_json_file = './filtered_data.json'

# Function to read video IDs from a txt file
def read_ids_from_file(file_path):
    with open(file_path, 'r') as f:
        return set(f.read().splitlines())

# Read the IDs from the txt file
valid_ids = read_ids_from_file(txt_file)

# Load the JSON data
with open(json_file, 'r') as f:
    data = json.load(f)

# Output the original length of the JSON file
original_json_length = len(data)
print(f"Original JSON length: {original_json_length}")

# Filter out the entries in the JSON file that do not have valid IDs
filtered_data = [entry for entry in data if entry['video'].split('_')[1].split('-')[0] in valid_ids]

# Write the filtered JSON data to a new file
with open(filtered_json_file, 'w') as f:
    json.dump(filtered_data, f, indent=2)

# Output the length of the filtered JSON data
filtered_json_length = len(filtered_data)
print(f"Filtered JSON length: {filtered_json_length}")
