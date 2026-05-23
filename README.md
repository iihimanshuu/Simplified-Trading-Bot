# Simplified Trading Bot

CLI tool to place **MARKET** and **LIMIT** orders on **Binance Futures Testnet** (fake funds only).

All code and setup instructions are in the [`trading_bot`](trading_bot/) folder.

```bash
cd trading_bot
pip install -r requirements.txt
copy .env.example .env
python -m bot.cli --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```
