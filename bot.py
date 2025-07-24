import discord
from discord.ext import commands
from discord import app_commands
import datetime
from datetime import datetime as dt
import httpx
import aiohttp
import urllib.parse

DISCORD_BOT_TOKEN = "YOUR_BOT_TOKEN"
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
    await bot.add_cog(GuildStats(bot))
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
    embed.add_field(name="/stats", value="View Hypixel stats (BedWars, SkyWars, Duels)", inline=False)
    embed.add_field(name="/guildstats", value="View Guild Stats (Guild Stats, Player Guild Stats)", inline=False)
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
# 🟡 Hypixel Stats
# --------------------------

async def get_uuid(username):
    url = f"https://api.mojang.com/users/profiles/minecraft/{username}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == 200:
            return response.json()["id"]
        return None

async def fetch_stats(uuid):
    url = f"https://api.hypixel.net/player?key={HYPIXEL_API_KEY}&uuid={uuid}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == 200:
            return response.json().get("player", {}).get("stats", {})
        return None

@tree.command(name="stats", description="Get Hypixel stats for BedWars, SkyWars, or Duels")
@app_commands.describe(game="The game mode: bedwars, skywars, duels", username="Minecraft username")
async def stats(interaction: discord.Interaction, game: str, username: str):
    await interaction.response.defer()
    game = game.lower()

    uuid = await get_uuid(username)
    if not uuid:
        await interaction.followup.send("❌ Could not find UUID for that username.")
        return

    all_stats = await fetch_stats(uuid)
    if not all_stats:
        await interaction.followup.send("❌ Failed to fetch data from Hypixel API.")
        return

    embed = discord.Embed(title=f"📊 {game.title()} Stats for {username}", color=discord.Color.purple())

    if game == "bedwars":
        stats = all_stats.get("Bedwars", {})
        embed.add_field(name="Wins", value=stats.get("wins_bedwars", 0), inline=True)
        embed.add_field(name="Losses", value=stats.get("losses_bedwars", 0), inline=True)
        embed.add_field(name="Kills", value=stats.get("kills_bedwars", 0), inline=True)
        embed.add_field(name="Deaths", value=stats.get("deaths_bedwars", 0), inline=True)
        embed.add_field(name="Final Kills", value=stats.get("final_kills_bedwars", 0), inline=True)
        embed.add_field(name="Final Deaths", value=stats.get("final_deaths_bedwars", 0), inline=True)
        embed.add_field(name="Beds Broken", value=stats.get("beds_broken_bedwars", 0), inline=True)
        embed.add_field(name="Beds Lost", value=stats.get("beds_lost_bedwars", 0), inline=True)

    elif game == "skywars":
        stats = all_stats.get("SkyWars", {})
        embed.add_field(name="Wins", value=stats.get("wins", 0), inline=True)
        embed.add_field(name="Losses", value=stats.get("losses", 0), inline=True)
        embed.add_field(name="Kills", value=stats.get("kills", 0), inline=True)
        embed.add_field(name="Deaths", value=stats.get("deaths", 0), inline=True)
        embed.add_field(name="Souls Collected", value=stats.get("souls_gathered", 0), inline=True)
        embed.add_field(name="Coins", value=stats.get("coins", 0), inline=True)

    elif game == "duels":
        stats = all_stats.get("Duels", {})
        embed.add_field(name="Wins", value=stats.get("wins", 0), inline=True)
        embed.add_field(name="Losses", value=stats.get("losses", 0), inline=True)
        embed.add_field(name="Kills", value=stats.get("kills", 0), inline=True)
        embed.add_field(name="Deaths", value=stats.get("deaths", 0), inline=True)
        embed.add_field(name="Games Played", value=stats.get("games_played_duels", 0), inline=True)
        embed.add_field(name="Winstreak", value=stats.get("current_winstreak", 0), inline=True)

    else:
        await interaction.followup.send("❌ Invalid game. Choose one of: `bedwars`, `skywars`, `duels`.")
        return

    await interaction.followup.send(embed=embed)


class GuildStats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="guildstats", description="Get guild stats or member info from Hypixel guild")
    @app_commands.describe(guild_name="The name of the guild", username="Optional Minecraft username in the guild")
    async def guildstats(self, interaction: discord.Interaction, guild_name: str, username: str = None):
        await interaction.response.defer()

      
        url = f"https://api.hypixel.net/guild?key={HYPIXEL_API_KEY}&name={urllib.parse.quote(guild_name)}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    await interaction.followup.send("❌ Failed to fetch data from Hypixel API.")
                    return

                data = await response.json()

        if not data.get("success") or not data.get("guild"):
            await interaction.followup.send(f"❌ Guild `{guild_name}` not found on Hypixel.")
            return

        guild = data["guild"]

        # Guild info
        guild_name = guild.get("name", "N/A")
        level = guild.get("level", "N/A")
        master = guild.get("master", "N/A")
        exp = guild.get("exp", 0)
        created_timestamp = guild.get("created")
        members = guild.get("members", [])

        created_str = "N/A"
        if created_timestamp:
            created_str = f"<t:{int(created_timestamp / 1000)}:D>"  

      
        if username:
            member = None
            username_lower = username.lower()
            for m in members:
             
                pass

      

            # Fetch UUID for given username
            async with aiohttp.ClientSession() as session:
                mojang_url = f"https://api.mojang.com/users/profiles/minecraft/{username}"
                async with session.get(mojang_url) as r:
                    if r.status == 200:
                        mojang_data = await r.json()
                        user_uuid = mojang_data.get("id")
                    else:
                        await interaction.followup.send(f"❌ Could not find Minecraft user `{username}`.")
                        return

            member = next((m for m in members if m.get("uuid") == user_uuid), None)
            if not member:
                await interaction.followup.send(f"❌ Member `{username}` not found in guild `{guild_name}`.")
                return

            joined_str = "N/A"
            if "joined" in member:
                joined_str = f"<t:{int(member['joined'] / 1000)}:D>"

            exp_contributed = member.get("exp", 0)

            embed = discord.Embed(
                title=f"👤 {username} in {guild_name}",
                color=discord.Color.green()
            )
            embed.add_field(name="Joined", value=joined_str, inline=True)
            embed.add_field(name="EXP Contributed", value=f"{exp_contributed:,}", inline=True)

            await interaction.followup.send(embed=embed)
            return
            
        embed = discord.Embed(
            title=f"📊 Guild Stats: {guild_name}",
            color=discord.Color.blue()
        )
        embed.add_field(name="🧪 Level", value=level, inline=True)
        embed.add_field(name="👥 Members", value=len(members), inline=True)
        embed.add_field(name="📅 Created", value=created_str, inline=True)
        embed.add_field(name="🧑 Master", value=master, inline=True)
        embed.add_field(name="🌟 Total EXP", value=f"{exp:,}", inline=True)

        await interaction.followup.send(embed=embed)



# --------------------------
# 🔓 Run the bot
# --------------------------

bot.run(DISCORD_BOT_TOKEN)
