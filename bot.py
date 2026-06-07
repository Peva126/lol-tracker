import discord
import aiohttp
import asyncio
from datetime import datetime

# Configuration
DISCORD_TOKEN = "your-discord-token"
RIOT_API_KEY = "your-riot-api-key"
CHANNEL_ID = 0  # Your Discord channel ID

PLAYERS = [
    {"name": "player-name", "tag": "player-tag"},
    {"name": "player-name", "tag": "player-tag"},
]

REGION = "europe"
PLATFORM = "euw1"

QUEUE_TYPES = {
    420: "Ranked Solo/Duo",
    440: "Ranked Flex",
    400: "Normal Draft",
    430: "Normal Blind",
    450: "ARAM"
}

# Memory of notified matches
notified_matches = set()

# Discord bot setup
intents = discord.Intents.default()
client = discord.Client(intents=intents)


async def get_puuid(player):
    url = f"https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{player['name']}/{player['tag']}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers={"X-Riot-Token": RIOT_API_KEY}) as r:
            data = await r.json()
            return data["puuid"]


async def get_last_match(puuid):
    url = f"https://{REGION}.api.riotgames.com/l
