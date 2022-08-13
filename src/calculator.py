import discord
from discord.ext import commands
import js2py
from typing import Union

class DeleteMsg(discord.ui.View):
    def __init__(self, author: Union[discord.Member, discord.User], *args, **kwargs):
        self.author = author
        super().__init__(timeout = 30 , *args, **kwargs)
    
    @discord.ui.button(label= "Delete", emoji = "<:delete:1007971748886622240>" , style = discord.ButtonStyle.danger)
    async def callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.message.delete()
        self.stop()
    
    async def interaction_check(self, interaction: discord.Interaction):
        return self.author == interaction.user
    
    async def on_timeout(self) -> None:
        await self.message.edit(content= "⏰ Timed Out...", embed=None, view=None)
        
class Calculator(commands.Cog):
    def __init___(self, bot: commands.AutoShardedBot):
        self.bot = bot
    
    def exp_decorator(self, expression:str) -> str:
        return f"```yaml\n{expression}```"

    def res_decorator(self, res: Union[str, int]) -> str:
        return f"```fix\n{res}```"
    
    def make_embed(self , expression: str, res: str, author: Union[discord.Member, discord.User]) -> discord.Embed:
        embed = discord.Embed(title= 'Calculator Command')
        embed.color = 0xffffff
        if res == 'Error :(':
            embed.color = 0xff0000
            embed.add_field(name= "[Error] - Invalid Expression" , value = "** ** ", inline = True)
            return embed
        
        embed.add_field(name= "Expression", value = self.exp_decorator(expression), inline = False)
        embed.add_field(name= "Result" , value = self.res_decorator(res) , inline = False)
        embed.set_footer(text = f"Requested by {author.name}", icon_url = author.avatar.url)
        return embed
            
    @commands.Cog.listener()
    async def on_ready(self):
        print(self.__class__.__name__)
    
    @discord.commands.slash_command(name = "calculator" , description = "เครื่องคิดเลข")
    async def calc(self, ctx: discord.ApplicationContext, expression: str):
        eval_result, calculator = js2py.run_file("utility/calculator.js")
        result = calculator.calculate(expression)
        embed = self.make_embed(expression= expression, res= result, author = ctx.interaction.user)
        view = DeleteMsg(ctx.interaction.user)
        await ctx.respond(embed= embed , view = view)
        view.message = await ctx.interaction.original_message()
        
def setup(bot : commands.AutoShardedBot):
    bot.add_cog(Calculator(bot))
