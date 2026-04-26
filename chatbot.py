import re 
from chatbot_base import ChatbotBase

class TrekkingBot(ChatbotBase):
    def __init__(self, name="TrekSathi"):
        super().__init__(name=name)
        self.is_active = True

        self.slots = {
            "destination": None,
            "duration":None,
            "difficulty":None
        }
    def greeting(self):
        print(f"Namaste! I am {self.name}, your personal trekking planner.")
        print(f"I can help you building custom trekking itinerary in Nepal.")
    
    def farewell(self):
        print(f"\nThank You for using {self.name}. Have a safe and wonderful Journey.")

    def check_active(self):
        return self.is_active

    def process_input(self, user_input):
       
        text = user_input.lower()
        
        if any(word in text for word in ['quit', 'exit', 'bye', 'stop']):
            return {"intent": "exit"}

        if "permit" in text or "tims" in text:
            return {"intent": "general", "topic": "permit"}
        if "weather" in text or "best time" in text:
            return {"intent": "general", "topic": "weather"}

        extracted_data = {}
        
        destinations = ['everest', 'annapurna', 'langtang', 'manaslu']
        for dest in destinations:
            if dest in text:
                extracted_data['destination'] = dest.title()
        
        duration_match = re.search(r'(\d+)\s*day', text)
        if duration_match:
            extracted_data['duration'] = duration_match.group(1) + " days"

        difficulties = ['easy', 'beginner', 'moderate', 'hard', 'advanced']
        for diff in difficulties:
            if diff in text:
                extracted_data['difficulty'] = diff.title()

        return {"intent": "planning", "data": extracted_data}
    def generate_response(self, processed_input):

        intent = processed_input.get("intent")
        
        if intent == "exit":
            self.is_active = False
            return "Closing the planner..."

        if intent == "general":
            topic = processed_input.get("topic")
            if topic == "permit":
                return "Most treks in Nepal require a TIMS card and a National Park permit. Shall we start planning your route?"
            if topic == "weather":
                return "The best times to trek are Spring (March-May) and Autumn (Sept-Nov). Where do you want to go?"

        if intent == "planning":
            data = processed_input.get("data", {})
            
            for key, value in data.items():
                if value:
                    self.slots[key] = value

            if not self.slots["destination"]:
                return "Which region are you interested in? (e.g., Everest, Annapurna, Langtang, Manaslu)"
            
            elif not self.slots["duration"]:
                return f"Awesome, {self.slots['destination']} is beautiful! How many days do you have for the trek?"
            
            elif not self.slots["difficulty"]:
                return f"Got it, {self.slots['duration']} in {self.slots['destination']}. What difficulty level do you prefer? (Easy, Moderate, Hard)"
            
            else:
                final_plan = (
                    f"\nYour Custom Itinerary is Ready!\n"
                    f"Destination: {self.slots['destination']}\n"
                    f"Duration: {self.slots['duration']}\n"
                    f"Difficulty: {self.slots['difficulty']}\n\n"
                    f"Let me know if you want to plan another trip, or type 'exit' to leave."
                )
                
                self.slots = {"destination": None, "duration": None, "difficulty": None}
                return final_plan

        return "I didn't quite catch that. Could you tell me where you want to trek, or ask about permits/weather?"