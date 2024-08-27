import json

# Load the JSON data
with open('./cleaned_data.json', 'r') as file:
    data = json.load(file)

# Iterate through each entry in the JSON data
for entry in data:
    # Extract the digits between the underscores and hyphens
    video_name = entry['video'].split('_')[1].split('-')[0]
    # Rename the video entry
    entry['video'] = video_name + '.mp4'

# Save the updated JSON data
with open('data_updated.json', 'w') as file:
    json.dump(data, file, indent=2)

# Output the length of the JSON file (number of entries)
print(f"Video names updated successfully. Total number of entries: {len(data)}")
