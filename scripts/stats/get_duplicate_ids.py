import json

# Load JSON file
with open('./filtered_data.json', 'r') as file:
    data = json.load(file)

# Dictionary to track occurrences of each ID
id_dict = {}

# List to store indices of duplicates to remove
duplicates_to_remove = []

# Iterate through the data to find duplicates
for index, entry in enumerate(data):
    video_id = entry['video'].split('_')[1].split('-')[0]  # Extract video ID
    if video_id in id_dict:
        # Duplicate found
        print(f"Video ID: {video_id} appears in entries: {id_dict[video_id]} and {index + 1}")
        print(f"  - Entry {id_dict[video_id] + 1}: {data[id_dict[video_id]]['video']}")
        print(f"  - Entry {index + 1}: {entry['video']}")
        duplicates_to_remove.append(index)  # Mark the duplicate for removal
    else:
        id_dict[video_id] = index

# Remove duplicates from the data
for i in sorted(duplicates_to_remove, reverse=True):
    del data[i]

# Save the cleaned JSON
with open('cleaned_data.json', 'w') as file:
    json.dump(data, file, indent=2)

# Output the final length of the cleaned JSON
print(f"Final number of entries in JSON: {len(data)}")
