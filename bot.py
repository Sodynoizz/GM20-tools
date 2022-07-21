import discord
from discord.ext import commands
from discord.gateway import DiscordWebSocket
from secret.keys import BOT_TOKEN 
from utility.mobilestatus import Status

class MyBot(commands.AutoShardedBot):    
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(command_prefix = commands.when_mentioned_or("uwu") , case_insensitive = True , help_command = None , intents = intents)
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.user} is ready!")

bot = MyBot()
bot.load_extensions('src.clear', 
                    'src.events', 
                    'src.help', 
                    'src.order', 
                    'src.report', 
                    'src.stats', 
                    'src.stock', 
                    'src.utils',
                    'src.faq',
                    'src.friends')
    
DiscordWebSocket.identify = Status.identify
bot.run(BOT_TOKEN)