# Auto-post daily matches
import discord
from discord.ext import commands
import requests
import asyncio
from dotenv import load_dotenv
import os
from datetime import datetime
import pytz

# Load environment variablescle
load_dotenv()
PANDASCORE_TOKEN = os.getenv("PANDASCORE_TOKEN")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
# print(f"PANDASCORE_TOKEN: {PANDASCORE_TOKEN}")
# print(f"DISCORD_TOKEN: {DISCORD_TOKEN}")
PANDASCORE_URL = "https://api.pandascore.co/matches/upcoming"
HEADERS = {"Authorization": f"Bearer {PANDASCORE_TOKEN}"}

# Discord bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Timezone conversion
def convert_utc_to_local(utc_time, timezone="US/Pacific"):
    try:
        utc_dt = datetime.strptime(utc_time, "%Y-%m-%dT%H:%M:%SZ")
        utc_dt = pytz.utc.localize(utc_dt)
        local_dt = utc_dt.astimezone(pytz.timezone(timezone))
        return local_dt.strftime("%Y-%m-%d at %H:%M %Z")
    except Exception as e:
        print(f"Timezone error: {e}")
        return utc_time[:10] + " (UTC)"

# Auto-post daily matches
async def post_daily_matches():
    while True:
        channel = bot.get_channel(1361641234803855373)
        if channel:
            for game in ["league-of-legends", "valorant"]:
                try:
                    response = requests.get(
                        PANDASCORE_URL,
                        headers=HEADERS,
                        params={
                            "filter[videogame]": game,
                            "page[size]": 3,
                            "range[begin_at]": "2025-04-01,2025-12-31"
                        }
                    )
                    print(f"Auto-post {game}: {response.status_code}, {response.text}")
                    if response.status_code == 200:
                        matches = response.json()
                        if matches:
                            await channel.send(f"📢 Upcoming {game.upper()} matches:")
                            for match in matches:
                                local_time = convert_utc_to_local(match["scheduled_at"])
                                await channel.send(f"**{match['name']}** | {match['tournament']['name']} | Starts: {local_time}")
                        else:
                            await channel.send(f"No upcoming {game.upper()} matches found!")
                    else:
                        await channel.send(f"Error fetching {game} matches: {response.status_code}")
                except Exception as e:
                    await channel.send(f"Oops, broke for {game}: {str(e)}")
        await asyncio.sleep(86400)  # 24 hours

@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")
    bot.loop.create_task(post_daily_matches())

@bot.command()
async def ping(ctx):
    await ctx.send("Pong! I’m alive!")

@bot.command()
async def matches(ctx, game="valorant"):
    try:
        valid_games = {"valorant": "valorant", "lol": "league-of-legends", "cs2": "cs2", "dota2": "dota2"}
        if game.lower() not in valid_games:
            await ctx.send(f"Invalid game! Try: {', '.join(valid_games.keys())}")
            return
        response = requests.get(
            PANDASCORE_URL,
            headers=HEADERS,
            params={
                "filter[videogame]": valid_games[game.lower()],
                "page[size]": 5,
                "range[begin_at]": "2025-04-01,2025-12-31"
            }
        )
        print(f"Matches {game}: {response.status_code}, {response.text}")
        if response.status_code == 200:
            matches = response.json()
            if matches:
                for match in matches:
                    name = match["name"]
                    tournament = match["tournament"]["name"]
                    local_time = convert_utc_to_local(match["scheduled_at"])
                    await ctx.send(f"🎮 **{name}** | {tournament} | 🕒 {local_time} | Get hyped! 🚀")
            else:
                await ctx.send(f"No upcoming {game} matches found! Try later or check tournaments.")
        else:
            await ctx.send(f"Error fetching matches: {response.status_code}")
    except Exception as e:
        await ctx.send(f"Oops, something broke: {str(e)}")

@bot.command()
async def tournaments(ctx, game="valorant"):
    try:
        valid_games = {"valorant": "valorant", "lol": "league-of-legends", "cs2": "cs2", "dota2": "dota2"}
        if game.lower() not in valid_games:
            await ctx.send(f"Invalid game! Try: {', '.join(valid_games.keys())}")
            return
        response = requests.get(
            f"https://api.pandascore.co/{valid_games[game.lower()]}/tournaments",
            headers=HEADERS,
            params={"page[size]": 5}
        )
        print(f"Tournaments {game}: {response.status_code}, {response.text}")
        if response.status_code == 200:
            tournaments = response.json()
            if tournaments:
                for t in tournaments:
                    await ctx.send(f"🏆 {t['name']} | League: {t.get('league', {}).get('name', 'N/A')}")
            else:
                await ctx.send(f"No {game} tournaments found!")
        else:
            await ctx.send(f"Error fetching tournaments: {response.status_code}")
    except Exception as e:
        await ctx.send(f"Oops, something broke: {str(e)}")

    
@bot.command()
async def hype(ctx, *, query):
    await ctx.send(f"Checking X for hype on '{query}'... One sec!")
    await ctx.send(f"X is buzzing for {query}! Fans are hyped—check back for more!")  # Replace with my real analysis
bot.run(DISCORD_TOKEN)  # Your Discord token