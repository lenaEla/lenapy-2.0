from asyncio.tasks import sleep
import discord, asyncio
import discord_slash
from discord_slash.utils.manage_components import *
from discord_slash import ButtonStyle

from adv import *
from classes import *
from donnes import *
from gestion import *
from advance_gestion import *
from emoji import backward_arrow,check
from commands_files.command_start import chooseAspiration,chooseColor,changeCustomColor

inventoryMenu = create_select(
    options=[
        create_select_option("Inventaire d'Arme",value="0",emoji=getEmojiObject('<:splattershot:866367647113543730>')),
        create_select_option("Inventaire de Compétences",value="1",emoji=getEmojiObject('<:splatbomb:873527088286687272>')),
        create_select_option("Inventaire d'Equipement",value="2",emoji=getEmojiObject('<:bshirt:867156711251771402>')),
        create_select_option("Inventaire d'Objets",value="3",emoji=getEmojiObject('<:changeAppa:872174182773977108>')),
        create_select_option("Éléments",value="4",emoji=getEmojiObject('<:krysTal:888070310472073257>'))
        ],
    placeholder="Sélectionnez l'inventaire dans lequel vous voulez aller"
        )

returnButton = create_button(2,"Retour",backward_arrow,"return")

changeElemEnable = create_button(1,"Utiliser comme élément principal",getEmojiObject('<:krysTal:888070310472073257>'),"change")
changeElemDisabled = create_button(1,"Utiliser comme élément principal",getEmojiObject('<:krysTal:888070310472073257>'),"change",disabled=True)
changeElemEnable2 = create_button(1,"Utiliser comme élément principal",getEmojiObject('<:krysTal2:907638077307097088>'),"change")
changeElemDisabled2 = create_button(1,"Utiliser comme élément principal",getEmojiObject('<:krysTal2:907638077307097088>'),"change",disabled=True)

changeElemEnable3 = create_button(1,"Utiliser comme élément secondaire",getEmojiObject('<:krysTal:888070310472073257>'),"change2")
changeElemDisabled3 = create_button(1,"Utiliser comme élément secondaire",getEmojiObject('<:krysTal:888070310472073257>'),"change2",disabled=True)
changeElemEnable4 = create_button(1,"Utiliser comme élément secondaire",getEmojiObject('<:krysTal2:907638077307097088>'),"change2")
changeElemDisabled4 = create_button(1,"Utiliser comme élément secondaire",getEmojiObject('<:krysTal2:907638077307097088>'),"change2",disabled=True)

confirmButton = create_button(ButtonStyle.green,"Équiper",check,"confirm")
useMimikator = create_button(ButtonStyle.gray,"Utiliser votre Mimikator",getEmojiObject(mimique.emoji),"mimikator")
hideNonEquip = create_button(ButtonStyle.blue,"Cacher Non équip.",custom_id="hideNoneEquip",emoji=getEmojiObject('<:invisible:899788326691823656>'))
affExclu = create_button(ButtonStyle.green,"Aff. Exclusivité",custom_id="affExclu",emoji=getEmojiObject(matriseElemEff.emoji[0][0]))
affNonEquip = create_button(ButtonStyle.grey,"Aff. Non équip.",custom_id="affNoneEquip",emoji=getEmojiObject("<:noeuil:887743235131322398>"))
allType = create_button(ButtonStyle.gray,"Aff. Tout",custom_id="allDamages",emoji=getEmojiObject('<:targeted:912415337088159744>'))
onlyPhys = create_button(ButtonStyle.success,"Aff. Phy./Corp. un.",custom_id="onlyPhys",emoji=getEmojiObject("<:berkSlash:916210295867850782>"))
onlyMag = create_button(ButtonStyle.blurple,"Aff Mag./Psy. un.",custom_id="onlyMag",emoji=getEmojiObject('<:lizDirectSkill:917202291042435142>'))
affAcc = create_button(ButtonStyle.success,"Aff. Accessoire",getEmojiObject('<:defHead:896928743967301703>'),"acc")
affBody = create_button(ButtonStyle.green,"Aff. Tenue",getEmojiObject('<:defMid:896928729673109535>'),"dress")
affShoes = create_button(ButtonStyle.blue,"Aff. Chaussures",getEmojiObject('<:defShoes:896928709330731018>'),"flats")
affAllStuff = create_button(ButtonStyle.grey,"Aff. Tout",getEmojiObject('<:dualMagie:899628510463803393>'),"all")

affCompMelee = create_button(ButtonStyle.red,"Aff. Comp. Mêlée",getEmojiObject(absorbingStrike.emoji),"melee_ult")
affCompDist = create_button(ButtonStyle.red,"Aff. Comp. Distance",getEmojiObject(absorbingArrow.emoji),"dist_ult")

tablStatsName = nameStats+nameStats2+["Soins","Boost","Armure","Direct","Indirect"]

skillult, skillnonult, skillMono, skillAoe = [], [], [], []
for skilly in skills:
    if skilly.ultimate:
        skillult.append(skilly)
    else:
        skillnonult.append(skilly)
    if skilly.area == AREA_MONO:
        skillMono.append(skilly)
    else:
        skillAoe.append(skilly)

returnAndConfirmActionRow = create_actionrow(returnButton,confirmButton)

def getSortSkillValue(object : skill, wanted : int):
    if wanted in [15,17]:       # Indirect Dmg or Armor
        eff = findEffect(object.effect[0])
        if eff == None:
            eff = findEffect(object.effectOnSelf)
            if (eff == None or (eff != None and eff.type not in [TYPE_INDIRECT_DAMAGE,TYPE_ARMOR])) and object.effectAroundCaster != None:
                eff = findEffect(object.effectAroundCaster[2])
        if eff != None:
            if wanted == 15:
                return eff.power * object.effPowerPurcent/100
            elif wanted == 17:
                return eff.overhealth
        else:
            print("{0} n'a rien a faire dans la catégorie {1} !".format(object.name,["Dégâts indirects","Armure"][int(wanted==17)]))
            return 0
    elif wanted == 14:      # Dmg     
        while not(object.effectOnSelf == None or findEffect(object.effectOnSelf).replica == None):
            object = findSkill(findEffect(object.effectOnSelf).replica)
        if object.type == TYPE_DAMAGE:
            return object.power * object.repetition
        elif object.effectAroundCaster != None:
            return object.effectAroundCaster[2]

    elif wanted == 16:  # Heal
        if object.effect[0] == None:
            while not(object.effectOnSelf == None or findEffect(object.effectOnSelf).replica == None):
                object = findSkill(findEffect(object.effectOnSelf).replica)
            return object.power
        else:
            if object.effect[0] != None:
                return findEffect(object.effect[0]).power
            elif object.effectOnSelf != None:
                return findEffect(object.effectOnSelf).power
            elif object.effectAroundCaster != None:
                return object.effectAroundCaster[2]

    return 0

def changeDefault(select : dict, value : int):
    """Chance the default value from a Select Menu for the selected option"""
    value = str(value)
    temp = copy.deepcopy(select)
    for a in temp["options"]:
        if a["value"] == value:
            a["default"] = True
        elif a["default"] == True:
            a["default"] = False

    return temp

elemOptions = []
for a in range(0,len(elemDesc)):
    elemOptions.append(create_select_option(elemNames[a],str(a),getEmojiObject(elemEmojis[a])))

elemSelect = create_select(elemOptions,placeholder="En savoir plus ou changer d'élément")

async def mimikThat(bot : discord.client, ctx : ComponentContext, msg : discord.Message, user : char, toChange : Union[weapon,stuff]):
    index = type(toChange) == stuff
    
    desc = "Votre {0} prendra l'apparance de __{1} {2}__, voulez vous continuer ?".format(["arme","accessoire"][index],toChange.emoji,toChange.name)
    await msg.edit(embed=discord.Embed(title="__Mimikator :__ {0} {1}".format(toChange.emoji,toChange.name),color=user.color,description=desc),components=[create_actionrow(returnButton,confirmButton)])

    def checkMate(m):
        return int(m.author_id) == int(ctx.author_id)

    try:
        react = await wait_for_component(bot,msg,check=checkMate,timeout=60)
    except:
        return False

    if react.custom_id == "return":
        return False
    else:
        user = loadCharFile("./userProfile/{0}.prof".format(user.owner))
        if index:
            user.apparaAcc = toChange
        else:
            user.apparaWeap = toChange

        user.otherInventory.remove(mimique)
        saveCharFile("./userProfile/{0}.prof".format(user.owner),user)

        await msg.edit(embed=discord.Embed(title="__Mimikator :__ {0} {1}".format(toChange.emoji,toChange.name),color=user.color,description="Votre mimikator a bien été utilisé"),components=[])
        return True

async def compare(bot : discord.client, ctx : ComponentContext, user : char, see : Union[weapon,stuff]):
    if type(see) == stuff:
        toCompare = user.stuff[see.type]
    elif type(see) == weapon:
        toCompare = user.weapon

    embed = discord.Embed(title="__Comparaison : {0} {2} -> {3} {1}__".format(toCompare.name,see.name,toCompare.emoji,see.emoji),color=user.color)
    compBonus = ""
    compMalus = ""
    allStaty = allStatsNames + ["Soins","Boost","Armure","Direct","Indirect"]
    allStatsCompare = toCompare.allStats() + [toCompare.resistance,toCompare.percing,toCompare.critical,toCompare.negativeHeal*-1,toCompare.negativeBoost*-1,toCompare.negativeShield*-1,toCompare.negativeDirect*-1,toCompare.negativeIndirect*-1]
    allStatsSee = see.allStats() + [see.resistance,see.percing,see.critical,see.negativeHeal*-1,see.negativeBoost*-1,see.negativeShield*-1,see.negativeDirect*-1,see.negativeIndirect*-1]

    for cmpt in range(len(allStatsSee)):
        diff = allStatsSee[cmpt] - allStatsCompare[cmpt]
        if diff > 0:
            compBonus += "{0} : **+{1}**\n".format(allStaty[cmpt],diff)
        elif diff < 0:
            compMalus += "{0} : {1}\n".format(allStaty[cmpt],diff)

    if compBonus != "":
        embed.add_field(name="<:empty:866459463568850954>\n__Gains de statistiques :__",value=compBonus,inline=True)
    if compMalus != "":
        embed.add_field(name="<:empty:866459463568850954>\n__Pertes de statistiques :__",value=compMalus,inline=True)

    if type(see) == weapon:
        comp = ""
        tabl1 = ["Puissance","Précision","Nombre de tirs","Portée"]
        tabl2 = [see.power - toCompare.power, see.sussess - toCompare.sussess, see.repetition - toCompare.repetition, see.effectiveRange - toCompare.effectiveRange]

        for cmpt in range(len(tabl1)):
            if tabl2[cmpt] > 0:
                comp += "{0} : +**{1}**\n".format(tabl1[cmpt],tabl2[cmpt])
            else:
                comp += "{0} : {1}\n".format(tabl1[cmpt],tabl2[cmpt])

        comp += "\n"
        if see.use != toCompare.use:
            comp += "Statistique de base : ~~{0}~~ -> {1}\n".format(allStatsNames[toCompare.use],allStatsNames[see.use])

        embed.add_field(name="<:empty:866459463568850954>\n__Différences de puissance :__",value=comp,inline=False)

    # Send
    try:
        await ctx.send(embed=embed,delete_after=30)
    except:
        await ctx.channel.send(embed=embed,delete_after=30)

async def elements(bot : discord.client, ctx : discord.Message, msg : discord.Message, user : classes.char):
    """Function to call for inventory elements.\n
    Edit de Msg for display the actual element of the user and a short description.\n
    Can also change the element if th user have a Elemental Cristal."""

    def check(m):
        return m.author_id == ctx.author.id and m.origin_message.id == msg.id

    def checkSecond(m):
        return m.author_id == ctx.author.id and m.origin_message.id == secondMsg.id

    if user.level < 10: # The user doesn't have the level
        elemEmbed = discord.Embed(title="__Éléments__",color=user.color,description="Les éléments renforcent la spécialisation d'un personnage en augmentant les dégâts qu'il fait suivant certaines conditions définie par l'élément choisi\nLes équipements peuvent également avoir des éléments. Avoir des équipements du même élément que soit accroie un peu leurs statistiques\n")
        elemEmbed.add_field(name="__Contenu verouillé :__",value="Les éléments se débloquent à partir du nieau 10")
        await msg.edit(embed=elemEmbed,components=[])

    else:
        while 1:
            elemEmbed = discord.Embed(title="__Éléments__",color=user.color,description="Les éléments renforcent la spécialisation d'un personnage en augmentant les dégâts qu'il fait suivant certaines conditions définie par l'élément choisi\nLes équipements peuvent également avoir des éléments. Avoir des équipements du même élément que soit accroie un peu leurs statistiques\n")
            elemEmbed.add_field(name="<:em:866459463568850954>\n__Votre élément principal actuel est l'élément **{0}** ({1}) :__".format(elemNames[user.element],elemEmojis[user.element]),value=elemDesc[user.element]+"\n\n**__Passif principal :__\n"+elemMainPassifDesc[user.element]+"**", inline=False)
            if user.level >= 30:
                elemEmbed.add_field(name="<:em:866459463568850954>\n__Votre élément secondaire actuel est l'élément **{0}** ({1}) :__".format(elemNames[user.secElement],elemEmojis[user.secElement]),value=elemDesc[user.secElement]+"\n\n**__Passif secondaire :__\n"+elemSecPassifDesc[user.secElement]+"**", inline=False)
            else:
                elemEmbed.add_field(name="<:em:866459463568850954>\n__Votre élément secondaire actuel est l'élément **{0}** ({1}) :__".format(elemNames[user.secElement],elemEmojis[user.secElement]),value="Vous pourrez changer d'élément secondaire une fois le __niveau 30__ atteint", inline=False)

            await msg.edit(embed = elemEmbed,components=[create_actionrow(elemSelect)])

            try:
                respond = await wait_for_component(bot,msg,check=check,timeout=60)
            except:
                await msg.edit(embed = elemEmbed,components=[])
                break

            resp = int(respond.values[0])
            respEmb = discord.Embed(title = "__Élément : {0}__".format(elemNames[resp]),description = elemDesc[resp]+"\n\n__Passif principal :__\n"+elemMainPassifDesc[resp]+"\n\n__Passif secondaire__\n"+elemSecPassifDesc[resp],color=user.color)

            if resp not in [ELEMENT_LIGHT,ELEMENT_DARKNESS,ELEMENT_SPACE,ELEMENT_TIME]:
                if user.have(elementalCristal) and user.level >= 10:
                    actionrow = create_actionrow(returnButton,changeElemEnable)
                else:
                    respEmb.set_footer(text="Vous ne possédez pas de cristaux élémentaires ou n'avez pas le niveau requis")
                    actionrow = create_actionrow(returnButton,changeElemDisabled)
            else:
                if user.have(dimentioCristal) and user.level >= 20:
                    actionrow = create_actionrow(returnButton,changeElemEnable2)
                else:
                    respEmb.set_footer(text="Vous ne possédez pas de cristaux dimentionnels ou n'avez pas le niveau requis")
                    actionrow = create_actionrow(returnButton,changeElemDisabled2)

            if user.level < 30:
                secElemButton = []
            else:
                if resp in [ELEMENT_LIGHT,ELEMENT_DARKNESS,ELEMENT_SPACE,ELEMENT_TIME]:
                    if user.have(dimentioCristal):
                        secElemButton = [create_actionrow(changeElemEnable4)]
                    else:
                        secElemButton = [create_actionrow(changeElemDisabled4)]
                else:
                    if user.have(elementalCristal):
                        secElemButton = [create_actionrow(changeElemEnable3)]
                    else:
                        secElemButton = [create_actionrow(changeElemDisabled3)]

            try:
                secondMsg = await respond.send(embed = respEmb,components=[actionrow]+secElemButton)
            except:
                secondMsg = await ctx.channel.send(embed = respEmb,components=[actionrow]+secElemButton)

            try:
                respond = await wait_for_component(bot,secondMsg,check=checkSecond,timeout=60)
            except:
                await secondMsg.delete()
                await msg.edit(embed = elemEmbed,components=[])
                break

            if respond.custom_id == "change":
                user.element = resp
                if resp not in [ELEMENT_LIGHT,ELEMENT_DARKNESS,ELEMENT_SPACE,ELEMENT_TIME]:
                    user.otherInventory.remove(elementalCristal)
                else:
                    user.otherInventory.remove(dimentioCristal)
                saveCharFile(absPath+"/userProfile/"+str(user.owner)+".prof",user)
                await secondMsg.edit(embed = discord.Embed(title="__Élément : {0}__".format(elemNames[resp]),description="Votre élément principal a bien été modifié",color=user.color),components=[],delete_after=3)

            elif respond.custom_id == "change2":
                user.secElement = resp
                if resp not in [ELEMENT_LIGHT,ELEMENT_DARKNESS,ELEMENT_SPACE,ELEMENT_TIME]:
                    user.otherInventory.remove(elementalCristal)
                else:
                    user.otherInventory.remove(dimentioCristal)
                saveCharFile(absPath+"/userProfile/"+str(user.owner)+".prof",user)
                await secondMsg.edit(embed = discord.Embed(title="__Élément : {0}__".format(elemNames[resp]),description="Votre élément secondaire a bien été modifié",color=user.color),components=[],delete_after=3)

            else:
                await secondMsg.delete()

async def blablaEdit(bot : discord.client, ctx : discord.Message, msg : discord.Message, user : classes.char):
    pathUserProfile = absPath + "/userProfile/" + str(user.owner) + ".prof"

    def check(m):
        return m.author_id == ctx.author.id and m.origin_message.id == msg.id

    def checkMsg(message):
        return int(message.author.id) == int(ctx.author.id) and int(message.channel.id) == int(msg.channel.id)

    while 1:
        user = loadCharFile(pathUserProfile)
        tablSays = user.says.tabl()
        option = []
        for count in range(len(tablCat)):
            desc = "Aucun message enregistré"
            if tablSays[count] != None:
                if len(tablSays[count]) <= 98:
                    desc = "\"{0}\"".format(tablSays[count])
                else:
                    desc = "\"{0}(...)\"".format(tablSays[count][:93])
            option.append(create_select_option(tablCat[count],str(count),description=desc))

        select = create_select(option,placeholder="Sélectionnez un événement")

        embed = discord.Embed(title="__/inventory says__",color=user.color,description="Vous pouvez enregistrer des messages que votre personnage dira lors de certain événements durant le combat\n\nCertains messages n'apparaitrons pas sistématiquement\n\nVous pouvez modifier autant de message que vous voulez, mais lors que le bot détectera une trop longue inactivité, votre Blablator sera consommé")
        await msg.edit(embed=embed,components=[create_actionrow(select)])

        try:
            respond = await wait_for_component(bot,messages=msg,check=check,timeout=180)
        except:
            break

        select = create_select(option,placeholder="Sélectionnez un événement",disabled=True)
        await msg.edit(embed=embed,components=[create_actionrow(select)])
        repValue = int(respond.values[0])

        if tablSays[repValue] == None:
            desc = "Vous n'avez pas encore enregistré de message pour cet événement"
        else:
            desc = "Le message suivant est enregistré pour cet évémenement :\n\"{0}\"".format(tablSays[repValue])

        desc += "\n\nVeuillez renseigner le nouveau message :"
        if repValue in [1,2,12]:
            desc += "\n\n__Vous pouvez utiliser les balises suivantes pour cette catégorie :__\n{target} : Nom de la cible\n{caster} : Nom du lanceur\n{skill} : Nom de la compétence"
        elif repValue in [3]:
            desc += "\n\n__Vous pouvez utiliser les balises suivantes pour cette catégorie :__\n{target} : Nom de la cible éliminée\n{caster} : Nom du tueur"
        elif repValue in [4,5]:
            desc += "\n\n__Vous pouvez utiliser les balises suivantes pour cette catégorie :__\n{target} : Nom du tueur, réanimateur\n{caster} : Nom de la personne éliminée, réanimée"
        elif repValue in [15]:
            desc += "\n\n__Vous pouvez utiliser les balises suivantes pour cette catégorie :__\n{skill} : Nom de la compétence"
        elif repValue in [16,17]:
            desc += "\n\n__Vous pouvez utiliser les balises suivantes pour cette catégorie :__\n{killer} : Nom du tueur\n{downed} : Nom de la personne éliminée"
        elif repValue in [13,14]:
            desc += "\n\n__Vous pouvez utiliser les balises suivantes pour cette catégorie :__\n{caster} : Nom du réanimateur\n{skill} : Compétence utilisée"

        embed2 = discord.Embed(title = "__/inventory says - {0}__".format(tablCat[repValue]),color=user.color,description=desc)
        reply = await respond.send(embed = embed2)

        try:
            newMessage = await bot.wait_for("message",check=checkMsg,timeout=180)
        except:
            break

        new = newMessage.content
        while new.startswith(" "):
            new = new[1:]
        while new.endswith(" "):
            new = new[:-2]
        tablSays[repValue] = new
        temp = says()
        user.says = temp.fromTabl(tablSays)
        saveCharFile(pathUserProfile,user)
        try:
            await newMessage.delete()
        except:
            print("J'ai pas pu effacer le message :|")
        await reply.edit(embed=discord.Embed(title = "/inventory says - {0}".format(tablCat[repValue]),color=user.color,description="Le message suivant a bien été enregistré pour cet événement :\n{0} : *\"{1}\"*".format(await getUserIcon(bot,user),new)),delete_after=10)

    try:
        user.otherInventory.remove(blablator)
        saveCharFile(pathUserProfile,user)
    except:
        pass

    try:
        await reply.delete()
    except:
        pass

    await msg.edit(embed=discord.Embed(title="/inventory say",color=user.color,description="Votre Blablator a été consommé"))

async def inventory(bot : discord.client, ctx : discord.Message, identifiant : str, delete=False, procur=None):
    """Old function for the user's inventory. Still called when we go a id"""
    oldMsg = None
    if procur != None:
        pathUserProfile = "./userProfile/" + str(procur) + ".prof"
    else:
        pathUserProfile = "./userProfile/" + str(ctx.author.id) + ".prof"

    def checkIsAuthorReact(reaction,user):
        return int(user.id) == int(ctx.author.id) and int(reaction.message.id) == int(oldMsg.id)

    user = loadCharFile(pathUserProfile)
    if user.owner != ctx.author.id:
        if ctx.author.id not in user.procuration:
            try:
                await ctx.send(embed = errorEmbed("__/inventory__",f"{user.name} ne vous a pas donné procuration sur son inventaire"),delete_after=10)
            except:
                await ctx.channel.send(embed = errorEmbed("__/inventory__",f"{user.name} ne vous a pas donné procuration sur son inventaire"),delete_after=10)
            return 0

    if oldMsg == None:
        try:
            oldMsg = await ctx.send(embed = discord.Embed(title = "/inventory", description = emoji.loading))
        except:
            oldMsg = await ctx.channel.send(embed = discord.Embed(title = "/inventory", description = emoji.loading))
    inv = whatIsThat(identifiant)
    if inv != None:
        if inv == 0:                # Weapon
            weap = findWeapon(identifiant)
            emb = infoWeapon(weap,user,ctx)
            
            trouv = False
            for a in user.weaponInventory:
                if a.id == identifiant or a.name.lower() == identifiant.lower():
                    trouv = True

            if not(trouv):
                emb.set_footer(text = "Vous ne possédez pas cette arme")
                if delete:
                    await oldMsg.edit(embed = emb,components=[],delete_after=60)
                else:
                    await oldMsg.edit(embed = emb,components=[])
            elif weap == user.weapon:
                emb.set_footer(text = "Vous utilisez déjà cette arme")
                if delete:
                    await oldMsg.edit(embed = emb,components=[])
                else:
                    await oldMsg.edit(embed = emb,components=[])
            else:
                emb.set_footer(text = "Cliquez sur l'icone de l'arme pour l'équiper")
                compareButton = create_button(ButtonStyle.grey,"Comparer",getEmojiObject(user.weapon.emoji),custom_id="compare")
                if user.have(mimique):
                    toAdd = [create_actionrow(useMimikator)]
                else:
                    toAdd = []
                await oldMsg.edit(embed = emb,components=[returnAndConfirmActionRow,create_actionrow(compareButton)]+toAdd)

                def check(m):
                    return m.author_id == ctx.author.id and m.origin_message.id == oldMsg.id

                while 1:
                    try:
                        rep = await wait_for_component(bot,timeout=60,check=check,messages=oldMsg)
                    except:
                        try:
                            if delete :
                                await oldMsg.delete()
                            else:
                                await oldMsg.edit(embed = emb,components=[])
                        except:
                            pass
                        break

                    if rep.custom_id == "confirm":
                        user.weapon = weap
                        if saveCharFile(pathUserProfile,user):
                            await oldMsg.edit(embed = discord.Embed(title = "__/inventory__",color = user.color,description = "Votre nouvelle équipement a bien été équipée"),components=[create_actionrow(create_select([create_select_option(unhyperlink(weap.name),"bidule",getEmojiObject(weap.emoji),default=True)],disabled=True))],delete_after=5)
                        else:
                            await oldMsg.edit(embed = errorEmbed("Erreur","Une erreur est survenue. La modification a pas été enregistrée"))
                        break
                    elif rep.custom_id == "compare":
                        await compare(bot,rep,user,weap)
                    elif rep.custom_id == "return":
                        if delete :
                            await oldMsg.delete()
                        else:
                            await oldMsg.edit(embed = emb,components=[])
                        break
                    elif rep.custom_id == "mimikator":
                        var = await mimikThat(bot,ctx,oldMsg,user,weap)
                        break

        elif inv == 1:              # Skills
            invSkill = findSkill(identifiant)
            emb = infoSkill(invSkill,user,ctx)
            emb = infoSkill(invSkill,user,ctx)

            ballerine=True
            if invSkill.group != 0:
                for skilly in user.skills:
                    if type(skilly) == skill and skilly.group not in [0,invSkill.group]:
                        ballerine = False
                        break

            if invSkill not in user.skillInventory:
                emb.set_footer(text = "Vous ne possédez pas cette compétence")
                if delete:
                    await oldMsg.edit(embed = emb,components=[],delete_after=60)
                else:
                    await oldMsg.edit(embed = emb,components=[])
            elif invSkill in user.skills:
                emb.set_footer(text = "Vous avez déjà équipé cette compétence. Voulez vous la déséquiper ?")
                await oldMsg.edit(embed = emb,components=[returnAndConfirmActionRow])

                def check(m):
                    return m.author_id == ctx.author.id and m.origin_message.id == oldMsg.id

                try:
                    rep = await wait_for_component(bot,timeout=60,check=check,messages=oldMsg)
                except:
                    if delete:
                        await oldMsg.delete()
                    else:
                        await oldMsg.edit(embed = emb,components=[])
                    return 0

                if rep.custom_id == "confirm":
                    for a in range(0,7):
                        if user.skills[a] == invSkill:
                            user.skills[a] = "0"
                            break

                    saveCharFile(pathUserProfile,user)
                    await oldMsg.edit(embed = discord.Embed(title="Inventory",color=user.color,description="Votre compétence a bien été déséquipée"),delete_after=5,components=[])
                else:
                    if delete:
                        await oldMsg.delete()
                    else:
                        await oldMsg.edit(embed = emb,components=[])
                    return 0
            elif not(ballerine):
                emb.set_footer(text = "Vous utilisez déjà une compétence du groupe opposé")
                if delete:
                    await oldMsg.edit(embed = emb,components=[],delete_after=60)
                else:
                    await oldMsg.edit(embed = emb,components=[])
            elif not(invSkill.havConds(user=user)):
                emb.set_footer(text = "Vous ne respectez pas les conditions de cette compétence")
                if delete:
                    await oldMsg.edit(embed = emb,components=[],delete_after=60)
                else:
                    await oldMsg.edit(embed = emb,components=[])
            else:
                hasUltimate=False
                for a in [0,1,2,3,4,5,6]:
                    if type(user.skills[a]) == skill:
                        if user.skills[a].ultimate and invSkill.ultimate:
                            hasUltimate=True
                            break
                options = []
        
                if user.level < 5:
                    addPerLevel = []
                elif user.level < 15:
                    addPerLevel = [3]
                elif user.level < 25:
                    addPerLevel = [3,4]
                elif user.level < 35:
                    addPerLevel = [3,4,5]
                else:
                    addPerLevel = [3,4,5,6]

                skillWithLevel = []
                for slotNb in range(len(lvlToUnlockSkill)):
                    if user.level >= lvlToUnlockSkill[slotNb]:
                        skillWithLevel.append(slotNb)


                for comp in skillWithLevel:
                    if type(user.skills[comp]) == skill:
                        ultimatum = ""
                        if user.skills[comp].ultimate:
                            ultimatum = "Capacité ultime - "
                        if hasUltimate and user.skills[comp].ultimate and invSkill.ultimate:
                            options += [create_select_option(user.skills[comp].name,user.skills[comp].id,getEmojiObject(user.skills[comp].emoji),ultimatum+tablTypeStr[user.skills[comp].type])]
                        elif not(hasUltimate):
                            options += [create_select_option(user.skills[comp].name,user.skills[comp].id,getEmojiObject(user.skills[comp].emoji),ultimatum+tablTypeStr[user.skills[comp].type])]
                    elif not(hasUltimate):
                        options += [create_select_option(f"Slot de compétence vide",str(comp+1),emoji.count[comp+1])]

                select = create_select(options,placeholder="Sélectionnez un emplacement")

                emb.set_footer(text = "Cliquez sur l'icone d'emplacement pour équiper")
                await oldMsg.edit(embed = emb,components=[create_actionrow(returnButton),create_actionrow(select)])
                def check(m):
                    return m.author_id == ctx.author.id and m.origin_message.id == oldMsg.id
                react = None
                try:
                    react = await wait_for_component(bot,messages=oldMsg,timeout=60,check=check)
                except:
                    if delete :
                        await oldMsg.delete()
                    else:
                        await oldMsg.edit(embed = emb,components=[])

                if react != None:
                    try:
                        await oldMsg.edit(embed = emb,components=[create_actionrow(getChoisenSelect(select,react.values[0]))])

                        for a in [0,1,2,3,4,5,6]:
                            ballerine,babie = False,react.values[0] == str(a+1)
                            if type(user.skills[a]) == skill:
                                ballerine = react.values[0] == user.skills[a].id

                            if babie or ballerine:
                                try:
                                    user.skills[a] = invSkill
                                    saveCharFile(pathUserProfile,user)
                                    await oldMsg.edit(embed = discord.Embed(title = "__/inventory__",color = user.color,description="Vous avez bien équipé votre compétence !",components=[create_actionrow(create_select([create_select_option(unhyperlink(invSkill.name),"bidule",getEmojiObject(invSkill.emoji),default=True)],disabled=True))]),delete_after=5)
                                except:
                                    await oldMsg.edit(embed = errorEmbed("__/inventory__","Une erreur est survenue",components=[]))
                                break
                    except:
                        await oldMsg.delete()

        elif inv == 2:              # Stuff
            invStuff = findStuff(identifiant)
            emb = infoStuff(invStuff,user,ctx)

            trouv = False
            for a in user.stuffInventory:
                if a.id == identifiant or a.name.lower() == identifiant.lower():
                    trouv = True

            if not(trouv):
                emb.set_footer(text = "Vous ne possédez pas cet équipement")
                if delete:
                    await oldMsg.edit(embed = emb,components=[],delete_after=60)
                else:
                    await oldMsg.edit(embed = emb,components=[])

            elif invStuff == user.stuff[invStuff.type]:
                emb.set_footer(text = "Vous portez déjà cet équipement")
                if delete:
                    await oldMsg.edit(embed = emb,components=[],delete_after=60)
                else:
                    await oldMsg.edit(embed = emb,components=[])
                
            elif invStuff.minLvl > user.level:
                emb.set_footer(text = "Cet équipement donne trop de statistiques pour votre niveau")
                if delete:
                    await oldMsg.edit(embed = emb,components=[],delete_after=60)
                else:
                    await oldMsg.edit(embed = emb,components=[])

            else:
                emb.set_footer(text = "Cliquez sur l'icone de l'équipement pour l'équiper")
                compareButton = create_button(ButtonStyle.grey,"Comparer",getEmojiObject(user.stuff[invStuff.type].emoji),custom_id="compare")
                if user.have(mimique) and invStuff.type == 0:
                    toAdd = [create_actionrow(useMimikator)]
                else:
                    toAdd = []
                await oldMsg.edit(embed = emb,components=[returnAndConfirmActionRow,create_actionrow(compareButton)]+toAdd)

                def check(m):
                    return m.author_id == ctx.author.id and m.origin_message.id == oldMsg.id

                while 1:
                    try:
                        rep = await wait_for_component(bot,timeout=60,check=check,messages=oldMsg)
                    except:
                        if delete :
                            try:
                                await oldMsg.delete()
                            except:
                                pass

                        else:
                            try:
                                await oldMsg.edit(embed = emb,components=[])
                            except:
                                pass
                        break

                    if rep.custom_id == "confirm":
                        user.stuff[invStuff.type] = invStuff
                        if saveCharFile(pathUserProfile,user):
                            await oldMsg.edit(embed = discord.Embed(title = "__/inventory__",color = user.color,description = "Votre nouvelle équipement a bien été équipée"),components=[create_actionrow(create_select([create_select_option(unhyperlink(invStuff.name),"bidule",getEmojiObject(invStuff.emoji),default=True)],disabled=True))],delete_after=5)
                        else:
                            await oldMsg.edit(embed = errorEmbed("Erreur","Une erreur est survenue. La modification a pas été enregistrée"))
                        break
                    elif rep.custom_id == "compare":
                        await compare(bot,rep,user,invStuff)
                    elif rep.custom_id == "return":
                        if delete :
                            await oldMsg.delete()
                        else:
                            await oldMsg.edit(embed = emb,components=[])
                        break
                    elif rep.custom_id == "mimikator":
                        var = await mimikThat(bot,ctx,oldMsg,user,invStuff)
                        break

        elif inv == 3:              # Other
            obj = findOther(identifiant)
            emb = infoOther(obj,user)

            if obj == autoPoint:
                emb.add_field(name ='<:empty:866459463568850954>\n__Status de votre {0} :__'.format(obj.name),value=["Activé","Désactivé"][not(user.autoPoint)],inline=False)
                emb.add_field(name ='<:empty:866459463568850954>\n__Statistiques recommandées pour votre aspiration :__',value="{0}\n{1}".format(nameStats[recommandedStat[user.aspiration][0]],nameStats[recommandedStat[user.aspiration][1]]),inline=False)

            if obj == autoStuff:
                emb.add_field(name ='<:empty:866459463568850954>\n__Status de votre {0} :__'.format(obj.name),value=["Activé","Désactivé"][not(user.autoStuff)],inline=False)
                emb.add_field(name ='<:empty:866459463568850954>\n__Statistiques recommandées pour votre aspiration :__',value="{0}\n{1}\n{2}".format(tablStatsName[recommandedStuffStat[user.aspiration][0]],tablStatsName[recommandedStuffStat[user.aspiration][1]],tablStatsName[recommandedStuffStat[user.aspiration][2]]),inline=False)

            trouv = False
            for a in user.otherInventory:
                if a.id == identifiant or a.name.lower() == identifiant.lower():
                    trouv = True

            if not(trouv):
                emb.set_footer(text = "Vous ne possédez pas cet objet")
                await oldMsg.edit(embed = emb,components=[])

            else:
                if obj != elementalCristal:
                    emb.set_footer(text = "Cliquez sur l'icone de l'objet l'utiliser")
                else:
                    emb.set_footer(text = "Cet objet s'utilise avec /inventory destination: Élément")

                await oldMsg.edit(embed = emb,components=[])
                if obj not in [elementalCristal,dimentioCristal,mimique]:
                    await oldMsg.add_reaction(obj.emoji)

                def checkisReaction(reaction, user):
                    return int(user.id) == int(ctx.author.id) and str(reaction.emoji) ==  obj.emoji

                try:
                    await bot.wait_for("reaction_add",timeout=60,check=checkisReaction)
                    await oldMsg.clear_reactions()
                except asyncio.TimeoutError:
                    await oldMsg.clear_reactions()
                    return 0

                if obj==changeAspi:
                    try:
                        user.aspiration = await chooseAspiration(bot,oldMsg,ctx,user)
                        if user.aspiration != None:
                            user = restats(user)

                            user.otherInventory.remove(changeAspi)
                            if saveCharFile(pathUserProfile,user):
                                
                                await oldMsg.edit(embed = discord.Embed(title = "__/inventory__",color = user.color,description = "Votre nouvelle aspiration a bien été prise en compte et vous avez récupéré vos points bonus"))
                            else:
                                
                                await oldMsg.edit(embed = errorEmbed("__/inventory__","Une erreure est survenue"))
                    except:
                        await oldMsg.edit(embed = errorEmbed("__/inventory__","Une erreure est survenue"))
                elif obj==changeAppa:
                    
                    await oldMsg.edit(embed = discord.Embed(title = "__/inventory__" + " : Espèce",color = light_blue,description = f"Sélectionnez l'espèce de votre personnage :\n\n<:ikaLBlue:866459302319226910> Inkling\n<:takoLBlue:866459095875190804> Octaling\n\nL'espèce n'a aucune influence sur les statistiques du personnage."))
                    await oldMsg.add_reaction('<:ikaLBlue:866459302319226910>')
                    await oldMsg.add_reaction('<:takoLBlue:866459095875190804>')

                    def checkIsAuthorReact1(reaction,user):
                        return int(user.id) == int(ctx.author.id) and int(reaction.message.id) == int(oldMsg.id) and (str(reaction)=='<:ikaLBlue:866459302319226910>' or str(reaction) == '<:takoLBlue:866459095875190804>')

                    respond = await bot.wait_for("reaction_add",timeout = 60,check = checkIsAuthorReact1)

                    if str(respond[0]) == '<:ikaLBlue:866459302319226910>':
                        user.species = 1
                    else:
                        user.species = 2
                    
                    await oldMsg.clear_reactions()
                    await oldMsg.edit(embed = discord.Embed(title = "__/inventory__" + " : Genre",color = light_blue,description = f"Renseignez (ou non) le genre personnage :\nLe genre du personnage n'a aucune incidences sur ses statistiques\n"))
                    await oldMsg.add_reaction('♂️')
                    await oldMsg.add_reaction('♀️')
                    await oldMsg.add_reaction(emoji.forward_arrow)

                    def checkIsAuthorReact(reaction,user):
                        return int(user.id) == int(ctx.author.id) and int(reaction.message.id) == int(oldMsg.id) and (str(reaction)=='♀️' or str(reaction) == '♂️' or str(reaction) == emoji.forward_arrow)

                    respond = await bot.wait_for("reaction_add",timeout = 60,check = checkIsAuthorReact)
                    testouille,titouille = [GENDER_MALE,GENDER_FEMALE,GENDER_OTHER],['♂️','♀️',emoji.forward_arrow]
                    for a in range(0,len(titouille)):
                        if str(respond[0]) == titouille[a]:
                            user.gender = testouille[a]

                    user = await chooseColor(bot,oldMsg,ctx,user)

                    if user != False:
                        user.otherInventory.remove(changeAppa)
                        saveCharFile(pathUserProfile,user)
                        
                        await oldMsg.edit(embed = discord.Embed(title="Changement d'apparence",color = user.color,description="Votre changement a bien été pris en compte !"),components = [])
                elif obj==changeName: 
                    
                    await oldMsg.edit(embed = discord.Embed(title = "__/inventory__" + " : Nom",color = light_blue,description = f"Ecrivez le nom de votre personnage :\n\nVous ne pourrez pas modifier le nom de votre personnage par la suite"))
                    timeout = False
                    def checkIsAuthor(message):
                        return int(ctx.author.id) == int(message.author.id)
                    try:
                        respond = await bot.wait_for("message",timeout = 60,check = checkIsAuthor)
                    except:
                        timeout = True

                    if not(timeout):    
                        user.name = respond.content
                        user.otherInventory.remove(changeName)

                        try:
                            await respond.delete()
                        except:
                            pass

                        saveCharFile(pathUserProfile,user)
                        
                        await oldMsg.edit(embed = discord.Embed(title="Changement de nom",color = user.color,description="Votre changement a bien été pris en compte !",components=[]))
                    else:
                        await oldMsg.add_reaction('🕛')
                elif obj==restat:
                    
                    restats(user)
                    user.otherInventory.remove(restat)

                    saveCharFile(pathUserProfile,user)
                    
                    await oldMsg.edit(embed = discord.Embed(title="Rénitialisation des points bonus",color = user.color,description=f"Votre changement a bien été pris en compte !\nVous avez {user.points} à distribuer avec la commande \"points\""))
                elif obj==customColor:
                    user = await changeCustomColor(bot,oldMsg,ctx,user)
                    if user != None:
                        user.otherInventory.remove(customColor)
                        saveCharFile(pathUserProfile,user)
                        
                        await oldMsg.edit(embed = discord.Embed(title="Couleur personnalisée",description="Votre couleur a bien été enregistrée\n\nCelle-ci sera appliquée à votre icone lors de sa prochaine modification",color=user.color))
                elif obj==blablator:
                    await blablaEdit(bot,ctx,oldMsg,user)
                elif obj in changeIconForm:
                    for cmpt in range(len(changeIconForm)):
                        if changeIconForm[cmpt] == obj:
                            if user.iconForm != cmpt:
                                user.iconForm = cmpt
                                user.otherInventory.remove(obj)
                                saveCharFile(user=user)
                                await oldMsg.edit(embed=discord.Embed(title="__/inventory__",color=user.color,description="Votre {0} a bien été utilisé".format(obj.name)).set_image(url="https://cdn.discordapp.com/emojis/{0}.png".format(getEmojiObject(await getUserIcon(bot,user))["id"])))
                            else:
                                await oldMsg.edit(embed=discord.Embed(title="__/inventory__",color=user.color,description="Vous utilisez déjà cette forme d'icon"))
                            break
                elif obj==autoPoint:
                    if user.autoPoint:
                        user.autoPoint = False
                        user.otherInventory.remove(obj)
                        saveCharFile(user=user)
                        await oldMsg.edit(embed=discord.Embed(title="__Pai'rte de Nheur'o'Nes :__",color=user.color,description="Votre Pai'rte de Nheur'o'Nes a été désactivé"))
                    elif user.stars > 0:
                        user.autoPoint = True
                        user.otherInventory.remove(obj)
                        saveCharFile(user=user)
                        await oldMsg.edit(embed=discord.Embed(title="__Pai'rte de Nheur'o'Nes :__",color=user.color,description="Votre Pai'rte de Nheur'o'Nes a bien été activé.\n\n__Vos futurs points bonus seront attribués aux statistiques suivantes :__\n{0}\n{1}".format(nameStats[recommandedStat[user.aspiration][0]],nameStats[recommandedStat[user.aspiration][1]])))
                    else:
                        await oldMsg.edit(embed=discord.Embed(title="__Pai'rte de Nheur'o'Nes :__",color=user.color,description="Vous n'avez pas le niveau requis pour utiliser cet objet"))
                elif obj==autoStuff:
                    if user.autoStuff:
                        user.autoStuff = False
                        user.otherInventory.remove(obj)
                        saveCharFile(user=user)
                        await oldMsg.edit(embed=discord.Embed(title="__Garde-robe de la Fée Niante :__",color=user.color,description="Votre Garde-robe de la Fée Niante a été désactivé"))
                    elif user.stars > 0:
                        user.autoStuff = True
                        user.otherInventory.remove(obj)
                        saveCharFile(user=user)
                        await oldMsg.edit(embed=discord.Embed(title="__Garde-robe de la Fée Niante :__",color=user.color,description="Votre Garde-robe de la Fée Niante a bien été activé.\n\n__Vos futurs équipements seront sélectionnés selon les statistiques suivantes :__\n{0}\n{1}\n{2}".format(tablStatsName[recommandedStuffStat[user.aspiration][0]],tablStatsName[recommandedStuffStat[user.aspiration][1]],tablStatsName[recommandedStuffStat[user.aspiration][2]])))
                    else:
                        await oldMsg.edit(embed=discord.Embed(title="_Garde-robe de la Fée Niante :__",color=user.color,description="Vous n'avez pas le niveau requis pour utiliser cet objet"))
                await oldMsg.clear_reactions()

async def inventoryV2(bot : discord.client,ctx : discord_slash.SlashContext ,destination : int ,user : classes.char):
    """New function for the user's inventory. Heavely copied from encyclopedia"""
    if destination == 4:
        msg = await ctx.send(embed = discord.Embed(title=randomWaitingMsg[random.randint(0,len(randomWaitingMsg)-1)]))
        await elements(bot,ctx,msg,user)
    else:
        def check(m):
            return m.author_id == ctx.author.id and m.origin_message.id == msg.id

        msg = None
        opValues=["equipement","armes","competences","autre"]
        tri = 0
        needRemake, stuffStatus, hideUlt, affMono, stuffMenuStatus = True, 0, 0, 0, 0, 

        affult = create_button(ButtonStyle.green,"Aff. tout type",getEmojiObject(skillult[random.randint(0,len(skillult)-1)].emoji),"aff_ult")
        hideult = create_button(ButtonStyle.blue,"Cacher Ultimes",getEmojiObject(skillnonult[random.randint(0,len(skillnonult)-1)].emoji),"hide_ult")
        affonlyult = create_button(ButtonStyle.grey,"Aff. seulement Ult.",getEmojiObject(skillult[random.randint(0,len(skillult)-1)].emoji),"affonly_ult")
        tablShowUltButton = [affult,hideult,affonlyult,affCompMelee,affCompDist]
        affmono = create_button(ButtonStyle.green,"Aff. comp. monocibles",getEmojiObject(skillMono[random.randint(0,len(skillMono)-1)].emoji),"mono_area")
        affaoe = create_button(ButtonStyle.blue,"Aff. comp. Zone",getEmojiObject(skillAoe[random.randint(0,len(skillAoe)-1)].emoji),"aoe_area")
        affallarea = create_button(ButtonStyle.grey,"Aff. toutes zones",getEmojiObject(skills[random.randint(0,len(skills)-1)].emoji),"all_area")
        tablSkillArea = [affmono,affaoe,affallarea]

        listUserProcure = [user]
        for a in user.haveProcurOn:
            listUserProcure.append(loadCharFile("./userProfile/{0}.prof".format(a)))
        
        mainUser = loadCharFile("./userProfile/{0}.prof".format(ctx.author_id))
        def userSortValue(user):
            if user.owner == mainUser.owner:
                return 2
            elif user.team == mainUser.team and user.team != 0:
                return 1
            else:
                return 0
        listUserProcure.sort(key=lambda ballerine: userSortValue(ballerine),reverse=True)

        if len(listUserProcure) > 24:
            listUserProcure = listUserProcure[:24]

        affAll,stuffAff,statsToAff,stuffToAff = 0,False,0,0
        while 1:
            if len(listUserProcure) > 0:
                procurOptions = []
                for a in listUserProcure:
                    ilevel = (a.stuff[0].minLvl + a.stuff[1].minLvl + a.stuff[2].minLvl)//3
                    procurOptions.append(create_select_option(a.name,"user_{0}".format(a.owner),getEmojiObject(await getUserIcon(bot,a)),default=a.owner == user.owner,description="Niveau {0}, Niv. Equip. {1}".format(a.level, ilevel)))
                procurSelect = [create_actionrow(create_select(procurOptions))]
            else:
                procurSelect = []

            catSelect = create_select(
                [
                    create_select_option("Equipements","cat_0",getEmojiObject('<:uniform:866830066008981534>'),default=destination==0),
                    create_select_option("Armes","cat_1",getEmojiObject('<:kcharger:870870886939508737>'),default=destination==1),
                    create_select_option("Compétences","cat_2",getEmojiObject('<:stingray:899243721378390036>'),default=destination==2)
                ],
                placeholder="Changer de catégorie d'objets"
            )
            user = loadCharFile(absPath + "/userProfile/" + str(user.owner) + ".prof")
            for a in range(len(listUserProcure)):
                if listUserProcure[a].owner == user.owner:
                    listUserProcure[a] = user
                    break

            userIconThub = getEmojiObject(await getUserIcon(bot,user))["id"]
            options = [
                create_select_option("Ordre Alphabétique ↓","0",'🇦',default=0==tri or(tri > 3 and destination > 3 and destination != 9)),
                create_select_option("Ordre Alphabétique ↑","1",'🇿',default=1==tri)
            ]

            if destination in [0,1]:
                options+=[
                    [
                        create_select_option("Force","4",'💪',default=4==tri),
                        create_select_option("Endurance","5",'🏃',default=5==tri),
                        create_select_option("Charisme",'6','💃',default=6==tri),
                        create_select_option("Agilité","7",'🤸',default=7==tri),
                        create_select_option("Précision","8",'🏹',default=8==tri),
                        create_select_option("Intelligence","9",'🎓',default=9==tri),
                        create_select_option("Magie","10",'🧙',default=10==tri),
                        create_select_option("Résistance","11",'🛡️',default=11==tri),
                        create_select_option("Pénétration","12",'🗡️',default=12==tri),
                        create_select_option("Critique","13",'🎲',default=13==tri),
                        create_select_option("Soins","14",getEmojiObject('<:cure:925190515845132341>'),default=14==tri),
                        create_select_option("Boost","15",getEmojiObject('<:dyna:932618114892439613>'),default=15==tri),
                        create_select_option("Armures","16",getEmojiObject('<:inkArmor:866829950463246346>'),default=16==tri),
                        create_select_option("Directs","17",getEmojiObject('<:splatbomb:873527088286687272>'),default=17==tri),
                        create_select_option("Indirects","18",getEmojiObject('<:estabistia:883123793730609172>'),default=18==tri),
                        create_select_option("Autre cat.","autCat_1","➡️")
                    ],
                    [
                        create_select_option("Cat. classiques","autCat_0","⬅️"),
                        create_select_option("For. - Pré.","22",getEmojiObject('<:lightBlue:933728207453163590>'),default=22==tri),
                        create_select_option("For. - Agi.","23",getEmojiObject('<:green:933734508317003846>'),default=23==tri),
                        create_select_option("Endur. - For.","24",getEmojiObject('<:black:933728357152096277>'),default=24==tri),
                        create_select_option("Endur. - Mag.","25",getEmojiObject('<:orangeBatEarRing:938496708554416168>'),default=25==tri),
                        create_select_option("Endur. - Soins / Char.","26",getEmojiObject('<:apGreenBatEar:938496729718849546>'),default=26==tri),
                        create_select_option("Endur. - Intel. / Arm.","27",getEmojiObject('<:darkblue:933728323455045672>'),default=27==tri),
                        create_select_option("Char. - Soins","28",getEmojiObject('<:white:933785500257513472>'),default=28==tri),
                        create_select_option("Char. - Boost","29",getEmojiObject('<:pink:933728188754980904>'),default=29==tri),
                        create_select_option("Intel. - Arm.","30",getEmojiObject('<:blue:933728247995305994>'),default=30==tri),
                        create_select_option("Intel. - Boost","31",getEmojiObject('<:yellowBatER:937740799150555148>'),default=31==tri),
                        create_select_option("Mag. - Préc.","32",getEmojiObject('<:red:933728281289715782> '),default=32==tri),
                    ]
                ][stuffMenuStatus]

            elif destination == 2:
                options+=[
                    create_select_option("Dégâts","14",getEmojiObject('<:meteor:904164411990749194>'),default=14==tri),
                    create_select_option("Dégâts indirects","15",getEmojiObject('<:tentamissile:884757344397951026>'),default=15==tri),
                    create_select_option("Soins","16",getEmojiObject('<:AdL:873548073769533470>'),default=16==tri),
                    create_select_option("Armure","17",getEmojiObject('<:orbeDef:873725544427053076>'),default=17==tri),
                    create_select_option("Boost",'18',getEmojiObject('<:bpotion:867165268911849522>'),default=18==tri),
                    create_select_option("Malus","19",getEmojiObject('<:nostalgia:867162802783649802>'),default=19==tri),
                    create_select_option("Invocation","20",getEmojiObject('<:sprink1:887747751339757599>'),default=20==tri),
                    create_select_option("Passif","21",getEmojiObject('<:IdoOH:909278546172719184>'),default=21==20)
                ]

            sortOptions = create_select(options,placeholder=["Trier par statistique","Afficher une catégorie en particulier"][destination == 2])

            if needRemake:
                tablToSee = []
                if destination == 0:
                    tablToSee = user.stuffInventory
                    if not(stuffAff) or stuffToAff > 0:
                        for a in tablToSee[:]:
                            if not(stuffAff) and not(a.havConds(user)):
                                tablToSee.remove(a)
                            elif stuffToAff > 0 and a.type != stuffToAff-1:
                                tablToSee.remove(a)

                elif destination == 1:
                    tablToSee = user.weaponInventory
                elif destination == 2:
                    tablToSee = user.skillInventory
                    if tri >= 14:
                        typeTabl = [TYPE_DAMAGE,TYPE_INDIRECT_DAMAGE,[TYPE_HEAL,TYPE_INDIRECT_HEAL,TYPE_RESURECTION,TYPE_INDIRECT_REZ],TYPE_ARMOR,TYPE_BOOST,TYPE_MALUS,TYPE_SUMMON,TYPE_PASSIVE]
                        see = typeTabl[tri-14]
                        if type(see) != list:
                            for ski in tablToSee[:]:
                                if (see != TYPE_BOOST and not(ski.type == see or (ski.effect != [None] and findEffect(ski.effect[0]).type == see) or (ski.effectAroundCaster != None and ski.effectAroundCaster[0] == see) or (ski.effectOnSelf != None and findEffect(ski.effectOnSelf).type == see))) or (see == TYPE_BOOST and ski.type != TYPE_BOOST):
                                    tablToSee.remove(ski)

                        else:
                            for ski in tablToSee[:]:
                                if not(ski.type in see or (ski.effect != [None] and findEffect(ski.effect[0]).type in see) or (ski.effectAroundCaster != None and ski.effectAroundCaster[0] in see) or (ski.effectOnSelf != None and findEffect(ski.effectOnSelf).type in see)):
                                    tablToSee.remove(ski)

                    if affAll==0:
                        for a in tablToSee[:]:
                            if not(a.havConds(user)):
                                tablToSee.remove(a)
                    elif affAll == 1:
                        for a in tablToSee[:]:
                            if not(a.havConds(user)) or a.condition == []:
                                tablToSee.remove(a)

                    if statsToAff > 0:
                        for skilly in tablToSee[:]:
                            if skilly.use not in [[STRENGTH,AGILITY,PRECISION],[MAGIE,CHARISMA,INTELLIGENCE]][statsToAff-1]:
                                tablToSee.remove(skilly)
                    if hideUlt == 1:
                        for skilly in tablToSee[:]:
                            if skilly.ultimate:
                                tablToSee.remove(skilly)
                    elif hideUlt == 2:
                        for skilly in tablToSee[:]:
                            if not skilly.ultimate:
                                tablToSee.remove(skilly)
                    elif hideUlt == 3:
                        for skilly in tablToSee[:]:
                            if skilly.ultimate or skilly.range not in areaMelee+areaMixte:
                                tablToSee.remove(skilly)
                    elif hideUlt == 4:
                        for skilly in tablToSee[:]:
                            if skilly.ultimate or skilly.range not in areaDist+areaMixte:
                                tablToSee.remove(skilly)
                    if affMono == 1:
                        for skilly in tablToSee[:]:
                            if skilly.area != AREA_MONO:
                                tablToSee.remove(skilly)
                    elif affMono == 2:
                        for skilly in tablToSee[:]:
                            if skilly.area == AREA_MONO:
                                tablToSee.remove(skilly)

                    if tri in [14,16]:
                        tablToSee.sort(key=lambda ballerine:getSortSkillValue(ballerine,tri),reverse=True)
                    elif tri in [15]:
                        tablToSee.sort(key=lambda ballerine:getSortSkillValue(ballerine,tri),reverse=True)
                    elif tri in [17]:
                        tablToSee.sort(key=lambda ballerine:getSortSkillValue(ballerine,tri),reverse=True)

                elif destination == 3:
                    tablToSee = user.otherInventory

                if destination in [0,1]:
                    tablToSee.sort(key=lambda ballerine:ballerine.name, reverse=tri)
                    if tri in [2,3]:
                        tablToSee.sort(key=lambda ballerine:user.have(ballerine), reverse=not(tri-2))
                    elif tri == 4:
                        tablToSee.sort(key=lambda ballerine:ballerine.strength + max(ballerine.negativeDirect *-1,ballerine.negativeIndirect *-1), reverse=True)
                    elif tri == 5:
                        tablToSee.sort(key=lambda ballerine:ballerine.endurance, reverse=True)
                    elif tri == 6:
                        tablToSee.sort(key=lambda ballerine:ballerine.charisma + max(ballerine.negativeHeal *-1,ballerine.negativeBoost *-1), reverse=True)
                    elif tri == 7:
                        tablToSee.sort(key=lambda ballerine:ballerine.agility, reverse=True)
                    elif tri == 8:
                        tablToSee.sort(key=lambda ballerine:ballerine.precision, reverse=True)
                    elif tri == 9:
                        tablToSee.sort(key=lambda ballerine:ballerine.intelligence + max(ballerine.negativeShield *-1,ballerine.negativeBoost *-1), reverse=True)
                    elif tri == 10:
                        tablToSee.sort(key=lambda ballerine:ballerine.magie + max(ballerine.negativeDirect *-1,ballerine.negativeIndirect *-1), reverse=True)
                    elif tri == 11:
                        tablToSee.sort(key=lambda ballerine:ballerine.resistance, reverse=True)
                    elif tri == 12:
                        tablToSee.sort(key=lambda ballerine:ballerine.percing, reverse=True)
                    elif tri == 13:
                        tablToSee.sort(key=lambda ballerine:ballerine.critical, reverse=True)
                    elif tri == 14:
                        tablToSee.sort(key=lambda ballerine:-ballerine.negativeHeal + ballerine.charisma, reverse=True)
                    elif tri == 15:
                        tablToSee.sort(key=lambda ballerine:-ballerine.negativeBoost + max(ballerine.charisma,ballerine.intelligence), reverse=True)
                    elif tri == 16:
                        tablToSee.sort(key=lambda ballerine:-ballerine.negativeShield + ballerine.intelligence, reverse=True)
                    elif tri == 17:
                        tablToSee.sort(key=lambda ballerine:-ballerine.negativeDirect + max(ballerine.magie,ballerine.strength), reverse=True)
                    elif tri == 18:
                        tablToSee.sort(key=lambda ballerine:-ballerine.negativeIndirect + max(ballerine.magie,ballerine.strength), reverse=True)
                    elif tri == 22:
                        tablToSee.sort(key=lambda ballerine:ballerine.strength + ballerine.precision + min(ballerine.negativeDirect,ballerine.negativeIndirect)*-1, reverse=True)
                    elif tri == 23:
                        tablToSee.sort(key=lambda ballerine:ballerine.strength + ballerine.agility + min(ballerine.negativeDirect,ballerine.negativeIndirect)*-1, reverse=True)
                    elif tri == 24:
                        tablToSee.sort(key=lambda ballerine:ballerine.strength + ballerine.endurance + min(ballerine.negativeDirect,ballerine.negativeIndirect)*-1, reverse=True)
                    elif tri == 25:
                        tablToSee.sort(key=lambda ballerine:ballerine.endurance + ballerine.magie + min(ballerine.negativeDirect,ballerine.negativeIndirect)*-1, reverse=True)
                    elif tri == 26:
                        tablToSee.sort(key=lambda ballerine:ballerine.charisma + ballerine.endurance + ballerine.negativeHeal*-1, reverse=True)
                    elif tri == 27:
                        tablToSee.sort(key=lambda ballerine:ballerine.intelligence + ballerine.endurance + ballerine.negativeShield*-1, reverse=True)
                    elif tri == 28:
                        tablToSee.sort(key=lambda ballerine:ballerine.charisma + ballerine.negativeHeal*-1, reverse=True)
                    elif tri == 29:
                        tablToSee.sort(key=lambda ballerine:ballerine.charisma + ballerine.negativeBoost*-1, reverse=True)
                    elif tri == 30:
                        tablToSee.sort(key=lambda ballerine:ballerine.intelligence + ballerine.negativeShield*-1, reverse=True)
                    elif tri == 31:
                        tablToSee.sort(key=lambda ballerine:ballerine.intelligence + ballerine.negativeBoost*-1, reverse=True)
                    elif tri == 32:
                        tablToSee.sort(key=lambda ballerine:ballerine.magie + ballerine.precision + min(ballerine.negativeDirect,ballerine.negativeIndirect)*-1, reverse=True)
                elif destination != 2:
                    tablToSee.sort(key=lambda ballerine:ballerine.name,reverse=tri==1)

                lenTabl = len(tablToSee)
                maxPage=lenTabl//15 - int(lenTabl%15 == 0)
                page=0
                needRemake = False

            if destination == 0:      # Equipement
                desc = "**__Équipement équipé :__\n{0} {1}\n{2} {3}\n{4} {5}**".format(user.stuff[0].emoji,user.stuff[0].name,user.stuff[1].emoji,user.stuff[1].name,user.stuff[2].emoji,user.stuff[2].name)
            elif destination == 1:    # Arme
                desc = "**__Arme équipée :__\n{0} {1}**".format(user.weapon.emoji,user.weapon.name)
            elif destination == 2:    # Compétences
                desc = "**__Compétences équipées :__"
                for tip in range(len(user.skills)):
                    if type(user.skills[tip]) == skill:
                        desc += "\n{0} {1}".format(user.skills[tip].emoji,user.skills[tip].name)
                    else:
                        if user.level >= lvlToUnlockSkill[tip]:
                            desc += "\n -"
                        else:
                            desc += "\n 🔒"
                desc += "**"
            else:
                desc = "Les objets spéciaux permettent de modifier votre personnage"

            firstOptions = []

            if page > 0:
                firstOptions.append(create_select_option("Page précédente","goto{0}".format(page-1),'◀️'))
            if lenTabl != 0: # Génération des pages
                if destination != 3:
                    mess=""
                    if page != maxPage:
                        maxi = (page+1)*15
                    else:
                        maxi = lenTabl
                    for a in tablToSee[(page)*15:maxi]:
                        # Nom, posession
                        canEquip = ""
                        if type(a) in [skill,stuff] and not(a.havConds(user)):
                            canEquip = "`"
                        elif a in [user.weapon]+user.skills+user.stuff:
                            canEquip = "**"

                        mess += f"\n{a.emoji} __{canEquip}{a.name}{canEquip}__\n"
                        if type(a) == skill:
                            eff = findEffect(a.effect[0])

                        # Première info utile
                        if destination == 0 and type(a) == stuff:
                            mess +="*"+a.orientation+"*\n"
                        elif destination in [1,2] and type(a) != stuff:
                            ballerine = tablTypeStr[a.type]
                            if destination == 1:
                                eff = a.effect
                            else:
                                eff = None
                            if a.power > 0:
                                ballerine += " - {0}".format(a.power)
                            elif eff != None and eff.power > 0:
                                ballerine += " - {0}".format(eff.power)
                            elif type(a)==skill and a.effectOnSelf != None and findEffect(a.effectOnSelf).replica != None:
                                finalSkill = a
                                while (finalSkill.effectOnSelf != None and findEffect(finalSkill.effectOnSelf).replica != None):
                                    finalSkill = findSkill(findEffect(finalSkill.effectOnSelf).replica)
                                ballerine += " - {0}".format(finalSkill.power)

                            if type(a) in [skill,weapon] and a.repetition > 1:
                                ballerine += " x{0}".format(a.repetition)

                            if a.use != None and a.use != HARMONIE:
                                sandale = nameStats[a.use]
                            elif a.use == None:
                                sandale = "Fixe"
                            elif a.use == HARMONIE:
                                sandale = "Harmonie"

                            if destination == 1:
                                babie = ["Mêlée","Distance","Longue Distance"][a.range]+" - "
                            else:
                                babie=''

                            affinity = ""
                            if type(a) == stuff and a.affinity != None:
                                affinity = elemEmojis[a.affinity]
                            elif type(a) == skill and a.condition != []:
                                if a.condition[:2] == [0, 2]:
                                    affinity = elemEmojis[a.condition[2]]
                                elif a.condition[:2] == [0, 1]:
                                    affinity = aspiEmoji[a.condition[2]]
                                elif a.condition[:2] == [0, 3]:
                                    affinity = secElemEmojis[a.condition[2]]
                            if affinity != "":
                                affinity = " - "+affinity

                            mess += f"*{babie}{ballerine} - {sandale}{affinity}*\n"

                        # Statistiques
                        temp = ""
                        if destination in [0,1,2]:
                            if type(a) != skill:
                                stats,abre = [a.strength,a.endurance,a.charisma,a.agility,a.precision,a.intelligence,a.magie,a.resistance,a.percing,a.critical,a.negativeHeal*-1,a.negativeBoost*-1,a.negativeShield*-1,a.negativeDirect*-1,a.negativeIndirect*-1],["For","End","Cha","Agi","Pre","Int","Mag","Rés","Pén","Cri","Soi","Boo","Arm","Dir","Ind"]
                                for b in range(0,len(stats)):
                                    if stats[b] != 0:
                                        form = ""
                                        if b == tri-4:
                                            form = "**"
                                        if tri in [4,10] and b in [13,14]:
                                            if (b == 13 and (stats[13] > stats[14] or stats[13] == stats[14])) or (b == 14 and (stats[14] > stats[13] or stats[13] == stats[14])):
                                                form = "**"
                                        elif tri == 6 and b in [10,11]:
                                            if (b == 10 and (stats[10] > stats[11] or stats[10] == stats[11])) or (b == 11 and (stats[11] > stats[10] or stats[11] == stats[10])):
                                                form = "**"
                                        elif tri == 9 and b in [12,11]:
                                            if (b == 12 and (stats[12] > stats[11] or stats[12] == stats[11])) or (b == 11 and (stats[11] > stats[12] or stats[11] == stats[12])):
                                                form = "**"
                                        temp+=f"{form}{abre[b]}: {stats[b]}{form}, "
                                if a.affinity != None:
                                    nim = elemNames[a.affinity]
                                    if len(nim) > 3:
                                        nim = nim[0:3]+"."
                                    temp += " Elem. : "+nim

                                if a.effect != None:
                                    temp += " *{0}*".format(findEffect(a.effect).name)

                            else:
                                if a.ultimate:
                                    temp += "Ultime"

                                if a.effectOnSelf != None and findEffect(a.effectOnSelf).replica != None:
                                    castTime, finalSkill = 0, a
                                    while (finalSkill.effectOnSelf != None and findEffect(finalSkill.effectOnSelf).replica != None):
                                        finalSkill = findSkill(findEffect(finalSkill.effectOnSelf).replica)
                                        castTime += 1

                                    if temp != "":
                                        temp += ", "
                                    temp += "T. Cast : {0}".format(castTime)

                                if a.cooldown > 1:
                                    if temp != "":
                                        temp += ", "
                                    temp += "Cd. : {0}".format(a.cooldown)
                                if a.initCooldown > 1 and a.type != TYPE_PASSIVE:
                                    if temp != "":
                                        temp += ", "
                                    temp += "Cd. init. : {0}".format(a.initCooldown)
                        # Création de l'option
                        mess += temp+"\n"
                        firstOptions += [create_select_option(unhyperlink(a.name),a.id,getEmojiObject(a.emoji))]
                else:
                    mess = ""
                    if page != maxPage:
                        maxi = (page+1)*10
                    else:
                        maxi = lenTabl
                    for a in tablToSee[(page)*10:maxi]:
                        mess += f"{a.emoji} __{a.name}__"
                        firstOptions+=[create_select_option(unhyperlink(a.name),a.name,getEmojiObject(a.emoji))]
                        mess+="\n"
                
                if len(mess) > 4056: # Mess abrégé
                    mess = unemoji(mess)

            else:
                mess = "Il n'y a rien à afficher dans cette catégorie"

            if page < maxPage:
                firstOptions.append(create_select_option("Page suivante","goto{0}".format(page+1),'▶️'))

            embed = discord.Embed(title="__/inventory__",description=desc+"\n\n__Page **{0}** / {1} :__\n".format(page+1,maxPage+1)+mess,color=user.color)
            embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/{0}.png".format(userIconThub))

            if destination in [1,2]:
                temp1 = [hideNonEquip,affExclu,affNonEquip][affAll-1]
                if statsToAff == 0:
                    temp2 = onlyPhys
                elif statsToAff == 1:
                    temp2 = onlyMag
                else:
                    temp2 = allType

                if destination == 1:
                    ultimateTemp = [create_actionrow(temp1,temp2)]
                else:
                    temp3 = tablShowUltButton[(hideUlt+1)%5]
                    temp4 = tablSkillArea[affMono]
                    ultimateTemp = [create_actionrow(temp1,temp2,temp3,temp4)]

            elif destination == 0:
                temp1 = [hideNonEquip,affNonEquip,affExclu][affAll]
                temp2 = [affAcc,affBody,affShoes,affAllStuff][stuffToAff%4]
                ultimateTemp = [create_actionrow(temp1,temp2)]
            else:
                ultimateTemp = []

            if len(firstOptions) > 0:
                firstSelect = create_select(options=firstOptions,placeholder="Voir la page de l'équipement")
            else:
                firstSelect = create_select(options=[create_select_option("None","None")],placeholder="Cette catégorie n'a rien à afficher",disabled=True)

            if msg == None:
                try:
                    msg = await ctx.send(embed=embed,components=procurSelect+[create_actionrow(catSelect),create_actionrow(sortOptions),create_actionrow(firstSelect)]+ultimateTemp)
                except:
                    msg = await ctx.channel.send(embed=embed,components=procurSelect+[create_actionrow(catSelect),create_actionrow(sortOptions),create_actionrow(firstSelect)]+ultimateTemp)
            else:
                try:
                    await msg.edit(embed=embed,components=procurSelect+[create_actionrow(catSelect),create_actionrow(sortOptions),create_actionrow(firstSelect)]+ultimateTemp)
                except:
                    procurOptions = []
                    for a in listUserProcure:
                        procurOptions.append(create_select_option(a.name,"user_{0}".format(a.owner),getEmojiObject(await getUserIcon(bot,a)),default=a.owner == user.owner))
                    procurSelect = [create_actionrow(create_select(procurOptions))]
                    await msg.edit(embed=embed,components=procurSelect+[create_actionrow(catSelect),create_actionrow(sortOptions),create_actionrow(firstSelect)]+ultimateTemp)

            try:
                respond = await wait_for_component(bot,msg,check=check,timeout=180)
            except:
                embed = discord.Embed(title="__/inventory__",color=user.color)
                embed.add_field(name="__Arme :__",value="{0} {1}".format(user.weapon.emoji,user.weapon.name))
                embed.add_field(name="__Equipement :__",value="{0} {1}\n{2} {3}\n{4} {5}".format(user.stuff[0].emoji,user.stuff[0].name,user.stuff[1].emoji,user.stuff[1].name,user.stuff[2].emoji,user.stuff[2].name))
                temp = ""

                for nb in range(len(user.skills)):
                    if type(user.skills[nb])==skill:
                        temp += "{0} {1}\n".format(user.skills[nb].emoji,user.skills[nb].name)
                    else:
                        if user.level >= lvlToUnlockSkill[nb]:
                            temp += " -\n"
                        else:
                            temp += " 🔒\n"

                embed.add_field(name="__Compétences :__",value=temp)
                embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/{0}.png".format(userIconThub))
                await msg.edit(embed = embed, components = [])
                return 0

            if respond.component_type == 2:
                respond.values = [respond.custom_id]

            if respond.values[0].isdigit():
                respond = int(respond.values[0])
                sortOptions = changeDefault(sortOptions,respond)

                if respond in [0,1] or respond >= 14:
                    needRemake=True
                else:
                    tablToSee.sort(key=lambda ballerine: ballerine.name)
                    if respond == 4:
                        tablToSee.sort(key=lambda ballerine:ballerine.strength + max(ballerine.negativeDirect *-1,ballerine.negativeIndirect *-1), reverse=True)
                    elif respond == 5:
                        tablToSee.sort(key=lambda ballerine:ballerine.endurance, reverse=True)
                    elif respond == 6:
                        tablToSee.sort(key=lambda ballerine:ballerine.charisma + max(ballerine.negativeHeal *-1,ballerine.negativeBoost *-1), reverse=True)
                    elif respond == 7:
                        tablToSee.sort(key=lambda ballerine:ballerine.agility, reverse=True)
                    elif respond == 8:
                        tablToSee.sort(key=lambda ballerine:ballerine.precision, reverse=True)
                    elif respond == 9:
                        tablToSee.sort(key=lambda ballerine:ballerine.intelligence + max(ballerine.negativeShield *-1,ballerine.negativeBoost *-1), reverse=True)
                    elif respond == 10:
                        tablToSee.sort(key=lambda ballerine:ballerine.magie + max(ballerine.negativeDirect *-1,ballerine.negativeIndirect *-1), reverse=True)
                    elif respond == 11:
                        tablToSee.sort(key=lambda ballerine:ballerine.resistance, reverse=True)
                    elif respond == 12:
                        tablToSee.sort(key=lambda ballerine:ballerine.percing, reverse=True)
                    elif respond == 13:
                        tablToSee.sort(key=lambda ballerine:ballerine.critical, reverse=True)

                tri=respond

            elif respond.values[0].startswith("cat_"):
                destination = int(respond.values[0].replace("cat_",""))
                needRemake, tri, affAll, stuffAff, statsToAff, stuffToAff = True, 0, 1, False, 0, 0

            elif respond.values[0].startswith("goto"):
                page = int(respond.values[0].replace("goto",""))

            elif respond.values[0].startswith("user_"):
                user = loadCharFile("./userProfile/{0}.prof".format(respond.values[0].replace("user_","")))
                needRemake, tri, affAll, stuffAff, statsToAff, stuffToAff = True, 0, 0, False, 0, 0

            elif respond.values[0] in ["hideNoneEquip","affNoneEquip","affExclu"]:
                for cmpt in range(3):
                    if respond.values[0] == ["hideNoneEquip","affExclu","affNoneEquip"][cmpt]:
                        affAll = cmpt
                        break
                stuffAff = not(stuffAff)
                needRemake = True
            elif respond.values[0] in ["allDamages","onlyPhys","onlyMag","acc","dress","flats","all"]:
                if destination == 2:
                    statsToAff = (statsToAff+1)%3
                elif destination == 0:
                    stuffToAff = (stuffToAff+1)%4
                needRemake = True
            elif respond.values[0].endswith("_ult"):
                hideUlt = (hideUlt+1)%5
                needRemake = True
            elif respond.values[0].endswith("_area"):
                affMono = (affMono+1)%3
                needRemake = True
            elif respond.values[0].startswith("autCat_"):
                stuffMenuStatus, needRemake = int(respond.values[0][-1]), True
                tri = [0,22][stuffMenuStatus]
            else:
                inter = respond
                respond = respond.values[0]

                if respond in opValues:
                    for a in range(0,len(opValues)):
                        if opValues[a] == respond:
                            destination = a
                            needRemake = True
                            break

                else:
                    await msg.edit(embed=embed,components=[create_actionrow(create_select([create_select_option("None","None")],placeholder="Une autre action est en cours",disabled=True))])
                    if ctx.author_id != user.owner:
                        await inventory(bot,inter,respond,delete=True,procur=user.owner)
                    else:
                        await inventory(bot,inter,respond,delete=True)
