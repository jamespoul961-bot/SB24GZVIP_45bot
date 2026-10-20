# SB24GZVIP_45bot

Telegram bot with sports, weather, time zones, promos, bonuses & fun tools.

## Features
- ⚽ Sports updates
- 🌤️ Weather by city
- 🕐 Time zone converter
- 🎁 Promos & daily bonus
- 💬 Quote / 😂 Joke / 🧠 Fact
- 🧮 Calculator
- 🆔 User info

## Deploy on Railway
1. Push this repo to GitHub
2. Create new Railway project → Deploy from GitHub
3. Add environment variable `BOT_TOKEN`
4. Railway runs `worker: python bot.py`

## Local run
```bash
pip install -r requirements.txt
export BOT_TOKEN=your_token
python bot.py
