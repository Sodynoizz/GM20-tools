import discord
from discord.ext import commands

class Purge(commands.Cog):
    def __init__(self , bot : commands.AutoShardedBot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(self.__class__.__name__)
        
    @discord.commands.slash_command(name = "ลบข้อความ", description = "ล้างข้อความใน channel นั้นๆ")
    async def purge(self , ctx : discord.ApplicationContext , amount : discord.commands.Option(int , name = "จำนวนข้อความ" , description = "ใส่จำนวนข้อความที่ต้องการจะลบ" , required = True)):
        await ctx.channel.purge(limit=amount)
        await ctx.respond(content = f"ลบข้อความใน channel : {ctx.channel.mention} นี้เเล้วจำนวน : `{amount}` ข้อความ" , delete_after = 5)

def setup(bot : commands.AutoShardedBot):
    bot.add_cog(Purge(bot))