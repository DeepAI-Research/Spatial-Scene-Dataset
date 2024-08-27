import cv2
import os

def get_video_resolution_and_size(video_path):
    # Check if the file exists
    if not os.path.isfile(video_path):
        return "File not found."

    # Get file size in bytes and convert it to a human-readable format
    file_size = os.path.getsize(video_path)
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if file_size < 1024:
            break
        file_size /= 1024
    size = f"{file_size:.2f} {unit}"

    # Capture video
    video = cv2.VideoCapture(video_path)

    # Check if the video can be opened
    if not video.isOpened():
        return "Error opening video file."

    # Get video resolution
    width = video.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = video.get(cv2.CAP_PROP_FRAME_HEIGHT)

    # Release the video capture object
    video.release()

    # Return video resolution and file size
    return f"{int(width)}x{int(height)}", size
