import os
import json
from google import genai
from dotenv import load_dotenv

# 1. Load the hidden variables from the .env file
load_dotenv()

# 2. Grab the key and initialize the Client
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("API key not found. Please check your .env file.")

client = genai.Client(api_key=api_key)

# 3. Analyze single task complexity
async def analyze_task_complexity(task_name: str, description: str) -> str:
    prompt = f"Analyze cognitive load for task '{task_name}': {description}. Provide a 2-sentence summary."
    
    response = client.models.generate_content(
        model='gemini-3.6-flash', 
        contents=prompt
    )
    return response.text

# 4. Multi-table user synthesis
async def synthesize_user_data(tasks_data: str, checkins_data: str) -> dict:
    prompt = f"""
    You are an expert analytical engine. Analyze the relationship between this user's task load and physiological metrics.
    
    Tasks: {tasks_data}
    Check-ins: {checkins_data}
    
    You MUST return the response as a valid JSON object with exactly these keys:
    - "overall_cognitive_load": (string, e.g., "High", "Moderate", "Low")
    - "productivity_impact": (1-2 sentences analyzing how sleep/energy affected task completion)
    - "actionable_recommendation": (1 sentence of specific advice)
    
    Do not include markdown formatting, backticks, or the word 'json'. Return ONLY the raw JSON string.
    """
    
    response = client.models.generate_content(
        model='gemini-3.6-flash',
        contents=prompt
    )

    # Parse the string returned into a native Python dictionary
    try:
        # Clean any accidental formatting backticks before loading
        clean_text = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(clean_text)
    except json.JSONDecodeError:
        return {"error": "AI failed to return valid JSON", "raw_response": response.text}