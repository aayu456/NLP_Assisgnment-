# Introduction to Artificial Intelligence(25/26)

## Student name: Aayusha KC
## Student number: 2319494
## Project title: NLP_Assisgnment
## Link to project video recording: 

# TrekSathi: Virtual Trekking Guide

TrekSathi is a Natural Language Processing (NLP) chatbot built in Python. It acts as a virtual travel agent to help users plan trekking adventures in Nepal. By chatting naturally with the user, TrekSathi extracts their preferences and generates a customized day-by-day itinerary based on real trekking data.

## Key Features
* **Dynamic Itinerary Generation:** Reads data dynamically from `trek_data.json`, meaning new treks can be added without changing the Python code.
* **Intent Recognition:** Uses tokenization, stop-word removal, and Jaccard Similarity to understand what the user is asking (e.g., planning a trip, asking for weather, checking permit requirements, or exiting).
* **Entity Extraction:** Uses Regular Expressions (Regex) to extract the **Destination** (e.g., "Everest", "Upper Mustang"), **Duration** (e.g., "5 days"), and **Difficulty** (e.g., "hard", "easy").
* **Conversational Flow:** Asks follow-up questions if missing information and handles graceful fallbacks if it doesn't recognize a destination.
* **Natural Delays:** Simulates a realistic "thinking" state while generating the final itinerary.

## Project Structure
* `chatbot_base.py` - The base template class (`ChatbotBase`) that defines the core interface and basic functions for the chatbot.
* `chatbot.py` - Contains the `TrekkingBot` class (which inherits from `ChatbotBase`). This file houses all the main NLP logic, intent classification, entity extraction, and response generation.
* `run_chatbot.py` - The main script containing the `TrekkingBot` class (which inherits from `ChatbotBase`) and the execution loop.
* `trek_data.json` - The database file containing the day-by-day breakdown of various trekking routes.

## How to Run the Project

**Prerequisites:**
You need Python 3.x installed on your computer. This project relies entirely on Python's built-in libraries (`re`, `string`, `json`, `time`), so no external installations (like `pip install`) are required!

**Execution:**
1. Open your terminal or command prompt.
2. Navigate to the folder containing your project files.
3. Run the following command:
   ```bash
   python run_chatbot.py

