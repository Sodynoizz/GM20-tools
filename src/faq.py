import discord
import json
from discord.ext import commands

async def get_faq():
    with open("database/faq.json", "r", encoding="utf-8") as faq:
        data = json.load(faq)

        #? question 1
        question1 = data["FAQ1"]["Question"]
        answer1 = data["FAQ1"]["Answer"]
        
        #? question 2
        question2 = data["FAQ2"]["Question"]
        answer2 = data["FAQ2"]["Answer"]
        
        #? question 3
        question3 = data["FAQ3"]["Question"]
        answer3 = data["FAQ3"]["Answer"]        
        
        return question1, answer1, question2, answer2, question3, answer3

class FAQ(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(self.__class__.__name__)
        
    @discord.commands.slash_command(name = "faq",description = "ปัญหาที่พบบ่อย")
    async def faq(self, ctx: discord.ApplicationContext):
        question1, answer1, question2, answer2, question3, answer3 = await get_faq()
        embed = discord.Embed(title = "FAQ" , description = "รายการปัญหาที่พบบ่อย", color = 0xffffff)
        embed.add_field(name = f"Question 1", value = f"```fix\n{question1}\nตอบ {answer1}```", inline = False)
        embed.add_field(name = f"Question 2", value = f"```yaml\n{question2}\nตอบ {answer2}```", inline = False)
        embed.add_field(name = f"Question 3", value = f"```{question3}\nตอบ {answer3}```", inline = False)
        await ctx.respond(embed=embed, ephemeral = True)

def setup(bot: commands.AutoShardedBot):
    bot.add_cog(FAQ(bot))