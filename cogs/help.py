import discord
import secrets
import asyncio
import aiohttp

from discord import Embed
from io import BytesIO
from discord.ext import commands
from utils import lists, permissions, http, default

class customHelp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = default.config()



    @commands.group(pass_context=True,aliases=["h","help","commands","command","cmd"])
    async def helpme(self, ctx):
        if ctx.invoked_subcommand is None:
            helpEmbed = discord.Embed(title=f"คำสั่งต่างๆ ของ {ctx.bot.user}",color=0xF8485E, description="prefix ของบอท `&`")
            helpEmbed.add_field(name="สนุกสนาน",value="`meme` สุ่มมีมฮาๆ\n`coinflip`,`coin` หัว/ก้อย!!\n`คำคม` สุ่มคำคม หลายอารมณ์\n`slot` เล่นสลอต แมคชีน",inline=True)
            helpEmbed.add_field(name="COVID-19", value="`covidth` ดูสถานการณ์ COVID-19 ประเทศไทย วันนี้",inline=True)
            helpEmbed.add_field(name="ข้อมูลต่างๆ",value="`avatar` ดูรูปประจำตัวของตัวเอง หรือของคนอื่น\n`joindat` ดูวันที่เข้าร่วมเซิฟ\n`server` เกี่ยวกับเซิฟเวอร์\n`user` เกี่ยวกับคุณ",inline=True)
            helpEmbed.add_field(name="NSFW", value="พิมพ์ `help nsfw` เพื่อดูคำสั่ง NSFW (คำสั่งสำหรับสายหื่น สาย 18+ เท่านั้น!!)",inline=False)
            await ctx.send(embed = helpEmbed)

    @helpme.group(pass_context=True,aliases=["nsfw","NSFW"])
    async def nsfwCMD(self, ctx):
        #if ctx.invoked_subcommand is None:
            #await ctx.send("NSFW คำสั่ง")
        nsfwEmbed = discord.Embed(title="คำสั่ง NSFW", color=0xF8485E, description="คำสั่ง 18+ ใช้ได้แค่ในช่อง NSFW เท่านั้น!!! ใครไม่ชอบ อย่าหาพิมพ์!")
        nsfwEmbed.add_field(name="คำสั่ง", value="`porngif`, `cumslut`, `gonewild`, `creampies`, `anal`, `realgirls`, `blowjobs`, `tits`, `collegesluts`")
        await ctx.send(embed = nsfwEmbed)


def setup(bot):
    bot.add_cog(customHelp(bot))
