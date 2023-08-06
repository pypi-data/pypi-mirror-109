import base64
import json
from datetime import datetime


def get_expiry_date(token: str) -> datetime:
    """Get the expiration datetime from the given token

    Args:
        token (str): The JSONWebToken

    Returns:
        datetime: The datetime the token expires
    """
    parts = token.split(".")
    payload_str = base64.standard_b64decode(parts[1] + "==").decode('ascii')
    payload = json.loads(payload_str)
    time = datetime.fromtimestamp(payload["exp"])
    return time
