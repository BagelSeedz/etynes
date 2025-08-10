import discord
import os
import requests
from dotenv import load_dotenv
import json
from datetime import datetime, timezone
import time
import asyncio

load_dotenv()

help_message = "Hi, I am evan's bot. Made by Bagel_Seedz."
bot = discord.Bot(help_message)

def get_latest_video_link(api_key: str, channel_ids: dict) -> str | None:
    """
    Returns the URL of the most recently uploaded video.
    """
    latest_time = None
    latest_link = None

    for channel_id in channel_ids.values():
        search_url = "https://www.googleapis.com/youtube/v3/search"
        params = {
            "key": api_key,
            "channelId": channel_id,
            "part": "snippet",
            "order": "date",
            "maxResults": 1,
            "type": "video",
            "fields": (
                "items(id/videoId,"
                "snippet/title,"
                "snippet/publishedAt,"
                "snippet/description,"
                "snippet/thumbnails/default/url)"
            )
        }

        resp = requests.get(search_url, params=params)
        resp.raise_for_status()
        data = resp.json()
        
        items = data.get("items")
        if not items:
            print("No videos found on this channel.")
            continue

        # Parse into a timezone-aware datetime object in UTC
        published_dt = datetime.strptime(items[0]["snippet"]["publishedAt"], "%Y-%m-%dT%H:%M:%SZ")
        published_dt = published_dt.replace(tzinfo=timezone.utc)

        if not latest_time:
            latest_time = published_dt
            video_id = items[0]["id"]["videoId"]
            latest_link = f"https://www.youtube.com/watch?v={video_id}"
        elif latest_time < published_dt:
            latest_time = published_dt
            video_id = items[0]["id"]["videoId"]
            latest_link = f"https://www.youtube.com/watch?v={video_id}"

    return latest_link

        

@bot.application_command()
async def test_evan(ctx):
    await ctx.respond("hi")

@bot.event
async def on_ready():
    print("Evan's bot is ready!")

async def detect_uploads():
    while True:
        with open("settings.json") as settingsFile:
            settings = json.load(settingsFile)
            channels = settings['channels']
            link = get_latest_video_link(os.getenv("YOUTUBE_API_KEY"), channels)
            print(link)
        
        await asyncio.sleep(60) # Check for uploads every minute

if __name__ == "__main__":
    bot.loop.create_task(detect_uploads())

    token = os.getenv("BOT_TOKEN")
    bot.run(token)