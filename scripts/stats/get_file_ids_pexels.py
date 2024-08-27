import os

def extract_ids_from_filenames(directory, output_file):
    ids = []
    
    for filename in os.listdir(directory):
        if filename.endswith('.mp4'):  # Ensure it's a video file
            if '-sd' in filename:
                video_id = filename.split('-sd')[0]  # Extract the ID before "-sd"
            elif '-uhd' in filename:
                video_id = filename.split('-uhd')[0]  # Extract the ID before "-uhd"
            else:
                continue  # If neither pattern is found, skip this file
            ids.append(video_id)
    
    with open(output_file, 'w') as f:
        for video_id in ids:
            f.write(video_id + '\n')
    
    print(f"Extracted {len(ids)} IDs and saved to {output_file}")

directory = '/Users/ericsheen/Desktop/DeepAI_Research/SSD'
output_file = '/Users/ericsheen/Desktop/DeepAI_Research/Spatial-Scene-Dataset/download/video_ids.txt'

extract_ids_from_filenames(directory, output_file)
