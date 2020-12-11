import json

def pretty(d, indent=4):
    print(json.dumps(d, indent=indent))