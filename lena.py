##########################################################
# Importations :
import asyncio
import datetime
import os
import random
import shutil
import sys

import discord
from discord.ext import commands, tasks
from discord_slash import *
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_choice, create_option

import emoji
from adv import *
from advance_gestion import *
from classes import *
from commands_files.alice_stats_endler import *
from commands_files.command_duty import adventureDutySelect
from commands_files.command_encyclopedia import *
from commands_files.command_expedition import *
from commands_files.command_fight import *
from commands_files.command_help import *
from commands_files.command_inventory import *
from commands_files.command_patchnote import *
from commands_files.command_points import *
from commands_files.command_procuration import *
from commands_files.command_shop import *
from commands_files.command_start import *
from commands_files.sussess_endler import *
from data.bot_tokens import lenapy, shushipy
from data.database import *
from donnes import *
from gestion import *
from datetime import datetime

###########################################################
# Initialisations des variables de bases :
started = False
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="l!",
                   description="LenaPy par LenaicU", intents=intents)
slash = SlashCommand(bot, sync_commands=True)

existDir(absPath + "/userProfile/")
existDir(absPath + "/data/images/")
existDir(absPath + "/data/database/")
existDir(absPath + "/data/images/headgears/")
existDir(absPath + "/data/images/weapons/")
existDir(absPath + "/data/images/char_icons/")
existDir(absPath + "/data/patch/")
existDir(absPath + "/data/fightLogs/")
existDir(absPath + "/data/images/elemIcon/")
existDir(absPath + "/data/backups/")

if not(os.path.exists("./data/advScriptTxt/")):
    raise Exception("Missing folder error : advScriptTxt do not exist")

for verif in allActs:
    if not(os.path.exists("./data/advScriptTxt/"+verif[0])):
        raise Exception(
            "Missing folder error : {0} do not exist".format(verif[0]))
    else:
        for fileVerif in verif[1:]:
            if not(os.path.exists("./data/advScriptTxt/"+verif[0]+"/"+fileVerif)):
                raise Exception("Missing file error : {0} do not exist".format(
                    verif[0]+"/"+fileVerif))

actualyFight, actualyQuickFight = [], []
pathUserProfile = absPath + "/userProfile/"

###########################################################
# Initialisation
allShop = weapons + skills + stuffs + others

class shopClass:
    """The class who endle the shop\n
    Maybe I should shearch how it's writed...
    """

    def __init__(self, shopList: list = []):
        """When inited, look for a existing shop data in the database and load it"""
        self.shopping = []
        summation = 0
        for a in shopRepatition:
            summation += a
        cmpt = 0
        while cmpt < summation:
            self.shopping.append(None)
            cmpt += 1

        if shopList != False:
            for a in range(0, len(shopList)):
                if a != None:
                    nani = whatIsThat(shopList[a])
                    try:
                        if nani == 0:
                            self.shopping[a] = findWeapon(shopList[a])
                        elif nani == 1:
                            self.shopping[a] = findSkill(shopList[a])
                        elif nani == 2:
                            self.shopping[a] = findStuff(shopList[a])
                        elif nani == 3:
                            self.shopping[a] = findOther(shopList[a])
                    except:
                        pass

    async def newShop(self):
        """Genere a new shop and upload it in the database\n
        - Returns\n
            - ``True`` if it succed
            - ``False`` else"""
        try:
            shopping = list(range(0, len(self.shopping)))

            if globalVar.fightEnabled():
                babies = datetime.now() + horaire + timedelta(hours=1)
                while babies.hour % 3 != 0:
                    babies = babies + timedelta(hours=1)

                await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="Prochain shop ?? "+babies.strftime('%Hh')))

            shopWeap, shopSkill, shopStuff, ShopOther = [], [], [], others[:]
            for a in weapons:
                if a.price > 0:
                    shopWeap.append(a)
                    if a in weapons[:3]:
                        shopWeap.append(a)

            for a in skills:
                if a.price > 0:
                    shopSkill.append(a)
                    if a in skills[:5]:
                        shopWeap.append(a)

            for a in stuffs:
                if a.price > 0:
                    shopStuff.append(a)
                    if a in stuffs[:5]:
                        shopWeap.append(a)

            temp = shopRepatition
            tablShop: List[list[Union[weapon, skill, stuff, other]]] = [
                shopWeap, shopSkill, shopStuff, ShopOther]
            cmp = 0
            for a in [0, 1, 2, 3]:
                cmpt = 0
                while cmpt < temp[a]:
                    fee = random.randint(0, len(tablShop[a])-1)
                    shopping[cmp] = tablShop[a][fee]
                    tablShop[a].remove(tablShop[a][fee])
                    cmpt += 1
                    cmp += 1

            temp = ""
            stuffDB.addShop(shopping)
            for a in shopping:
                temp += f"\n{a.name}"

            print("\n--------------\nLe nouveau shop est :"+temp+"\n------------")
            self.shopping = shopping
            return True
        except:
            return False

async def inventoryVerif(bot, toVerif: Union[char, str]):
    if type(toVerif) == str:
        user = loadCharFile(absPath + "/userProfile/" + toVerif)
    else:
        user = toVerif
    aliceStatsDb.addUser(user)
    allReadySee, haveUltimate, modifSkill, modifStuff = [], False, 0, 0
    ballerine = "Une ou plusieurs comp??tences ont ??t?? d??s??quip??s de votre personnage :\n"
    babie = "Un ou plusieurs ??quipements ont ??t?? retir?? de votre inventaire :\n"

    for a in range(0, 7):
        if type(user.skills[a]) == skill:
            if user.skills[a] in allReadySee:
                ballerine += f"\n__{user.skills[a].name}__ (Doublon)"
                modifSkill += 1
                user.skills[a] = "0"
            else:
                allReadySee += [user.skills[a]]

            if user.skills[a] != "0" and not(user.skills[a].havConds(user=user)):
                ballerine += f"\n__{user.skills[a].name}__ (Conditions non respect??es)"
                modifSkill += 1
                user.skills[a] = "0"

            if user.skills[a] != "0" and user.skills[a].ultimate and haveUltimate:
                ballerine += f"\n__{user.skills[a].name}__ (Plus de 1 comp??tence ultime ??quip??e)"
                modifSkill += 1
                user.skills[a] = "0"
            elif user.skills[a] != "0" and user.skills[a].ultimate:
                haveUltimate = True

            if user.skills[a] != "0" and lvlToUnlockSkill[a] > user.level:
                ballerine += f"\n__{user.skills[a].name}__ (Emplacement non d??bloqu??)"
                modifSkill += 1
                user.skills[a] = "0"

    tablInventory = [user.weaponInventory, user.skillInventory,
                     user.stuffInventory, user.otherInventory]
    for y in tablInventory:
        allReadySee = []
        for a in y:
            if a not in allReadySee:
                allReadySee.append(a)
            else:
                babie += f"\n__{a.name}__ (Doublon)"
                modifStuff += 1
                y.remove(a)
                user.currencies += a.price

    if modifStuff > 0:
        user.weaponInventory, user.skillInventory, user.stuffInventory, user.otherInventory = tablInventory[
            0], tablInventory[1], tablInventory[2], tablInventory[3]
        babie += "\n\nCes objets vous ont ??t?? rembours??s"

    if modifSkill+modifStuff > 0:
        saveCharFile(user=user)
        try:
            toUser = await bot.fetch_user(user.owner)
            message = ""
            if modifSkill > 0:
                message += ballerine+"\n"
            if modifStuff > 0:
                message += babie
            await toUser.send(embed=discord.Embed(title="__Probl??me lors de la v??rification automatique de l'inventaire__", color=user.color, description=message))
        except:
            pass

        print(f"Le profil de {user.name} a ??t?? mise ?? jour")

    temp = ""

    for equip in user.stuff:
        if equip == None:
            for a in (0, 1, 2):
                if user.stuff[a] == None:
                    user.stuff[a] = [bbandeau, bshirt, bshoes][a]
                    temp += "<:LenaWhat:760884455727955978> __Objet non trouv??__ -> {0} {1}\n".format(
                        [bbandeau, bshirt, bshoes][a].emoji, [bbandeau, bshirt, bshoes][a].name)
        elif not(equip.havConds(user)):
            change = getAutoStuff(equip, user)
            user.stuff[equip.type] = change

            temp += "{0} {2} -> {1} {3}\n".format(
                equip.emoji, change.emoji, equip.name, change.name)

    if temp != "":
        temp = "Vous ne respectez pas les conditions de niveaux d'un ou plusieurs de vos ??quipements\nLe(s) ??quipement(s) suivant a(ont) automatiquement ??t?? remplac??(s) :\n\n"+temp
        saveCharFile(user=user)
        try:
            toUser = await bot.fetch_user(user.owner)
            await toUser.send(embed=discord.Embed(title="__Probl??me lors de la v??rification automatique de l'inventaire__", color=user.color, description=temp))
        except:
            pass

        print(f"Le profil de {user.name} a ??t?? mise ?? jour")

    userAchivments = achivement.getSuccess(user)
    tempMissingAchivRecompMsg = ""
    for ach in userAchivments.tablAllSuccess():
        if ach.haveSucced and ach.recompense != [None] and ach.recompense not in [["qe"], ["qh"]]:
            for rec in ach.recompense:
                whatty = whatIsThat(rec)
                obj = [findWeapon(rec), findSkill(rec), findStuff(rec)][whatty]

                if not(user.have(obj)):
                    if whatty == 0:
                        user.weaponInventory.append(obj)
                    elif whatty == 1:
                        user.skillInventory.append(obj)
                    elif whatty == 2:
                        user.stuffInventory.append(obj)

                    tempMissingAchivRecompMsg += "\n{0} {1} ({2})".format(
                        obj.emoji, obj.name, ach.name)
            saveCharFile("./userProfile/{0}.prof".format(user.owner), user)

    if tempMissingAchivRecompMsg != "":
        try:
            toUser = await bot.fetch_user(user.owner)
            await toUser.send(embed=discord.Embed(title="__Probl??me lors de la v??rification automatique de l'inventaire__", color=user.color, description="Une ou plusieurs r??compenses de succ??s n'ont pas ??t?? trouv??es dans votre inventaire et vous ont ??t?? restitu??e :\n"+tempMissingAchivRecompMsg))
            print("{0} n'avait pas toutes ces r??compenses de succ??s".format(user.name))
        except:
            pass

    if user.level > 55:
        user = loadCharFile(user=user)
        user.level, user.exp = 55, 0
        user = restats(user)

        saveCharFile(user=user)

        toSend = await bot.fetch_user(user.owner)

        try:
            await toSend.send(embed=discord.Embed(title="__Probl??me lors de la v??rification automatique de votre inventaire :__", description="Votre niveau est sup??rieur au niveau maximal, et ?? ??t?? ramen?? ?? ce dernier\nVos points bonus ont ??t?? r??nitialis??es\n\nPensez ?? faire un tour vers /prestige", color=light_blue))
        except:
            pass

bidule = stuffDB.getShop()
if bidule != False:
    shopping = shopClass(bidule["ShopListe"])
else:
    shopping = shopClass(False)
    shopping.newShop()

async def restart_program(bot: discord.Client, ctx=None):
    """If no teams are into a fight, restart the bot\n
    If a team fighting, wiat for them to finish then restart the bot"""
    if ctx != None:
        msg = await ctx.send(embed=discord.Embed(title="Red??marrage en attente...", description="V??rifications des ??quipes en combat..."))
    else:
        chan = await bot.fetch_channel(912137828614426707)
        msg = await chan.send(embed=discord.Embed(title="Red??marrage automatique en attente...", description="V??rifications des ??quipes en combat..."))
    globalVar.changeFightEnabled(False)
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Game(name="attendre la fin des combats en cours pour red??marrer"))

    globalVar.getRestartMsg(int(msg.id))
    fighting = True
    firstIt = True
    while fighting:
        fighting = False
        for team in userTeamDb.getAllTeamIds():
            if teamWinDB.isFightingBool(team)[0]:
                if firstIt:
                    teamTemp = userTeamDb.getTeamMember(team)
                    us = await bot.fetch_user(teamTemp[0])
                    await msg.edit(embed=discord.Embed(title="Red??marrage en attente...", description="Un combat est encore en cours <a:loading:862459118912667678> ({0})".format(us.mention)))
                    firstIt = False
                fighting = True
                break
        if fighting:
            await asyncio.sleep(3)

    await msg.edit(embed=discord.Embed(title="Red??marrage en attente...", description="Red??marrage en cours..."))
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game(name="red??marrer"))

    args = sys.argv[:]

    args.insert(0, sys.executable)
    if sys.platform == 'win32':
        args = ['"%s"' % arg for arg in args]
    os.execv(sys.executable, args)

def create_backup():
    """Copy all the characters profiles files into a new directory\n
    Return a ``string`` with the path of the backup directory"""
    now = datetime.now()
    nowStr = now.strftime("%Y%m%d_%H%M")
    path = "./data/backups/"+nowStr
    try:
        os.mkdir(path)
    except:
        pass

    for charFile in os.listdir("./userProfile/"):
        shutil.copy('./userProfile/{0}'.format(charFile), path+"/"+charFile)

    return "Un backup a ??t?? sauvegard?? ?? la destinaiton suivante :\n"+path

def delete_old_backups():
    """Remove backups directorys older than 3 days"""
    now = datetime.now()
    temp = ""
    for name in os.listdir("./data/backups/"):
        timeBUp = datetime.strptime(name, "%Y%m%d_%H%M")
        if now > timeBUp+timedelta(days=3):
            for files in os.listdir("./data/backups/{0}/".format(name)):
                os.remove("./data/backups/{0}/{1}".format(name, files))
            try:
                os.removedirs("./data/backups/{0}".format(name))
                temp += "./data/backups/{0} a ??t?? supprim??\n".format(name)
            except:
                temp += "./data/backups/{0} n'a pas pu ??tre supprim??\n".format(
                    name)
    return temp

async def remakeEmojis(ctx=None):
    if ctx != None:
        msg = await ctx.send(embed=discord.Embed(title="Remake des emojis..."))
    else:
        chan = await bot.fetch_channel(912137828614426707)
        msg = await chan.send(embed=discord.Embed(title="Remake des emojis..."))

    await bot.change_presence(status=discord.Status.idle, activity=discord.Game(name="refaire les emojis..."))

    async def refresh(text: str):
        await msg.edit(embed=discord.Embed(title="Remake des emojis...", description=text))

    await refresh("Suppression de la base de donn??es...")
    try:
        customIconDB.dropCustom_iconTablDB()
    except:
        pass
    await refresh("Supression des emojis...")

    iconGuildList = []
    if not(isLenapy):
        iconGuildList = ShushyCustomIcons
    else:
        iconGuildList = LenaCustomIcons

    allEmojisNum = 0
    for a in iconGuildList:
        emojiGuild = await bot.fetch_guild(a)
        allEmojisNum += len(emojiGuild.emojis)

    cmpt = 0
    now = datetime.now().second
    lastTime = copy.deepcopy(now)
    for a in iconGuildList:
        emojiGuild = await bot.fetch_guild(a)

        for b in emojiGuild.emojis:
            try:
                print("Emoji de {0} supprim??".format(b.name))
            except:
                pass
            await b.delete()
            await asyncio.sleep(0.5)
            cmpt += 1

            if now >= lastTime + 3 or (now <= 3 and now >= lastTime + 3 - 60):
                await refresh("Supression des emojis ({0} %)".format(int(cmpt/allEmojisNum*100)))
                lastTime = now

    await refresh("Cr??ation des ??mojis...")
    allChar = os.listdir("./userProfile/")
    lenAllChar = len(allChar)
    cmpt = 0

    for num in allChar:
        user = loadCharFile("./userProfile/"+num)
        await makeCustomIcon(bot, user)
        cmpt += 1

        if now >= lastTime + 3 or (now <= 3 and now >= lastTime + 3 - 60):
            await refresh("Cr??ation des ??mojis ({0} %)".format(int(cmpt/lenAllChar*100)))
            lastTime = now

    await refresh("Fini !")
    if ctx != None:
        await ctx.channel.send("Le remake des emojis est termin??es !", delete_after=10)

    ballerine = datetime.now() + horaire + timedelta(hours=1)
    while ballerine.hour % 3 != 0:
        ballerine = ballerine + timedelta(hours=1)

    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="Prochain shop ?? "+ballerine.strftime('%Hh')))

async def verifEmojis(ctx=None):
    if ctx != None:
        msg = await ctx.send(embed=discord.Embed(title="V??rification des ??mojis...", description="__Progression :__ 0%"))
    else:
        chan = await bot.fetch_channel(912137828614426707)
        msg = await chan.send(embed=discord.Embed(title="V??rification des ??mojis...", description="__Progression :__ 0%"))
    remaked, lastProgress = "", 0
    listAllUsersFiles = os.listdir("./userProfile/")
    lenAllUser, progress = len(listAllUsersFiles), 0
    try:
        for path in listAllUsersFiles:
            user, haveSucced = loadCharFile("./userProfile/"+path), False
            userIcon = await getUserIcon(bot, user)
            haveSucced = False
            for guildId in [ShushyCustomIcons, LenaCustomIcons][isLenapy]:
                guild = await bot.fetch_guild(guildId)
                try:
                    await guild.fetch_emoji(getEmojiObject(userIcon)["id"])
                    haveSucced = True
                    break
                except:
                    pass
            if not(haveSucced):
                customIconDB.removeUserIcon(user)
                await makeCustomIcon(bot, user)
                if await getUserIcon(bot, user) not in ['<:LenaWhat:760884455727955978>', '<a:lostSilver:917783593441456198>']:
                    remaked += "Emoji de {0} refait\n".format(user.name)
                else:
                    remaked += "Erreur lors du remake de l'emoji de {0}\n".format(
                        user.name)
            progress += 1

            if progress/lenAllUser * 100 > lastProgress + 5:
                await msg.edit(embed=discord.Embed(title="V??rification des ??mojis...", description="__Progression :__ {0}%\n".format(round(progress/lenAllUser * 100, 2))+remaked))
                lastProgress = progress/lenAllUser * 100

        await msg.edit(embed=discord.Embed(title="V??rification des ??mojis", description="__Progression :__ Termin??\n"+remaked, color=light_blue))
    except:
        await msg.edit(embed=discord.Embed(title="V??rification des ??mojis", description="__Interrompue__\n"+format_exc(), color=red))

@tasks.loop(seconds=1)
async def oneClock():
    """A simple clock who check every second if a minute have passed\n
    If it is the case, start ``minuteClock``"""
    tick = datetime.now()
    if tick.second % 60 == 0 and not(minuteClock.is_running()):
        minuteClock.start()

@tasks.loop(minutes=1)
async def minuteClock():
    """
        A simple clock who check every minutes if a hour have passed\n
        If it is the case, start ``hourClock``\n
        If ``oneClock`` is running, end it
    """
    if oneClock.is_running():
        oneClock.stop()
    tick = datetime.now()
    if tick.minute % 60 == 0 and not(hourClock.is_running()):
        hourClock.start()

@tasks.loop(hours=1)
async def hourClock():
    if minuteClock.is_running():
        minuteClock.stop()
    tick = datetime.now()+horaire
    if tick.hour % 3 == 0:
        temp = False
        while not(temp):
            temp = await shopping.newShop()

    elif tick.hour == 4:
        chan = await bot.fetch_channel(912137828614426707)
        if tick.day == 19:
            chan = await bot.fetch_channel(912137828614426707)
            await chan.send(embed=discord.Embed(title="__Reset des records__", color=light_blue, description=aliceStatsDb.resetRecords()))
        for log in os.listdir("./data/fightLogs/"):
            try:
                os.remove("./data/fightLogs/"+log)
                print("{0} supprim??".format("./data/fightLogs/"+log))
            except:
                print("{0} n'a pas pu ??tre supprim??".format(
                    "./data/fightLogs/"+log))
        await chan.send(embed=discord.Embed(title="__Suppression des logs__", color=light_blue, description="Les logs de combats ont ??t?? supprim??s"))
        await chan.send(embed=discord.Embed(title="__Auto backup__", color=light_blue, description=create_backup()))
        temp = delete_old_backups()
        if temp != "":
            await chan.send(embed=discord.Embed(title="__Auto backup__", color=light_blue, description=temp))
        await verifEmojis()

        for userPath in os.listdir("./userProfile/"):
            user = loadCharFile('./userProfile/{0}'.format(userPath))
            aliceStatsDb.updateJetonsCount(user, max(0,9-(userShopPurcent(user)//10)))
        await restart_program(bot)

    # Skill Verif
    for filename in os.listdir("./userProfile/"):
        await inventoryVerif(bot, filename)

# -------------------------------------------- ON READY --------------------------------------------
@bot.event
async def on_ready():
    print("\n---------\nThe bot is fully online ! Starting the initialisations things...\n---------\n")
    startMsg = globalVar.getRestartMsg()
    if startMsg != 0:                           # If the bot was rebooted with the admin command, change the status
        msg = await bot.fetch_channel(912137828614426707)
        msg = await msg.fetch_message(startMsg)

        await msg.edit(embed=discord.Embed(title="Red??marrage en cours...", description="Phase d'initalisation..."))
        globalVar.changeFightEnabled(True)

    # Shop reload and status change
    if bidule != False:
        ballerine = datetime.now() + horaire + timedelta(hours=1)
        while ballerine.hour % 3 != 0:
            ballerine = ballerine + timedelta(hours=1)

        if not(globalVar.fightEnabled()):
            await bot.change_presence(status=discord.Status.dnd, activity=discord.Game(name="Les combats sont actuellements d??sactiv??s"))
        else:
            await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="Prochain shop ?? "+ballerine.strftime('%Hh')))

    if not(oneClock.is_running()):
        oneClock.start()

    teamWinDB.resetAllFightingStatus()

    print("\nDownloading the emojis for the custom icons...")
    await downloadAllHeadGearPng(bot)
    await downloadAllWeapPng(bot)
    await downloadAllIconPng(bot)
    await downloadElementIcon(bot)
    print("Download complete\nVerefying the characters inventorys...")

    if isLenapy:
        for filename in os.listdir("./userProfile/"):
            await inventoryVerif(bot, filename)

        if os.path.exists("./userTeams/"):
            for teamPath in os.listdir("./userTeams/"):
                team = readSaveFiles("./userTeams/"+teamPath)[0]
                userTeamDb.updateTeam(int(teamPath.replace(".team", "")), team)
                os.remove("./userTeams/"+teamPath)
            os.rmdir("./userTeams/")

    print("\n------- End of the initialisation -------")
    if not(isLenapy):
        print(datetime.now().strftime('%H:%M'))

    if startMsg != 0:
        await msg.edit(embed=discord.Embed(title="Red??marrage en cours...", color=light_blue, description="Le bot a bien ??t?? red??marr??"))
        await msg.channel.send("Le red??marrage du bot est termin?? L??na", delete_after=10)
        globalVar.getRestartMsg(int(0))
        print("Red??marrage termin??")

# ====================================================================================================
#                                               COMMANDS
# ====================================================================================================

# -------------------------------------------- ON MESSAGE --------------------------------------------
@bot.event
async def on_message(ctx: discord.message.Message):
    if ctx.content.startswith("l!test") and ctx.author.id == 213027252953284609:
        user = loadCharFile("./userProfile/213027252953284609.prof".format(ctx.author.id))
        await makeCustomIcon(bot, user)
        await ctx.reply(embed=discord.Embed(title="__Icone de personnage__", color=user.color).set_image(url="https://cdn.discordapp.com/emojis/{0}.png".format(getEmojiObject(await getUserIcon(bot, user))["id"])))

    elif ctx.content.startswith("l!emoji") and ctx.author.id == 213027252953284609:
        try:
            user = loadCharFile("./userProfile/213027252953284609.prof".format(ctx.author.id))
            user.apparaAcc = user.apparaWeap = None
            tablStuff, user.showAcc = [
                ironHelmet, batEarRings, batPendant, fecaShield, anakiMask, catEars], True
            for handed in [0, 1]:
                user.handed = handed
                for stuffy in tablStuff:
                    user.stuff[0] = stuffy
                    imageFile = await makeCustomIcon(bot, user, True)
                    filing = open("./data/images/temp.png", "wb")
                    filing.write(imageFile)
                    filing.close()
                    filing = open("./data/images/temp.png", "rb")
                    await ctx.channel.send(content="Position : {0}".format(stuffy.position), file=discord.File(fp=filing))
                    filing.close()
        except:
            await ctx.channel.send(content=format_exc())

    else:
        pathUserProfile = "./userProfile/{0}.prof".format(ctx.author.id)
        if os.path.exists(pathUserProfile) and len(ctx.content) >= 3:
            try:
                await addExpUser(bot, pathUserProfile, ctx, 3, 3)
            except:
                print("Erreur dans la gestion du message de {0}".format(
                    ctx.author.name))
                print_exc()

# -------------------------------------------- ENCYCLOPEDIA --------------------------------------------

@slash.slash(name="encyclopedia", description="Vous permet de consulter l'encyclop??die", options=[
    create_option(
        name="destination", description="Que voulez vous consulter ?", required=True, option_type=3,
        choices=[
            create_choice(name="Accessoires", value="accessoires"),
            create_choice(name="V??tements", value="vetements"),
            create_choice(name="Chaussures", value="chaussures"),
            create_choice(name="Armes", value="armes"),
            create_choice(name="Comp??tences", value="competences"),
            create_choice(name="Alli??s Temporaires", value='tempAlies'),
            create_choice(name="Ennemis", value="ennemies"),
            create_choice(name="Boss", value="boss"),
            create_choice(name="Objets non-poss??d??s", value="locked"),
            create_choice(name="Succ??s", value="achivements")
        ]
    )
])
async def comEncyclopedia(ctx, destination):
    if not(await botChannelVerif(bot, ctx)):
        return 0

    pathUserProfile = absPath + "/userProfile/" + str(ctx.author.id) + ".prof"
    user = loadCharFile(pathUserProfile)

    await encylopedia(bot, ctx, destination, user)

# -------------------------------------------- FIGHT --------------------------------------------
# normal fight
@slash.subcommand(base="fight", name="normal", description="Permet de lancer un combat normal")
async def normal(ctx):
    msg = None
    if not(await botChannelVerif(bot, ctx)):
        return 0
    if not(globalVar.fightEnabled()):
        await ctx.send(embed=discord.Embed(title="__Combats d??sactiv??s__", description="Les combats sont actuellement d??sactiv??s pour cause de bug ou de d??ploiment imminant d'une mise ?? jour\nVeuillez vous r??f??rer au status du bot pour savoir si les combats sont d??sactiv??s ou non"), delete_after=10)
        return 0

    pathUserProfile = absPath + "/userProfile/" + str(ctx.author.id) + ".prof"
    try:
        user = loadCharFile(pathUserProfile)
    except:
        await ctx.send("Vous n'avez pas commenc?? l'aventure", delete_after=10)
        return 0

    ballerine, temp = 0, 0
    if user.team == 0:
        ballerine = user.owner
    else:
        ballerine = user.team

    timing = teamWinDB.getFightCooldown(ballerine)

    if timing > 0:
        if timing > 60*10:
            await ctx.send(embed=errorEmbed("Cooldown", "Votre ??quipe ne pourra faire de combats normaux que dans {0} minute{1} et {2} seconde{3}".format(timing//60, ["", "s"][timing//60 > 1], timing % 60, ["", "s"][timing % 60 > 1])), delete_after=10)
            return 0
        else:
            while 1:
                timing = teamWinDB.getFightCooldown(ballerine)
                if timing > 0:
                    try:
                        if msg == None:
                            msg = await ctx.send(embed=await getRandomStatsEmbed(bot, [user], text="Votre combat a ??t?? mis en liste d'attente (Reste {0}:{1})".format(timing//60, timing % 60)))
                        else:
                            await msg.edit(embed=await getRandomStatsEmbed(bot, [user], text="Votre combat a ??t?? mis en liste d'attente (Reste {0}:{1})".format(timing//60, timing % 60)))
                    except:
                        pass
                    await asyncio.sleep(10)
                else:
                    try:
                        if msg == None:
                            msg = await ctx.send(embed=await getRandomStatsEmbed(bot, [user], text="Combat en cour de g??n??ration..."))
                        else:
                            await msg.edit(embed=await getRandomStatsEmbed(bot, [user], text="Combat en cour de g??n??ration..."))
                    except:
                        pass
                    break

    fightingStatus = teamWinDB.isFightingBool(ballerine)
    if fightingStatus[0]:
        channel = await bot.fetch_channel(fightingStatus[2])
        fightingMessage = await channel.fetch_message(fightingStatus[0])

        fightingRespond = "__Votre ??quipe affronte actuellement :__\n"
        temp = ""
        for letter in fightingStatus[1]:
            if letter == ";" and len(temp) > 0:
                ennemi = findEnnemi(temp)
                if ennemi == None:
                    ennemi = findAllie(temp)
                if ennemi != None:
                    fightingRespond += "{0} {1}\n".format(
                        ennemi.icon, ennemi.name)
                else:
                    fightingRespond += "<:blocked:897631107602841600> L'ennemi n'a pas pu ??tre trouv??\n"
                temp = ""
            else:
                temp += letter

        if msg == None:
            await ctx.send(embed=discord.Embed(title="__/fight__", color=user.color, description=fightingRespond+"\nsur __[{0}]({1})__".format(channel.guild.name, fightingMessage.jump_url)), delete_after=15)
        else:
            await msg.edit(embed=discord.Embed(title="__/fight__", color=user.color, description=fightingRespond+"\nsur __[{0}]({1})__".format(channel.guild.name, fightingMessage.jump_url)), delete_after=15)
        return 0

    team1 = []
    if user.team != 0:
        for a in userTeamDb.getTeamMember(user.team):
            team1 += [loadCharFile("./userProfile/{0}.prof".format(a))]
    else:
        team1 = [user]

    # Random event
    fun, teamLvl = random.randint(0, 99), 0
    for ent in team1:
        teamLvl = max(ent.level,teamLvl)

    if fun < 0:                # For testing purposes
        temp = copy.deepcopy(findAllie("Lena"))
        temp.changeLevel(50)
        await fight(bot, [temp], [], ctx, False, procurFight=True, msg=msg)

    elif fun < 1:              # All OctoHeals ! Yes, it's for you H
        temp = team1
        temp.sort(key=lambda overheal: overheal.level, reverse=True)
        maxLvl = temp[0].level

        team2 = []
        lenBoucle = 8
        cmpt = 0

        octoHealVet = findEnnemi("Octo Soigneur V??t??ran")
        octoHeal = findEnnemi("Octo Soigneur")

        if maxLvl < octoHealVet.baseLvl:
            alea = copy.deepcopy(octoHeal)
        else:
            alea = copy.deepcopy(octoHealVet)

        alea.changeLevel(maxLvl)
        alea.charisma = alea.charisma//2

        while cmpt < lenBoucle:
            team2.append(alea)
            cmpt += 1

        await fight(bot, team1, team2, ctx, False, msg=msg)

    elif fun < 2:              # All Temmies
        temp = team1
        temp.sort(key=lambda overheal: overheal.level, reverse=True)
        maxLvl = temp[0].level

        team2 = []
        lenBoucle = 8
        cmpt = 0

        alea = copy.deepcopy(findEnnemi("Temmie"))
        alea.changeLevel(maxLvl)
        alea.magie = alea.magie // 3

        while cmpt < lenBoucle:
            team2.append(alea)
            cmpt += 1

        await fight(bot, team1, team2, ctx, False, msg=msg)

    elif fun < 3:              # BOUM BOUM BOUM BOUM
        temp = team1
        temp.sort(key=lambda overheal: overheal.level, reverse=True)
        maxLvl = temp[0].level

        team2 = []
        lenBoucle = 8
        cmpt = 0

        alea = copy.deepcopy(findEnnemi("OctoBOUM"))
        alea.skills, alea.weapon, alea.magie, alea.exp = [
            totalAnnilCastSkill0, None, None, None, None, None, None], BOUMBOUMBOUMBOUMweap, int(alea.magie * 2), 12
        alea.changeLevel(maxLvl)

        while cmpt < lenBoucle:
            team2.append(alea)
            cmpt += 1

        await fight(bot, team1, team2, ctx, False, msg=msg)

    elif fun < 10 and teamLvl >= 25:             # Raid
        if msg == None:
            msg = await ctx.send(embed=discord.Embed(title="__Combat de raid__", color=light_blue, description="Les ??quipes sont en cours de g??n??ration..."))
        try:
            tablAllTeams, allReadySeen = userTeamDb.getAllTeamIds(), []
            if user.team not in ["0",0]:
                tablAllTeams.remove(user.team)
            random.shuffle(tablAllTeams)

            moyTeam = 0
            for a in team1:
                moyTeam += a.level
                allReadySeen.append(a.owner)

            moyTeam = moyTeam/len(team1)

            for tempTeamId in tablAllTeams:
                tempTeam, moyTempTeam = [], 0
                for a in userTeamDb.getTeamMember(tempTeamId):
                    if a not in allReadySeen:
                        tempUser = loadCharFile(
                            "./userProfile/{0}.prof".format(a))
                        moyTempTeam += tempUser.level
                        tempTeam += [tempUser]

                moyTempTeam = moyTempTeam/max(1, len(tempTeam))
                if moyTeam <= moyTempTeam+10 and moyTeam >= moyTempTeam-10:
                    team1 += tempTeam
                    break

            temp = team1
            temp.sort(key=lambda overheal: overheal.level, reverse=True)
            maxLvl = temp[0].level
            team2 = []
            alea = copy.deepcopy(
                tablRaidBoss[random.randint(0, len(tablRaidBoss)-1)])

            alea.changeLevel(maxLvl)
            team2.append(alea)

            await fight(bot, team1, team2, ctx, False, bigMap=True, msg=msg)
        except:
            await msg.edit(embed=discord.Embed(title="__Unknow error during fight__", description=format_exc()))
            teamWinDB.changeFighting(team1[0].team, value=False, channel=0)

    elif fun < 20:              # Procu Fight
        level = team1[0].level
        team1, team2, randomRoll = [], [], random.randint(0, 99)
        if randomRoll < 60: # ClemClem
            procurData = procurTempStuff["Cl??mence Exalt??e"]
            ent = copy.deepcopy(findAllie("Cl??mence Exalt??e"))
            level += random.randint(0, 100)
            ent.changeLevel(level)
            ent.stuff = [
                stuff(procurData[1][0],procurData[1][1],0,0,int(procurData[4][0][0]*procurData[4][0][1]*ent.level),int(procurData[4][1][0]*procurData[4][1][1]*ent.level),int(procurData[4][2][0]*procurData[4][2][1]*ent.level),int(procurData[4][3][0]*procurData[4][3][1]*ent.level),int(procurData[4][4][0]*procurData[4][4][1]*ent.level),int(procurData[4][5][0]*procurData[4][5][1]*ent.level),int(procurData[4][6][0]*procurData[4][6][1]*ent.level),int(procurData[4][7][0]*procurData[4][7][1]*ent.level),int(procurData[4][8][0]*procurData[4][8][1]*ent.level),int(procurData[4][9][0]*procurData[4][9][1]*ent.level),emoji=procurData[1][2]),
                stuff(procurData[2][0],procurData[2][1],1,0,int(procurData[4][0][0]*procurData[4][0][1]*ent.level),int(procurData[4][1][0]*procurData[4][1][1]*ent.level),int(procurData[4][2][0]*procurData[4][2][1]*ent.level),int(procurData[4][3][0]*procurData[4][3][1]*ent.level),int(procurData[4][4][0]*procurData[4][4][1]*ent.level),int(procurData[4][5][0]*procurData[4][5][1]*ent.level),int(procurData[4][6][0]*procurData[4][6][1]*ent.level),int(procurData[4][7][0]*procurData[4][7][1]*ent.level),int(procurData[4][8][0]*procurData[4][8][1]*ent.level),int(procurData[4][9][0]*procurData[4][9][1]*ent.level),emoji=procurData[2][2]),
                stuff(procurData[3][0],procurData[3][1],0,0,int(procurData[4][0][0]*procurData[4][0][1]*ent.level),int(procurData[4][1][0]*procurData[4][1][1]*ent.level),int(procurData[4][2][0]*procurData[4][2][1]*ent.level),int(procurData[4][3][0]*procurData[4][3][1]*ent.level),int(procurData[4][4][0]*procurData[4][4][1]*ent.level),int(procurData[4][5][0]*procurData[4][5][1]*ent.level),int(procurData[4][6][0]*procurData[4][6][1]*ent.level),int(procurData[4][7][0]*procurData[4][7][1]*ent.level),int(procurData[4][8][0]*procurData[4][8][1]*ent.level),int(procurData[4][9][0]*procurData[4][9][1]*ent.level),emoji=procurData[3][2])
            ]

            team1.append(ent)

        elif randomRoll < 100:  # Luna
            ent = copy.deepcopy(findAllie("Luna pr??."))
            procurData = procurTempStuff["Luna pr??."]
            level += random.randint(0, 50)
            ent.changeLevel(level)

            ent.stuff = [
                stuff(procurData[1][0],procurData[1][1],0,0,int(procurData[4][0][0]*procurData[4][0][1]*ent.level),int(procurData[4][1][0]*procurData[4][1][1]*ent.level),int(procurData[4][2][0]*procurData[4][2][1]*ent.level),int(procurData[4][3][0]*procurData[4][3][1]*ent.level),int(procurData[4][4][0]*procurData[4][4][1]*ent.level),int(procurData[4][5][0]*procurData[4][5][1]*ent.level),int(procurData[4][6][0]*procurData[4][6][1]*ent.level),int(procurData[4][7][0]*procurData[4][7][1]*ent.level),int(procurData[4][8][0]*procurData[4][8][1]*ent.level),int(procurData[4][9][0]*procurData[4][9][1]*ent.level),emoji=procurData[1][2]),
                stuff(procurData[2][0],procurData[2][1],1,0,int(procurData[4][0][0]*procurData[4][0][1]*ent.level),int(procurData[4][1][0]*procurData[4][1][1]*ent.level),int(procurData[4][2][0]*procurData[4][2][1]*ent.level),int(procurData[4][3][0]*procurData[4][3][1]*ent.level),int(procurData[4][4][0]*procurData[4][4][1]*ent.level),int(procurData[4][5][0]*procurData[4][5][1]*ent.level),int(procurData[4][6][0]*procurData[4][6][1]*ent.level),int(procurData[4][7][0]*procurData[4][7][1]*ent.level),int(procurData[4][8][0]*procurData[4][8][1]*ent.level),int(procurData[4][9][0]*procurData[4][9][1]*ent.level),emoji=procurData[2][2]),
                stuff(procurData[3][0],procurData[3][1],0,0,int(procurData[4][0][0]*procurData[4][0][1]*ent.level),int(procurData[4][1][0]*procurData[4][1][1]*ent.level),int(procurData[4][2][0]*procurData[4][2][1]*ent.level),int(procurData[4][3][0]*procurData[4][3][1]*ent.level),int(procurData[4][4][0]*procurData[4][4][1]*ent.level),int(procurData[4][5][0]*procurData[4][5][1]*ent.level),int(procurData[4][6][0]*procurData[4][6][1]*ent.level),int(procurData[4][7][0]*procurData[4][7][1]*ent.level),int(procurData[4][8][0]*procurData[4][8][1]*ent.level),int(procurData[4][9][0]*procurData[4][9][1]*ent.level),emoji=procurData[2][2])
            ]

            team1.append(ent)

            if random.randint(0, 99) < 50:               # Eclipse Eternelle
                ent2 = copy.deepcopy(findAllie('Iliana pr??.'))
                procurData = procurTempStuff["Iliana pr??."]
                ent2.changeLevel(level)

                ent2.stuff = [
                    stuff(procurData[1][0],procurData[1][1],0,0,int(procurData[4][0][0]*procurData[4][0][1]*ent2.level),int(procurData[4][1][0]*procurData[4][1][1]*ent2.level),int(procurData[4][2][0]*procurData[4][2][1]*ent2.level),int(procurData[4][3][0]*procurData[4][3][1]*ent2.level),int(procurData[4][4][0]*procurData[4][4][1]*ent2.level),int(procurData[4][5][0]*procurData[4][5][1]*ent2.level),int(procurData[4][6][0]*procurData[4][6][1]*ent2.level),int(procurData[4][7][0]*procurData[4][7][1]*ent2.level),int(procurData[4][8][0]*procurData[4][8][1]*ent2.level),int(procurData[4][9][0]*procurData[4][9][1]*ent2.level),emoji=procurData[1][2]),
                    stuff(procurData[2][0],procurData[2][1],1,0,int(procurData[4][0][0]*procurData[4][0][1]*ent2.level),int(procurData[4][1][0]*procurData[4][1][1]*ent2.level),int(procurData[4][2][0]*procurData[4][2][1]*ent2.level),int(procurData[4][3][0]*procurData[4][3][1]*ent2.level),int(procurData[4][4][0]*procurData[4][4][1]*ent2.level),int(procurData[4][5][0]*procurData[4][5][1]*ent2.level),int(procurData[4][6][0]*procurData[4][6][1]*ent2.level),int(procurData[4][7][0]*procurData[4][7][1]*ent2.level),int(procurData[4][8][0]*procurData[4][8][1]*ent2.level),int(procurData[4][9][0]*procurData[4][9][1]*ent2.level),emoji=procurData[2][2]),
                    stuff(procurData[3][0],procurData[3][1],0,0,int(procurData[4][0][0]*procurData[4][0][1]*ent2.level),int(procurData[4][1][0]*procurData[4][1][1]*ent2.level),int(procurData[4][2][0]*procurData[4][2][1]*ent2.level),int(procurData[4][3][0]*procurData[4][3][1]*ent2.level),int(procurData[4][4][0]*procurData[4][4][1]*ent2.level),int(procurData[4][5][0]*procurData[4][5][1]*ent2.level),int(procurData[4][6][0]*procurData[4][6][1]*ent2.level),int(procurData[4][7][0]*procurData[4][7][1]*ent2.level),int(procurData[4][8][0]*procurData[4][8][1]*ent2.level),int(procurData[4][9][0]*procurData[4][9][1]*ent2.level),emoji=procurData[2][2])
                ]
                
                team1.append(ent2)

                if user.aspiration in [ALTRUISTE, IDOLE, INOVATEUR, PREVOYANT, VIGILANT, PROTECTEUR]:
                    team1 = [ent2, ent]

                boss = copy.deepcopy(unformBoss)
                boss.changeLevel(level + random.randint(201, 250))
                team2, listDangerous, cmpt = [boss], [findEnnemi('Lueur informe A'), findEnnemi('Ombre informe A'), findEnnemi('Ombre informe B')], 1
                while cmpt < 8:
                    temp = copy.deepcopy(listDangerous[random.randint(0, len(listDangerous)-1)])
                    temp.changeLevel(level + random.randint(100, 150))
                    team2.append(temp)
                    cmpt += 1

        else:
            procurShushiWeapEff = effect("T??n??bres d??phas??s", "procurShushiWeapEff", MAGIE, power=50,area=AREA_CIRCLE_1, type=TYPE_INDIRECT_DAMAGE, trigger=TRIGGER_END_OF_TURN)
            procurShushiWeap = weapon("Rapi??re magique", "procurShushiWeap", RANGE_MELEE, AREA_CIRCLE_3, 50, 80, magie=20, endurance=20, resistance=20, area=AREA_ARC_2, effectOnUse=procurShushiWeapEff)

        try:
            await fight(bot, team1, team2, ctx, False, procurFight=True, msg=msg)
        except:
            if msg == None:
                await ctx.send(embed=discord.Embed(title="__Unknow error during fight__", description=format_exc()))
            else:
                await msg.edit(embed=discord.Embed(title="__Unknow error during fight__", description=format_exc()))
            teamWinDB.changeFighting(team1[0].team, value=False, channel=0)

    else:
        await fight(bot, team1, [], ctx, False, msg=msg)

# quick fight
@slash.subcommand(base="fight", name="quick", description="Vous permet de faire un combat en sautant directement ?? la fin")
async def comQuickFight(ctx):
    if not(await botChannelVerif(bot, ctx)):
        return 0
    if not(globalVar.fightEnabled()):
        await ctx.send(embed=discord.Embed(title="__Combats d??sactiv??s__", description="Les combats sont actuellement d??sactiv??s pour cause de bug ou de d??ploiment imminant d'une mise ?? jour\nVeuillez vous r??f??rer au status du bot pour savoir si les combats sont d??sactiv??s ou non"), delete_after=10)
        return 0

    pathUserProfile = absPath + "/userProfile/" + str(ctx.author.id) + ".prof"
    try:
        user = loadCharFile(pathUserProfile)
    except:
        await ctx.send("Vous n'avez pas commenc?? l'aventure", delete_after=10)
        return 0

    ballerine, temp = 0, 0
    if user.team == 0:
        ballerine = user.owner
    else:
        ballerine = user.team

    timing = teamWinDB.getFightCooldown(ballerine, True)
    fightingStatus = teamWinDB.isFightingBool(ballerine)

    if fightingStatus[0]:
        channel = await bot.fetch_channel(fightingStatus[2])
        fightingMessage = await channel.fetch_message(fightingStatus[0])

        fightingRespond = "__Votre ??quipe affronte actuellement :__\n"
        temp = ""
        for letter in fightingStatus[1]:
            if letter == ";" and len(temp) > 0:
                ennemi = findEnnemi(temp)
                if ennemi == None:
                    ennemi = findAllie(temp)
                if ennemi != None:
                    fightingRespond += "{0} {1}\n".format(
                        ennemi.icon, ennemi.name)
                else:
                    fightingRespond += "<:blocked:897631107602841600> L'ennemi n'a pas pu ??tre trouv??\n"
                temp = ""
            else:
                temp += letter

        await ctx.send(embed=discord.Embed(title="__/fight__", color=user.color, description=fightingRespond+"\nsur __[{0}]({1})__".format(channel.guild.name, fightingMessage.jump_url)), delete_after=15)
        return 0
    elif timing > 0:
        await ctx.send(embed=errorEmbed("Cooldown", "Votre ??quipe ne pourra faire de combats rapide que dans {0} minute{1} et {2} seconde{3}".format(timing//60, ["", "s"][timing//60 > 1], timing % 60, ["", "s"][timing % 60 > 1])), delete_after=10)
        return 0

    team1 = []
    if user.team != 0:
        for a in userTeamDb.getTeamMember(user.team):
            team1 += [loadCharFile("./userProfile/{0}.prof".format(a))]
    else:
        team1 = [user]

    fun, teamLvl = random.randint(0, 99), 0
    for ent in team1:
        teamLvl = max(ent.level,teamLvl)

    if fun < 5 and teamLvl >= 25:             # Raid
        msg = await ctx.send(embed=discord.Embed(title="__Combat de raid__", color=light_blue, description="Les ??quipes sont en cours de g??n??ration..."))
        try:
            tablAllTeams, allReadySeen = userTeamDb.getAllTeamIds(), []
            try:
                tablAllTeams.remove(user.team)
            except:
                pass
            random.shuffle(tablAllTeams)

            moyTeam = 0
            for a in team1:
                moyTeam += a.level
                allReadySeen.append(a.owner)

            moyTeam = moyTeam/len(team1)

            for tempTeamId in tablAllTeams:
                tempTeam, moyTempTeam = [], 0
                for a in userTeamDb.getTeamMember(tempTeamId):
                    if a not in allReadySeen:
                        tempUser = loadCharFile(
                            "./userProfile/{0}.prof".format(a))
                        moyTempTeam += tempUser.level
                        tempTeam += [tempUser]

                moyTempTeam = moyTempTeam/max(1, len(tempTeam))
                if moyTeam <= moyTempTeam+10 and moyTeam >= moyTempTeam-10:
                    team1 += tempTeam
                    break

            temp = team1
            temp.sort(key=lambda overheal: overheal.level, reverse=True)
            maxLvl = temp[0].level
            team2 = []
            alea = copy.deepcopy(tablRaidBoss[random.randint(0, len(tablRaidBoss)-1)])
            #alea = copy.deepcopy(findEnnemi("Nacialisla"))

            alea.changeLevel(maxLvl)
            team2.append(alea)

            await fight(bot, team1, team2, ctx, True, bigMap=True, msg=msg)
        except:
            await msg.edit(embed=discord.Embed(title="__Unknow error during fight__", description=format_exc()))
            teamWinDB.changeFighting(team1[0].team, value=False, channel=0)

    else:
        await fight(bot, team1, [], ctx)

# octogone fight
@slash.subcommand(base="fight", subcommand_group="octogone", name="solo", description="Affrontez quelqu'un en 1v1 Gare Du Nord !", options=[
    create_option("versus", "Affronter qui ?", 6, required=True)
])
async def octogone(ctx, versus):
    if not(await botChannelVerif(bot, ctx)):
        return 0
    pathUserProfile = absPath + "/userProfile/" + str(ctx.author.id) + ".prof"
    if not(os.path.exists(pathUserProfile)):
        await ctx.send("Comment veut-tu affronter quelqu'un si tu n'a pas de personnage ?\nVa donc faire un tour vers /start", delete_after=15)
        return 0

    if os.path.exists(absPath + "/userProfile/" + str(versus.id) + ".prof"):
        await fight(bot, [loadCharFile(pathUserProfile)], [loadCharFile(absPath + "/userProfile/" + str(versus.id) + ".prof")], ctx, auto=False, octogone=True)

    elif versus.id in [623211750832996354, 769999212422234122]:
        temp = loadCharFile(pathUserProfile)
        tempi = tablAllAllies[0]
        tempi.changeLevel(50)
        await fight(bot, [temp], [tempi], ctx, auto=False, octogone=True)

    else:
        await ctx.send("La personne que tu as d??sign?? ne poss??de pas de personnage d??sol??", delete_after=15)

# team fight
@slash.subcommand(base="fight", subcommand_group="octogone", name="team", description="Affrontez l'??quipe de quelqu'un avec la votre", options=[
    create_option("versus", "Affronter qui ?", 6, required=True)
])
async def teamFight(ctx, versus):
    if not(await botChannelVerif(bot, ctx)):
        return 0
    pathUserProfile = absPath + "/userProfile/" + str(ctx.author.id) + ".prof"
    if not(os.path.exists(pathUserProfile)):
        await ctx.send("Vous ne poss??dez pas de personnage.\nAllez donc faire un tour vers /start", delete_after=15)
        return 0
    user = loadCharFile(pathUserProfile)
    team1 = []
    if user.team != 0:
        for a in userTeamDb.getTeamMember(user.team):
            team1 += [loadCharFile("./userProfile/{0}.prof".format(a))]
    else:
        team1 = [user]

    team2 = []
    pathOctogonedProfile = absPath + "/userProfile/" + str(versus.id) + ".prof"
    if not(os.path.exists(pathOctogonedProfile)) and versus.id not in [623211750832996354, 769999212422234122]:
        await ctx.send("L'utilisateur d??sign?? ne poss??de pas de personnage", delete_after=15)
        return 0

    if versus.id not in [623211750832996354, 769999212422234122]:
        octogoned = loadCharFile(pathOctogonedProfile, ctx)
        if octogoned.team != 0:
            for a in userTeamDb.getTeamMember(user.team):
                team2 += [loadCharFile("./userProfile/{0}.prof".format(a))]
        else:
            team2 = [octogoned]
    else:
        tablLenaTeam = ["Lena", "Gwendoline", "Shushi",
                        "Cl??mence", "Alice", "F??licit??", "H??l??ne", "Iliana"]
        for a in tablLenaTeam:
            alea = copy.deepcopy(findAllie(a))
            alea.changeLevel(55)
            team2.append(alea)

    await fight(bot, team1, team2, ctx, False, octogone=True)

# -------------------------------------------- COOLDOWN --------------------------------------------
@slash.slash(name="cooldowns", description="Vous donne les cooldowns des commandes /fight et /quickFight pour votre ??quipe")
async def cooldowns(ctx):
    pathUserProfile = absPath + "/userProfile/" + str(ctx.author.id) + ".prof"
    if os.path.exists(pathUserProfile):
        user = loadCharFile(pathUserProfile)
        involvedTeam, involvedEmoji = [[user.team,user.owner][user.team==0]], [await getUserIcon(bot,user)]

        for procur in user.haveProcurOn:
            usr = loadCharFile("./userProfile/{0}.prof".format(procur))
            if usr.team not in involvedTeam or usr.team == 0:
                involvedTeam.append([usr.team,user.owner][usr.team==0])
                involvedEmoji.append(await getUserIcon(bot,usr))
            else:
                for cmpt in range(len(involvedTeam)):
                    if involvedTeam[cmpt] == usr.team:
                        involvedEmoji[cmpt]+=await getUserIcon(bot,usr)
        
        color = user.color
        if not(globalVar.fightEnabled()):
            color = red
        toReply = discord.Embed(title="__Cooldowns des commandes Fight__", color=color)

        for cmpt in range(len(involvedTeam)):
            team = involvedTeam[cmpt]
            cd = teamWinDB.getFightCooldown(team)
            cd2 = teamWinDB.getFightCooldown(team, True)
            fcooldown, fseconds, fqcooldown, fqseconds, faccord, fqaccord, fsaccord, fqsaccord = cd//60, cd % 60, cd2//60, cd2 % 60, "", "", "", ""
            if fcooldown > 1:
                faccord = "s"
            if fqcooldown > 1:
                fqaccord = "s"
            if fseconds > 1:
                fsaccord = "s"
            if fqseconds > 1:
                fqsaccord = "s"

            fightingStatus = teamWinDB.isFightingBool(int(team))
            if not(globalVar.fightEnabled()):
                notFight = "**<:noneWeap:917311409585537075> __Les combats sont actuellement d??sactiv??es !__**\n\n"
                color = red
            else:
                notFight = ""
                color = user.color

            if fightingStatus[0]:
                channel = await bot.fetch_channel(fightingStatus[2])
                fightingMessage = await channel.fetch_message(fightingStatus[0])

                fightingRespond = "__Votre ??quipe affronte actuellement :__\n"
                temp = ""
                for letter in fightingStatus[1]:
                    if letter == ";" and len(temp) > 0:
                        ennemi = findEnnemi(temp)
                        if ennemi == None:
                            ennemi = findAllie(temp)
                        if ennemi != None:
                            fightingRespond += "{0} {1}\n".format(
                                ennemi.icon, ennemi.name)
                        else:
                            fightingRespond += "<:blocked:897631107602841600> L'ennemi n'a pas pu ??tre trouv??\n"
                        temp = ""
                    else:
                        temp += letter

                toReply.add_field(name="__Cooldowns__",value=involvedEmoji[cmpt]+"\n"+notFight+fightingRespond+"\nsur __[{0}]({1})__".format(channel.guild.name, fightingMessage.jump_url))
            else:
                toReply.add_field(name="__Cooldowns__",value=involvedEmoji[cmpt]+"\n"+notFight+f"__Normal__ : {fcooldown} minute{faccord} et {fseconds} seconde{fsaccord}\n__Quick__ : {fqcooldown} minute{fqaccord} et {fqseconds} seconde{fqsaccord}")
            
        try:
            await ctx.send(embed = toReply, delete_after=10)
        except:
            toReply.set_footer(text="/cooldown ({0}#{1})".format(ctx.author.name, ctx.author.discriminator),icon_url=ctx.author.avatar_url)
            await ctx.channel.send(embed= toReply, delete_after=10)

# -------------------------------------------- PATCHNOTE --------------------------------------------
@slash.slash(name="patchnote", description="Renvoie le dernier patchnote du bot")
async def patchnote(ctx):
    if not(await botChannelVerif(bot, ctx)):
        return 0
    await send_patchnote(ctx)

# -------------------------------------------- ROLL --------------------------------------------
@slash.slash(name="roll", description="Permet de lancer un d??", options=[
    create_option(name="min", description="Minimum du jet. Par d??faut, 1",
                  option_type=4, required=False),
    create_option(name="max", description="Minimum du jet. Par d??faut, 100",
                  option_type=4, required=False),
])
async def roll(ctx, min=1, max=100):
    if not(await botChannelVerif(bot, ctx)):
        return 0
    rollmes = rollMessage[random.randint(0, len(rollMessage)-1)]
    await ctx.send(embed=discord.Embed(title=f"???? roll {min} - {max}", color=light_blue, description=rollmes.format(random.randint(min, max))))

# -------------------------------------------- SHOP --------------------------------------------
@slash.slash(name="shop", description="Vous permet d'entrer dans le magasin")
async def shopSlash(ctx):
    if not(await botChannelVerif(bot, ctx)):
        return 0
    await shop2(bot, ctx, shopping.shopping)

# -------------------------------------------- INVENTORY --------------------------------------------
@slash.slash(name="inventory", description="Vous permet de naviger dans votre inventaire", options=[
    create_option("destination", "Dans quel inventaire voulez-vous aller ?", 3, required=False, choices=[
        create_choice("Equipement", "Equipement"),
        create_choice("Arme", "Arme"),
        create_choice("Comp??tences", "Comp??tences"),
        create_choice("Objets sp??ciaux", "Objets sp??ciaux"),
        create_choice("Elements", "Elements")
    ]),
    create_option(
        "procuration", "De qui voulez vous consulter l'inventaire ?", 6, required=False),
    create_option(
        "nom", "Le nom ou l'identifiant d'un objet. Les espaces peuvent ??tre remplac??s par des _", 3, required=False)
])
async def invent2(ctx, destination="Equipement", procuration=None, nom=None):
    if not(await botChannelVerif(bot, ctx)):
        return 0
    for a in range(5):
        if ["Equipement", "Arme", "Comp??tences", "Objets sp??ciaux", "Elements"][a] == destination:
            destination = a
            break

    if procuration != None:
        user = loadCharFile(absPath + "/userProfile/" +
                            str(procuration.id) + ".prof")
    else:
        user = loadCharFile(absPath + "/userProfile/" +
                            str(ctx.author.id) + ".prof")

    if nom != None:
        nom = nom.replace("_", " ")
        nom = remove_accents(nom.lower())
        while nom.endswith(" "):
            nom = nom[0:-1]

        if whatIsThat(nom) == None:
            research = weapons[:]+skills[:]+stuffs[:]+others[:]+[token,trans]
            lastResarch = []
            nameTempCmpt, lenName = 0, len(nom)
            while 1:
                lastResarch = research[:]
                if nameTempCmpt+1 <= lenName:
                    nameTempCmpt += 1
                else:
                    nameTempCmpt = lenName

                for a in research[:]:
                    temp = remove_accents(a.name.lower())
                    if nom[0:nameTempCmpt] not in temp:
                        research.remove(a)

                leni = len(research)
                if leni == 1:
                    nom = research[0].name
                    break
                elif leni <= 0 or nameTempCmpt == lenName:
                    desc = ""
                    options = []
                    for a in lastResarch:
                        have = ""
                        if not(user.have(a)):
                            have = "`"
                        desc += "{0} {2}{1}{2}\n".format(a.emoji, a.name, have)
                        options += [create_select_option(unhyperlink(
                            a.name), a.name, getEmojiObject(a.emoji))]

                    if len(options) > 24:
                        def getNameSortValue(obj):
                            cmpt = 0
                            for letter in nom:
                                if letter in obj.name:
                                    cmpt+=1
                            return cmpt
                        
                        lastResarch.sort(key=lambda obj:getNameSortValue(obj))
                        lastResarch = lastResarch[:24]
                        options, desc = [], ""
                        for a in lastResarch:
                            have = ""
                            if not(user.have(a)):
                                have = "`"
                            desc += "{0} {2}{1}{2}\n".format(a.emoji, a.name, have)
                            options += [create_select_option(unhyperlink(a.name), a.name, getEmojiObject(a.emoji))]

                    select = create_select(options, placeholder="S??lectionnez un objet :")
                    msg = await ctx.send(embed=discord.Embed(title="/inventory", color=light_blue, description="L'objet sp??cifi?? n'a pas ??t?? trouv??. Voici une liste des r??sultats les plus proches :\n\n"+desc), components=[create_actionrow(select)])

                    def check(m):
                        return m.author_id == ctx.author.id and m.origin_message.id == msg.id

                    try:
                        respond = await wait_for_component(bot, components=select, check=check, timeout=60)
                    except:
                        await msg.edit(embed=discord.Embed(title="/inventory", color=light_blue, description="Liste des r??sultats correspondant ?? la recherche\n\n"+desc), components=[])
                        return 0
                        break

                    nom = respond.values[0]
                    await msg.edit(embed=discord.Embed(title="/inventory", color=light_blue, description="L'objet sp??cifi?? n'a pas ??t?? trouv??. Voici une liste des r??sultats les plus proches :\n\n"+desc), components=[create_actionrow(getChoisenSelect(select, respond.values[0]))])
                    break

        if nom == token.name:
            obj = token
            repEmb = infoOther(obj, user)
            try:
                await ctx.send(embed=repEmb, components=[])
            except:
                await ctx.channel.send(embed=repEmb, components=[])
            return 0
        elif nom in [trans.name,"lb"]:
            transField = "La **Transcendance** est une comp??tence commune ?? tous les joueurs et alli??s temporaires d??bloqu??e et ??quip??e automatiquement d??s le d??but.\nLorsqu'utilis??e, cette comp??tence deviens l'une des comp??tences list??e si dessous en fonction du nombre de **jauges transcendiques** remplie ainsi que de l'aspiration du lanceur.\nLe nombre de jauges transcendiques disponibles dans un combat d??pend de divers crit??res. Chaques crit??res remplie rajoute une barre pour l'??quipe en question :\n> - L'??quipe comporte au moins 8 membres\n> - L'??quipe comporte au moins 16 membres\n> - L'??quipe adverse contient au moins 1 boss\n> - L'??quipe adverse est compos??e d'un boss AllvOne\n> - L'??quipe adverse est compos??e d'alli??s temporaires ou de joueurs\n\nLorsqu'utilis??e, toutes les **jauges transcendiques** de l'??quipe sont remises ?? 0, m??me si elles n'??taient pas toutes remplies."
            emby = discord.Embed(title="__Transcendance :__",color=light_blue,description=transField)
            await ctx.send(embed=emby)

            transNames, cmpt, tably = ["__Transcendances niveau 1__ <:lbFull:983450379205378088>","__Transcendances niveau 2__ <:lbFull:983450379205378088><:lbFull:983450379205378088>","__Transcendances niveau 3__ <:lbFull:983450379205378088><:lbFull:983450379205378088><:lbFull:983450379205378088>","__Transcendances niveau 4__ <:lbFull:983450379205378088><:lbFull:983450379205378088><:lbFull:983450379205378088><:lbFull:983450379205378088>"], 0, [lb1MinTabl,lb2MinTabl,lb3Tabl,[lb4]]
            
            while cmpt < 4:
                transField = ""
                for skilly in tably[cmpt]:
                    usedBy = ""
                    if cmpt != 3:
                        for cmpt2 in range(len(inspi)):
                            if [lb1Tabl,lb2Tabl,lb3Tabl][cmpt][cmpt2] == skilly:
                                usedBy += aspiEmoji[cmpt2]
                    else:
                        for cmpt2 in range(len(inspi)):
                            usedBy += aspiEmoji[cmpt2]
                    transField += "{0} __{1} :__ ({3})\n> {2}\n\n".format(skilly.emoji,skilly.name,skilly.description.replace("\n","\n> "),usedBy)
                emby = discord.Embed(title=transNames[cmpt],color=light_blue,description=transField)
                emby.set_thumbnail(url="https://cdn.discordapp.com/emojis/{0}.png".format(getEmojiObject(trans.emoji)["id"]))

                await ctx.channel.send(embed=emby)
                cmpt += 1
            return 1

        nom = [nom, None]

    else:
        nom = [None]

    if nom != [None]:
        await inventory(bot, ctx, nom[0], procur=user.owner)
    else:
        await inventoryV2(bot, ctx, destination, user)

# -------------------------------------------- POINTS --------------------------------------------
@slash.slash(name="points", description="Vous permet de r??partir vos points bonus", options=[
    create_option(
        "procuration", "De qui voulez vous consulter l'inventaire ?", 6, required=False)
])
async def pts(ctx, procuration=None):
    if not(await botChannelVerif(bot, ctx)):
        return 0
    await points(bot, ctx, ["/points", None], procuration, slashed=True)

# -------------------------------------------- TEAM --------------------------------------------
detailPlus = create_button(ButtonStyle.blue, "Aff. d??taill??", "???", "detail")
detailMinus = create_button(
    ButtonStyle.blue, "Aff. simplifi??", "???", detailPlus["custom_id"])

# team view
@slash.subcommand(base="team", name="view", description="Permet de voir les ??quipements de votre ??quipe ou de celle de quelqu'un d'autre", options=[
    create_option("joueur", "Voir l'??quipe d'un autre joueur",
                  6, required=False)
])
async def teamView(ctx, joueur=None):
    if not(await botChannelVerif(bot, ctx)):
        return 0
    if joueur == None:
        joueur = ctx.author
    pathUserProfile = absPath + "/userProfile/" + str(joueur.id) + ".prof"

    if os.path.exists(pathUserProfile):
        user, extended = loadCharFile(pathUserProfile), False
        msg = await loadingSlashEmbed(ctx)
        if user.team == 0:
            teamMates = [user]
        else:
            teamMates = []
            for usr in userTeamDb.getTeamMember(user.team):
                teamMates.append(loadCharFile(
                    path="./userProfile/{0}.prof".format(usr)))

        def checky(m):
            return m.author_id == ctx.author_id

        while 1:
            temp = ""
            if not(extended):
                for usr in teamMates:
                    level = str(usr.level) + ["", "<:ls:925860806602682369>{0}".format(usr.stars)][usr.stars > 0]
                    ballerine = f'{aspiEmoji[usr.aspiration]}|{usr.weapon.emoji}|{usr.stuff[0].emoji}{usr.stuff[1].emoji}{usr.stuff[2].emoji}|'
                    for cmpt in range(len(usr.skills)):
                        if type(usr.skills[cmpt]) == skill:
                            ballerine += usr.skills[cmpt].emoji
                        elif usr.level >= lvlToUnlockSkill[cmpt]:
                            ballerine += "<:noSkill:978458473018830858>"
                        else:
                            ballerine += "????"
                    ballerine += "\n\n"

                    icon = await getUserIcon(bot, usr)
                    points = ""
                    if usr.points > 0:
                        points = " *(+)*"
                    temp += f"__{icon} **{usr.name}** ({level})__{points}\n{ballerine}"
                if int(user.owner) == int(ctx.author.id):
                    embed = discord.Embed(title="/team view", color=user.color,description="__Votre ??quipe se compose de :__\n\n"+temp)
                else:
                    embed = discord.Embed(title="/team view", color=user.color,description="__L'??quipe de {0} se compose de :__\n\n".format(user.name)+temp)

                if user.team != 0:
                    embed.add_field(name="<:empty:866459463568850954>\n__R??sultats des derniers combats :__",value=teamWinDB.getVictoryStreakStr(user))

            else:
                embed = await getFullteamEmbed(bot, teamMates, user)

            await msg.edit(embed=embed, components=[create_actionrow([detailPlus, detailMinus][extended])])

            try:
                react = await wait_for_component(bot, msg, check=checky, timeout=60)
            except:

                await msg.edit(embed=embed, components=[])
                break

            if react.custom_id == detailPlus["custom_id"]:
                extended = not(extended)

# team add
@slash.subcommand(base="team", name="add", description="Permet de rajouter un joueur dans son ??quipe", options=[
    create_option("joueur", "Le joueur ?? rajouter", 6, required=True)
])
async def teamAdd(ctx, joueur):
    if not(await botChannelVerif(bot, ctx)):
        return 0
    pathUserProfile = absPath + "/userProfile/" + str(ctx.author.id) + ".prof"
    if os.path.exists(pathUserProfile):
        user = loadCharFile(pathUserProfile)

        msg = await loadingSlashEmbed(ctx)

        if user.team == 0:
            rdm = str(random.randint(1, 999999999))
            while rdm in userTeamDb.getAllTeamIds():
                rdm = str(random.randint(1, 999999999))
            userTeamDb.updateTeam(rdm, [user])
            user.team = rdm
            saveCharFile(pathUserProfile, user)

        noneCap, selfAdd, temp = True, False, userTeamDb.getTeamMember(
            user.team)

        if len(temp) >= 8:
            noneCap = False

        if ctx.author == joueur:
            selfAdd = True

        if noneCap and not(selfAdd):
            mention = joueur
            if os.path.exists(absPath + "/userProfile/" + str(mention.id) + ".prof"):
                allReadyinTeam, allReadyInThatTeam, mate = False, False, loadCharFile(
                    absPath + "/userProfile/" + str(mention.id) + ".prof")
                if mate.team != 0:
                    allReadyinTeam = True
                    if mate.team == user.team:
                        allReadyInThatTeam = True

                if not(allReadyinTeam):
                    await msg.edit(embed=discord.Embed(title="/team add "+joueur.name, color=user.color, description=f"{mention.mention}, {ctx.author.mention} vous propose de rejoidre son ??quipe. Qu'en dites vous ?"))
                    await msg.add_reaction(emoji.check)
                    await msg.add_reaction(emoji.cross)

                    def checkisIntendedUser(reaction, user):
                        return int(user.id) == int(mention.id)

                    try:
                        reaction = await bot.wait_for("reaction_add", timeout=60, check=checkisIntendedUser)
                    except:
                        await msg.clear_reactions()
                        await msg.edit(embed=errorEmbed("/team add "+joueur.name, "La commande n'a pas pu aboutir"))

                    if str(reaction[0]) == emoji.check:
                        mate.team = user.team
                        saveCharFile(absPath + "/userProfile/" +
                                     str(mention.id) + ".prof", mate)
                        team = userTeamDb.getTeamMember(user.team)
                        team.append(mention.id)
                        userTeamDb.updateTeam(user.team, team)
                        await msg.clear_reactions()
                        await msg.edit(embed=discord.Embed(title="/team add "+joueur.name, color=user.color, description="Vous faites dor??navent parti de la m??me ??quipe"))

                elif allReadyInThatTeam:
                    await msg.edit(embed=errorEmbed("/team add "+joueur.name, "Ce joueur est d??j?? dans ton ??quipe"))
                elif allReadyinTeam:
                    await msg.edit(embed=errorEmbed("/team add "+joueur.name, "Ce joueur a d??j?? une ??quipe"))

            else:
                await msg.edit(embed=errorEmbed("/team add "+joueur.name, "Cet utilisateur n'a pas commenc?? l'aventure"))
        elif selfAdd:
            await msg.edit(embed=errorEmbed("/team add "+joueur.name, "Vous voulez faire ??quipe avec vous-m??me ?"))
        else:
            await msg.edit(embed=errorEmbed("/team add "+joueur.name, "Votre ??quipe est d??j?? au complet"))

# team quit
@slash.subcommand(base="team", name="quit", description="Permet de quitter son ??quipe")
async def teamQuit(ctx):
    if not(await botChannelVerif(bot, ctx)):
        return 0
    pathUserProfile = absPath + "/userProfile/" + str(ctx.author.id) + ".prof"
    if os.path.exists(pathUserProfile):
        user = loadCharFile(pathUserProfile)

    if user.team != 0:
        team = userTeamDb.getTeamMember(user.team)
        team.remove(ctx.author.id)
        user.team = 0

        userTeamDb.updateTeam(user.team, team)
        await ctx.send(embed=discord.Embed(title="/team quit", color=user.color, description="Vous avez bien quitt?? votre ??quipe"))
        saveCharFile(pathUserProfile, user)
    else:
        await ctx.send(embed=errorEmbed("/team quit", "Vous n'avez aucune ??quipe ?? quitter"))

# team fact
@slash.subcommand(base="team", name="fact", description="Permet d'avoir des facts sur les membres de votre ??quipe")
async def teamFact(ctx):
    if not(await botChannelVerif(bot, ctx)):
        return 0
    pathUserProfile = absPath + "/userProfile/" + str(ctx.author.id) + ".prof"
    if os.path.exists(pathUserProfile):
        user = loadCharFile(pathUserProfile)

    teamUser = []

    if user.team != 0:
        for a in userTeamDb.getTeamMember(user.team):
            teamUser.append(loadCharFile(
                absPath + "/userProfile/" + str(a) + ".prof"))

    else:
        teamUser.append(user)

    button = create_actionrow(create_button(
        ButtonStyle.grey, "Autre fact", "????", "????"))
    msg = None

    while 1:
        embed = await getRandomStatsEmbed(bot, teamUser, "/team fact")
        if msg == None:
            msg = await ctx.send(embed=embed, components=[button])
        else:
            await msg.edit(embed=embed, components=[button])

        try:
            await wait_for_component(bot, msg, timeout=60)
        except:
            await msg.edit(embed=embed, components=[])
            break

# -------------------------------------------- HELP --------------------------------------------
@slash.slash(name="help", description="Ouvre la page d'aide du bot")
async def helpCom(ctx):
    if not(await botChannelVerif(bot, ctx)):
        return 0
    await helpBot(bot, ctx)

# -------------------------------------------- START --------------------------------------------
@slash.slash(name="start", description="Permet de commence l'aventure")
async def started(ctx):
    if not(await botChannelVerif(bot, ctx)):
        return 0
    await start(bot, ctx)

# -------------------------------------------- STATS --------------------------------------------
@slash.slash(name="stats", description="Permet de voir vos statistiques ou celles d'un autre joueur", options=[
    create_option(
        "joueur", "Voir les statistiques d'un autre joueur", 6, False)
])
async def statsCmd(ctx, joueur=None):
    if not(await botChannelVerif(bot, ctx)):
        return 0
    if joueur == None:
        pathUserProfile = absPath + "/userProfile/" + \
            str(ctx.author.id) + ".prof"
    else:
        pathUserProfile = absPath + "/userProfile/" + str(joueur.id) + ".prof"

    if os.path.exists(pathUserProfile):
        msg = await loadingSlashEmbed(ctx)
        user = loadCharFile(pathUserProfile)

        userIcon = await getUserIcon(bot, user)

        level = str(
            user.level)+['', "<:littleStar:925860806602682369>{0}".format(user.stars)][user.stars > 0]
        exp = [str(user.level*50-20), "MAX"][user.level == 55]
        rep = discord.Embed(title=f"__Page de statistique de {user.name} {userIcon}__", color=user.color,
                            description=f"__Niveau :__ {level}\n__Exp??rience :__ {user.exp} / {exp}\n\n__Element :__ {elemEmojis[user.element]} {elemNames[user.element]} ({elemEmojis[user.secElement]} {elemNames[user.secElement]})\n<:empty:866459463568850954>")

        rep.set_thumbnail(
            url="https://cdn.discordapp.com/emojis/{0}.png".format(getEmojiObject(userIcon)["id"]))
        rep.add_field(name="__Aspiration :__",
                      value=aspiEmoji[user.aspiration] + " " + inspi[user.aspiration], inline=False)

        sumStatsBonus = [user.majorPoints[0], user.majorPoints[1], user.majorPoints[2], user.majorPoints[3], user.majorPoints[4], user.majorPoints[5], user.majorPoints[6],
                         user.majorPoints[7], user.majorPoints[8], user.majorPoints[9], user.majorPoints[10], user.majorPoints[11], user.majorPoints[12], user.majorPoints[13], user.majorPoints[14]]

        for a in [user.weapon, user.stuff[0], user.stuff[1], user.stuff[2]]:
            sumStatsBonus[0] += a.strength
            sumStatsBonus[1] += a.endurance
            sumStatsBonus[2] += a.charisma
            sumStatsBonus[3] += a.agility
            sumStatsBonus[4] += a.precision
            sumStatsBonus[5] += a.intelligence
            sumStatsBonus[6] += a.magie
            sumStatsBonus[7] += a.resistance
            sumStatsBonus[8] += a.percing
            sumStatsBonus[9] += a.critical
            sumStatsBonus[10] += a.negativeHeal * -1
            sumStatsBonus[11] += a.negativeBoost * -1
            sumStatsBonus[12] += a.negativeShield * -1
            sumStatsBonus[13] += a.negativeDirect * -1
            sumStatsBonus[14] += a.negativeIndirect * -1

        for a in range(len(sumStatsBonus)):
            if sumStatsBonus[a] > 0:
                sumStatsBonus[a] = "+"+str(sumStatsBonus[a])

        rep.add_field(name="<:empty:866459463568850954>\n__Stats. principaux :__",
                      value=f"__Force :__ {user.strength} ({sumStatsBonus[0]})\n__Endurance :__ {user.endurance} ({sumStatsBonus[1]})\n__Charisme :__ {user.charisma} ({sumStatsBonus[2]})\n__Agilit?? :__ {user.agility} ({sumStatsBonus[3]})\n__Pr??cision :__ {user.precision} ({sumStatsBonus[4]})\n__Intelligence :__ {user.intelligence} ({sumStatsBonus[5]})\n__Magie :__ {user.magie} ({sumStatsBonus[6]})", inline=True)
        rep.add_field(name="<:empty:866459463568850954>\n__Stats. secondaires :__",
                      value=f"__R??sistance :__ {user.resistance} ({sumStatsBonus[7]})\n__P??n??tration :__ {user.percing} ({sumStatsBonus[8]})\n__Critique :__ {user.critical} ({sumStatsBonus[9]})", inline=True)
        rep.add_field(name="<:empty:866459463568850954>\n__Stats. d'actions :__",
                      value=f"__Soins :__ 0 ({sumStatsBonus[10]})\n__Boost et Malus :__ 0 ({sumStatsBonus[11]})\n__Armures :__ 0 ({sumStatsBonus[12]})\n__D??g??ts directs :__ 0 ({sumStatsBonus[13]})\n__D??g??ts indirects :__ 0 ({sumStatsBonus[14]})", inline=True)
        tempStuff, tempSkill = "", ""
        for a in [0, 1, 2]:
            tempStuff += f"{ user.stuff[a].emoji} {user.stuff[a].name}\n"

        for a in [0, 1, 2, 3, 4, 5, 6]:
            try:
                tempSkill += f"{user.skills[a].emoji} {user.skills[a].name}\n"
            except:
                if user.level >= lvlToUnlockSkill[a]:
                    tempSkill += " -\n"
                else:
                    tempSkill += " ????\n"

        rep.add_field(name="<:empty:866459463568850954>\n__Arme et ??quipements :__",
                      value=user.weapon.emoji+" "+user.weapon.name+"\n\n"+tempStuff, inline=True)
        rep.add_field(name="<:empty:866459463568850954>\n__Comp??tences :__",
                      value=tempSkill, inline=True)

        await msg.edit(embed=rep)

    else:
        if joueur == None:
            await ctx.send("Tu n'a pas commenc?? l'aventure")
        else:
            await ctx.send("{0} n'a pas commenc?? l'aventure".format(joueur.name))

# -------------------------------------------- MANUEL --------------------------------------------
@slash.slash(name="manuel", description="Permet de consulter le manuel de l'Aventure", options=[
    create_option(
        "page", "Sp??cifiez une page ?? laquelle ouvrir le manuel", 4, False)
])
async def manuel(ctx, page=0):
    if not(await botChannelVerif(bot, ctx)):
        return 0
    msg, manPage, chapterInt, ini = await loadingSlashEmbed(ctx), page, 0, True

    def checkReaction(reaction, user):
        return int(reaction.message.id) == int(msg.id) and int(user.id) == int(ctx.author.id) and (str(reaction) == emoji.backward_arrow or str(reaction) == emoji.forward_arrow or str(reaction) == '???' or str(reaction) == '???')

    while 1:
        if manPage < lenChapter[chapterInt]:
            chapterInt -= 1
        elif chapterInt != len(lenChapter)-1:
            if manPage >= lenChapter[chapterInt+1]:
                chapterInt += 1

        ballerine = discord.Embed(title="__"+tablPage[manPage][0]+" :__", color=light_blue,
                                  description=tablPage[manPage][1]).set_footer(text=f"Page {manPage} / {len(tablPage)-1}")

        if len(tablPage[manPage]) == 3:
            ballerine.set_image(url=tablPage[manPage][2])

        await msg.edit(embed=ballerine)
        if ini:
            await msg.add_reaction('???')
            await msg.add_reaction(emoji.backward_arrow)
            await msg.add_reaction(emoji.forward_arrow)
            await msg.add_reaction('???')
            ini = False

        reaction = None
        try:
            reaction = await bot.wait_for("reaction_add", timeout=380, check=checkReaction)
        except:
            await msg.clear_reactions()
            break

        if reaction != None:
            if str(reaction[0]) == emoji.backward_arrow:
                if manPage == 0:
                    manPage = len(tablPage)-1
                else:
                    manPage -= 1

            elif str(reaction[0]) == emoji.forward_arrow:
                if manPage == len(tablPage)-1:
                    manPage = 0
                else:
                    manPage += 1

            elif str(reaction[0]) == '???':
                if chapterInt == 0:
                    manPage = lenChapter[len(lenChapter)-1]
                else:
                    manPage = lenChapter[chapterInt]

            elif str(reaction[0]) == '???':
                if chapterInt == len(lenChapter)-1:
                    manPage = 0
                else:
                    manPage = lenChapter[chapterInt+1]

            await msg.remove_reaction(str(reaction[0]), reaction[1])

# -------------------------------------------- SEE LOGS --------------------------------------------
@slash.subcommand(base="see", name="FightLogs", description="Permet de consulter les logs des combats du jour", guild_ids=[615257372218097691])
async def seeLogs(ctx):
    listLogs = os.listdir("./data/fightLogs/")
    listLogs.sort(key=lambda name: name[-8:])

    page = 0
    maxPage = len(listLogs) // 24
    msg = None
    while 1:
        desc = "__Page **{0}** / {1} :__\n".format(page+1, maxPage+1)
        option = []
        maxi = min(len(listLogs), (page+1)*24)
        for log in listLogs[page*24:maxi]:
            desc += "> - {0}\n".format(log)
            option.append(create_select_option(log, log))

        embed = discord.Embed(
            title="__Logs des combats du jour__", color=light_blue, description=desc)

        if len(option) > 0:
            select = create_select(option)
        else:
            select = create_select([create_select_option(
                "disabled", "0")], placeholder="Il n'y a aucun logs ?? afficher", disabled=True)

        if page != 0:
            previousBoutton = create_button(ButtonStyle(
                2), "Page pr??c??dente", emoji.backward_arrow, "back")
        else:
            previousBoutton = create_button(ButtonStyle(
                2), "Page pr??c??dente", emoji.backward_arrow, "back", disabled=True)
        if page != maxPage:
            nextBoutton = create_button(ButtonStyle(
                2), "Page suivante", emoji.forward_arrow, "forward")
        else:
            nextBoutton = create_button(ButtonStyle(
                2), "Page suivante", emoji.forward_arrow, "forward", disabled=True)

        buttons = create_actionrow(previousBoutton, nextBoutton)

        if msg == None:
            try:
                msg = await ctx.send(embed=embed, components=[create_actionrow(select), buttons])
            except:
                msg = await ctx.channel.send(embed=embed, components=[create_actionrow(select), buttons])
        else:
            await msg.edit(embed=embed, components=[create_actionrow(select), buttons])

        try:
            respond = await wait_for_component(bot, msg, timeout=180)
        except:
            break

        try:
            resp = respond.values[0]
        except:
            resp = respond.custom_id
        if resp not in ["back", "forward"]:
            opened = open("./data/fightLogs/{0}".format(resp), "rb")
            try:
                await respond.send("Voici les logs du combat :", file=discord.File(fp=opened))
            except:
                await ctx.channel.send("Voici les logs du combat :", file=discord.File(fp=opened))
            opened.close()
        elif resp == "back":
            page -= 1
        elif resp == "forward":
            page += 1

# -------------------------------------------- SEE STUFF --------------------------------------------
@slash.subcommand(base="see", name="StuffRepartition", description="Permet de consulter la r??portation des logs", guild_ids=[615257372218097691])
async def seeStuffRepartition(ctx):
    rep = "=============================================="
    temp = copy.deepcopy(stuffs)
    temp.sort(key=lambda ballerine: ballerine.minLvl)
    allreadySeenLvl = []
    for a in temp:
        if a.minLvl not in allreadySeenLvl:
            allreadySeenLvl.append(a.minLvl)
            rep += "\n__Stuff de niveau {0} :__\n\n".format(a.minLvl)
        rep += "{0} {1}\n".format(a.emoji, a.name)

    temp = ""
    temp2 = ""
    for a in rep:
        if a == "\n":
            if len(temp2+temp) > 2000:
                await ctx.channel.send(temp2)
                temp2 = ""
                temp = ""
            else:
                temp2 += temp+a
                temp = ""
        else:
            temp += a
    await ctx.channel.send(temp2)

# -------------------------------------------- CHOOSE --------------------------------------------
@slash.slash(name="Choose", description="Renvoie une ??l??ment al??atoire de la liste donn??e", options=[
    create_option("choix1", description="Le premier ??l??ment de la liste",
                  option_type=discord_slash.SlashCommandOptionType.STRING, required=True),
    create_option("choix2", description="Le second ??l??ment de la liste",
                  option_type=discord_slash.SlashCommandOptionType.STRING, required=True),
    create_option("choix3", description="Un potentiel troisi??me de la liste",
                  option_type=discord_slash.SlashCommandOptionType.STRING, required=False),
    create_option("choix4", description="Un potentiel quatri??me de la liste",
                  option_type=discord_slash.SlashCommandOptionType.STRING, required=False),
    create_option("choix5", description="Un potentiel cinqui??me de la liste",
                  option_type=discord_slash.SlashCommandOptionType.STRING, required=False)
])
async def chooseCmd(ctx, choix1, choix2, choix3=None, choix4=None, choix5=None):
    if not(await botChannelVerif(bot, ctx)):
        return 0
    tempTabl = [choix1, choix2]
    for a in [choix3, choix4, choix5]:
        if a != None:
            tempTabl.append(a)

    selected = tempTabl[random.randint(0, len(tempTabl)-1)]
    while selected.endswith(" "):
        selected = selected[:-1]
    while selected.startswith(" "):
        selected = selected[1:]
    await ctx.send(embed=discord.Embed(title="/choose", color=light_blue, description="{0} :\n__{1}__".format(randChooseMsg[random.randint(0, len(randChooseMsg)-1)], selected)))

# -------------------------------------------- ADMIN --------------------------------------------
if isLenapy:
    adminServ = [912137828614426704]
else:
    adminServ = [927195778013859902]


@slash.subcommand(base="admin", name="enable_Fight", guild_ids=adminServ, description="Permet d'activer les combats ou non", options=[
    create_option("valeur", "Activer ou d??saciver les combats",
                  SlashCommandOptionType.BOOLEAN, False)
])
async def addEnableFight(ctx, valeur=None):
    globalVar.changeFightEnabled(valeur)
    if valeur == None:
        valeur = globalVar.fightEnabled()

    if not(valeur):
        await bot.change_presence(status=discord.Status.dnd, activity=discord.Game(name="Les combats sont actuellements d??sactiv??s"))
    else:
        ballerine = datetime.now() + horaire + timedelta(hours=1)
        while ballerine.hour % 3 != 0:
            ballerine = ballerine + timedelta(hours=1)

        await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="Prochain shop ?? "+ballerine.strftime('%Hh')))

    await ctx.send(embed=discord.Embed(title="__Admin Enable Fight__", description="Les combats sont d??sormais __{0}__".format(["d??sactiv??s", "activ??s"][int(valeur)]), color=[red, light_blue][int(valeur)]))


@slash.subcommand(base="admin", name="restart_Bot", guild_ids=adminServ, description="Permet de red??marrer le bot lorsque tous les combats seront fini")
async def restartCommand(ctx):
    await restart_program(bot, ctx)

@slash.subcommand(base="admin", subcommand_group="emoji", name="reset_all", guild_ids=adminServ, description="Lance une r??nitialisation des emojis")
async def resetCustomEmoji(ctx):
    msg = await ctx.send(embed=discord.Embed(title="R??nitialisation des emojis..."))
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game(name="r??nitialiser les emojis..."))

    async def refresh(text: str):
        await msg.edit(embed=discord.Embed(title="R??nitialisation des emojis...", description=text))

    await refresh("Suppression des dossiers images...")
    path = "./data/images"
    for a in os.listdir(path):
        for b in os.listdir(path+"/"+a):
            os.remove(path+"/"+a+"/"+b)
            print(f"{path}/{a}/{b} supprim??")
        os.rmdir(path+"/"+a)
        print(f"{path}/{a} supprim??")

    os.rmdir("./data/images")
    print(f"{path} supprim??")
    await refresh("Suppression de la base de donn??es")
    try:
        customIconDB.dropCustomDB()
    except:
        pass
    await refresh("Supression des emojis")
    iconGuildList = []
    if os.path.exists("../Kawi/"):
        iconGuildList = ShushyCustomIcons
    else:
        iconGuildList = LenaCustomIcons

    allEmojisNum = 0
    for a in iconGuildList:
        emojiGuild = await bot.fetch_guild(a)
        allEmojisNum += len(emojiGuild.emojis)

    cmpt = 0
    now = datetime.now().second
    lastTime = copy.deepcopy(now)
    for a in iconGuildList:
        emojiGuild = await bot.fetch_guild(a)

        for b in emojiGuild.emojis:
            try:
                print("Emoji {0} supprim??".format(b.name))
            except:
                pass
            await b.delete()
            cmpt += 1

            if now >= lastTime + 3 or (now <= 3 and now >= lastTime + 3 - 60):
                await refresh("Supression des emojis ({0} %)".format(int(cmpt/allEmojisNum*100)))
                lastTime = now

    await refresh("Cr??ation des dossiers...")
    existDir(absPath + "/data/images/")
    existDir(absPath + "/data/images/headgears/")
    existDir(absPath + "/data/images/weapons/")
    existDir(absPath + "/data/images/char_icons/")
    existDir(absPath + "/data/images/elemIcon/")
    await refresh("Cr??ation de la base de donn??e")
    base = open("./data/database/custom_icon.db", "w")
    base.close()
    customIconDB.remarkeCustomDB()
    await downloadAllHeadGearPng(bot, msg, lastTime)
    await downloadAllWeapPng(bot, msg, lastTime)
    await refresh("T??l??chargements des icones de bases...")
    await downloadAllIconPng(bot)
    await downloadElementIcon(bot)

    allChar = os.listdir("./userProfile/")
    lenAllChar = len(allChar)
    cmpt = 0

    await refresh("Cr??ation des ??mojis...")
    for num in allChar:
        user = loadCharFile("./userProfile/"+num)
        await getUserIcon(bot, user)
        cmpt += 1

        if now >= lastTime + 3 or (now <= 3 and now >= lastTime + 3 - 60):
            await refresh("Cr??ation des ??mojis ({0} %)".format(int(cmpt/lenAllChar*100)))
            lastTime = now

    await refresh("Fini !")
    await ctx.channel.send("La r??nitialisation des emojis est termin??es !", delete_after=10)

    ballerine = datetime.now() + horaire + timedelta(hours=1)
    while ballerine.hour % 3 != 0:
        ballerine = ballerine + timedelta(hours=1)

    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="Prochain shop ?? "+ballerine.strftime('%Hh')))

@slash.subcommand(base="admin", subcommand_group="emoji", name="remake_all", guild_ids=adminServ, description="Supprime puis refait tous les emojis de personnage")
async def remakeCustomEmoji(ctx):
    await remakeEmojis(ctx)

@slash.subcommand(base="admin", subcommand_group="backup", name="new", description="Permet de r??aliser un backup des profiles de personnages", guild_ids=adminServ)
async def adminBackup(ctx):
    temp = create_backup()
    try:
        await ctx.send(embed=discord.Embed(title="__Admin : Backups__", color=light_blue, description=temp))
    except:
        await ctx.channel.send(embed=discord.Embed(title="__Admin : Backups__", color=light_blue, description=temp))

@slash.subcommand(base="admin", subcommand_group="stat", name="silentRestatAll", description="silentRestat all users", guild_ids=adminServ)
async def silentRestatForEveryone(ctx):
    msg = await ctx.send(embed=discord.Embed(title="__/admin stat silentRestallAll__", color=light_blue, description="Restats en cours..."))
    try:
        for fileName in os.listdir("./userProfile/"):
            user = loadCharFile("./userProfile/"+fileName)
            user = silentRestats(user)
            saveCharFile(user=user)
        await msg.edit(embed=discord.Embed(title="__/admin stat silentRestallAll__", color=light_blue, description="Tous les utilisateurs ont ??t?? restats ????"))
    except:
        await msg.edit(embed=discord.Embed(title="__/admin stat silentRestallAll__", description="Une erreur est survenue :\n"+format_exc()))

@slash.subcommand(base="admin", subcommand_group="shop", name="forceNewShop", description="silentRestat all users", guild_ids=adminServ)
async def forceShop(ctx):
    try:
        await shopping.newShop()
        await ctx.send("Succ??s")
    except:
        await ctx.send("Echec")

@slash.subcommand(base="admin", subcommand_group="stat", name="reset_records", guild_ids=adminServ)
async def resetRecord(ctx):
    await ctx.send(embed=discord.Embed(title="__Reset des records__", color=light_blue, description=aliceStatsDb.resetRecords()))

# -------------------------------------------- KIKIMETER --------------------------------------------
if isLenapy:
    tabl = [912137828614426704, 405331357112205326]
else:
    tabl = adminServ

@slash.slash(name="Kikimeter", description="Permet de voir le top 5 de chaques cat??gories", guild_ids=tabl, options=[create_option(name="what", description="Que regarder", option_type=str, required=True, choices=[create_choice("total", "total"), create_choice("max", "max")])])
async def kikimeterCmd(ctx, what):
    listAllChars = []
    for text in os.listdir("./userProfile/"):
        listAllChars.append(loadCharFile("./userProfile/" + text))

    for cmpt in range(len(listAllChars)):
        temp = aliceStatsDb.getUserStats(listAllChars[cmpt], "all")
        listAllChars[cmpt] = {"char": listAllChars[cmpt], "{what}Damage".format(what=what): temp["{what}Damage".format(what=what)], "{what}Kill".format(what=what): temp["{what}Kill".format(what=what)], "{what}Resu".format(what=what): temp["{what}Resu".format(what=what)], "{what}RecivedDamage".format(
            what=what): temp["{what}RecivedDamage".format(what=what)], "{what}Heal".format(what=what): temp["{what}Heal".format(what=what)], "{what}Armor".format(what=what): temp["{what}Armor".format(what=what)], "{what}Supp".format(what=what): temp["{what}Supp".format(what=what)]}

    embed = discord.Embed(
        title="__Kikimeter__", description="=========================================================")
    for cat in ["{what}Damage".format(what=what), "{what}Kill".format(what=what), "{what}Resu".format(what=what), "{what}RecivedDamage".format(what=what), "{what}Heal".format(what=what), "{what}Armor".format(what=what), "{what}Supp".format(what=what)]:
        listAllChars.sort(
            key=lambda character: character["{0}".format(cat)], reverse=True)
        desc = ""

        for cmpt in range(min(5, len(listAllChars)-1)):
            if listAllChars[cmpt]["{0}".format(cat)] > 0:
                desc += "{0} - {1} {2} ({3})\n".format(cmpt+1, await getUserIcon(bot, listAllChars[cmpt]["char"]), listAllChars[cmpt]["char"].name, separeUnit(int(listAllChars[cmpt]["{0}".format(cat)])))

        if desc != "":
            embed.add_field(
                name="<:empty:866459463568850954>\n__{0}__".format(cat), value=desc)
    try:
        await ctx.send(embed=embed)
    except:
        await ctx.channel.send(embed=embed)

# -------------------------------------------- PROCURATION --------------------------------------------
@slash.slash(name="procuration", description="Permet de donner ?? un autre utilisateur procuration sur votre inventaire", options=[create_option("utilisateur", "L'utilisateur qui pourra modifier vos objets ??quip??s", 6, True)])
async def procurCmd(ctx, utilisateur):
    if not(await botChannelVerif(bot, ctx)):
        return 0
    await procuration(ctx, utilisateur)

# -------------------------------------------- ICON --------------------------------------------
@slash.slash(name="icon", description="Renvoie l'icone de votre personnage", options=[create_option("utilisateur", "Voir l'icone d'un autre utilisateur", 6, False)])
async def iconCommand(ctx, utilisateur=None):
    if not(await botChannelVerif(bot, ctx)):
        return 0
    try:
        if utilisateur == None:
            user = loadCharFile("./userProfile/{0}.prof".format(ctx.author_id))
        else:
            user = loadCharFile(
                "./userProfile/{0}.prof".format(utilisateur.id))
    except:
        if utilisateur == None:
            await ctx.send("Vous devez avoir commenc?? l'Aventure pour utiliser cette commande\nFaites donc un tour du c??t?? de /start !", delete_after=15)
        else:
            await ctx.send("La personne mentionn??e n'a pas commenc?? l'aventure", delete_after=15)
        return 0

    embed = discord.Embed(title="__Icone de personnage__", color=user.color)
    embed.set_image(url="https://cdn.discordapp.com/emojis/{0}.png".format(getEmojiObject(await getUserIcon(bot, user))["id"]))

    await ctx.send(embed=embed)

# -------------------------------------------- ADVENTURE ---------------------------------------------
@slash.subcommand(base="adventure", subcommand_group="duty", name="select", description="Permet de commencer une nouvelle mission", base_description="Commandes de l'Aventure", guild_ids=[615257372218097691])
async def dutyStart(ctx):
    still = True
    try:
        user = loadCharFile("./userProfile/{0}.prof".format(ctx.author.id))
    except:
        still = False
        await ctx.send(embed=discord.Embed(title="__Commande de l'Aventure :__", description="Vous devez avoir commenc?? l'aventure pour utiliser cette commande.\n\nFaites donc un tour vers /start"), delete_after=15)

    if still:
        actName, dutyName, msg = await adventureDutySelect(bot, ctx, user)
        await msg.edit(embed=discord.Embed(title="__Mission s??lectionn??e__", color=light_blue, description="Vous avez s??lection?? la mission \"{0} - {1}\"".format(actName, dutyName[0].upper()+dutyName[1:].lower())), components=[])

# -------------------------------------------- ROULETTE --------------------------------------------
@slash.slash(name="roulette", description="Permet d'utiliser un Jeton de roulette pour obtenir un objet ou des pi??ces")
async def rouletteSlash(ctx):
    if not(await botChannelVerif(bot, ctx)):
        return 0
    try:
        user = loadCharFile("./userProfile/{0}.prof".format(ctx.author_id))
    except:
        await ctx.send(embed=discord.Embed(title="__Commande de l'Aventure :__", description="Vous devez avoir commenc?? l'aventure pour utiliser cette commande.\n\nFaites donc un tour vers /start"), delete_after=15)
        return 0

    await roulette(bot, ctx, user)

# -------------------------------------------- SEE ENEMY REPARTITION -------------------------------
@slash.subcommand(base="see", name="enemyRepartition", guild_ids=[615257372218097691], description="Permet de voir la r??partition des ennemis")
async def seeEnnemyRep(ctx):
    # 0 : Dmg; 1 : Heal/Armor; 2 : Buff/Debuff
    octoRolesNPos = [[[], [], []], [[], [], []], [[], [], []]]
    dicidants = []

    for octa in tablUniqueEnnemies:
        if octa.aspiration in [BERSERK, POIDS_PLUME, MAGE, ENCHANTEUR, OBSERVATEUR, TETE_BRULE]:
            roleId = 0
        elif octa.aspiration in [ALTRUISTE, PREVOYANT]:
            roleId = 1
        elif octa.aspiration in [IDOLE, PROTECTEUR]:
            roleId = 2
        else:
            dicidants.append(octa)
            roleId = -1

        if roleId != -1:
            octoRolesNPos[roleId][octa.weapon.range].append(octa)

    for cmpt in (0, 1, 2):
        embed = discord.Embed(title="__Ennemi r??partion : {0}__".format(
            ["DPT_PHYS", "Healer/Shilder", "Support"][cmpt]), color=light_blue)
        for cmptBis in range(len(octoRolesNPos[cmpt])):
            desc = ""
            for name in octoRolesNPos[cmpt][cmptBis]:
                desc += "{0} {1}\n".format(name.icon, name.name)
            if len(desc) > 0:
                embed.add_field(name=["__M??l??e :__", "__Distance :__",
                                "__Backline :__"][cmptBis], value=desc, inline=True)
            else:
                embed.add_field(name=["__M??l??e :__", "__Distance :__",
                                "__Backline :__"][cmptBis], value="`-`", inline=True)

        if cmpt == 0:
            await ctx.send(embed=embed)
        else:
            await ctx.channel.send(embed=embed)

    desc = ''
    for name in dicidants:
        desc += "{0} {1}\n".format(name.icon, name.name)
    embed = discord.Embed(title="__Hors cat??gorie :__".format(
        ["DPT_PHYS", "Healer/Shilder", "Support"][cmpt]), color=light_blue, description=desc)

    await ctx.channel.send(embed=embed)

# ------------------------------------------- PRESTIGE ---------------------------------------------
@slash.slash(name="prestige", description="Permet de revenir au niveau 1, avec quelques bonus en primes")
async def prestigeCmd(ctx):
    if not(await botChannelVerif(bot, ctx)):
        return 0
    try:
        user = loadCharFile("./userProfile/{0}.prof".format(ctx.author.id))
    except:
        await ctx.send("Vous n'avez m??me pas encore commenc?? l'aventure et vous voulez d??j?? prestige ?", delete_after=15)
        return 0

    if user.level < 55:
        await ctx.send("Vous devez ??tre niveau 55 pour pouvoir utiliser cette commande", delete_after=15)
        return 0

    embed = discord.Embed(title="__Prestige__", color=light_blue,description="En prestigeant votre personnage, vous retournerez au niveau 1<:littleStar:925860806602682369>{0}.\n\nVous conserverez votre inventaire d'objet des de comp??tences et obtiendrez un __Point Majeur__.\nVous pourrez l'utiliser pour augmenter une de vos statistiques principales de 30 points suppl??mentaires, ou augmenter vos statistiques secondaires de 10 points".format(user.stars+1))
    comfirm = create_button(ButtonStyle.green, "Prestige votre personnage", '???', '???')

    msg = await ctx.send(embed=embed, components=[create_actionrow(comfirm)])

    def check(m):
        return int(m.author_id) == int(ctx.author.id)

    try:
        await wait_for_component(bot, msg, check=check, timeout=30)
    except:
        await msg.edit(embed=embed, components=[])
        return 0

    user = loadCharFile(user=user)
    user.level, user.exp, user.stars = 1, 0, user.stars+1
    user = restats(user)

    saveCharFile(user=user)
    await makeCustomIcon(bot, user)
    await inventoryVerif(bot, user)
    await msg.edit(embed=discord.Embed(title="__Prestige__", color=light_blue, description="Vous avez bien prestige votre personnage"), components=[])

# ------------------------------------------- SET_BOT_CHANNEL --------------------------------------
@slash.slash(name="set_bot_channel", description="Permet de d??finir un salon comme salon bot", options=[create_option("salon", "Le salon dans lequel les utilisateurs pourront utiliser les commandes", 7, True)])
async def setChannel(ctx: discord_slash.SlashContext, salon: discord.TextChannel):
    if not(ctx.author.guild_permissions.manage_channels):
        await ctx.send(embed=discord.Embed(title="__/set_bot_channel__", color=red, description="Tu as besoin des permissions de g??rer les salons textuels pour utiliser cette commande, d??sol??e"), delete_after=10)
        return 0
    if type(salon) != discord.TextChannel:
        await ctx.send(embed=discord.Embed(title="__/set_bot_channel__", color=red, description="Seul un salon textuel peut ??tre rajout?? comme salon bot, d??sol??e"), delete_after=10)
        return 0

    globalVar.setGuildBotChannel(ctx.guild_id, salon.id)
    await ctx.send(embed=discord.Embed(title="__/set_bot_channel__", color=light_blue, description="Le salon {0} a bien ??t?? enregistr?? comme salon bot\nChaque serveur ne peut avoir qu'un seul salon bot, r??utiliser la commande remplacera l'ancien".format(salon.mention)))

# ------------------------------------------- VERIF ------------------------------------------------
@slash.slash(name="verif_user", description="Permet de voir toutes les informations d'un personnage", guild_ids=adminServ, options=[create_option("identifiant", "L'identifiant de l'utilisateur", SlashCommandOptionType.STRING, True)])
async def verifuser(ctx, identifiant):
    user = loadCharFile("./userProfile/{0}.prof".format(identifiant))
    await ctx.send(embed=await seeAllInfo(bot, user))

@slash.slash(name="verif_team", guild_ids=adminServ)
async def verifTeams(ctx):
    toSend, allReadySeen, msg, userTeam = "", [], None, []

    def getUserMainTeam(user: char):
        for look in userTeam:
            if look[0] == user.owner:
                return int(look[1])

    for team in userTeamDb.getAllTeamIds():
        temp = "__Team **{0}** :__".format(team)
        teamMembers = userTeamDb.getTeamMember(team)

        tmpTeamMembers = teamMembers[:]
        for ids in teamMembers:
            user = loadCharFile(path="./userProfile/{0}.prof".format(ids))
            if user.owner in allReadySeen:
                warn = "~~"
                if getUserMainTeam(user) != team:
                    tmpTeamMembers.remove(str(user.owner))
            else:
                warn = ""
                allReadySeen.append(user.owner)
                userTeam.append([user.owner, team])

            if user.team != team:
                user.team = team
                saveCharFile(user=user)
                redacted = " ????"
            else:
                redacted = ""

            temp += "\n{2}{0} {1}{2}{3}".format(await getUserIcon(bot, user), user.name, warn, redacted)

        if len(tmpTeamMembers) > 0:
            userTeamDb.updateTeam(team, tmpTeamMembers)

        temp += "\n"
        if len(toSend+temp) > 4000:
            if msg == None:
                try:
                    msg = await ctx.send(embed=discord.Embed(title="__Team V??rification__", color=light_blue, description=toSend))
                except:
                    msg = await ctx.channel.send(embed=discord.Embed(title="__Team V??rification__", color=light_blue, description=toSend))
            else:
                await ctx.channel.send(embed=discord.Embed(title="__Team V??rification__", color=light_blue, description=toSend))
            toSend = temp
            temp = ""
        else:
            toSend = toSend + temp + "\n"

    if toSend != "":
        if msg == None:
            try:
                msg = await ctx.send(embed=discord.Embed(title="__Team V??rification__", color=light_blue, description=toSend))
            except:
                msg = await ctx.channel.send(embed=discord.Embed(title="__Team V??rification__", color=light_blue, description=toSend))
        else:
            await ctx.channel.send(embed=discord.Embed(title="__Team V??rification__", color=light_blue, description=toSend))

@slash.slash(name="verif_emoji", guild_ids=adminServ)
async def emojiVerficition(ctx):
    msg, remaked, lastProgress = await ctx.send(embed=discord.Embed(title="V??rification des ??mojis...", description="__Progression :__ 0%")), "", 0
    listAllUsersFiles = os.listdir("./userProfile/")
    lenAllUser, progress = len(listAllUsersFiles), 0
    try:
        for path in listAllUsersFiles:
            user, haveSucced = loadCharFile("./userProfile/"+path), False
            userIcon = await getUserIcon(bot, user)
            haveSucced = False
            for guildId in [ShushyCustomIcons, LenaCustomIcons][isLenapy]:
                guild = await bot.fetch_guild(guildId)
                try:
                    await guild.fetch_emoji(getEmojiObject(userIcon)["id"])
                    haveSucced = True
                    break
                except:
                    pass
            if not(haveSucced):
                customIconDB.removeUserIcon(user)
                await makeCustomIcon(bot, user)
                if await getUserIcon(bot, user) not in ['<:LenaWhat:760884455727955978>', '<a:lostSilver:917783593441456198>']:
                    remaked += "Emoji de {0} refait\n".format(user.name)
                else:
                    remaked += "Erreur lors du remake de l'emoji de {0}\n".format(
                        user.name)
            progress += 1

            if progress/lenAllUser * 100 > lastProgress + 5:
                await msg.edit(embed=discord.Embed(title="V??rification des ??mojis...", description="__Progression :__ {0}%\n".format(round(progress/lenAllUser * 100, 2))+remaked))
                lastProgress = progress/lenAllUser * 100

        await msg.edit(embed=discord.Embed(title="V??rification des ??mojis", description="__Progression :__ Termin??\n"+remaked, color=light_blue))
    except:
        await msg.edit(embed=discord.Embed(title="V??rification des ??mojis", description="__Interrompue__\n"+format_exc(), color=red))

@slash.slash(name="char_settings", description="Permet de modifier les param??tres de son icone de personnage")
async def char_settings(ctx):
    user = loadCharFile("./userProfile/{0}.prof".format(ctx.author_id))
    await userSettings(bot, user, ctx)

@slash.slash(name="Test", guild_ids=adminServ)
async def expeditionTest(ctx):
    user, chan = loadCharFile(
        "./userProfile/{0}.prof".format(ctx.author.id)), ctx.channel
    listEmbed = await generateExpeditionReport(bot, [user], user, datetime.now(), ctx)
    for a in listEmbed:
        await chan.send(embed=a)

@slash.slash(name="area_test",guild_ids=adminServ)
async def areaTest(ctx):
    first = True
    for area in [AREA_CONE_3,AREA_LINE_3,AREA_ARC_1]:
        emb = discord.Embed(title=areaNames[area],color=light_blue)
        for cmpt in (0,1,2,3):
            emb.add_field(name=["__From Left__","__From Right__","__From Up__","__From Down__"][cmpt],value=visuArea(area,ENEMIES,False,cmpt),inline=False)
        if first:
            await ctx.send(embed=emb)
            first = False
        else:
            await ctx.channel.send(embed=emb)
            
###########################################################
# D??marrage du bot
if not(isLenapy):
    print("\nKawiiiiii")
    try:
        bot.run(shushipy)
    except:
        print("La connexion a ??couch??")
else:
    print("\nIl semblerait que je sois seule cette fois. Je m'occuperais de Shushi une autre fois")
    bot.run(lenapy)
