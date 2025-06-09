# app/utils/json_encoder.py

from decimal import Decimal
from flask.json.provider import DefaultJSONProvider

class CustomJSONProvider(DefaultJSONProvider):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)  # Converte Decimal → float
        return super().default(obj)