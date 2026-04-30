# Import your chatbot class here
from chatbot import TrekkingBot

if __name__ == "__main__":
    # The code for running your chatbot goes here
    chatbot = TrekkingBot()
    chatbot.greeting()

    response = chatbot.respond("How many days you want to plan a trek for?")

    while chatbot.conversation_is_active:
        response = chatbot.respond(response)
    
    chatbot.farewell()