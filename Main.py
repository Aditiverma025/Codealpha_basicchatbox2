import json
import random
from datetime import datetime
from pathlib import Path

USER_DATA_FILE = Path("user_data.json")
CHAT_LOG_FILE = Path("chat_history.txt")
FEEDBACK_FILE = Path("feedback.txt")

DEVELOPER_INFO = {
    "name": "aditi verma",
    "age": "20",
    "location": "Noida",
    "education": "B.Tech CSE Student",
    "internship": "CodeAlpha Python Programming Internship",
    "project": "SmartHelp Chatbot"
}

INTENTS = {
    "greeting": {
        "keywords": ["hello", "hi", "hey", "good morning", "good evening"],
        "responses": [
            "Hello! I am SmartHelp Bot. How can I help you today?",
            "Hi there! What would you like to ask?",
            "Hey! I am ready to help you."
        ]
    },

    "wellbeing": {
        "keywords": ["how are you", "how are you doing", "are you fine"],
        "responses": [
            "I'm doing great. Thanks for asking!",
            "I'm fine and ready to help you.",
            "I am working perfectly."
        ]
    },

    "bot_name": {
        "keywords": ["your name", "who are you", "what is your name"],
        "responses": [
            "My name is SmartHelp Bot.",
            "I am SmartHelp Bot, your Python virtual assistant."
        ]
    },

    "creator": {
        "keywords": [
            "who made you",
            "your developer",
            "created you",
            "developer info",
            "about developer",
            "about naman"
        ],

        "responses": [
            "I was created by Naman Phogat, a B.Tech CSE student from Noida, during the CodeAlpha Python Programming Internship.",
            "My developer is Naman Phogat. He built me as an advanced Python chatbot project for CodeAlpha."
        ]
    },

    "help": {
        "keywords": ["help", "features", "what can you do"],
        "responses": [
            "I can answer FAQs, remember your name, show date/time, save chat history, and collect feedback."
        ]
    },

    "thanks": {
        "keywords": ["thanks", "thank you", "thx"],
        "responses": [
            "You're welcome!",
            "Glad I could help!",
            "Anytime!"
        ]
    },

    "bye": {
        "keywords": ["bye", "goodbye", "exit", "quit"],
        "responses": [
            "Goodbye! Have a great day.",
            "Bye! Thanks for chatting.",
            "See you soon!"
        ]
    }
}

FAQS = {
    "python": "Python is a powerful high-level programming language used in AI, web development, automation, and data science.",

    "codealpha": "CodeAlpha provides internship opportunities and project-based learning for students.",

    "internship": "An internship helps students gain practical experience through real-world projects.",

    "chatbot": "A chatbot is a software application that interacts with users through text or voice.",

    "json": "JSON stands for JavaScript Object Notation. It is used to store and exchange data.",

    "file handling": "File handling means reading and writing data into files using programming."
}


def load_user_data():
    if USER_DATA_FILE.exists():
        try:
            with open(USER_DATA_FILE, "r") as file:
                return json.load(file)

        except json.JSONDecodeError:
            return {}

    return {}


def save_user_data(data):
    with open(USER_DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)


def log_chat(user_message, bot_response):
    with open(CHAT_LOG_FILE, "a") as file:
        file.write(f"[{datetime.now()}] User: {user_message}\n")
        file.write(f"[{datetime.now()}] Bot: {bot_response}\n\n")


def save_feedback(feedback):
    with open(FEEDBACK_FILE, "a") as file:
        file.write(f"[{datetime.now()}] {feedback}\n")


def detect_intent(message):
    message = message.lower()

    for intent, data in INTENTS.items():
        for keyword in data["keywords"]:
            if keyword in message:
                return intent

    if "date" in message:
        return "date"

    if "time" in message:
        return "time"

    return "unknown"


def search_faq(message):
    message = message.lower()

    for topic, answer in FAQS.items():
        if topic in message:
            return answer

    return None


def get_bot_response(user_message, user_data):
    message = user_message.lower().strip()

    # Save user name
    if message.startswith("my name is"):
        name = user_message[11:].strip().title()

        if name:
            user_data["name"] = name
            save_user_data(user_data)

            return f"Nice to meet you, {name}. I will remember your name."

        return "Please tell me your name properly."

    # Recall saved name
    if "what is my name" in message or "do you know my name" in message:

        if "name" in user_data:
            return f"Your name is {user_data['name']}."

        return "I don't know your name yet. Type: My name is Naman"

    # Developer Information
    if (
        "developer info" in message
        or "about developer" in message
        or "about naman" in message
    ):

        return (
            f"Developer Name: {DEVELOPER_INFO['name']}\n"
            f"Age: {DEVELOPER_INFO['age']}\n"
            f"Location: {DEVELOPER_INFO['location']}\n"
            f"Education: {DEVELOPER_INFO['education']}\n"
            f"Internship: {DEVELOPER_INFO['internship']}\n"
            f"Project: {DEVELOPER_INFO['project']}"
        )

    # Feedback
    if message.startswith("feedback"):

        feedback = user_message.replace("feedback", "", 1).strip()

        if feedback:
            save_feedback(feedback)

            return "Thank you! Your feedback has been saved."

        return "Please write your feedback after the word feedback."

    # FAQ Search
    faq_answer = search_faq(message)

    if faq_answer:
        return faq_answer

    # Intent Detection
    intent = detect_intent(message)

    if intent == "date":
        return "Today's date is " + datetime.now().strftime("%d-%m-%Y")

    if intent == "time":
        return "Current time is " + datetime.now().strftime("%I:%M %p")

    if intent in INTENTS:
        return random.choice(INTENTS[intent]["responses"])

    return (
        "I am not sure about that.\n"
        "You can ask me about:\n"
        "- Python\n"
        "- CodeAlpha\n"
        "- Internship\n"
        "- JSON\n"
        "- File Handling\n"
        "- Date and Time\n"
        "- Developer Info"
    )


def show_intro():

    print("=" * 60)
    print("                 SMARTHELP CHATBOT")
    print("=" * 60)

    print(f"Developer : {DEVELOPER_INFO['name']}")
    print(f"Education : {DEVELOPER_INFO['education']}")
    print(f"Project   : {DEVELOPER_INFO['project']}")
    print(f"Internship: {DEVELOPER_INFO['internship']}")

    print("=" * 60)

    print("Features:")
    print("- Remembers your name")
    print("- Answers FAQs")
    print("- Shows current date and time")
    print("- Saves chat history")
    print("- Saves feedback")
    print("- Shows developer information")
    print("- Type 'bye' to exit")

    print("=" * 60)


def chatbot():

    user_data = load_user_data()

    show_intro()

    if "name" in user_data:
        print(f"Bot: Welcome back, {user_data['name']}!")

    else:
        print("Bot: Hello! Tell me your name using:")
        print("Bot: My name is Aditi")

    while True:

        user_message = input("\nYou: ").strip()

        if user_message == "":
            print("Bot: Please type something.")
            continue

        bot_response = get_bot_response(user_message, user_data)

        print("Bot:", bot_response)

        log_chat(user_message, bot_response)

        if detect_intent(user_message) == "bye":
            break


if __name__ == "__main__":
    chatbot()
