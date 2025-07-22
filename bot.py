import discord
from discord.ext import commands
from discord import app_commands
import datetime

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.messages = True
bot = commands.Bot(command_prefix="/", intents=intents)
tree = bot.tree

mod_logs = {}

@bot.event
async def on_ready():
    await tree.sync()
    print(f"Logged in as {bot.user}")

# /clean @user [amount] command
@tree.command(name="clean", description="Clean specific user's messages")
@app_commands.describe(user="User to delete messages from", amount="Amount of messages to delete (optional)")
async def clean(interaction: discord.Interaction, user: discord.User, amount: int):
    if not interaction.channel.permissions_for(interaction.user).manage_messages:
        await interaction.response.send_message("You don't have permission to do that.", ephemeral=True)
        return

    await interaction.response.defer(ephemeral=True)

    def is_target_user(m):
        return m.author == user

    deleted = []
    async for msg in interaction.channel.history(limit=100):
        if msg.author == user:
            deleted.append(msg)
        if len(deleted) >= amount:
            break

    for msg in deleted:
        await msg.delete()

    await interaction.followup.send(f"✅ Deleted {len(deleted)} messages from {user.mention}.", ephemeral=True)

# /clear command
@tree.command(name="clear", description="Delete the last N messages from this channel")
@app_commands.describe(amount="Number of recent messages to delete")
async def clear(interaction: discord.Interaction, amount: int):
    await interaction.response.defer(thinking=True)
    deleted = await interaction.channel.purge(limit=amount + 1)
    await interaction.followup.send(f"🧹 Deleted {len(deleted)-1} messages", ephemeral=True)

# /core command
@tree.command(name="core", description="View core bot commands")
async def core(interaction: discord.Interaction):
    embed = discord.Embed(title="📘 Core Commands", color=0x3498db)
    embed.add_field(name="/clean @user [amount]", value="Delete a user's messages", inline=False)
    embed.add_field(name="/clear [amount]", value="Delete last N messages", inline=False)
    embed.add_field(name="/logs @user", value="View moderation history", inline=False)
    await interaction.response.send_message(embed=embed, ephemeral=True)

# /logs @user
@tree.command(name="logs", description="View moderation logs for a user")
@app_commands.describe(user="User to check logs for")
async def logs(interaction: discord.Interaction, user: discord.User):
    embed = discord.Embed(title=f"📝 Mod Logs for {user.mention}", color=0xe74c3c)
    logs = mod_logs.get(user.id, [])
    
    if logs:
        for log in logs:
            embed.add_field(name=log['type'], value=f"{log['reason']} ({log['when']})", inline=False)
        embed.set_footer(text=f"Total Strikes: {len([l for l in logs if l['type'] == '⚠️ Warning'])}")
    else:
        embed.description = "No moderation logs found for this user."

    await interaction.response.send_message(embed=embed, ephemeral=True)

# database
@bot.command()
async def addlog(ctx, user: discord.User, type: str, *, reason: str):
    if user.id not in mod_logs:
        mod_logs[user.id] = []
    mod_logs[user.id].append({
        'type': type,
        'reason': reason,
        'when': f"{datetime.datetime.utcnow().strftime('%d %b %Y')}"
    })
    await ctx.send(f"Log added for {user.name}")

bot.run("YOUR_AUTH_TOKEN")
