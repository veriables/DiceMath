import json
from json import JSONEncoder

class CustomEncoder(json.JSONEncoder):
    def default(self, o):
            return o.__dict__