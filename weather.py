import pyowm

from constants import open_weather_api

owm = pyowm.OWM(api_key=open_weather_api)
manager = owm.weather_manager()


def can_launch_rocket(location):
    observation = manager.weather_at_place(location)
    w = observation.to_dict()
    print("\n".join("{}\t{}".format(k, v) for k, v in w.items()))
    return observation.weather.clouds < 75