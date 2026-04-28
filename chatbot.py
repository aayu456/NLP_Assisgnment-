import re
import string
from chatbot_base import ChatbotBase


class TrekkingBot(ChatbotBase):

    def __init__(self, name="TrekSathi"):
        super().__init__(name=name)

        del self.conversation_is_active
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
            "exit": {"bye", "exit", "quit"}
        }

        self.itinerary_db = {
                "everest": {
                    "short": """
            Day 1: Fly to Lukla (2,860m) & Trek to Phakding (2,610m)
            - Duration: 3-4 hours
            - Highlights: Scenic mountain flight, Dudh Koshi river walk

            Day 2: Trek to Namche Bazaar (3,440m)
            - Duration: 6-7 hours
            - Highlights: Suspension bridges, first view of Everest

            Day 3: Acclimatization Day at Namche
            - Short hike to Everest View Hotel
            - Explore local markets and Sherpa culture

            Day 4: Trek back to Lukla
            - Duration: 6-7 hours
            - Descend through forests and villages

            Day 5: Fly back to Kathmandu
            - Morning flight with mountain views
            """,

                    "long": """
            Day 1: Fly to Lukla & Trek to Phakding
            Day 2: Trek to Namche Bazaar
            Day 3: Acclimatization Day
            Day 4: Trek to Tengboche
            Day 5: Trek to Dingboche
            Day 6: Acclimatization Day
            Day 7: Trek to Lobuche
            Day 8: Trek to Everest Base Camp
            Day 9: Return to Pheriche
            Day 10: Trek to Namche
            Day 11: Trek to Lukla
            Day 12: Fly to Kathmandu

            - Includes full Everest Base Camp experience
            - High altitude trekking preparation required
            """
                },

                "annapurna": {
                    "short": """
            Day 1: Drive to Nayapul & Trek to Tikhedhunga
            Day 2: Trek to Ghorepani
            Day 3: Sunrise hike to Poon Hill & Trek to Tadapani
            Day 4: Trek to Ghandruk
            Day 5: Return to Pokhara

            - Famous for sunrise view over Annapurna range
            - Moderate difficulty, beginner friendly
            """,

                    "long": """
            Day 1: Drive to Nayapul
            Day 2: Trek to Chhomrong
            Day 3: Trek to Bamboo
            Day 4: Trek to Deurali
            Day 5: Trek to Annapurna Base Camp
            Day 6: Explore ABC
            Day 7: Return trek
            Day 8-10: Exit via Jhinu Danda

            - Full Annapurna Base Camp experience
            - Includes hot springs at Jhinu
            """
                },

                "manaslu": {
                    "short": """
            Day 1: Drive to Soti Khola
            Day 2: Trek to Machha Khola
            Day 3: Trek to Jagat
            Day 4: Trek back
            Day 5: Return drive

            - Remote and less crowded trail
            - Cultural villages and river valleys
            """,

                    "long": """
            Day 1: Drive to Soti Khola
            Day 2-6: Trek through Jagat, Deng, Namrung
            Day 7: Reach Samagaon
            Day 8: Acclimatization
            Day 9: Trek to Samdo
            Day 10: Cross Larke Pass (5,160m)
            Day 11-14: Descend and exit via Dharapani

            - One of Nepal’s best off-the-beaten-path treks
            - High altitude and physically demanding
            """
    }
}

    def conversation_is_active(self):
        return self._is_active


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
        text = text.lower()

        if re.search(r"\b(everest|ebc)\b", text):
            self.slots["destination"] = "everest"

        elif re.search(r"\b(annapurna|abc)\b", text):
            self.slots["destination"] = "annapurna"

        elif re.search(r"\b(manaslu)\b", text):
            self.slots["destination"] = "manaslu"

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

        elif re.search(r"\b(hard|expert)\b", text):
            self.slots["difficulty"] = "hard"

    def process_input(self, user_input):
        tokens = self.tokenize(user_input)
        intent = self.classify_intent(tokens)

        self.extract_entities(user_input)

        return {"intent": intent}

    def generate_response(self, processed_input):
        intent = processed_input["intent"]

        if intent == "exit":
            self._is_active = False
            return "Ending session..."

        if not self.slots["destination"]:
            return "Please choose destination (Everest, Annapurna, Manaslu)."

        if not self.slots["duration"]:
            return f"{self.slots['destination'].title()} selected. How many days?"

        if not self.slots["difficulty"]:
            return "Preferred difficulty? (easy/moderate/hard)"

        if intent == "weather":
            return "Best seasons: Spring (Mar-May) and Autumn (Sep-Nov)."

        if intent == "permit":
            return "You need TIMS card and National Park permit."

        destination = self.slots["destination"]
        duration = self.slots["duration"]

        if duration < 7:
            itinerary = self.itinerary_db[destination]["short"]
        else:
            itinerary = self.itinerary_db[destination]["long"]

        response = f"""

        TREKSATHI TREKKING PLAN
--------------------------------------------------
Destination : {destination.title()}
Duration    : {duration} Days
Difficulty  : {self.slots["difficulty"].title()}

Recommended Itinerary:
{itinerary}

--------------------------------------------------
"""
        self.slots = {
            "destination": None,
            "duration": None,
            "difficulty": None
        }

        return response