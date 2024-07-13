import os
from wyl.config import logger
from twitchio.ext import commands
from dotenv import load_dotenv

load_dotenv('.env')

client_id = os.getenv('TWITCH_CLIENT_ID')
refresh_token = os.getenv('TWITCH_REFRESH_TOKEN')
access_token = os.getenv('TWITCH_ACCESS_TOKEN')


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(token=access_token, prefix='!', initial_channels=['itz_izzeeeey'])

    async def event_command_error(self, context: commands.Context, error: Exception):
        if isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, commands.ArgumentParsingFailed):
            await context.send(error.message)
        else:
            logger.error(error)

    async def event_ready(self):
        logger.debug(f'Logged in as | {self.nick}')
        logger.debug(f'User id is | {self.user_id}')

    async def event_message(self, message):
        if message.echo:
            return

        logger.info(f"message ({message.author.name}): {message.channel.name}: {message.content}")
        await self.handle_commands(message)

    @commands.command()
    async def command_list(self, ctx: commands.Context):
        await ctx.send(f'Current Commands: !hello (Greets the User)')
