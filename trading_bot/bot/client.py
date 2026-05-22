import hashlib
import hmac
import os
import time
from pathlib import Path
from urllib.parse import urlencode

import requests
from dotenv import load_dotenv

from bot.logging_config import setup_logging

ENV_FILE = Path(__file__).resolve().parent.parent / ".env"

BASE_URL = "https://testnet.binancefuture.com"
ORDER_PATH = "/fapi/v1/order"
RECV_WINDOW = 5000

logger = setup_logging()


class MissingCredentialsError(Exception):
    pass


class ApiError(Exception):
    def __init__(self, message, code=None):
        super().__init__(message)
        self.code = code


class NetworkError(Exception):
    pass


def load_credentials():
    load_dotenv(ENV_FILE)
    api_key = os.getenv("BINANCE_API_KEY", "").strip()
    api_secret = os.getenv("BINANCE_API_SECRET", "").strip()
    if not api_key or not api_secret:
        raise MissingCredentialsError(
            "API credentials are missing. Set BINANCE_API_KEY and BINANCE_API_SECRET in a .env file or environment variables."
        )
    return api_key, api_secret


def create_signature(query_string, secret_key):
    return hmac.new(
        secret_key.encode("utf-8"),
        query_string.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()


class FuturesClient:
    def __init__(self, api_key=None, api_secret=None):
        if api_key is None or api_secret is None:
            api_key, api_secret = load_credentials()
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = BASE_URL

    def place_order(self, params):
        signed_params = dict(params)
        signed_params["recvWindow"] = RECV_WINDOW
        signed_params["timestamp"] = int(time.time() * 1000)
        query_string = urlencode(signed_params)
        signature = create_signature(query_string, self.api_secret)
        signed_params["signature"] = signature
        url = f"{self.base_url}{ORDER_PATH}"
        headers = {"X-MBX-APIKEY": self.api_key}
        logger.info("API request | POST %s | params=%s", ORDER_PATH, signed_params)
        try:
            response = requests.post(url, headers=headers, params=signed_params, timeout=30)
        except requests.exceptions.Timeout:
            logger.error("Network error | request timed out")
            raise NetworkError("The request timed out. Check your internet connection and try again.")
        except requests.exceptions.ConnectionError:
            logger.error("Network error | connection failed")
            raise NetworkError("Could not connect to Binance Futures Testnet. Check your internet connection.")
        except requests.exceptions.RequestException as exc:
            logger.error("Network error | %s", exc)
            raise NetworkError(f"Network error: {exc}")
        logger.info("API response | status=%s | body=%s", response.status_code, response.text)
        return self._parse_response(response)

    def _parse_response(self, response):
        try:
            data = response.json()
        except ValueError:
            logger.error("API error | invalid JSON response")
            raise ApiError(f"Invalid response from server (HTTP {response.status_code}).")
        if response.status_code >= 400:
            code = data.get("code")
            message = data.get("msg", "Unknown API error")
            logger.error("API error | code=%s | message=%s", code, message)
            raise ApiError(message, code=code)
        return data
