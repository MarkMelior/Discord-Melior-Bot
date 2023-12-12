import nextcord
from nextcord.ext import commands
import config

intents = nextcord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='+', intents=intents)

@bot.command()
async def test(ctx, arg):
    await ctx.send(arg)
    
bot.load_extension('cogs.command.chat')
@bot.event
async def on_ready():
    print('Ready')

# ЗАПУСК БОТА
bot.run( config.TOKEN )