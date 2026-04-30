import re
import string
from chatbot_base import ChatbotBase
import json
import time

class TrekkingBot(ChatbotBase):

    def __init__(self, name="TrekSathi"):
        super().__init__(name=name)

        self._is_active = True

        self.slots = {
            "destination": None,
            "duration": None,
            "difficulty": None
        }

        self.stopwords = {
            "a", "an", "the", "is", "to", "i", "want", "for", "my", "me",
            "what", "how", "do", "can"
        }

        self.intents = {
            "greeting": {"hello", "hi", "hey", "namaste"},
            "planning": {"plan", "trek", "trip", "itinerary"},
            "weather": {"weather", "temperature", "season"},
            "permit": {"permit", "tims", "document"},
            "exit": {"bye", "exit", "quit", "stop", "no", "nope"}
        }

        self.trek_data = self.load_json_data("trek_data.json")

    def load_json_data(self, filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Warning: '{filepath}' not found. Please ensure the file exists.")
            return {"places": [], "treks": {}}
        except json.JSONDecodeError:
            print(f"Warning: '{filepath}' contains invalid JSON.")
            return {"places": [], "treks": {}} 

  # def conversation_is_active(self):
  #     return self._is_active

    def tokenize(self, text):
        text = text.lower()
        text = text.translate(str.maketrans('', '', string.punctuation))
        words = text.split()
        return set([w for w in words if w not in self.stopwords])

    def jaccard_similarity(self, A, B):
        return len(A & B) / len(A | B) if len(A | B) != 0 else 0

    def classify_intent(self, tokens):
        best_intent = "planning"  
        highest_score = 0

        for intent, corpus in self.intents.items():
            score = self.jaccard_similarity(tokens, corpus)

            if score > highest_score:
                highest_score = score
                best_intent = intent

        return best_intent

    def extract_entities(self, text):
        original_text = text
        text = text.lower()

        treks_dict = self.trek_data.get("treks", {})

        for key in treks_dict.keys():
            search_term = key.replace('_', ' ') 
            if re.search(r"\b" + re.escape(search_term) + r"\b", text) or \
               re.search(r"\b" + re.escape(key) + r"\b", text):
                self.slots["destination"] = key
                break
        
        if not self.slots["destination"]:
            if re.search(r"\b(ebc)\b", text): self.slots["destination"] = "everest"
            elif re.search(r"\b(abc)\b", text): self.slots["destination"] = "annapurna"
        
        if not self.slots["destination"]:
            clean_text = re.sub(r"\b(i|want|to|plan|a|trek|go|for)\b", "", text).strip()
            is_duration = bool(re.search(r"(\d+)\s*(day|days|week|weeks)", text))
            is_difficulty = bool(re.search(r"\b(easy|moderate|hard)\b", text))
            
            if clean_text and len(clean_text.split()) <= 4 and not is_duration and not is_difficulty:
                if not any(w in clean_text for w in ["hi", "hello", "bye", "weather", "permit", "no", "nope"]):
                    self.slots["destination"] = clean_text.title()
                    
        match = re.search(r"(\d+)\s*(day|days|week|weeks)", text)
        if match:
            num = int(match.group(1))
            unit = match.group(2)
            if "week" in unit:
                num *= 7
            self.slots["duration"] = num

        if re.search(r"\b(easy|beginner)\b", text):
            self.slots["difficulty"] = "easy"
        elif re.search(r"\b(moderate|medium)\b", text):
            self.slots["difficulty"] = "moderate"
        elif re.search(r"\b(hard|expert|challenging)\b", text):
            self.slots["difficulty"] = "hard"

    def process_input(self, user_input):
        tokens = self.tokenize(user_input)
        intent = self.classify_intent(tokens)

        self.extract_entities(user_input)

        return {"intent": intent}
    
    def format_itinerary(self, itinerary_list):
        if not itinerary_list or not isinstance(itinerary_list, list):
            return "I am not able to give you day-by-day breakdown for this one this time, but it's an amazing place!"
        
        formatted_text = ""
        for day in itinerary_list:
            formatted_text += f"Day {day.get('day')}: {day.get('title')}\n"
            formatted_text += f"  - Altitude: {day.get('altitude')}\n"
            formatted_text += f"  - Walking Time: {day.get('walking_hours')}\n"
            formatted_text += f"  - Difficulty: {day.get('difficulty')}\n"
            formatted_text += f"  - Accommodation: {day.get('accommodation')}\n\n"
        
        return formatted_text.strip()

    def generate_response(self, processed_input):
        intent = processed_input["intent"]

        if intent == "exit":
            self._is_active = False
            return "Happy trails! I'll be right here whenever you're ready for your next adventure. Namaste!"

        if intent == "weather":
            return "For the clearest mountain views, I highly recommend Spring (March-May) or Autumn (September-November)!"

        if intent == "permit":
            return "You'll definitely need a TIMS card and the specific National Park permit. Don't worry, these are easy to arrange in Kathmandu, Pokhara or Chitwan."

        if not self.slots["destination"]:
            return "That sounds like an amazing idea! Which place are you dreaming of exploring? (e.g., Everest, Upper Mustang, Rara Lake...)"

        destination_display = self.slots['destination'].replace('_', ' ').title()

        if not self.slots["duration"]:
            return f"{destination_display} is a beautiful choice! How many days are you planning for this trip?"
        
        if not self.slots["difficulty"]:
            return "Got it! And what kind of challenge are you looking for? (Easy, Moderate, or Hard?)"
        
        destination = self.slots["destination"]
        duration = self.slots["duration"]
        difficulty = self.slots["difficulty"].title()

        treks_db = self.trek_data.get("treks", {})
        
        if destination not in treks_db:
            self.slots["destination"] = None
            return f"I am not able to give you a day-by-day breakdown for {destination_display} this time, but it's an amazing place! Could we try another one?"

        trek_info = treks_db[destination]

        if duration <= 5:
            itinerary_data = trek_info.get("short", [])
        else:
            itinerary_data = trek_info.get("long", trek_info.get("short", []))
        
        formatted_itinerary = self.format_itinerary(itinerary_data)

        print("\nGenerating your custom itinerary... Please wait", flush=True)
        time.sleep(2)
        response = f"""

Awesome! I've put together a custom plan for you:

     YOUR {destination_display.upper()} ADVENTURE
--------------------------------------------------
Destination : {destination.title()}
Duration    : {duration} Days
Difficulty  : {self.slots["difficulty"].title()}

Recommended Itinerary:
{formatted_itinerary}

--------------------------------------------------
Would you like to plan another one?
"""
        self.slots = {
            "destination": None,
            "duration": None,
            "difficulty": None
        }

        return response
    