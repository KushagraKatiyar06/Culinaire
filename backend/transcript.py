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
        print("no url provided.")
        return None
    else:
        match = re.search(YOUTUBE_REGEX, url)
        if match:
            print("video ID found:", match.group(1))
            return match.group(1)
        else:
            return None
        
def getVideoMetadata(videoID: str) -> dict | None:
    url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={videoID}&format=json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print("video metadata fetched.")
        return {
            "title": data.get("title", ""),
            "author": data.get("author_name", "")
        }
    
    print("failed to fetch video metadata.")
    return {"title": "Unkown", "author": "Unknown"}

def fetchTranscript(videoID: str) -> list[FetchedTranscriptSnippet]:
    try:
        ytt_api = YouTubeTranscriptApi()
        transcript = ytt_api.fetch(videoID)
        snippets = transcript.snippets
        
        if not snippets:
            print(f"Warning: Transcript for {videoID} is empty.")
            return []
            
        print(f"found transcript snippets of {videoID}")
        return snippets

    except Exception as e:
        print(f"could not fetch transcript for {videoID}")
        return []
    
def isValidTranscript(snippets: list) -> bool:
    total_text = " ".join([snippet.text for snippet in snippets])
    if len(total_text) < 100:
        print("transcript invalid.")
        return False
    
    clean_text = re.sub(r'\[.*?\]|\(.*?\)', '', total_text).strip()
    if len(clean_text) < 50: 
        print("transcript invalid.")
        return False

    print("transcript valid.")
    return True

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
        
    if isValidTranscript(snippets) is False:
        print("Video ID, Title, Author:", f"{videoID}, {videoName}, {videoAuthor}")
        return
    else:
        printTranscript(snippets)
        print("Video ID, Title, Author:", f"{videoID}, {videoName}, {videoAuthor}")
       

if __name__ == "__main__":
    print("testing trasncript.py methods.\n")
    # desktop
    
        # desktop link video
    # test_url("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        # desktop short link video
    # test_url("https://www.youtube.com/shorts/-veIcB4yxUA")

    #mobile 
        # mobile link video
        # mobile short video
    # test_url("https://youtube.com/shorts/bOUvLPmTWSw?si=qBb3pum-MJo5WtsN")

    # testing dialogue-less videos
    test_url("https://youtube.com/shorts/RDJto3R5IbE?si=wT1V1E2Ofd2Nv_T1")

