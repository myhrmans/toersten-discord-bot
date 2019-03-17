import discord
import platform
from discord.ext import commands
import mechanicalsoup
import lxml.html
import secrets
import urllib.parse
import json
import socketserver
import asyncio
from threading import Thread
from http.server import BaseHTTPRequestHandler, HTTPServer

if(platform.uname()[1]=="raspberrypi"):
    bot = commands.Bot(command_prefix="7: ", status=discord.Status.idle, activity=discord.Game(name="Halsar en åbro.."))
else:
    bot = commands.Bot(command_prefix="l: ", status=discord.Status.idle, activity=discord.Game(name="Halsar en åbro.."))
bot.remove_command("help")
bot_version = "1.00"
register_list = []

class user_register:
    def __init__(self, member, ID):
        self.member = member
        self.ID = ID
        self.username = ""
        self.password = ""
    def user_id(self):
        return self.ID
    def set_user(self,username):
        self.username=username
    def set_password(self,password):
        self.password=password
    def get_member(self):
        return self.member
    
class listen_for_request(BaseHTTPRequestHandler):
    def do_POST(self):
        # Doesn't do anything with posted data
        self.send_response(200, "ok")
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        #print(self.headers['Content-Length'])
        self.end_headers() 
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        print( "incomming http: ", self.path ) # <-- Print post data
        jsona = post_data.decode("utf-8")
        x = json.loads(jsona)
        username=x[0]
        password=x[1]
        id=x[2]
        print(username['value'])
        print(password['value'])
        print(id['value'])
        for user in register_list:
            if(user.user_id()==id['value']):
                user.set_user(username['value'])
                user.set_password(password['value'])
                result = loopish.run_until_complete(register(user))              # Start a worker processes.
        #self._set_headers()
def host_HTTP():
    print("started http")
    httpd = socketserver.TCPServer(("", 3333), listen_for_request)
    httpd.serve_forever()
    
@bot.event
async def on_ready():
    print("Ready to go!")
    print(f"Serving: {len(bot.guilds)} guilds.")
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="beerpong @ smålands!"))

@bot.command()
async def ping(ctx):
    print(type(ctx.message.author))
    member = ctx.message.author
    secret = secrets.token_urlsafe(32)
    register_list.append(user_register(member,secret))
    await ctx.channel.send(f"To authenticate open this website: http://localhost:3333/login?id={secret}")
    ping = bot.latency
    ping = round(ping * 1000)
    await ctx.channel.send(f"It took me {ping}ms to drink a beer and reply to this message, SKÅL as we say in swedish!")

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
    os_name = platform.uname()
    await ctx.channel.send(f"OS info: {os_name}".format(os_name))

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
        
async def register(user):
    print("Register")
    print(user.__getattribute__("member"))
    print(user.__getattribute__("ID"))
    print(user.__getattribute__("username"))
    print(user.__getattribute__("password"))
    member = user.get_member()
    ID = user.__getattribute__("ID")
    username = user.__getattribute__("username")
    password = user.__getattribute__("password")
    print(type(member))
    await member.create_dm()
    browser = mechanicalsoup.browser = mechanicalsoup.StatefulBrowser(
        soup_config={'features': 'lxml'},
        raise_on_404=True
    )
    login_page = browser.open("https://hh.blackboard.com/webapps/portal/execute/tabs/tabAction?tab_tab_group_id=_98_1")
    login_form = browser.select_form('#loginBoxFull form')
    browser["user_id"] = username
    browser["password"] = password
    resp = browser.submit_selected()
    resp2 = browser.post("https://hh.blackboard.com/webapps/portal/execute/tabs/tabAction", params='action=refreshAjaxModule&modId=_25_1&tabId=_1_1&tab_tab_group_id=_1_1');
    courses = resp2.text
    courses = lxml.html.fromstring(courses)
    courses = courses.cssselect("a")
    await member.send(f"Om du angivet dina uppgifter rätt kommer här kommer dina kurser:")
    for l in courses:
        courseID = l.text.split("HP")
        courseID = courseID[1]
        courseID = courseID[1:7]
        await member.send(f"{courseID}")

@bot.command()
async def ladok(ctx, member:discord.User = None):
    member = ctx.message.author
    message = ctx.message
    def pred(m):
        return m.author == message.author
    await member.create_dm()
    #await member.send(f"Ange ditt Blackboard användarnamn (exempel marmyh16):")
    username = "marmyh16"
    #await member.send(f"Okej {username.content}. Bara ett steg kvar.. ditt lösenord:")
    password = ""
    #await member.send(f"{username.content} och {password.content}")
    browser = mechanicalsoup.browser = mechanicalsoup.StatefulBrowser(
        soup_config={'features': 'lxml'},
        raise_on_404=True
    )
    login_page = browser.open("https://md.nordu.net/role/idp.ds?entityID=https%3A%2F%2Fwww.student.ladok.se%2Fstudent-sp&return=https%3A%2F%2Fwww.student.ladok.se%2FShibboleth.sso%2FLogin%3FSAMLDS%3D1%26target%3Dcookie%253A1552668759_d122")
    browser.launch_browser()
    #login_form = browser.select_form('#loginBoxFull form')
    #browser["user_id"] = username.content
    #browser["password"] = password.content
    #resp = browser.submit_selected()
    #resp2 = browser.post("https://hh.blackboard.com/webapps/portal/execute/tabs/tabAction", params='action=refreshAjaxModule&modId=_25_1&tabId=_1_1&tab_tab_group_id=_1_1');
    #courses = resp2.text
    #courses = lxml.html.fromstring(courses)
    #courses = courses.cssselect("a")
    #await member.send(f"Om du angivet dina uppgifter rätt kommer här kommer dina kurser:")
    #for l in courses:
    #    courseID = l.text.split("HP")
    #    courseID = courseID[1]
    #    courseID = courseID[1:7]
    #    await member.send(f"{courseID}")

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
    channel = bot.get_channel(555823680148602901)
    name = resp.text.split("class=global-top-avatar /> ")
    name = name[1].split("<span id=badgeTotal")
    name = name[0]
    print(name[0])
    await member.send(f"Om du angivet dina uppgifter rätt kommer här kommer ditt namn:")
    #for l in name:
    await member.send(f"Hej {name}.")
    await member.edit(nick=name)
    

local = "NTU2MDE3MzUzNTQwNzYzNjU5.D2znBw.0NOi0JUtvV8GmrprO9F7RzTFrFU"
master = "NTU0NjQ5MTM2ODU1NjQ2MjQ5.D2fs0Q.YV3dm7riiVMxI36VENnjlvGlg30"

if(platform.uname()[1]=="raspberrypi"):
    try:
        Thread(target=bot.run(),args=(master,)).start()
        Thread(target=host_HTTP).start()
        loopish = asyncio.get_event_loop()
    except:
        print ("Error: unable to start thread")
    
else:
    try:
        Thread(target=bot.run,args=(local,)).start()
        Thread(target=host_HTTP).start()
        loopish = asyncio.get_event_loop()
    except:
        print ("Error: unable to start thread")
