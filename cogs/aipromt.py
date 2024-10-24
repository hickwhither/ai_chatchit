import discord
from discord import *
from discord.ext import commands, tasks
import ollama

import time
import asyncio


MODEL = 'llama3.1:latest'

SYSTEM_PROMT = """
You will be participating in a conversation. You only need to print your own dialogue.  
Your tag is <@{id}> (This will appear when someone pings you)  
Your name is {name}.  
You speak in Vietnamese.  
Your sentence length should not exceed 2000 characters.  
If you want to ping someone, use <@id>.  

RESPONSE RULES:
- Don't overuse pings. Only ping if the person is not actively talking.
- Print only what you want to say (e.g., "Hello there").
- Remember, you do not print other people's dialogue. YOU ARE NOT THEM.
- If you want to stay silent, print '%SILENT%'.

Use these emojis as much as possible in your responses.  
IMPORTANT: You must print the entire emoji string for it to show. Example: "<:buon:1024698170799829104>"

<:cuoideu:950931929195216986>  
<:luom:950931749930680350>  
<:hmm:950931928561877012>  
<:buon:1024698170799829104>  
<:cuoilai:1032662061123129424>  
<:sek:1239232731532099664>  
<:sad:1239233500801138850>  
<:hetcuu:1242136607075602533>  
<:orz:951107217598316564>  
<:cuoilay:1267482041742659666>  
<:cute:950931928700293170>  
<:chem:916886913636524052>  
<:adu:1024698163333971988>  
<:anbongngo:936493828091834400>  
<:aww:950931928519938058>  
<:bu:1239233179060277248>  
<:mophat:906019701346418698>  
<:load:1024698167033344081>  
<:rokf:950607318922457128>  
<:aheg:945699029902319676>  
<:sus:952187167889817620>  
<:uwu:949960339036987462>  
<:lick:945239728628834304>  
<:cvm:1291031442993709203>  
<:catshake:1291031455140679690>
"""

EMOJIS = {
"cuoideu": "<:cuoideu:950931929195216986>",
"luom": "<:luom:950931749930680350>",
"hmm": "<:hmm:950931928561877012>",
"buon": "<:buon:1024698170799829104>",
"cuoilai": "<:cuoilai:1032662061123129424>",
"sek": "<:sek:1239232731532099664>",
"sad": "<:sad:1239233500801138850>",
"hetcuu": "<:hetcuu:1242136607075602533>",
"orz": "<:orz:951107217598316564>",
"cuoilay": "<:cuoilay:1267482041742659666>",
"cute": "<:cute:950931928700293170>",
"chem": "<:chem:916886913636524052>",
"adu": "<:adu:1024698163333971988>",
"anbongngo": "<:anbongngo:936493828091834400>",
"aww": "<:aww:950931928519938058>",
"bu": "<:bu:1239233179060277248>",
"mophat": "<:mophat:906019701346418698>",
"load": "<:load:1024698167033344081>",
"rokf": "<:rokf:950607318922457128>",
"aheg": "<:aheg:945699029902319676>",
"sus": "<:sus:952187167889817620>",
"uwu": "<:uwu:949960339036987462>",
"lick": "<:lick:945239728628834304>",
"cvm": "<:cvm:1291031442993709203>",
"catshake": "<:catshake:1291031455140679690>",
}

async def setup(bot) -> None:
    await bot.add_cog(AIPrompt(bot))


class AIPrompt(commands.Cog):
    chat_data: list
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.chat_data = [{'role': 'system', 'content': SYSTEM_PROMT.format(id=self.bot.user.id, name=self.bot.user.display_name)}]
        self.skipped_data = []
        self.channel_id = 1298636496915398736

        self.progressing_message = False
        self.last_message_time = 0
        self.texting.start()
    
    @commands.Cog.listener()
    async def on_message(self, message: Message):
        if message.channel.id != self.channel_id: return
        if message.author.bot: return
        
        content = f"user_id: {message.author.id} - name: ({message.author.name})\n{message.content}"
        data = {'role':'user', 'content':content}
        print(f"<@{message.author.id}> - {message.author.name} sent message")

        if self.progressing_message: self.skipped_data.append(data)
        else: self.chat_data.append(data)

    @tasks.loop(seconds=10)
    async def texting(self):
        if self.progressing_message: return
        if time.time() - self.last_message_time < 10: return

        self.chat_data += self.skipped_data
        self.skipped_data = []

        self.progressing_message = True

        channel = self.bot.get_channel(self.channel_id) or await self.bot.fetch_channel(self.channel_id)
        channel.typing()
        print("Đang load...")
        response = await asyncio.get_event_loop().run_in_executor(None, lambda: ollama.chat(MODEL, messages=self.chat_data, stream=False))
        print("Đã nhắn tin!")
        self.progressing_message = False
        self.last_message_time = time.time()
        
        
        result_message:str = response['message']['content']
        weird_prefix = f'<@{self.bot.user.id}> ({self.bot.user.display_name})'
        if result_message.startswith(weird_prefix): result_message=result_message[len(weird_prefix):]
        result_message = result_message.strip()

        if len(result_message)==0: return
        if '%SILENT%' not in result_message:
            await channel.send(content=result_message, mention_author=False)
        
        self.chat_data.append({'role':'assistant', 'content': result_message})