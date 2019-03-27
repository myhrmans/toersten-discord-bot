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
import sys
from itertools import cycle
import base64
from pyvirtualdisplay import Display
import datetime
import ssl
from arsenic import get_session, keys, browsers, services

if(platform.uname()[1]=="raspberrypi"):
    bot = commands.Bot(command_prefix="7: ", status=discord.Status.idle, activity=discord.Game(name="Halsar en åbro.."))
else:
    bot = commands.Bot(command_prefix="l: ", status=discord.Status.idle, activity=discord.Game(name="Halsar en åbro.."))
bot.remove_command("help")
bot_version = "1.00"
register_list = []
course_list = []
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
        for user in register_list:
            if(user.user_id()==id['value']):
                user.set_user(username['value'])
                user.set_password(password['value'])
                result = loopish.run_until_complete(hello_world(user))              # Start a worker processes.
        #self._set_headers()
def host_HTTP():
    print("started http")
    httpd = socketserver.TCPServer(("", 3333), listen_for_request)
    #httpd.socket = ssl.wrap_socket (httpd.socket, 
    #    keyfile="/home/pi/key.pem", 
    #    certfile='/home/pi/cert.pem', server_side=True)
    httpd.serve_forever()
    
@bot.event
async def on_ready():
    print("Ready to go!")
    print(f"Serving: {len(bot.guilds)} guilds.")
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="beerpong @ smålands!"))

@bot.command()
async def ping(ctx):
    sent_time = ctx.message.created_at
    proccess_time = datetime.datetime.utcnow()
    difference = (proccess_time - sent_time)
    duration_in_s = difference.total_seconds()

    #await ctx.channel.send(f"{sent_time} and {proccess_time}")
    await ctx.channel.send(f"It took me {duration_in_s}s to drink a beer and reply to this message, SKÅL as we say in swedish!")

@bot.command()
async def welcome_message(ctx):
    channel = bot.get_channel(557509634437677056)
    await channel.send("Welcome to ÖDETs Discord channel!\n\nThe main purpose of this channel is for students to discuss courses, exams and labs etc.\nMain language is Swedish but all of the documentation is written in english since there might be x-change students discussing in some of the courses.\nTo use this channel you must first authenticate that you're a student of ÖDET, this by reacting on this message. By authenticating to this channel you accept the following community guidelines:\n\n- No harassment\n- No hate or racism\n- No cheating\n- Keep good tone to each other\n- You need to follow Swedish laws such as 'Diskrimineringslagen'.\n\nWe are all here to help each other and we all want a nice community to discuss our studies, if you can't follow these simple rules you will get banned.\n\n---------------------------------------------------------------------------------------------------------------\n\nCheck the README.md file in the github repository for commands on how to interact with Toersten. If there's any problems, don't hesitate to contact the channel admins! If you want to contribute to the community or with development, feel free to contact us! Especially if you have experience with Python and JavaScript.\n\n//Admins\nP.S Toersten vakar över oss alla, ty han är den allsmäktige!")
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

@bot.event
async def on_raw_reaction_add(payload):
    if(payload.message_id == 558226835599785984):
        member = bot.get_user(payload.user_id)
        if(str(payload.emoji) == "✅"):
            secret = secrets.token_urlsafe(32)
            register_list.append(user_register(member,secret))
            await member.create_dm()
            await member.send(f"Thanks for accepting the rules of this server. You will now get a URL to authenticate yourself against.")
            await member.send(f"To authenticate open this website: https://odethh.se/register/?ID={secret}")
            await member.send(f"Once you're done with this you will have access to your classes.")
        else:
            channel = bot.get_channel(payload.channel_id)
            async for elem in channel.history():
                await elem.remove_reaction(payload.emoji,member)
@bot.command()
async def unregister(ctx, member:discord.User = None):
    member = ctx.message.author
    message = ctx.message
    def pred(m):
        return m.author == message.author
    await member.create_dm()
    channels = bot.get_all_channels()
    for channel in channels:
        await channel.set_permissions(member, overwrite=None)
    await member.send(f"All channels removed")

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
    member = user.get_member()
    ID = user.__getattribute__("ID")
    username = user.__getattribute__("username")
    password = user.__getattribute__("password")
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
    await member.send(f"Om du angivet dina uppgifter rätt kommer här kommer dina kurser, dessa har du även tillgång till nu:")
    for l in courses:
        courseID = l.text.split("HP")
        courseID = courseID[1]
        courseID = courseID[1:7]
        for course in course_list:
            if(course.get_courseID()==courseID):
                channel = bot.get_channel(int(course.get_channelID()))
                await channel.set_permissions(member, read_messages=True,
                                                      send_messages=True)
        await member.send(f"{courseID}")

async def hello_world(user):
    display = Display(visible=0, size=(800, 400))
    display.start()
    member = user.get_member()
    ID = user.__getattribute__("ID")
    username = user.__getattribute__("username")
    username = str(username)
    password = user.__getattribute__("password")
    password = str(password)
    course_list_ladok = []
    await member.create_dm()
    service = services.Chromedriver(binary="/usr/lib/chrome-browser/chromedriver")
    browser = browsers.Chrome()
    async with get_session(service, browser) as session:
        session.set_window_size(350,200)
        await session.get('https://www.student.ladok.se/student/loggain')
        chooseSite = await session.wait_for_element(10, 'p:nth-child(5) > a')
        await chooseSite.click()
        halmstad = await session.wait_for_element(10, '#searchlist > div:nth-child(5)')
        await halmstad.click()
        proceed_to_login = await session.wait_for_element(10, '#proceed')
        await proceed_to_login.click()
        username_element = await session.wait_for_element(10, 'body > div > div > div > div > form > div > div > div:nth-child(1) > div > input')
        await member.send(f"{username}")
        print(username)
        await username_element.send_keys(username)
        password = await session.get_element('body > div > div > div > div > form > div > div > div:nth-child(2) > div > input')
        await password.send_keys(password)
        login = await session.get_element('body > div > div > div > div > form > div > div > div:nth-child(3) > button')
        await login.click()
        real_name = await session.wait_for_element(10, '#navigation-first-meny > div.ldk-visa-desktop.ml-auto > div > ladok-inloggad-student')
        name = await real_name.get_text()
        current = await session.get_elements('#ldk-main-wrapper > ng-component > ladok-aktuell > div.row > div:nth-child(1) > ladok-pagaende-kurser > div:nth-child(3) > ladok-pagaende-kurser-i-struktur > div > ladok-pagaende-kurslista > div')
        for element in current:
            element = await element.get_element('div > h4 > ladok-kurslink > div.ldk-visa-desktop > a')
            element_text = await element.get_text()
            courseID = element_text.split("|")
            courseID = courseID[2]
            courseID = courseID[1:7]
            course_list_ladok.append(courseID) #ADD TO COURSE HERE
        uncompleted = await session.get_elements('#ldk-main-wrapper > ng-component > ladok-aktuell > div.row > div:nth-child(3) > ladok-oavslutade-kurser > div:nth-child(3) > ladok-oavslutade-kurser-i-struktur > div > ladok-kommande-kurslista > div')
        for element in uncompleted:
            element = await element.get_element('div > h4 > ladok-kurslink > div.ldk-visa-desktop > a')
            element_text = await element.get_text()
            courseID = element_text.split("|")
            courseID = courseID[2]
            courseID = courseID[1:7]
            course_list_ladok.append(courseID) #ADD TO COURSE HERE
        self_contained_courses = await session.get_elements('#ldk-main-wrapper > ng-component > ladok-aktuell > div.row > div:nth-child(3) > ladok-oavslutade-kurser > div:nth-child(4) > ladok-kommande-kurslista > div')
        for element in self_contained_courses:
            element = await element.get_element('div > h4 > ladok-kurslink > div.ldk-visa-desktop > a')
            element_text = await element.get_text()
            courseID = element_text.split("|")
            courseID = courseID[2]
            courseID = courseID[1:7]
            course_list_ladok.append(courseID) #ADD TO COURSE HERE
        fullname = name.split("|")
        fullname = fullname[0]
        fullname = fullname.split(",")
        firstname = fullname[1]
        firstname = firstname[1:-1]
        lastname = fullname[0]
        fullname = firstname + " " + lastname
        print(fullname) # FULLNAME HERE
        await session.close()
    await member.send(f"Om du angivet dina uppgifter rätt {fullname} kommer här kommer dina kurser, dessa har du även tillgång till nu:")
    topyear = 1
    for course in course_list:
            discord_courseID = course.get_courseID()
            for courseID in course_list_ladok:
                if(discord_courseID==courseID):
                    course_year=int(course.get_year())
                    if(course_year > topyear):
                        topyear = course_year
                    channel = bot.get_channel(int(course.get_channelID()))
                    await channel.set_permissions(member, read_messages=True,
                                                        send_messages=True)
    for courseID in course_list_ladok:
        await member.send(f"{courseID}")
    years = {
        1: "549996194898771978",
        2: "549996363400740866",
        3: "549996416882442270",
        4: "553999707689451532",
        5: "553999955228884993",
    }
    role = years[topyear]
    guild = bot.get_guild(547454095360000011)
    role_disc = guild.get_role(int(role))
    member_guild = guild.get_member(member.id)
    await member_guild.add_roles(role_disc)
    await member_guild.edit(nick=fullname)

'''async def register_ladok(user):
    print("Register")
    member = user.get_member()
    ID = user.__getattribute__("ID")
    username = user.__getattribute__("username")
    password = user.__getattribute__("password")
    course_list_ladok = []
    await member.create_dm()
    display = Display(visible=0, size=(800, 400))
    display.start()
    print("Before driver")
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-extensions')
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')    
    try:
        driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver", chrome_options=options)
        driver.set_window_size(800,400)
    except Exception as e:
        print(f"Driver Failed: {e}")
    driver.get('https://www.student.ladok.se/student/loggain')
    #driver.find_element_by_link_text('Välj lärosäte / Choose university').click()
    try:
        choose_learning = WebDriverWait(driver, 40).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div/p[3]/a"))
        )
        choose_learning.click()
    except Exception as e:
        print(e)
    try:
        search = WebDriverWait(driver, 40).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div[1]/form/div[2]/div[5]")))
        search.click()
    except Exception as e:
        print(e)
    try:
        element = WebDriverWait(driver, 40).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='proceed']")))
        element.click()
    except Exception as e:
        print(e)
    try:
        element = WebDriverWait(driver, 40).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div/form/div/div/div[1]/div/input")))
        element.send_keys(username)
        passwordField = driver.find_element_by_xpath("/html/body/div[1]/div/div/div/form/div/div/div[2]/div/input")
        passwordField.send_keys(password)
        driver.find_element_by_xpath("/html/body/div[1]/div/div/div/form/div/div/div[3]/button").click()
    except Exception as e:
        print(e)
    try:
        element = WebDriverWait(driver, 40).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/ladok-applikation/div/main/div/ng-component/ladok-aktuell/div[2]/div[1]/ladok-pagaende-kurser/div[3]/ladok-pagaende-kurser-i-struktur/div/ladok-pagaende-kurslista/div[1]/div/h4/ladok-kurslink/div[2]/a")))
    except Exception as e:
        print(e)
    current = driver.find_elements_by_xpath("/html/body/ladok-applikation/div/main/div/ng-component/ladok-aktuell/div[2]/div[1]/ladok-pagaende-kurser/div[3]/ladok-pagaende-kurser-i-struktur/div/ladok-pagaende-kurslista/div")
    print("--------Kurser Ladok--------")
    for element in current:
        courseID = element.find_element_by_xpath("./div/h4/ladok-kurslink/div[2]/a")
        courseID = courseID.get_attribute('textContent')
        courseID = courseID.split("|")
        courseID = courseID[2]
        courseID = courseID[1:7]
        course_list_ladok.append(courseID)
    fullname = driver.find_element_by_xpath("/html/body/ladok-applikation/div/header/ladok-meny/div/nav[1]/div[2]/div[1]/div/ladok-inloggad-student")
    fullname = fullname.get_attribute('textContent')
    old = driver.find_elements_by_xpath("/html/body/ladok-applikation/div/main/div/ng-component/ladok-aktuell/div[2]/div[3]/ladok-oavslutade-kurser/div[3]/ladok-oavslutade-kurser-i-struktur/div/ladok-kommande-kurslista/div")
    for element in old:
        course = element.find_element_by_xpath("./div/h4/ladok-kurslink/div[2]/a")
        courseID = course.get_attribute('textContent')
        courseID = courseID.split("|")
        courseID = courseID[2]
        courseID = courseID[1:7]
        course_list_ladok.append(courseID)
    fri = driver.find_elements_by_xpath("/html/body/ladok-applikation/div/main/div/ng-component/ladok-aktuell/div[2]/div[3]/ladok-oavslutade-kurser/div[4]/ladok-kommande-kurslista/div")
    for element in fri:
        course = element.find_element_by_xpath("./div/h4/ladok-kurslink/div[2]/a")
        courseID = course.get_attribute('textContent')
        courseID = courseID.split("|")
        courseID = courseID[2]
        courseID = courseID[1:7]
    driver.quit()
    display.stop()
    fullname = fullname.split("|")
    fullname = fullname[0]
    fullname = fullname.split(",")
    firstname = fullname[1]
    firstname = firstname[1:-2]
    lastname = fullname[0]
    fullname = firstname + " " + lastname
    await member.send(f"Om du angivet dina uppgifter rätt {fullname} kommer här kommer dina kurser, dessa har du även tillgång till nu:")
    topyear = 1
    for course in course_list:
            discord_courseID = course.get_courseID()
            for courseID in course_list_ladok:
                if(discord_courseID==courseID):
                    course_year=int(course.get_year())
                    if(course_year > topyear):
                        topyear = course_year
                    channel = bot.get_channel(int(course.get_channelID()))
                    await channel.set_permissions(member, read_messages=True,
                                                        send_messages=True)
    for courseID in course_list_ladok:
        await member.send(f"{courseID}")
    years = {
        1: "549996194898771978",
        2: "549996363400740866",
        3: "549996416882442270",
        4: "553999707689451532",
        5: "553999955228884993",
    }
    role = years[topyear]
    guild = bot.get_guild(547454095360000011)
    role_disc = guild.get_role(int(role))
    member_guild = guild.get_member(member.id)
    await member_guild.add_roles(role_disc)
    await member_guild.edit(nick=fullname)'''             
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
    await member.send(f"Om du angivet dina uppgifter rätt kommer här kommer ditt namn:")
    #for l in name:
    await member.send(f"Hej {name}.")
    print(type(member))
    await member.edit(nick=name)
    

local = "NTU2MDE3MzUzNTQwNzYzNjU5.D2znBw.0NOi0JUtvV8GmrprO9F7RzTFrFU"
master = "NTU0NjQ5MTM2ODU1NjQ2MjQ5.D2fs0Q.YV3dm7riiVMxI36VENnjlvGlg30"
course_file = open("courses/courses.txt", "r")
year=-1

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
#--------- TO START MASTER BOT --------------
if(platform.uname()[1]=="raspberrypi"):
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
        #bot.run(master)
    except Exception as e:
        print(f"Fail bot: {e}")
#--------- TO START BOT LOCAL BOT 0001 ----------------
elif(sys.argv[1] == "0001"):
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
