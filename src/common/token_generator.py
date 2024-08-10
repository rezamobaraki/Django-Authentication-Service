import base64
import random
import secrets
import time

from core.env import env

otp_length = env.int("AUTH_OTP_LENGTH", default=6)


def generate_otp() -> int:
    return random.randrange(10 ** otp_length, 10 ** (otp_length + 1) - 1)


def generate_token():
    token = secrets.token_hex(8)
    timestamp = str(int(time.time()))
    combined = f"{token}_{timestamp}"
    encoded_token = base64.b64encode(combined.encode()).decode()
    return encoded_token
