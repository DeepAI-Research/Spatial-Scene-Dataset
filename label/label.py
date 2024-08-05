"""
Install the Google AI Python SDK

$ pip install google-generativeai

See the getting started guide for more information:
https://ai.google.dev/gemini-api/docs/get-started/python
"""

import os
import time
import json
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Configure your API key
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def upload_to_gemini(path, mime_type=None):
    """Uploads the given file to Gemini.

    See https://ai.google.dev/gemini-api/docs/prompting_with_media
    """
    file = genai.upload_file(path, mime_type=mime_type)
    print(f"Uploaded file '{file.display_name}' as: {file.uri}")
    return file

def wait_for_files_active(files):
    """Waits for the given files to be active.

    Some files uploaded to the Gemini API need to be processed before they can be
    used as prompt inputs. The status can be seen by querying the file's "state"
    field.

    This implementation uses a simple blocking polling loop. Production code
    should probably employ a more sophisticated approach.
    """
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

# Create the model
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
    # safety_settings = Adjust safety settings
    # See https://ai.google.dev/gemini-api/docs/safety-settings
)

def generate_caption(video_path, prompt_text):
    # Upload your local video to Gemini
    video_file = upload_to_gemini(video_path, mime_type="video/mp4")

    # Wait for the video to be processed and ready
    wait_for_files_active([video_file])

    # Start a chat session
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    video_file,
                ],
            },
            {
                "role": "user",
                "parts": [
                    prompt_text,
                ],
            }
        ]
    )

    # Send a message with your input prompt to generate captions
    response = chat_session.send_message("Please analyze the video and provide the necessary information.")

    return response.text

# Define your prompt
prompt = """
Analyze this video sequence and describe:
1. The main objects present
2. Their relative positions (e.g., left, right, above, below)
3. Any movements or changes in position of these objects
Focus only on the objects, their positions, and movements. 
Do not describe camera movements or general scene descriptions.
Provide a concise summary.
"""

# Example usage with local video paths
video_paths = ["./videos/0.mp4", "./videos/1.mp4"]  # Add your video paths here

video_captions = []
for video_path in video_paths:
    caption = generate_caption(video_path, prompt)
    video_captions.append({"video": video_path, "caption": caption})

# Save the generated captions to a JSON file
with open('./output/gemini_video_captions.json', 'w') as f:
    json.dump(video_captions, f, indent=2)

print("Captions generated and saved to gemini_video_captions.json")
