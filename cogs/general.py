import time, datetime
import discord
from discord import Message
from discord.ext import commands

async def setup(bot) -> None:
    await bot.add_cog(General(bot))

class General(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
    
    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def ping(self, ctx):
        """Test my respond time"""
        latency = round(self.bot.latency * 1000)  # Độ trễ tính bằng ms
        await ctx.send(f"Pong! Độ trễ: {latency}ms")

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def uptime(self, ctx):
        """How long I've been up"""
        current_time = time.time()
        uptime_seconds = int(current_time - self.bot.start_time)
        uptime_str = str(datetime.utcfromtimestamp(uptime_seconds).strftime('%H:%M:%S'))
        await ctx.send(f"Bot đã online trong: {uptime_str}")

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def invite(self, ctx):
        """Get my invite link"""
        permissions = discord.Permissions(permissions=8)
        invite_url = discord.utils.oauth_url(self.bot.user.id, permissions=permissions)
        await ctx.send(f"Invite me by this link: {invite_url}")

