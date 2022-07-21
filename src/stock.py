import discord, json
from discord.ext import commands

def get_stats():
    with open("database/stock.json", "r" , encoding="utf8") as stock:
        data = json.load(stock)
        zenith = data["zenith"]
        prakeawchaw = data["prakeawchaw"]
        prakeawafternoon = data["prakeawafternoon"]
    return zenith , prakeawchaw , prakeawafternoon

class Stock(commands.Cog):
    def __init__(self , bot : commands.AutoShardedBot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(self.__class__.__name__)
    
    @discord.commands.slash_command(name = "รายการสินค้า" , description = "แสดงผลรายการสินค้า")
    async def stock(self , ctx : discord.ApplicationContext):
        zenith , prakeawchaw , prakeawafternoon = get_stats()
        embed = discord.Embed(title = "คลังสินค้า" , color = discord.Colour.green())
        embed.add_field(name = f"1. {zenith['name']}" , value = f"```รายละเอียด : {zenith['description']}\nราคา : {zenith['price']}\nในคลัง : {zenith['in-stock']}\n```" , inline = False)
        embed.add_field(name = f"2. {prakeawchaw['name']}" , value = f"```รายละเอียด : {prakeawchaw['description']}\nราคา : {prakeawchaw['price']}\nในคลัง : {prakeawchaw['in-stock']}\n```" , inline = False)
        embed.add_field(name = f"3. {prakeawafternoon['name']}" , value = f"```รายละเอียด : {prakeawafternoon['description']}\nราคา : {prakeawafternoon['price']}\nในคลัง : {prakeawafternoon['in-stock']}\n```" , inline = False)
        embed.add_field(name = "ประกาศจาก TU85 [GM20]" , value = "`None`" , inline = False)
        embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/982317337250263090/982574785768857600/58316.jpg")
        await ctx.respond(embed=embed)
    
def setup(bot : commands.AutoShardedBot):
    bot.add_cog(Stock(bot))