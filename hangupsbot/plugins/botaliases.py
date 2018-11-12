"""aliases for the bot"""
import logging

logger = logging.getLogger(__name__)


def _initialise(bot):
    """load in bot aliases from memory, create defaults if none"""

    if bot.config.exists(["bot.command_aliases"]):
        bot_command_aliases = bot.config.get("bot.command_aliases")

    if not isinstance(bot_command_aliases, list):
        bot_command_aliases = []

    if len(bot_command_aliases) == 0:
        bot.append("/bot")

    bot._handlers.bot_command = bot_command_aliases
    logger.info("aliases: {}".format(bot_command_aliases))

    return []
