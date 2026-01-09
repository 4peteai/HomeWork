# 🐘 Grey - Difficult Conversations Training

**"The conversation didn't fail. You just missed the elephant."**

Grey is an AI-powered negotiation simulator that reveals the hidden dynamics in difficult workplace conversations. Unlike traditional communication training, Grey shows you **what they actually heard** and **what they didn't say** — the elephant in the room that makes or breaks real conversations.

## 🎯 Core Philosophy

Most conversations don't break because of bad intentions. They break in the gap between:
- **What you said**
- **What they actually heard**
- **What stayed unspoken**

Grey puts you inside that gap and shows you what you missed.

## 🚀 Key Features

### **4-Layer Cognitive System**

Every conversational turn reveals four distinct layers of cognition:

1. **👂 Alex Heard** (Perception Layer)
   - How Alex interpreted your message through their biased, emotional filter
   - Example: You say "Can we talk?" → Alex hears "Another vague meeting request wasting my time."

2. **💭 Alex Thought** (Inner Monologue)
   - Raw, unfiltered emotions driving Alex's response
   - Example: "Great, another fire drill. Why do I always get stuck cleaning up their mess?"

3. **💬 Alex Said** (Spoken Response)
   - What Alex actually says out loud, staying in character

4. **💡 Strategic Insight** (The Coach)
   - Explains the psychological impact: "Your vagueness triggered Alex's anxiety about unknown commitments."
   - Suggests high-level tactics: "Use a 'softener' to acknowledge their workload before making the ask."
   - **Never provides scripts** — you must think strategically, not copy-paste phrases

### **5 Relationship-Testing Scenarios**

Grey features five conversations that pressure different fault lines in the same working relationship with Alex, your Tech Lead:

1. **📅 Friday Favor**
   - Trigger: Timing | Focus: Intent
   - You need a favor. Alex is already done for the week.

2. **⚡ Scope Change Under Pressure**
   - Trigger: Overload | Focus: Balance
   - You need Alex to take on more work. They already feel overloaded.

3. **💔 Broken Promise**
   - Trigger: Trust | Focus: Repair
   - You didn't deliver what you promised. Alex is dealing with the fallout.

4. **🚀 Security Blocker**
   - Trigger: Risk | Focus: Navigation
   - Progress is blocked because of perceived risk. Alex has the authority to stop everything.

5. **💀 Uptime Standoff**
   - Trigger: Accountability | Focus: Authority
   - Acting now is risky. Waiting is costly. Alex doesn't want to own the downside.

### **Character Continuity: One Relationship, Five Fault Lines**

All scenarios feature the same character (Alex, Tech Lead) to create a continuous relationship arc. This design choice:
- Mirrors real workplace relationships where the same person appears in different high-pressure contexts
- Allows skills to compound across scenarios
- Creates psychological continuity and deeper strategic learning

### **Turn-Based Gamification System**

Each scenario has a **Par Score** (optimal minimum turns to completion):
- **Optimal Path**: Meet the par score in 1-3 turns
- **Over Par**: Complete the scenario in more turns
- **Completion Modal**: Shows your performance vs. optimal path with color-coded feedback

### **AI-Generated Winning Explanations**

When you successfully complete a scenario (100% goal alignment), the AI analyzes **what you specifically did** and generates a tactical explanation:

Example:
> "You acknowledged the timing issue upfront and offered a specific trade-off (pushing back the dashboard work). This reciprocity shifted the frame from 'demanding more' to 'negotiating fairly,' which preserved the relationship."

This ensures every winning strategy is personalized to your actual conversation, not generic advice.

### **Director Mode: Goal Tracking & Off-Topic Detection**

The Game Director monitors whether you're actually engaging with the scenario:
- **`is_off_topic`**: Detects test messages, nonsense, or irrelevant input
- **`goal_alignment_score`**: 0-100% progress toward successfully navigating the conversation
- **`director_warning`**: Stern intervention when you drift from the mission

### **Material Design 3 Interface**

Grey features a premium Material Design 3 dark mode interface:
- **Surface containers** with subtle elevation (1-2dp)
- **28px border radius** for cards and components
- **M3 typography scale** with proper hierarchy
- **Material Symbols Rounded** iconography
- **Tonal color system** (no harsh contrasts)
- **Responsive design** with mobile-optimized text (desktop: "Start Scenario" / mobile: "Start")

## 🎨 Design System

### Color Tokens
```css
--bg-body: #131314        /* Deep charcoal background */
--bg-surface: #1E1F20     /* Card/header surface */
--bg-user-bubble: #2D2E2F /* User message pill */
--text-primary: #E3E3E3   /* Off-white primary text */
--text-secondary: #C4C7C5 /* Light gray secondary text */
--accent-color: #A8C7FA   /* Pale blue accents */
--border-color: #444746   /* Subtle borders */
```

### Typography Hierarchy
- **Display Large**: 56px (homepage title)
- **Title Large**: 36px (section headers)
- **Title Medium**: 18px (card titles)
- **Body Medium**: 16px (primary content)
- **Body Small**: 14px (supporting text)
- **Label**: 13px (metadata labels)

## 🛠 Tech Stack

- **Backend**: Python 3.11+ with FastAPI
- **AI**: OpenAI GPT-4o (structured JSON outputs)
- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **Session Management**: In-memory UUID-keyed sessions
- **Design**: Material Design 3 compliant
- **Icons**: Material Symbols Rounded
- **Typography**: Inter font family

## 🏃 Quick Start

### Local Development

1. **Clone the repository**:
```bash
git clone <repo-url>
cd grey-conversations
```

2. **Set your OpenAI API key**:
```bash
export OPENAI_API_KEY="sk-..."
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Run the server**:
```bash
python3 -m uvicorn agent:app --host 0.0.0.0 --port 5000
```

5. **Open your browser**:
```
http://localhost:5000
```

### Using Docker

```bash
docker build -t grey-conversations .
docker run -p 10000:10000 -e OPENAI_API_KEY="sk-..." grey-conversations
```

Then visit `http://localhost:10000`

### Deployment to Render.com

1. **Push to GitHub**:
```bash
git init
git add .
git commit -m "Initial commit: Grey - Difficult Conversations Training"
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
   - Add: `OPENAI_API_KEY` = `sk-...`

4. **Deploy**:
   - Click "Create Web Service"
   - Access your app at `https://your-app-name.onrender.com`

## 📂 Project Structure

```
.
├── agent.py                 # FastAPI backend + OpenAI GPT-4o integration
├── scenarios.json           # 5 scenario definitions with triggers/skills/par scores
├── templates/
│   ├── home.html           # Homepage with Zero Card + scenario grid
│   ├── scenario.html       # Conversation interface with 4-layer display
│   └── index.html          # Legacy template (deprecated)
├── static/
│   ├── style.css           # Material Design 3 dark mode styling
│   ├── scenario.js         # Conversation logic, typing animation, completion modal
│   └── favicon.svg         # 🐘 elephant favicon
├── requirements.txt         # Python dependencies
├── Dockerfile              # Production deployment config
└── README.md               # This file
```

## 🧠 Architecture Decisions

### **Strategic Coaching, Not Scripts**

The coaching system provides **strategic insights** rather than **copy-paste scripts**.

**Why?**
- Scripts create dependency and prevent learning
- Strategy forces active thinking about communication principles
- Transferable skills that generalize to new situations

**How it works:**
The system prompt explicitly forbids the AI from providing example phrases:
1. Explain the psychological impact ("Your vagueness triggered anxiety")
2. Suggest high-level tactics ("Use a 'softener' to acknowledge workload")

### **100% Goal Alignment Required**

Scenarios only complete when `goal_alignment_score == 100`:
- No partial credit (removed 75% threshold from earlier versions)
- Forces users to fully navigate the conversation
- AI generates personalized winning explanation only at 100%

### **Punchy, Raw Language**

Early versions used academic language:
- ❌ "It seems they're trying to be diplomatic, but it still feels like another last-minute request."

Current version uses gut reactions:
- ✅ "Another last-minute request dumped on me."

**Why?** Raw language is faster to read, more emotionally impactful, and closer to how people actually think.

### **Zero Card: The Intro Pattern**

The homepage features a "Zero Card" — an intro card that sits in the same grid as scenario cards:
- Same dimensions and styling as scenario cards
- No CTA, no background image, no trigger/focus labels
- Left-aligned text with M3 typography hierarchy
- Establishes context before user chooses a scenario

## 🎓 Educational Philosophy

Grey is based on the principle that **negotiation is pattern recognition**:

1. **Identify emotional state** (stressed, defensive, rushed)
2. **Adapt communication style** (acknowledge constraints, show empathy)
3. **Track progress** (moving toward resolution or escalation?)

By forcing users to analyze *why* their message failed (not just *what* to say instead), Grey builds transferable communication skills.

## 🔮 Future Enhancements

- **Additional Personas**: Passive-aggressive PM, perfectionist designer, burned-out QA
- **Stress Meter Visualization**: Real-time emotional state graph
- **Conversation Branching**: Critical decision points with multiple strategic paths
- **Export Transcript**: Download conversation history for review
- **Difficulty Levels**: Beginner (forgiving) to Expert (hair-trigger responses)
- **Persistent Sessions**: Redis/PostgreSQL for cross-deployment continuity
- **Mobile App**: Native iOS/Android versions

## 📄 License

MIT License - Free to use for training, education, or research.

## 🤝 Contributing

Suggestions for improving coaching logic, adding new scenarios, or enhancing the AI reasoning system are welcome!

---

**🐘 Built for better workplace communication**
