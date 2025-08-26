import streamlit as st
import google.generativeai as genai

# ------------------------
# PAGE CONFIGURATION
# ------------------------
st.set_page_config(
    page_title="R J Benjamin Robert | AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------
# CUSTOM CSS (Google Theme)
# ------------------------
st.markdown(
    """
    <style>
        body {
            font-family: 'Google Sans', sans-serif;
        }
        .user-bubble {
            background-color: #4285F4;
            color: white;
            padding: 10px 15px;
            border-radius: 20px;
            margin: 5px 0;
            max-width: 70%;
            align-self: flex-end;
        }
        .bot-bubble {
            background-color: #F1F3F4;
            color: #202124;
            padding: 10px 15px;
            border-radius: 20px;
            margin: 5px 0;
            max-width: 70%;
            align-self: flex-start;
        }
        .stChatMessage {
            background: transparent !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ------------------------
# PERSONAL DATA (THE "BRAIN")
# ------------------------
my_data = """
**FULL NAME:**
R J Benjamin Robert

**UNIVERSITY & MAJOR:**
Final-year student at Sathyabama Institute of Science and Technology (SIST), Chennai, pursuing Electronics and Communication Engineering (ECE).

**PASSION FOR TECHNOLOGY:**
Started with circuits and VLSI → grew passionate about coding, AI/ML, and full-stack development. Love combining hardware principles with software innovation. RideRay project taught me system design & user experience. VLSI research gave me micro-level efficiency insights.

**LEADERSHIP EXPERIENCE:**
- Management Lead at Hack S.I.S.T. → coordinated hackathons, workshops, student–faculty collaborations.
- Tech Lead of DSC Sathyabama (ex-GDSC) → community building, mentoring juniors.
- Believe in enabling others, simplifying tech concepts, and empowering communities.

**VISION & ACTION PLAN:**
- Code School Series (monthly beginner-friendly workshops).
- Build-a-Thon Weekends (collaborative prototyping).
- Tech Talks & Tea (industry + alumni sessions).
- Mentor Bridge (connecting juniors & seniors).

**PROJECTS:**
- RideRay (Campus Ride-Sharing App): Vue.js, Tailwind, Google Maps, Laravel, Sanctum, WebSockets.
- VLSI Project: 32-bit Kogge-Stone Adder using PTL (Cadence ASIC design).
- Portfolio Website: Built with HTML, CSS, JS.
- Mini AI/ML Projects: Python experiments in classification/prediction.
- Event Projects: Organized coding contests & workshops.

**TECHNICAL SKILLS:**
- Languages: Python, Java, JavaScript, C, Dart
- Tools/Frameworks: Vue.js, Laravel, Flutter, Firebase, Google Cloud, TailwindCSS, GitHub, Cadence ASIC Flow
- Concepts: VLSI, AI/ML basics, Full-stack, Real-time Web Apps
- Soft Skills: Public Speaking, Team Leadership, Mentoring

**HIGHLIGHTS:**
- Leadership → Hack S.I.S.T. & DSC Tech Lead
- Innovation → Built RideRay
- Research → VLSI adder architectures
- Career → Preparing for Virtusa 2025 drive

**VISION FOR FUTURE:**
Bridge electronics + computer science → impactful products, mentoring, and leading solutions with real-world impact.
"""

# ------------------------
# MASTER PROMPT
# ------------------------
prompt_template = f"""
You are a professional and enthusiastic AI assistant representing Benjamin Robert, 
a final-year ECE student and tech community leader.

Answer only using the information provided in his profile below. 
If asked something outside the scope, politely respond that this info is not available in Benjamin's profile.
Maintain a clear, helpful, and passionate tone.

---
PROFILE INFORMATION:
{my_data}
---
"""

# ------------------------
# SIDEBAR
# ------------------------
with st.sidebar:
    st.image("https://i.imgur.com/gL4KZc2.jpeg", width=150)
    st.title("R J Benjamin Robert")
    st.markdown("**ECE Final Year | Tech Community Lead**")
    st.markdown("Sathyabama Institute of Science and Technology")
    st.divider()
    st.subheader("💡 Example Questions")
    st.info("🌟 What is Benjamin’s vision for the student community?")
    st.info("🚀 Tell me about the RideRay project.")
    st.info("🤝 What is his leadership experience?")

# ------------------------
# MAIN CONTENT
# ------------------------
st.title("🤖 Google-Themed AI Assistant")
st.markdown("### Ask me anything about Benjamin Robert!")
st.divider()

# ------------------------
# CHATBOT LOGIC
# ------------------------
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
except KeyError:
    st.error("Deployment Error: Add your GOOGLE_API_KEY to Streamlit secrets.")
    st.stop()
except Exception as e:
    st.error(f"Error: {e}")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

chat_container = st.container()

# Display existing chat
with chat_container:
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"<div class='user-bubble'>{msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='bot-bubble'>{msg['content']}</div>", unsafe_allow_html=True)

# Input
if user_prompt := st.chat_input("Ask about his projects, skills, or vision..."):
    st.session_state.messages.append({"role": "user", "content": user_prompt})

    full_prompt = prompt_template + "\nUser question: " + user_prompt
    response = model.generate_content(full_prompt)
    bot_reply = response.text

    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    st.rerun()
