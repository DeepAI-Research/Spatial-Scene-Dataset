import os
import time
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def generate_gemini(model, template, prompt):
    content = template + prompt

    max_retries = 3
    step = 30
    delay = 30

    for attempt in range(max_retries):
        try:
            chat_session = model.start_chat(history=[])
            response = chat_session.send_message(content)
            captions_content = response.text.strip()
            return captions_content
        except Exception as e:
            print(f"Error on attempt {attempt + 1}: {str(e)}")
            if attempt < max_retries - 1:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
                delay += step  # Exponential backoff
            else:
                print("Max retries reached. Returning None.")
                return None

    return None

def parse_gemini_json(raw_output):
    try:
        if "```json" in raw_output:
            json_start = raw_output.index("```json") + 7
            json_end = raw_output.rindex("```")
            json_content = raw_output[json_start:json_end].strip()
        else:
            json_content = raw_output.strip()

        json_content = json_content.strip(',')

        if json_content.strip().startswith('"') and ':' in json_content:
            json_content = "{" + json_content + "}"

        parsed_json = json.loads(json_content)
        
        return parsed_json
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {str(e)}")
        return None

def upload_to_gemini(path, mime_type=None):
    file = genai.upload_file(path, mime_type=mime_type)
    print(f"Uploaded file '{file.display_name}' as: {file.uri}")
    return file

def wait_for_files_active(files):
    print("Waiting for file processing...")
    for name in (file.name for file in files):
        file = genai.get_file(name)
        while file.state.name == "PROCESSING":
            print(".", end="", flush=True)
            time.sleep(10)
            file = genai.get_file(name)
        if file.state.name != "ACTIVE":
            raise Exception(f"File {file.name} failed to process")
    print("...all files ready")
    print()

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

def process_videos(video_paths, prompt, batch_size=5):
    processed_videos = {}
    batch_counter = 0

    if os.path.exists('./output/processed_videos.txt'):
        with open('./output/processed_videos.txt', 'r') as f:
            lines = f.readlines()
            for line in lines:
                video, status = line.strip().split(' - ')
                processed_videos[video] = status
        batch_counter = len(lines) // batch_size

    unprocessed_videos = []

    for i in range(0, len(video_paths), batch_size):
        batch = video_paths[i:i+batch_size]
        batch_counter += 1
        print(f"Processing batch {batch_counter}...")

        # Upload batch of videos
        files = [upload_to_gemini(video, mime_type="video/mp4") for video in batch]
        wait_for_files_active(files)

        # Start a new chat session for this batch
        chat_session = model.start_chat(history=[])

        for file in files:
            chat_session.history.append({
                "role": "user",
                "parts": [
                    file,
                ],
            })

        try:
            # Send the prompt for this batch
            caption = chat_session.send_message(prompt)
            caption = caption.text.strip()

            print(caption)

            # Split the captions by line breaks or a specified delimiter
            caption_list = caption.split("\n\n")

            # Generate captions for each video in the batch
            output_data = []
            for video_path, caption_text in zip(batch, caption_list):
                if caption_text:
                    processed_videos[video_path] = "COMPLETED"
                    # Save the generated captions to the list
                    output_data.append({"video": video_path, "caption": caption_text.strip()})

                    # Update processed_videos.txt
                    with open('./output/processed_videos.txt', 'a') as f:
                        f.write(f"{video_path} - COMPLETED\n")

            # Write the batch data to the JSON file
            with open(f'./output/gemini_video_captions_batch_{batch_counter}.json', 'w') as f:
                json.dump(output_data, f, indent=2)

        except Exception as e:
            print(f"Error processing batch {batch_counter}: {str(e)}")
            # Log the unprocessed videos in a separate file
            with open('./output/unprocessed_videos.txt', 'a') as f:
                for video_path in batch:
                    f.write(f"{video_path}\n")
            print(f"Logged unprocessed videos to './output/unprocessed_videos.txt'")
            continue  # Continue with the next batch

        # Clear the chat history for the next batch
        chat_session.history.clear()

        print(f"Batch {batch_counter} processing complete.\n")

prompt = """
Analyze each of the 5 videos and provide a detailed description from a third-person perspective. For each video, include:

Scene identification: Describe the overall setting and context of the video (e.g., indoor/outdoor, time of day, weather conditions, type of environment).
Main objects and subjects: Identify and list the primary objects, people, or animals present in the scene. The main focus should be spatial relationships of objects and relative to each other.

Caption must have: 

Spatial relationships:
a. Describe the relative positions of objects (e.g., left, right, above, below, behind, infront, etc). Don't have to use these exact just an example.
b. Estimate distances between objects when relevant (doesn't have to be accurate but give a sense of scale).
c. Note any depth or perspective cues in the scene.
Object attributes:
a. Describe colors, sizes, shapes, and textures of key objects.
b. Mention any notable features or characteristics.
Actions and movements:
a. Detail any movements or changes in position of objects or subjects (moving right, left, up, down, towards me, further away). Don't have to use these exact just an example.
b. Describe the direction, speed, and nature of movements.
c. Note any interactions between objects or subjects.
Temporal changes:
a. Describe how the scene evolves over time.
b. Note any significant changes in lighting, object positions, or overall composition.
Spatial composition:
a. Describe how objects are arranged within the frame.
b. Note any patterns, symmetry, or intentional groupings.
Lighting and atmosphere:
a. Describe the lighting conditions and their effect on the scene.
b. Note any shadows, reflections, or other lighting-related details that affect spatial perception.
Scale and proportion:
a. Describe the relative sizes of objects in the scene.
b. Note any objects that appear unusually large or small in context.
Occlusions and partial visibility:
a. Mention any objects that are partially hidden or obscured by others.
b. Describe how this affects the spatial understanding of the scene.
Camear movement:
a. Describe any camera movements or changes in perspective. Different camera angles or zoom levels like zoomed in or orbiting around an object.
b. Note how these movements affect the spatial relationships between objects.

Guidelines:

- Provide a cohesive, flowing description incorporating these elements.
- Focus primarily on spatial information and relationships between objects.
- Describe the scene as if observing it happen, not as if you are in it or watching a video. 
- Be accurate in describing where things are in the scene and how they move relative to each other.
- Describe depth as much as possible relative to you! (e.g. "the person is closer to me than the tree" or "the tree is further away than the car" or "tree infront  of the car")
- Describe the positions and movements RELATIVE TO YOU. Even if a person for example is biking "foward" but in your perspect is moving left relative to you, you should say moving left)
- DO NOT use FPV language and phrases like "we see" or "the viewer can observe." or "I see" DO NOT MENITON THE CAMERA OR SCREEN OR THE FRAME. Describe relative to you but not in a FPV way.
- Don't describe what you think will happen, only describe what is happening
- Each video description should be a single, detailed paragraph without line breaks or bullet points.
- Separate each video's caption with a single new line, without any additional formatting.
- Aim for rich, vivid descriptions that capture the essence of the scene's spatial composition and dynamics.
- Do not mention the camera, video, frame, or screen explicitly. Nor should the relationships of the objects be described in such a way

After writing each description, review it to ensure adherence to these guidelines and Caption must have and focus on spatial information.
Each caption for each video should be separated by a new line and nothing more (no dashes or anything else).
"""

def get_video_paths_from_dir(directory):
    video_paths = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith((".mp4", ".mov", ".avi", ".mkv")):  # Add more extensions if needed
                video_paths.append(os.path.join(root, file))
    return video_paths

video_dir = "/Users/ericsheen/Desktop/DeepAI_Research/SpatialSceneDataset"  # Replace with your directory
video_paths = get_video_paths_from_dir(video_dir)

process_videos(video_paths, prompt)
