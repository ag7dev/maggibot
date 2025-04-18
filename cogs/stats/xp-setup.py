import discord
from discord.ext import commands
import json
import os
import datetime
from dotenv import load_dotenv
from handlers.debug import LogSystem, LogError, LogDebug, LogNetwork
from handlers.config import load_stats, save_stats, load_multiplier_config, save_multiplier_config

load_dotenv()
MESSAGE_XP_COUNT = float(os.getenv("MESSAGE_XP_COUNT", 0.2))
ATTACHMENT_XP_COUNT = float(os.getenv("ATTACHMENT_XP_COUNT", 0.5))

STATS_FILE = "data/stats.json"
XP_MULTIPLIER_FILE = "data/xpmultiplier.json"

class XPSetup(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.embed_colors = {
            "stats": 0x3498DB,
            "leaderboard": 0xF1C40F,
            "system": 0x2ECC71,
            "error": 0xE74C3C,
            "mod": 0x992D22
        }

    def create_embed(self, title, description="", color_type="stats"):
        embed = discord.Embed(
            title=title,
            description=description,
            color=self.embed_colors.get(color_type, 0x3498DB),
            timestamp=datetime.datetime.now()
        )
        embed.set_footer(
            text="AG7 Stats System",
            icon_url="https://ag7-dev.de/favicon/favicon.ico"
        )
        return embed



    @commands.slash_command(name="xp-setmultiplier", description="⚖️ Set role XP multiplier")
    @commands.is_owner()
    async def xp_setmultiplier(self, ctx: discord.ApplicationContext, 
                              role: discord.Role, multiplier: float):
        await ctx.defer(ephemeral=True)
        LogDebug(f"Multiplier set for {role.id} by {ctx.author.id}")
        
        try:
            config = load_multiplier_config()
            config["multipliers"][str(role.id)] = multiplier
            save_multiplier_config(config)
            
            embed = self.create_embed(
                "⚖️ Multiplier Updated",
                f"Role {role.mention} now grants `{multiplier}x` XP",
                "system"
            )
            await ctx.followup.send(embed=embed)

        except Exception as e:
            LogError(f"Set multiplier error: {str(e)}")
            raise

    @commands.slash_command(name="xp-showmultiplier", description="📜 Show current multipliers")
    @commands.is_owner()
    async def xp_showmultiplier(self, ctx: discord.ApplicationContext):
        await ctx.defer(ephemeral=True)
        
        try:
            config = load_multiplier_config()
            embed = self.create_embed(
                "📜 Active Multipliers",
                color_type="system"
            )

            if config["multipliers"]:
                for role_id, mult in config["multipliers"].items():
                    role = ctx.guild.get_role(int(role_id))
                    embed.add_field(
                        name=f"⚖️ {role.name if role else 'Deleted Role'}",
                        value=f"`{mult}x` Multiplier",
                        inline=True
                    )
            else:
                embed.description = "```diff\n- No multipliers set```"

            await ctx.followup.send(embed=embed)

        except Exception as e:
            LogError(f"Show multipliers error: {str(e)}")
            raise

    @commands.slash_command(name="xp-removemultiplier", description="🗑️ Remove role multiplier")
    @commands.is_owner()
    async def xp_removemultiplier(self, ctx: discord.ApplicationContext, role: discord.Role):
        await ctx.defer(ephemeral=True)
        LogDebug(f"Multiplier removed for {role.id} by {ctx.author.id}")
        
        try:
            config = load_multiplier_config()
            role_id = str(role.id)
            
            if role_id in config["multipliers"]:
                del config["multipliers"][role_id]
                save_multiplier_config(config)
                embed = self.create_embed(
                    "🗑️ Multiplier Removed",
                    f"Removed multiplier for {role.mention}",
                    "system"
                )
            else:
                embed = self.create_embed(
                    "⚠️ Not Found",
                    f"No multiplier set for {role.mention}",
                    "error"
                )
            
            await ctx.followup.send(embed=embed)

        except Exception as e:
            LogError(f"Remove multiplier error: {str(e)}")
            raise


    @commands.slash_command(name="xp-count", description="📦 Show stats database info")
    async def xp_count(self, ctx: discord.ApplicationContext):
        await ctx.defer()
        
        try:
            stats = load_stats()
            total = len(stats)
            active = sum(1 for u in stats.values() if u.get("xp", 0) > 0)
            
            embed = self.create_embed(
                "📦 Database Statistics",
                color_type="stats"
            )
            embed.add_field(
                name="Total Users",
                value=f"```yaml\n{total}```",
                inline=True
            )
            embed.add_field(
                name="Active Users",
                value=f"```yaml\n{active}```",
                inline=True
            )
            await ctx.followup.send(embed=embed)

        except Exception as e:
            LogError(f"XP count error: {str(e)}")
            raise

def setup(bot):
    bot.add_cog(XPSetup(bot))