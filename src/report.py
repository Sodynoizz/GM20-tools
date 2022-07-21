import discord
from discord.ext import commands

class MyModal(discord.ui.Modal):
    def __init__(self , bot : commands.AutoShardedBot ,  *args , **kwargs):
        self.bot = bot
        super().__init__(title = "รายงานปัญหา")
        self.add_item(discord.ui.InputText(label = "อธิบายรายละเอียดของปัญหา" , style = discord.InputTextStyle.paragraph , placeholder = "พิมพ์ตรงนี้..."))
    
    async def callback(self , interaction : discord.Interaction):
        channel = self.bot.get_channel(982313955663937547)
        embed = discord.Embed(title = "ปัญหา" , description = f"```{self.children[0].value}```" , color = discord.Colour.red())
        embed.set_footer(text = "Requested by " + interaction.user.name , icon_url = interaction.user.avatar.url)
        if interaction.channel.id == channel.id:
            await channel.send(embed=embed)
        else:
            await interaction.response.send_message(content = "ปัญหาของคุณได้ถูกรายงานเเล้วที่ <#982313955663937547>" , ephemeral = True)
            await channel.send(embed=embed)

class Report(commands.Cog):
    def __init__(self , bot , *args , **kwargs):
        self.bot = bot
        super().__init__(*args , **kwargs)
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(self.__class__.__name__)
    
    @discord.commands.slash_command(name = "รายงานบัค" , description = "รายงานปัญหาบอท")
    async def report(self , ctx : discord.ApplicationContext):
        await ctx.interaction.response.send_modal(modal = MyModal(self.bot))

def setup(bot : commands.AutoShardedBot):
    bot.add_cog(Report(bot))