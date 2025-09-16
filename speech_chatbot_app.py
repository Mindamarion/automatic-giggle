# speech_chatbot.py

# 1. Import necessary packages
import nltk
import streamlit as st
import speech_recognition as sr

# Make sure NLTK data is available
nltk.download("punkt")

# 2. Load and preprocess chatbot data
# For demonstration, we'll use a very simple chatbot dataset
chatbot_corpus = {
    "hello": "Hi there! How can I help you?",
    "how are you": "I'm doing great, thanks for asking!",
    "what is your name": "I'm your AI chatbot assistant.",
    "bye": "Goodbye! Have a nice day!"
}

# Preprocessing: lowercase for matching
def preprocess(text):
    return text.lower().strip()

# 3. Simple chatbot algorithm
def chatbot_response(user_input):
    processed = preprocess(user_input)
    return chatbot_corpus.get(processed, "Sorry, I didn’t understand that.")

# 4. Function for speech-to-text
def transcribe_speech():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        st.info("🎤 Listening... please speak now.")
        recognizer.adjust_for_ambient_noise(source)  # Handle background noise
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        st.success(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        st.error("Sorry, I could not understand the audio.")
        return None
    except sr.RequestError:
        st.error("Could not request results, please check your internet connection.")
        return None

# 5. Build Streamlit app
st.title("🗣️ Speech-Enabled Chatbot")

st.write("You can interact with the chatbot using **text input** or **speech input**.")

# User input mode selection
mode = st.radio("Choose input mode:", ("Text", "Speech"))

if mode == "Text":
    user_text = st.text_input("Type your message:")
    if st.button("Send"):
        if user_text:
            response = chatbot_response(user_text)
            st.write("🤖 Chatbot:", response)

elif mode == "Speech":
    if st.button("🎙️ Speak Now"):
        speech_text = transcribe_speech()
        if speech_text:
            response = chatbot_response(speech_text)
            st.write("🤖 Chatbot:", response)
