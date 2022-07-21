import discord
from discord.ext import commands

class Event(commands.Cog):
    def __init__(self , bot : commands.AutoShardedBot):
        self.bot = bot
    
    async def getemote(self , arg):
        emoji = discord.utils.get(self.bot.emojis , name = arg.strip(":"))
        if emoji is not None:
            if emoji.animated:
                add = "a"
            else:
                add = ""
            return f"<{add}:{emoji.name}:{emoji.id}>"
    
    async def getinstr(self , content):
        ret = []
        
        space = content.split(" ")
        count = content.split(":")
        
        if len(count) > 1:
            for item in space:
                if item.count(":") > 1:
                    wr = ""
                    if item.startswith("<") and item.endswith(">"):
                        ret.append(item)
                    else:
                        count = 0
                        for i in item:
                            if count == 2:
                                aaa = wr.replace(" " , "")
                                ret.append(aaa)
                                wr = ""
                                count = 0
                            if i != ":":
                                wr += i
                            else:
                                if wr == "" or count == 1:
                                    wr += " : "
                                    count += 1
                                else:
                                    aaa = wr.replace(" ","")
                                    ret.append(aaa)
                                    wr = ":"
                                    count = 1
                        aaa = wr.replace(" " , "")
                        ret.append(aaa)
                else:
                    ret.append(item)   
        else:
            return content
        
        return ret
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(self.__class__.__name__)
        
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if ":" in message.content:
            msg = await self.getinstr(message.content)
            ret = ""
            em = False
            smth = message.content.split(":")
            if len(smth) > 1:
                for word in msg:
                    if word.startswith(":") and word.endswith(":") and len(word) > 1:
                        emoji = await self.getemote(word)
                        if emoji is not None:
                            em = True
                            ret += f" {emoji}"
                        else:
                            ret += f" {word}"
                    elif word.startswith("`:") and word.endswith(":`") and len(word) > 1:
                        emoji = await self.getemote(word)
                        em = True
                        ret = f"`{emoji}`"
                    else:
                        ret += f" {word}"
            else:
                ret += msg
            
            if em:
                webhooks = await message.channel.webhooks()
                webhook = discord.utils.get(webhooks , name = "Sodynoizz")
                if webhook is None:
                    webhook = await message.channel.create_webhook(name = "Sodynoizz")
                await webhook.send(ret , username = message.author.name , avatar_url = message.author.avatar.url) 
                await message.delete()

def setup(bot : commands.AutoShardedBot):
    bot.add_cog(Event(bot))