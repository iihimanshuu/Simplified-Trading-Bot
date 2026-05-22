# Trading Bot (Binance Futures Testnet)

Places **MARKET** and **LIMIT** orders on Binance Futures Testnet. Uses fake money only — not live trading.

## What it does

- **BUY** / **SELL**
- **MARKET** / **LIMIT** orders (LIMIT needs `--price`)
- Checks your input before calling the API
- Prints order summary and response in the terminal
- Writes requests, responses, and errors to `logs/trading_bot.log`

## Requirements

- Python 3.8+
- [Binance Futures Testnet](https://testnet.binancefuture.com/) account and API key

## Setup

```bash
cd trading_bot
python -m venv venv
```

Windows:

```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```

Edit `.env`:

```
BINANCE_API_KEY=your_testnet_key
BINANCE_API_SECRET=your_testnet_secret
```

Do not commit `.env`.

## Run

From the `trading_bot` folder:

```bash
python -m bot.cli --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
python -m bot.cli --symbol BTCUSDT --side BUY --type LIMIT --quantity 0.001 --price 45000
```

| Option | Required | Notes |
|--------|----------|--------|
| `--symbol` | Yes | e.g. `BTCUSDT` |
| `--side` | Yes | `BUY` or `SELL` |
| `--type` | Yes | `MARKET` or `LIMIT` |
| `--quantity` | Yes | Number |
| `--price` | LIMIT only | Omit for MARKET |

## Project layout

```
trading_bot/
  bot/           client, orders, validators, cli
  logs/          trading_bot.log (created on run)
  .env.example
  requirements.txt
```

## Common issues

| Error | Fix |
|-------|-----|
| Missing credentials | Create `.env` with both keys |
| Invalid API key | Use testnet keys from testnet.binancefuture.com |
| Insufficient margin | Add testnet balance or lower quantity |
| Price required / not allowed | Add `--price` for LIMIT; remove it for MARKET |
| `ModuleNotFoundError: bot` | Run commands inside `trading_bot` |

## Logs

`trading_bot/logs/trading_bot.log` — API requests, responses, and errors (secrets are not logged).
