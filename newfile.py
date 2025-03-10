class SimpleChatbot:
    def __init__(self):
        self.greetings = ["Hello!", "Hi there!", "Greetings!", "How can I help you today?"]
        self.questions = {
            "how are you": "I'm just a bot, but thanks for asking!",
            "what is your name": "I'm a simple chatbot created for chatting!",
            "tell me a joke": "Why don't scientists trust atoms? Because they make up everything!",
            "are you dumb?":"you are.",
        }

    def greet(self):
        return random.choice(self.greetings)

    def respond(self, user_input):
        user_input = user_input.lower()
        return self.questions.get(user_input, "I'm sorry, I don't understand that.")

def main():
    bot = SimpleChatbot()
    print(bot.greet())

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["bye", "exit", "quit"]:
            print("Bot: Goodbye! Have a great day!")
            break
        response = bot.respond(user_input)
        print("Bot:", response)

if __name__ == "__main__":
    import random
    main()
