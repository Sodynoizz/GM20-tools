import enum
import discord , json
from discord.ext import commands
import pytz , datetime
from matplotlib import pyplot as plt

class OrderModal(discord.ui.Modal):
    def __init__(self , bot : commands.AutoShardedBot):
        self.bot = bot
        super().__init__(title = "จองหนังสือ")
        self.add_item(discord.ui.InputText(label = "ใส่ชื่อของคุณ (ระบุชื่อ-นามสกุล) เป็นภาษาไทย" , style = discord.InputTextStyle.short , required = True))
        self.add_item(discord.ui.InputText(label = "ใส่ที่อยู่ที่ต้องการจัดส่งหนังสือ" , style = discord.InputTextStyle.paragraph , required = True))
        self.add_item(discord.ui.InputText(label = "ต้องการรับหนังสือ Zenith กี่เล่ม" , style = discord.InputTextStyle.short , required = False , value = 0))
        self.add_item(discord.ui.InputText(label = "ต้องการรับหนังสือ เอื้อมพระเกี้ยวเช้า กี่เล่ม" , style = discord.InputTextStyle.short , required = False , value = 0))
        self.add_item(discord.ui.InputText(label = "ต้องการรับหนังสือ เอื้อมพระเกี้ยวบ่าย กี่เล่ม" , style = discord.InputTextStyle.short , required = False , value = 0))
    async def checkargs(self , interaction : discord.Interaction , value) -> None:
        try:
            if value.isnumeric() is True:
                if "." in value:
                    return await interaction.response.send_message(content = "❌ **[Error]** : กรุณาระบุตัวเลขการรับหนังสือเป็นจำนวนเต็มเท่านั้น")
                return value
        except:
            return await interaction.response.send_message(content = "❌ **[Error]** : กรุณาระบุตัวเลขการรับหนังสือเป็นจำนวนเต็มเท่านั้น" , ephemeral = True)

    
    def current(self):
        tz = pytz.timezone('Asia/Bangkok')
        now1 = datetime.datetime.now(tz)
        month_name = 'x Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec'.split()[now1.month]
        thai_year = now1.year + 543
        time_str = now1.strftime('%H:%M:%S')
        return "%d %s %d %s"%(now1.day, month_name, thai_year, time_str) # 30 ตุลาคม 2560 20:45:30

    async def callback(self , interaction : discord.Interaction):
        # create dm room
        zenith = await self.checkargs(interaction , self.children[2].value)
        prakeawchaw = await self.checkargs(interaction , self.children[3].value)
        prakeawafternoon = await self.checkargs(interaction , self.children[4].value)
        
        try:
            description = f"```1.ชื่อผู้จัดส่ง : {self.children[0].value}\n2.ที่อยู่ : {self.children[1].value}\n3.จำนวนหนังสือ zenith ทั้งหมด : {zenith} เล่ม\n4.จำนวนหนังสือ เอื้อมพระเกี้ยวเช้า ทั้งหมด : {prakeawchaw} เล่ม\n5. จำนวนหนังสือ เอื้อมพระเกี้ยวบ่าย : {prakeawafternoon}```"
            embed = discord.Embed(title = "จองหนังสือ", description = description , color = discord.Colour.green())
            embed.set_thumbnail(url = interaction.user.avatar.url)
            embed.set_footer(text = f"สั่งจองโดย {interaction.user}")
        
            # queue ID system
            index = 0
            with open("database/queue.json", "r") as queue:
                data = json.load(queue)
                index = int(data["queue"]) + 1
                with open("database/queue.json", "w") as writeFile:
                    json.dump({"queue" : index}, writeFile)

            # add to footer embed
            embed.set_footer(text = f"หมายเลขการจอง (ID) : {index}" , icon_url = interaction.user.avatar.url)
            
            # add to history
            with open("database/history.txt", "a") as history:
                history.write(f"Order {index}: [{self.current()}]\t({self.children[0].value})\t->\tprakeawchaw : {prakeawchaw} books, prakeawafternoon : {prakeawafternoon} books, zenith : {zenith} books\n")
            
            #? admin room checking
            adminroom = self.bot.get_channel(982491688830369853)
            await adminroom.send(embed = embed)
            
            #? check interaction channel for
            if interaction.channel.id != 982301617959338074:
                await interaction.response.send_message(content = f"✅ ลูกค้า {interaction.user.mention} ได้ทำการจองหนังสือ zenith จำนวน `{zenith}` เล่ม , หนังสือเอื้อมพระเกี้ยวเช้า จำนวน `{prakeawchaw}` และหนังสือ เอื้อมพระเกี้ยวบ่าย จำนวน `{prakeawafternoon}` เล่ม เรียบร้อยแล้วครับ\nสามารถตรวจสอบรายการการจองหนังสือของท่านได้ที่ direct message ของท่าน" , ephemeral = True)
                return await interaction.user.send(embed = embed , content = f"รายการจองหนังสือของท่าน หมายเลข ID : `{index}`\nหากมีข้อผิดพลาดให้ติดต่อ admin ในห้อง <#982313955663937547> โดยด่วน\n📔 **Note** : หากต้องการยกเลิก order ให้รายงานในห้อง <#982313955663937547> ดังรูปแบบตัวอย่างข้างล่างนี้\n```ออเดอร์ ID : {index}\nต้องการ : ยกเลิกการจอง\nสาเหตุ : เนื่องจากสั่งหนังสือเกินจำนวนที่ต้องการ```")
            return await interaction.user.send(embed = embed)
        
        except:
            pass
        
class Order(commands.Cog):
    def __init__(self , bot : commands.AutoShardedBot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(self.__class__.__name__)
    
    @discord.commands.slash_command(name = "จองหนังสือ" , description = "ใช้คอมมานด์นี้เพื่อทำการจองหนังสือ")
    async def จองหนังสือ(self , ctx : discord.ApplicationContext):
        await ctx.response.send_modal(modal = OrderModal(self.bot))
    
    @discord.commands.slash_command(name = "ยกเลิกการจองหนังสือ" , description = "ใช้คอมมานด์นี้เพื่อทำการยกเลืกการจองหนังสือ")
    @discord.default_permissions(administrator = True)
    async def ยกเลิกการจองหนังสือ(self , ctx : discord.ApplicationContext , 
        order : discord.commands.Option(int , name = "หมายเลขรายการจอง" , description = "ใส่หมายเลขรายการจองที่ต้องการยกเลิก" , required = True)):
        gettext = ""
        with open("database/history.txt","r+") as f:
            new_f = f.readlines()
            f.seek(0)
            for line in new_f:
                if f"Order {order}" not in line:
                    f.write(line)
            f.truncate()
        await ctx.respond(content = f"✅ ยกเลิกการจองหนังสือเรียบร้อยเเล้ว รายการจองหนังสือของคุณคือ #{order}")

            
def setup(bot : commands.AutoShardedBot):
    bot.add_cog(Order(bot))