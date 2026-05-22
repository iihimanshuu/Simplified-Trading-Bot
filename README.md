# Simplified Trading Bot

Small Python application that places orders on **Binance Futures Testnet (USDT-M)**.

The full project lives in the [`trading_bot`](trading_bot/) folder. See [`trading_bot/README.md`](trading_bot/README.md) for setup, configuration, and usage.

Quick start:

```bash
cd trading_bot
python -m venv venv
pip install -r requirements.txt
copy .env.example .env
python -m bot.cli --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```
