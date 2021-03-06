import time
import discord
import psutil
import os
import urllib, json
import asyncio
import aiohttp
import requests

from discord import Embed
from datetime import datetime
from discord.ext import commands
from utils import default,http

class Information(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = default.config()
        self.process = psutil.Process(os.getpid())

    @commands.command()
    async def ping(self, ctx):
        """ Pong! """
        before = time.monotonic()
        before_ws = int(round(self.bot.latency * 1000, 1))
        message = await ctx.send("🏓 Pong")
        ping = (time.monotonic() - before) * 1000
        await message.edit(content=f"🏓 WS: {before_ws}ms  |  REST: {int(ping)}ms")

    @commands.command(aliases=["joinme", "join", "botinvite"])
    async def invite(self, ctx):
        """ Invite me to your server """
        await ctx.send(f"**{ctx.author.name}**, use this URL to invite me\n<{discord.utils.oauth_url(self.bot.user.id)}>")

    @commands.command()
    async def source(self, ctx):
        """ Check out my source code <3 """
        # Do not remove this command, this has to stay due to the GitHub LICENSE.
        # TL:DR, you have to disclose source according to MIT.
        # Reference: https://github.com/AlexFlipnote/discord_bot.py/blob/master/LICENSE
        await ctx.send(f"**{ctx.bot.user}** is powered by this source code:\nhttps://github.com/AlexFlipnote/discord_bot.py")

    @commands.command(aliases=["supportserver", "feedbackserver"])
    async def botserver(self, ctx):
        """ Get an invite to our support server! """
        if isinstance(ctx.channel, discord.DMChannel) or ctx.guild.id != 86484642730885120:
            return await ctx.send(f"**Here you go {ctx.author.name} 🍻\n<{self.config['botserver']}>**")
        await ctx.send(f"**{ctx.author.name}** this is my home you know :3")

    @commands.command(aliases=["info", "stats", "status"])
    async def about(self, ctx):
        """ About the bot """
        ramUsage = self.process.memory_full_info().rss / 1024**2
        avgmembers = sum(g.member_count for g in self.bot.guilds) / len(self.bot.guilds)

        embedColour = discord.Embed.Empty
        if hasattr(ctx, "guild") and ctx.guild is not None:
            embedColour = ctx.me.top_role.colour

        embed = discord.Embed(colour=embedColour)
        embed.set_thumbnail(url=ctx.bot.user.avatar_url)
        embed.add_field(name="ปิดปรับปรุงล่าสุด", value=default.timeago(datetime.now() - self.bot.uptime), inline=True)
        embed.add_field(
            name=f"ผู้พัฒนา{'' if len(self.config['owners']) == 1 else 's'}",
            value=", ".join([str(self.bot.get_user(x)) for x in self.config["owners"]]),
            inline=True
        )
        embed.add_field(name="Library", value="[discord.py](https://discordpy.readthedocs.io/en/stable/)\n(อื่นๆอีก 62)", inline=True)
        #embed.add_field(name="Servers", value=f"{len(ctx.bot.guilds)} ( avg: {avgmembers:,.2f} users/server )", inline=True)
        embed.add_field(name="ภาษาที่ใช้", value="Python", inline=True)
        embed.add_field(name="จำนวนคำสั่ง", value=len([x.name for x in self.bot.commands]), inline=True)
        #embed.add_field(name="RAM", value=f"{ramUsage:.2f} MB", inline=True)
        embed.add_field(name="GitHub", value="[konkamonBot](https://github.com/BigzaaGamer/konkamonBot-discord)\n[Source](https://github.com/AlexFlipnote/discord_bot.py)")
        embed.add_field(name="ข้อความจากผู้พัฒนา", value="**22/08/2021**: ทีแรกกะว่าจะใช้เว็บ Autobot แต่ขอลองเขียนเองก่อน สนุกดี555", inline=False)

        await ctx.send(content=f"ℹ เกี่ยวกับ **{ctx.bot.user}** | เวอร์ชั่น **{self.config['version']}**", embed=embed)


def setup(bot):
    bot.add_cog(Information(bot))
