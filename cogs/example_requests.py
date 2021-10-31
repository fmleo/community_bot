import aiohttp

import discord
from discord.ext import commands


class ExampleRequests(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(
        help="Sends a fact about axolotls and an image."
    )
    async def axolotl(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://axoltlapi.herokuapp.com/") as response:
                try:
                    response.raise_for_status()
                    response_json = await response.json()
                except aiohttp.ClientResponseError:
                    return await ctx.send('Unable to connect to the server! Please wait a while and try again.')
                embed = discord.Embed(
                    color=ctx.me.color,  # defines the embed color as the bot's color in the server
                    description=response_json.get("facts"),
                )

                embed.set_image(url=response_json.get("url"))  # sets the embed image with the url returned by the api

                # adds a footer to the embed, the icon_url parameter takes any url with an image in it.
                embed.set_footer(
                    text="Command made by leowonardo#2443",
                    icon_url="https://en.gravatar.com/userimage/171548483/05a79763322fb378f65535c1054e8d82.jpeg"
                )

                await ctx.reply(embed=embed, mention_author=False)


def setup(client):
    client.add_cog(ExampleRequests(client))
