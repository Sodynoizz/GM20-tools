import discord
from discord.ext import commands
from typing import Optional

class Helper(commands.Cog):
    def __init__(self , bot : commands.AutoShardedBot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(self.__class__.__name__)
    
    help = discord.Bot().create_group(name="ช่วยเหลือ", description="ช่วยเหลือเกี่ยวกับการใช้งานบอท")
    
    def build_embed(self , title : str , description : str , image : Optional[str] = None) -> discord.Embed:
        embed = discord.Embed(title=title, description=description , color=0xffffff)
        if image is not None:
            embed.set_image(url = image)
        return embed

    @help.command(name = "ขั้นตอนการจอง" , description = "แสดงผลขั้นตอนการจองหนังสือ")
    async def help_booking(self , ctx : discord.ApplicationContext):
        title = "ช่วยเหลือเกี่ยวกับการจองหนังสือ"
        description = "**1.** พิมพ์คำว่า `/จองหนังสือ` ในห้อง <#982307879866474577>\n**2.** กรอกแบบฟอร์มที่ปรากฏขึ้นให้ครบถ้วน\n**3.** เมื่อกรอกเสร็จจะพบกับข้อความใน direct message ให้ตรวจสอบรายละเอียดการจองหนังสือของคุณให้ครบถ้วน หากมีข้อมูลที่กรอกผิดพลาดให้รีบแจ้ง Admin ห้อง <#982313955663937547> โดยด่วน\n\t__Note__ : วิธีการรายงานปัญหาด้านการกรอกข้อมูลผิดให้พิพม์คำสั่ง `/ช่วยเหลือ การรายงานปัญหา` เพือดูรูปแบบการรายงานเพิ่มเติม : \n**4.** หากคุณกรอกข้อมูลครบเเล้วและถูกต้องเเล้ว เป็นอันเสร็จสิ้นการจองหนังสือผ่านระบบนี้"
        embed = self.build_embed(title = title , description = description , image = "https://cdn.discordapp.com/attachments/780424031035457588/983024756926341160/5ad53e2e9da81977.png")
        await ctx.respond(embed=embed)
    
    @help.command(name = "การรายงานปัญหา" , description = "แสดงผลวิธีรายงานปัญหาการกรอกข้อมูลผิด")
    async def help_reporting(self , ctx : discord.ApplicationContext):
        title = "ช่วยเหลือเกี่ยวกับการรายงานปัญหา"
        description = f"หากกรอกข้อมูลผิดให้รายงานปัญหาที่ห้อง <#982313955663937547>\nรูปแบบ format การรายงานปัญหา [Example] :\n```ออเดอร์ ID : 1 (หาได้จากรูปภาพประกอบด้านล่างนี้)\nต้องการ : ยกเลิกการจอง\nสาเหตุ : เนื่องจากสั่งหนังสือเกินจำนวนที่ต้องการ```"
        embed = self.build_embed(title = title , description = description , image = "https://cdn.discordapp.com/attachments/975979987142320171/983022585589665842/IMG_0757.jpg")
        await ctx.respond(embed=embed)
    
def setup(bot):
    bot.add_cog(Helper(bot))