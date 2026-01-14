from youtube_transcript_api import FetchedTranscriptSnippet, YouTubeTranscriptApi
import requests
import re

'''
class FetchedTranscript:
    snippets: list[FetchedTranscriptSnippet]
    video_id: str
    language: str
    language_code: str
    is_generated: bool
'''

def getVideoID(url: str) -> str | None:
    YOUTUBE_REGEX = r"(?:v=|\/)([0-9A-Za-z_-]{11})"
    if not url:
        print("no url provided.\n")
        return None
    else:
        match = re.search(YOUTUBE_REGEX, url)
        if match:
            print("video ID found:", match.group(1), "\n")
            return match.group(1)
        else:
            return None
        
def getVideoMetadata(videoID: str) -> dict | None:
    url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={videoID}&format=json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print("video metadata fetched.\n")
        return {
            "title": data.get("title", ""),
            "author": data.get("author_name", "")
        }
    
    print("failed to fetch video metadata.\n")
    return {"title": "Unkown", "author": "Unknown"}

def fetchTranscript(videoID: str) -> list[FetchedTranscriptSnippet]:
    ytt_api = YouTubeTranscriptApi()
    transcript = ytt_api.fetch(videoID)

    snippets = transcript.snippets
    video_ID = transcript.video_id

    print(f"found transcript snippets of {video_ID}\n")
    return snippets

def printTranscript(snippets: list[FetchedTranscriptSnippet]) -> None:
    for snippet in snippets:
        dialogue = snippet.text
        start = snippet.start
        duration = snippet.duration
        end = start + duration
        print(f"[{start:.2f} -> {end:.2f}] {dialogue}")

def test_url(url: str) -> None:
    videoID = getVideoID(url)
    if videoID is None:
        print("Invalid YouTube URL")
        return

    snippets = fetchTranscript(videoID)
    videoMetaData = getVideoMetadata(videoID)

    if videoMetaData:
        videoName = videoMetaData["title"]
        videoAuthor = videoMetaData["author"]
    else:
        videoName = "Unknown"
        videoAuthor = "Unknown"
        
    printTranscript(snippets)
    print("Video ID, Title, Author:", f"{videoID}, {videoName}, {videoAuthor}")

if __name__ == "__main__":
    test_url("https://www.youtube.com/watch?v=dQw4w9WgXcQ")





