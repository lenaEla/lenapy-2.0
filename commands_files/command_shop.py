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
buttonGift = create_button(3,"Offrir",emoji='🎁',custom_id="1")
buttonAllGift = create_button(3,"Offrir à tous",emoji=getEmojiObject('<:teamBought:906621631143743538>'),custom_id="2")
allButtons = create_actionrow(buttonReturn,buttonBuy,buttonGift,buttonAllGift)
buttonsWithoutBuy = create_actionrow(buttonReturn,buttonGift,buttonAllGift)
onlyReturn = create_actionrow(buttonReturn)


haveIcon = "<:bought:906623435256504451>" 
allTeamHaveIcon = "<:teamBought:906621631143743538>"

async def shop2(bot : discord.Client, ctx : discord.message,shopping : list):
    pathUserProfile = absPath + "/userProfile/" + str(ctx.author.id) + ".prof"
    if os.path.exists(pathUserProfile): # Does the user have a character
        user = loadCharFile(pathUserProfile,ctx)
        try:
            msg = await loadingEmbed(ctx)
        except:
            msg = await loadingSlashEmbed(ctx)

        shopRdMsg = shopRandomMsg[random.randint(0,len(shopRandomMsg)-1)].format(ctx.author.name,user.name)
        initMsg = msg
        while 1: 
            # Loading the user's team
            if user.team != 0:
                team = readSaveFiles(absPath + "/userTeams/" + str(user.team) +".team")[0]
                teamMember = []
                for a in team:
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
                            desc2 = " - Vous possédez déjà cet objet"
                        
                        if user.team != 0:
                            allTeamHave = True
                            for c in teamMember:
                                if not(c.have(b)):
                                    allTeamHave = False
                                    break

                            if allTeamHave:
                                icon = " ("+allTeamHaveIcon+")"
                                desc2 = " - Toute votre équipe possède cet objet"

                        shopField[a] += icon
                        options += [create_select_option(unhyperlink(b.name),b.id,getEmojiObject(b.emoji),desc+desc2)]
                if len(shopField[a]) <= 1024:
                    shopEmb.add_field(name="<:empty:866459463568850954>\n"+shopMsg[a],value=shopField[a],inline=False)
                else:
                    shopField[a] = ""
                    for b in [shopWeap,shopSkill,shopStuff,shopOther][a]:
                        if b != None:
                            shopField[a] += f"\n - {b.name} : {b.price} pièces"
                            icon = ""
                            if user.have(b):
                                icon = " (☑️)"

                            if user.team != 0:
                                allTeamHave = True
                                for c in teamMember:
                                    if not(c.have(b)):
                                        allTeamHave = False
                                        break

                                if allTeamHave:
                                    icon = " (✅)"

                            shopField[a] += icon

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

            if not(teamWinDB.isFightingBool(ballerine)):
                shopEmb.add_field(name=f"<:empty:866459463568850954>\n__Cooldowns des commandes Fight l'équipe :__",value=f"__Normal__ : {fcooldown} minute{faccord} et {fseconds} seconde{fsaccord}\n__Quick__ : {fqcooldown} minute{fqaccord} et {fqseconds} seconde{fqsaccord}",inline=False)
            else:
                shopEmb.add_field(name=f"<:empty:866459463568850954>\n__Cooldowns des commandes Fight l'équipe :__",value=f"__Normal__ : En combat <:turf:810513139740573696>\n__Quick__ : {fqcooldown} minute{fqaccord} et {fqseconds} seconde{fqsaccord}",inline=False)

            if userShopPurcent(user) >= 75 and not(user.have(trans)):
                fullEmb = discord.Embed(title="Vous avez obtenu 75% du magasin",description="Vous recevez la compétence suivante en récompense :\n<:limiteBreak:886657642553032824> Transcendance (identifiant : yt)",color=user.color)
                user.skillInventory.append(trans)
                saveCharFile(pathUserProfile,user)
                await ctx.channel.send(embed=fullEmb)

            select = create_select(
                options=options,
                placeholder="Choisissez un article pour avoir plus d'informations dessus"
                )
            
            await initMsg.edit(embed = shopEmb,components=[create_actionrow(select)])

            def check(m):
                return m.author_id == ctx.author.id and m.origin_message.id == msg.id

            def check2(m):
                return m.author_id == ctx.author.id and m.origin_message.id == initMsg.id

            try:
                respond = await wait_for_component(bot,components=select,check=check2,timeout=60)
                await initMsg.edit(embed = shopEmb,components=[create_actionrow(getChoisenSelect(select,respond.values[0]))])
            except:
                await initMsg.edit(embed = shopEmb,components=[timeoutSelect])
                break

            rep = None
            for a in range(0,len(shopped)):
                if shopped[a].id == respond.values[0]:
                    rep = a
                    break

            try:
                msg = await respond.send(embed = discord.Embed(title="shop",description="Recherche de l'objet dans les rayons..."))
            except:
                msg = await initMsg.channel.send(embed = discord.Embed(title="shop",description="Recherche de l'objet dans les rayons..."))
            if rep != None:
                typ = whatIsThat(shopped[rep])

                if typ == 0: # Is weapon
                    arm = shopped[rep]
                    repEmb = infoWeapon(arm,user,ctx)

                    if user.currencies < arm.price:
                        repEmb.set_footer(text = "Vous n'avez pas suffisament de pièces")
                        await msg.edit(embed = repEmb,components=[onlyReturn])
                    elif user.have(arm):
                        repEmb.set_footer(text = "Vous possédez déjà cette arme")
                        await msg.edit(embed = repEmb,components=[buttonsWithoutBuy])
                    else:
                        repEmb.set_footer(text = "Cliquez sur le bouton \"Acheter\" pour acheter cet objet !")
                        await msg.edit(embed = repEmb,components=[allButtons])

                    rep = await wait_for_component(bot,components=[buttonReturn,buttonBuy,buttonGift,buttonAllGift],check=check,timeout=60)

                    if rep.custom_id == "0":
                        try:
                            user.weaponInventory += [arm]
                            user.currencies = user.currencies - arm.price
                            saveCharFile(pathUserProfile,user)
                            await msg.edit(embed = discord.Embed(title="shop"+ " - " +arm.name,color = user.color,description = f"Votre achat a bien été effectué ! Faites \"l!inventory {arm.id}\" pour l'équiper"),components=[],delete_after=5)
                        except:
                            await msg.edit(embed = errorEmbed("shop","Une erreur s'est produite"))

                    elif rep.custom_id == "1":          # Gift
                        options = []
                        for a in teamMember:
                            if arm not in a.weaponInventory and a.owner != user.owner:
                                options += [create_select_option(a.name,a.owner,getEmojiObject(await getUserIcon(bot,a)))]

                        if options == [] :
                            select = create_select([create_select_option("Vous n'avez pas à voir ça","Nani")],placeholder="Toute votre équipe a déjà cet objet",disabled=True)
                        else:
                            select = create_select(options,placeholder="À qui voulez vous offrir cet objet ?")
                        await msg.edit(embed= repEmb, components=[])
                        await msg.edit(embed= repEmb, components=[create_actionrow(buttonReturn),create_actionrow(select)])

                        respond = await wait_for_component(bot,components=[buttonReturn,select],timeout = 60)
                        try:
                            for a in teamMember:
                                if a.owner == respond.values[0]:
                                    try:
                                        try:
                                            temp = await respond.send("Envoie du cadeau...")
                                        except:
                                            temp = await initMsg.channel.send("Envoie du cadeau...")
                                        a.weaponInventory += [arm]
                                        user.currencies = user.currencies - arm.price
                                        saveCharFile(absPath + "/userProfile/" + str(a.owner) + ".prof",a)
                                        saveCharFile(absPath + "/userProfile/" + str(ctx.author.id) + ".prof",user)
                                        try:
                                            dest = await bot.fetch_user(a.owner)
                                            await dest.send(embed = discord.Embed(title="Livraison",description = "Vous avez reçu l'objet __{0}__ de la part de {1}".format(unhyperlink(arm.name),user.name),color = a.color))
                                        except:
                                            pass
                                        await temp.delete()
                                        await msg.edit(embed = discord.Embed(title="shop",color = user.color,description = f"Votre cadeau a bien été envoyé !"),components = [create_actionrow(getChoisenSelect(select,respond.values[0]))],delete_after=5)
                                    except:
                                        await msg.edit(embed = errorEmbed("shop","Une erreur s'est produite"))
                                    break
                        except:
                            await msg.delete()

                    elif rep.custom_id == "2":          # All Gift
                        tablTeamToGift, msgTeamToGift = [],"Voulez vous offrir __{0}__ aux coéquipiers suivants ?\n".format(arm.name)

                        for a in teamMember:
                            if arm not in a.weaponInventory:
                                tablTeamToGift.append(a)
                                msgTeamToGift += "{0} {1}\n".format(await getUserIcon(bot,a), a.name)

                        msgTeamToGift += "\nPrix total : {0} <:coins:862425847523704832>".format(arm.price * len(tablTeamToGift))

                        if user.currencies >= arm.price * len(tablTeamToGift):
                            buttonConfirm = create_button(1,"Rendez moi pauvre !",getEmojiObject('<:coins:862425847523704832>'),"buy")
                        else:
                            buttonConfirm = create_button(1,"Rendez moi pauvre !",getEmojiObject('<:coins:862425847523704832>'),"buy",disabled=True)

                        await msg.edit(embed = discord.Embed(title="__/shop {0}__".format(arm.name),color=user.color,description=msgTeamToGift),components=[create_actionrow(buttonReturn,buttonConfirm)])

                        try:
                            respond = await wait_for_component(bot,messages=msg,timeout = 60)
                        except:
                            break

                        if respond.custom_id == "buy":
                            await msg.edit(embed = discord.Embed(title="__/shop {0}__".format(arm.name),color = user.color,description = f"Envoie de vos cadeaux... <a:loading:862459118912667678>"),components = [])
                            for a in tablTeamToGift:
                                if int(a.owner) != int(user.owner):
                                    a.weaponInventory += [arm]
                                    user.currencies = user.currencies - arm.price
                                    saveCharFile(absPath + "/userProfile/" + str(a.owner) + ".prof",a)
                                    saveCharFile(absPath + "/userProfile/" + str(ctx.author.id) + ".prof",user)
                                    try:
                                        dest = await bot.fetch_user(a.owner)
                                        await dest.send(embed = discord.Embed(title="Livraison",description = "Vous avez reçu l'objet __{0}__ de la part de {1}".format(unhyperlink(arm.name),user.name),color = a.color))
                                    except:
                                        pass
                                else:
                                    user.weaponInventory += [arm]
                                    user.currencies = user.currencies - arm.price
                                    saveCharFile(absPath + "/userProfile/" + str(ctx.author.id) + ".prof",user)

                            await msg.edit(embed = discord.Embed(title="shop",color = user.color,description = f"Vos cadeaux ont bien été envoyés !"),components = [],delete_after=5)
                        else:
                            await msg.delete()

                    elif rep.custom_id == "-1":
                        await msg.delete()

                elif typ == 1: # Is skill
                    arm = shopped[rep]
                    repEmb = infoSkill(shopped[rep],user,ctx)
                    if user.currencies < arm.price: # Not enougth coins
                        repEmb.set_footer(text = "Vous n'avez pas suffisament de pièces")
                        await msg.edit(embed = repEmb,components=[onlyReturn])
                    elif user.have(arm): # Already have
                        repEmb.set_footer(text = "Vous possédez déjà cette compétence")
                        await msg.edit(embed = repEmb,components=[buttonsWithoutBuy])
                    else: # Buy
                        repEmb.set_footer(text = "Cliquez sur le bouton \"Acheter\" pour acheter cet objet !")
                        await msg.edit(embed = repEmb,components=[allButtons])

                    rep = await wait_for_component(bot,components=[buttonReturn,buttonBuy,buttonGift,buttonAllGift],check=check,timeout=60)

                    if rep.custom_id == "0": # Buyed
                        try:
                            user.skillInventory += [arm]
                            user.currencies = user.currencies - arm.price
                            saveCharFile(pathUserProfile,user)
                            await msg.edit(embed = discord.Embed(title="shop"+ " - " +arm.name,color = user.color,description = f"Votre achat a bien été effectué ! Faites \"l!inventory {arm.id}\" pour l'équiper"),components=[],delete_after=5)
                        except:
                            await msg.edit(embed = errorEmbed("shop","Une erreur s'est produite"))
                    elif rep.custom_id == "1": # Gift
                        options = []
                        for a in teamMember:
                            if arm not in a.skillInventory and a.owner != user.owner:
                                options += [create_select_option(a.name,a.owner,getEmojiObject(await getUserIcon(bot,a)))]

                        if options == [] :
                            select = create_select([create_select_option("Vous n'avez pas à voir ça","Nani")],placeholder="Toute votre équipe a déjà cet objet",disabled=True)
                        else:
                            select = create_select(options,placeholder="À qui voulez vous offrir cet objet ?")
                        await msg.edit(embed= repEmb, components=[])
                        await msg.edit(embed= repEmb, components=[create_actionrow(buttonReturn),create_actionrow(select)])

                        respond = await wait_for_component(bot,components=[buttonReturn,select],timeout = 60)
                        try:
                            for a in teamMember:
                                if a.owner == respond.values[0]:
                                    try:
                                        try:
                                            temp = await respond.send("Envoie du cadeau...")
                                        except:
                                            temp = await initMsg.channel.send("Envoie du cadeau...")
                                        a.skillInventory += [arm]
                                        user.currencies = user.currencies - arm.price
                                        saveCharFile(absPath + "/userProfile/" + str(a.owner) + ".prof",a)
                                        saveCharFile(absPath + "/userProfile/" + str(ctx.author.id) + ".prof",user)
                                        try:
                                            dest = await bot.fetch_user(a.owner)
                                            await dest.send(embed = discord.Embed(title="Livraison",description = "Vous avez reçu l'objet __{0}__ de la part de {1}".format(arm.name,user.name),color = a.color))
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
                        tablTeamToGift, msgTeamToGift = [],"Voulez vous offrir __{0}__ aux coéquipiers suivants ?\n".format(arm.name)

                        for a in teamMember:
                            if arm not in a.skillInventory:
                                tablTeamToGift.append(a)
                                msgTeamToGift += "{0} {1}\n".format(await getUserIcon(bot,a), a.name)

                        msgTeamToGift += "\nPrix total : {0} <:coins:862425847523704832>".format(arm.price * len(tablTeamToGift))

                        if user.currencies >= arm.price * len(tablTeamToGift):
                            buttonConfirm = create_button(1,"Rendez moi pauvre !",getEmojiObject('<:coins:862425847523704832>'),"buy")
                        else:
                            buttonConfirm = create_button(1,"Rendez moi pauvre !",getEmojiObject('<:coins:862425847523704832>'),"buy",disabled=True)

                        await msg.edit(embed = discord.Embed(title="__/shop {0}__".format(arm.name),color=user.color,description=msgTeamToGift),components=[create_actionrow(buttonReturn,buttonConfirm)])

                        try:
                            respond = await wait_for_component(bot,messages=msg,timeout = 60)
                        except:
                            break

                        if respond.custom_id == "buy":
                            await msg.edit(embed = discord.Embed(title="__/shop {0}__".format(arm.name),color = user.color,description = f"Envoie de vos cadeaux... <a:loading:862459118912667678>"),components = [])
                            for a in tablTeamToGift:
                                if int(a.owner) != int(user.owner):
                                    a.skillInventory += [arm]
                                    user.currencies = user.currencies - arm.price
                                    saveCharFile(absPath + "/userProfile/" + str(a.owner) + ".prof",a)
                                    saveCharFile(absPath + "/userProfile/" + str(ctx.author.id) + ".prof",user)
                                    try:
                                        dest = await bot.fetch_user(a.owner)
                                        await dest.send(embed = discord.Embed(title="Livraison",description = "Vous avez reçu l'objet __{0}__ de la part de {1}".format(unhyperlink(arm.name),user.name),color = a.color))
                                    except:
                                        pass
                                else:
                                    user.skillInventory += [arm]
                                    user.currencies = user.currencies - arm.price
                                    saveCharFile(absPath + "/userProfile/" + str(ctx.author.id) + ".prof",user)
                            await msg.edit(embed = discord.Embed(title="shop",color = user.color,description = f"Vos cadeaux ont bien été envoyés !"),components = [],delete_after=5)
                        else:
                            await msg.delete()
                    elif rep.custom_id == "-1":
                        await msg.delete()

                elif typ == 2: # Is gear
                    arm = shopped[rep]
                    repEmb = infoStuff(arm,user,ctx)
                    if user.currencies < arm.price:
                        repEmb.set_footer(text = "Vous n'avez pas suffisament de pièces")
                        await msg.edit(embed = repEmb,components=[onlyReturn])
                    elif user.have(arm):
                        repEmb.set_footer(text = "Vous possédez déjà cet objet")
                        await msg.edit(embed = repEmb,components=[buttonsWithoutBuy])
                    
                    else:
                        repEmb.set_footer(text = "Cliquez sur le bouton \"Acheter\" pour acheter cet objet !")
                        await msg.edit(embed = repEmb,components=[allButtons])

                    rep = await wait_for_component(bot,components=[buttonReturn,buttonBuy,buttonGift,buttonAllGift],check=check,timeout=60)

                    if rep.custom_id == "0":
                        try:
                            user.stuffInventory += [arm]
                            user.currencies = user.currencies - arm.price
                            saveCharFile(pathUserProfile,user)
                            await msg.edit(embed = discord.Embed(title="shop"+ " - " +arm.name,color = user.color,description = f"Votre achat a bien été effectué ! Faites \"l!inventory {arm.id}\" pour l'équiper"),components=[],delete_after=5)
                        except:
                            await msg.edit(embed = errorEmbed("shop","Une erreur s'est produite"))

                    elif rep.custom_id == "1":
                        options = []
                        for a in teamMember:
                            if arm not in a.stuffInventory and a.owner != user.owner:
                                options += [create_select_option(a.name,a.owner,getEmojiObject(await getUserIcon(bot,a)))]

                        if options == [] :
                            select = create_select([create_select_option("Vous n'avez pas à voir ça","Nani")],placeholder="Toute votre équipe a déjà cet objet",disabled=True)
                        else:
                            select = create_select(options,placeholder="À qui voulez vous offrir cet objet ?")
                        await msg.edit(embed= repEmb, components=[])
                        await msg.edit(embed= repEmb, components=[create_actionrow(buttonReturn),create_actionrow(select)])

                        respond = await wait_for_component(bot,components=[buttonReturn,select],timeout = 60)
                        try:
                            for a in teamMember:
                                if a.owner == respond.values[0]:
                                    try:
                                        try:
                                            temp = await respond.send("Envoie du cadeau...")
                                        except:
                                            temp = await initMsg.channel.send("Envoie du cadeau...")
                                        a.stuffInventory += [arm]
                                        user.currencies = user.currencies - arm.price
                                        saveCharFile(absPath + "/userProfile/" + str(a.owner) + ".prof",a)
                                        saveCharFile(absPath + "/userProfile/" + str(ctx.author.id) + ".prof",user)
                                        try:
                                            dest = await bot.fetch_user(a.owner)
                                            await dest.send(embed = discord.Embed(title="Livraison",description = "Vous avez reçu l'objet __{0}__ de la part de {1}".format(arm.name,user.name),color = a.color))
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
                        tablTeamToGift, msgTeamToGift = [],"Voulez vous offrir __{0}__ aux coéquipiers suivants ?\n".format(arm.name)

                        for a in teamMember:
                            if arm not in a.stuffInventory:
                                tablTeamToGift.append(a)
                                msgTeamToGift += "{0} {1}\n".format(await getUserIcon(bot,a), a.name)

                        msgTeamToGift += "\nPrix total : {0} <:coins:862425847523704832>".format(arm.price * len(tablTeamToGift))

                        if user.currencies >= arm.price * len(tablTeamToGift):
                            buttonConfirm = create_button(1,"Rendez moi pauvre !",getEmojiObject('<:coins:862425847523704832>'),"buy")
                        else:
                            buttonConfirm = create_button(1,"Rendez moi pauvre !",getEmojiObject('<:coins:862425847523704832>'),"buy",disabled=True)

                        await msg.edit(embed = discord.Embed(title="__/shop {0}__".format(arm.name),color=user.color,description=msgTeamToGift),components=[create_actionrow(buttonReturn,buttonConfirm)])

                        try:
                            respond = await wait_for_component(bot,messages=msg,timeout = 60)
                        except:
                            break

                        if respond.custom_id == "buy":
                            await msg.edit(embed = discord.Embed(title="__/shop {0}__".format(arm.name),color = user.color,description = f"Envoie de vos cadeaux... <a:loading:862459118912667678>"),components = [])
                            for a in tablTeamToGift:
                                if int(a.owner) != int(user.owner):
                                    a.stuffInventory += [arm]
                                    user.currencies = user.currencies - arm.price
                                    saveCharFile(absPath + "/userProfile/" + str(a.owner) + ".prof",a)
                                    saveCharFile(absPath + "/userProfile/" + str(ctx.author.id) + ".prof",user)
                                    try:
                                        dest = await bot.fetch_user(a.owner)
                                        await dest.send(embed = discord.Embed(title="Livraison",description = "Vous avez reçu l'objet __{0}__ de la part de {1}".format(unhyperlink(arm.name),user.name),color = a.color))
                                    except:
                                        pass
                                else:
                                    user.stuffInventory += [arm]
                                    user.currencies = user.currencies - arm.price
                                    saveCharFile(absPath + "/userProfile/" + str(ctx.author.id) + ".prof",user)
                            await msg.edit(embed = discord.Embed(title="shop",color = user.color,description = f"Vos cadeaux ont bien été envoyés !"),components = [],delete_after=5)
                        else:
                            await msg.delete()

                    elif rep.custom_id == "-1":
                        await msg.delete()

                elif typ == 3: # Is special object
                    arm = shopped[rep]
                    repEmb = infoOther(arm,user)
                    if user.currencies < arm.price:
                        repEmb.set_footer(text = "Vous n'avez pas suffisament de pièces")
                        await msg.edit(embed = repEmb,components=[onlyReturn])
                    elif user.have(arm):
                        repEmb.set_footer(text = "Vous possédez déjà cette arme")
                        await msg.edit(embed = repEmb,components=[buttonsWithoutBuy])
                    else:
                        repEmb.set_footer(text = "Cliquez sur le bouton \"Acheter\" pour acheter cet objet !")
                        await msg.edit(embed = repEmb,components=[allButtons])

                        rep = await wait_for_component(bot,components=[buttonReturn,buttonBuy,buttonGift,buttonAllGift],check=check,timeout=60)

                        if rep.custom_id == "0":
                            try:
                                user.otherInventory += [arm]
                                user.currencies = user.currencies - arm.price
                                saveCharFile(pathUserProfile,user)
                                await msg.edit(embed = discord.Embed(title="shop"+ " - " +arm.name,color = user.color,description = f"Votre achat a bien été effectué ! Faites \"l!inventory {arm.id}\" pour l'équiper"),components=[],delete_after=5)
                            except:
                                await msg.edit(embed = errorEmbed("shop","Une erreur s'est produite"))

                        elif rep.custom_id == "1":
                            options = []
                            for a in teamMember:
                                if arm not in a.otherInventory and a.owner != user.owner:
                                    options += [create_select_option(a.name,a.owner,getEmojiObject(await getUserIcon(bot,a)))]

                            if options == [] :
                                select = create_select([create_select_option("Vous n'avez pas à voir ça","Nani")],placeholder="Toute votre équipe a déjà cet objet",disabled=True)
                            else:
                                select = create_select(options,placeholder="À qui voulez vous offrir cet objet ?")
                            await msg.edit(embed= repEmb, components=[])
                            await msg.edit(embed= repEmb, components=[create_actionrow(buttonReturn),create_actionrow(select)])

                            respond = await wait_for_component(bot,components=[buttonReturn,select],timeout = 60)
                            try:
                                for a in teamMember:
                                    if a.owner == respond.values[0]:
                                        try:
                                            try:
                                                temp = await respond.send("Envoie du cadeau...")
                                            except:
                                                temp = await initMsg.channel.send("Envoie du cadeau...")
                                            a.otherInventory += [arm]
                                            user.currencies = user.currencies - arm.price
                                            saveCharFile(absPath + "/userProfile/" + str(a.owner) + ".prof",a)
                                            saveCharFile(absPath + "/userProfile/" + str(ctx.author.id) + ".prof",user)
                                            try:
                                                dest = await bot.fetch_user(a.owner)
                                                await dest.send(embed = discord.Embed(title="Livraison",description = "Vous avez reçu l'objet __{0}__ de la part de {1}".format(arm.name,user.name),color = a.color))
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
                            tablTeamToGift, msgTeamToGift = [],"Voulez vous offrir __{0}__ aux coéquipiers suivants ?\n".format(arm.name)

                            for a in teamMember:
                                if arm not in a.otherInventory:
                                    tablTeamToGift.append(a)
                                    msgTeamToGift += "{0} {1}\n".format(await getUserIcon(bot,a), a.name)

                            msgTeamToGift += "\nPrix total : {0} <:coins:862425847523704832>".format(arm.price * len(tablTeamToGift))

                            if user.currencies >= arm.price * len(tablTeamToGift):
                                buttonConfirm = create_button(1,"Rendez moi pauvre !",getEmojiObject('<:coins:862425847523704832>'),"buy")
                            else:
                                buttonConfirm = create_button(1,"Rendez moi pauvre !",getEmojiObject('<:coins:862425847523704832>'),"buy",disabled=True)

                            await msg.edit(embed = discord.Embed(title="__/shop {0}__".format(arm.name),color=user.color,description=msgTeamToGift),components=[create_actionrow(buttonReturn,buttonConfirm)])

                            try:
                                respond = await wait_for_component(bot,messages=msg,timeout = 60)
                            except:
                                break

                            if respond.custom_id == "buy":
                                await msg.edit(embed = discord.Embed(title="__/shop {0}__".format(arm.name),color = user.color,description = f"Envoie de vos cadeaux... <a:loading:862459118912667678>"),components = [])
                                for a in tablTeamToGift:
                                    if int(a.owner) != int(user.owner):
                                        a.otherInventory += [arm]
                                        user.currencies = user.currencies - arm.price
                                        saveCharFile(absPath + "/userProfile/" + str(a.owner) + ".prof",a)
                                        saveCharFile(absPath + "/userProfile/" + str(ctx.author.id) + ".prof",user)
                                        try:
                                            dest = await bot.fetch_user(a.owner)
                                            await dest.send(embed = discord.Embed(title="Livraison",description = "Vous avez reçu l'objet __{0}__ de la part de {1}".format(unhyperlink(arm.name),user.name),color = a.color))
                                        except:
                                            pass
                                    else:
                                        user.otherInventory += [arm]
                                        user.currencies = user.currencies - arm.price
                                        saveCharFile(absPath + "/userProfile/" + str(ctx.author.id) + ".prof",user)
                                await msg.edit(embed = discord.Embed(title="shop",color = user.color,description = f"Vos cadeaux ont bien été envoyés !"),components = [],delete_after=5)
                            else:
                                await msg.delete()

                        elif rep.custom_id == "-1":
                            await msg.delete()

    else:
        await ctx.channel.send(embed = errorEmbed("shop","Vous n'avez pas commencé l'aventure"))