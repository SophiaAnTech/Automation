!pip install youtube-transcript-api

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import re

# the YouTube video URL
VIDEO_URL = "https://www.youtube.com/watch?v=_mN9NUD2mGw"


# Extract video ID from the URL
video_id = VIDEO_URL.split("v=")[1]

# Fetch the transcript
ytt = YouTubeTranscriptApi()
transcript = ytt.fetch(video_id)

# Format transcript as plain text
formatter = TextFormatter()
formatted_text = formatter.format_transcript(transcript)
formatted_text = formatted_text.replace("\n", " ")

# put each sentence on a line
formatted_text = re.sub(r'(?<=[.!?]) ', '\n\n', formatted_text)

# Save to a text file
output_file = "youtube transcript_" + video_id + ".txt"

with open(output_file, "w", encoding="utf-8") as f:
    f.write(formatted_text)

print("Transcript saved to " + output_file)
