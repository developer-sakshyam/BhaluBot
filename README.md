# BhaluBot
---
Developed by lord-sakshyam

BhaluModBot is a reliable and easy-to-use moderation bot for Discord. It helps keep servers clean, safe, and well-managed with simple slash commands. Whether you're moderating a large server or running a private community, BhaluModBot has the tools you need.

---
🚀 Features
🔧 Quick message deletion

🧹 Clean messages from specific users

📜 View moderation logs

📌 Core help menu

📊 In-game stats via Hypixel API (e.g., /stats username:mr_bhalu)

---
Simple, lightweight, and effective

🛠️ Commands
/clear [amount]
Description:
Deletes the specified number of recent messages in the current channel.

Usage:
/clear 5 → Deletes the last 5 messages in the channel.

Notes:

Deletes its own message after execution.

Can only delete messages from the last 14 days (Discord API limitation).

Permissions Needed:
Manage Messages

/clean @user [amount]
Description:
Deletes a specific number of messages sent by the mentioned user in the current channel.

Usage:
/clean @username 3 → Deletes the last 3 messages from @username.

Notes:

Works only in the current channel.

Only deletes messages from the mentioned user.

---
/logs @user
Description:
Displays moderation logs or past actions for a specific user (e.g., deletions, joins, leaves).

Usage:
/logs @username

Note:
Admin-only command in most cases.

/core
Description:
Displays all available bot commands in a list.

Usage:
/core

Example Output:

bash
Copy
Edit
/clear — Clear messages  
/clean — Clean user messages  
/logs — Check user logs  
/core — Show this help menu  
/stats username:<IGN>
Description:
Fetches basic game statistics using the Hypixel API for Minecraft players.

---
Usage:
/stats game:bedwars username:mr_bhalu

Currently supports BedWars by default. Future updates may allow selecting other games.

✅ Required Bot Permissions
Make sure your bot has the following permissions:

Send Messages

Manage Messages

Embed Links

Read Message History

Use Slash Commands

---
<br>
<h2>****UPDATED**** </h2>
<br>
--<h4>ADDED #🧙 Hypixel BEDWARS Stats</h4>

A simple Discord bot that fetches and displays **Hypixel BEDWARS stats** using the official Hypixel API.

---

## ⚙️ Features

- 📊 `/stats` slash command to get Minecraft player BEDWARS stats  
- 🎮 Supports game-specific stats like Bedwars, Skywars, Duels, etc.  
- 🧠 Built with `discord.py` and `aiohttp`  
- 🌐 Uses Mojang API to resolve Minecraft UUID  
- 🔐 Uses your own Hypixel API key  

---



