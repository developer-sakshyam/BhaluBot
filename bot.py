import discord
from discord.ext import commands
from discord import app_commands
import datetime
import httpx
from discord import app_commands


DISCORD_BOT_TOKEN = "YOUR_DISCORD_BOT_TOKEN"
HYPIXEL_API_KEY = "YOUR_HYPIXEL_API"

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
    print(f"✅ Logged in as {bot.user}")

# --------------------------
# 📘 Moderation Commands
# --------------------------

@tree.command(name="clean", description="Clean specific user's messages")
@app_commands.describe(user="User to delete messages from", amount="Amount of messages to delete")
async def clean(interaction: discord.Interaction, user: discord.User, amount: int):
    if not interaction.channel.permissions_for(interaction.user).manage_messages:
        await interaction.response.send_message("You don't have permission to do that.", ephemeral=True)
        return

    await interaction.response.defer(ephemeral=True)
    deleted = []
    async for msg in interaction.channel.history(limit=100):
        if msg.author == user:
            deleted.append(msg)
        if len(deleted) >= amount:
            break

    for msg in deleted:
        await msg.delete()

    await interaction.followup.send(f"✅ Deleted {len(deleted)} messages from {user.mention}.", ephemeral=True)

@tree.command(name="clear", description="Delete the last N messages from this channel")
@app_commands.describe(amount="Number of recent messages to delete")
async def clear(interaction: discord.Interaction, amount: int):
    await interaction.response.defer(thinking=True)
    deleted = await interaction.channel.purge(limit=amount + 1)
    await interaction.followup.send(f"🧹 Deleted {len(deleted)-1} messages", ephemeral=True)

@tree.command(name="core", description="View core bot commands")
async def core(interaction: discord.Interaction):
    embed = discord.Embed(title="📘 Core Commands", color=0x3498db)
    embed.add_field(name="/clean", value="Delete a user's messages", inline=False)
    embed.add_field(name="/clear", value="Delete last N messages", inline=False)
    embed.add_field(name="/logs", value="View moderation history", inline=False)
    embed.add_field(name="/stats", value="View BedWars stats from Hypixel", inline=False)
    await interaction.response.send_message(embed=embed, ephemeral=True)

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

# --------------------------
# 🟡 Hypixel BedWars Stats
# --------------------------

async def get_uuid(username):
    url = f"https://api.mojang.com/users/profiles/minecraft/{username}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == 200:
            data = response.json()
            return data["id"]
        return None

async def get_bedwars_stats(uuid):
    url = f"https://api.hypixel.net/player?key={HYPIXEL_API_KEY}&uuid={uuid}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == 200:
            data = response.json()
            stats = data.get("player", {}).get("stats", {}).get("Bedwars", {})
            return {
                "wins": stats.get("wins_bedwars", 0),
                "losses": stats.get("losses_bedwars", 0),
                "kills": stats.get("kills_bedwars", 0),
                "deaths": stats.get("deaths_bedwars", 0),
                "final_kills": stats.get("final_kills_bedwars", 0),
                "final_deaths": stats.get("final_deaths_bedwars", 0),
                "beds_broken": stats.get("beds_broken_bedwars", 0),
                "beds_lost": stats.get("beds_lost_bedwars", 0),
            }
        return None

@tree.command(name="stats", description="Get Hypixel stats")
@app_commands.describe(game="The game mode (e.g., bedwars)", username="Minecraft username")
async def stats(interaction: discord.Interaction, game: str, username: str):
    await interaction.response.defer()

    uuid = await get_uuid(username)
    if not uuid:
        await interaction.followup.send("❌ Could not find UUID for that username.")
        return

    stats = await get_bedwars_stats(uuid)
    if not stats:
        await interaction.followup.send("❌ Error fetching BedWars stats.")
        return

    embed = discord.Embed(
        title=f"🏆 BedWars Stats for {username}",
        color=discord.Color.gold()
    )
    embed.add_field(name="Wins", value=stats["wins"], inline=True)
    embed.add_field(name="Losses", value=stats["losses"], inline=True)
    embed.add_field(name="Kills", value=stats["kills"], inline=True)
    embed.add_field(name="Deaths", value=stats["deaths"], inline=True)
    embed.add_field(name="Final Kills", value=stats["final_kills"], inline=True)
    embed.add_field(name="Final Deaths", value=stats["final_deaths"], inline=True)
    embed.add_field(name="Beds Broken", value=stats["beds_broken"], inline=True)
    embed.add_field(name="Beds Lost", value=stats["beds_lost"], inline=True)

    await interaction.followup.send(embed=embed)

# --------------------------
# 🔓 Run the bot
# --------------------------

bot.run(DISCORD_BOT_TOKEN)
