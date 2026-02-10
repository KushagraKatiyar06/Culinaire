import os
from openai import OpenAI
from transcript import (getVideoID, fetchTranscript)
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv, find_dotenv

# Pydantic Classes
class Ingredient(BaseModel):
    name: str
    quantity: str
    unit: str

class GroupedStep(BaseModel):
    start_time: float
    end_time: float
    action: str
    detail: str
    tools: List[str]
    currentIngredients: List[str]

class RecipeData(BaseModel):
    title: str
    servings: str
    ingredient: List[Ingredient]
    instructions: List[GroupedStep]
    calories: str 

# Generate Recipes
load_dotenv(find_dotenv())

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("no openai key found.")
    exit(1) 

client = OpenAI(api_key=api_key)

def generateRecipe(url: str):
    videoID = getVideoID(url)
    print(f"Generating recipe for URL: {url}\n")

    if videoID is None:
        return None
    
    snippets = fetchTranscript(videoID)
    normalizedTranscript = "\n".join(
        [f"[{snippet.start:.2f}s - {snippet.start + snippet.duration:.2f}s]: {snippet.text}" for snippet in snippets]
    )

    system_prompt = (
    "You are a helpful culinary assistant. Analyze the transcript provided and: "
    "1. Consolidate info into logical cooking steps with start and end times. "
    "2. For each step, identify the specific 'tools' used (e.g., whisk, frying pan). "
    "3. For each step, identify 'currentIngredients' involved in that specific action. "
    "4. Estimate total calories for the entire recipe. "
    "Do not create separate steps for every sentence; group them by physical action."
    )
    
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": normalizedTranscript},
        ],
        response_format=RecipeData,
    )

    recipe = completion.choices[0].message.parsed
    

    print(f"Recipe Title: {recipe.title}")
    print(f"Servings: {recipe.servings}\n")

    print("Ingredients:")
    for ing in recipe.ingredient:
        print(f"- {ing.quantity} {ing.unit} {ing.name}")

    print("\nInstructions:")
    for step in recipe.instructions:
        print(f"[{step.start_time}s - {step.end_time}s] {step.action}")
        print(f"Tools: {', '.join(step.tools)}")
        print(f"Ingredients here: {', '.join(step.currentIngredients)}")

    print(f"\nCalories: {recipe.calories}")
    
    return recipe

if __name__ == "__main__":
    print("testing recipe.py methods.\n")
    #test_url = "https://www.youtube.com/watch?v=hDjK5C2aoSs"
    #generateRecipe(test_url)