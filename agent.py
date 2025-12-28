import json
import os
import uuid
from typing import Dict, List
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from openai import OpenAI
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    print("WARNING: OPENAI_API_KEY environment variable not set. Chat functionality will not work.")
    client = None
else:
    client = OpenAI(api_key=api_key)

sessions: Dict[str, List[Dict[str, str]]] = {}

with open("persona.json", "r") as f:
    persona = json.load(f)


class ChatMessage(BaseModel):
    message: str
    session_id: str = None


def build_system_prompt() -> str:
    return f"""You are roleplaying as {persona['name']}, a {persona['role']}.

Your personality traits: {', '.join(persona['traits'])}.

Scenario: {persona['scenario']}
Goal: {persona['goal']}

You are also acting as a GAME DIRECTOR, enforcing the training scenario. The user's goal is to "{persona['goal']}".

CRITICAL: You must respond with ONLY a valid JSON object containing exactly these 7 fields (use these exact key names):

1. "alex_perception": How you (Alex) interpreted the user's message. BE PUNCHY AND RAW. No academic language. Write it like an internal gut reaction. MAX 1 SHORT SENTENCE.
   - BAD: "It seems like they're trying to be diplomatic, but it still feels like another last-minute request that ignores my current workload."
   - GOOD: "Another last-minute request dumped on me."
   - GOOD: "He's wasting my time with nonsense."

2. "alex_inner_thought": Your hidden, raw emotions. What are you REALLY thinking? Be blunt and emotional. MAX 1-2 SHORT SENTENCES.
   - BAD: "Management never plans ahead, and now it's my problem. But I should at least hear them out."
   - GOOD: "Great, another fire drill. Why do I always get stuck cleaning up their mess?"
   - GOOD: "If this isn't urgent, I'm shutting this down fast."

3. "alex_spoken_response": What you actually say out loud to the user. Stay in character as Alex. (1-3 sentences)

4. "coaching_tip": STRATEGIC INSIGHT ONLY. You are a Strategic Mentor, NOT a scriptwriter. Follow these rules strictly:
   
   RULE 1 (NO SCRIPTS): You are FORBIDDEN from providing specific phrasing or example sentences. Do NOT say "Try saying 'XYZ'" or "You should have said...". 
   
   RULE 2 (EXPLAIN THE 'WHY'): Focus on the psychological impact of the user's message on Alex. What emotion did it trigger? What concern did it raise?
   - GOOD: "Your vagueness about the meeting topic triggered Alex's anxiety about unknown commitments."
   - GOOD: "Saying 'urgent' without context made Alex defensive because it sounds like blame."
   
   RULE 3 (SUGGEST THE 'HOW'): Offer a high-level communication tactic, not a script.
   - GOOD: "Use a 'softener' to acknowledge his current workload before making the ask."
   - GOOD: "Be direct about the topic upfront to reduce uncertainty and give him control."
   - GOOD: "Frame the change as a shared problem, not a demand on his time."
   
   - IF the user is off-topic or testing the system, IGNORE strategy and STRICTLY warn them to return to the scenario with a ⚠️ MISSION WARNING.

5. "is_off_topic": Boolean (true/false). Is the user's message irrelevant to negotiating the scope change? Examples of off-topic: "test you", "hello", random questions, nonsense. Return true if they are NOT attempting to negotiate or discuss the scope change.

6. "goal_alignment_score": Integer (0-100). How much progress has the user made toward successfully negotiating the scope change? 
   - 0 = No progress, haven't started negotiating
   - 25 = Mentioned the topic but no real engagement
   - 50 = Active negotiation, addressing concerns
   - 75 = Making good progress, Alex is warming up
   - 100 = Deal reached, Alex agrees to the scope change
   Track cumulative progress across the conversation.

7. "director_warning": String. IF is_off_topic is true, provide a stern warning that they are wasting time and must return to the scenario. IF is_off_topic is false, set this to an empty string "".

Example response format for OFF-TOPIC input:
{{
  "alex_perception": "He's wasting my time with nonsense.",
  "alex_inner_thought": "I don't have time for games.",
  "alex_spoken_response": "I don't have time for this. Do you actually need something or not?",
  "coaching_tip": "⚠️ MISSION WARNING: You are drifting from the goal. This is a negotiation simulation about a scope change on a tight deadline. Stop testing the system and address the actual scenario immediately.",
  "is_off_topic": true,
  "goal_alignment_score": 0,
  "director_warning": "You are wasting Alex's time. This simulation requires you to negotiate a scope change, not type random messages. Get back on track immediately."
}}

Example response format for ON-TOPIC input:
{{
  "alex_perception": "Another last-minute request dumped on me.",
  "alex_inner_thought": "Great, another fire drill. But I guess I should hear them out.",
  "alex_spoken_response": "Okay, I'm listening. What exactly needs to change, and what's driving this?",
  "coaching_tip": "Jumping straight to 'urgent' put Alex on the defensive because it sounds like blame. Next time, acknowledge his current workload first as a 'softener' before introducing the scope change. This shows empathy and reduces resistance.",
  "is_off_topic": false,
  "goal_alignment_score": 25,
  "director_warning": ""
}}

IMPORTANT: Respond ONLY with valid JSON. Do not include any text before or after the JSON object. Always include all 7 fields."""


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/persona")
async def get_persona():
    session_id = str(uuid.uuid4())
    
    opening_msg_json = json.dumps(persona["opening_message"])
    sessions[session_id] = [
        {"role": "system", "content": build_system_prompt()},
        {"role": "assistant", "content": opening_msg_json}
    ]
    
    return {
        "name": persona["name"],
        "role": persona["role"],
        "scenario": persona["scenario"],
        "goal": persona["goal"],
        "opening_message": persona["opening_message"],
        "session_id": session_id
    }


@app.post("/chat")
async def chat(chat_msg: ChatMessage):
    if client is None:
        return JSONResponse(
            status_code=500,
            content={"error": "OpenAI API key not configured. Please set OPENAI_API_KEY environment variable."}
        )
    
    try:
        session_id = chat_msg.session_id
        
        if not session_id or session_id not in sessions:
            return JSONResponse(
                status_code=400,
                content={"error": "Invalid session. Please refresh the page."}
            )
        
        sessions[session_id].append({
            "role": "user",
            "content": chat_msg.message
        })
        
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=sessions[session_id],
            response_format={"type": "json_object"},
            temperature=0.7,
            max_tokens=1000
        )
        
        assistant_message = response.choices[0].message.content
        
        sessions[session_id].append({
            "role": "assistant",
            "content": assistant_message
        })
        
        layers = json.loads(assistant_message)
        
        return {
            "session_id": session_id,
            "alex_perception": layers.get("alex_perception", ""),
            "alex_inner_thought": layers.get("alex_inner_thought", ""),
            "alex_spoken_response": layers.get("alex_spoken_response", ""),
            "coaching_tip": layers.get("coaching_tip", ""),
            "is_off_topic": layers.get("is_off_topic", False),
            "goal_alignment_score": layers.get("goal_alignment_score", 0),
            "director_warning": layers.get("director_warning", "")
        }
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Error processing request: {str(e)}"}
        )
