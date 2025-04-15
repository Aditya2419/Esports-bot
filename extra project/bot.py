import discord
from discord.ext import commands
# Create intents
intents = discord.Intents.default()
intents.messages = True  # Enable message-related events (optional)
intents.guilds = True  # Enable guild-related events (optional)

# Create bot instance with intents
bot = commands.Bot(command_prefix="!", intents=intents)


# Event: Bot is ready
@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")

# Command: Test the bot
@bot.command()
async def ping(ctx):
    await ctx.send("Pong! I’m alive!")

# Run the bot with your token
bot.run("MTM0Nzk0NjQwNTM4NTM0MzEwOQ.GiKaSn.D9GLmgcBTceAdQLNBGqrtjWwhz_F29vcpL5zHc")  # Replace with your token from Step 2