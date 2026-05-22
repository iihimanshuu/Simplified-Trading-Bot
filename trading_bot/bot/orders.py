from bot.client import FuturesClient
from bot.validators import validate_order_inputs


def build_order_params(validated):
    params = {
        "symbol": validated["symbol"],
        "side": validated["side"],
        "type": validated["type"],
        "quantity": validated["quantity"],
    }
    if validated["type"] == "LIMIT":
        params["price"] = validated["price"]
        params["timeInForce"] = "GTC"
    return params


def place_order(symbol, side, order_type, quantity, price=None, client=None):
    validated = validate_order_inputs(symbol, side, order_type, quantity, price)
    params = build_order_params(validated)
    if client is None:
        client = FuturesClient()
    response = client.place_order(params)
    return validated, response
