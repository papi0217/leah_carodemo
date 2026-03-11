# LEAH Concierge Demo Bot

A production-ready Telegram bot that demonstrates the LEAH AI concierge system using Groq API and real-time weather data.

## Overview

This bot simulates how LEAH assists luxury properties with guest services:
- Instant property information (WiFi, amenities, check-in/out)
- Restaurant recommendations
- Local attractions and activities
- Real-time weather information
- Emergency support

## Features

✅ **Groq API Integration** — Uses mixtral-8x7b-32768 for intelligent responses  
✅ **Weather API** — Real-time weather data for guest queries  
✅ **World-Class Demo Flow** — Guided experience with value commentary  
✅ **Sales Pivot** — Automatic transition to sales pitch after 5 messages  
✅ **Session Management** — Automatic cleanup and conversation history  
✅ **Error Handling** — Graceful fallbacks and user-friendly messages  
✅ **Comprehensive Logging** — Full audit trail for debugging  
✅ **Production Ready** — Clean architecture, tested, deployable  

## Quick Start

### 1. Get Your Credentials

**Telegram Bot Token:**
- Open Telegram
- Search for @BotFather
- Send `/newbot`
- Follow prompts, copy the token

**Groq API Key:**
- Go to https://console.groq.com
- Create account/login
- Go to API Keys
- Create new key

**Weather API Key (Optional):**
- Go to https://openweathermap.org/api
- Create account/login
- Get your API key

### 2. Install

```bash
git clone https://github.com/papi0217/leah_carodemo.git
cd leah_carodemo
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure

```bash
cp .env.example .env
nano .env  # Edit with your credentials
```

Add your credentials:
```
TELEGRAM_BOT_TOKEN=your_token_here
GROQ_API_KEY=your_groq_key_here
WEATHER_API_KEY=your_weather_key_here
BOT_ID=leah_carodemo_bot
```

### 4. Run

```bash
python bot/main.py
```

You'll see:
```
Starting LEAH Concierge Demo Bot
Bot is ready to accept messages
```

## Test the Bot

On Telegram:
1. Search for your bot username
2. Click `/start`
3. Chat naturally

**Try these:**
- "What's the WiFi password?"
- "Best restaurants nearby?"
- "What's the weather?"
- "What attractions should I visit?"

## Commands

- `/start` - Start the demo
- `/help` - Get help
- `/reset` - Reset conversation
- `/status` - Check session

## Architecture

```
bot/
  main.py       - Entry point
  handlers.py   - Message handlers

services/
  ai_service.py - Groq API + Weather API integration

config/
  settings.py   - Configuration
```

## How It Works

1. **User starts bot** → Welcome message with guided questions
2. **User asks questions** → Groq API generates intelligent responses
3. **Weather queries** → Real-time weather data fetched and included
4. **After 5 messages** → Sales pivot triggered
5. **Value commentary** → Meta-commentary highlights business benefits

## Logs

View bot activity:
```bash
tail -f leah_bot.log
```

## Stop the Bot

Press `Ctrl+C` in the terminal

## Troubleshooting

**Bot not responding:**
```bash
ps aux | grep python
tail -f leah_bot.log
```

**API errors:**
- Check `.env` credentials
- Verify internet connection
- Check Groq API status

**Timeout:**
- Increase `RESPONSE_TIMEOUT` in `config/settings.py`

## That's It

The bot is ready to demonstrate LEAH to potential clients.
