from re import findall
import discord, os
from discord_slash.utils.manage_components import *
from adv import *
from classes import *
from donnes import *
from gestion import *
from advance_gestion import *
from commands_files.command_fight import teamWinDB

buttonReturn = create_button(2,"Retour",emoji='◀️',custom_id="-1")
buttonBuy = create_button(1,"Acheter",getEmojiObject('<:coins:862425847523704832>'),custom_id="0")
onlyReturn = create_actionrow(buttonReturn)

allBuyButton = create_button(ButtonStyle.primary,"Devenir pauvre",getEmojiObject('<:bought:906623435256504451>'),"buy all")
allGiveButton = create_button(ButtonStyle.secondary,"Devenir pauvre (Deluxe)",getEmojiObject('<:teamBought:906621631143743538>'),"buy'n'send all")

allBuyButtonButPoor = create_button(ButtonStyle.gray,"Vous êtes pauvre",getEmojiObject('<:bought:906623435256504451>'),"buy all",disabled=True)
allGiveButtonButPoor = create_button(ButtonStyle.gray,"Vous êtes pauvre, mais deluxe",getEmojiObject('<:teamBought:906621631143743538>'),"buy'n'send all",disabled=True)
allBuyButtonButAllreadyHaveM = create_button(ButtonStyle.gray,"Vous êtes un acheteur compulsif",getEmojiObject('<:bought:906623435256504451>'),"buy all",disabled=True)
allGiveButtonButAllreadyHaveM = create_button(ButtonStyle.gray,"Vous êtes un acheteur compulsif deluxe",getEmojiObject('<:teamBought:906621631143743538>'),"buy'n'send all",disabled=True)
allBuyButtonButAllreadyHaveF = create_button(ButtonStyle.gray,"Vous êtes une acheteuse compulsive",getEmojiObject('<:bought:906623435256504451>'),"buy all",disabled=True)
allGiveButtonButAllreadyHaveF = create_button(ButtonStyle.gray,"Vous êtes une acheteuse compulsive deluxe",getEmojiObject('<:teamBought:906621631143743538>'),"buy'n'send all",disabled=True)

haveIcon = "<:bought:906623435256504451>" 
allTeamHaveIcon = "<:teamBought:906621631143743538>"

async def shop2(bot : discord.Client, ctx : discord.message,shopping : list):
    pathUserProfile = absPath + "/userProfile/" + str(ctx.author.id) + ".prof"
    if os.path.exists(pathUserProfile): # Does the user have a character
        user = loadCharFile(pathUserProfile)
        try:
            msg = await loadingEmbed(ctx)
        except:
            msg = await loadingSlashEmbed(ctx)

        shopTotalRandom = copy.deepcopy(shopRandomMsg)

        dateNow = datetime.now()
        years = dateNow.year

        if dateNow > datetime.strptime("23/12/{0}".format(years),"%d/%m/%Y") and dateNow < datetime.strptime("4/1/{0}".format(years+1),"%d/%m/%Y"):
            shopTotalRandom += shopEventEndYears 

        if dateNow.month <= 2 or dateNow.month == 12:
            shopTotalRandom += shopSeasonWinter
        elif dateNow.month <= 5:
            shopTotalRandom += shopSeasonSpring
        elif dateNow.month <= 8:
            shopTotalRandom += shopSeasonsSummer
        elif dateNow.mouth <= 11:
            shopTotalRandom += shopSeasonsAutomne

        for shopDict in shopEventOneDay:
            if shopDict["date"] == (dateNow.day,dateNow.month):
                shopTotalRandom = shopDict["tabl"]
                break

        shopRdMsg = shopTotalRandom[random.randint(0,len(shopTotalRandom)-1)].format(
            ctx.author.name,
            user.name,
            lena = tablAllAllies[0].icon,
            alice = tablAllAllies[3].icon,
            shushi = tablAllAllies[4].icon,
            clemence = tablAllAllies[2].icon,
            luna = '<:luna:909047362868105227>',
            feli = '<:felicite:909048027644317706>',
            icelia = '<:icealia:909065559516250112>',
            shihu = '<:shihu:909047672541945927>',
            shehisa = '<:shehisa:919863933320454165>', helene = tablAllAllies[6].icon,
            sixtine = '<:sixtine:908819887059763261>',
            iliana = '<:Iliana:926425844056985640>',
            gweny = tablAllAllies[1].icon, alty = '<:alty:906303048542990347>', klikli ='<:klikli:906303031837073429>', karai = '<:karail:974079383197339699>'
            )
        initMsg = msg

        if user.team != 0:
            teamList = userTeamDb.getTeamMember(user.team)
        else:
            teamList = [user.owner]

        buttonGift = create_button(3,"Offrir",emoji='🎁',custom_id="1",disabled=len(teamList) == 1)
        buttonAllGift = create_button(3,"Offrir à tous",emoji=getEmojiObject('<:teamBought:906621631143743538>'),custom_id="2",disabled=len(teamList) == 1)

        allButtons = create_actionrow(buttonReturn,buttonBuy,buttonGift,buttonAllGift)
        buttonsWithoutBuy = create_actionrow(buttonReturn,buttonGift,buttonAllGift)
        while 1: 
            # Loading the user's team
            if len(teamList) > 1:
                teamMember = []
                for a in teamList:
                    if a != int(ctx.author.id):
                        teamMember += [loadCharFile(absPath + "/userProfile/" + str(a) + ".prof")]

            shopEmb = discord.Embed(title = "shop" +" - Céphalochic",color = user.color, description = "Le magasin est commun à tous les serveurs et est actualisé toutes les 3 heures"+f"\n\nVous disposez actuellement de {user.currencies} {emoji.coins}.\nVous êtes en possession de **{round(userShopPurcent(user),2)}**% du magasin.\n\n*{shopRdMsg}*")

            shopWeap,shopSkill,shopStuff,shopOther = [],[],[],[]
            for a in shopping:
                if type(a)==weapon:
                    shopWeap.append(a)
                elif type(a)==skill:
                    shopSkill.append(a)
                elif type(a)==stuff:
                    shopStuff.append(a)
                else:
                    shopOther.append(a)

            shopped = shopWeap+shopSkill+shopStuff+shopOther
            shopMsg = ["__**Armes :**__","__**Compétences :**__","__**Equipement :**__","**__Autre :__**"]
            options = []
            listNotHave,listNotAllTeamHave,totalCost,totalTeamCost = [],[],0,0

            shopField = ["","","",""]
            for a in [0,1,2,3]:
                for b in [shopWeap,shopSkill,shopStuff,shopOther][a]:
                    if b != None:
                        shopField[a] += f"\n{b.emoji} {b.name} ({b.price} {emoji.coins})"
                        desc = ["Arme","Compétence","Equipement","Autre"][a]
                        desc2 = ""

                        icon = ""
                        if user.have(b):
                            icon = " ("+haveIcon+")"
                            desc2 = " - Possédé"
                        else:
                            listNotHave.append(b)
                            totalCost += b.price
                        
                        if len(teamList) > 1:
                            allTeamHave = True
                            for c in teamMember:
                                if not(c.have(b)):
                                    allTeamHave = False
                                    totalTeamCost += b.price

                            if allTeamHave:
                                icon = " ("+allTeamHaveIcon+")"
                                desc2 = " - Toute votre équipe possède cet objet"
                            else:
                                listNotAllTeamHave.append(b)

                        shopField[a] += icon
                        options += [create_select_option(unhyperlink(b.name),b.id,getEmojiObject(b.emoji),desc+desc2)]
                if len(shopField[a]) <= 1024:
                    shopEmb.add_field(name="<:empty:866459463568850954>\n"+shopMsg[a],value=shopField[a],inline=False)
                else:
                    shopField[a] = ""
                    for b in [shopWeap,shopSkill,shopStuff,shopOther][a]:
                        if b != None:
                            tempName, temp = "",""
                            for letter in unhyperlink(b.name+" "):
                                if letter == " ":
                                    if len(temp) > 4:
                                        tempName += " {0}.".format(temp[:3])
                                    else:
                                        tempName += " {0}".format(temp[:4])
                                    temp = ""
                                else:
                                    temp += letter

                            shopField[a] += f"\n{b.emoji}{tempName} : {b.price} pièces"
                            icon = ""
                            if user.have(b):
                                icon = " (☑️)"

                            if len(teamList) > 1:
                                allTeamHave = True
                                for c in teamMember:
                                    if not(c.have(b)):
                                        allTeamHave = False
                                        break

                                if allTeamHave:
                                    icon = " (✅)"

                            shopField[a] += icon

                    if shopField[a] == "":
                        shopField[a] = "???"

                    shopEmb.add_field(name="<:empty:866459463568850954>\n"+shopMsg[a],value=shopField[a],inline=False)

            fcooldown,fseconds,fqcooldown,fqseconds,faccord,fqaccord,fsaccord,fqsaccord = teamWinDB.getFightCooldown(user.team)//60,teamWinDB.getFightCooldown(user.team)%60,teamWinDB.getFightCooldown(user.team,True)//60,teamWinDB.getFightCooldown(user.team,True)%60,"","","",""
            if fcooldown > 1:
                faccord = "s"
            if fqcooldown > 1:
                fqaccord = "s"
            if fseconds > 1:
                fsaccord = "s"
            if fqseconds > 1:
                fqsaccord = "s"
            if user.team == 0:
                ballerine = user.owner
            else:
                ballerine = user.team

            fightingStatus = teamWinDB.isFightingBool(ballerine)

            if fightingStatus[0]:
                channel = await bot.fetch_channel(fightingStatus[2])
                fightingMessage = await channel.fetch_message(fightingStatus[0])
                
                fightingRespond = "__Votre équipe affronte actuellement :__\n"
                temp = ""
                for letter in fightingStatus[1]:
                    if letter==";" and len(temp) > 0:
                        ennemi = findEnnemi(temp)
                        if ennemi == None:
                            ennemi = findAllie(temp)

                        if ennemi != None:
                            fightingRespond += "{0} {1}\n".format(ennemi.icon,ennemi.name)
                        else:
                            fightingRespond += "<:blocked:897631107602841600> L'ennemi n'a pas pu être trouvé\n"
                        temp = ""
                    else:
                        temp+=letter

                shopEmb.add_field(name="<:em:866459463568850954>\n__/cooldowns__",value=fightingRespond+"\nsur __[{0}]({1})__".format(channel.guild.name,fightingMessage.jump_url))
            else:
                if fcooldown == fseconds == 0 and not(globalVar.fightEnabled()):
                    normalFightMsg = '<:noneWeap:917311409585537075>'
                else:
                    normalFightMsg = f'{fcooldown} minute{faccord} et {fseconds} seconde{fsaccord}'

                if fqcooldown == fqseconds == 0 and not(globalVar.fightEnabled()):
                    quickFightMsg = '<:noneWeap:917311409585537075>'
                else:
                    quickFightMsg = f'{fqcooldown} minute{fqaccord} et {fqseconds} seconde{fqsaccord}'

                shopEmb.add_field(name=f"<:em:866459463568850954>\n__Cooldowns des commandes Fight l'équipe :__",value=f"__Normal__ : {normalFightMsg}\n__Quick__ : {quickFightMsg}",inline=False)


            select = create_select(options=options,placeholder="Choisissez un article pour avoir plus d'informations dessus")

            if totalCost > user.currencies:
                temp1 = allBuyButtonButPoor
            elif totalCost == 0:
                temp1 = [allBuyButtonButAllreadyHaveM,allBuyButtonButAllreadyHaveF,allBuyButtonButAllreadyHaveM][user.gender]
            elif user.currencies >= totalCost:
                temp1 = allBuyButton

            if len(teamList) <= 1:
                temp2 = create_button(ButtonStyle.gray,"Vous n'avez pas d'amis",getEmojiObject('<:teamBought:906621631143743538>'),"buy'n'send all",disabled=True)
            elif totalTeamCost > user.currencies:
                temp2 = allGiveButtonButPoor
            elif totalTeamCost == 0:
                temp2 = [allGiveButtonButAllreadyHaveM,allGiveButtonButAllreadyHaveF,allGiveButtonButAllreadyHaveM][user.gender]
            elif user.currencies >= totalTeamCost:
                temp2 = allGiveButton

            tablAddPoorButtons = [create_actionrow(temp1,temp2)]

            await initMsg.edit(embed = shopEmb,components=[create_actionrow(select)]+tablAddPoorButtons)

            def check(m):
                return int(m.author_id) == int(ctx.author.id)

            try:
                respond = await wait_for_component(bot,messages=initMsg,check=check,timeout=60)
            except:
                timeoutEmbed = discord.Embed(title="__/shop__",color=user.color,description=shopRdMsg)
                shopField = ["","",""]
                for a in [0,1,2]:
                    for b in [shopWeap,shopSkill,shopStuff,shopOther][a]:
                        if b != None:
                            shopField[a] += "\n{0} {1}".format(b.emoji,b.name)

                    timeoutEmbed.add_field(name="<:em:866459463568850954>\n"+shopMsg[a],value=shopField[a],inline=True)

                await initMsg.edit(embed = timeoutEmbed,components=[])
                return 0

            if respond.component_type == 2:
                if respond.custom_id =="buy all":
                    tempMsg = await respond.send(embed=discord.Embed(title="__/shop__ - Devenir pauvre",color=user.color,description="Vos achats sont en cours d'enregistrement..."))
                    user = loadCharFile("./userProfile/{0}.prof".format(user.owner))
                    tempTabl = []
                    for obj in listNotHave:
                        if not(user.have(obj)) and user.currencies >= obj.price:
                            if type(obj) == weapon:
                                user.weaponInventory.append(obj)
                            elif type(obj) == skill:
                                user.skillInventory.append(obj)
                            elif type(obj) == stuff:
                                user.stuffInventory.append(obj)
                            elif type(obj) == other:
                                user.otherInventory.append(obj)
                            user.currencies -= obj.price
                            tempTabl += [[obj.emoji,obj.name]]
                    saveCharFile("./userProfile/{0}.prof".format(user.owner),user)
                    temp = ""
                    for a in tempTabl:
                        temp += "{0} {1}\n".format(a[0],a[1])
                    await tempMsg.edit(embed=discord.Embed(title="__/shop__ - Devenir pauvre",color=user.color,description="__Vous avez acheté les objets suivants pour la somme de **{0}** <:coins:862425847523704832> :__\n{1}".format(separeUnit(totalCost),temp)))

                elif respond.custom_id == "buy'n'send all":
                    tempMsg = await respond.send(embed=discord.Embed(title="__/shop__ - Devenir pauvre (Deluxe)",color=user.color,description="Vos achats sont en cours d'enregistrement..."))
                    user = loadCharFile("./userProfile/{0}.prof".format(user.owner))
                    tempTabl1,tempTabl2,tempTabl3 = [],[],[]
                    for teamUser in teamMember:
                        gifted = loadCharFile("./userProfile/{0}.prof".format(teamUser.owner))
                        tempDeleveryMsg = ""
                        for obj in listNotAllTeamHave:
                            if not(gifted.have(obj)) and user.currencies >= obj.price:
                                if type(obj) == weapon:
                                    gifted.weaponInventory.append(obj)
                                elif type(obj) == skill:
                                    gifted.skillInventory.append(obj)
                                elif type(obj) == stuff:
                                    gifted.stuffInventory.append(obj)
                                elif type(obj) == other:
                                    gifted.otherInventory.append(obj)
                                user.currencies -= obj.price
                                tempDeleveryMsg += "\n{0} {1}".format(obj.emoji,obj.name)

                                if obj.name not in tempTabl1:
                                    tempTabl1.append(obj.name)
                                    tempTabl2.append(1)
                                    tempTabl3.append(obj.emoji)
                                else:
                                    for cmpt in range(len(tempTabl1)):
                                        if tempTabl1[cmpt] == obj.name:
                                            tempTabl2[cmpt] += 1

                        saveCharFile("./userProfile/{0}.prof".format(gifted.owner),gifted)

                        if tempDeleveryMsg != "":
                            giftedUser = await bot.fetch_user(gifted.owner)
                            try:
                                await giftedUser.send(embed=discord.Embed("__Livraison :__",color=user.color,description="__{0}__ vous a offert les objets suivants :\n".format(user.name)+tempDeleveryMsg))
                            except:
                                pass
                    
                    for obj in listNotAllTeamHave:
                        if not(user.have(obj)) and user.currencies >= obj.price:
                            if type(obj) == weapon:
                                user.weaponInventory.append(obj)
                            elif type(obj) == skill:
                                user.skillInventory.append(obj)
                            elif type(obj) == stuff:
                                user.stuffInventory.append(obj)
                            elif type(obj) == other:
                                user.otherInventory.append(obj)
                            user.currencies -= obj.price

                    temp = ""
                    for cmpt in range(len(tempTabl1)):
                        temp += "{0} {1} *x{2}*\n".format(tempTabl3[cmpt],tempTabl1[cmpt],tempTabl2[cmpt])

                    saveCharFile("./userProfile/{0}.prof".format(user.owner),user)
                    await tempMsg.edit(embed=discord.Embed(title="__/shop__ - Devenir pauvre (Deluxe)",color=user.color,description="__Vous avez acheté les objets suivants pour la somme de **{0}** <:coins:862425847523704832> :__\n{1}".format(separeUnit(totalTeamCost),temp)))

            else:
                await initMsg.edit(embed = shopEmb,components=[create_actionrow(getChoisenSelect(select,respond.values[0]))])
                rep = None
                for a in range(0,len(shopped)):
                    if shopped[a].id == respond.values[0]:
                        rep = a
                        break

                try:
                    msg = await respond.send(embed = discord.Embed(title="shop",description="Recherche de l'objet dans les rayons..."))
                except:
                    msg = await initMsg.channel.send(embed = discord.Embed(title="shop",description="Recherche de l'objet dans les rayons..."))

                try:
                    if rep == None:                     # Object not found
                        await msg.edit(embed=discord.Embed(title="Error in shop command",description="Unfound object"))
                    else:
                        typ, obj = whatIsThat(shopped[rep]), shopped[rep]
                        if typ == 0:
                            repEmb = infoWeapon(obj,user,ctx)
                        elif typ == 1:
                            repEmb = infoSkill(shopped[rep],user,ctx)
                        elif typ == 2:
                            repEmb = infoStuff(obj,user,ctx)
                        elif typ == 3:
                            repEmb = infoOther(obj,user)

                        if user.currencies < obj.price:
                            repEmb.set_footer(text = "Vous n'avez pas suffisament de pièces")
                            await msg.edit(embed = repEmb,components=[onlyReturn])
                        else:
                            if user.have(obj):
                                repEmb.set_footer(text = "Vous possédez déjà cet objet")
                                await msg.edit(embed = repEmb,components=[buttonsWithoutBuy])
                            else:
                                repEmb.set_footer(text = "Cliquez sur le bouton \"Acheter\" pour acheter cet objet")
                                await msg.edit(embed = repEmb,components=[allButtons])

                            try:
                                rep = await wait_for_component(bot,messages=msg,check=check,timeout=60)
                            except:
                                await msg.delete()
                                rep = None

                            if rep != None:
                                if rep.custom_id == "0":                # Buy for them self
                                    try:
                                        if typ == 0:
                                            user.weaponInventory.append(obj)
                                        elif typ == 1:
                                            user.skillInventory.append(obj)
                                        elif typ == 2:
                                            user.stuffInventory.append(obj)
                                        elif typ == 3:
                                            user.otherInventory.append(obj)
                                        user.currencies = user.currencies - obj.price
                                        saveCharFile(pathUserProfile,user)
                                        await msg.edit(embed = discord.Embed(title="shop"+ " - " +obj.name,color = user.color,description = f"Votre achat a bien été effectué ! Faites \"/inventory nom:{obj.id}\" pour l'équiper"),components=[],delete_after=5)
                                    except:
                                        await msg.edit(embed = errorEmbed("shop","Une erreur s'est produite"))

                                elif rep.custom_id == "1":              # Gift to annother teamMate
                                    options = []
                                    for a in teamMember:
                                        if not(a.have(obj)) and a.owner != user.owner:
                                            options += [create_select_option(a.name,str(a.owner),getEmojiObject(await getUserIcon(bot,a)))]

                                    if options == [] :
                                        select = create_select([create_select_option("Vous n'avez pas à voir ça","Nani")],placeholder="Toute votre équipe a déjà cet objet",disabled=True)
                                    else:
                                        select = create_select(options,placeholder="À qui voulez vous offrir cet objet ?")
                                    await msg.edit(embed= repEmb, components=[create_actionrow(buttonReturn),create_actionrow(select)])

                                    respond = None
                                    try:
                                        respond = await wait_for_component(bot,messages=msg,timeout = 60)
                                    except:
                                        await msg.delete()
                                    if respond != None:
                                        try:
                                            for teamMate in teamMember:
                                                if teamMate.owner == respond.values[0]:
                                                    try:
                                                        try:
                                                            temp = await respond.send("Envoie du cadeau...")
                                                        except:
                                                            temp = await initMsg.channel.send("Envoie du cadeau...")
                                                        if typ == 0:
                                                            teamMate.weaponInventory.append(obj)
                                                        elif typ == 1:
                                                            teamMate.skillInventory.append(obj)
                                                        elif typ == 2:
                                                            teamMate.stuffInventory.append(obj)
                                                        elif typ == 3:
                                                            teamMate.otherInventory.append(obj)
                                                        user.currencies = user.currencies - obj.price
                                                        saveCharFile(absPath + "/userProfile/" + str(teamMate.owner) + ".prof",teamMate)
                                                        saveCharFile(absPath + "/userProfile/" + str(ctx.author.id) + ".prof",user)
                                                        try:
                                                            dest = await bot.fetch_user(teamMate.owner)
                                                            await dest.send(embed = discord.Embed(title="Livraison",description = "Vous avez reçu l'objet __{0}__ de la part de {1}".format(obj.name,user.name),color = teamMate.color))
                                                        except:
                                                            pass
                                                        await temp.delete()
                                                        await msg.edit(embed = discord.Embed(title="shop",color = user.color,description = f"Votre cadeau a bien été envoyé !"),components = [create_actionrow(getChoisenSelect(select,respond.values[0]))],delete_after=5)
                                                    except:
                                                        await msg.edit(embed = errorEmbed("shop","Une erreur s'est produite"))
                                                    break
                                        except:
                                            await msg.delete()

                                elif rep.custom_id == "2":
                                    tablTeamToGift, msgTeamToGift = [],"Voulez vous offrir __{0}__ aux coéquipiers suivants ?\n".format(obj.name)

                                    for a in teamMember:
                                        if obj not in a.otherInventory:
                                            tablTeamToGift.append(a)
                                            msgTeamToGift += "{0} {1}\n".format(await getUserIcon(bot,a), a.name)

                                    msgTeamToGift += "\nPrix total : {0} <:coins:862425847523704832>".format(obj.price * len(tablTeamToGift))

                                    if user.currencies >= obj.price * len(tablTeamToGift):
                                        buttonConfirm = create_button(1,"Rendez moi pauvre !",getEmojiObject('<:coins:862425847523704832>'),"buy")
                                    else:
                                        buttonConfirm = create_button(1,"Rendez moi pauvre !",getEmojiObject('<:coins:862425847523704832>'),"buy",disabled=True)

                                    await msg.edit(embed = discord.Embed(title="__/shop {0}__".format(obj.name),color=user.color,description=msgTeamToGift),components=[create_actionrow(buttonReturn,buttonConfirm)])

                                    try:
                                        respond = await wait_for_component(bot,messages=msg,timeout = 60,check=check)
                                    except:
                                        break

                                    if respond.custom_id == "buy":
                                        await msg.edit(embed = discord.Embed(title="__/shop {0}__".format(obj.name),color = user.color,description = f"Envoie de vos cadeaux... <a:loading:862459118912667678>"),components = [])
                                        for a in tablTeamToGift:
                                            if int(a.owner) != int(user.owner):
                                                if typ == 0:
                                                    a.weaponInventory.append(obj)
                                                elif typ == 1:
                                                    a.skillInventory.append(obj)
                                                elif typ == 2:
                                                    a.stuffInventory.append(obj)
                                                elif typ == 3:
                                                    a.otherInventory.append(obj)
                                                user.currencies = user.currencies - obj.price
                                                saveCharFile(absPath + "/userProfile/" + str(a.owner) + ".prof",a)
                                                saveCharFile(absPath + "/userProfile/" + str(ctx.author.id) + ".prof",user)
                                                try:
                                                    dest = await bot.fetch_user(a.owner)
                                                    await dest.send(embed = discord.Embed(title="Livraison",description = "Vous avez reçu l'objet __{0}__ de la part de {1}".format(unhyperlink(obj.name),user.name),color = a.color))
                                                except:
                                                    pass
                                            else:
                                                user.otherInventory += [obj]
                                                user.currencies = user.currencies - obj.price
                                                saveCharFile(absPath + "/userProfile/" + str(ctx.author.id) + ".prof",user)
                                        await msg.edit(embed = discord.Embed(title="shop",color = user.color,description = f"Vos cadeaux ont bien été envoyés !"),components = [],delete_after=5)
                                    else:
                                        await msg.delete()

                                elif rep.custom_id == "-1":
                                    await msg.delete()
                except:
                    await msg.edit(embed=discord.Embed(title="Uncatch error in shop command",description=format_exc()),components=[])
    else:
        await ctx.send(embed = errorEmbed("shop","Vous n'avez pas commencé l'aventure"),delete_after=15)
