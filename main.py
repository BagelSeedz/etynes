import discord
import os
from dotenv import load_dotenv

help_message = "Hi, I am evan's bot. Made by Bagel_Seedz."
bot = discord.Bot(help_message)

@bot.application_command()
async def test_evan(ctx):
    await ctx.respond("hi")

@bot.event
async def on_ready():
    print("Evan's bot is ready!")

load_dotenv()
token = os.getenv("TOKEN")

bot.run(token)