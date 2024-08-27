# import os
# import subprocess
# import ffmpeg

# def get_video_dimensions(file_path):
#     """Get the dimensions of the video using ffprobe."""
#     try:
#         result = subprocess.run(
#             [
#                 'ffprobe',
#                 '-v', 'error',
#                 '-select_streams', 'v:0',
#                 '-show_entries', 'stream=width,height',
#                 '-of', 'default=noprint_wrappers=1:nokey=1',
#                 file_path
#             ],
#             stdout=subprocess.PIPE,
#             stderr=subprocess.PIPE,
#             check=True
#         )
#         width, height = map(int, result.stdout.decode().strip().split('\n'))
#         return width, height
#     except subprocess.CalledProcessError as e:
#         print(f"Error getting video dimensions: {e.stderr.decode()}")
#         return None, None

# def resize_video(input_file, output_file, target_width, target_height):
#     # Ensure the output directory exists
#     output_dir = os.path.dirname(output_file)
#     if not os.path.exists(output_dir):
#         os.makedirs(output_dir)
#         print(f"Created directory: {output_dir}")

#     try:
#         # Get the input video's dimensions
#         original_width, original_height = get_video_dimensions(input_file)
#         if original_width is None or original_height is None:
#             return

#         # Calculate the new dimensions while maintaining aspect ratio
#         aspect_ratio = original_width / original_height
        
#         if target_width / aspect_ratio <= target_height:
#             new_width = target_width
#             new_height = int(target_width / aspect_ratio)
#         else:
#             new_width = int(target_height * aspect_ratio)
#             new_height = target_height

#         # Ensure dimensions are divisible by 2
#         new_width = new_width - (new_width % 2)
#         new_height = new_height - (new_height % 2)
        
#         print(f"Resizing to: {new_width}x{new_height}")

#         (
#             ffmpeg
#             .input(input_file)
#             .filter('scale', new_width, new_height)
#             .output(output_file)
#             .run()
#         )
#         print(f"Video resized successfully: {output_file}")
#     except ffmpeg.Error as e:
#         error_message = e.stderr.decode() if e.stderr else "Unknown error occurred"
#         print(f"Error resizing video: {error_message}")

# if __name__ == "__main__":
#     input_video = "/Users/ericsheen/Desktop/DeepAI_Research/Spatial-Scene-Dataset/output/3683300-uhd_3840_2160_24fps.mp4"
#     output_video = "/Users/ericsheen/Desktop/DeepAI_Research/Spatial-Scene-Dataset/output/video_resized.mp4"
#     target_width = 720
#     target_height = 480

#     resize_video(input_video, output_video, target_width, target_height)


import os
import subprocess
import ffmpeg

def get_video_dimensions(file_path):
    """Get the dimensions of the video using ffprobe."""
    try:
        result = subprocess.run(
            [
                'ffprobe',
                '-v', 'error',
                '-select_streams', 'v:0',
                '-show_entries', 'stream=width,height',
                '-of', 'default=noprint_wrappers=1:nokey=1',
                file_path
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
        width, height = map(int, result.stdout.decode().strip().split('\n'))
        return width, height
    except subprocess.CalledProcessError as e:
        print(f"Error getting video dimensions: {e.stderr.decode()}")
        return None, None

def resize_video(input_file, output_file, target_width, target_height):
    """Resize the video to the target dimensions."""
    try:
        # Get the input video's dimensions
        original_width, original_height = get_video_dimensions(input_file)
        if original_width is None or original_height is None:
            return

        # Calculate the new dimensions while maintaining aspect ratio
        aspect_ratio = original_width / original_height
        
        if target_width / aspect_ratio <= target_height:
            new_width = target_width
            new_height = int(target_width / aspect_ratio)
        else:
            new_width = int(target_height * aspect_ratio)
            new_height = target_height

        # Ensure dimensions are divisible by 2
        new_width = new_width - (new_width % 2)
        new_height = new_height - (new_height % 2)
        
        print(f"Resizing to: {new_width}x{new_height}")

        (
            ffmpeg
            .input(input_file)
            .filter('scale', new_width, new_height)
            .output(output_file)
            .run()
        )
        print(f"Video resized successfully: {output_file}")

        # Delete the original file after successful resizing
        if os.path.exists(output_file):
            os.remove(input_file)
            print(f"Original video deleted: {input_file}")
        else:
            print(f"Failed to create resized video, original video not deleted: {output_file}")
    except ffmpeg.Error as e:
        error_message = e.stderr.decode() if e.stderr else "Unknown error occurred"
        print(f"Error resizing video: {error_message}")

def process_videos(input_dir, output_dir, target_width, target_height):
    """Process all videos in the input directory."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}")

    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith(('.mp4')):  # Add more formats if needed
                input_file = os.path.join(root, file)
                output_file = os.path.join(output_dir, file)
                resize_video(input_file, output_file, target_width, target_height)

if __name__ == "__main__":
    input_video_dir = "/Users/ericsheen/Desktop/DeepAI_Research/SSD_preprocessed"
    output_video_dir = "/Users/ericsheen/Desktop/DeepAI_Research/SSD_resized"
    target_width = 720
    target_height = 480

    process_videos(input_video_dir, output_video_dir, target_width, target_height)
