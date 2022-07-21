import discord
import json
from discord.ext import commands, pages

def get_list():
    mapping = {}
    with open("database/friends.json", "r", encoding="utf8") as friend:
        data = json.load(friend)
        for index in range(1, 45):
            mapping[index] = dict(
                name = data[f"{index}"]["name"],
                nickname = data[f"{index}"]["nickname"],
                instragram = data[f"{index}"]["instragram"],
                link = data[f"{index}"]["link"]
            )
    return mapping

class Friends(commands.Cog):
    def __init__(self, bot : commands.AutoShardedBot):
        self.bot = bot
        self.pages = []    

    def build_pages(self) -> list:
        self.pages = []
        mapping = get_list()
        for index in range(1, 45):
            embed = discord.Embed(title= "สมาชิก GM20", description= "รายชื่อเด็ก gifted-math 20 โรงเรียนเตรียมอุดมศึกษา", color=discord.Colour.green())
            embed.add_field(name="ชื่อจริง นามสกุล",value=f"> {mapping[index]['name']}", inline=False)
            embed.add_field(name="ชื่อเล่น",value=f"> {mapping[index]['nickname']}", inline=False)
            embed.add_field(name="Instragram",value=f"> {mapping[index]['instragram']}", inline=False)
            embed.add_field(name="ลิงค์", value=f"> [`Click Here`]({mapping[index]['link']})", inline=False)
            embed.set_footer(text=f"Page : {index}/44")
            self.pages.append(embed)
        return self.pages
             
    @commands.Cog.listener()
    async def on_ready(self):
        print(self.__class__.__name__)
        
    @discord.commands.slash_command(name= "giftedmath", description= "แสดงรายชื่อ gifted math")
    async def gm(self, ctx: discord.ApplicationContext):
        paginator = pages.Paginator(
            pages=self.build_pages(),
            use_default_buttons=False,
            loop_pages=True,
            show_disabled=True,
            timeout=None
        )  
        paginator.add_button(pages.PaginatorButton(button_type="first", emoji="⏪", style=discord.ButtonStyle.secondary, loop_label="⏪"))
        paginator.add_button(pages.PaginatorButton(button_type="second", emoji="⬅️",style=discord.ButtonStyle.secondary, loop_label="⬅️"))
        paginator.add_button(pages.PaginatorButton(button_type="page_indicator", style=discord.ButtonStyle.primary, disabled=True))
        paginator.add_button(pages.PaginatorButton(button_type="next", emoji= "➡️", style=discord.ButtonStyle.secondary, loop_label="➡️"))
        paginator.add_button(pages.PaginatorButton(button_type="last", emoji= "⏩", style=discord.ButtonStyle.secondary, loop_label="⏩"))
        await paginator.respond(ctx.interaction, ephemeral=False)

def setup(bot : commands.AutoShardedBot):
    bot.add_cog(Friends(bot))