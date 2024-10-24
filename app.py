import discord
from discord.ext.commands import Bot

import os
import time, random, string
import dotenv
dotenv.load_dotenv()


class BotChat(Bot):
    def __init__(self):
        super().__init__(
            command_prefix = 'ai.',
            intents = discord.Intents.all(),
            application_id = os.environ['APPLICATION_ID'],
            owner_ids = [
                403476178549211156, # Hick
            ]
        )
    
    async def setup_hook(self):
        for file in os.listdir('cogs'):
            if not file.startswith('_') and (os.path.exists(os.path.join('cogs', file)) or file.endswith('.py')):
                if file.endswith('.py'): file = file[:-3]
                try:
                    await self.load_extension(f'cogs.{file}')
                    print(f'✅ Loaded {file}')
                except Exception as e:
                    print(f'❌ Error {file}: {e}')

    async def on_ready(self):
        print(f'=== Logged as {self.user} ({self.user.id}) ===')
        self.start_time = time.time()
    
if __name__ == '__main__':
    bot = BotChat()
    bot.run(os.environ['TOKEN'])

