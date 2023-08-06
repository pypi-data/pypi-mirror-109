# discord-Economy
##### ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ Makes Economy much easier
___
##### discord_economy.Client(db='discord_economy', db_cluster='Economy', mongo_datebase='localhost:27017', Guild_only=False)

###  Example 
```py
import discord, discord_economy, random
from discord.ext.commands import Bot

eco_discord = discord_economy.Client()
bot = Bot(command_prefix='e!')

@bot.event
async def on_ready(): 
     print(f'{bot.user.name} is online | e!help')
 
 @bot.command()
 async def work(self, ctx):
    amount = random.randint(1, 50)
    eco_discord.work(amount, ctx.author.id)
    await ctx.send(f'You worked and gained ${amount}')
    

```

## Functions
  if guild_only is set to true then the economy will be guild only instead of global
  discord_economy.Client().work(amount, user_id) # Gain more money

  discord_economy.Client().deposit(amount, user_id) # deposit the money to the bank

  discord_economy.Client().withdraw(amount, user_id) # withdraw the money from the bank

  discord_economy.Client().get_cash(user_id) #How much cash they have

  discord_economy.Client().get_bank(amount, user_id) #Gets the bank value

  discord_economy.Client().get_network(amount, user_id) # Cash + Bank = Network
[Discord Server](https://discord.gg/GcHFjejEWR)