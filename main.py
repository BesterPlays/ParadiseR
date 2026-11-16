import os
import discord
from discord import app_commands
from discord.ext import commands

TOKEN = "MTU0MzAzNTYzMTA2MjYxODIyMw.GPg8FD.nWsLkHHJvWaN_KIIjtvqomGT6pBqO_mnRU4EvU"
DISCORD_URL = "discord.gg/4EWvEqmAcc"
INVITE = DISCORD_URL    
TOOL_NAME = "PARADISE"

try:
    with open("msg.txt", "r", encoding="utf-8") as f:
        ANNOUNCEMENT = f.read().strip()
except FileNotFoundError:
    ANNOUNCEMENT = "msg.txt file not found!"

bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())


class ConfirmView(discord.ui.View):
    def __init__(self, owner_id, no_ad, no_ping):
        super().__init__(timeout=60)
        self.owner_id = owner_id
        self.no_ad = no_ad
        self.no_ping = no_ping

    @discord.ui.button(label="Confirm?", style=discord.ButtonStyle.danger)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.owner_id:
            return await interaction.response.send_message("This confirmation isn't yours.", ephemeral=True)

        button.disabled = True
        base_text = ANNOUNCEMENT if self.no_ad else f"{ANNOUNCEMENT}\n{INVITE}"
        
        await interaction.response.edit_message(view=self)

        try:
            for _ in range(5):
                await interaction.followup.send(base_text, allowed_mentions=discord.AllowedMentions.none())
        except discord.HTTPException as error:
            await interaction.followup.send(f"Discord API error: {error}", ephemeral=True)

        self.stop()

    async def on_timeout(self):
        for item in self.children:
            item.disabled = True


@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Online as {bot.user}")
    print("Slash commands synchronized.")
    print(f"Tool: {TOOL_NAME}")
    print(f"Discord: {DISCORD_URL}")


@bot.tree.command(name="r4id", description="r4ids a server")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.describe(no_ad="Remove the advertisement", no_ping="Disable everyone ping")
async def r4id(interaction: discord.Interaction, no_ad: bool = False, no_ping: bool = False):
    embed = discord.Embed(
        title="/r4id command", 
        description=f"**No ad:** {no_ad}\n\n**No ping:** {no_ping}", 
        color=discord.Color.red()
    )
    await interaction.response.send_message(embed=embed, view=ConfirmView(interaction.user.id, no_ad, no_ping), ephemeral=True)

bot.run(TOKEN)