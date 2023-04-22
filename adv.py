from classes import *
from advObjects.advWeapons import *
from advObjects.advSkills import *
from advObjects.advStuffs import *
from advObjects.advInvocs import *
from advObjects.advEffects import *
from advObjects.advEnnemies import *
from advObjects.advAllies import *
from typing import Union
import copy

poidPlumeEff = effect("Poids Plume","poidCritEff",None,trigger=TRIGGER_END_OF_TURN,silent=True,lvl=0,type=TYPE_UNIQUE,unclearable=True,turnInit=-1,emoji=uniqueEmoji(aspiEmoji[POIDS_PLUME]))
obsEff = effect("Observateur","obsCritEff",None,silent=True,lvl=0,type=TYPE_UNIQUE,unclearable=True,turnInit=-1,emoji=uniqueEmoji(aspiEmoji[OBSERVATEUR]))

#Other
changeAspi = other("Changement d'aspiration","qa",description="Vous permet de changer d'aspiration",emoji='<:changeaspi:868831004545138718>')
changeAppa = other("Changement d'apparence","qb",description="Vous permet de changeer votre genre, couleur et espèce",emoji='<:changeAppa:872174182773977108>',price=500)
changeName = other("Changement de nom","qc",description="Vous permet de changer le nom de votre personnage",emoji='<:changeName:872174155485810718>',price=500)
restat = other("Rénitialisation des points bonus","qd",description="Vous permet de redistribuer vos points bonus",emoji='<:restats:872174136913461348>',price=500)
elementalCristal = other("Cristal élémentaire","qe",500,description="Ces cristaux vous permettent de changer l'élément de votre personnage dans /inventory element (lvl 10)\n\nCe cristal permet de sélectionner les éléments suivants :\n<:fire:887847475203932261> Feu\n<:water:887847459211079760> Eau\n<:air:887847440932290560> Air\n<:earth:887847425459503114> Terre",emoji="<:krysTal:888070310472073257>")
customColor = other("Couleur personnalisée","qf",500,description="Vous permet de rentrer une couleur personnalisée pour votre personnage",emoji='<:changeColor:892350738322300958>')
seeshell = other("Super Coquillage","None",500,description="Ce coquillage permet de changer son bonus iné dans /inventory bonus (lvl 25)")
blablator = other("Blablator","qg",500,description="Permet de définir des messages que votre personnages dira lors de certains événements",emoji='<:blablator:918073481562816532>')
dimentioCristal = other("Cristal dimentionel",'qh',500,'<:krysTal2:907638077307097088>',"Ces cristaux vous permettent de changer l'élément de votre personnage dans /inventory element (lvl 20)\n\nCe cristal permet de choisir les éléments suivants :\n<:light:887847410141921362> Lumière\n<:darkness:887847395067568128> Ténèbre\n<:astral:907467653147410475> Astral\n<:temporel:907467620930973707> Temporel")
token = other("Jeton de roulette","None",0,'<:jeton:917793426949435402>',"Ce jeton est à utiliser dans la Roulette\nAllez donc faire un tour à /roulette !")
mimique = other("Mimikator","qi",500,"<:mimikator:918073466077446164>","Cet emoji vous permet de changer l'apparance de votre arme ou accessoire sur votre icone de personnage.\n\nPour ce faire, appuyez juste sur le bouton correspondant lorsque vous ouvrez une page d'information d'une arme ou accessoire avec /inventory")
ilianaGrelot = other("Grelot","qj",350,'<:iliGrelot:930385123130609684>',"Vous permet de changer la forme de votre icone de personnage en Inkling Chat ou Octaling Chat")
grandNouveau = other("Boucles d'oreilles originelle","qk",350,amethystEarRings.emoji,"Vous permet de rénitialiser la forme de votre icone de personnage")
aliceBatEarRing = other("Amulette chauve-souris","ql",350,invocBat.emoji,"Vous permet de changer la forme de votre icone de personnage en Chauve-Souris")
birdup = other("Pigeon de compagnie","qm",350,'<:birdUp:930906195999473684>',"Vous permet de changer la forme de votre icone de personnage en Aviaire")
Megalovania = other("Musique qui rentre dans la tête","qn",350,'<:lazyBones:930949502133747762>',"Vous permet de changer la forme de votre icone de personnage en Crâne")
amary = other("Amaryllis",'qo',350,'<:amaryllis:935337538426642483>','Vous permet de changer la forme de votre icone en icone Féérique')
autoPoint = other("Pai'rte de Nheur'o'Nes",'qp',3500,emoji='<:autPoint:1041625800581066752>',description="Une fois cette object activé, chaque point bonus obtenus en montant de niveau est automatiquement attribué selon les statistiques recommandés pour votre aspiration\n\nNécessite d'être au moins niveau 1<:littleStar:925860806602682369>1")
autoStuff = other("Garde-robe de la Fée Niante",'qq',3500,emoji='<:autStuff:1041625746340323330>',description="Une fois cette object activé, à chaque fois que vous atteigné un pallié de niveau, modifie automatiquement votre équipement selon les statistiques recommandés pour votre aspiration\n\nNécessite d'être au moins niveau 1<:littleStar:925860806602682369>1")

others = [elementalCristal,customColor,changeAspi,changeAppa,changeName,restat,blablator,dimentioCristal,mimique,ilianaGrelot,grandNouveau,aliceBatEarRing,birdup,Megalovania,amary,autoPoint,autoStuff]

previewDict = {
    ilianaGrelot.id:'https://cdn.discordapp.com/emojis/930806243461857301.png',
    grandNouveau.id:'https://cdn.discordapp.com/emojis/930807241064480828.png',
    aliceBatEarRing.id:'https://cdn.discordapp.com/emojis/930807423483129876.png',
    birdup.id:'https://cdn.discordapp.com/emojis/930908758773743616.png',
    Megalovania.id:'https://cdn.discordapp.com/emojis/930911733307027536.png',
    amary.id:'https://cdn.discordapp.com/emojis/935340408723112047.png'
}

changeIconForm = [grandNouveau,ilianaGrelot,aliceBatEarRing,birdup,Megalovania,amary]

# Specials skills ================================================================================
# Total Kboum
totalAnnilLauch = copy.deepcopy(explosion)
totalAnnilLauch.power = 500

totalAnnilCastEff = effect("Cast - {replicaName}","totalBoomCast",turnInit=2,silent=True,replique=totalAnnilLauch)
totalAnnilCast = copy.deepcopy(totalAnnilLauch)
totalAnnilCast.power, totalAnnilCast.effectOnSelf = 0, totalAnnilCastEff

BOUMBOUMBOUMBOUMweap = weapon("noneWeap","noneweap",1,AREA_CIRCLE_1,0,0,0)
fairyBomb.effects[0].callOnTrigger = copy.deepcopy(findEffect("me"))
fairyBomb.effects[0].callOnTrigger.power = int(fairyBomb.effects[0].callOnTrigger.power*0.4)

hemoBomb.effects[0].callOnTrigger = copy.deepcopy(findEffect("mx"))
hemoBomb.effects[0].callOnTrigger.power = fairyBomb.effects[0].callOnTrigger.power//2

def findOther(otherId : Union[str,other]) -> Union[other,None]:
    if type(otherId) == other:
        return otherId
    else:
        otherId = otherId.replace("\n","")
        for a in others:
            if a.id == otherId or a.name.lower() == otherId.lower():
                return a
    return None

listAllBuyableShop = []
for a in weapons+skills+stuffs:
    if a.price > 0:
        listAllBuyableShop.append(a)

for cmpt in range(len(skills)):
    if skills[cmpt].invocation != None:
        summon: invoc = findSummon(skills[cmpt].invocation)
        timeLeft, iaPow, selfDestruc = 0, 0, False
        for skil in summon.skills:
            if type(skil) == skill:
                iaPow += skil.iaPow
                if not(skil.replay) or skil.type not in [TYPE_PASSIVE]:
                    timeLeft += 1
                if skil.effectOnSelf != None and skil.effectOnSelf.id == autoEff.id:
                    iaPow -= autoEff.power
                    selfDestruct = True
        if timeLeft < 3 and not(selfDestruc):
            iaPow += summon.weapon.power * (3-timeLeft)
        skills[cmpt].iaPow += (iaPow * skills[cmpt].nbSummon)
        if skills[cmpt].description in [None,""]:
            skills[cmpt].description = "Permet d'invoquer (un{0}) {2} {1} : {3}".format(["","e"][summon.gender == GENDER_FEMALE], summon.icon[0], summon.name, summon.description)

def userShopPurcent(user : char):
    totalShop = len(listAllBuyableShop)
    tablToSee = listAllBuyableShop[:]
    for a in listAllBuyableShop:
        if user.have(a):
            tablToSee.remove(a)

    return 100-(len(tablToSee)/totalShop*100)

def seeSimilarStuffNameMinLvl(name:str):
    tablLvl,tablName = [],[]

    name = name.lower()

    for obj in stuffs:
        if name in obj.name.lower():
            if obj.minLvl in tablLvl:
                for cmpt in range(len(tablLvl)):
                    if tablLvl[cmpt] == obj.minLvl:
                        tablName[cmpt].append(obj)
                        break
            else:
                tablLvl.append(obj.minLvl)
                tablName.append([obj])

    if tablLvl == []:
        return "==================================\n\"{0}\" :\nAucun objet trouvé".format(name)

    tablLvl.sort()
    tablName.sort(key=lambda alice: alice[0].minLvl)

    toReturn = "==================================\n\"{0}\" :".format(name)
    for cmpt in range(len(tablLvl)):
        toReturn += "\n- {0}".format(tablLvl[cmpt])
        tablName[cmpt].sort(key=lambda clemence:clemence.name)
        for obj in tablName[cmpt]:
            toReturn += "\n   {0}".format(obj.name)

    return toReturn

def seeAllStuffAtMinLvl(level:int):
    tablToSee = []
    for obj in stuffs:
        if obj.minLvl == level:
            tablToSee.append(obj.name)

    if tablToSee == []:
        return "==================================\n\"{0}\" :\nAucun objet trouvé".format(level)

    tablToSee.sort()

    toReturn = "==================================\n\"{0}\" :".format(level)
    for name in tablToSee:
        toReturn += "\n   {0}".format(name)

    return toReturn

# Stuff verifications ===========================================================================
if not(isLenapy):
    print("=============================\nVérification de l'équilibrage des stuffs...")
    print("Nombre d'équipements : ", len(stuffs))
    allstats = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    for a in stuffs:
        if a.effects == None or (a.effects != None and findEffect(a.effects).id != summonerMalus.id):
            ballerine = a.allStats()+[a.resistance,a.percing,a.critical]
            babie = [a.negativeHeal,a.negativeBoost,a.negativeShield,a.negativeDirect,a.negativeIndirect]
            sumation = 0
            for b in range(0,len(ballerine)):
                sumation += ballerine[b]
                allstats[b] += ballerine[b]

            for b in babie:
                sumation -= b

            if sumation != 20 and a.effects == None and a.name != "Claquettes chaussettes":
                print("{0} n'a pas le bon cumul de stats : {1}".format(a.name,sumation))

            elif sumation != 10 and a.effects != None:
                print("{0} n'a pas le bon cumul de stats : {1}".format(a.name,sumation))

    temp = "\nDistribution des statistiques :\n"
    total = 0
    for a in allstats:
        total += a

    for a in range(0,len(allStatsNames)):
        temp += "{0} : {1}% ({2})\n".format(allStatsNames[a],round(allstats[a]/total*100,2),allstats[a])
    #print(temp)

    lvlTabl = [{"level":0,"nombre":0}]
    for equip in stuffs:
        find = False
        for temp in lvlTabl:
            if temp["level"] == equip.minLvl:
                temp["nombre"]+=1
                find = True
                break

        if not(find):
            lvlTabl.append({"level":equip.minLvl,"nombre":1})

    lenStuff = len(stuffs)
    lvlTabl.sort(key=lambda ballerine: ballerine["level"])

    tempToPrint = ''
    for temp in lvlTabl:
        tempToPrint+="\nObjets de niveau {0} : {1} ({2})%, statsAttendues : {3}".format(temp["level"],temp["nombre"],round(temp["nombre"]/lenStuff*100,2),20 + (temp["level"] * 2))
    #print(tempToPrint)

    tabl = copy.deepcopy(tablAllAllies)
    tablTank = []
    tablMid = []
    tablBack = []

    for allie in tabl:
        [tablTank,tablMid,tablBack][allie.weapon.range].append(allie)

    #print("")
    for num in range(3):
        pass
        #print("Nombre de Temp's en {0} : {1}".format(["mêlée","distance","backline"][num],len([tablTank,tablMid,tablBack][num])))

    tabl = copy.deepcopy(tablAllEnnemies)
    alReadySeen = []
    tablTank = []
    tablMid = []
    tablBack = []

    for ennemi in tabl:
        if ennemi.name not in alReadySeen:
            [tablTank,tablMid,tablBack][ennemi.weapon.range].append(ennemi)
            alReadySeen.append(ennemi.name)
            stat = ennemi.allStats()+[ennemi.resistance,ennemi.percing,ennemi.critical]
            summ = 0
            for a in stat:
                summ += a

            awaited = int((280+110*3)*1)
            if summ < awaited*0.9 or summ > awaited*1.1:
                print("{0} n'a pas le bon cumul de stats : {1} ({2})".format(ennemi.name,summ,awaited))

    #print("")
    for num in range(3):
        #print("Nombre d'ennemis en {0} : {1}".format(["mêlée","distance","backline"][num],len([tablTank,tablMid,tablBack][num])))
        pass

    for weap in weapons:
        summation = 0
        for stats in weap.allStats()+[weap.resistance,weap.percing,weap.critical]:
            if stats < 0:
                print("{0} : Stat négative détectée !".format(weap.name))
            else:
                summation += stats

        toVerif = 30
        if weap.effects != None or weap.effectOnUse != None:
            toVerif = 15

        if int(summation) != int(toVerif):
            print("{0} : Cumule de stats non égal à {1} ({2} / {1})".format(weap.name,toVerif,summation))
    print("Vérification de l'équilibrage des stuffs terminée\n=============================")

"""listObjWithNoOrientation = []
for obj in stuffs:
    if obj.orientation == "Neutre":
        listObjWithNoOrientation.append(obj.name)"""

"""if listObjWithNoOrientation != []:
    print("=================== Objets sans orientations ===================")
    for obj in listObjWithNoOrientation:
        print(obj)
"""

if not(isLenapy):
    allReadySeen = []
    for obj in stuffs+weapons+skills+others:
        if obj.id not in allReadySeen:
            allReadySeen.append(obj.id)
        else:
            what = ""
            for whaty in stuffs+weapons+skills+others:
                if whaty.id == obj.id:
                    what += whaty.name + ", "
            raise Exception("Identifiant doublon : {0}({1})".format(what,obj.id))

#print(seeSimilarStuffNameMinLvl("papillon rose"))
#print(seeAllStuffAtMinLvl(0))

"""for stuffy in stuffs:
    if stuffy.emoji in ['<:defHead:896928743967301703>','<:defMid:896928729673109535>','<:defShoes:896928709330731018>']:
        print("{0} use a default emoji".format(stuffy.name))"""

cmpt = 0
for obj in skills+tablVarAllies+tablUniqueEnnemies+tablBoss+tablBossPlus+tablRaidBoss:
    tablToSee: List[skill] = []
    if type(obj) == skill and obj.become == None and obj.depl == None:
        tablToSee = [obj]
    elif type(obj) == skill and obj.become != None:
        tablToSee = obj.become
    elif type(obj) == skill:
        tablToSee = [obj.depl.skills]
    else:
        for ski in obj.skills:
            if type(ski) == skill:
                tablToSee.append(ski)

    for ski in tablToSee:
        effToSee = []
        effPlus = [None]
        if ski.effectAroundCaster != None and type(ski.effectAroundCaster[2]) == effect:
            effPlus = [ski.effectAroundCaster[2]]
        for eff in ski.effects+[ski.effectOnSelf]+effPlus:
            if type(eff) == effect:
                if eff.id in [vulne.id,dmgUp.id,dmgDown.id,defenseUp.id,absEff.id,upgradedLifeSteal.id] and eff.stat in [FIXE,None] and not(str(eff.power) in eff.name):
                    eff.name = eff.name + " ({0}%)".format(eff.power)
                    cmpt += 1

if cmpt > 0:
    print("{0} effets ont été renommés".format(cmpt))

class preDefSkillSet:
    def __init__(self,element: Union[int, None] = None, skillList : List[skill] = []):
        self.element = element
        self.skillList = skillList

dictPreDefSkillSet = {
    BERSERK:[
        preDefSkillSet(skillList=[findSkill("Défi"),findSkill("Danse des sabres"),findSkill("Combo Tempête de Fer"),findSkill("Conviction du Berserkeur"),findSkill("Choc Chromatique"),findSkill("Bain de Sang Avancé"),findSkill("Impact Justicier")]),
        preDefSkillSet(element=ELEMENT_EARTH,skillList=[findSkill("Défi"),findSkill("Elipse Terrestre"),findSkill("Frappe Terre"),findSkill("Bain de Sang"),findSkill("Force de volonté"),findSkill("Frappe Convertissante Avancée"),findSkill("Pied Voltige")]),
        preDefSkillSet(element=ELEMENT_AIR,skillList=[findSkill("Défi"),findSkill("Frappe Air"),findSkill("Poussée Aviaire"),findSkill("Convertion élémentaire"),findSkill("Dernier Voyage"),findSkill("Soyokaze"),findSkill("Aer ferrum")]),
        preDefSkillSet(skillList=[findSkill("Défi"),findSkill("Linceuil de Lémure"),findSkill("Fétu Suppliant"),findSkill("Uppercut"),findSkill("Dernier Voyage"),findSkill("Ombre de la Mort"),findSkill("HighKick")]),
        preDefSkillSet(skillList=[findSkill("Défi"),findSkill("Attaque Sournoise"),findSkill("Pied Voltige"),findSkill("Corps à corps"),findSkill("Assasinat"),findSkill("Mort Vivant"),findSkill("Bain de Sang")]),
        preDefSkillSet(skillList=[findSkill("Défi"),findSkill("Invocation - Chauve-souris"),findSkill("Carnage"),findSkill("Choc Cardinal"),findSkill("Démolition"),findSkill("Voyage Ombral"),findSkill("Frappe Vangeresse")]),
        preDefSkillSet(element=ELEMENT_AIR,skillList=[findSkill("Défi"),findSkill("Plumes Perçantes"),findSkill("Déluge de plume"),findSkill("Plumes Célestes"),findSkill("Danse de la pluie étoilée"),findSkill("Plumes Rémanantes"),findSkill("Flèche aérienne")])
    ],
    POIDS_PLUME:[
        preDefSkillSet(element=ELEMENT_AIR,skillList=[findSkill("Défi"),findSkill("Plumes Perçantes"),findSkill("Déluge de plume"),findSkill("Plumes Célestes"),findSkill("Danse de la pluie étoilée"),findSkill("Plumes Rémanantes"),findSkill("Flèche aérienne")]),
        preDefSkillSet(skillList=[findSkill("Défi"),findSkill("Baleyette"),findSkill("Uppercut"),findSkill("Pied Voltige"),findSkill("Choc Ténébreux"),findSkill("Triple Attaque"),findSkill("Assaut du Crabe")]),
        preDefSkillSet(element=ELEMENT_AIR,skillList=[findSkill("Défi"),findSkill("Libération"),findSkill("Flèche aérienne"),findSkill("Convertion élémentaire"),findSkill("Démolition"),findSkill("Envolée féérique"),findSkill("Soyokaze")]),
        preDefSkillSet(skillList=[findSkill("Défi"),findSkill("Combo Eventails Célestes"),findSkill("Chorégraphie de l'éventail"),findSkill("Danse des sabres"),findSkill("Danse de la pluie étoilée"),findSkill("Final Classique"),findSkill("Final Technique")]),
        preDefSkillSet(skillList=[findSkill("Défi"),findSkill("Attaque Sournoise"),findSkill("Pied Voltige"),findSkill("Corps à corps"),findSkill("Assasinat"),findSkill("Mort Vivant"),findSkill("Bain de Sang")]),
        preDefSkillSet(skillList=[findSkill("Défi"),findSkill("Linceuil de Lémure"),findSkill("Fétu Suppliant"),findSkill("Uppercut"),findSkill("Dernier Voyage"),findSkill("Ombre de la Mort"),findSkill("HighKick")]),
    ],
}

for cmpt in range(ASPI_NEUTRAL):
    try:
        dictPreDefSkillSet[cmpt]
    except KeyError:
        dictPreDefSkillSet[cmpt] = []

varAllies = [
    findAllie("Shihu"),findAllie("Belle"),findAllie("Klironovia"),findAllie("Altikia"),findAllie("Luna"),findAllie("Chûri-Hinoro")
]

for ally in tablAllAllies+varAllies:
    elem = None
    for skilly in ally.skills:
        skilly = findSkill(skilly)
        if skilly != None and len(skilly.condition) > 1 and skilly.condition[1] == ELEMENT:
            elem = skilly.condition[2]
    dictPreDefSkillSet[ally.aspiration].append(preDefSkillSet(skillList=ally.skills,element=elem))

    if ally.changeDict != None:
        for chDict in ally.changeDict:
            asp, elem = ally.aspiration, None
            if chDict.aspiration != None:
                asp = chDict.aspiration
            if chDict.skills != None:
                for skilly in chDict.skills:
                    if len(skilly.condition) > 1 and skilly.condition[1] == ELEMENT:
                        elem = skilly.condition[2]
                dictPreDefSkillSet[asp].append(preDefSkillSet(skillList=chDict.skills,element=elem))

listUseSkills = []
for aspiCmpt in dictPreDefSkillSet:
    for defSki in dictPreDefSkillSet[aspiCmpt]:
        for skilly in defSki.skillList:
            if skilly not in listUseSkills:
                listUseSkills.append(skilly)

for ally in tablAllAllies:
    for skilly in ally.skills:
        if type(skilly) == skill and skilly not in listUseSkills:
            listUseSkills.append(skilly)
    if ally.changeDict != None:
        for cdi in ally.changeDict:
            if type(cdi) == tempAltBuilds:
                for skilly in cdi.skills:
                    if type(skilly) == skill and skilly not in listUseSkills:
                        listUseSkills.append(skilly)
            else:
                for cdi2 in cdi:
                    for skilly in cdi2.skills:
                        if type(skilly) == skill and skilly not in listUseSkills:
                            listUseSkills.append(skilly)

if False:
    print("Used skills : {0}%".format(round(len(listUseSkills)/len(skills)*100,2)))
    for cmpt in range(ASPI_NEUTRAL):
        print(inspi[cmpt],len(dictPreDefSkillSet[cmpt]))

#exclusiveRepartition()

dictSmallReticens = {
    "Clémence":["Gwendoline","Klironovia","Altikia","Lena","Luna","Ruby","Julie"],
    "Lena":["Clémence","Gwendoline","Klironovia","Altikia","Iliana"],
    "Lohica":["Shehisa","Hélène","Astra","Hina","Ly"],
    "Félicité":["Clémence","Lia","Lio"],
    "Alice":["Lio"],
    "Ruby":["Félicité","Sixtine","Alice","Shushi","Shihu"],
    "Julie":["Félicité","Sixtine","Alice","Shushi","Shihu"],
    "Ly":["Lohica"],
    "Anna":["Shushi","Shihu"],
    "Bénédicte":["Clémence"],
    "Shehisa":["Icealia","Lohica"],
    "Hélène":["Icealia","Lohica"]
}

dictMediumReticens = {
    "Lena":["Félicité","Sixtine","Alice"],
    "Gwendoline":["Félicité","Sixtine","Alice","Shushi","Shihu"],
    "Clémence":["Félicité","Sixtine","Alice","Shushi","Shihu"],
    "Alice":["Clémence","Bénédicte","Lily","Anna","Belle"],
    "Shushi":["Lena","Gwendoline","Klironovia","Altikia","Luna","Félicité","Sixtine","Alice"],
    "Shihu":["Lena","Gwendoline","Klironovia","Altikia","Luna","Félicité","Sixtine","Alice"],
    "Hélène":["Shehisa","Astra","Amary"],
    "Shehisa":["Amary","Astra","Hélène"],
    "Astra":["Shehisa","Hélène","Icealia"],
    "Félicité":["Sixtine","Lena","Gwendoline","Klironovia","Altikia","Luna","Iliana"],
    "Sixtine":["Félicité","Lena","Gwendoline","Klironovia","Altikia","Luna","Iliana"],
    "Icealia":["Shehisa","Lohica","Astra","Amary"],
    "Ruby":["Julie","Clémence"],
    "Julie":["Clémence"],
    "Iliana":["Félicité","Sixtine","Alice","Gwendoline","Klironovia","Altikia"]
}

def getAllieFromEnemy(enemy:octarien,lvl:int,gearEmotes:List[str]=[None,None,None],color=None) -> tmpAllie:
    tablStats = [
        int(enemy.strength*(max(10,lvl)/50)*1.5/3),
        int(enemy.endurance*(max(10,lvl)/50)*1.5/3),
        int(enemy.charisma*(max(10,lvl)/50)*1.5/3),
        int(enemy.agility*(max(10,lvl)/50)*1.5/3),
        int(enemy.precision*(max(10,lvl)/50)*1.5/3),
        int(enemy.intelligence*(max(10,lvl)/50)*1.5/3),
        int(enemy.strength*(max(10,lvl)/50)*1.5/3),
        int(enemy.resistance*1.2/3),
        int(enemy.percing*1.2/3),
        int(enemy.critical*1.2/3)
    ]
    tempStuff = [
        stuff("noName","noId",0,0,
              strength=tablStats[0],
              endurance=tablStats[1],
              charisma=tablStats[2],
              agility=tablStats[3],
              precision=tablStats[4],
              intelligence=tablStats[5],
              magie=tablStats[6],
              resistance=tablStats[7],
              percing=tablStats[8],
              critical=tablStats[9],
              emoji=gearEmotes[0]),
        stuff("noName","noId",1,0,
              strength=tablStats[0],
              endurance=tablStats[1],
              charisma=tablStats[2],
              agility=tablStats[3],
              precision=tablStats[4],
              intelligence=tablStats[5],
              magie=tablStats[6],
              resistance=tablStats[7],
              percing=tablStats[8],
              critical=tablStats[9],
              emoji=gearEmotes[1]),
        stuff("noName","noId",2,0,
              strength=tablStats[0],
              endurance=tablStats[1],
              charisma=tablStats[2],
              agility=tablStats[3],
              precision=tablStats[4],
              intelligence=tablStats[5],
              magie=tablStats[6],
              resistance=tablStats[7],
              percing=tablStats[8],
              critical=tablStats[9],
              emoji=gearEmotes[2])
        ]

    toReturn = tmpAllie(
        enemy.name,
        1,
        [color,light_blue][color==None],
        enemy.aspiration,
        enemy.weapon,
        tempStuff,
        enemy.gender,
        enemy.skills,
        enemy.description,
        deadIcon=enemy.deadIcon,
        icon=enemy.icon,
        say=enemy.says,
        splashArt=enemy.splashArt,
        splashIcon=enemy.splashIcon)

    return toReturn
