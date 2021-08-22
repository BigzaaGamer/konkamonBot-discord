import time
import discord
import psutil
import os
import urllib, json
import asyncio
import aiohttp
import requests

from datetime import datetime
from discord import Embed
from datetime import datetime
from discord.ext import commands
from utils import default,http

class Covid_Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = default.config()
        self.process = psutil.Process(os.getpid())

    async def covidthapi(self, ctx, url: str, updateDate: str, newCase: str, totalCase: str, todayDeath: str, totalDeath: str,todayRecov: str, Recov: str, active: str, token: str = None):
        try:
            cv = await http.get(
                url, res_method="json", no_cache=True,
                headers={"Authorization": token} if token else None
            )
        except aiohttp.ClientConnectorError:
            return await ctx.send("The API seems to be down...")
        except aiohttp.ContentTypeError:
            return await ctx.send("The API returned an error or didn't return JSON...")
        
        bruh = cv[updateDate] / 1000
        bruh2 = datetime.fromtimestamp(bruh)
        updateD = bruh2.strftime("%m/%d/%Y, %H:%M:%S")
        today_case = "{:,}".format(cv[newCase])
        total_case = "{:,}".format(cv[totalCase])
        today_death = "{:,}".format(cv[todayDeath])
        total_death= "{:,}".format(cv[totalDeath])
        covidEmbed = discord.Embed(title="สถานการณ์ COVID-19 ประเทศไทย",color=0xB61919,description="อัพเดทเมื่อ: " + updateD)
        covidEmbed.set_thumbnail(url="https://disease.sh/assets/img/flags/th.png")
        covidEmbed.add_field(name="จำนวนผู้ติดเชื้อวันนี้", value=today_case,inline=True)
        covidEmbed.add_field(name="ผู้ติดเชื้อทั้งหมด", value=total_case,inline=True)
        covidEmbed.add_field(name="ผู้เสียชีวิตวันนี้",value=today_death,inline=True)
        covidEmbed.add_field(name="ผู้เสียชีวิตทั้งหมด", value=total_death,inline=True)
        covidEmbed.add_field(name="หายแล้ว (วันนี้)", value="{:,}".format(cv[todayRecov]) ,inline=True)
        covidEmbed.add_field(name="หายแล้ว (ทั้งหมด)", value="{:,}".format(cv[Recov]) ,inline=True)
        covidEmbed.add_field(name="กำลังรักษา",value="{:,}".format(cv[active]) ,inline=True)
        
        await ctx.send(embed = covidEmbed)

    @commands.command()
    async def covidth(self, ctx):        
        await self.covidthapi(ctx, "https://disease.sh/v3/covid-19/countries/thailand", "updated", "todayCases","cases", "todayDeaths", "deaths", "todayRecovered", "recovered", "active")
    

def setup(bot):
    bot.add_cog(Covid_Commands(bot))
