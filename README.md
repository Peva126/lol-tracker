# LoL Match Tracker Bot 🎮

A Discord bot that monitors a League of Legends player and automatically sends a notification at the end of each match with detailed stats.

## Features

- Automatic notification at the end of each match
- Detailed stats: KDA, damage, CS, wards, vision score, towers, duration
- Champion icon in the embed
- Match date and time
- Automatic check every 5 minutes

## Tech Stack

- Python
- discord.py
- Riot Games API
- aiohttp

## Setup

1. Clone the repository
2. Install dependencies: `pip install discord.py aiohttp`
3. Create a Discord bot at [discord.com/developers](https://discord.com/developers)
4. Get an API key at [developer.riotgames.com](https://developer.riotgames.com)
5. Edit the variables in `bot.py`:
   - `DISCORD_TOKEN`
   - `RIOT_API_KEY`
   - `CHANNEL_ID`
   - `SUMMONER_NAME` and `SUMMONER_TAG`
6. Run the bot: `python bot.py`