import discord , json
import pandas as pd
from discord.ext import commands
from typing import Union
import matplotlib.pyplot as plt

class Confirm(discord.ui.View):
    def __init__(self , user_react : Union[discord.User , discord.Member]):
        self.user_react = user_react 
        super().__init__(timeout = 30)
    
    async def interaction_check(self , interaction : discord.Interaction):
        return interaction.user == self.user_react

    @discord.ui.button(label = "ยืนยัน" , style = discord.ButtonStyle.success)
    async def confirm(self , button : discord.ui.Button , interaction : discord.Interaction):
        with open("database/history.txt", "w") as history:
            history.write("ลำดับ            วันที่             ชื่อ               รายการสั่งซื้อ\n")
        
        with open("database/queue.json", "w") as writeFile:
            json.dump({"queue" : 0}, writeFile)
    
        self.confirm.disabled = True
        self.deny.disabled = True
        await interaction.response.edit_message(content = "✅ ลบประวัติการสั่งจองทั้งหมดเรียบร้อยแล้ว" , view = self)
        self.stop()
    
    @discord.ui.button(label = "ปฏิเสธ" , style = discord.ButtonStyle.danger)
    async def deny(self , button : discord.ui.Button , interaction : discord.Interaction):
        self.confirm.disabled = True
        self.deny.disabled = True
        await interaction.response.edit_message(content = "❌ ยกเลิกการลบประวัติการสั่งจองเรียบร้อยแล้ว" , view = self)
        self.stop()
    
    async def on_timeout(self):
        self.disable_all_items()
        await self.message.edit_original_message(content = "⏰ Timed out" , view = self)
          
class Stats(commands.Cog):
    def __init__(self , bot : commands.AutoShardedBot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(self.__class__.__name__)
            
    @discord.commands.slash_command(name = "ประวัติการสั่งจอง" , description = "เช็คประวัติการสั่งจอง")
    @discord.default_permissions(administrator = True)
    async def history(self , ctx : discord.ApplicationContext):
        file = discord.File("database/history.txt")
        try:
            await ctx.respond(file = file)
        except:
            member = ctx.interaction.guild.fetch_member(772023332865966092)
            member.send(content = f"{member.mention} Warning : You need to make a new file name 'history2.txt'.")

    @discord.commands.slash_command(name = "ลบประวัติการสั่งจอง" , description = "ลบประวัติการสั่งจองทั้งหมด")
    @discord.default_permissions(administrator = True)
    async def clear_history(self , ctx : discord.ApplicationContext):
        view = Confirm(ctx.interaction.user)
        view.message = await ctx.respond(content = "คุณแน่ใจที่จะ reset ประวัติการจองใช่หรือไม่ ?" , view = view)
        
def setup(bot : commands.AutoShardedBot):
    bot.add_cog(Stats(bot))