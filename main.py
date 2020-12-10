import pyowm
from keys import open_weather_api
import os
import json
import flask

owm = pyowm.OWM(api_key=open_weather_api)
manager = owm.weather_manager()

app = flask.Flask(__name__)

def can_launch_rocket(city):
    observation = manager.weather_at_place(city)
    w = observation.to_dict()
    print("\n".join("{}\t{}".format(k, v) for k, v in w.items()))
    return observation["weather"]["clouds"] < 75

@app.route('/webhook', methods=['POST'])
def webhook():
    req = flask.request.get_json(silent=True, force=True)
    print(f"Request {json.dumps(req, indent=4)}")
    res = makeWebhookResult(req)
    res = json.dumps(res, indent=4)
    print(res)
    r = flask.make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):
    if req.get("result").get("action") != "interest":
        return {}
    result = req.get("result")
    parameters = result.get("parameters")
    city = parameters.get("city-name")
    can_launch = can_launch_rocket(city)
    speech = f"Niestety nie uda się wystrzelić rakietę w {city}"
    if can_launch:
        speech = f"Tak! Możesz teraz wystrzelić rakietę w {city}"
    print(f"Response: {speech}")
    return {
        "speech": speech,
        "displayText": speech,
        "source": "Here"
    }



if __name__ == '__main__':
    port = int(os.getenv('PORT', 1345))
    app.run(debug=True, port=port, host="0.0.0.0")