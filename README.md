# BhaluBot
BhaluBot develop by lord-sakshyam <br> BhaluModBot — A reliable and easy-to-use moderation bot for Discord. Quickly clean messages, clear channels, view moderation logs, and access core commands all in one place. Designed to help admins and moderators keep their servers organized and safe.
<br>
commands in this bot:-
<br>
<h4>/clear [amount] <br>
  
Description: Deletes the specified number of recent messages in the channel, regardless of who sent them. <br
                                                                                                            
Usage: /clear 5 → deletes the last 5 messages in the channel. <br>

Note: The command will also delete its own message after running. <br>

Permissions Needed: Manage Messages <br
                                      
Limit: Can only delete messages from the last 14 days due to Discord rules. </h4>
<br>
<h4>/clean [@user] [amount] <br>
  
Description: Deletes a specific number of messages sent by a mentioned user in the current channel. <br>

Usage: /clean @username 3 → deletes 3 messages sent by @username. <br>

Note:
Works only in the current channel. <br>

It won’t delete other users' messages except the given username one. <br>

It might include your messages if you're the user being cleaned.
</h4>

<h4>/core <br>
  
Description: Displays a list of all available commands that the bot can perform. <br
                                                                                   
Usage: Simply type /core <br>

Example Output: <br>

/clear — Clear messages <br>

/clean — Clean user messages <br>

/logs — Check user logs <br>

/core — Show this help menu <br> </h4>

<h4>/logs @user <br>
Description: Shows log details or past actions (like message deletions, joins, leaves, or warnings) of a specific user. <br>
Usage: /logs @username — displays logs related to @username <br>
Note: You must mention the user. Admin-only command in most setups.</h4>
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



