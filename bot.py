import asyncio
import base64
import datetime
import discord
from discord.ext import commands
from gpiozero import CPUTemperature, LoadAverage, DiskUsage
from http.server import BaseHTTPRequestHandler, HTTPServer
from itertools import cycle
import json
import lxml.html
import mechanicalsoup
import platform
from pyppeteer import launch
import re
import secrets
import socketserver
import ssl
import sys
from threading import Thread
import urllib.parse
import requests

if(platform.uname()[1]=="raspberrypi"):
    bot = commands.Bot(command_prefix="7: ", status=discord.Status.idle, activity=discord.Game(name="Halsar en åbro.."))
else:
    bot = commands.Bot(command_prefix="l: ", status=discord.Status.idle, activity=discord.Game(name="Halsar en åbro.."))
bot.remove_command("help")
register_list = []
course_list = []
course_list_id = []
program_list = []
bot_version = 0.00

isLocalBot = 0
class course:
    def __init__(self, courseID, channelID, year):
        self.courseID = courseID
        self.channelID = channelID
        self.year = year
    def get_courseID(self):
        return self.courseID
    def get_channelID(self):
        return self.channelID
    def get_year(self):
        return self.year
    
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
        self.end_headers() 
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        jsona = post_data.decode("utf-8")
        x = json.loads(jsona)
        username=x[0]
        password=x[1]
        id=x[2]
        print(len(register_list))
        register_list_temp = register_list.copy()
        for index,user in enumerate(register_list_temp):
            if(user.user_id()==id['value']):
                user.set_user(username['value'])
                user.set_password(password['value'])
                register_list.pop(index)
                loopish.run_until_complete(ladok(user))# Start a worker processes
def host_HTTP():
    print("started http")
    httpd = socketserver.TCPServer(("", 3333), listen_for_request)
    httpd.socket = ssl.wrap_socket (httpd.socket, 
        keyfile="/home/pi/key.pem", 
        certfile='/home/pi/cert.pem')
    httpd.serve_forever()
    
@bot.event
async def on_ready():
    print("Ready to go!")
    print(f"Serving: {len(bot.guilds)} guilds.")
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="beerpong @ smålands!"))
    channel = bot.get_channel(560931911682490379)
    if isLocalBot == 0:
        await channel.send(f"I've rebooted, cheers! :beers: Running this commit: https://github.com/myhrmans/toersten-discord-bot/commit/{bot_version}")


@bot.command()
async def ping(ctx):
    sent_time = ctx.message.created_at
    proccess_time = datetime.datetime.utcnow()
    difference = (proccess_time - sent_time)
    duration_in_s = difference.total_seconds()

    #await ctx.channel.send(f"{sent_time} and {proccess_time}")
    await ctx.channel.send(f"It took me {duration_in_s}s to drink a beer and reply to this message, SKÅL as we say in swedish!")

@bot.command()
async def pi(ctx, *, args):
    member = ctx.message.author
    if(isAdmin(member)):
        if "temp" in args:
            cpu = CPUTemperature()
            cpu_temp = round(cpu.temperature)
            await ctx.channel.send(f"Temp: {cpu_temp}°C")
        if "load" in args:
            load = LoadAverage()
            load_avg = round(load.load_average*100)
            await ctx.channel.send(f"Load: {load_avg}%")
        if "disk" in args:
            disk = DiskUsage()
            disk_usage = round(disk.usage)
            await ctx.channel.send(f"Disk: {disk_usage}%")
        if "all" in args:
            cpu = CPUTemperature()
            load = LoadAverage()
            load_avg = round(load.load_average*100)
            disk = DiskUsage()
            disk_usage = round(disk.usage)
            await ctx.channel.send(f"Temp: {cpu.temperature}°C")
            await ctx.channel.send(f"Load: {load_avg}%")
            await ctx.channel.send(f"Disk: {disk_usage}%")

@bot.command()
async def welcome_message(ctx):
    member = ctx.message.author
    if isAdmin(member):
        channel = bot.get_channel(557509634437677056)
        await channel.send("Welcome to ÖDETs Discord channel!\n\nThe main purpose of this channel is for students to discuss courses, exams and labs etc.\nMain language is Swedish but all of the documentation is written in english since there might be x-change students discussing in some of the courses.\nTo use this channel you must first authenticate that you're a student of ÖDET, to start the sign-up process, react with an :white_check_mark: on this message. By authenticating to this channel you accept the following community guidelines:\n\n- No harassment\n- No hate or racism\n- No cheating\n- Keep good tone to each other\n- You need to follow Swedish laws such as 'Diskrimineringslagen'.\n\nWe are all here to help each other and we all want a nice community to discuss our studies, if you can't follow these simple rules you will get banned.\n\n---------------------------------------------------------------------------------------------------------------\n\nCheck the README.md file in the github repository for commands on how to interact with Toersten. If there's any problems, don't hesitate to contact the channel admins! If you want to contribute to the community or with development, feel free to contact us! Especially if you have experience with Python and JavaScript.\n\n//Admins\nP.S Toersten vakar över oss alla, ty han är den allsmäktige!")

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
    await channel.send(f"A new bug was reported by {member.mention}\nDescription: {message.content}")

@bot.command()
async def show(ctx, *, args):
    if ("wednesday" in args) or ("dudes" in args):
        await ctx.channel.send(f"https://www.youtube.com/watch?v=V37A21Mr7eQ")
    elif ("ok" in args) or ("oke" in args) or ("okej" in args) or ("okay" in args):
        await ctx.channel.send(f"https://www.youtube.com/watch?v=80Rdk6h7sHo")
    elif ("hot" in args) or ("willy" in args):
        await ctx.channel.send(f"https://www.youtube.com/watch?v=iRjUvXoyojw")
    elif "breakfast" in args:
        await ctx.channel.send(f"https://www.youtube.com/watch?v=cgtxdMSCjZk")
    elif ("friday" in args) or ("rebecca" in args) or ("black" in args):
        await ctx.channel.send(f"https://www.youtube.com/watch?v=kfVsfOSbJY0")
    elif ("ödet" in args) or ("livet" in args) or ("nordman" in args):
        await ctx.channel.send(f"https://www.youtube.com/watch?v=ehORcoh7fbI")
    elif "brittmarie" in args:
        await ctx.channel.send(f"https://www.youtube.com/watch?v=w5MTdkPgKc8")
    elif "kazoo" in args:
        await ctx.channel.send(f"https://www.youtube.com/watch?v=cRpdIrq7Rbo")
    elif "subgap" in args:
        await sendpewdiepieSubgap(ctx)
    elif "hinkenhelp" in args:
        await ctx.channel.send(f"http://dixon.hh.se/mikael/")
    elif "help" in args:
        await showhelp(ctx)
    elif ("git" in args) or ("github" in args):
        await ctx.channel.send(f"Source of project is: https://github.com/myhrmans/toersten-discord-bot")
    elif "topmeme" in args:
        await sendProgrammerHumorTopMeme(ctx)
    else:
        await ctx.channel.send(f"Sorry. The only thing i could find was this beer! 🍺")


@bot.event
async def sendpewdiepieSubgap(ctx):
    key = "AIzaSyDLldX_e_RHl9JyfvCnZ5cG0Z9ahuXyNHI"
    #document.getElementById("subscriber-count").innerHTML.slice(0,document.getElementById("subscriber-count").innerHTML.length-13)
    name= "PewDiePie"
    pew_data = requests.get("https://www.googleapis.com/youtube/v3/channels?part=statistics&forUsername="+name+"&key="+key, headers = {'User-agent': 'Toersten'})
    pew_subs = int(pew_data.json()["items"][0]["statistics"]["subscriberCount"])
    name= "TSeries"
    t_data = requests.get("https://www.googleapis.com/youtube/v3/channels?part=statistics&forUsername="+name+"&key="+key, headers = {'User-agent': 'Toersten'})
    t_subs = int(t_data.json()["items"][0]["statistics"]["subscriberCount"])
    if pew_subs < t_subs:
        await ctx.channel.send("Tseries is currently {} subscribers ahead of Pewdiepie".format(str(t_subs - pew_subs)))
    else:
        await ctx.channel.send("Pewdiepie is currently {} subscribers ahead of T-series".format(str(pew_subs - t_subs)))
@bot.event 
async def sendProgrammerHumorTopMeme(ctx):
        data = requests.get("https://www.reddit.com/r/ProgrammerHumor.json?limit=1", headers = {'User-agent': 'Toersten'})
        data = data.json()
        link = data["data"]["children"][2]["data"]["url"]
        await ctx.channel.send(f"Top meme from /r/programmerhumor of today is: {link}")
           
@bot.event
async def on_raw_reaction_add(payload):
    if(payload.message_id == 562730849800421384):
        member = bot.get_user(payload.user_id)
        if(str(payload.emoji) == "✅"):
            secret = secrets.token_urlsafe(32)
            register_list.append(user_register(member,secret))
            await member.create_dm()
            await member.send(f"Thanks for accepting the rules of this server. You will now get a URL to authenticate yourself against.\nTo authenticate open this website: https://odethh.se/register/?ID={secret}\nThis link will only work one time. If you fail for some reason you will have to press the :white_check_mark: in #welcome again. Once you're done with this you will have access to your classes.")
        else:
            channel = bot.get_channel(payload.channel_id)
            async for elem in channel.history():
                await elem.remove_reaction(payload.emoji,member)
@bot.command()
async def unregister(ctx, member:discord.User = None):
    member = ctx.message.author
    await member.create_dm()
    channels = bot.get_all_channels()
    for channel in channels:
        await channel.set_permissions(member, overwrite=None)
    for idx, val in enumerate(member.roles):
        if(idx!=0):
            await member.remove_roles(val,reason="Called for unregister")
    await member.edit(nick=None)
    await member.send(f"All information about you are now removed from this discord channel. Have a nice day! :beers:")
    time_unreg = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    channel = bot.get_channel(562647258722598935)
    await channel.send(f"-----\nUser: {member.mention}\nAction: Unregister\nTime: {time_unreg}\n-----")

@bot.command()
async def version(ctx):
    await ctx.channel.send(f"Running this: https://github.com/myhrmans/toersten-discord-bot/commit/{bot_version}")

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
def getKeyByValue(dic, value):
    listOfItems = dic.items()
    for item in listOfItems:
        if item[1] == value:
            return  item[0]
    return 0
async def ladok(user):
    member = user.get_member()
    username = user.__getattribute__("username")
    username = str(username)
    password = user.__getattribute__("password")
    password = str(password)
    course_list_ladok = []
    await member.create_dm()
    await member.send("Perfect. I've now started working on finding your courses. This can take up to two minutes. Please be patient! :beers:")
    channel = bot.get_channel(555823680148602901)
    #---- Launch browser ----#
    browser = await launch(options = {'headless': True, 'executablePath': '/usr/bin/chromium-browser','args': '--no-sandbox'})
    page = await browser.newPage()
    #---- Navigate browser to ladok ----#
    await page.goto('https://www.student.ladok.se/')
    await page.setViewport({'width':1024, 'height': 870})
    try:
        await page.waitForSelector("p:nth-child(5) > a", options={'timeout':10000})
        await page.click("p:nth-child(5) > a")
    except:
            await channel.send(f"Something went wrong during selecting next step (1) for {member.mention}")
    try:
        await page.waitForSelector("div#searchlist > div:nth-child(5)", options={'timeout':10000})
        await page.click('div#searchlist > div:nth-child(5)')
    except:
        await channel.send(f"Something went wrong during selecting next step (2) for {member.mention}")
    try:
        await page.waitForSelector("a#proceed",options={'timeout':10000})
        await page.click("a#proceed")
    except:
        await channel.send(f"Something went wrong during selecting next step (3) for {member.mention}")
    #---- Enter Username and password ----#
    try:
        await page.waitForSelector('body > div > div > div > div > form > div > div > div:nth-child(1) > div > input', options={'timeout':10000})
        await page.focus('body > div > div > div > div > form > div > div > div:nth-child(1) > div > input')
        await page.keyboard.type(username)
        await page.focus('body > div > div > div > div > form > div > div > div:nth-child(2) > div > input')
        await page.keyboard.type(password)
        await page.click('body > div > div > div > div > form > div > div > div:nth-child(3) > button')
    except:
        await channel.send(f"Something went wrong during selecting next step (4) for {member.mention}")
    try:
        await page.waitForSelector('div#navigation-first-meny div > ladok-inloggad-student', options={'timeout':4500})
            #---- Get name ----#
        element = await page.querySelector('div#navigation-first-meny div > ladok-inloggad-student')
        name = await page.evaluate('(element) => element.textContent', element)
        fullname = name.split("|")
        fullname = fullname[0]
        fullname = fullname.split(",")
        firstname = fullname[1]
        firstname = firstname[1:-1]
        lastname = fullname[0]
        fullname = firstname + "" + lastname
        print(fullname)
        #---- Get program name ----#
        try:
            element = await page.waitForSelector('div#ldk-main-wrapper > ng-component > ladok-aktuell > div.row > div:nth-child(1) > ladok-pagaende-kurser > div:nth-child(3) > div > ladok-paketeringlink > h3', options={'timeout':10000})
            program_name = await page.evaluate('(element) => element.textContent', element)
            program_name = program_name.split("|")
            program_name = program_name[0]
            program_name = program_name[1:-1]
        except:
            await channel.send(f"Something went wrong during getting program name for {member.mention}")
        #---- Get current courses ----#
        try:
            await page.waitForSelector('div#ldk-main-wrapper > ng-component > ladok-aktuell > div.row > div:nth-child(1) > ladok-pagaende-kurser > div:nth-child(3) > div > ladok-pagaende-kurslista > ladok-kurser > div', options={'timeout':10000})
            current = await page.querySelectorAll('div#ldk-main-wrapper > ng-component > ladok-aktuell > div.row > div:nth-child(1) > ladok-pagaende-kurser > div:nth-child(3) > div > ladok-pagaende-kurslista > ladok-kurser > div')
            for element in current:
                    element = await element.querySelector('div > ladok-kurs-i-lista > h4 > ladok-kurslink > div.ldk-visa-desktop > a')
                    element_text = await page.evaluate('(element) => element.textContent', element)
                    courseID = element_text.split("|")
                    courseID = courseID[2]
                    courseID = courseID[1:7]
                    course_list_ladok.append(courseID)
        except:
            await channel.send(f"Something went wrong during getting current courses for {member.mention}")
        #---- Get uncompleted courses ----#
        try:
            uncompleted = await page.querySelectorAll('div#ldk-main-wrapper > ng-component > ladok-aktuell > div.row > div:nth-child(3) > ladok-oavslutade-kurser > div:nth-child(3) > div > ladok-oavslutade-kurslista > ladok-kurser > div')
            for element in uncompleted:
                element = await element.querySelector('div > ladok-kurs-i-lista > h4 > ladok-kurslink > div.ldk-visa-desktop > a')
                element_text = await page.evaluate('(element) => element.textContent', element)
                courseID = element_text.split("|")
                courseID = courseID[2]
                courseID = courseID[1:7]
                course_list_ladok.append(courseID)
        except:
            await channel.send(f"Something went wrong during getting uncompleted courses for {member.mention}")

        #---- Get self-contained courses ----#
        try:
            self_contained_courses = await page.querySelectorAll('div#ldk-main-wrapper > ng-component > ladok-aktuell > div.row > div:nth-child(3) > ladok-oavslutade-kurser > div:nth-child(4) > ladok-oavslutade-kurslista > ladok-kurser > div')
            for element in self_contained_courses:
                element = await element.querySelector('div > ladok-kurs-i-lista > h4 > ladok-kurslink > div.ldk-visa-desktop > a')
                element_text = await page.evaluate('(element) => element.textContent', element)
                courseID = element_text.split("|")
                courseID = courseID[2]
                courseID = courseID[1:7]
                course_list_ladok.append(courseID)
        except:
            await channel.send(f"Something went wrong during getting self-contained courses for {member.mention}")

        #---- Close Browser ----#
        await browser.close()

        #---- Calculate Year and add to channels ----#
        topyear = 0
        isOdet = 0
        for course in course_list:
                discord_courseID = course.get_courseID()
                for courseID in course_list_ladok:
                    if(discord_courseID==courseID): 
                        course_year=int(course.get_year())
                        isOdet=1
                        if(course_year > topyear):
                            topyear = course_year
                        channel = bot.get_channel(int(course.get_channelID()))
                        await channel.set_permissions(member, read_messages=True,
                                                            send_messages=True)
        if(isOdet==1):
            channel = bot.get_channel(555823680148602901)
            for courseID in course_list_ladok:
                if courseID not in course_list_id:
                        await channel.send(f"A course that was not in our list was reported by {member.mention} via sign-up.")
                        await channel.send(f"Course ID: {courseID}")
                        await channel.send(f"User had program: {program_name}")
        else: 
            await member.send(f"No courses found which associates with ÖDET. Looks like you are reading {program_name}. This discord is only for people in ÖDET.")
        years = {
            0: "0",
            1: "549996194898771978",
            2: "549996363400740866",
            3: "549996416882442270",
            4: "553999707689451532",
            5: "553999955228884993",
        }

        if program_name not in program_list:
            topyear = 0
        role = years[topyear]
        guild = bot.get_guild(547454095360000011)
        member_guild = guild.get_member(member.id)
        years_text = {
            1: "1st",
            2: "2nd",
            3: "3rd",
            4: "4th",
            5: "5th"
        }
        if(isOdet==1 and topyear!=0):
            role_disc = guild.get_role(int(role))
            await member_guild.add_roles(role_disc)
            yr = years_text[topyear]
            await member.send(f"-----\nWelcome to ÖDET Discord Channel. You, {fullname}, should now have full access to all your courses and from what we could understand you are reading the {yr} year at Högskolan i Halmstad. \nIf this is incorrect please contact the admins of the discord.  \nRemember the rules and enjoy they stay! \n//Toersten\n-----")
            await member_guild.edit(nick=fullname)
            courses_name = {
                1: 'Computer Science and Engineering',
                2: 'Computer Engineer',
                3: 'Intelligent Systems',
                4: 'Mechatronic Engineer',
                5: 'Electrical Engineer'
            }
            courses_id = {
                1: "553990861705183340",
                2: "554057748275265627",
                3: "553990362352582690",
                4: "554058018384379925",
                5: "554057912989777952"
            }
            course_int_id = getKeyByValue(courses_name, program_name)
            role_program = courses_id[course_int_id]
            role_disc = guild.get_role(int(role_program))
            await member_guild.add_roles(role_disc)
        await browser.close()
        time_unreg = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        n_couses = len(course_list_ladok)
        channel = bot.get_channel(562647258722598935)
        await channel.send(f"-----\nUser: {member.mention}\nName: {fullname}\nAction: Register\nTime: {time_unreg}\nProgram: {program_name}\nCourses: {n_couses}\n-----")
    except Exception as e:
        print(e)
        channel = bot.get_channel(555823680148602901)
        await channel.send(f"Something went wrong during login for {member.mention}\nError message: \n{e}")
        channel = bot.get_channel(557509634437677056)
        async for elem in channel.history():
            await elem.remove_reaction("✅",member)
        await member.send("Wrong username or password. Please try again by going into #welcome.")
        await browser.close()
async def isAdmin(member):
    admin = False
    for role in member.roles:
        if "admin" == role.name:
            admin = True
    return admin
@bot.command()
async def add(ctx, *, args, member:discord.User = None):
    member = ctx.message.author
    """
        Uses regex to extract [## Todo] from README.md, then splits the Todo to a list to easly insert e new item.
        Then rebuilds the README.md file and overwrites the old one.
    """
    newTodoList = ""
    if isAdmin(member):    
        try:
            File = open("./README.md", "r+", encoding="UTF-8")
            FileInfo = File.read()
            regexBeforeTodo = r"(.*)(?=## Todo)"            # Info before Todo
            regexTodo = r"(?=## Todo)(.*)(?=## Commands)"   # The Todo-list
            regexAfterTodo = r"(?=## Commands)(.*)"         # After the Todo
            matchesBeforeTodo = re.search(regexBeforeTodo, FileInfo, re.DOTALL)
            matchesTodo = re.search(regexTodo, FileInfo, re.DOTALL)
            matchesAfterTodo = re.search(regexAfterTodo, FileInfo, re.DOTALL)

            if matchesBeforeTodo and matchesTodo and matchesAfterTodo:  # Basically if there is anything in the README.md file
                output = matchesTodo.group().split("\n")                # Split the list to easly add new item
                if not (args[0] == " " or args[0] == "-"):              # Just to check correct format
                    del output[len(output)-2]                           # Deletes a \n in the array, dunno why you have to take the index len(output)-2 to delete it but it wont work otherwise LOL 
                    output.insert(len(output)-1, "- " + args)           # Formats the new item for markdown
            
                for todoItem in output:
                    newTodoList = newTodoList + todoItem + "\n"         # Constructs the Todo-list
                
            File.seek(0)                                                # Set the cursor back to the beginning to overwrite the old file
            File.write((matchesBeforeTodo.group() + newTodoList + matchesAfterTodo.group())) # Stitch back together the new Todo-list with the old data
            File.close()

            await ctx.channel.send(f"Task: [{args}] added to [## Todo] in README.md")

        except:
            await ctx.channel.send(f"Error, contact admins!")
    else:
        await ctx.channel.send(f"Permission denied!")


@bot.command()
async def todo(ctx, member:discord.User = None):
    member = ctx.message.author
    """
        Uses regex to extract [## Todo] from README.md.
    """
    if isAdmin(member):    
        try:
            File = open("./README.md", "r", encoding="UTF-8")
            FileInfo = File.read()
            regexTodo = r"(?=## Todo)(.*)(?=## Commands)"   # The Todo-list
            matchesTodo = re.search(regexTodo, FileInfo, re.DOTALL)
            
            if matchesTodo:                                             # Basically if there is anything in the README.md file
                await ctx.channel.send(matchesTodo.group())

        except:
            await ctx.channel.send(f"Error, contact admins!")
    else:
        await ctx.channel.send(f"Permission denied!")



@bot.command()
async def help(ctx):
    """
        Prints a message with the current commands.
    """
    try:
        File = open("./README.md", "r+", encoding="UTF-8")
        helpFile = File.read()
        helpFileList = helpFile.split(sep="## Commands")
        commands = helpFileList[1].split("##")[0]
        await ctx.channel.send(f"``` \n ## Commands \n {commands} \n ```")
    except:
        await ctx.channel.send(f"Error: Cant find README.md, contact admins!")

async def showhelp(ctx):
    """
        Prints a message with the current commands.
    """
    try:
        File = open("./README.md", "r+", encoding="UTF-8")
        showhelpFile = File.read()
        showhelpFileList = showhelpFile.split(sep="## Options for show")
        commands = showhelpFileList[1].split("##")[0]
        await ctx.channel.send(f"``` \n ## Options for show \n {commands} \n ```")
    except:
        await ctx.channel.send(f"Error: Cant find README.md, contact admins!")

course_file = open("courses/courses.txt", "r")
program_file = open("courses/programs.txt", "r")
year = 3

""" ------------------------------- Encryption -------------------------------"""
local0001Encrypted = "6+k<\x14gN=\x192=`X%4@>\x01'95\x18_<d^0\x08o/hd;\x13\x1c\x10\x19\x03@\x12\x1d@_\x1e\x0e\x19.5\x0e&\x05P\x01\x11\x00\x05\x0e\x11-\t\x19\x00!g[\x0c#K;\r\r#-\x05\x06 :k\t,\x04`"
local0010Encrypted = "6+k<\x14<F=\x1f>\x03~o\x0e\x11\x0f>5\x05%\x1c}_{gR\x12\x08X\x06\x0cf;\x13\x1c\x13(]?!#@^.\x03\x1cA='\x08@\\\x06\x0fc=\x16\x12\x13\x0c.\x04\x0fI^\x18+~$h\x1dA.\x0804:X\x0e\x12\x04`"
masterEncrypted = "6^\x00:)\x01p\x08\x18.\x07s\\'\x02+8T\x16\x134\x18O h^(|3\x00!u\t\x12\x1c\x03\x0bSG\x15g\x01Y>\x12/7&\x18\x05Ys\x03e>;0\x1c-3\x00\x00\x0bjX7\x07'\r\t<w+\x7f\x02?7G\x18sof"

def xor_strings(string, theKey):
    """xor two strings together"""
    if isinstance(string, str):
        # Text strings contain single characters
        return b"".join(chr(ord(a) ^ ord(b)) for a, b in zip(string, cycle(key)))
    else:
        # Python 3 bytes objects contain integer values in the range 0-255
        return bytes([a ^ b for a, b in zip(string, cycle(key))])   

""" --------------------------------------------------------------------------"""


for line in course_file:
        line = line.split(" ")
        if(line[0]=="ÅR"):
            year=line[1]
        course_list.append(course(line[0],line[1],int(year)))
course_file.close()
lines = program_file.read().split('\n')
for line in lines:
        program_list.append(line)
program_file.close()
for course in course_list:
    course_list_id.append(course.get_courseID())
#--------- TO START MASTER BOT --------------
if(platform.uname()[1]=="raspberrypi"):
    bot_version = sys.argv[2]
    try:
        Thread(target=host_HTTP).start()
    except:
        print ("Error2: unable to start thread")
    try:
        loopish = asyncio.get_event_loop()
    except:
        print ("Error3: unable to start thread")
    try:
        key = base64.encodestring(bytes(sys.argv[1], encoding="UTF-8"))
        decryptedHost = base64.decodestring(xor_strings(bytes(masterEncrypted, encoding="UTF-8"), key)).decode("UTF-8")
        bot.run(decryptedHost)
        decryptedHost = 0
    except Exception as e:
        print(f"Fail bot: {e}")
#--------- TO START BOT LOCAL BOT 0001 ----------------
elif(sys.argv[1] == "0001"):
    isLocalBot = 1
    # SPECAIL CASE IF LOCAL BOT ISN'T RUNNING ON UNIX SYSTEM
    if(platform.uname()[0] != "Linux"):
        try:
            #Thread(target=bot.run,args=(local,)).start()
            key = base64.encodestring(bytes(sys.argv[2], encoding="UTF-8"))
            decryptedHost = base64.decodestring(xor_strings(bytes(local0001Encrypted, encoding="UTF-8"), key)).decode("UTF-8")

            Thread(target=bot.run,args=(decryptedHost,)).start()
            decryptedHost = 0
            Thread(target=host_HTTP).start()
            loopish = asyncio.get_event_loop()
        except:
            print ("Error: unable to start thread")
    # TO START LOCAL BOT ON UNIX SYSTEM
    else:
        try:
            Thread(target=host_HTTP).start()
        except:
            print ("Error2: unable to start thread")
        try:
            loopish = asyncio.get_event_loop()
        except:
            print ("Error3: unable to start thread")
        try:
            key = base64.encodestring(bytes(sys.argv[2], encoding="UTF-8"))
            decryptedHost = base64.decodestring(xor_strings(bytes(local0001Encrypted, encoding="UTF-8"), key)).decode("UTF-8")
            bot.run(decryptedHost)
            decryptedHost = 0
        except Exception as e:
            print(f"Fail bot: {e}")
#--------- TO START BOT LOCAL BOT 0002 ----------------
elif(sys.argv[1] == "0010"):
    isLocalBot =1
    # SPECAIL CASE IF LOCAL BOT ISN'T RUNNING ON UNIX SYSTEM
    if(platform.uname()[0] != "Linux"):
        try:
            #Thread(target=bot.run,args=(local,)).start()
            key = base64.encodestring(bytes(sys.argv[2], encoding="UTF-8"))
            decryptedHost = base64.decodestring(xor_strings(bytes(local0010Encrypted, encoding="UTF-8"), key)).decode("UTF-8")

            Thread(target=bot.run,args=(decryptedHost,)).start()
            decryptedHost = 0
            Thread(target=host_HTTP).start()
            loopish = asyncio.get_event_loop()
        except:
            print ("Error: unable to start thread")
    # TO START LOCAL BOT ON UNIX SYSTEM
    else:
        try:
            Thread(target=host_HTTP).start()
        except:
            print ("Error2: unable to start thread")
        try:
            loopish = asyncio.get_event_loop()
        except:
            print ("Error3: unable to start thread")
        try:
            key = base64.encodestring(bytes(sys.argv[2], encoding="UTF-8"))
            decryptedHost = base64.decodestring(xor_strings(bytes(local0010Encrypted, encoding="UTF-8"), key)).decode("UTF-8")
            bot.run(decryptedHost)
            decryptedHost = 0
        except Exception as e:
            print(f"Fail bot: {e}")
