"""
Plugin to lookup words from Oxford Dictionaries

instructions:
* pip3 install oxforddictionaries
* get API KEY and APP ID from the OD website
* put API KEY and APP ID in config.json
"""

from oxforddictionaries.words import OxfordDictionaries
import plugins
import logging

logger = logging.getLogger(__name__)

_internal = {}

def _initialise(bot):
    appid = bot.get_config_option("oxforddict-appid")
    apikey = bot.get_config_option("oxforddict-apikey")
    if appid and apikey:
        _internal["client"] = OxfordDictionaries(appid, apikey)
        plugins.register_user_command(["define", "synonym", "antonym"])
    else:
        logger.error('Dictionary: config["oxforddict-appid"] and config["oxforddict-apikey"] required')


def _entry_format(entry):
    nice_domains = None
    if entry.get('domains'):
        domains = ', '.join(entry.get('domains', ''))
        nice_domains = '(%s)' % domains

    definition = entry['definitions'][0].capitalize()

    if nice_domains:
        return "%s %s" % (nice_domains, definition)
    else:
        return definition


def define(bot, event, *args):
    """request data from oxford dict"""

    if not len(args):
        yield from bot.coro_send_message(event.conv,
                                         _("You need to ask Dictionary a question"))
        return

    keyword = ' '.join(args)
    info = _internal["client"].get_info_about_word(keyword)

    if info.status_code == 404:
        yield from bot.coro_send_message(event.conv,
                                         _("The definition for %s was not found" % keyword))
        return

    val = info.json()['results'][0]

    word = val['word']
    lexical_category = val['lexicalEntries'][0]['lexicalCategory']
    entries = val['lexicalEntries'][0]['entries'][0]['senses']
    definitions = [_entry_format(entry) for entry in entries if entry.get('definitions') is not None]

    html = '<b>{}</b> ({})'.format(word.capitalize(), lexical_category.capitalize())
    for idx, definition in enumerate(definitions):
        html += '<br />{}. {}'.format(idx + 1, definition)

    yield from bot.coro_send_message(event.conv, html)
