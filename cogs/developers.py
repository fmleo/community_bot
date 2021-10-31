import traceback

from discord.ext import commands


class Developers(commands.Cog):
    """Developer only commands"""
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.command(aliases=["load"])
    @commands.is_owner()
    async def load_extension(self, ctx, extension):
        """
        owner-only command used to load cogs
        the cog needs to be unloaded first
        in order to be able to be loaded

        :param ctx: Context (not provided)
        :param extension: Extension name to be loaded
        """
        try:
            self.bot.load_extension(f'cogs.{extension}')
        except commands.ExtensionAlreadyLoaded:
            return await ctx.send(
                f"Extension {extension} has already been loaded. Perhaps you mean `{ctx.prefix}reload {extension}`?"
            )
        except commands.ExtensionNotFound:
            return await ctx.send(
                f"Extension {extension} cannot be found. Did you type something wrong? (name is case sensitive)"
            )
        except commands.NoEntryPointError:
            return await ctx.send(
                f"Extension {extension} doesn't have a `setup` entry point function. See https://pycord.readthedocs.io/"
                f"en/latest/ext/commands/extensions.html#ext-commands-extensions for more details."
            )
        await ctx.send(f"Extension {extension} loaded successfully!")

    @commands.command(aliases=["unload"])
    @commands.is_owner()
    async def unload_extension(self, ctx, extension):
        """
        owner-only command used to unload cogs
        the cog needs to be loaded first
        in order to be able to be unloaded
        """
        try:
            self.bot.unload_extension(f'cogs.{extension}')
        except commands.ExtensionNotLoaded:
            return await ctx.send(f"Extension {extension} is not loaded. Did you type something wrong?"
                                  f"(name is case sensitive)")
        await ctx.send(f"Extension {extension} unloaded successfully!")

    @commands.command(aliases=["reload"])
    @commands.is_owner()
    async def reload_extension(self, ctx, extension):
        """
        owner-only command used to reload cogs.
        the reloaded cog needs to be loaded in
        order for this command to work
        """
        try:
            self.bot.reload_extension(f"cogs.{extension}")
        except commands.ExtensionNotFound:
            return await ctx.send(
                f"Extension {extension} cannot be found. Did you type something wrong? (name is case sensitive)"
            )
        except commands.NoEntryPointError:
            return await ctx.send(
                f"Extension {extension} doesn't have a `setup` entry point function. See https://pycord.readthedocs.io/"
                f"en/latest/ext/commands/extensions.html#ext-commands-extensions for more details."
            )
        except commands.ExtensionError as e:
            tb = traceback.TracebackException.from_exception(e)
            traceback_string = ''.join(tb.format())
            return await ctx.send(
                f"An error occured while trying to reload extension {extension}:\n"
                f"```python\n{traceback_string}```"
            )
        await ctx.send(f"Extension {extension} reloaded successfully!")


def setup(bot):
    bot.add_cog(Developers(bot))
