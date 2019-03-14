import discord
from discord.ext import commands
import mechanicalsoup
import lxml.html
bot = commands.Bot(command_prefix="7: ", status=discord.Status.idle, activity=discord.Game(name="Halsar en åbro.."))
bot.remove_command("help")
bot_version = "1.00"

@bot.event
async def on_ready():
    print("Ready to go!")
    print(f"Serving: {len(bot.guilds)} guilds.")
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="beerpong @ smålands!"))

@bot.command()
async def ping(ctx):
    ping_ = bot.latency
    ping = round(ping_ * 1000)
    await ctx.channel.send(f"It took me {ping}ms to drink a beer and reply to this message, SKÅL... as we say in swedish!")

@bot.command()
async def report(ctx, member:discord.User = None):
    member = ctx.message.author
    message = ctx.message
    def pred(m):
        return m.author == message.author
    await member.create_dm()
    await member.send(f"Beskriv ditt problem:")
    message = await bot.wait_for('message', check=pred)
    channel = bot.get_channel(555823680148602901)
    await channel.send(f"A new bug was reported by {member.mention}")
    await channel.send(f"Description: {message.content}")
    
@bot.command()
async def version(ctx):
    await ctx.channel.send("Current Version: {}".format(bot_version))

@bot.event
async def on_reaction_add(reaction, user):
    reactionResponses = {
        '🍻': f"{user.mention} bjuder alla på en backbro, SKÅL!",
        '🍺' : f"{user.mention} bjuder alla på en tvåbro, SKÅL!"
    }
    channel = reaction.message.channel
    if str(reaction.emoji) in reactionResponses.keys():
        await channel.send(reactionResponses[reaction.emoji])
    #do stuff

@bot.command()
async def courses(ctx, member:discord.User = None):
    member = ctx.message.author
    message = ctx.message
    def pred(m):
        return m.author == message.author
    await member.create_dm()
    await member.send(f"Ange ditt Blackboard användarnamn (exempel marmyh16):")
    username = await bot.wait_for('message', check=pred)
    await member.send(f"Okej {username.content}. Bara ett steg kvar.. ditt lösenord:")
    password = await bot.wait_for('message', check=pred)
    #await member.send(f"{username.content} och {password.content}")
    browser = mechanicalsoup.browser = mechanicalsoup.StatefulBrowser(
        soup_config={'features': 'lxml'},
        raise_on_404=True
    )
    login_page = browser.open("https://hh.blackboard.com/webapps/portal/execute/tabs/tabAction?tab_tab_group_id=_98_1")
    login_form = browser.select_form('#loginBoxFull form')
    browser["user_id"] = username.content
    browser["password"] = password.content
    resp = browser.submit_selected()
    resp2 = browser.post("https://hh.blackboard.com/webapps/portal/execute/tabs/tabAction", params='action=refreshAjaxModule&modId=_25_1&tabId=_1_1&tab_tab_group_id=_1_1');
    courses = resp2.text
    courses = lxml.html.fromstring(courses)
    courses = courses.cssselect("a")
    await member.send(f"Om du angivet dina uppgifter rätt kommer här kommer dina kurser:")
    for l in courses:
        await member.send(f"{l.text}")


@bot.command()
async def nickname(ctx, member:discord.User = None):
    member = ctx.message.author
    message = ctx.message
    def pred(m):
        return m.author == message.author
    await member.create_dm()
    await member.send(f"Vi kommer nu hämta ditt fulla namn...")
    await member.send(f"Ange ditt Blackboard användarnamn (exempel marmyh16):")
    username = await bot.wait_for('message', check=pred)
    await member.send(f"Okej {username.content}. Bara ett steg kvar.. ditt lösenord:")
    password = await bot.wait_for('message', check=pred)
    #await member.send(f"{username.content} och {password.content}")
    browser = mechanicalsoup.browser = mechanicalsoup.StatefulBrowser(
        soup_config={'features': 'lxml'},
        raise_on_404=True
    )
    login_page = browser.open("https://hh.blackboard.com/webapps/portal/execute/tabs/tabAction?tab_tab_group_id=_98_1")
    login_form = browser.select_form('#loginBoxFull form')
    browser["user_id"] = username.content
    browser["password"] = password.content
    resp = browser.submit_selected()
    name = resp.text
    name = lxml.html.fromstring(name)
    name = name.cssselect("a[id='global-nav-link']")
    await member.send(f"Om du angivet dina uppgifter rätt kommer här kommer ditt namn:")
    await member.send(f"{name}")

bot.run("NTU0NjQ5MTM2ODU1NjQ2MjQ5.D2fs0Q.YV3dm7riiVMxI36VENnjlvGlg30")
