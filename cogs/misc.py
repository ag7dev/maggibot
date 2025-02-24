import discord
from discord.ext import commands
from discord.commands import slash_command
from datetime import datetime
import os
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import requests
from io import BytesIO
import io
import textwrap
import asyncio


class Miscellaneous(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot
        
        @commands.slash_command(description='TEST COMMAND')
        async def test(ctx):
            await ctx.respond('Test')

        @commands.slash_command(description='Check the bot\'s latency')
        async def ping(ctx):
            loading_embed = discord.Embed(
                title="🏓 Pong!",
                description="Calculating latency... ⏳",
                color=discord.Color.blue()
            )
            loading_message = await ctx.respond(embed=loading_embed)

            latency = bot.latency * 1000
            await asyncio.sleep(1)

            embed = discord.Embed(
                title="🏓 Pong!",
                description=f"Latency: `{latency:.2f} ms`",
                color=discord.Color.green()
            )
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
            await loading_message.edit(embed=embed)
        
        @commands.slash_command(description='Get Info from a user')
        async def userinfo(ctx, target: discord.Member = None):
            target = target or ctx.author
            embed = discord.Embed(title="👤 User Information",
                                  colour=target.colour,
                                  timestamp=datetime.utcnow())
            embed.set_thumbnail(url=target.avatar.url)

            user_guilds_count = sum(1 for guild in bot.guilds if target in guild.members)

            fields = [
                ("📝 Name", str(target), True),
                ("🆔 ID", target.id, True),
                ("🤖 Bot?", "Yes" if target.bot else "No", True),
                ("🏅 Top Role", target.top_role.mention, True),
                ("💬 Status", str(target.status).title(), True),
                ("🎮 Activity", f"{str(target.activity.type).split('.')[-1].title() if target.activity else 'N/A'} {target.activity.name if target.activity else ''}", True),
                ("📅 Created At", target.created_at.strftime("%d/%m/%Y %H:%M:%S"), True),
                ("📅 Joined At", target.joined_at.strftime("%d/%m/%Y %H:%M:%S"), True),
                ("🚀 Boosted", "Yes" if target.premium_since else "No", True),
                ("🔖 Roles", ", ".join([role.mention for role in target.roles[1:]]) if len(target.roles) > 1 else "None", False),
                ("🖼️ Avatar URL", target.avatar.url, False),
                ("🔢 Discriminator", target.discriminator, True),
                ("🌐 Is Online?", "Yes" if target.status == discord.Status.online else "No", True),
                ("📺 Is Streaming?", "Yes" if target.activity and target.activity.type == discord.ActivityType.streaming else "No", True),
                ("🌍 Servers with Bot", user_guilds_count, True)
            ]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
            await ctx.respond(embed=embed)
        
        @commands.has_permissions(administrator=True)
        @bot.slash_command(description='Stops the bot')
        async def stop(ctx):
            authorised = int(os.getenv('OWNER_ID'))
            if ctx.author.id == authorised:
                embed = discord.Embed(
                    title="🛑 Bot Shutdown",
                    description="The bot is shutting down... Please wait a moment.",
                    color=discord.Color.red()
                )
                embed.add_field(name="Shutdown Reason", value="Manual shutdown initiated by the owner.", inline=False)
                embed.add_field(name="Time of Shutdown", value=datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"), inline=False)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
                await ctx.respond(embed=embed)
                await self.bot.close()
            else:
                embed = discord.Embed(
                    title="🚫 Permission Denied",
                    description="You do not have permission to stop the bot. Please contact the owner for assistance.",
                    color=discord.Color.orange()
                )
                embed.add_field(name="Owner ID", value=os.getenv('OWNER_ID'), inline=True)
                embed.add_field(name="Your ID", value=ctx.author.id, inline=True)
                embed.add_field(name="Contact Method", value="Please send a direct message to the owner.", inline=False)
                embed.set_footer(text=f"Requested by {ctx.author} | ID: {ctx.author.id}", icon_url=ctx.author.avatar.url)
                await ctx.respond(embed=embed)


        @commands.slash_command(description="Is my PC on fire? 🔥")
        async def ismypconfire(ctx):
            responses = [
                "🔥 Your PC is now classified as a nuclear reactor. RUN! 🏃💨",
                "💻 Your PC is fine... for now. But I hear the fans screaming. 👀",
                "🚒 Firefighters are on the way! Hope you have backups! 😨",
                "🥵 Your PC is sweating harder than a gaming laptop in summer!",
                "❄️ Nope, your PC is chilling. Maybe too much? Try overclocking! 😆",
                "🧯 Everything is fine! But keep an extinguisher nearby... just in case. 👀",
                "💀 Your PC died from overheating. It’s now in a better place. R.I.P. 😭",
                "🔥🔥🔥 SYSTEM OVERHEATING! RELEASING MAGIC SMOKE! 🔥🔥🔥"
            ]

            await ctx.respond(random.choice(responses))








def setup(bot: discord.Bot):
    bot.add_cog(Miscellaneous(bot))




