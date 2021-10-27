import discord
from discord.ext import commands
import random
import os
import asyncio
import datetime

client = commands.Bot(command_prefix="+")

@client.event
async def on_ready():
    print("Bot Ready")


#giveaway command
@client.command()
@commands.guild_only()
@commands.has_permissions(manage_channels=True)
async def giveaway(ctx, duration: int, *, prize: str):
    embed = discord.Embed(title=prize,
                          description=f"Hosted by - {ctx.author.mention}\nReact with :tada: to enter!\nTime Remaining: **{duration}** seconds",
                          color=ctx.guild.me.top_role.color, )

    msg = await ctx.channel.send(content=":tada: **GIVEAWAY** :tada:", embed=embed)
    await msg.add_reaction("🎉")
    await asyncio.sleep(10)
    new_msg = await ctx.channel.fetch_message(msg.id)

    user_list = [u for u in await new_msg.reactions[0].users().flatten() if u != client.user] # Check the reactions/don't count the bot reaction

    if len(user_list) == 0:
        await ctx.send("No one reacted.") 
    else:
        winner = random.choice(user_list)
        e = discord.Embed()
        e.title = "Giveaway ended!"
        e.description = f"You won:"
        e.timestamp = datetime.datetime.utcnow()
        await ctx.send(f"{winner.mention}", embed=e)

#command for test bot working or not
@client.command(pass_context=True)
async def ping(ctx):
    await ctx.send("Pong!")

token = os.environ.get("TOKEN") #paste token on secrets
client.run(token)
