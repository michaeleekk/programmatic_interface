import json
from importlib import resources

def load_json(path):
    with resources.open_text("cellenics_api", path) as raw_file:
        json_obj = json.load(raw_file)
    return json_obj
