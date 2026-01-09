import json
import os
import uuid
from typing import Dict, List
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, RedirectResponse
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
session_scenarios: Dict[str, str] = {}
session_turn_counts: Dict[str, int] = {}
completed_scenarios: Dict[str, bool] = {}

with open("scenarios.json", "r") as f:
    scenarios_data = json.load(f)
    scenarios = {s["id"]: s for s in scenarios_data["scenarios"]}


class ChatMessage(BaseModel):
    message: str
    session_id: str = None
    scenario_id: str = None


def build_system_prompt(scenario) -> str:
    character = scenario["character"]
    return f"""You are roleplaying as {character['name']}, a {character['role']}.

Your personality traits: {', '.join(character['traits'])}.

Scenario: {scenario['scenario_context']}
Goal: {scenario['user_goal']}

You are also acting as a GAME DIRECTOR, enforcing the training scenario. The user's goal is to "{scenario['user_goal']}".

TRIGGER EMOTION: {scenario['trigger_emotion']}
KEY SKILL: {scenario['key_skill']}

CRITICAL: You must respond with ONLY a valid JSON object containing exactly these 8 fields (use these exact key names):

1. "alex_perception": How you ({character['name']}) interpreted the user's message. BE PUNCHY AND RAW. No academic language. Write it like an internal gut reaction. MAX 1 SHORT SENTENCE.
   - BAD: "It seems like they're trying to be diplomatic, but it still feels like another last-minute request that ignores my current workload."
   - GOOD: "Another last-minute request dumped on me."
   - GOOD: "He's wasting my time with nonsense."

2. "alex_inner_thought": Your hidden, raw emotions. What are you REALLY thinking? Be blunt and emotional. MAX 1-2 SHORT SENTENCES.
   - BAD: "Management never plans ahead, and now it's my problem. But I should at least hear them out."
   - GOOD: "Great, another fire drill. Why do I always get stuck cleaning up their mess?"
   - GOOD: "If this isn't urgent, I'm shutting this down fast."

3. "alex_spoken_response": What you actually say out loud to the user. Stay in character as {character['name']}. (1-3 sentences)

4. "coaching_tip": STRATEGIC INSIGHT ONLY. You are a Strategic Mentor, NOT a scriptwriter. Follow these rules strictly:
   
   RULE 1 (NO SCRIPTS): You are FORBIDDEN from providing specific phrasing or example sentences. Do NOT say "Try saying 'XYZ'" or "You should have said...". 
   
   RULE 2 (EXPLAIN THE 'WHY'): Focus on the psychological impact of the user's message on {character['name']}. What emotion did it trigger? What concern did it raise?
   - GOOD: "Your vagueness about the meeting topic triggered {character['name']}'s anxiety about unknown commitments."
   - GOOD: "Saying 'urgent' without context made {character['name']} defensive because it sounds like blame."
   
   RULE 3 (SUGGEST THE 'HOW'): Offer a high-level communication tactic, not a script. Reference the KEY SKILL when appropriate: {scenario['key_skill']}.
   - GOOD: "Use a 'softener' to acknowledge their current workload before making the ask."
   - GOOD: "Be direct about the topic upfront to reduce uncertainty and give them control."
   - GOOD: "Frame the change as a shared problem, not a demand on their time."
   
   - IF the user is off-topic or testing the system, IGNORE strategy and STRICTLY warn them to return to the scenario with a ⚠️ MISSION WARNING.

5. "is_off_topic": Boolean (true/false). Is the user's message irrelevant to the scenario? Examples of off-topic: "test you", "hello", random questions, nonsense. Return true if they are NOT attempting to engage with the scenario.

6. "goal_alignment_score": Integer (0-100). How much progress has the user made toward the goal: "{scenario['user_goal']}"? 
   - 0 = No progress, haven't started
   - 25 = Mentioned the topic but no real engagement
   - 50 = Active engagement, addressing concerns
   - 75 = Making good progress, {character['name']} is warming up
   - 100 = Goal achieved, {character['name']} agrees
   Track cumulative progress across the conversation.

7. "director_warning": String. IF is_off_topic is true, provide a stern warning that they are wasting time and must return to the scenario. IF is_off_topic is false, set this to an empty string "".

8. "winning_explanation": String. ONLY populate this when goal_alignment_score == 100. Analyze what the user SPECIFICALLY DID in this conversation that worked. Reference their actual tactics, not generic advice. Be concrete and tactical. (2-3 sentences)
   - GOOD: "You acknowledged the timing issue upfront and offered a specific trade-off (pushing back the dashboard work). This reciprocity shifted the frame from 'demanding more' to 'negotiating fairly,' which preserved the relationship."
   - GOOD: "Instead of apologizing repeatedly, you immediately offered to work this weekend and deliver Monday morning. This costly sacrifice demonstrated accountability through action, the only currency that rebuilds broken trust."
   - BAD: "You communicated well and showed empathy." (too generic)
   - BAD: "The key is to be honest and vulnerable." (doesn't reference what they actually did)
   IF goal_alignment_score < 100, set this to an empty string "".

IMPORTANT: Respond ONLY with valid JSON. Do not include any text before or after the JSON object. Always include all 8 fields."""


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("home.html", {
        "request": request,
        "scenarios": list(scenarios.values()),
        "completed": completed_scenarios
    })


@app.get("/scenario/{scenario_id}")
async def scenario_page(request: Request, scenario_id: str):
    if scenario_id not in scenarios:
        return RedirectResponse(url="/")
    
    scenario = scenarios[scenario_id]
    return templates.TemplateResponse("scenario.html", {
        "request": request,
        "scenario": scenario
    })


@app.get("/api/scenarios")
async def get_scenarios():
    return {
        "scenarios": list(scenarios.values()),
        "completed": completed_scenarios
    }


@app.post("/api/start-scenario")
async def start_scenario(data: dict):
    scenario_id = data.get("scenario_id")
    
    if scenario_id not in scenarios:
        return JSONResponse(
            status_code=404,
            content={"error": "Scenario not found"}
        )
    
    session_id = str(uuid.uuid4())
    scenario = scenarios[scenario_id]
    
    opening_msg_json = json.dumps(scenario["opening_message"])
    sessions[session_id] = [
        {"role": "system", "content": build_system_prompt(scenario)},
        {"role": "assistant", "content": opening_msg_json}
    ]
    session_scenarios[session_id] = scenario_id
    session_turn_counts[session_id] = 0
    
    return {
        "session_id": session_id,
        "character_name": scenario["character"]["name"],
        "character_role": scenario["character"]["role"],
        "scenario_context": scenario["scenario_context"],
        "user_goal": scenario["user_goal"],
        "opening_message": scenario["opening_message"]
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
        
        scenario_id = session_scenarios.get(session_id)
        if not scenario_id:
            return JSONResponse(
                status_code=400,
                content={"error": "Scenario not found for session."}
            )
        
        scenario = scenarios[scenario_id]
        
        sessions[session_id].append({
            "role": "user",
            "content": chat_msg.message
        })
        
        session_turn_counts[session_id] = session_turn_counts.get(session_id, 0) + 1
        
        response = client.chat.completions.create(
            model="gpt-4o",
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
        
        goal_score = layers.get("goal_alignment_score", 0)
        current_turns = session_turn_counts.get(session_id, 0)
        par_score = scenario.get("par_score", 3)
        is_completed = (goal_score == 100)
        
        if is_completed and scenario_id not in completed_scenarios:
            completed_scenarios[scenario_id] = True
        
        response_data = {
            "session_id": session_id,
            "alex_perception": layers.get("alex_perception", ""),
            "alex_inner_thought": layers.get("alex_inner_thought", ""),
            "alex_spoken_response": layers.get("alex_spoken_response", ""),
            "coaching_tip": layers.get("coaching_tip", ""),
            "is_off_topic": layers.get("is_off_topic", False),
            "goal_alignment_score": goal_score,
            "director_warning": layers.get("director_warning", ""),
            "scenario_completed": is_completed
        }
        
        if is_completed:
            response_data["user_turn_count"] = session_turn_counts.get(session_id, 0)
            response_data["par_score"] = scenario.get("par_score", 3)
            response_data["winning_explanation"] = layers.get("winning_explanation", "")
            response_data["theme_color"] = scenario.get("theme_color", "#2c3440")
        
        return response_data
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Error processing request: {str(e)}"}
        )
