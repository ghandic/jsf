import base64
import hashlib
import hmac
import json
import secrets
from datetime import timezone

from faker import Faker

faker = Faker()


def base64url_encode(input: bytes) -> str:
    return base64.urlsafe_b64encode(input).decode("utf-8").replace("=", "")


def jwt(api_key: str, expiry: int, api_sec: str) -> str:
    segments = []

    header = {"typ": "JWT", "alg": "HS256"}
    payload = {"iss": api_key, "exp": expiry}

    json_header = json.dumps(header, separators=(",", ":")).encode()
    json_payload = json.dumps(payload, separators=(",", ":")).encode()

    segments.append(base64url_encode(json_header))
    segments.append(base64url_encode(json_payload))

    signing_input = ".".join(segments).encode()
    key = api_sec.encode()
    signature = hmac.new(key, signing_input, hashlib.sha256).digest()

    segments.append(base64url_encode(signature))

    encoded_string = ".".join(segments)

    return encoded_string


def create_random_jwt(*args, **kwargs) -> str:
    api_key = secrets.token_urlsafe(16)
    api_sec = secrets.token_urlsafe(16)

    expiry = int(faker.date_time(timezone.utc).timestamp())

    return jwt(api_key, expiry, api_sec)
