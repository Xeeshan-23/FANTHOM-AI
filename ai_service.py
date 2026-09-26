import json
from google import genai
from google.genai import types
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()
client = genai.Client()

# Shared Component
class ActionItem(BaseModel):
    task: str
    assignee: str
    completed: bool

# --- TEMPLATE SCHEMAS ---
class DefaultTemplate(BaseModel):
    executive_summary: str
    key_decisions: list[str]
    action_items: list[ActionItem]

class SalesTemplate(BaseModel):
    deal_summary: str
    customer_objections: list[str]
    budget_discussed: str
    next_steps: list[ActionItem]

class StandupTemplate(BaseModel):
    progress_updates: list[str]
    blockers: list[str]
    action_items: list[ActionItem]

# --- AI ROUTING ---
def generate_meeting_intelligence(transcript: str, template_type: str = "default") -> dict:
    # 1. Select the correct Pydantic schema and adjust the prompt focus
    if template_type == "sales":
        schema = SalesTemplate
        prompt_focus = "Focus on the sales deal, budget, and any customer objections."
    elif template_type == "standup":
        schema = StandupTemplate
        prompt_focus = "Focus on team progress, blockers, and immediate action items."
    else:
        schema = DefaultTemplate
        prompt_focus = "Focus on a general executive summary and key decisions."

    prompt = (
        f"You are an AI meeting assistant. Analyze the following transcript.\n"
        f"{prompt_focus}\n\n"
        f"Transcript:\n{transcript}"
    )
    
    # 2. Pass the dynamic schema to Gemini
    # 2. Pass the dynamic schema to Gemini
    response = client.models.generate_content(
        model="gemini-3.6-flash", # Updated to the available Flash model
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=schema, 
            temperature=0.4, 
            automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
        ),
    )
    
    try:
        return json.loads(response.text)
    except Exception as e:
        print(f"Failed to parse Gemini response: {e}")
        raise ValueError("Invalid JSON returned by Gemini")