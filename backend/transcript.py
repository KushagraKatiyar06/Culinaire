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
        return None
    else:
        match = re.search(YOUTUBE_REGEX, url)
        if match:
            return match.group(1)
        else:
            return None
        
def getVideoTItle(videoID: str) -> str | None:
    url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={videoID}&format=json"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("title")
    return None
        
def getVideoAuthor(videoID: str) -> str | None:
    url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={videoID}&format=json"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("author_name")
    return None

def fetchTranscript(videoID: str) -> list[FetchedTranscriptSnippet]:
    ytt_api = YouTubeTranscriptApi()
    transcript = ytt_api.fetch(videoID)

    snippets = transcript.snippets
    video_ID = transcript.video_id

    print(f"transcript snippets of {video_ID}")
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
    videoName = getVideoTItle(videoID)
    videoAuthor = getVideoAuthor(videoID)

    printTranscript(snippets)
    print("Video ID, Title, Author:", f"{videoID}, {videoName}, {videoAuthor}")

if __name__ == "__main__":
    test_url("https://www.youtube.com/watch?v=dQw4w9WgXcQ")





