# Import your chatbot class here
from chatbot import TrekkingBot

if __name__ == "__main__":
    # The code for running your chatbot goes here
    chatbot = TrekkingBot()
    chatbot.greeting()

    response = chatbot.respond("I want to plan a trek.")

    while chatbot.conversation_is_active():
        response = chatbot.respond(response)
    
    chatbot.farewell()