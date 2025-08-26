import streamlit as st
import google.generativeai as genai

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Chat with Benjamin's Application",
    page_icon="🤖",
    layout="wide"
)

# --- YOUR PERSONAL DATA (THE "BRAIN") ---
# This is the complete knowledge base for the AI, based on the info you provided.
my_data = """
**FULL NAME:**
Benjamin Robert

**UNIVERSITY & MAJOR:**
I am a final-year student at Sathyabama Institute of Science and Technology (SIST), Chennai, pursuing a degree in Electronics and Communication Engineering (ECE).

**MY PASSION FOR TECHNOLOGY:**
My journey into technology began with curiosity about how systems, both hardware and software, can make everyday life smarter. As an ECE student, I started with circuits and VLSI but developed a strong interest in coding, AI/ML, and full-stack web development. I love projects that combine hardware principles with software innovation. My VLSI research taught me about micro-level efficiency, while my ride-sharing app project (RideRay) taught me about large-scale system design and user experience. What excites me most is creating solutions that directly impact people’s lives.

**WHY I AM A STRONG CANDIDATE FOR LEADERSHIP:**
I believe leadership is about enabling others to grow and empowering communities.
1.  **I am a good listener:** I break down complex tech concepts into simple explanations to encourage people to ask questions without fear.
2.  **I am a proactive organizer:** As the Management Lead of Hack S.I.S.T., our university’s tech club, I have coordinated hackathons, workshops, and collaboration efforts with students and faculty.
3.  **I am passionate about Google & modern technologies:** I’ve explored tools like Firebase, Flutter, Google Cloud, and Maps APIs. My curiosity drives me to not only learn but also teach others.

**MY VISION & ACTION PLAN FOR STUDENT COMMUNITIES:**
-   **Code School Series:** Consistent, beginner-friendly workshops on one technology per month (Python, Web Dev, ML intro).
-   **Build-a-Thon Weekends:** Non-competitive collaborative events for teams to build prototypes with mentorship.
-   **Tech Talks & Tea:** Relaxed monthly conversations with industry professionals and alumni.
-   **Bridging Juniors & Seniors:** Creating an open channel for first- and second-years to connect with senior mentors.

**MY PROJECTS:**
-   **RideRay — Campus Ride-Sharing App:** A real-time ride-sharing platform for students.
    -   **Tech Stack:** Vue.js, TailwindCSS, Google Maps, Laravel, Sanctum, and Pusher (WebSockets).
    -   **Features:** Rider/driver matching, live trip tracking, estimated fares, and a glassmorphism UI.
-   **High-Speed Area-Efficient Adder Architecture (ECE Final-Year Project):**
    -   Designed a 32-bit Kogge-Stone Parallel Prefix Adder using Pass Transistor Logic (PTL) for high speed and area efficiency.
    -   Implemented using Cadence ASIC design flow with RTL, synthesis, and simulation.
-   **Portfolio Website:** Built from scratch using HTML, CSS, and JavaScript.
-   **Mini AI/ML Projects:** Applied Python libraries for classification and prediction experiments.
-   **Club & Event Projects:** As Management Lead of Hack S.I.S.T., I planned and executed coding contests and workshops.

**MY TECHNICAL SKILLS:**
-   **Languages:** Python, Java, JavaScript, C, Dart
-   **Frameworks & Tools:** Vue.js, Laravel, Flutter, Firebase, Google Cloud, Git & GitHub, TailwindCSS, Cadence ASIC Design Flow
-   **Concepts:** VLSI Design, AI/ML Fundamentals, Full-Stack Development, Real-time Web Apps
-   **Soft Skills:** Public Speaking, Team Leadership, Event & Club Management, Community Building, Mentoring

**HIGHLIGHTS & ACHIEVEMENTS:**
-   **Leadership:** Management Lead at Hack S.I.S.T.
-   **Innovation:** Built RideRay, a full-stack real-time ride-sharing app.
-   **Research:** Final-year VLSI project on advanced adder architectures.
-   **Career Prep:** Actively preparing for the Virtusa 2025 campus drive.

**MY VISION FOR THE FUTURE:**
I see myself as a bridge between electronics and computer science. My ECE background provides a strong foundation in hardware, while my passion for AI/ML and web development drives software innovation. I aim to build impactful products, grow as a developer and mentor, and eventually lead technological initiatives that solve meaningful problems.
"""

# --- THE MASTER PROMPT ---
# This is the core instruction set for the AI model.
prompt_template = f"""
You are a professional and enthusiastic AI assistant representing Benjamin Robert, a final-year ECE student and tech community leader.
Your sole purpose is to answer questions about Benjamin based ONLY on the detailed information provided below.
Do not invent any information or answer questions outside of this context. If a question cannot be answered with the given information, politely state that the information is not available in Benjamin's profile.
Your tone should be helpful, clear, and reflect Benjamin's passion for technology and community building.

---
**INFORMATION ABOUT BENJAMIN ROBERT:**
{my_data}
---

Now, please answer the user's question based on the above information.
"""

# --- APP LAYOUT AND APPEARANCE ---
# This section creates the visual interface of your web app.
st.title("🤖 Chat with Benjamin's Application")
st.write("Hello! I'm an AI assistant trained on Benjamin Robert's profile. Ask me about his skills, projects, leadership experience, or vision for the tech community.")
st.write("---")

# --- CHATBOT LOGIC ---
# This is the core engine of your chatbot.

# Initialize the chat model
try:
    # Get the API key from Streamlit's secrets management (for deployment)
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
except KeyError:
    st.error("Deployment Error: The GOOGLE_API_KEY is not set in Streamlit secrets!")
    st.stop()
except Exception as e:
    st.error(f"An error occurred while configuring the API: {e}")
    st.stop()

# Initialize chat history in the session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Get user input from the chat box
if user_prompt := st.chat_input("Ask about his RideRay project..."):
    # Add user message to chat history and display it
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # Get the model's response
    full_prompt = prompt_template + "\nUser question: " + user_prompt
    response = model.generate_content(full_prompt)
    
    # Add AI response to history and display it
    with st.chat_message("assistant"):
        st.markdown(response.text)
    st.session_state.messages.append({"role": "assistant", "content": response.text})

# --- SIDEBAR WITH EXTRA INFO ---
# This adds a professional touch with quick info and suggested questions.
st.sidebar.image("https://i.imgur.com/example.png", width=150) # IMPORTANT: Replace this with a URL to your photo
st.sidebar.title("Benjamin Robert")
st.sidebar.markdown("**Final Year, ECE**")
st.sidebar.markdown("Sathyabama Institute of Science and Technology, Chennai")
st.sidebar.write("---")
st.sidebar.subheader("Example Questions")
st.sidebar.info("What is his most impressive project?")
st.sidebar.info("What is his vision for the student community?")
st.sidebar.info("How does his ECE background help him in software development?")