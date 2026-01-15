from pydantic import BaseModel
from typing import List

class Ingredient(BaseModel):
    name: str
    quantity: str
    unit: str

class GroupedStep(BaseModel):
    start_time: float
    end_time: float
    action: str
    detail: str

class RecipeData(BaseModel):
    title: str
    servings: str
    ingredient: List[Ingredient]
    instructions: List[GroupedStep]

import os
from openai import OpenAI
from transcript import (getVideoID, fetchTranscript)
import dotenv

dotenv.load_dotenv()
client = OpenAI(api_key=os.getenv("OPEN_API_KEY"))

def generateRecipe(url: str):
    videoID = getVideoID(url)

    print("Generating recipe for URL:", url)

    if videoID is None:
        return None
    
    snippets = fetchTranscript(videoID)
    normalizedTranscript = "\n".join(
        [f"[{snippet.start:.2f}s] - {snippet.start + snippet.duration:.2f}s]: {snippet.text}" for snippet in snippets]
    )



if __name__ == "__main__":
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    generateRecipe(test_url)



