import discord
from discord.ext import commands, tasks
import aiohttp
from datetime import datetime
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
API_URL = os.getenv("API_URL")
NEWS_CHANNEL_ID = int(os.getenv("NEWS_CHANNEL_ID"))

# Set up Discord bot intents and command prefix
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Custom emojis
peppino = "<:peppino:1384575766842577036>"

# Down services list
down_services = {}

@bot.command()
async def test(ctx):
    """Send a test embed simulating a down service."""
    current_time = datetime.now().strftime('%H:%M:%S')
    image_url = "https://cdn.discordapp.com/app-icons/1384568070072172714/d8c81fd0f89d09d4d83c940c2f3c2d11.png?size=512"
    embed = discord.Embed(
        title=f"PeppinoChecker - {current_time}",
        description="-------------------------------------------------------------------------------------",
        color=discord.Color.red(),
        timestamp=datetime.now()
    )
    # Example down service data
    embed.add_field(name="Service", value="webserver", inline=True)
    embed.add_field(name="Action", value="check_http", inline=True)
    embed.add_field(name="STDOUT", value="Connection refused", inline=True)
    embed.set_image(url=image_url)
    await ctx.send(embed=embed)

@bot.event
async def on_ready():
    print(f"Bot connected as {bot.user}")
    channel = bot.get_channel(NEWS_CHANNEL_ID)
    if channel:
        embed = discord.Embed(
            title=f"{peppino} **PEPPINO IS ONLINE!** {peppino}",
            description=(
                "Peppino is now active and monitoring your services!\n"
                "If any service goes down, you'll get an alert right here.\n\n"
                "This channel has been set as the **news channel**! 📢"
            ),
            color=discord.Color.green()
        )
        embed.set_footer(text="Peppino Bot is ready to monitor 👀")
        await channel.send(embed=embed)

@tasks.loop(seconds=60)
async def send_news():
    channel = bot.get_channel(NEWS_CHANNEL_ID)
    if not channel:
        print("Channel not found!")
        return

    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL) as response:
            data = await response.json()

    c = datetime.now()
    current_time = c.strftime('%H:%M:%S')
    fields = []
    image_url = "https://cdn.discordapp.com/app-icons/1384568070072172714/d8c81fd0f89d09d4d83c940c2f3c2d11.png?size=512"

    try:
        services = data['rounds'][-1]['services']
    except (KeyError, IndexError):
        return

    # New: track currently down services
    currently_down = set()
    for service in services:
        checks = service.get('checks', [])
        is_down = False
        for check in checks:
            if check.get('exitCode') != 101:
                is_down = True
                break
        if is_down:
            currently_down.add(service.get('shortname', ''))

    # Notify when services come back online
    for svc in list(down_services):
        if svc not in currently_down:
            # Service is back online
            embed = discord.Embed(
                title=f"{peppino} Service ONLINE",
                description=f"The service `{svc}` is back online at {current_time}!",
                color=discord.Color.green(),
                timestamp=datetime.now()
            )
            await channel.send(embed=embed)
            del down_services[svc]

    # Notify down services (as before)
    for service in services:
        checks = service.get('checks', [])
        services_emb = []
        actions_emb = []
        stdout_emb = []
        is_down = False

        for check in checks:
            if check.get('exitCode') != 101:
                services_emb.append(service.get('shortname', ''))
                actions_emb.append(check.get('action', ''))
                stdout_emb.append(check.get('stdout', ''))
                is_down = True

        if is_down:
            down_services[service.get('shortname', '')] = True

        if services_emb:
            fields.append({
                'name': "Service",
                'value': "\n".join(services_emb),
                'inline': True
            })
            fields.append({
                'name': "Action",
                'value': "\n".join(actions_emb),
                'inline': True
            })
            fields.append({
                'name': "STDOUT",
                'value': "\n".join(stdout_emb),
                'inline': True
            })

    if fields:
        embed = discord.Embed(
            title=f"PeppinoChecker - {current_time}",
            description="-------------------------------------------------------------------------------------",
            color=discord.Color.red(),
            timestamp=datetime.now()
        )
        for field in fields:
            embed.add_field(name=field['name'], value=field['value'], inline=field['inline'])
        embed.set_image(url=image_url)
        await channel.send(embed=embed)

bot.run(BOT_TOKEN)