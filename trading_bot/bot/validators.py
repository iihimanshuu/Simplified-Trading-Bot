class ValidationError(Exception):
    pass


VALID_SIDES = {"BUY", "SELL"}
VALID_ORDER_TYPES = {"MARKET", "LIMIT"}


def validate_symbol(symbol):
    if not symbol:
        raise ValidationError("Symbol is required.")
    cleaned = symbol.strip().upper()
    if len(cleaned) < 5:
        raise ValidationError("Symbol looks too short. Example: BTCUSDT")
    if not cleaned.isalnum():
        raise ValidationError("Symbol must contain only letters and numbers.")
    return cleaned


def validate_side(side):
    if not side:
        raise ValidationError("Side is required.")
    cleaned = side.strip().upper()
    if cleaned not in VALID_SIDES:
        raise ValidationError("Side must be BUY or SELL.")
    return cleaned


def validate_order_type(order_type):
    if not order_type:
        raise ValidationError("Order type is required.")
    cleaned = order_type.strip().upper()
    if cleaned not in VALID_ORDER_TYPES:
        raise ValidationError("Order type must be MARKET or LIMIT.")
    return cleaned


def validate_quantity(quantity):
    try:
        value = float(quantity)
    except (TypeError, ValueError):
        raise ValidationError("Quantity must be a valid number.")
    if value <= 0:
        raise ValidationError("Quantity must be greater than zero.")
    return value


def validate_price(price, order_type):
    cleaned_type = order_type.strip().upper()
    if cleaned_type == "MARKET":
        if price is not None:
            raise ValidationError("Price must not be used for MARKET orders.")
        return None
    if price is None:
        raise ValidationError("Price is required for LIMIT orders.")
    try:
        value = float(price)
    except (TypeError, ValueError):
        raise ValidationError("Price must be a valid number.")
    if value <= 0:
        raise ValidationError("Price must be greater than zero.")
    return value


def validate_order_inputs(symbol, side, order_type, quantity, price):
    clean_symbol = validate_symbol(symbol)
    clean_side = validate_side(side)
    clean_type = validate_order_type(order_type)
    clean_quantity = validate_quantity(quantity)
    clean_price = validate_price(price, clean_type)
    return {
        "symbol": clean_symbol,
        "side": clean_side,
        "type": clean_type,
        "quantity": clean_quantity,
        "price": clean_price,
    }
