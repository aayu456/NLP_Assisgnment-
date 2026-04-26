# Import your chatbot class here
from chatbot import TrekkingBot

if __name__ == "__main__":
    # The code for running your chatbot goes here
    chatbot = TrekkingBot("TrekSathi")

    chatbot.greeting()

    response = chatbot.respond("Where would you like to go?")

    while chatbot.check_active():
        response = chatbot.respond(response)
    
    chatbot.farewell()