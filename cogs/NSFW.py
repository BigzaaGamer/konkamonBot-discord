import discord
import secrets
import asyncio
import aiohttp

from discord import Embed
from io import BytesIO
from discord.ext import commands
from utils import lists, permissions, http, default

class NSFW(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = default.config()

    async def randomNSFW(self, ctx, url: str, endpoint: str, title: str, source: str, token: str = None):
        try:
            rr = await http.get(
                url, res_method="json", no_cache=True,
                headers={"Authorization": token} if token else None
            )
        except aiohttp.ClientConnectorError:
            return await ctx.send("The API seems to be down...")
        except aiohttp.ContentTypeError:
            return await ctx.send("The API returned an error or didn't return JSON...")

        memeTitle = rr[title]
        memeImage = rr[endpoint]
        memeSource = rr[source]
        memeEmbed=discord.Embed(title=memeTitle,color=discord.Color.blue(),url=memeSource)
        memeEmbed.set_image(url=memeImage)
        await ctx.send(embed = memeEmbed)
    
    @commands.command()
    async def porngif(self, ctx):
        """ สุ่ม GIF โป๊ๆ 18+ """
        if ctx.channel.is_nsfw():
            await self.randomNSFW(ctx, "https://meme-api.herokuapp.com/gimme/porngif", "url","title","postLink")
        else:
            await ctx.reply("คำสั่งนี้สำหรับห้อง NSFW..\nสามารถใช้ได้ใน <#573117765528059914>") 

    @commands.command()
    async def cumslut(self, ctx):
        """ จากชืื่อคำสั่ง ก็น่าจะรู้นะ 555 """
        if ctx.channel.is_nsfw():
            await self.randomNSFW(ctx, "https://meme-api.herokuapp.com/gimme/cumsluts", "url","title","postLink")
        else:
            await ctx.reply("คำสั่งนี้สำหรับห้อง NSFW..\nสามารถใช้ได้ใน <#573117765528059914>") 

    @commands.command()
    async def gonewild(self, ctx):
        if ctx.channel.is_nsfw():
            await self.randomNSFW(ctx, "https://meme-api.herokuapp.com/gimme/gonewild", "url","title","postLink")
        else:
            await ctx.reply("คำสั่งนี้สำหรับห้อง NSFW..\nสามารถใช้ได้ใน <#573117765528059914>") 

    @commands.command()
    async def creampies(self, ctx):
        if ctx.channel.is_nsfw():
            await self.randomNSFW(ctx, "https://meme-api.herokuapp.com/gimme/creampies", "url","title","postLink")
        else:
            await ctx.reply("คำสั่งนี้สำหรับห้อง NSFW..\nสามารถใช้ได้ใน <#573117765528059914>") 

    @commands.command()
    async def anal(self, ctx):
        if ctx.channel.is_nsfw():
            await self.randomNSFW(ctx, "https://meme-api.herokuapp.com/gimme/anal", "url","title","postLink")
        else:
            await ctx.reply("คำสั่งนี้สำหรับห้อง NSFW..\nสามารถใช้ได้ใน <#573117765528059914>")

    @commands.command()
    async def realgirls(self, ctx):
        if ctx.channel.is_nsfw():
            await self.randomNSFW(ctx, "https://meme-api.herokuapp.com/gimme/RealGirls", "url","title","postLink")
        else:
            await ctx.reply("คำสั่งนี้สำหรับห้อง NSFW..\nสามารถใช้ได้ใน <#573117765528059914>")
    @commands.command()
    async def blowjobs(self, ctx):
        if ctx.channel.is_nsfw():
            await self.randomNSFW(ctx, "https://meme-api.herokuapp.com/gimme/blowjobs", "url","title","postLink")
        else:
            await ctx.reply("คำสั่งนี้สำหรับห้อง NSFW..\nสามารถใช้ได้ใน <#573117765528059914>")
            
    @commands.command()
    async def tits(self, ctx):
        if ctx.channel.is_nsfw():
            await self.randomNSFW(ctx, "https://meme-api.herokuapp.com/gimme/BustyPetite", "url","title","postLink")
        else:
            await ctx.reply("คำสั่งนี้สำหรับห้อง NSFW..\nสามารถใช้ได้ใน <#573117765528059914>")    

    @commands.command()
    async def collegesluts(self, ctx):
        if ctx.channel.is_nsfw():
            await self.randomNSFW(ctx, "https://meme-api.herokuapp.com/gimme/collegeslut", "url","title","postLink")
        else:
            await ctx.reply("คำสั่งนี้สำหรับห้อง NSFW..\nสามารถใช้ได้ใน <#573117765528059914>") 
                            

def setup(bot):
    bot.add_cog(NSFW(bot))
