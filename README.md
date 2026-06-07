# LoL Match Tracker Bot 🎮

A Discord bot that monitors multiple League of Legends players and automatically sends a notification at the end of each match with detailed stats.

## Features

- Monitor multiple players simultaneously
- Automatic notification at the end of each match
- Detailed stats: KDA, damage, CS, wards, vision score, towers, duration
- Shows game mode (Ranked Solo/Duo, Ranked Flex, Normal, ARAM)
- Shows current rank only for ranked games
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
   - `DISCORD_TOKEN` — your Discord bot token
   - `RIOT_API_KEY` — your Riot Games API key (expires every 24h)
   - `CHANNEL_ID` — your Discord channel ID
   - `PLAYERS` — list of players to monitor
6. Run the bot: `python bot.py`

## Notes

- The Riot Games development API key expires every 24 hours and needs to be renewed
- Add as many players as you want in the `PLAYERS` list
- Each player gets an individual notification as soon as their match ends
