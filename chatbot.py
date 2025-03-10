import random

class Chatbot:
    def __init__(self, name):
        self.name = name
        self.responses = {
            "greeting": ["Hello!", "Hi there!", "Greetings!", "How can I assist you today?"],
            "farewell": ["Goodbye!", "See you later!", "Take care!", "Have a great day!"],
            "default": ["I'm not sure how to respond to that.", "Can you please rephrase?", "Let's talk about something else."]
        }

    def get_response(self, user_input):
        user_input = user_input.lower()
        if any(word in user_input for word in ["hello", "hi"]):
            return random.choice(self.responses["greeting"])
        elif any(word in user_input for word in ["bye", "goodbye"]):
            return random.choice(self.responses["farewell"])
        else:
            return random.choice(self.responses["default"])

def main():
    bot = Chatbot("ChatBot")
    print("Welcome to the ChatBot!") 

    while True:
        user_input = input("You: ")
        if user_input.lower() == "quit":
            break
        response = bot.get_response(user_input)
        print("ChatBot:", response)

if __name__ == "__main__":
    main()