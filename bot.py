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
    url = f"https://{REGION}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count=1"
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers={"X-Riot-Token": RIOT_API_KEY}) as r:
            data = await r.json()
            return data[0] if data else None


async def get_match_details(match_id, puuid):
    url = f"https://{REGION}.api.riotgames.com/lol/match/v5/matches/{match_id}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers={"X-Riot-Token": RIOT_API_KEY}) as r:
            data = await r.json()

            participants = data["info"]["participants"]
            player = next(p for p in participants if p["puuid"] == puuid)

            return {
                "win": player["win"],
                "champion": player["championName"],
                "kills": player["kills"],
                "deaths": player["deaths"],
                "assists": player["assists"],
                "damage": player["totalDamageDealtToChampions"],
                "duration": round(data["info"]["gameDuration"] / 60, 1),
                "cs": player["totalMinionsKilled"] + player["neutralMinionsKilled"],
                "wards_placed": player["wardsPlaced"],
                "vision_score": player["visionScore"],
                "towers": player["turretKills"],
                "date": data["info"]["gameStartTimestamp"],
                "queue": QUEUE_TYPES.get(data["info"]["queueId"], "Other")
            }


async def get_rank(puuid):
    url = f"https://{PLATFORM}.api.riotgames.com/lol/league/v4/entries/by-puuid/{puuid}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers={"X-Riot-Token": RIOT_API_KEY}) as r:
            data = await r.json()

            ranked = next((e for e in data if e["queueType"] == "RANKED_SOLO_5x5"), None)

            if ranked:
                return f"{ranked['tier']} {ranked['rank']} — {ranked['leaguePoints']} LP"
            else:
                return "Unranked"


async def send_notification(channel, details, match_id, rank, player):
    result = "✅ VICTORY" if details["win"] else "❌ DEFEAT"
    color = 0x00ff00 if details["win"] else 0xff0000
    icon_url = f"https://ddragon.leagueoflegends.com/cdn/14.24.1/img/champion/{details['champion']}.png"

    embed = discord.Embed(
        title=f"{result} — {details['champion']}",
        color=color
    )
    embed.set_author(name=f"{player['name']} #{player['tag']}")
    embed.set_thumbnail(url=icon_url)
    embed.add_field(name="Mode", value=details['queue'], inline=True)
    embed.add_field(name="KDA", value=f"{details['kills']}/{details['deaths']}/{details['assists']}", inline=True)
    embed.add_field(name="Damage", value=f"{details['damage']:,}", inline=True)
    embed.add_field(name="Duration", value=f"{details['duration']} min", inline=True)
    embed.add_field(name="CS", value=details['cs'], inline=True)
    embed.add_field(name="Wards", value=details['wards_placed'], inline=True)
    embed.add_field(name="Vision", value=details['vision_score'], inline=True)
    embed.add_field(name="Towers", value=details['towers'], inline=True)

    if details["queue"] in ["Ranked Solo/Duo", "Ranked Flex"]:
        embed.add_field(name="Rank", value=rank, inline=True)

    match_date = datetime.fromtimestamp(details['date'] / 1000).strftime("%d/%m/%Y %H:%M")
    embed.set_footer(text=f"Match ID: {match_id} · {match_date}")

    await channel.send(embed=embed)


async def check_matches():
    while True:
        for player in PLAYERS:
            try:
                puuid = await get_puuid(player)
                match_id = await get_last_match(puuid)

                if match_id and match_id not in notified_matches:
                    details = await get_match_details(match_id, puuid)
                    rank = await get_rank(puuid)
                    channel = client.get_channel(CHANNEL_ID)
                    await send_notification(channel, details, match_id, rank, player)
                    notified_matches.add(match_id)

            except Exception as e:
                print(f"Error: {e}")

        await asyncio.sleep(300)


@client.event
async def on_ready():
    print(f"Bot connected as {client.user}")
    asyncio.create_task(check_matches())


client.run(DISCORD_TOKEN)
