import discord, os, sys
from functions import *
import json
from discord.ext import commands



config = json.load(open("config.json", encoding="utf-8"))


def load_apps():
    
    apps = json.load(open("apps.json", encoding="utf-8"))
    applications = []
    for app in apps:
        applications.append(app)
        
    return applications

activity = discord.Activity(type=discord.ActivityType.watching, name = "api")
bot = commands.Bot(command_prefix = ">", intents = discord.Intents.all(), activity = activity)

@bot.event
async def on_ready():
    print()
    print(f"[+] {bot.user} is online.")


@bot.slash_command(guild_ids = [config["guildID"]], name="addapp", description="Add an application.")
async def addapp(ctx, sellerkey: discord.Option(str, "Keyauth application seller key", required = True)):
    
    if ctx.author.id not in config["whitelist"]:
        return await ctx.respond(embed = discord.Embed(description = f"You don't have permission to use this comamnd.", color = 0xFF0000))

    apps = json.load(open("apps.json", encoding="utf-8"))
    appName = app_info(sellerkey)
    if appName != False:
        data = {appName : sellerkey}
        
        apps.update(data)
        with open("apps.json", "w") as appdatafile:
            json.dump(apps, appdatafile, indent=4)

        await ctx.respond(embed = discord.Embed(description = f"Added `{appName}` to the database.", color = 0x4598d2))
    
    else:
        await ctx.respond(embed = discord.Embed(description = f"Failed to add `{appName}` to the database.", color = 0xFF0000))
    

@bot.slash_command(guild_ids = [config["guildID"]], name="hwidreset", description="Reset HWID of a user.")
async def hwidreset(ctx, application: discord.Option(str, choices = load_apps(), required = True), user: discord.Option(str, "Keyauth username.", required = True)):
    
    if ctx.author.id not in config["whitelist"]:
        return await ctx.respond(embed = discord.Embed(description = f"You don't have permission to use this comamnd.", color = 0xFF0000))
    
    sellerkey = json.load(open("apps.json", encoding="utf-8"))[application]
    message = reset_hwid(user, sellerkey)
    
    return await ctx.respond(embed = discord.Embed(description = message, color = 0x4598d2))


@bot.slash_command(guild_ids = [config["guildID"]], name="restart", description="Restarts the bot.")
async def restart(ctx):
    await ctx.respond(embed = discord.Embed(description = "Restarting...", color = 0x4598d2))
    os.execv(sys.executable, ['python'] + sys.argv)
    
    
    
bot.run(config['token'])
