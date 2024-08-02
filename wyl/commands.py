import json
from datetime import datetime

import yarl
from typing import Annotated

from wyl import bot

# twitchio stuff
from twitchio import User
from twitchio.ext import commands

# bot-components
from wyl.converters import youtube_converter
from wyl.config import logger
from wyl.modules.helpers import get_dict_with_highest_key_value
from wyl.modules.location import get_lat_lon
from wyl.modules.weather import weather_dict_to_template_str, weather_location_to_csv_line, append_location_if_new, \
    get_weather


@bot.command(name="share")
async def share_command(
    ctx: commands.Context,
    url: Annotated[yarl.URL, youtube_converter],
    hype: int,
    *,
    comment: str
) -> None:
    hype_level = "hype" if 0 < hype < 5 else "very hype"
    logger.info(f"{ctx.author.name} wants to share a {hype_level} link on {url.host}: {comment}")
    await ctx.send(f"{ctx.author.name} wants to share a {hype_level} link on {url.host}: {comment}")


@bot.command(name="!yt")
async def share_command(
    ctx: commands.Context,
    url: Annotated[yarl.URL, youtube_converter],
    hype: int,
    *,
    comment: str
) -> None:
    hype_level = "hype" if 0 < hype < 5 else "very hype"
    logger.info(f"{ctx.author.name} wants to share a {hype_level} link on {url.host}: {comment}")
    await ctx.send(f"{ctx.author.name} wants to share a {hype_level} link on {url.host}: {comment}")


@bot.command(name="cookie", aliases=("cookies", "biscuits", "Cookie", "Cookies"))
async def cookie(ctx: commands.Context, amount: int = None, user: User = None) -> None:
    if user is None:
        if amount is None:
            logger.info(f"{ctx.author.name} gets a cookie!")
            await ctx.send(f"{ctx.author.name} gets a cookie!")
        else:
            logger.info(f"{ctx.author.name} gets {amount} cookies!")
            await ctx.send(f"{ctx.author.name} gets {amount} cookies!")
    else:
        logger.info(f"{user.name} gets {amount} cookies from {ctx.author.name}!")
        await ctx.send(f"{user.name} gets {amount} cookies from {ctx.author.name}!")

import requests

session = requests.session()


@bot.command(name="weather", aliases=("whatweather", "currentweather"))
async def cookie(ctx: commands.Context, message: str = None) -> None:
    city_lat_lon: list = get_lat_lon(message, requests_session=session)
    weather_template = "No weather-template content"
    highest_importance = get_dict_with_highest_key_value(city_lat_lon)
    if highest_importance is not None:
        lat, lon = highest_importance.get('lat'), highest_importance.get('lon')
        weather: dict = get_weather(lat, lon, requests_session=session)

        now = datetime.now()
        weather_line = f"query={message},time={now.timestamp()};weather={json.dumps(weather)}"
        with open("weather.csv", "a") as weather_csv:
            weather_csv.write(weather_line + "\n")
        current_place_id, csv_line_data = weather_location_to_csv_line(message, highest_importance)
        appended = append_location_if_new(message, current_place_id, csv_line_data)
        weather_template = weather_dict_to_template_str(weather)
    await ctx.send(f"weather for {message}: {weather_template}")
