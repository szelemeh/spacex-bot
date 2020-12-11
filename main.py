import pyowm
from constants import *
import os
import json
import flask

owm = pyowm.OWM(api_key=open_weather_api)
manager = owm.weather_manager()

app = flask.Flask(__name__)


def can_launch_rocket(location):
    a = 'Krakow,PL'
    observation = manager.weather_at_place(location)
    w = observation.to_dict()
    print("\n".join("{}\t{}".format(k, v) for k, v in w.items()))
    return observation.weather.clouds < 75


@app.route('/webhook', methods=['POST'])
def webhook():
    req = flask.request.get_json(silent=True, force=True)
    print(f"Request {json.dumps(req, indent=4)}")
    res = make_webhook_result(req)
    res = json.dumps(res, indent=4)
    print(res)
    r = flask.make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def make_city_suitability_result(request):
    result = request.get("queryResult")
    parameters = result.get("parameters")
    location = parameters.get("location")["city"] + "," + parameters.get("location")["country"]
    can_launch = can_launch_rocket(location)
    speech = f"Niestety nie uda się wystrzelić rakietę w {location}"
    if can_launch:
        speech = f"Tak! Możesz teraz wystrzelić rakietę w {location}"
    print(f"Response: {speech}")
    return {
        "fulfillmentMessages": [
            {
                "text": {
                    "text": [
                        speech
                    ]
                }
            }
        ]
    }


def make_webhook_result(request):
    if request['queryResult']['intent']['name'] == city_suitability_intent:
        return make_city_suitability_result(request)
    else:
        return {}


if __name__ == '__main__':
    port = int(os.getenv('PORT', 1234))
    app.run(debug=True, port=port, host="0.0.0.0")
