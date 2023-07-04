import discord
from discord.ext import commands
from datetime import datetime
import asyncio
import requests

#Welcome & Channel IDS
TOKEN = "ENTER TOKEN HERE"
channel_id = 123456789

#Random Quote API
intents = discord.Intents.all()
intents.members = True
client = commands.Bot(command_prefix = '!', intents = intents, help_command = None)

@client.event
async def on_ready():
    print("Alarmbot is now Ready.")
    asyncio.create_task(daily_quote())

daily_timer = 86400
async def daily_quote():
    while True:
        api = "http://api.quotable.io/random"
        random_quote = requests.get(api).json()
        content = random_quote["content"]
        author = random_quote["author"]
        quote = content + "\n" + "By " + author
    
        # Replace 'daily_quote_channel_id' with the actual ID of the channel you want to send the quote to
        channel = client.get_channel(channel_id)
    
        # Sends the quote to the specified channel
        await channel.send(quote)
        await asyncio.sleep(daily_timer)
    
    
        

#Command List
@client.command()
async def help(ctx):
    info_message = "Here are the following Commands:\n" \
                   "```\n" \
                   "--------!create_reminder--------\n" \
                   "--------!delete_reminder--------\n" \
                   "```\n" \
                   "Feel free to use these commands to manage your reminders!"
    await ctx.send(info_message)



#Creating a Reminder 

reminders = {} #create dictionary with user_id to as key to delete the correct reminders.
format = "%m/%d/%Y %H:%M" #datetime format

@client.command()
async def remind(ctx, date: str, time: str, *, reminder: str):
    
    try:
        #Time Difference Calculations
        user_time = str(date + " " + time)
        print(user_time)
        future = datetime.strptime(user_time,format)
        now = datetime.now()
        time_diff = (future - now).total_seconds()
        
        reminder_message = f"{ctx.author.mention}, Here's your reminder: {reminder}"
        await ctx.send("Reminder set!")
        
        # Store the reminder in the reminders dictionary
        reminders[ctx.author.id] = (reminder_message, future)
        await asyncio.sleep(time_diff)
        
    except ValueError as e:
        await ctx.send("Invalid format, please follow this formatting: !remind %m/%d/%yyyy %HH:%MM '(24 hour time)' + your reminder name")
        
    # Check if the reminder still exists in the dictionary (not deleted)
    if ctx.author.id in reminders:
        del reminders[ctx.author.id]
        await ctx.author.send(reminder_message)

    
#Deleting a reminder
@client.command()
async def cancel(ctx):
    if ctx.author.id in reminders:
        del reminders[ctx.author.id]
        await ctx.send("Your reminder has been cancelled")
    else:
        await ctx.send("No Reminders Found.")

    
client.run(TOKEN)
