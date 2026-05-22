# Simplified Trading Bot (Binance Futures Testnet)

A small Python project that places **MARKET** and **LIMIT** orders on **Binance Futures Testnet (USDT-M)**. It is built for learning, demos, and junior internship portfolios. The code is modular, readable, and uses direct REST API calls with HMAC signing.

This bot only talks to the testnet. It does not place real-money orders on mainnet.

---

## Project Overview

You run a single command from the terminal with your order details (symbol, side, type, quantity, and price for limit orders). The app validates your input, signs the request with your API secret, sends it to Binance Futures Testnet, prints a clear summary in the terminal, and writes request/response details to a log file.

### Features

- Place **MARKET** and **LIMIT** orders
- Support **BUY** and **SELL** sides
- CLI input with **argparse**
- Input validation before any API call
- Error handling for invalid input, missing credentials, API errors, and network errors
- File logging for API requests, responses, and errors
- Credentials from a `.env` file or environment variables
- Testnet-only base URL: `https://testnet.binancefuture.com`

---

## Requirements

- Python 3.8 or newer
- A Binance Futures Testnet account
- Testnet API key and secret (from the testnet website)
- Internet connection

---

## Project Structure

```
trading_bot/
  bot/
    __init__.py
    client.py          API client and signing
    orders.py          Order building and placement
    validators.py      Input validation
    logging_config.py  Log file setup
    cli.py             Command-line interface
  logs/
    trading_bot.log    Created when you run the app
  .env.example         Sample credentials file
  requirements.txt
  README.md
```

---

## Setup Steps

### 1. Clone or download the project

Open a terminal in the `trading_bot` folder (the folder that contains `bot/` and `requirements.txt`).

### 2. Create a virtual environment (recommended)

**Windows (PowerShell):**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Configure API Credentials

1. Go to [Binance Futures Testnet](https://testnet.binancefuture.com/) and log in.
2. Create or copy your **API Key** and **Secret Key** for futures testnet trading.
3. Copy `.env.example` to `.env` in the `trading_bot` folder:

```bash
copy .env.example .env
```

On macOS/Linux:

```bash
cp .env.example .env
```

4. Edit `.env` and paste your keys:

```
BINANCE_API_KEY=your_actual_testnet_key
BINANCE_API_SECRET=your_actual_testnet_secret
```

Never commit `.env` to GitHub. The `.gitignore` file already excludes it.

You can also set `BINANCE_API_KEY` and `BINANCE_API_SECRET` as system environment variables instead of using a `.env` file.

---

## How to Run the App

From the `trading_bot` directory (with your virtual environment activated):

```bash
python -m bot.cli --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

```bash
python -m bot.cli --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 50000
```

### CLI Arguments

| Argument     | Required | Description                          |
|-------------|----------|--------------------------------------|
| `--symbol`  | Yes      | Pair, e.g. `BTCUSDT`                 |
| `--side`    | Yes      | `BUY` or `SELL`                      |
| `--type`    | Yes      | `MARKET` or `LIMIT`                  |
| `--quantity`| Yes      | Order size (number)                  |
| `--price`   | LIMIT only | Limit price (do not use for MARKET) |

---

## Example Commands

**Market buy:**

```bash
python -m bot.cli --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

**Market sell:**

```bash
python -m bot.cli --symbol BTCUSDT --side SELL --type MARKET --quantity 0.001
```

**Limit buy:**

```bash
python -m bot.cli --symbol BTCUSDT --side BUY --type LIMIT --quantity 0.001 --price 45000
```

**Limit sell:**

```bash
python -m bot.cli --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.01 --price 3500
```

---

## Assumptions

- You use **one-way position mode** (default on testnet). The bot does not send `positionSide` unless you extend it later.
- **LIMIT** orders use `timeInForce=GTC` (good till cancelled).
- Quantity and price are passed as numbers; the API receives them in the signed request.
- Symbol names are uppercase (the app converts input to uppercase).
- You have enough testnet balance and meet minimum order size rules for your symbol.
- Orders are sent only to `https://testnet.binancefuture.com` (hardcoded in the client).

---

## Binance Futures Testnet Notes

- Testnet funds are fake. Use testnet for practice only.
- Testnet API keys are separate from your live Binance account keys.
- Register and manage keys at [https://testnet.binancefuture.com](https://testnet.binancefuture.com).
- Binance may update testnet URLs or rules over time. If orders fail with connection or endpoint errors, check the latest [Binance Futures API documentation](https://developers.binance.com/docs/derivatives/usds-margined-futures/general-info).
- Rate limits and minimum order sizes still apply on testnet.

---

## Troubleshooting

| Problem | What to try |
|--------|-------------|
| `API credentials are missing` | Create `.env` from `.env.example` and set both keys, or set environment variables. |
| `Invalid API-key` or `-2015` | Use futures **testnet** keys, not mainnet keys. |
| `Insufficient margin` | Add testnet funds or reduce quantity. |
| `MIN_NOTIONAL` or quantity errors | Increase quantity or check symbol rules on testnet. |
| `Price is required for LIMIT` | Add `--price` for limit orders. |
| `Price must not be used for MARKET` | Remove `--price` for market orders. |
| Connection / timeout errors | Check internet, firewall, and that testnet is online. |
| `ModuleNotFoundError: bot` | Run commands from the `trading_bot` folder, not the repo root. |
| Import errors for `requests` | Run `pip install -r requirements.txt` inside your virtual environment. |

---

## Log File

When you run the bot, logs are written to:

```
trading_bot/logs/trading_bot.log
```

Each line includes a timestamp, log level, and message. The log records:

- Outgoing API requests (endpoint and parameters; secrets are never logged)
- API responses (status and body)
- Validation, network, API, and unexpected errors

Use this file to debug issues without exposing keys in the terminal.

---

## Security Reminders

- Do not share your API secret.
- Do not commit `.env` to version control.
- Restrict API key permissions to what you need for testing.
- This project is for education and testnet use only.

---

## License

See the repository root `LICENSE` file if present.
