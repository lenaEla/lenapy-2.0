import os
from adv import *
from classes import *
from donnes import *
from gestion import *
from advance_gestion import *
from commands_files.command_fight import teamWinDB

buttonReturn = interactions.Button(style=2, label="Retour",emoji=PartialEmoji(name="◀️"),custom_id="-1")
buttonBuy = interactions.Button(style=1, label="Acheter", emoji=getEmojiObject('<:coins:862425847523704832>'),custom_id="0")
onlyReturn = interactions.ActionRow(buttonReturn)

allBuyButton = interactions.Button(style=ButtonStyle.PRIMARY,label="Devenir pauvre",emoji=getEmojiObject('<:bought:906623435256504451>'),custom_id="buy all")
allGiveButton = interactions.Button(style=ButtonStyle.SECONDARY,label="Devenir pauvre (Deluxe)",emoji=getEmojiObject('<:teamBought:906621631143743538>'),custom_id="buy'n'send all")

allBuyButtonButPoor = interactions.Button(style=ButtonStyle.SECONDARY,label="Vous êtes pauvre",emoji=getEmojiObject('<:bought:906623435256504451>'),custom_id="buy all",disabled=True)
allGiveButtonButPoor = interactions.Button(style=ButtonStyle.SECONDARY,label="Vous êtes pauvre, mais deluxe",emoji=getEmojiObject('<:teamBought:906621631143743538>'),custom_id="buy'n'send all",disabled=True)
allBuyButtonButAllreadyHaveM = interactions.Button(style=ButtonStyle.SECONDARY,label="Vous êtes un acheteur compulsif",emoji=getEmojiObject('<:bought:906623435256504451>'),custom_id="buy all",disabled=True)
allGiveButtonButAllreadyHaveM = interactions.Button(style=ButtonStyle.SECONDARY,label="Vous êtes un acheteur compulsif deluxe",emoji=getEmojiObject('<:teamBought:906621631143743538>'),custom_id="buy'n'send all",disabled=True)
allBuyButtonButAllreadyHaveF = interactions.Button(style=ButtonStyle.SECONDARY,label="Vous êtes une acheteuse compulsive",emoji=getEmojiObject('<:bought:906623435256504451>'),custom_id="buy all",disabled=True)
allGiveButtonButAllreadyHaveF = interactions.Button(style=ButtonStyle.SECONDARY,label="Vous êtes une acheteuse compulsive deluxe",emoji=getEmojiObject('<:teamBought:906621631143743538>'),custom_id="buy'n'send all",disabled=True)
global shopMaraine
shopMaraine = "iiiiii"

haveIcon = "<:bought:906623435256504451>"
allTeamHaveIcon = "<:teamBought:906621631143743538>"


def formatShop(txt:str) -> str:
    baddyTabl = ["","","","",""]
    if "baddy" in txt:
        for cmpt in range(0,5):
            baddyTabl[cmpt]=["<:baddy{0}:1003027064112287764>".format(cmpt),"<:baddy{0}:1003027102196572270>".format(cmpt)][int(random.randint(0,99)//50)]
    if "{maraine}" in txt:
        global shopMaraine
        shopMaraine = shopMaraine + "iii"

    return txt.format(
        lena = '<:lena:909047343876288552>',
        alice = '<:alice:908902054959939664>',
        shushi = '<:shushi:909047653524963328>',timeo="<:timeoB:1104517210728308746>",
        clemence = '<:clemence:908902579554111549>', john = '<:john:908887592756449311>', sclem = '<:smallClemence:1178113069973508126>',
        luna = '<:luna:909047362868105227>', stella = "<:stella:1116365644263333988>", celeste = "<:celeste:1129042444479119401>", abigail = "<:abigail:1130264097271853056>",
        feli = '<:felicite:909048027644317706>', felicite = '<:felicite:909048027644317706>',
        icealia = '<:icealia:909065559516250112>',lohica='<:lohica:919863918166417448>',ly='<:ly:943444713212641310>',amary='<:amary:979441677460713502>',pirate='<:pirSab1:1059519845177249812>',pirate1='<:pirSab1:1059519845177249812>',pirate2='<:pirGun1:1059519820376330351>',pirate3='<:pirGun2:1059519760284528640>',
        shihu = '<:shihu:909047672541945927>', stimeo = '<:stimeo:1089164206336647168>', itimeo = "<:itimeo:1103217741172846614>",
        shehisa = '<:shehisa:919863933320454165>', helene = tablAllAllies[6].icon, astra = "<:astra:1051825407466426430>",
        sixtine = '<:sixtine:908819887059763261>', lily = '<:lily:1006442350471553076>', dSixtine = "<:dreamSixtine:1100793996483235851>",
        iliana = '<:Iliana:926425844056985640>', catili = '<:catIli:1006440617146060850>', childIli = "<:childIli:1089607519380443229>", miniIli = "<:miniIli:1089607564548898876>", aurora = "<:aurora:1100791091483136133>", suivant = "Suivant d'Aurora", gaurora = "<:gaurora:1103332091594281050>",
        gweny = tablAllAllies[1].icon, alty = '<:alty:1112517632671875152>', klikli ='<:klikli:906303031837073429>', karai = '<:karail:974079383197339699>',
        lio = "<:lio:908754690769043546>", liu = "<:liu:908754674449018890>", liz = '<:lie:908754710121574470>', lia = "<:lia:908754741226520656>", kitsune = "<:kitsune:935552850686255195>", penelope = "<:penelope:1178446515459588106>",
        anna = "<:anna:943444730430246933>", belle = "<:belle:943444751288528957>",
        edelweiss = '<:edelweiss:918451422939451412>', epiphyllum = "<:epiphilium:1014094726351294484>",
        ruby='<:ruby:1112519724799103037>', julie = '<:julie:910185448951906325>',
        akia = '<a:akia:993550766415564831>',
        nacialisla = "<:nacialisla:985933665534103564>", silicia = "<:silicia:1045109225615003729>", ailill = "<a:Ailill:882040705814503434>",
        benedicte = "<:benedict:1116416894426173520>", 
        kiku = "<:kiku:962082466368213043>", churi = '<:churi:992941366537633914>', skeleton = "<a:smnMage:1054312154452471838>", churHin = '<:churHi:994045813175111811>', anais="<:anais:1166806279042375780>",
        akira = '<:akira:909048455828238347>', krys = "<:krys:916118008991215726>",
        baddy1 = baddyTabl[0], baddy2 = baddyTabl[1], baddy3 = baddyTabl[2], baddy4 = baddyTabl[3], baddy5 = baddyTabl[4],
        maraine = "Mara{0}ne".format(shopMaraine), chauvesouris = "🦇", thomas = "Thomas",
        surrin = "<:surin:1113685316319072297>", bow = "<:bow:1113685339400327198>", imea = "<:imea:1116364997073829998>", isa = "<:isa:1158136337061400797>",
        soul = "<:ghostB:1119951487032901722>", vampire = "Vampire", jade = "<:jade:1178453233442754701>", alexandre = '<:alexandre:1178570945368162405>', zeneca = '<:zeneca:1177606488496283689>', kaleb='<:kaleb:1183176411452813433>'
    )

async def shop2(bot : interactions.Client, ctx : interactions.Message,shopping : list):
    pathUserProfile = absPath + "/userProfile/" + str(ctx.author.id) + ".prof"
    if os.path.exists(pathUserProfile): # Does the user have a character
        user = loadCharFile(pathUserProfile)
        if random.randint(0,99) < 90:
            shopTotalRandom = copy.deepcopy(shopRandomMsg)

            dateNow = datetime.now(parisTimeZone).replace(tzinfo=None)
            years = dateNow.year

            if dateNow > datetime.strptime("23/12/{0}".format(years),"%d/%m/%Y") and dateNow < datetime.strptime("4/1/{0}".format(years+1),"%d/%m/%Y"):
                shopTotalRandom += shopEventEndYears 

            shopTotalRandom += shopMonthlyMsg[dateNow.month-1]+shopMonthlyMsg[dateNow.month-1]+shopMonthlyMsg[dateNow.month-1]+ shopLastMonthlyMsg[dateNow.month-1]

            for shopDict in shopEventOneDay:
                if shopDict["date"] == (dateNow.day,dateNow.month):
                    shopTotalRandom = shopDict["tabl"]
                    break

            shopRdMsg = formatShop(shopTotalRandom[random.randint(0,len(shopTotalRandom)-1)])
        else:
            shopRdMsg = formatShop(singingShopMsg[random.randint(0,len(singingShopMsg)-1)])
        initMsg = None

        if user.team != 0:
            teamList = userTeamDb.getTeamMember(user.team)
        else:
            teamList = [user.owner]

        buttonGift = interactions.Button(style=3, label="Offrir",emoji=PartialEmoji(name='🎁'),custom_id="1",disabled=len(teamList) == 1)
        buttonAllGift = interactions.Button(style=3, label="Offrir à tous",emoji=getEmojiObject('<:teamBought:906621631143743538>'),custom_id="2",disabled=len(teamList) == 1)

        allButtons = interactions.ActionRow(buttonReturn,buttonBuy,buttonGift,buttonAllGift)
        buttonsWithoutBuy = interactions.ActionRow(buttonReturn,buttonGift,buttonAllGift)
        while 1: 
            # Loading the user's team
            if len(teamList) > 1:
                teamMember = []
                for a in teamList:
                    if a != int(ctx.author.id):
                        teamMember += [loadCharFile(absPath + "/userProfile/" + str(a) + ".prof")]

            shopEmb = interactions.Embed(title = "__Shop__",color = user.color, description = "Le magasin est commun à tous les serveurs et est actualisé toutes les 3 heures"+f"\n\nVous disposez actuellement de {user.currencies} <:coins:862425847523704832>.\nVous êtes en possession de **{round(userShopPurcent(user),2)}**% du magasin.\n\n{shopRdMsg}")

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
                        shopField[a] += f"\n{b.emoji} {b.name} ({b.price} <:coins:862425847523704832>)"
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
                        options += [interactions.StringSelectOption(label=unhyperlink(b.name),value=b.id,emoji=getEmojiObject(b.emoji),description=desc+desc2)]
                shopField[a] = reduceEmojiNames(shopField[a])
                if len(shopField[a]) <= 1024:
                    shopEmb.add_field(name="<:em:866459463568850954>\n"+shopMsg[a],value=shopField[a],inline=False)
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

                    shopEmb.add_field(name="<:em:866459463568850954>\n"+shopMsg[a],value=shopField[a],inline=False)

            cd = teamWinDB.getFightCooldown(user.team,timestamp=True)
            cd2 = teamWinDB.getFightCooldown(user.team, True, timestamp=True)

            fightingStatus = teamWinDB.isFightingBool(user.team)

            if fightingStatus[0]:
               
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

                shopEmb.add_field(name="<:em:866459463568850954>\n__/cooldowns__",value=fightingRespond)
            else:
                if not(globalVar.fightEnabled()):
                    normalFightMsg = '<:noneWeap:917311409585537075>'
                else:
                    normalFightMsg = cd

                if not(globalVar.fightEnabled()):
                    quickFightMsg = '<:noneWeap:917311409585537075>'
                else:
                    quickFightMsg = cd2

                shopEmb.add_field(name=f"<:em:866459463568850954>\n__Cooldowns des commandes Fight l'équipe :__",value=f"__Normal__ : {normalFightMsg}\n__Quick__ : {quickFightMsg}",inline=False)


            select = interactions.StringSelectMenu(options,custom_id = "seeMoreInfos",placeholder="Choisissez un article pour avoir plus d'informations dessus")

            if totalCost > user.currencies:
                temp1 = allBuyButtonButPoor
            elif totalCost == 0:
                temp1 = [allBuyButtonButAllreadyHaveM,allBuyButtonButAllreadyHaveF,allBuyButtonButAllreadyHaveM][user.gender]
            elif user.currencies >= totalCost:
                temp1 = allBuyButton

            actrow2 = ActionRow(temp1)
            if totalTeamCost > user.currencies:
                actrow2.add_component(allGiveButtonButPoor)
            elif totalTeamCost == 0:
                actrow2.add_component([allGiveButtonButAllreadyHaveM,allGiveButtonButAllreadyHaveF,allGiveButtonButAllreadyHaveM][user.gender])
            elif user.currencies >= totalTeamCost:
                actrow2.add_component(allGiveButton)

            if initMsg != None:
                await initMsg.edit(embeds = shopEmb,components=[interactions.ActionRow(select),actrow2])
            else:
                try:
                    initMsg = await ctx.send(embeds = shopEmb,components=[interactions.ActionRow(select),actrow2])
                except:
                    initMsg = await ctx.channel.send(embeds = shopEmb,components=[interactions.ActionRow(select),actrow2])

            def check(m):
                m = m.ctx
                return int(m.author.id) == int(ctx.author.id)

            try:
                respond = await bot.wait_for_component(messages=initMsg,check=check,timeout=60)
                respond: ComponentContext = respond.ctx
                await respond.defer()
            except:
                timeoutEmbed = interactions.Embed(title="__Shop__",color=user.color,description=shopRdMsg)
                shopField = ["","",""]
                for a in [0,1,2]:
                    for b in [shopWeap,shopSkill,shopStuff,shopOther][a]:
                        if b != None:
                            shopField[a] += "\n{0} {1}".format(b.emoji,b.name)

                    timeoutEmbed.add_field(name="<:em:866459463568850954>\n"+shopMsg[a],value=shopField[a],inline=True)

                await initMsg.edit(embeds = timeoutEmbed,components=[])
                return 0

            if respond.component_type == 2:
                if respond.custom_id =="buy all":
                    tempMsg = await respond.send(embeds=interactions.Embed(title="__/shop__ - Devenir pauvre",color=user.color,description="Vos achats sont en cours d'enregistrement..."))
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
                    await tempMsg.edit(embeds=interactions.Embed(title="__/shop__ - Devenir pauvre",color=user.color,description="__Vous avez acheté les objets suivants pour la somme de **{0}** <:coins:862425847523704832> :__\n{1}".format(separeUnit(totalCost),temp)))

                elif respond.custom_id == "buy'n'send all":
                    tempMsg = await respond.send(embeds=interactions.Embed(title="__/shop__ - Devenir pauvre (Deluxe)",color=user.color,description="Vos achats sont en cours d'enregistrement..."))
                    user = loadCharFile("./userProfile/{0}.prof".format(user.owner))
                    tempTabl1,tempTabl2,tempTabl3 = [],[],[]
                    for teamUser in teamMember:
                        gifted = loadCharFile("./userProfile/{0}.prof".format(teamUser.owner))
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

                                if obj.name not in tempTabl1:
                                    tempTabl1.append(obj.name)
                                    tempTabl2.append(1)
                                    tempTabl3.append(obj.emoji)
                                else:
                                    for cmpt in range(len(tempTabl1)):
                                        if tempTabl1[cmpt] == obj.name:
                                            tempTabl2[cmpt] += 1

                        saveCharFile("./userProfile/{0}.prof".format(gifted.owner),gifted)
                    
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
                    await tempMsg.edit(embeds=interactions.Embed(title="__/shop__ - Devenir pauvre (Deluxe)",color=user.color,description="__Vous avez acheté les objets suivants pour la somme de **{0}** <:coins:862425847523704832> :__\n{1}".format(separeUnit(totalTeamCost),temp)))

            else:
                await initMsg.edit(embeds = shopEmb,components=[interactions.ActionRow(getChoisenSelect(select,respond.values[0]))])
                rep = None
                for a in range(0,len(shopped)):
                    if shopped[a].id == respond.values[0]:
                        rep = a
                        break

                try:
                    msg = await respond.send(embeds = interactions.Embed(title="shop",description="Recherche de l'objet dans les rayons..."))
                except:
                    msg = await initMsg.channel.send(embeds = interactions.Embed(title="shop",description="Recherche de l'objet dans les rayons..."))

                try:
                    if rep == None:                     # Object not found
                        await msg.edit(embeds=interactions.Embed(title="Error in shop command",description="Unfound object"))
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
                            await msg.edit(embeds = repEmb,components=[onlyReturn])
                        else:
                            if user.have(obj):
                                repEmb.set_footer(text = "Vous possédez déjà cet objet")
                                await msg.edit(embeds = repEmb,components=[buttonsWithoutBuy])
                            else:
                                repEmb.set_footer(text = "Cliquez sur le bouton \"Acheter\" pour acheter cet objet")
                                await msg.edit(embeds = repEmb,components=[allButtons])

                            try:
                                rep = await bot.wait_for_component(messages=msg,check=check,timeout=60)
                                rep: ComponentContext = rep.ctx
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
                                        await msg.edit(embeds = interactions.Embed(title="shop"+ " - " +obj.name,color = user.color,description = f"Votre achat a bien été effectué ! Faites \"/inventory nom:{obj.id}\" pour l'équiper"),components=[])
                                    except:
                                        await msg.edit(embeds = errorEmbed("shop","Une erreur s'est produite"))

                                elif rep.custom_id == "1":              # Gift to annother teamMate
                                    options = []
                                    for a in teamMember:
                                        if not(a.have(obj)) and a.owner != user.owner:
                                            options += [interactions.StringSelectOption(label=a.name,value=str(a.owner),emoji=getEmojiObject(await getUserIcon(bot,a)))]

                                    if options == [] :
                                        select = interactions.StringSelectMenu([interactions.StringSelectOption(label="Vous n'avez pas à voir ça",value="Nani")],placeholder="Toute votre équipe a déjà cet objet",disabled=True,custom_id = "ohYouWantToSeeThis")
                                    else:
                                        select = interactions.StringSelectMenu(options,custom_id = "mudamudamudamudamuda",placeholder="À qui voulez vous offrir cet objet ?")
                                    await msg.edit(embeds= repEmb, components=[interactions.ActionRow(buttonReturn),interactions.ActionRow(select)])

                                    respond = None
                                    try:
                                        respond = await bot.wait_for_component(messages=msg,timeout = 60)
                                        respond: ComponentContext = respond.ctx
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
                                                        await temp.delete()
                                                        await msg.edit(embeds = interactions.Embed(title="shop",color = user.color,description = f"Votre cadeau a bien été envoyé !"),components = [interactions.ActionRow(getChoisenSelect(select,respond.values[0]))])
                                                    except:
                                                        await msg.edit(embeds = errorEmbed("shop","Une erreur s'est produite"))
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
                                        buttonConfirm = interactions.Button(style=1,label="Rendez moi pauvre !",emoji=getEmojiObject('<:coins:862425847523704832>'),custom_id="buy")
                                    else:
                                        buttonConfirm = interactions.Button(style=1,label="Rendez moi pauvre !",emoji=getEmojiObject('<:coins:862425847523704832>'),custom_id="buy",disabled=True)

                                    await msg.edit(embeds = interactions.Embed(title="__/shop {0}__".format(obj.name),color=user.color,description=msgTeamToGift),components=[interactions.ActionRow(buttonReturn,buttonConfirm)])

                                    try:
                                        respond = await bot.wait_for_component(messages=msg,timeout = 60,check=check)
                                        respond: ComponentContext = respond.ctx
                                    except:
                                        break

                                    if respond.custom_id == "buy":
                                        await msg.edit(embeds = interactions.Embed(title="__/shop {0}__".format(obj.name),color = user.color,description = f"Envoie de vos cadeaux... <a:loading:862459118912667678>"),components = [])
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

                                            else:
                                                user.otherInventory += [obj]
                                                user.currencies = user.currencies - obj.price
                                                saveCharFile(absPath + "/userProfile/" + str(ctx.author.id) + ".prof",user)
                                        await msg.edit(embeds = interactions.Embed(title="shop",color = user.color,description = f"Vos cadeaux ont bien été envoyés !"),components = [])
                                    else:
                                        await msg.delete()

                                elif rep.custom_id == "-1":
                                    await msg.delete()
                except:
                    await msg.edit(embeds=interactions.Embed(title="Uncatch error in shop command",description=format_exc()),components=[])
    else:
        await ctx.send(embeds = errorEmbed("shop","Vous n'avez pas commencé l'aventure"),ephemeral=True)

if not(isLenapy):
    print("Shop message verification...")
    tablShopMsg = shopRandomMsg+shopEventEndYears
    for temp in shopEventOneDay:
        tablShopMsg = tablShopMsg + temp["tabl"]
    for temp in shopMonthlyMsg:
        tablShopMsg = tablShopMsg + temp

    for shopmsg in tablShopMsg:
        try:
            formatShop(shopmsg)
        except:
            print("Error with the following shop message :\n{0}".format(shopmsg))
            print_exc()
    print("Shop message verification done")

async def seeSkillsRep(ctx : interactions.SlashContext, skillType:int, aspiration:int = None, element:int = None, use: int=None, skillRange : int = None):
    tablToSee: List[skill] = skillsCat[skillType][:]
    firstMsgSend = False

    for skillToSee in tablToSee[:]:
        if (element != None and skillToSee.condition != [EXCLUSIVE,ELEMENT,element]) or (aspiration != None and skillToSee.condition != [EXCLUSIVE,ASPIRATION,aspiration]) or (use != None and skillToSee.use != use):
            try:
                tablToSee.remove(skillToSee)
            except:
                pass

    tablsCd: List[List[skill]] = [[],[],[]]
    for skilly in tablToSee:
        if (use == None or skilly.use == use):
            if skilly.cooldown <= 3:
                tablsCd[0].append(skilly)
            elif skilly.cooldown <= 5:
                tablsCd[1].append(skilly)
            else:
                tablsCd[2].append(skilly)

    tablLens, lenTot = [0,len(tablsCd[0]),len(tablsCd[1])+len(tablsCd[0])], len(tablsCd[0])+len(tablsCd[1])+len(tablsCd[2])

    if len(tablsCd[0]) + len(tablsCd[1]) + len(tablsCd[2]) > 0:
        for cmpt in range(3):
            tablsCd[cmpt].sort(key=lambda ballerine : ballerine.iaPow, reverse=True)
            desc = ""
            for cmpt2 in range(len(tablsCd[cmpt])):
                desc += "{0} {2}{1}{2}".format(tablsCd[cmpt][cmpt2].emoji, tablsCd[cmpt][cmpt2].name, ["","`"][tablsCd[cmpt][cmpt2] in listUseSkills])
                toAdd = ""
                if len(tablsCd[cmpt][cmpt2].condition) > 0:
                    if tablsCd[cmpt][cmpt2].condition[1] == ASPIRATION:
                        toAdd += aspiEmoji[tablsCd[cmpt][cmpt2].condition[2]]
                    elif tablsCd[cmpt][cmpt2].condition[1] == ELEMENT:
                        toAdd += elemEmojis[tablsCd[cmpt][cmpt2].condition[2]]
                if tablsCd[cmpt][cmpt2].ultimate :
                    toAdd += "<:littleStar:925860806602682369>"
                if tablsCd[cmpt][cmpt2].group == SKILL_GROUP_DEMON:
                    toAdd += "<:dmon:1004737763771433130>"
                elif tablsCd[cmpt][cmpt2].group == SKILL_GROUP_HOLY:
                    toAdd += "<:dvin:1004737746377654383>"
                if toAdd != "":
                    desc += " - {0}".format(toAdd)
                desc += "\n"
                if len(desc) > 4000 or tablsCd[cmpt][cmpt2] == tablsCd[cmpt][-1]:
                    if not(firstMsgSend):
                        if ctx.__class__ == interactions.Message:
                            await ctx.edit(embeds=interactions.Embed(title="__Cooldown {0}__".format(["faible","moyen","élevé"][cmpt]),description=desc,color=light_blue,footer=EmbedFooter(text="{0}/{1}".format(tablLens[cmpt]+cmpt2+1,lenTot))))
                        else:
                            await ctx.send(embeds=interactions.Embed(title="__Cooldown {0}__".format(["faible","moyen","élevé"][cmpt]),description=desc,color=light_blue,footer=EmbedFooter(text="{0}/{1}".format(tablLens[cmpt]+cmpt2+1,lenTot))))
                        firstMsgSend = True
                    else:
                        await ctx.channel.send(embeds=interactions.Embed(title="__Cooldown {0}__".format(["faible","moyen","élevé"][cmpt]),description=desc,color=light_blue,footer=EmbedFooter(text="{0}/{1}".format(tablLens[cmpt]+cmpt2+1,lenTot))))
                    desc = ""
    else:
        
        await ctx.send(embeds=interactions.Embed(title="__Aucune correspondance__",description="-",color=light_blue))

async def testShopMsgFunction(ctx: interactions.SlashContext):
    listEmbed: List[interactions.Embed] = []
    dateNow, started = datetime.now(parisTimeZone), False
    for cmpt in range(len(shopMonthlyMsg[dateNow.month-1])):
        if not(started):
            await ctx.send(embeds=[interactions.Embed(title=str(cmpt),description=formatShop(shopMonthlyMsg[dateNow.month-1][cmpt]))])
            started = True
        else:
            await ctx.channel.send(embeds=[interactions.Embed(title=str(cmpt),description=formatShop(shopMonthlyMsg[dateNow.month-1][cmpt]))])
