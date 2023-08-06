

# region [Imports]

# * Standard Library Imports ---------------------------------------------------------------------------->
import os
import re
import json
from pprint import pformat
from dotenv import load_dotenv
# * Third Party Imports --------------------------------------------------------------------------------->
import discord
from discord.ext import commands, flags, tasks
from emoji import demojize, emojize, emoji_count
from emoji.unicode_codes import EMOJI_UNICODE_ENGLISH
from webdav3.client import Client
from typing import TYPE_CHECKING
# * Gid Imports ----------------------------------------------------------------------------------------->
import gidlogger as glog
# * Local Imports --------------------------------------------------------------------------------------->
from antipetros_discordbot.utility.misc import generate_bot_data
from antipetros_discordbot.utility.gidtools_functions import writejson
from antipetros_discordbot.init_userdata.user_data_setup import ParaStorageKeeper
from antipetros_discordbot.utility.enums import CogMetaStatus, UpdateTypus
from antipetros_discordbot.engine.replacements import AntiPetrosBaseCog, auto_meta_info_command
from antipetros_discordbot.utility.discord_markdown_helper.special_characters import ListMarker
from antipetros_discordbot.utility.discord_markdown_helper.general_markdown_helper import CodeBlock
from antipetros_discordbot.utility.converters import CommandConverter, SeparatedListConverter, RoleOrIntConverter
from pyyoutube import Api
from antipetros_discordbot.utility.sqldata_storager import general_db
from marshmallow import Schema
from rich import inspect as rinspect
from antipetros_discordbot.schemas.bot_schema import AntiPetrosBotSchema
import ftfy
from hashlib import blake2b
import json
if TYPE_CHECKING:
    from antipetros_discordbot.engine.antipetros_bot import AntiPetrosBot
# endregion [Imports]

# region [Logging]

log = glog.aux_logger(__name__)
glog.import_notification(log, __name__)

# endregion[Logging]

# region [Constants]
APPDATA = ParaStorageKeeper.get_appdata()
BASE_CONFIG = ParaStorageKeeper.get_config('base_config')
COGS_CONFIG = ParaStorageKeeper.get_config('cogs_config')
# location of this file, does not work if app gets compiled to exe with pyinstaller
THIS_FILE_DIR = os.path.abspath(os.path.dirname(__file__))


# endregion [Constants]

# region [TODO]

# TODO: create regions for this file
# TODO: Document and Docstrings


# endregion [TODO]

class RoleSchema(Schema):

    class Meta:
        additional = ("id", "name", "mentionable", "position", 'created_at', 'hoist')


class GeneralDebugCog(AntiPetrosBaseCog, command_attrs={'hidden': True}):
    """
    Cog for debug or test commands, should not be enabled fo normal Bot operations.
    """

    public = False
    meta_status = CogMetaStatus.WORKING | CogMetaStatus.OPEN_TODOS | CogMetaStatus.UNTESTED | CogMetaStatus.FEATURE_MISSING | CogMetaStatus.NEEDS_REFRACTORING | CogMetaStatus.DOCUMENTATION_MISSING | CogMetaStatus.FOR_DEBUG

    def __init__(self, bot: "AntiPetrosBot"):
        super().__init__(bot)
        self.ready = False
        self.bob_user = None
        self.antidevtros_member = None
        self.antipetros_member = None
        self.edit_embed_message = None
        self.general_db = general_db

        glog.class_init_notification(log, self)

    async def on_ready_setup(self):

        self.bob_user = await self.bot.fetch_antistasi_member(346595708180103170)
        for member in self.bot.antistasi_guild.members:
            if member.bot is True:
                if member.display_name.casefold() == 'antidevtros':
                    self.antidevtros_member = member

                elif member.display_name.casefold() == 'antipetros':
                    self.antipetros_member = member
                else:
                    if self.antidevtros_member is not None and self.antipetros_member is not None:
                        break
        await generate_bot_data(self.bot, self.antipetros_member)

        self.ready = True
        log.debug('setup for cog "%s" finished', str(self))

    async def update(self, typus: UpdateTypus):

        log.debug('cog "%s" was updated', str(self))

    @auto_meta_info_command()
    async def tell_sub_supporter(self, ctx: commands.Context):
        text = ListMarker.make_list([str(sub_sup) for sub_sup in self.bot.support.subsupports])
        await ctx.send(text, allowed_mentions=discord.AllowedMentions.none(), delete_after=120)

    @ auto_meta_info_command()
    async def dump_bot(self, ctx: commands.Context):
        schema = AntiPetrosBotSchema()
        data = schema.dump(self.bot)
        with open('bot_dump.json', 'w') as f:
            f.write(json.dumps(data, default=str, sort_keys=True, indent=4))

        await ctx.send('done')

    @ auto_meta_info_command()
    async def cached_msgs(self, ctx: commands.Context):
        data = list(map(lambda x: x.content, self.bot.cached_messages))
        writejson(data, "cached_msgs.json")

    @ auto_meta_info_command()
    async def save_msg(self, ctx: commands.Context, channel: discord.TextChannel, message_id: int):
        msg = await channel.fetch_message(message_id)
        with open(str(message_id) + ".txt", 'w', encoding='utf-8', errors='ignore') as f:
            f.write(msg.content)
        writejson(msg.content, str(message_id) + '.json')
        await ctx.send('done')

    @auto_meta_info_command()
    async def say_bot_emoji(self, ctx: commands.Context):
        for name in self.bot.color_emoji_id_map:
            await ctx.send(await self.bot.get_color_emoji(name))

    @auto_meta_info_command()
    async def force_reconnect(self, ctx: commands.Context, seconds: int, times: int = 2):
        import time
        for i in range(times):
            time.sleep(seconds)
            await ctx.send(f"slept blocking for {seconds} seconds")

    @auto_meta_info_command()
    async def say_best_alias(self, ctx: commands.Context, command: CommandConverter):
        await ctx.send(command.best_alias)

    @auto_meta_info_command()
    async def taken_colors(self, ctx: commands.Context):
        taken = []
        for cog_name, cog_object in sorted(self.bot.cogs.items(), key=lambda x: (x[1].color != 'default', x[1].color)):
            await ctx.send(f"{cog_name} | {await self.bot.get_color_emoji(cog_object.color)} | {cog_object.color}")
            if cog_object.color in taken and cog_object.color != 'default':
                await ctx.send(f"duplicate color {cog_object.color}")
            taken.append(cog_object.color)
        not_taken = []
        taken = set(taken)
        for color in self.bot.color_emoji_id_map:
            if color not in taken:
                not_taken.append(color)
        await ctx.send('\n'.join(not_taken))

    @auto_meta_info_command()
    async def other_guild_emojis(self, ctx: commands.Context):
        x = {}
        for _emoji in self.bot.bot_testing_guild.emojis:
            name = _emoji.name.casefold()
            if name not in {'antidevtros', 'link_emoji'}:
                x[_emoji.name.casefold()] = _emoji.id
        x['default'] = 839782169303449640
        x = {key: value for key, value in sorted(x.items(), key=lambda x: (x[0] != 'default', x[0]))}
        await ctx.send(CodeBlock(pformat(x, sort_dicts=False), "python"))

    @ auto_meta_info_command()
    async def dump_roles(self, ctx: commands.Context):
        async with ctx.typing():
            schema = RoleSchema()

            with open('role_dump.json', 'w') as f:
                f.write(schema.dumps(list(self.bot.antistasi_guild.roles), many=True))
            await ctx.send('done', delete_after=90, allowed_mentions=discord.AllowedMentions.none())

    @auto_meta_info_command()
    async def separated_list_converter_test(self, ctx: commands.Context, *, the_list: SeparatedListConverter(value_type=RoleOrIntConverter(), separator=',', strip_whitespace=True)):
        await ctx.send(ListMarker.make_list(the_list), allowed_mentions=discord.AllowedMentions.none())

    @auto_meta_info_command()
    async def check_message_existing(self, ctx: commands.Context, channel_id: int, message_id: int):
        try:
            await ctx.send(await self.bot.get_message_directly(channel_id, message_id), allowed_mentions=discord.AllowedMentions.none())
        except discord.errors.NotFound as e:
            await ctx.send(e, allowed_mentions=discord.AllowedMentions.none())
    # def cog_unload(self):
    #     log.debug("Cog '%s' UNLOADED!", str(self))

    async def cog_check(self, ctx):
        if ctx.author.id == 576522029470056450:
            return True
        return False


def setup(bot):
    """
    Mandatory function to add the Cog to the bot.
    """
    bot.add_cog(GeneralDebugCog(bot))
