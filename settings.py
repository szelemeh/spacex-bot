import os

from dotenv import load_dotenv
load_dotenv()

open_weather_api = os.getenv("OPEN_WEATHER_API")
city_suitability_intent = "projects/spacex-bot-296810/agent/intents/bd703993-fb92-4989-914e-188e75aedce5"
last_launch_url_intent = "projects/spacex-bot-296810/agent/intents/66111d88-8ec7-41aa-ad72-8d5bec56f4ac"
