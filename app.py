import streamlit as st
import ollama
import time
import json

# Custom CSS for a sleek dark theme
st.markdown("""
    <style>
        .stApp {
            background-color: #1a1a2e;
            color: #ffffff;
            font-family: 'Arial', sans-serif;
        }
        .stChatMessage {
            border-radius: 15px;
            padding: 15px;
            margin-bottom: 15px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.3);
            background-color: #16213e;
        }
        .user { border-left: 4px solid #00d4ff; }
        .assistant { border-left: 4px solid #ff00ff; }
        .stButton > button {
            background-color: #ff4d4d;
            color: white;
            border-radius: 10px;
            padding: 10px 20px;
            font-weight: bold;
            transition: all 0.3s ease;
        }
        .stButton > button:hover {
            background-color: #cc0000;
            transform: scale(1.05);
        }
        .stSidebar {
            background-color: #0f0f23;
            padding: 20px;
            border-right: 1px solid #333;
        }
        .stTextInput > div > div > input {
            background-color: #2a2a44;
            color: #ffffff;
            border-radius: 10px;
            padding: 10px;
            border: 1px solid #444;
        }
        .stTitle {
            color: #ff6f61;
            text-align: center;
            padding: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }
        .stSpinner > div {
            border-top-color: #ff4d4d !important;
        }
    </style>
""", unsafe_allow_html=True)

# Session state initialize for chat history and settings
if "messages" not in st.session_state:
    st.session_state.messages = []
if "model" not in st.session_state:
    st.session_state.model = "llama3"  # Default model
if "temperature" not in st.session_state:
    st.session_state.temperature = 0.7  # Default creativity level
if "user_image" not in st.session_state:
    st.session_state.user_image = "image1.jpg"  # Path to your image (add image1.jpg to the project folder)
if "user_profile" not in st.session_state:
    st.session_state.user_profile = {
        "name": "Muhammad Ubaid Raza",
        "profession": "Software Developer (Bachelor of Science in Software Engineering from Ilma University, Karachi - Continue)",
        "skills": "HTML, CSS, Java Script, MY SQL, Bootstrap, Python, React, Machine Learning",
        "experience": "01 years in tech industry, CIT Web Development from Institute of Business Management (IOBM), Karachi (3 months, In 2024)",
        "interests": "Agentic AI, Web Developer, Certified AI, Metaverse, and Web 3.0 Developer (Agentic AI) from Governer House",
        "education": "Intermediate (Pre-Engineering) B Grade 2021, Matriculation (Computer Science) A Grade 2019, Darse Nizami (Alim course, 6th year complete), Hifzul Quran ul Karim (Hafiz)",
        "personal": "Father’s Name: Muhammad Farooq, Date of Birth: 6th February 2002, Nationality: Pakistani, Marital Status: Single",
        "contact": "House No. 499, Area “A”, Korangi No 06, Market, Karachi. Cell #: +92-316-3657767, Email: ubaidraza3657767@gmail.com",
        "objective": "Seeking a professional position to utilizing my skills and abilities in the practical life to improve the strength of the company where my creative ideas and a genuine enthusiasm would allow me to progress and to grow professionally and to contribute within a team in challenging implementing and administrating setup."
    }  # Your details from CV hardcoded in code

# Sidebar for settings
with st.sidebar:
    st.title("Settings")
    
    # Available Ollama models list with error handling
    try:
        available_models = ollama.list()["models"]
        model_names = [model["model"] for model in available_models]  # Extract model names
        if not model_names:
            st.warning("No models available. Run 'ollama pull llama3'.")
            model_names = ["llama3"]  # Fallback
    except Exception as e:
        st.error(f"Could not connect to Ollama: {str(e)}. Start Ollama server (ollama serve) and check port 11434.")
        model_names = ["llama3"]  # Fallback
    
    st.session_state.model = st.selectbox("Select LLM Model", model_names, index=model_names.index(st.session_state.model) if st.session_state.model in model_names else 0)
    
    # Temperature slider for response creativity
    st.session_state.temperature = st.slider("Temperature (Creativity)", min_value=0.0, max_value=1.0, value=st.session_state.temperature, step=0.1)
    
    # Chat history export
    if st.button("Export Chat History"):
        with open("chat_history.json", "w") as f:
            json.dump(st.session_state.messages, f)
        st.success("Chat history exported to chat_history.json")

# Main page title and chat container
st.title("Advanced LLM Chat Interface")

# Conversation history chat bubbles with avatars
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="🧑‍💻" if message["role"] == "user" else st.session_state.user_image if st.session_state.user_image else "🤖"):
        st.markdown(f"**{message['role'].capitalize()}** ({message['timestamp']}): {message['content']}")

# User input chat-like bottom
prompt = st.chat_input("Enter your query here...")

if prompt:
    # Add user message to history with timestamp
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.messages.append({"role": "user", "content": prompt, "timestamp": timestamp})
    
    # Display user message immediately
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(f"**User** ({timestamp}): {prompt}")
    
    # Generate LLM response with loading animation
    with st.chat_message("assistant", avatar=st.session_state.user_image if st.session_state.user_image else "🤖"):
        with st.spinner("Thinking..."):
            try:
                response = ollama.chat(
                    model=st.session_state.model,
                    messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                    options={"temperature": st.session_state.temperature}
                )
                ai_response = response['message']['content']
                ai_timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                
                # Custom response for "Tell me about Ubaid Raza"
                if "ubaid raza" in prompt.lower():
                    profile_info = f"**About {st.session_state.user_profile['name']}**\n" \
                                 f"- **Objective**: {st.session_state.user_profile['objective']}\n" \
                                 f"- **Profession**: {st.session_state.user_profile['profession']}\n" \
                                 f"- **Skills**: {st.session_state.user_profile['skills']}\n" \
                                 f"- **Experience**: {st.session_state.user_profile['experience']}\n" \
                                 f"- **Interests**: {st.session_state.user_profile['interests']}\n" \
                                 f"- **Education**: {st.session_state.user_profile['education']}\n" \
                                 f"- **Personal Profile**: {st.session_state.user_profile['personal']}\n" \
                                 f"- **Contact**: {st.session_state.user_profile['contact']}"
                    ai_response = profile_info
                    if st.session_state.user_image:
                        st.image(st.session_state.user_image, caption=f"Image of {st.session_state.user_profile['name']}", use_column_width=True)
                
                st.markdown(f"**Assistant** ({ai_timestamp}): {ai_response}")
                
                # Add to history
                st.session_state.messages.append({"role": "assistant", "content": ai_response, "timestamp": ai_timestamp})
            except Exception as e:
                st.error(f"Error: {str(e)}. Check Ollama server or model.")
# Reset button for clearing history
if st.button("Reset Conversation"):
    st.session_state.messages = []
    st.rerun()  # Refresh app