import json
from pydantic import AnyUrl

class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, AnyUrl):
            return str(obj)
        return super().default(obj)