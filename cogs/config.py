import discord
from discord.ext import commands
from discord.ext.commands import Cog
import os
import json
import asyncio
import datetime
import logging
import handlers.config as config
import handlers.debug as DebugHandler


class Server(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.serverconfig = config.loadserverconfig()

    @commands.slash_command(name="setup-logchannel", description="Set the log channel for the server")
    @commands.has_permissions(administrator=True)
    async def settings_logchannel(self, ctx, channel: discord.TextChannel):
        try:
            guild_id = str(ctx.guild.id)
            
            DebugHandler.LogDebug(f"Current server config for guild {guild_id}: {self.serverconfig}")

            if guild_id not in self.serverconfig:
                self.serverconfig[guild_id] = {}

            self.serverconfig[guild_id]["logchannel"] = channel.id
            DebugHandler.LogDebug(f"Updated server config for guild {guild_id}: {self.serverconfig[guild_id]}")

            config.saveserverconfig(self.serverconfig)

            embed = discord.Embed(
                title="Success",
                description=f"Log channel has been set to {channel.mention}",
                color=0x00ff00
            )
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
            embed.timestamp = datetime.datetime.utcnow()
            embed.set_thumbnail(url=ctx.guild.icon.url)
            embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon.url)
            embed.add_field(name="Channel", value=channel.mention, inline=False)
            embed.add_field(name="Channel ID", value=channel.id, inline=False)
            embed.add_field(name="Guild ID", value=ctx.guild.id, inline=False)

            await ctx.respond(embed=embed)

        except Exception as e:
            # Log the error if there is an exception
            DebugHandler.LogDebug(f"An error occurred while setting the log channel: {e}")
            await ctx.respond(f"An error occurred while setting the log channel: {e}")



def setup(bot):
    bot.add_cog(Server(bot))
