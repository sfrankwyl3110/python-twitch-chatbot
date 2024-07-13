import yarl
from typing import Annotated

from wyl import bot

# twitchio stuff
from twitchio import User
from twitchio.ext import commands

# bot-components
from wyl.converters import youtube_converter
from wyl.config import logger


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
