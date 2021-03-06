import random
import discord
import time
import secrets
import asyncio
import aiohttp

from discord import Embed
from io import BytesIO
from discord.ext import commands
from utils import lists, permissions, http, default

class Fun_Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = default.config()
        self.alex_api_token = self.config["alexflipnote_api"]
    
    @commands.command(aliases=["8ball"])
    async def eightball(self, ctx, *, question: commands.clean_content):
        """ Consult 8ball to receive an answer """
        answer = random.choice(lists.ballresponse)
        await ctx.send(f"🎱 **Question:** {question}\n**Answer:** {answer}")

    async def randomimageapi(self, ctx, url: str, endpoint: str, token: str = None):
        try:
            r = await http.get(
                url, res_method="json", no_cache=True,
                headers={"Authorization": token} if token else None
            )
        except aiohttp.ClientConnectorError:
            return await ctx.send("The API seems to be down...")
        except aiohttp.ContentTypeError:
            return await ctx.send("The API returned an error or didn't return JSON...")

        await ctx.send(r[endpoint])

    async def randommemeapi(self, ctx, url: str, endpoint: str, title: str, source: str, token: str = None):
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
        memeEmbed=discord.Embed(title=memeTitle, color=0xFF4C29, url=memeSource)
        memeEmbed.set_image(url=memeImage)
        await ctx.send(embed = memeEmbed)

    async def api_img_creator(self, ctx, url: str, filename: str, content: str = None):
        async with ctx.channel.typing():
            req = await http.get(url, res_method="read")

            if not req:
                return await ctx.send("I couldn't create the image ;-;")

            bio = BytesIO(req)
            bio.seek(0)
            await ctx.send(content=content, file=discord.File(bio, filename=filename))

    @commands.command()
    @commands.cooldown(rate=1, per=1.5, type=commands.BucketType.user)
    async def duck(self, ctx):
        """ Posts a random duck """
        await self.randomimageapi(ctx, "https://random-d.uk/api/v1/random", "url")

    @commands.command()
    @commands.cooldown(rate=1, per=1.5, type=commands.BucketType.user)
    async def coffee(self, ctx):
        """ Posts a random coffee """
        await self.randomimageapi(ctx, "https://coffee.alexflipnote.dev/random.json", "file")

    @commands.command(aliases=["flip", "coin"])
    async def coinflip(self, ctx):
        """ Coinflip! """
        coinsides = ["หัว", "ก้อย"]
        await ctx.send(f"**{ctx.author.name}** ได้ทำการหมุนเหรียญ! ผลทีได้: **{random.choice(coinsides)}**!")

    @commands.command()
    async def f(self, ctx, *, text: commands.clean_content = None):
        """ Press F to pay respect """
        hearts = ["❤", "💛", "💚", "💙", "💜"]
        reason = f"for **{text}** " if text else ""
        await ctx.send(f"**{ctx.author.name}** has paid their respect {reason}{random.choice(hearts)}")

    @commands.command()
    @commands.cooldown(rate=1, per=2.0, type=commands.BucketType.user)
    async def urban(self, ctx, *, search: commands.clean_content):
        """ Find the 'best' definition to your words """
        async with ctx.channel.typing():
            try:
                url = await http.get(f"https://api.urbandictionary.com/v0/define?term={search}", res_method="json")
            except Exception:
                return await ctx.send("Urban API returned invalid data... might be down atm.")

            if not url:
                return await ctx.send("I think the API broke...")

            if not len(url["list"]):
                return await ctx.send("Couldn't find your search in the dictionary...")

            result = sorted(url["list"], reverse=True, key=lambda g: int(g["thumbs_up"]))[0]

            definition = result["definition"]
            if len(definition) >= 1000:
                definition = definition[:1000]
                definition = definition.rsplit(" ", 1)[0]
                definition += "..."

            await ctx.send(f"📚 Definitions for **{result['word']}**```fix\n{definition}```")

    @commands.command()
    async def reverse(self, ctx, *, text: str):
        """ !poow ,ffuts esreveR
        Everything you type after reverse will of course, be reversed
        """
        t_rev = text[::-1].replace("@", "@\u200B").replace("&", "&\u200B")
        await ctx.send(f"🔁 {t_rev}")

    @commands.command()
    async def meme(self, ctx):
        """ สุ่มมีมฮาๆ """
        await self.randommemeapi(ctx, "https://meme-api.herokuapp.com/gimme/memes", "url","title","postLink")

    @commands.command()
    async def ฮั่นแน่(self, ctx):
        """ สุ่มข้อความ ฮั่นแน่่!! """
        hunnae_answer = random.choice(lists.hunnaeresponse)
        await ctx.reply("ฮั่นแน่!!! " + hunnae_answer)
        #time.sleep(5)
        #await ctx.channel.purge(limit=2)
    
    @commands.command(name="คำคม")
    async def kumkhom(self, ctx):
        kumkhomEmbed = discord.Embed(color=0x7FC8A9)
        kumkhom_dict = {}
        
        for number in range(1,6):
            number2 = number
            number2 += number
            kumkhom_dict["kumkhom%s" %number] = random.choice(lists.kumkhom)
            kumkhom_dict["kumkhom%s" %number2] = random.choice(lists.kumkhom)
            kumkhomEmbed.add_field(name=kumkhom_dict["kumkhom%s" %number], value=kumkhom_dict["kumkhom%s" %number2 ],inline=False)

        await ctx.send(content="รวมคำคมเด็ดๆ หลากหลายอารมณ์!!", embed = kumkhomEmbed)

    @commands.command()
    async def password(self, ctx, nbytes: int = 18):
        """ Generates a random password string for you

        This returns a random URL-safe text string, containing nbytes random bytes.
        The text is Base64 encoded, so on average each byte results in approximately 1.3 characters.
        """
        if nbytes not in range(3, 1401):
            return await ctx.send("I only accept any numbers between 3-1400")
        if hasattr(ctx, "guild") and ctx.guild is not None:
            await ctx.send(f"Sending you a private message with your random generated password **{ctx.author.name}**")
        await ctx.author.send(f"🎁 **Here is your password:**\n{secrets.token_urlsafe(nbytes)}")

    @commands.command()
    async def rate(self, ctx, *, thing: commands.clean_content):
        """ Rates what you desire """
        rate_amount = random.uniform(0.0, 100.0)
        await ctx.send(f"I'd rate `{thing}` a **{round(rate_amount, 4)} / 100**")

    @commands.command()
    async def beer(self, ctx, user: discord.Member = None, *, reason: commands.clean_content = ""):
        """ Give someone a beer! 🍻 """
        if not user or user.id == ctx.author.id:
            return await ctx.send(f"**{ctx.author.name}**: paaaarty!🎉🍺")
        if user.id == self.bot.user.id:
            return await ctx.send("*drinks beer with you* 🍻")
        if user.bot:
            return await ctx.send(f"I would love to give beer to the bot **{ctx.author.name}**, but I don't think it will respond to you :/")

        beer_offer = f"เฮ้ **{user.name}**, **{ctx.author.name}** ได้ชวนคุณมาดื่มเบียร์ด้วยกัน!!!"
        beer_offer = beer_offer + f"\n\n**เหตุผล:** {reason}" if reason else beer_offer
        msg = await ctx.send(beer_offer)

        def reaction_check(m):
            if m.message_id == msg.id and m.user_id == user.id and str(m.emoji) == "🍻":
                return True
            return False

        try:
            await msg.add_reaction("🍻")
            await self.bot.wait_for("raw_reaction_add", timeout=30.0, check=reaction_check)
            await msg.edit(content=f"**{user.name}** กับ **{ctx.author.name}** ได่ดื่มเบีียร์กันอย่างสนุกสนาน!! 🍻")
        except asyncio.TimeoutError:
            await msg.delete()
            await ctx.send(f"well, doesn't seem like **{user.name}** wanted a beer with you **{ctx.author.name}** ;-;")
        except discord.Forbidden:
            # Yeah so, bot doesn't have reaction permission, drop the "offer" word
            beer_offer = f"**{user.name}**, you got a 🍺 from **{ctx.author.name}**"
            beer_offer = beer_offer + f"\n\n**Reason:** {reason}" if reason else beer_offer
            await msg.edit(content=beer_offer)

    @commands.command(aliases=["howhot", "hot"])
    async def hotcalc(self, ctx, *, user: discord.Member = None):
        """ Returns a random percent for how hot is a discord user """
        user = user or ctx.author

        random.seed(user.id)
        r = random.randint(1, 100)
        hot = r / 1.17

        if hot > 25:
            emoji = "❤"
        elif hot > 50:
            emoji = "💖"
        elif hot > 75:
            emoji = "💞"
        else:
            emoji = "💔"

        await ctx.send(f"**{user.name}** มีความหล่อเท่ **{hot:.2f}%** {emoji}")

    @commands.command(aliases=["noticemesenpai"])
    async def noticeme(self, ctx):
        """ Notice me senpai! owo """
        if not permissions.can_handle(ctx, "attach_files"):
            return await ctx.send("I cannot send images here ;-;")

        bio = BytesIO(await http.get("https://i.alexflipnote.dev/500ce4.gif", res_method="read"))
        await ctx.send(file=discord.File(bio, filename="noticeme.gif"))

    @commands.command(aliases=["slots", "bet"])
    @commands.cooldown(rate=1, per=3.0, type=commands.BucketType.user)
    async def slot(self, ctx):
        """ Roll the slot machine """
        emojis = "🍎🍊🍐🍋🍉🍇🍓🍒"
        a = random.choice(emojis)
        b = random.choice(emojis)
        c = random.choice(emojis)

        #slotmachine = f"**[ {a} {b} {c} ]\n{ctx.author.name}**,"
        slotmachine = discord.Embed(color=0xFFE459)
        slotmachine.add_field(name="1", value=a)
        slotmachine.add_field(name="2", value=b)
        slotmachine.add_field(name="3", value=c)

        if (a == b == c):
            await ctx.send(embed = slotmachine)
            #await ctx.send(f"{slotmachine} All matching, you won! 🎉")
            await ctx.send("All matching, you won! 🎉")
        elif (a == b) or (a == c) or (b == c):
            await ctx.send(embed = slotmachine)
            #await ctx.send(f"{slotmachine} 2 in a row, you won! 🎉")
            await ctx.send("2 in a row, you won! 🎉")
        else:
            await ctx.send(embed = slotmachine)
            #await ctx.send(f"{slotmachine} No match, you lost 😢")
            await ctx.send("No match, you lost 😢")


def setup(bot):
    bot.add_cog(Fun_Commands(bot))
