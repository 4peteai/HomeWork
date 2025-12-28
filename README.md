# Difficult Conversations: AI-Powered Negotiation Training

An agentic negotiation simulator designed to train professionals in difficult conversations with a defensive, stressed Senior Engineer named Alex. Built with a premium **Gemini 3-inspired dark mode interface** and powered by a 4-layer cognitive reasoning system.

## 🚀 Key Features

Unlike standard chatbots, this agent implements a **4-Layer Reasoning Loop** with distinct layers of cognition for every conversational turn:

### 1. **Perception Layer**
The agent first "hears" the user's input through a biased, emotional filter. For example:
- User says: "Can we talk?"
- Alex perceives: "Another vague meeting request wasting my time."

This models real-world communication breakdowns where intent ≠ interpretation.

### 2. **Inner Monologue**
Alex generates hidden thoughts that drive the spoken response. These are raw, unfiltered emotions:
- "Great, another fire drill. Why do I always get stuck cleaning up their mess?"

This layer reveals the psychological state influencing Alex's behavior, teaching users about emotional triggers.

### 3. **Spoken Response**
What Alex actually says out loud, staying in character as a stressed, defensive engineer.

### 4. **Strategic Insight (The Coach)**
A meta-layer that analyzes the conversation from a neutral perspective. The coach:
- **Explains the 'Why'**: "Your vagueness triggered Alex's anxiety about unknown commitments."
- **Suggests the 'How'**: "Use a 'softener' to acknowledge his workload before making the ask."
- **Never provides scripts**: Forces users to think strategically, not copy-paste phrases.

## 🎯 Advanced Features

### **Director Mode: Goal Tracking & Off-Topic Detection**
A Game Director monitors whether the user is actually attempting the negotiation scenario:

- **`is_off_topic`**: Boolean flag detecting test messages, nonsense, or irrelevant input
- **`goal_alignment_score`**: 0-100% progress meter toward successfully negotiating the scope change
- **`director_warning`**: Stern intervention when users drift from the mission

**Example:**
```
User: "test you"
Alex: "I don't have time for this. Do you actually need something or not?"
Coach: ⚠️ MISSION WARNING - You are wasting Alex's time. Get back to negotiating the scope change immediately.
Progress: 0% (RED)
```

### **Mission Progress Bar**
Visual feedback showing negotiation progress with color-coded states:
- **Red (0-24%)**: No progress, stuck
- **Orange (25-49%)**: Initial engagement
- **Purple (50-74%)**: Active negotiation
- **Green (75-100%)**: Near resolution

### **Multi-Scenario Platform**
The simulator supports multiple negotiation scenarios via dropdown selector:
- **Scope Change Under Pressure** (default): PM requesting scope change mid-sprint
- **Deadline Negotiation**: Discussing timeline extensions
- **Resource Conflict**: Competing priorities

Each scenario maintains isolated session state with scenario-specific context cards.

### **Whisper Design Pattern**
Alex's inner thoughts and perceptions use a "whisper" visual metaphor:
- **First Occurrence Labels**: "💭 Alex thought" and "👂 Alex heard" appear once, then switch to icon-only
- **Italic Secondary Text**: Reduced opacity (62-65%) for hierarchy without overwhelming
- **Inline Coaching**: 💡 icon appears next to user messages with tooltip-based strategic insights
- **Typography Hierarchy**: Primary text (white, 15px) vs. whisper text (gray, italic, 14px)

### **Typing Animation & Real-Time Feedback**
- **Immediate User Bubble**: User message appears instantly when sent
- **Typing Indicator**: Alex's avatar + 3 pulsing dots while waiting for API response
- **Progressive Enhancement**: Perception appears under user bubble after API returns
- **Auto-Scroll**: Timeline automatically scrolls to latest message

## 🎨 UI Design Philosophy: "Gemini 3 Dark Mode"

The interface draws inspiration from Google's Gemini 3 design language with:

- **Deep Charcoal Background (#131314)**: Premium AI-native aesthetic
- **Transparent Alex Bubbles**: Text sits directly on background for conversational flow
- **Pill-Shaped User Messages (#2D2E2F)**: Muted blue-grey with generous padding
- **Floating Capsule Input**: Elevated input field with shadow and rounded corners (border-radius: 100px)
- **Minimalist Header**: 3-zone grid layout (Brand | Scenario Dropdown | Progress Widget)
- **Typography-First Hierarchy**: Inter/Sans-serif with carefully tuned opacity levels
- **Subtle Animations**: Calm bounce for typing dots, smooth fade-ins, no aggressive motion
- **Strategic Insight Icon (💡)**: Minimalist tooltip-based coaching that doesn't interrupt flow

### Design Tokens (CSS Variables)
```css
--bg-body: #131314        /* Deep charcoal */
--bg-surface: #1E1F20     /* Input/header surface */
--bg-user-bubble: #2D2E2F /* User message pill */
--text-primary: #E3E3E3   /* Off-white */
--text-secondary: #C4C7C5 /* Light gray */
--accent-color: #A8C7FA   /* Pale blue */
--border-color: #444746   /* Subtle borders */
```

## 🛠 Tech Stack

- **Backend**: Python 3.11+ with FastAPI
- **AI**: OpenAI GPT-4 Turbo (JSON mode for structured outputs)
- **Frontend**: Vanilla JavaScript, HTML5, CSS3 (no frameworks)
- **Session Management**: In-memory dict keyed by UUID
- **Deployment**: Docker-ready for Render.com
- **Design**: Gemini 3-inspired dark mode with floating UI elements

## 🏃‍♂️ How to Run

### Local Development

1. Clone the repo:
```bash
git clone <repo-url>
cd first-attempt-2f8d
```

2. Set your OpenAI API key:
```bash
export OPENAI_API_KEY="sk-..."
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the server:
```bash
python3 -m uvicorn agent:app --host 0.0.0.0 --port 8000
```

5. Open your browser:
```
http://localhost:8000
```

### Using Docker

```bash
docker build -t alex-agent .
docker run -p 10000:10000 -e OPENAI_API_KEY="sk-..." alex-agent
```

Then visit `http://localhost:10000`

### Deployment to Render.com

The included `Dockerfile` is optimized for Render:

1. **Push to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Difficult Conversations Simulator"
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **Create Web Service on Render**:
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Build Command**: (auto-detected from Dockerfile)
     - **Start Command**: (auto-detected from Dockerfile)
     - **Port**: 10000

3. **Add Environment Variable**:
   - In Render dashboard, go to "Environment"
   - Add: `OPENAI_API_KEY` = `sk-...` (your OpenAI API key)

4. **Deploy**:
   - Click "Create Web Service"
   - Render will automatically build and deploy
   - Access your app at `https://your-app-name.onrender.com`

## 🧠 Architecture Decisions

### **The "Strategic Coach" (Not a Scriptwriter)**

I designed the coaching system to provide **strategic insights** rather than **copy-paste scripts**. 

**Why?** 
- Scripts create dependency: users don't learn communication principles
- Strategy forces active learning: users must think about *why* their approach failed
- Generalization: strategic thinking transfers to new situations

**How it works:**
The system prompt explicitly forbids the AI from providing example phrases. Instead, it must:
1. Explain the psychological impact ("Your vagueness triggered anxiety")
2. Suggest high-level tactics ("Use a 'softener' to acknowledge workload")

### **Perception as Translation Layer**

The "Alex heard" block appears directly under the user's message (not under Alex's response). This creates a visual metaphor:

```
[User's Message]
   ↓
[How Alex Twisted It] ← Translation/Distortion Layer
   ↓
[Alex's Response]
```

This makes communication breakdown *visible* and educational.

### **Session State Management**

The application maintains:
- **Conversation History**: Full chat log sent to GPT-4 for context continuity
- **Session Isolation**: Each browser session gets a unique UUID
- **Stateless Backend**: Sessions stored in-memory (scalable to Redis/DB for production)

Alex can "remember" earlier interactions, hold grudges, or gradually de-escalate based on cumulative behavior.

### **Punchy, Raw Language**

Early versions used academic language:
- ❌ "It seems they're trying to be diplomatic, but it still feels like another last-minute request."

Current version uses gut reactions:
- ✅ "Another last-minute request dumped on me."

**Why?** Raw language is:
- Faster to read
- More emotionally impactful
- Closer to how people actually think

### **Visual Hierarchy & Accessibility**

- **Alex Avatar**: 32px circular badge with "A" initial, dark background + border
- **User Messages**: Right-aligned, 80% max-width, pill-shaped bubbles
- **Alex Messages**: Left-aligned, transparent background (text on page background)
- **Context Card**: Centered system pill with "CONTEXT" label, transparent background with border
- **Progress Widget**: Compact bar (100px × 6px) with color-coded states:
  - **Red (0-24%)**: No progress
  - **Orange (25-49%)**: Initial engagement
  - **Purple (50-74%)**: Active negotiation
  - **Green (75-100%)**: Near resolution

## 📂 Project Structure

```
.
├── agent.py                 # FastAPI backend + OpenAI integration
├── persona.json             # Alex's personality configuration
├── templates/
│   └── index.html           # Frontend UI structure
├── static/
│   ├── style.css            # Gemini 3 dark mode styling
│   └── script.js            # Frontend logic (async, animations, tooltips)
├── requirements.txt         # Python dependencies
├── Dockerfile               # Production deployment config
├── .env                     # API key storage (git-ignored)
└── README.md                # This file
```

## 🎓 Educational Philosophy

This simulator is based on the principle that **negotiation is pattern recognition**:

1. **Identify the emotional state** (stressed, defensive, rushed)
2. **Adapt communication style** (acknowledge constraints, show empathy)
3. **Track progress** (Am I moving toward resolution or escalation?)

By forcing users to analyze *why* their message failed (not just *what* to say instead), the system builds transferable communication skills.

## 🔮 Future Enhancements

- **Multiple Active Scenarios**: Backend support for scenario switching (currently frontend-only)
- **Additional Personas**: Passive-aggressive PM, perfectionist designer, burned-out QA engineer
- **Stress Meter Visualization**: Real-time graph showing Alex's emotional state over time
- **Conversation Branching**: Critical decision points with multiple strategic paths
- **Export Transcript**: Download conversation history for review/training
- **Difficulty Levels**: Beginner (more forgiving) to Expert (hair-trigger emotional responses)
- **Mobile Optimization**: Enhanced touch interactions and responsive design refinements
- **Persistent Sessions**: Redis/PostgreSQL for session persistence across deployments

## 📄 License

MIT License - Feel free to use for training, education, or research.

## 🤝 Contributing

This is a demonstration project, but suggestions for improving the coaching logic or adding new personas are welcome!

---

**Built with ❤️ for better workplace communication**
