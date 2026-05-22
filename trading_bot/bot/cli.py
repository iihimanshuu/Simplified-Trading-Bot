import argparse
import sys

from bot.client import ApiError, MissingCredentialsError, NetworkError
from bot.logging_config import setup_logging
from bot.orders import place_order
from bot.validators import ValidationError

logger = setup_logging()


def build_parser():
    parser = argparse.ArgumentParser(
        description="Place MARKET or LIMIT orders on Binance Futures Testnet (USDT-M)."
    )
    parser.add_argument("--symbol", required=True, help="Trading pair, for example BTCUSDT")
    parser.add_argument("--side", required=True, help="BUY or SELL")
    parser.add_argument(
        "--type",
        required=True,
        dest="order_type",
        help="MARKET or LIMIT",
    )
    parser.add_argument("--quantity", required=True, help="Order quantity")
    parser.add_argument("--price", default=None, help="Limit price (required for LIMIT orders)")
    return parser


def print_order_summary(validated):
    print("\n--- Order Request Summary ---")
    print(f"Symbol:     {validated['symbol']}")
    print(f"Side:       {validated['side']}")
    print(f"Type:       {validated['type']}")
    print(f"Quantity:   {validated['quantity']}")
    if validated["type"] == "LIMIT":
        print(f"Price:      {validated['price']}")
    print("Environment: Binance Futures Testnet")
    print("-----------------------------\n")


def print_order_response(response):
    print("--- Order Response ---")
    order_id = response.get("orderId", "N/A")
    status = response.get("status", "N/A")
    executed_qty = response.get("executedQty", "N/A")
    avg_price = response.get("avgPrice", "N/A")
    print(f"Order ID:      {order_id}")
    print(f"Status:        {status}")
    print(f"Executed Qty:  {executed_qty}")
    print(f"Avg Price:     {avg_price}")
    print("----------------------\n")


def run(args):
    validated, response = place_order(
        symbol=args.symbol,
        side=args.side,
        order_type=args.order_type,
        quantity=args.quantity,
        price=args.price,
    )
    print_order_summary(validated)
    print_order_response(response)
    print("Order placed successfully.")
    logger.info(
        "Order success | symbol=%s side=%s type=%s orderId=%s",
        validated["symbol"],
        validated["side"],
        validated["type"],
        response.get("orderId"),
    )
    return 0


def main():
    parser = build_parser()
    args = parser.parse_args()
    try:
        return run(args)
    except ValidationError as exc:
        print(f"\nInput error: {exc}")
        logger.error("Validation error | %s", exc)
        return 1
    except MissingCredentialsError as exc:
        print(f"\nConfiguration error: {exc}")
        logger.error("Missing credentials | %s", exc)
        return 1
    except ApiError as exc:
        print(f"\nAPI error: {exc}")
        if exc.code is not None:
            print(f"Error code: {exc.code}")
        logger.error("API error | %s", exc)
        return 1
    except NetworkError as exc:
        print(f"\nNetwork error: {exc}")
        logger.error("Network error | %s", exc)
        return 1
    except Exception as exc:
        print(f"\nUnexpected error: {exc}")
        logger.error("Unexpected error | %s", exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())
