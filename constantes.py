"""
Constants module.
Here stand the first brick of the bot
"""
from datetime import timedelta, datetime
import os
from sre_constants import IN
from index import *
from discord_slash.utils.manage_components import *


FROM_LEFT, FROM_RIGHT, FROM_UP, FROM_DOWN, FROM_POINT = 0,1,2,3,4

# Constantes :
# Area of effects
AREA_MONO = 0  # Caster only
AREA_CIRCLE_1 = 1  # Circles (target include)
AREA_CIRCLE_2 = 2
AREA_CIRCLE_3 = 3
AREA_CIRCLE_4 = 4
AREA_CIRCLE_5 = 5
AREA_CIRCLE_6 = 6
AREA_CIRCLE_7 = 7
AREA_ALL_ALLIES = 8  # All allies
AREA_ALL_ENEMIES = 9  # All ennemies
AREA_ALL_ENTITES = 10  # All
AREA_CONE_2 = 11  # Cones
AREA_CONE_3 = 12
AREA_CONE_4 = 13
AREA_CONE_5 = 14
AREA_CONE_6 = 15
AREA_CONE_7 = 16
AREA_LINE_2 = 17  # Lines from target
AREA_LINE_3 = 18
AREA_LINE_4 = 19
AREA_LINE_5 = 20
AREA_LINE_6 = 21
AREA_DONUT_1 = 22  # Circles (target exclude)
AREA_DONUT_2 = 23
AREA_DONUT_3 = 24
AREA_DONUT_4 = 25
AREA_DONUT_5 = 26
AREA_DONUT_6 = 27
AREA_DONUT_7 = 28
AREA_DIST_3 = 29  # Circles (Must be > 2)
AREA_DIST_4 = 30
AREA_DIST_5 = 31
AREA_DIST_6 = 32
AREA_DIST_7 = 33
AREA_ARC_1 = 34  # Arc
AREA_ARC_2 = 35
AREA_ARC_3 = 36
AREA_RANDOMENNEMI_1 = 37
AREA_RANDOMENNEMI_2 = 38
AREA_RANDOMENNEMI_3 = 39
AREA_RANDOMENNEMI_4 = 40
AREA_RANDOMENNEMI_5 = 41
AREA_INLINE_2 = 42
AREA_INLINE_3 = 43
AREA_INLINE_4 = 44
AREA_INLINE_5 = 45

areaMelee = [AREA_MONO,AREA_CIRCLE_1,AREA_CIRCLE_2,AREA_CIRCLE_3,AREA_CONE_2,AREA_CONE_3,AREA_LINE_2,AREA_LINE_3,AREA_DONUT_1,AREA_DONUT_2,AREA_DONUT_3,AREA_INLINE_2,AREA_INLINE_3]
areaDist = [AREA_DIST_3,AREA_DIST_4,AREA_DIST_5,AREA_DIST_6,AREA_DIST_7]
areaMixte = []
for cmpt in range(AREA_INLINE_5+1):
    if cmpt not in [AREA_RANDOMENNEMI_1,AREA_RANDOMENNEMI_2,AREA_RANDOMENNEMI_3,AREA_RANDOMENNEMI_4,AREA_RANDOMENNEMI_5,AREA_ALL_ALLIES,AREA_ALL_ENEMIES,AREA_ALL_ENTITES] + areaMelee + areaDist:
        areaMixte.append(cmpt)

areaNames = ["Monocible", "Cercle de rayon 1", "Cercle de rayon 2", "Cercle de rayon 3", "Cercle de rayon 4", "Cercle de rayon 5", "Cercle de rayon 6", "Cercle de rayon 7", "Tous les alli??s", "Tous les ennemis", "Tous les combattants", "Cone simple", "Cone Large", "Cone Large", "Cone Large", "Cone Large", "Cone Large", "Ligne de 2 de longueur", "Ligne de 3 de longueur", "Ligne de 4 de longueur", "Ligne de 5 de longueur", "Ligne de 6 de longueur", "Donut de 1 de rayon", "Donut de 2 de rayon", "Donut de 3 de rayon", "Donut de 4 de rayon","Donut de 5 de rayon", "Donut de 6 de rayon", "Donut de 7 de rayon", "Anneau Distance de 1 de largeur", "Anneau Distance de 2 de largeur", "Anneau Distance de 3 de largeur", "Anneau Distance de 4 de largeur", "Anneau Distance de 5 de largeur", "Arc de Cercle de 1 de rayon", "Arc de Cercle de 2 de rayon", "Arc de Cercle de 3 de rayon", "1 ennemi al??atoire", "2 ennemis al??atoires", "3 ennemis al??atoires", "4 ennemis al??atoires", "5 ennemis al??atoires", "Croix de 2 cases", "Croix de 3 cases", "Croix de 4 cases", "Crois de 5 cases"]
allArea = range(0, 46)
listNumberEmoji = ["0??????","1??????","2??????","3??????","4??????","5??????","6??????","7??????","8??????","9??????","????","??????","??????","??????","??????","??????","??????","??????","???","???","???","???","??????","????","????","??????","??????","??????","??????","??????","??????","??????","??????","??????","??????"]
# Weapon's range
RANGE_MELEE = 0
RANGE_DIST = 1
RANGE_LONG = 2

# Triggers for the effects
TRIGGER_PASSIVE = 0
TRIGGER_DAMAGE = 1
TRIGGER_END_OF_TURN = 2
TRIGGER_DEATH = 3
TRIGGER_DEALS_DAMAGE = 4
TRIGGER_INSTANT = 5
TRIGGER_START_OF_TURN = 6
TRIGGER_ON_REMOVE = 7
TRIGGER_AFTER_DAMAGE = 8

allTriggers = [TRIGGER_PASSIVE, TRIGGER_DAMAGE, TRIGGER_END_OF_TURN, TRIGGER_DEATH,TRIGGER_DEALS_DAMAGE, TRIGGER_INSTANT, TRIGGER_START_OF_TURN, TRIGGER_ON_REMOVE, TRIGGER_AFTER_DAMAGE]
triggersTxt = [
    "passivement",
    "lorsque le porteur re??oit des d??g??ts directs",
    "?? la fin du tour du porteur",
    "?? la mort du porteur",
    "lorsque le porteur inflige des d??g??ts directs",
    "lors de la pose de cet effet",
    "au d??but du tour du porteur",
    "lors du retrait de cet effet",
    "apr??s que le porteur ai inflig?? des d??g??ts directs"
]

DMGBONUSATLVL50, HEALBONUSATLVL50, ARMORBONUSATLVL50, ARMORMALUSATLVL0 = 65, 15, 50, 20
DMGBONUSPERLEVEL, HEALBONUSPERLEVEL, ARMORLBONUSPERLEVEL = DMGBONUSATLVL50/50/100, HEALBONUSATLVL50/50/100, ARMORBONUSATLVL50/50/100
SUDDENDEATHDMG = 20

# Skills and effects types
TYPE_ARMOR = 0
TYPE_INDIRECT_DAMAGE = 1
TYPE_INDIRECT_HEAL = 2
TYPE_INDIRECT_REZ = 3
TYPE_BOOST = 4
TYPE_RESURECTION = 5
TYPE_DAMAGE = 6
TYPE_MALUS = 7
TYPE_HEAL = 8
TYPE_UNIQUE = 9
TYPE_SUMMON = 10
TYPE_PASSIVE = 11

tablTypeStr = ["Armure", "D??g??ts indirects", "Soins Indirects", "R??surection indirecte","Boost", "Resurection", "D??g??ts", "Malus", "Soins", "Unique", "Invocation", "Passif"]
allTypes = range(0, 12)

# Stats
STRENGTH = 0
ENDURANCE = 1
CHARISMA = 2
AGILITY = 3
PRECISION = 4
INTELLIGENCE = 5
MAGIE = 6
RESISTANCE = 7
PERCING = 8
CRITICAL = 9
ACT_HEAL_FULL = 10
ACT_BOOST_FULL = 11
ACT_SHIELD_FULL = 12
ACT_DIRECT_FULL = 13
ACT_INDIRECT_FULL = 14
PURCENTAGE = 11
FIXE = 12
HARMONIE = 13

ACT_HEAL = 0
ACT_BOOST = 1
ACT_SHIELD = 2
ACT_DIRECT = 3
ACT_INDIRECT = 4

nameStats, nameStats2 = ["Force", "Endurance", "Charisme", "Agilit??","Pr??cision", "Intelligence", "Magie"], ["R??sistance", "P??n??tration", "Critique"]
allStatsNames = nameStats+nameStats2

# Status for entities
STATUS_ALIVE, STATUS_DEAD, STATUS_RESURECTED, STATUS_TRUE_DEATH = 0, 1, 2, 3

DANGERUPPERSTAR = 5

# Aspirations
BERSERK, OBSERVATEUR, POIDS_PLUME, IDOLE, PREVOYANT, TETE_BRULE, MAGE, ALTRUISTE, ENCHANTEUR, PROTECTEUR, VIGILANT, SORCELER, INOVATEUR, ATTENTIF, ASPI_NEUTRAL = 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14
inspi = ["Berserkeur", "Observateur", "Poids plume", "Idole", "Pr??voyant", "T??te brul??e", "Mage","Altruiste", "Enchanteur", "Protecteur", "Vigilant", "Sorcier", "Inovateur", "Attentif", "Neutre"]
aspiEmoji = ["<:ber:985007311997263932>","<:obs:985007736360165407>","<:pplume:985007345648148541>","<:ido:985007596656275476>","<:pre:985007771613274133>","<:tbrule:985007436538740766>","<:ma:985010178900500561>","<:alt:985007803322224720>","<:enc:985007558156755004>","<:pro:985009037546487850>","<:vig:985009013097910302>","<:sor:985007632639205458>","<:inov:985007247656632360>","<:att:985007703707500555>","<:neutral:985011113458536538>"]
lbNames = ["Lames de l'Ombre","Odre de Tir : Dr??ne 3.4.8 Alpha","Frappe de Silicia","Apoth??ose plan??taire","Armure Galactique","Fracture Dimentionnelle","Col??re de Nacialisla","B??n??diction de Nacialisla","Desctruction Silicienne","Pous??e d'Espoir","Grandeur de Nacialisla","Cataclysme Powehien","Avenir Prometeur","Chef d'Oeuvre Balistique"]
lbDesc = ["Inflige des d??g??ts ?? l'ennemi cibl?? et vous soigne d'une partie des d??g??ts inflig??s","Inflige des d??g??ts ?? l'ennemi cibl?? et augmente vos statistiques","Inflige des d??g??ts ?? l'ennemi cibl?? et le repousse violament","Augmente les statistiques des alli??s ?? port??e et r??anime ceux qui sont vaincus","Octroi une armure aux alli??s ?? port??e et augmente leurs statistiques offensives","Inflige des d??g??ts ?? l'ennemi cibl?? et r??duit ses PV max","Inflige d??g??ts dans une large zone autour de l'ennemi cibl??","Soigne les alli??s ?? port??e et leur donne un effet de r??g??n??ration tout en r??animant ceux qui ??taient vaincus","Inflige des d??g??ts dans une large zone autour de l'ennemi cibl?? et vous octroit une armure","Octroi une armure aux alli??s ?? port??e et augmente leurs statistiques d??fensives","Soigne les alli??s ?? port??e en r??animant ceux vaincus tout en r??duisant vos d??g??ts subis","Inflige des d??g??ts dans une large zone autour de l'ennemi cibl?? et lui inflige un effet de d??g??ts indirects multi-cibles","Augmente les statistiques des alli??s ?? port??e et r??duit leurs d??g??ts subis pendant la m??me dur??e","Inflige des d??g??ts en ligne droite sur l'ennemi cibl?? et augmente vos statistiques"]
recommandedStat = [
    [STRENGTH, ENDURANCE],
    [STRENGTH, PRECISION],
    [AGILITY, STRENGTH],
    [CHARISMA, INTELLIGENCE],
    [INTELLIGENCE, PRECISION],
    [STRENGTH, PRECISION],
    [MAGIE, PRECISION],
    [CHARISMA, PRECISION],
    [MAGIE, ENDURANCE],
    [INTELLIGENCE, ENDURANCE],
    [CHARISMA, ENDURANCE],
    [MAGIE, INTELLIGENCE],
    [INTELLIGENCE, CHARISMA],
    [STRENGTH, INTELLIGENCE],
    [STRENGTH, MAGIE]
]
recommandedStuffStat = [
    [STRENGTH, RESISTANCE, ENDURANCE],
    [STRENGTH, PRECISION, ACT_DIRECT_FULL],
    [AGILITY, STRENGTH, RESISTANCE],
    [CHARISMA, ACT_BOOST_FULL, INTELLIGENCE],
    [INTELLIGENCE, ACT_SHIELD_FULL, PRECISION],
    [STRENGTH, PRECISION, CRITICAL],
    [MAGIE, PRECISION, ACT_DIRECT_FULL],
    [CHARISMA,ACT_HEAL_FULL, PRECISION],
    [MAGIE, ENDURANCE, RESISTANCE],
    [INTELLIGENCE, ENDURANCE, RESISTANCE],
    [CHARISMA, ENDURANCE, RESISTANCE],
    [MAGIE, INTELLIGENCE, ACT_INDIRECT_FULL],
    [INTELLIGENCE, ACT_SHIELD_FULL, CHARISMA],
    [STRENGTH, INTELLIGENCE, CRITICAL],
    [STRENGTH, MAGIE, ACT_DIRECT_FULL]
]

while len(aspiEmoji) < len(inspi):
    aspiEmoji.append('<a:menacing:917007335220711434>')

BERS_LIFE_STEAL = 35

# "Target" values
ALL, TEAM1, TEAM2, ALLIES, ENEMIES = 0, 1, 2, 3, 4

# Selected options for fight
OPTION_WEAPON, OPTION_SKILL, OPTION_MOVE, OPTION_SKIP = 0, 1, 2, 3

# Genders. 2 for default
GENDER_MALE, GENDER_FEMALE, GENDER_OTHER = 0, 1, 2

# Color constants
red, light_blue, yellow, green, blue, purple, pink, orange, white, black, aliceColor = 0xED0000, 0x94d4e4, 0xFCED12, 0x1ED311, 0x0035E4, 0x6100E4, 0xFB2DDB, 0xEF7C00, 0xffffff, 0x000000, 0xffc3ff
colorId = [red, orange, yellow, green,light_blue, blue, purple, pink, white, black]
colorChoice = ["Rouge", "Orange", "Jaune", "Vert","Bleu Clair", "Bleu", "Violet", "Rose", "Blanc", "Noir"]

# Aspiration's max stats
# Refert to Aspiration's constants value
aspiStats = [
    # Berserk
    [70, 60, 30, 35, 35, 25, 20],
    # Observateur
    [70, 10, 45, 35, 60, 20, 35],
    # Poids Plume
    [50, 40, 25, 75, 35, 10, 40],
    # Idole
    [25, 25, 70, 40, 35, 40, 40],
    # Pr??voyant
    [25, 35, 35, 35, 35, 75, 35],
    # T??te Brul??e
    [55, 45, 25, 35, 25, 35, 55],
    # Mage
    [25, 15, 40, 20, 50, 40, 85],
    # Altruise
    [15, 40, 85, 45, 20, 45, 25],
    # Enchanteur
    [25, 60, 30, 50, 25, 10, 75],
    # Protecteur
    [15, 60, 45, 35, 15, 75, 30],
    # Vigilant
    [15, 60, 70, 35, 35, 35, 25],
    # Sorcier
    [20, 35, 35, 35, 20, 50, 80],
    # Inovateur
    [20, 35, 40, 35, 35, 70, 40],
    # Attentif
    [60, 25, 30, 25, 60, 40, 35],
    # Neutre
    [40, 39, 39, 39, 39, 40, 39]
]

for a in range(0, len(inspi)):                           # Aspi base stats verification
    summation = 0
    for b in range(7):
        try:
            summation += aspiStats[a][b]
        except:
            pass

    if summation != 275:
        print("{0} n'a pas le bon cumul de stats : {1}".format(
            inspi[a], summation))

# Const Stuff Drop
constStuffDrop = {0:80,10:80,20:70,30:60,40:50,50:45,60:40,70:35,80:30,90:20,100:10}
constLooseStuffDrop = [50,35,15,5]
# Const Skill Drop
constSkillDrop = {0:100,10:90,20:80,30:70,40:60,50:50,60:40,70:35,80:30,90:20,100:10}

# Constants for "orientation" field for skills
TANK, DISTANCE, LONG_DIST = "Tank", "Distance", "Longue Distance"
DPT_PHYS, HEALER, BOOSTER, DPT_MAGIC, SHIELDER = "Bers, Obs, P.Plu, T.Bru, Att.", "Vig., Alt", "Ido, Inv.", "Enc, Mag, Sor.", "Pro., Pr??."

# Elementals ----------------------------------------------------------------------------------------------------------
ELEMENT_NEUTRAL = 0
ELEMENT_FIRE = 1
ELEMENT_WATER = 2
ELEMENT_AIR = 3
ELEMENT_EARTH = 4
ELEMENT_LIGHT = 5
ELEMENT_DARKNESS = 6
ELEMENT_SPACE = 7
ELEMENT_TIME = 8
ELEMENT_UNIVERSALIS_PREMO = 9

elemEmojis = ["<:neutral:921127224596385802>", "<:fire:918212781168275456>", "<:water:918212797320536124>", "<:air:918592529480446002>", "<:earth:918212824805801984>","<:light:918212861757653053>", "<:darkness:918212877419175946>", '<:space:918212897967075329>', '<:time:918212912408051814>', "<:univ:936302039456165898>"]
secElemEmojis = ["<:empty:866459463568850954>", "<:secFeu:932941340612894760>", "<:secEau:932941360858820618>", "<:secAir:932941299559063573>","<:secTerre:932941317804273734>", "<:secLum:932941251597201438>", "<:secTen:932941234501222410>", "<:secTempo:932941280785338389>", "<:secAst:932941221331075092>"]
elemDesc = [
    "L'??l??ment Neutre ({0}) est l'??l??ment le plus appr??ci?? des nouvelles recrues.\nSans sp??cialisations particuli??re, cet ??l??ment permet de tout faire sans trop se casser la t??te".format(elemEmojis[0]),
    "L'??l??ment Feu ({0}) est en g??n??ral pr??f??r?? par ceux qui aiment tirer sans distinction et faire carnage sans pareil.\nLes dissicles de l'??l??ment Feu infligent un peu plus de d??g??ts avec les armes et capacit?? de zone en distance.".format(elemEmojis[1]),
    "L'??l??ment Eau ({0}) est plus propice ?? la concentration et la s??r??nit??.\nLes adeptes de cet ??l??ment inflige plus de d??g??ts avec les armes ou capacit??s monocible ?? distance.".format(elemEmojis[2]),
    "L'??l??ment Air ({0}) a pour r??putation d'??tre assez capricieu et impr??visible.\nC'est pour cela que ses partisants filent tel le vent pour frapper plusieurs ennemis simultan??ment.".format(elemEmojis[3]),
    "L'??l??ment Terre ({0}) permet de ressentir la puissance des courants d'??nergie t??lurique et d'en tirer le meilleur parti.\nLes habitu??s de cet ??l??ment infligent des d??g??ts monocibles en m??l??e plus cons??quents.".format(elemEmojis[4]),
    "L'??l??ment Lumi??re ({0}) permet d'entrevoir l'espoir l?? o?? les autres ne voit que les ombres.\nLes soins et armures de ces illumin??s sont plus cons??quents que ceux de leurs cong??naires.".format(elemEmojis[5]),
    "L'??l??ment T??n??bre ({0}) n'a pas son pareil pour exploiter les zones d'ombres de leurs adversaires.\nLes d??g??ts indirects de ces individues sont plus cons??quents que ceux de leurs cong??n??res.".format(elemEmojis[6]),
    "L'??l??ment Astral ({0}) utilise la puissance cosmique ?? son aventage. Car rien ne se perd, rien ne se cr??ait, tout se transforme.".format(elemEmojis[7]),
    "L'??l??ment Temporel ({0}) permet de pr??voire les coups, car avoir une longueur d'avance est toujours bienvenue.".format(elemEmojis[8])
]
elemNames = ["Neutre", "Feu", "Eau", "Air", "Terre", "Lumi??re","T??n??bre", "Astral", "Temporel", "Universalis Premera"]
elemMainPassifDesc = [
    "Aucun passif principal",
    "P??n??tration : + 5\nD??g??ts zones et distance simultan??ment : +10%",
    "Pr??cision : + 10\nD??g??ts monocible et distance simultan??ment : +10%",
    "Agilit?? : + 10\nD??g??ts zones et m??l??e simultan??ment : +10%",
    "R??sistance : + 5\nD??g??ts monocible et m??l??e simultan??ment : +10%",
    "Soins et armures : +10%",
    "D??g??ts indirects : + 10%",
    "Puissance des boosts et malus donn??s : +10%\nPuissance des boost re??u d'autrui : +5%\nPuissance des malus re??us d'autrui : -5%",
    "Puissance des effets de soins indirects : +20%"
]
elemSecPassifDesc = [
    "Aucun passif secondaire",
    "Soins donn??s et re??us : +5%\nArmures donn??es et re??ues : -5%",
    "Armures donn??es et re??ues : +5%\nSoins donn??es et re??us : -5%",
    "Puissance des bonus et malus donn??es et re??us : +5%",
    "D??g??ts sur Armure inflig??s et re??us : +5%",
    "D??g??ts directs inflig??s et re??us : +5%",
    "D??g??ts directs inflig??s et re??us : -5%",
    "D??g??ts directs de zone inflig??es et re??us : +5%",
    "D??g??ts directs monocibles inflig??s et re??us : +5%"
]

# AoE stuff
AOEDAMAGEREDUCTION = 0.25
AOEMINDAMAGE = 0.2

def uniqueEmoji(emoji):
    return [[emoji, emoji], [emoji, emoji], [emoji, emoji]]

def sameSpeciesEmoji(team1, team2):
    return [[team1, team2], [team1, team2], [team1, team2]]

dangerEm = sameSpeciesEmoji('<a:dangerB:898372745023336448>', '<a:dangerR:898372723150041139>')
untargetableEmoji = uniqueEmoji('<:untargetable:899610264998125589>')

# List of guild ids for the bots
ShushyCustomIcons = [881900244487516180]
LenaCustomIcons = [881632520830087218, 881633183425253396]

stuffIconGuilds = [866782432997015613, 878720670006132787, 887756868787769434, 887846876114739261, 904164080204513331,908551466988486667, 914608569284964392, 922684334010433547, 928202839136825344, 933783830341484624, 953212496930562098]
weaponIconGuilds = [866363139931242506, 878720670006132787, 887756868787769434,938379180851212310, 887846876114739261, 916120008948600872, 911731670972002374]

# For some time related stuff. Time from server != time from France
if not(os.path.exists("../Kawi")):
    horaire = timedelta(hours=2)
else:
    horaire = timedelta(hours=0)

# Are we on the livebot or the test bot ?
isLenapy = not(os.path.exists("../Kawi"))

# Level to unlock skill slot
lvlToUnlockSkill = [0, 0, 0, 5, 15, 25, 35]

SKILL_GROUP_NEUTRAL, SKILL_GROUP_HOLY, SKILL_GROUP_DEMON = 0, 1, 2
skillGroupNames = ["neutre", "divine", "d??moniaque"]

# Tabl of random messages for the shop
shopRandomMsg = [
    "<:ikaBlue:866459319049650206> : `Sit down and eat pop-corns`\n{shushi} : `Regarde les pop-corns avec un air interres??e`",
    "<:soria:977183253255557140> : \"Flum POWA !\"\n{clemence} : \"Les coquelicots c'est mieux je trouve\"\n{alice} : \"N'importe quoi ! Ce sont les roses les plus jolies !\"\n{lena} : \"Vous trois, vous pourriez arr??ter de d??battre dans mon shop, s'il vous plait ?\"",
    '{clemence} : "Hum... j\'ai trouv?? des trucs qui pourrait t\'interresser lors de ma derni??re escapade dans les ruines d\'Elidyn, Lena"\n{lena} : "Ow ? Montre pour voir ?"',
    '{alice} : "Mooow tu sais que tu es trop mignone toi ?"\n{shushi} : "Heu... gwa ?"',
    '{shihu} : "Tu en pense qwa de cette coupe de cheveux ?"\n{shushi} : "Hum... Pi vraiment convaincue..."\n{shihu} : "Oh..."\n{shushi} : "Mais apr??s, je peux toujours en faire un queue de cheval regarde !\n{shihu} : :0',
    '{feli} : "H?? Cl??mence ! Je peux t\'accompagner pour ta prochaine aventure ? Je te promet que je te g??nerais pas !"\n{clemence} : "Tu va pas lacher hein... Si tu y tiens. Mais je suis pas responsable si Lena te gronde pour ??a, compris ?"\n{feli} : :D',
    '<:akira:909048455828238347> : ...\n{shihu} : ...\n<:akira:909048455828238347> {shihu} : ^^\n\n{lena} : <:LenaWhat:760884455727955978>',
    '{helene} : "Tu es au courant que mourir par h??morragie est tout sauf une mort agr??able hein ?"\n{shehisa} : "Je vois pas o?? est la diff??rence avec les infections que tu donnes ?? tes adversaires. Je suis peut-??tre pas une soigneuse, mais Papa m\'a suffisament initi??e pour savoir que les maladies que tu leur refile sont tous sauf agr??able"',
    '{shehisa} : "Tu me reproche d\'avoir suivi la voie de Maman, mais tu devrais voir comment tu te comporte face ?? un ennemi quand tu veux lui faire avaler la pilule"\n<:helene:906303162854543390> : "Qu\'est-ce que tu insinue par l?? ?"\n{shehisa} : "Que je suis pas la seule ?? avoir h??rit??e des talents de Maman"',
    '{shehisa} : "Toujours rassurant de te savoir dans les parages, Icealia"\n{icelia} : "Et moi je suis toujours rasur??e de te savoir dans mon camp..."',
    '<:determination:867894180851482644> : "Alors F??li, tu as fais des progr??s sur ta maitrise de la D??termination ?"\n{feli} : "Ouais :D ! Regarde ??a !"',
    '<:ruby:958786374759251988> : "Cl??mence, ??a va mieux avec ta cicatrice en ce moment ?"\n{clemence} : "?? part qu\'elle me br??le quand j\'utilise trop mes pouvoirs vampiriques ou quand il y a un Alpha dans le coin, rien ?? d??clarer"\n<:ruby:958786374759251988> : "Tss. Ces loups garoux..."\n{clemence} : "Pas la peine de prendre ce regard assassin Madame Ruby. J\'ai appris ?? faire avec maintenant"',
    '`Alice surgit au coins du couloir en courant et vous rentre dedans, ne vous ayant pas vu`\n\n{alice} : "D??-d??sol??e !"\n\n`Elle ramasse rapidement les cahiers qu\'elle portait dans ses bras et repart aussi vite qu\'elle est venue.\nVous constatez qu\'elle a oubli?? une feuille, qui a du se retrouver sous elle quand elle est tomb??e`\n\n???? [Devoir d\'astronomie sur les trous noirs](https://bit.ly/3kh8xP3)',
    '{alice} : "Maraiiiiiiiiine ?"\n{lena} : "Il y a un peu trop de "i" pour moi..."\n{alice} : "C\'est quoi ??a."\n\n`Elle sortie son t??l??phone et le mit directement devant le visage de Lena`\n\n???? [Photographie d\'une feuille de papier](https://bit.ly/3o74aal)\n\n{lena} : "... Merde. Et comment ??a, tu es all?? fouiller dans ma chambre !?"',
    '{lena} : "Tu sais que tu va finir par traumatiser des gens avec tes \"Boum boum\" toi ?"\n{shihu} : "Mais c\'est drole les Boum Boum..."',
    '{clemence} : "H?? Powehi, je me suis retrouv??e avec plein de Rotten Flesh lors de ma derni??re exp??dition, tu veux que je te les passes ?"\n<:powehi:909048473666596905> : "Oh que oui !"',
    '{gweny} : "Toujours ?? regarder les ??toiles ?"\n<:powehi:909048473666596905> : "J\'ai une question Gwendoline... Tu r??agirais comment si tu ??tais bloqu??e dans ce monde apr??s ta mort et ne pouvais que regarder les autres ??tre vivant te fuir d??s que tu t\'approches trop d\'eux ?"\n{gweny} : "Oh heu... Je sais pas vraiment d??sol??e. Compliqu?? de se mettre ?? ta place, j\'en ai bien peur"\n<:powehi:909048473666596905> : "C\'est pas grave, merci quand m??me..."',
    '`En entrant dans une pi??ce pr??sum??e vide, vous ??tes surpris de voir des reflets lumineux dans un coin. En allant l\'examiner, vous d??couvrez Shushi et Sixtine qui dorment l\'une contre l\'autre. Au sol se trouve un lecteur de musique`\n\n???? [Liste de musique en file d\'attente](https://bit.ly/3D6Ltdh)',
    "<:john:908887592756449311> : \"A-Alice, toi qui la connais bien tu... saurais ce que je pourrais faire pour... qu'elle me voit comme autre chose qu'un... ami ?\"\n{alice} : \"Commence par ??tre un peu plus s??r de toi. L??, elle continue de voir le louvetau na??f qui essayait de se coucher ?? ses pieds au lieu de fuir\"\n<:john:908887592756449311> : \"Mais je-\"\n{alice} : \"Passe ton temps avec elle sous ta forme de loup ?? ??tre couch?? ?? ses pieds. Si tu veux qu'elle te vois comme autre chose qu'un chien de compagnie, va falloir que tu arr??te de te comporter tel quel.\"",
    "<:lio:908754690769043546> : \"H-hm !? Oh c'est toi...\"\n{feli} : \"Tiens tu es l?? toi aussi ?\"\n<:lio:908754690769043546> : \"J'ai pas trouv?? d'autres points d'eau dans le coin donc oui... je suppose...\"",
    "{gweny} : \"Eh bien... On... fatigue d??j??... Liu... ?\"\n<:liu:908754674449018890> : \"Cer... Certainement pas... Je... pourrais courir... comme ??a... pendant encore des kilom??tres...\"",
    "<:lia:908754741226520656> : \"H?? Alice ! Tu penses quoi de ces fleurs l?? ?\"\n{alice} : \"Hum... un peu trop jaune ?? mon go??t...\"",
    "{shushi} : \"H?? h?? Madame des neiges ! J'ai touv?? ??a part terre, y a maqu?? quoi de??u ?\"\n{icelia} : \"Montre moi pour voir ^^ ?\"\n\n???? [Page de papier ?? l'encre rose](https://bit.ly/3DgXk8v)",
    "{lena} : \"La vache c'est bien plus compliqu?? que je le pensais de lancer ces plumes enfaites...\"\n<:hina:908820821185810454> : \"C'est qu'une question d'habitude ^^ H??nnetement... J'arriverai m??me pas ?? tenir un de tes fusils donc bon ^^'\"",
    "{sixtine} : \"...\"\n<:krys:916118008991215726> : ?\"\n{sixtine} : \"...\"\n<:krys:916118008991215726> : \"?.? Je peux t'aider ?\"\n{sixtine} : \"Oh heu... Je me demandais juste si tu avais un coeur de pierre...\"\n<:krys:916118008991215726> : \"??.??\"",
    "{iliana} : \"Cl-Clm??ence... ? Hum... tu sais pourquoi ta soeur m'??vite toi... ?\"\n{clemence} : \"Si tu parles d'Alice, elle a eu quelques porbl??mes avec un chat quand elle ??tait plus jeune donc elle en est un peu traumatis??e\"\n{iliana} : \"Oh... la pauvre...\"",
    "{sixtine} : \"Par curiosit?? Alice... tu as quoi comme info sur Iliana ?\"\n{alice} : \"Hum... Laisse moi voir... Tiens voil??\"\n\n[Feuille de papier frois??e](https://docs.google.com/document/d/1SUVmdch_lQ-Ub_zoTJKOtxTkwZMqyLD8xrbCq8CTcDQ/edit?usp=drivesdk)\n\n{sixtine} : \"M??me sur ??a tu as fais d'efforts... ?\"\n{alice} : S-Sixtine ! Tu sais bien que je peux juste... pas...",
    "{sixtine} : `Regarde le crusifix et le livre religieux ?? c??t?? du lit d'Alice` \"Comment tu arrives ?? dormir ?? c??t?? de ??a... Cl??mence ne supporte m??me pas d'??tre ?? proximit?? d'une croix...\"\n{alice} : `Fait une petite moue`\" C'est elle qui s'est d??finie en temps qu'ennemi du divin souss pr??texte que c'est sa nature. Mais ce genre de discipline tiens sa puissance en la Foi. Tant que tu l'as, qu'importe que ce tu es",
    "{clemence} : \"... Je sais que tu as la manie de dormir partout Sixtine... Mais dans mon cercueil tout en ??tant claustrophobe ?\"\n{sixtine} : `Dort ?? point ferm??`",
    "{lena} : \"Contente que tu ai chang?? d'avis\"\n<:ly:943444713212641310> : \"J'avais besoin de changer d'horizon\"",
    "<:edelweiss:918451422939451412> : \"... Je peux t'aider ? On le dirait pas comme ??a mais je me d??brouille plut??t bien en soins\"\n<:lohica:919863918166417448> : \"Tu me rappelle juste quelqu'un, c'est tout... Et ton truc c'est pas plut??t la protection ?\"\n<:edelweiss:918451422939451412> : `Hausse les ??paules` \"Je le fais parcequ'il y a d??j?? pas mal de personnes qui soignent ici, c'est tout\"",
    "{feli} : \"Dit Maraine, tu peux jouer ??a au violon ?\"\n{lena} : \"Hum laisse moi voir ? Si Do# Mi Fa# Mi R??# Do# Si Fa#... Oh. Je vois o?? tu veux en venir\"",
    "{lena} : \"Merci du coup de main Lio. Bon maintenant Shihu. Qu'est-ce que j'ai dit ?? propos de l'utilisation de la magie ?? la maison ?\"\n{shihu} : \"De... Pas utiliser la magie ?? la maison...\"\n{lena} : \"Et donc pourquoi on a du s'y mettre ?? trois pour ??teindre les flammes noires dans votre chambre ?\"\n{shihu} : \"Mais il y avait un moustique...\"\n{lena} : \"Et tu penses s??rieusement que risquer de r??duire la maison en cendre pour un moustique est une bonne id??e ?\"\n{shihu} : \"... au moins je l'ai eu...\"\n{lena} : \"... Vous ??tes toutes les deux priv??es de dessins anim??s et de dessert pour une semaine.\"\n{shushi} : \"Mais j'ai rien fait moi !\"\n{lena} : \"Justement.\"",
    "{shihu} : \"Lena ne va pas du tout ??tre contente quand elle vera que tu as pris un de ses pistolets d'airsoft...\"\n{shushi} : \"Elle n'en saura rien !\"\n{shihu} : \"Tu as m??me pas pris de protections..\"\n\n`Shushi visa une canette vide et tira, sans grand succ??s. La bille rebondit cependant sur le mur derri??re et explosa contre un bouclier lumineux qui s'??tait form??e devant la petite fille avant qu'elle n'ai eu le temps de bouger. Cette derni??re regarda un peu confuse autour d'elle puis elle remarqua la chatte blanche assise ?? c??t?? d'elle qui la regardait fixement`\n\n{shushi} : \"... s'il te plait le dis pas ?? Miman...\"\n{iliana} : \"Si tu ranges ??a, peut-??tre\"\n{shihu} : \"(Pff, elle fait juste ??a pour pas que Lena la tienne responsable ??galement)\"",
    "{alice} : `Carresse tr??s lentement Iliana en ??tant relativement tendue`\n{iliana} : `Se contente de ronronner sans bouger pour ??viter de l'effrayer. Et puis elle aime bien les caresses`\n{alice} : `Se met ?? lui caresser le ventre en voyant qu'elle s'est mise sur le dos`\n{iliana} : `Essaye le plus possible d'ignorer son instinct de f??lin qui lui hurle d'essayer de mordiller cette main qui se balade sur son ventre, parcequ'elle n'a pas envie que cette m??me main la projette contre un mur dans un mouvement brusque avec toute la force d'une jeune vampire paniqu??e. Quelque chose lui dit que plusieurs de ses os ne l'appr??ciraient pas trop`",
    "{shushi} : \"Maman tu fais quoi ?\"\n{lena} : \"Hum ? Oh rien d'important\" `Glisse une feuille de papier derri??re elle`\n{shushi} : \"Tu peux m'aider pour mes devoirs :< ? J'y arrive pas\"\n{lena} : \"Oh oui bien s??r ^^\"\n\n`Les deux quitt??rent la pi??ce en laissant la dite feuille sur le bureau`\n\n:page_with_curl: [Feuille de papier](https://docs.google.com/spreadsheets/d/1l6csj2GjnaHMPYhPgqaji6Hs7bU68eb4XC_Ss2oxT-4/edit?usp=drivesdk)",
    "<:benedict:958786319776112690> : \"Bon j'ai fais ce que tu m'as demand?? et selon mon correspondant, effectivement il a bien constat?? qu'une ??me incomplete est coinc??e au purgatoire depuis plusieurs d??cinies\"\n{shehisa} : \"Merci\"\n<:benedict:958786319776112690> : \"Juste merci :< ?\"\n{shehisa} : \"Merci B??n??dicte d'avoir fait jouer tes relations surnaturelles afin de r??pondre ?? ma question\"\n<:benedict:958786319776112690> : \":< ??a ira je suppose...\"",
    "{shehisa} : \"Tiens ??a me fait penser, mais tu avais pas dit que tu lib??rais tes morts-vivants si ils ??tait plus en ??tat de se d??placer correctement ?\"\n<:kiku:962082466368213043> : \"C'est le cas\"\n{shehisa} : \"Bah heu... \" `Jette un oeuil ?? une goule qui n'avait plus qu'un tron`\n<:kiku:962082466368213043> : \"C'est pas ce que tu crois. C'est lui qui veut pas que je le lib??re\"",
    "{alice}<:stella:958786101940736061> : \"??????????????? hihihiA, hihihiB, hihihiC, D, E !\"\n{shushi} : \"Elles ont pas bient??t finie... ? J'ai mal aux oreilles...\"\n{clemence} : \"Techniquement la chanson est finie, mais je doute qu'elles s'en arr??tent l?? malheureusement...",
    "{shehisa} : \"What is going on here? I'm a little out of sorts, I've been contemplating, Fallacies and things that scare me. Why not try to let go? I've been feeling out of order, I'm allowing change so, Take a good look, this is me. This is what I've come to be\"",
    "{lena} : \"FM comes in different colors, I believe... In the sewing machine, I've lost myself... Memories inside my heart are there to grieve... Color-coded by the love she gave to me...\"\n{luna} : \"Nostalgique ?\"\n{lena} : \"En quelques sortes, je suppose...\"",
    "{sixtine} : `Arr??te de dessiner` Hum... Enfaite Anna... heu... comme tu est une fant??me tu peux poss??der des gens ?\"\n<:anna:943444730430246933> : \"?? vrai dire, pas vraiment... par contre Belle...\"\n`Les deux se tourn??rent vers le miroir le plus proche o?? le reflet de Sixtine n'??tait absolument pas l?? o?? il devrait ??tre, mais en train de fouiller dans le reflet de la bo??te ?? bijoux d'Alice`\n{sixtine} : \"... C'est bien ce qu'il me semblait...\"",
    "{gweny} : \"Hey Cl??mence ! Tu veux faire une partie de paintball avec moi ce soir ?\"\n{clemence} : \"Pourquoi pas, mais il y aura Lena ?\"\n{gweny} : \"Hum...\"\n{clemence} : \"...\"\n{gweny} : \"...\"\n{clemence} : \"Je vais mettre plusieurs couches de tee-shirts\"\n{gweny} : \"Bonne id??e, je vais faire de m??me\"",
    "{clemence} : \"H?? Ly. Il faut qu'on parle.\"\n<:ly:943444713212641310> : \"A-Ah ?\"\n{clemence} : `La fixe du regard en croisant les bras pendants de longues secondes` \"Oh et au final nan j'ai pas envie. J'esp??re juste pour toi que tu fais un minimum attention au pass?? de ceux que tu ??limines et que tu ne te t'attaques pas ?? ceux qui se contente de vivre leur vie o?? aident les humains. Sinon tu risques d'avoir une vampire l??g??rement plus corriaces que les autres sur les bras.\"",
    "{clemence} : \"H?? Shihu, tu veux un conseil gratuis ? Si tu cr??ais une formule, arrange toi pour que tu n'ai pas ?? la regr??ter quand tu seras plus grande\"\n{shihu} : \"Genre pas \"Turlututu et Tralala\" ?\"\n{clemence} : \"Exactement\"\n{alice} : \"Ca reste tout de m??me mieux que \"Magicabou la magicabou et magici magica bou\"\"",
    "{alice} : \"Tu veux que je te dise U??-BB4, chez moi tu es une tueuse en s??rie qui a terroris?? la capitale pendant une d??c??nie avant de disparaitre dans la nature avec le titre de personne la plus recherch??e de la dimension\"\n{lena} : \"Si tu veux jouer ?? ce jeu, chez moi tu es une vampire qui a arr??t?? de grandir ?? l'??ge de 11 ans et demi\"\n{alice} : \"Oh la poisse\"",
    "{lena} : \"U??-BB4, vu que tu te d??brouille plut??t bien ?? longue distance, tu sais comment faire pour shotter un snipeur qui arr??te pas de nous faire chier ?\"\n{lena} : \"H?? bah tu peux toujours essayer de combattre le feu par le feu, il me semble que tu as des snipeurs dans l'EEV3 A??-E9A, non ?\"\n{lena} : \"Ils se font tous surpasser malheureusement...\"\n{lena} : `Soupir` \"Soit. Je m'en occupe. Tu peux me montrer la direction stp ? Ca fait un moment que je suis pas all?? dans le secteur A?? du multivers\"",
    "{gweny} : \"Tiens Kara?? ??a faisait un moment\"\n`La poup??e vint hug la jambe de Gwen sans rien dire`\n{gweny} : \"Ah. Je vois `Gwendoline prit la poup??e des ses bras en lui caressant doucement la t??te` Vas-y je t'??coute...\"\n{karai} : \"Pourquoi est-ce que je dois endurer tout ??a... 300 ans ?? attendre pour qu'au final ma place soit prise par une autre version de moi-m??me... Et par dessus ??a je peux m??me pas en finir...\"\n{gweny} : \"... Je n'ai pas de r??ponse ?? t'apporter malheureusement...\"\n\n{karai} : \"Prend soins de ton p??re pour moi s'il te pla??t...\"\n{gweny} : \"Honn??tement je ne pense pas qu'il ai vraiment besoin que je veille sur lui mais j'y penserais\"\n{karai} : \"Merci...\"",
    "`Gwen ??tait assise sur son lit en ??tant en train de surfer en ligne avec son ordinateur portable quand un mouvement dans le coin de la chambre attira son attention`\n{karai} : \"... Bonsoir Klironovia...\"\n{klikli} : \"Tiens, Kara??, ma poup??e pr??f??r??e `Elle prit la poup??e et la pla??a sur ses jambes tout en continuant sa navigation` Qu'est-ce qui t'am??ne donc ?\"\n{karai} : \"Oh hum... je voulais savoir si je pouvait dormir avec vous ce soir... Si ??a vous d??range pas...\"\n{klikli} : \"Moi ??a me va, et je pense pas que ??a d??range les autres non plus. Mais je d??cline toute responsabilit?? au cas ou tu te retrouve sous moi durant la nuit\"\n{karai} : \"C'est un risque que je suis pr??te ?? prendre...\"",
    "{karai} : \"Ainsi donc avec Clara tu es devenue une soigneuse Alty...\"\n{alty} : \"??a pose un probl??me particulier ?\"\n{karai} : \"Oh heu non ??vidammant ! C'est juste que... dans ma timeline tu ??tait plut??t du genre shinobi... ??a me fait bizarre c'est tout...\"\n{alty} : \"Si j'en crois que ce les autres m'ont dit ce changement est plus ou moins... logique\"",
    "{alty} : \"Et voil?? ^^ Et ??vite de courir trop vite la prochaine fois sinon tu vas retomber\"\n{shushi} : \":< Je veux un bisou magique !\"\n{alty} : \"Oh. `Fait un bisou sur le genou de Shushi` Et voil?? ^^\"\n{shushi} : \"Viiii :D\"",
    "{luna} : \"H?? Gwen, je me demandais, mais on peut ??changer nos ??p??es pour quelques minutes s'il te pla??t ?\"\n{klikli} : \"Hum, si tu veux mais pourquoi ?\"\n{luna} : \"Tester.\"",
    "<:stella:958786101940736061> : \"Oh Nacia' ! Tu te d??brouilles avec ton r??chauffement atmosph??rique en ce moment ?\"\n<:nacialisla:985933665534103564> : \"On peut pas vraiment dire que tu m'aide Stella...\"",
    "<:kitsune:935552850686255195> : \"Oh c'est toi. Ta vandetta est toujours dans tes projets ? Il me semble que la population d'humains ?? quand m??me sacr??ment diminu??e ces derni??res ann??es. Enfin... pas que les humains.\"\n<:nacialisla:985933665534103564> : \"On fait pas d'omelette sans casser des oeufs. Et pour r??pondre ?? ta question, j'ai tout de m??me pr??vu de leur faire quelques piq??res de rappels de temps en temps\"\n<:kitsune:935552850686255195> : \"J'aimerais juste que tu te souvienne qu'il y a pas que ces primates qui souffres de tes crises.\"\n<:nacialisla:985933665534103564> : \"Et je te rappelle que le g??nocide de tes d??cendantes n'a rien ?? voir avec moi.\"\n<:kitsune:935552850686255195> : \"Oh je ne parlais pas que pour mon \"esp??ce\" tu sais.\"",
    "<:lia:908754741226520656> : `Est couch??e dans l'herbe avec ses soeurs ?? regarder les nuages` \"Dites... Vous pensez qu'on a combien de soeurs, ni??ces, petites ni??ces etceteras... ?\"\n<:lie:908754710121574470> : \"Hum... Tu connais tr??s bien la r??ponse Lia...\"\n<:lia:908754741226520656> : `L??ve un bras au ciel comme pour essayer d'attraper les ??toiles en soupirant` \"Je reformule... Vous pensez qu'elles sont combien l?? haut ?\"\n<:lio:908754690769043546> : \"... J'aurais voulu les conna??tres aussi...\"\n<:lie:908754710121574470> : `Se redresse en regardant ses soeurs` \"??a ne sert ?? rien de s'apitoyer sur leurs sorts. Oui plus d'un millier d'ann??es nous s??pare de la mort de la derni??re repr??sentante de notre esp??ce, mais le fait est que Maman a r??ussi ?? se lib??rer et que nous as donn?? naissance. On est peut-??tre les kitsunes les plus jeunes ?? l'heure actuelle, mais de nous a le potenciel pour augmenter dragstiquement notre d??mographie\"\n<:liu:908754674449018890> : \"??a me fait bizarre de penser qu'on est en m??me temps tout en bas de l'arbre g??n??alogique mais en m??me temps tout en haut...\"\n<:lie:908754710121574470> : `Secoue la t??te` \"On est ni en bas ni en haut. On est une nouvelle branche ?? part enti??re\"",
    "<:rdmEvilGuy:866459027562954762> : \"Rien ni personne ne pourra m'arr??ter ! Mon plan est parfait et j'ai anticip?? toutes les possibilit??s ! Lorsque j'aurais assujeti le monde, personne ne remettra mes id??es en question et je serais enfin reconnu pour mon g??nie ! Puis je le d??truirais apr??s avoir termin?? mon vaiseau galactique et j'ira asurjetir la galaxie ! Et lorsque ??a sera fait, je la d??truirais ??galement parceque je le peux et que j'en ai les moyens ! Mon arm??e de robot est invincible et vous allez toutes mourirs dans d'affreuses souf-ARG !\"\n<:helene:906303162854543390> : \"Shehisa !\"\n<:shehisa:919863933320454165> : \"Oh vous comptiez ??couter son discourt pendant encore longtemps ? Vous savez pas comment c'est stressant de rester invisible derri??re les gens en attendant le moment parfait pour les planter une dague dans la nuque...\"\n<:icealia:909065559516250112> : \"Oh non tu as bien fais je commen??ais ?? en avoir marre aussi\"",
    "<:benedict:958786319776112690> : \"M??me si cette id??e me pla??t toujours pas, je dois avouer que tu fais une bonne enfant de coeur, tu as une plut??t bonne bouille quand tu as pas la bouche grande ouverte\"\n{alice} : M-merci ma Soeur, je suppose...\"",
    "<:benedict:958786319776112690> : \"Alice, m??me si je le con??ois tu chantes tr??s bien, est-ce que tu pourrais essayer de ne pas couvrir les autres ?? la chorale ? C'est un coeur, pas un solo\"\n{alice} : \"D-D??sol??e je m'en rend pas compte...\"",
    "{shihu} : \"Il me faut des cristaux magiques sinon je vais jamais y arriver...\"\n{shushi} : \"Tu en fais trop Shihu... Tu t'??puises pour rien, c'est pas grave si on y arrive pas...\"\n{shihu} : \"On doit y arriver sans l'aide de personne... On en peut plus de se faire rabaiss??e par Cl??mence d??s qu'elle en a l'occasion, je veux lui montrer qu'on est capacle de r??ussir l?? o?? elle a ??chou?? et lui rabatre le clapet... Pour une fois...\"\n{shushi} : \"Cl??mence a plus de quatre fois notre ??ge... On peut pas rivaliser !\"\n{shihu} : \"Mais on a quelque chose qu'elle n'a pas : Une r??serve presque infinie de l'une des quatres ??nergies qui r??gient l'univers.\"\n{shushi} : \"T-Tu va finir par disparaitre si tu continue comme ??a... J'ai... j'ai pas envie de me retrouver seule...\"\n{shihu} : \"... ??a serait peut-??tre mieux ainsi... Ma simple existance a d??bilement compliqu?? la tienne...\"\n{shushi} : `Prend spontan??ment le controle de sa main droite pour se gifler elle-m??me` \"Je t'interdis de penser ce genre de truc tu m'entends !?\""
]

shopEventEndYears = [
    "{lena} : \"Alors Shu' tu as des r??solutions pour l'ann??e ?? venir ^^ ?\"\n{shushi} : \"R??...so...lu... quoi ?\"",
    "{clemence} : \"Tu t'es surpass??e pour ta robe de no??l cette ann??e Alice\"\n{alice} : \"Tu trouves ^^ ?\"\n{clemence} : \"Puisque je te le dis x)\"",
    "{feli} : `Fait des calins ?? tous le monde` \"Bonne ann??e ^??^ !\"",
    "{shihu} : \"Mmg pourquoi il y a tout qui brille en ce moment... j'y vois rien...\"",
    "{icelia} : \"Vous avez pr??vu un truc pour cette fin d'ann??e, vous ?\"\n{shehisa} : \"Oh on comptait juste aller voir nos parents, ??a fais un moment qu'on n'est pas all?? leur faire un coucou",
    "{sixtine} : \"Mais puisque je te dis que ce pull me va tr??s bien...\"\n{alice} : \"Alleeeeez :<\"",
    "{alice} : `Regarde les babies roses ?? ruban que lui a offert Iliana` ...\n{sixtine} : \"Elle veut juste devenir ton amie... tu sais...",
]

shopEventOneDay = [
    {"date": (19, 1),
     "tabl": [
        "{shushi} : \"Joyeux naniversaire Miman !\" `Lui donne un joli dessin fait avec Sixtine`\n{lena} : \"Oh ^^ Merci Shu'\"",
        "{lena} : \"H?? L??na ! J'ai le droit ?? un jour de cong?? pour mon anniversaire ?\"\nC'est pas comme si tu ??tais un OC super occup??e...",
        "{feli} : \"Joyeux anniversaire Maraine ^??^\"\n{lena} : \"Merci F??li ^^\"",
        "{lena} : \"Le temps passe mine de rien... Et c'est pas parceque je n'ai pas de forme physique que je ne le ressent pas\"\nSi je peux me permettre, tu as quand m??me grandit depuis ton premier chara-desing\n{lena} : \"Tu me fais toujours de la m??me taille qu'Alice par contre.\"",
        "{lena} : `Regarde Shushi courir apr??s des ballons de baudruche` \"Parfois je me demande ?? quoi ressemble une vraie enfance...\"\nTu n'en a pas eu une super d??sagr??able pourtant\n{lena} : `Soupir` \"Tu sais tr??s bien que la seule enfance que j'ai ce sont les souvenirs que tu m'en a donn??\"",
        "{lena} : \"J'aurais pens?? que tu te ferais plus pr??sente aujourd'hui tout de m??me. Techniquement, c'est ton anniversaie aussi\"\n{luna} : \"Je comprend pas vraiment ce d??lire des \"anniversaires\"\""
    ]
    },
    {"date": (14, 2),
     "tabl": [
        "{lena} : `Soupir` \"Je dirais pas non ?? un petit chocolat chaud aujourd'hui...\"",
        "{clemence} : \"Alors Alice, pr??te ?? ??tre la boureau des coeurs du col??ge ?\"\n{alice} : \"Si tu crois que ??a m'amuse...\"",
        "{lena} : `Regarde Ly dormir sous un arbre ?? l'aur??e de la for??t` Je sais pas pourquoi je l'aurais pens?? plus active aujourd'hui...",
        "<:john:908887592756449311> : \"Hum... Cl??mence ? J'ai... des chocolats pour toi...\"\n{clemence} : \"Hum, d??sol??e, mais je dirg??re pas trop les chocolats ^^'\"\n{alice} : `Facepalm derri??re le dos de la vampire`"
    ]
    },
    {"date": (17, 4),
     "tabl": [
        "{alice} : \"H?? Cl??mence :D Regarde tous les oeufs que j'ai trouv??s !\"\n{clemence} : \"Effectivement c'est beaucoup\"",
        "{sixtine} : \"Cl??mence... ? Hum... Tu veux partager un oeuf en chocolat... ?\"\n{clemence} : \"D??sol??e Sixtine... tu sais bien que je dig??re pas le chocolat...\"",
        "{lena} : \"J'ai jamais compris pourquoi les gens cachent des oeufs en chocolat pour P??ques\"\n{luna} : \"??a ne t'emp??ches pas de le faire quand m??me\"\n{lena} : \"En m??me temps, m??me toi tu ne peux pas ??tre insensibles ?? toutes leurs bouilles heureuses\"\n{luna} : \"??vite de parler en mon nom s'il te pla??t... Mais oui\"",
        "{feli} : \"Aller Cl??mence viens chercher avec nous !\"\n{clemence} : \"Avec une main ??a va ??tre compliqu??\"\n{feli} : '^' \"Tu n'as qu'?? porter le panier !\""
    ]
    }
]

shopSeasonWinter = [
    "{clemence} : `Lit un grimoire en ??tant assise sur un fauteuil devant la chemin??e`",
    "{lena} : \"F??li, si tu pouvais arr??ter de dormir dans le feu ??a m'arrangerais pas mal\"\n{feli} : \"Bah pourquoi :< ?\"\n{lena} : \"Parceque apr??s tes soeurs et Shushi veulent faire la m??me chose. Et elles, elles ne sont pas fireproof.\"\n{feli} : \"Oh\"",
    "{alice} : `Boit un chocolat chaud en ??tant assise sur un fauteuil devant la chemin??e`\n{sixtine} : `Arrive dans le salon avec sa couette sur les ??paules et monte dans le fauteuil pour se blottir contre Alice`\n{alice} : \"??a va pas ?\"\n{sixtine} : \"Juste un cauchemar...\"\n{alice} : `patpat`",
    "{clemence} : `Regarde F??licit?? de haut en bas` \"Toi tu as encore dormi dans la chemin??e\"\n{feli} : \"D: Non c'est faux !\"\n{clemence} : \"Tu es pleine de cendres, s'il te pla??t x)\"",
    "{lena} : `Descend dans le salon ?? 3h du matin pour prendre un verre d'eau et voit une boule de poils blancs devant la chemin??e` \"C'est pour ??a qu'on porte des v??tements, Lio\"\n<:lio:908754690769043546> : `Eternue dans son sommeil`\n{lena} : `Soupir, remet une buche dans la chemin??e puis pose une couverture sur la grosse boule de poils`",
    "{lena} : \"`Aide Altikia ?? ranger les courses` Dit-moi... elles t'ont fait un truc les vampirettes ou comment ??a se passe ?\"\n{alty} : \"Hum ? Oh tu parles des gouses d'ails ? Bah Alice dort chez une amie et Cl??mence a dit qu'elle passerait la nuit ?? la biblioth??que donc je me suis dit que c'??tait l'occasion de changer un peu le menu ^^\"\n{lena} : \"Il va falloir passer un sacr?? coup de d??odorisant...\"",
    "{gweny} : \"Ta m??re ne va pas ??tre contente si elle te choppe en train de fouiller dans son atelier\"\n{shushi} : \"Gwen, tu sais pourquoi Miman a autant de balles incendiaires ? Son ??l??ment c'est plut??t la glace, non ?\"\n{gweny} : \"D??tourne pas le sujet. Mais pour r??pondre ?? ta question, je pense que ??a remonte ?? l'??poque o?? j'??tait encore flic ?? la ville. L'une des membres de la mafia locale ??tait d'??l??ment M??tal Pur et il me semble que ta m??re et elle se connaissaient personnellement. Et c'??tait pas l'amour fou entre les deux. Il me semble m??me que c'est la seule personne que Lena craind encore aujourd'hui, m??me si ??a fait des ann??es qu'elle n'a pas donn?? signe de vie. Et tu connais ta m??re, quand quelque chose la contrari elle pr??f??re contre attaquer, d'o?? le fait qu'elle ai pass?? pas mal de temps ?? mettre au point ces balles\"\n\n`Gwendoline se pencha pour prendre l'une des balles et l'observa attentivement pendant quelques secondes`\n\n{gweny} : \"Si je n'abuse, celle-l?? est pr??vu pour p??n??trer un blindage ultra-??pais et exploser ?? l'int??rieur en lib??rant des sharpels explosifs. De quoi te descendre un ??licopt??re blind?? d'une balle au vu de la puissance du fusil de Lena, si tu veux mon avis\"\n{shushi} : \"Wow...\"\n{shihu} : \"Je comprend mieux pourquoi elle veut pas nous voir jouer ici...\"",
    "{helene} : \"Ah Shi' ! Je t'ai fait une nouvelle tenue en fourure tu en pense quoi ?\"\n{shehisa} : `Prend la tenue et va se changer, puis se regarde dans un miroir` \"Hum... elle me plait bien. Et c'est vrai que je me sensait un peu... sous-v??tue ces derniers temps\"\n{helene} : \"Quelle id??e de porter des trucs aussi cours en hiver aussi...\"",
    "`Gwen descendit dans le s??jour pour aller pr??parer le petit d??jeun?? quand elle vit Lena en train de dormir sur le canap??. Sur la table se trouve plusieurs pi??ces de ce qu'elle devina ??tre un nouveau fusil longue port??e et en d??duit que l'inkling a encore veill?? jusqu'?? point d'heure pour mettre au point un nouveau joujou\nEn approchant, elle vit Shushi assise ?? c??t?? de sa m??re en train d'essayer de r??soudre un Rubik's cube silencieusement. En la voyant arriver, celle-ci mit doucement un doigt sur ses l??vres. Gwen lui sourit gentiment puis alla dans la cuisine`",
    "{clemence} : `Attend le trio de soeur en lisant assise (?? l'ombre) ?? la terrasse d'un caf?? tout en discutant avec Gwen, quand elle vit Sixitine venir seule` \"Comment ??a tu es toute seule Sixtine ? O?? sont F??li et Alice ?\"\n{sixtine} : \"F??li a dit qu'elle voulait aller voir la derni??re exp??dition sur les dieux de la Gr??ce Antique et Alice a... dit un truc ?? propos de l'Eglise je crois...\"\n{clemence} : \"... Gweny, tu veux bien t'occuper d'aller chercher Alice et je me charge de F??li ?\"\n{gweny} : \"Je suis pas vraiment la bienvenue dans les ??glises catholiques aussi tu sais ?\"\n{clemence} : \"D??j?? moins que moi...\"\n{sixtine} : \"Je peux y aller moi si vous voulez... Je suis qu'humaine...\"",    
]

shopSeasonSpring = [
    "{alice} : `Est assise sur une commode devant une f??netre et regarde la pluie arroser ses fleurs`",
    "{alice} : `Plante des fleurs dans le jardins tandis que Sixtine regarde les nuages`",
    "{luna} : \"Dans notre ancien chez nous les fleurs mourraient si elles avaient trop de Lumi??re\"\n{iliana} : \"Vraiment toutes ? M??me ici il y a des fleurs qui vivent dans l'ombre\"\n{luna} : \"?? quelques exeptions pr??s, effectivement\"",
    "{lena} : \"Surtout tu oublie pas ton parapluie !\"\n{shushi} : \"Mais il fait grand soleil !\"\n{lena} : \"Il peut tr??s rapidement se mettre ?? pleuvoir ?? cette saison, Shu'\"",
    "{alice} : \"J'ai hate que l'??t?? arrive ! Tu viendras avec nous ?? la plage Cl??mence :D ?\"\n{clemence} : \"Hum, tu veux dire sous un soleil de plomb en maillot de bain avec la mer qui fait ses remous juste ?? c??t?? alors que je d??teste l'eau et arrive ?? me chopper des coups de soleil en hiver et sans reflets sur la neige ?\"\n{alice} : \"... D??sol??e c'??tait stupide...\"",
    "<:anna:943444730430246933> : \"H?? Alice, tu en penses quoi de cet ensemble... ?\"\n{alice} : \"Un peu viellot, mais ??a te va bien\"",
    "{lena} : \"Oh est surtout, ??vitez de tra??ner trop avec Lia s'il vous pla??t. Le printemps est sa saison de pr??dilection\"",
    "<:determination:867894180851482644> :\"`S'??tire` C'est un chouette printemps que nous avons l??\"\n{alice} : \"Dis Chara... tu avais promis de m'aider avec mes fleurs :<\"\n<:determination:867894180851482644> : \"Oh mais je l'ai fais, pourquoi crois-tu qu'il y a une golden flower au milieu ?\"\n{alice} : \"Oh heu... c'est pas vraiment ce que je voulais dire par l?? mais... merci quand m??me\"\n<:determination:867894180851482644> : \"`Facepalm` Ah tu demandais des conseils en jardinage normal, c'est ??a ?\"\n{alice} : `Hoche la t??te`",
    "<a:Ailill:882040705814503434> : \"Est-ce que tu t'es d??j?? demand??e quel go??t avait le sang ?\"\n{lena} : \"Non merci, et si vraiment j'ai envie de savoir, je pr??f??re demander aux vampirettes plut??t qu'?? toi.\"\n<a:Ailill:882040705814503434> : \"Tu es pas dr??le tu sais\"",
    "{sixtine} : `Regarde les ??toiles dans une prairie, puis remarque qu'elle n'est pas seule` \"... toi aussi tu brillais autant ?? l'??poque o?? tu ??tais une ??toile aussi... ?\"\n<:powehi:909048473666596905> : \"Et comment ! J'??tais la plus grande, la plus chaude et la plus brillante de ma r??gion...\"\n{sixtine} : \"Tu avais un syst??me plan??taire aussi ?\"\n<:powehi:909048473666596905> : \"Trois. Elles ??taient plut??t sympatiques, et l'une d'entre elle abritait m??me la vie mais... `Soupir` Elles...\"\n{sixtine} : \"... Au moins je suis s??re qu'elles ont bien aim??e ta supernova...\"\n<:powehi:909048473666596905> : \"Je... je pense... Leurs repr??sentations se tenaient les mains sans vraiment avoir l'air effray??es...\""
]

shopSeasonsSummer = [
    "{alty} : \"Tu devrais aller dormir, Lena\"\n{lena} : \"C'est pas parceque tu fait deux t??tes de plus que moi que tu es sens?? agir comme ma m??re Altikia\"\n{alty} : \"Lena... Tu as dormis que 3h en deux jours... Et regarde moi ce nombre de canettes de Coca... Je sais pas ce que tu fais, mais je suis s??re que ??a peut attendre une bonne nuit de sommeil\"\n{lena} : \"??a va, t'en fais pas\"\n{alty} : \"??a fait deux fois que tu d??vise et revise la m??me vis dans le m??me trou depuis qu'on parle\"\n{lena} : \"Peut-??tre qui si tu arr??tais de me parler je serais plus concentr??e, effectivement.\"\n{alty} : \"`Soupir` Tu es en train de te d??foncer la sant?? et je doute fortement que le jeu en vale la chandelle. Maintenant tu va aller te coucher ou sinon tu va voir que mes deux t??tes suppl??mentaire vont faire une bonne diff??rence quand je vais te forcer ?? y aller.\"\n{lena} : \"`Se l??ve d'un coup pour aller confrontrer Altikia, ce qui f??t une erreur puisque qu'elle f??t imm??diatement prise de vertige et ses jambes se d??rob??rent sous elle. Puis elle soupira` Tu as peut-??tre pas tord au fond...\"\n{alty} : \"Tu vois ?\"",
    "{alice} : \"Cl??meeeence ? Tu peux venir nous surveiller pendant qu'on se baigne dans le lac s'il te pla??t :< ? On voudrait apprendre ?? Shushi ?? nager\"\n{clemence} : \"Hum... Tu me demande ??a ?? moi alors qu'il n'y a pas un nuage dans le ciel ?\"\n{alice} : \"Tu te doute bien que si je le fais c'est qu'il n'y a pas d'autres options... Gwen et Lena sont en ville aujourd'hui\"\n{clemence} : \"`Soupir` Je vais chercher des lunettes de soleils et le plus grand parasol de que je peux trouver alors... Mais si il arrive quoi que ce soit dans l'eau, c'est F??li qui s'en charge.\"\n{feli} : \"Capiche !\"\n{alice} : \"Viiii ^??^ Merci Cl??mence\"",
    "{sixtine} : \"`Fixe le plafond en arrivant pas ?? dormir lorsqu'elle entendit un b??tement d'ailes et senti une chauve-souris se blotir contre sa t??te` Un chauchemar ?\"\n{alice} : `R??pond par un petit couinement affirmatif`\n{sixtine} : `La prend doucement dans ses mains et la place contre sa poitrine en lui carressant la t??te avec son pouce`\n{alice} : `Finit par se rendormir berc??e par les b??tements de coeurs de sa soeur et ses caresses`",
    "<:liu:908754674449018890> : \"C'est pas parcequ'il fait chaud que tu dois porter encore moins de v??tements Liz tu sais ?\"\n<:lie:908754710121574470> : \"Je vois pas pourquoi tu me reproche ??a alors que tu dis rien ?? Lio. Et puis c'est la mode en ce moment\"\n<:liu:908754674449018890> : \"Ton short est tellement bas qu'on voit ta culotte...\"\n<:lie:908754710121574470> : \"Et ? C'est dans notre nature tu sais d'??tre attrayante\"\n<:liu:908754674449018890> : \"C'est pas de l'attrayance ??a c'est de la provocation, tu va finir par te faire vi... Ah. C'est exactement ce que tu veux enfaite, n'est-ce pas ?\n<:lie:908754710121574470> : \"D??j?? 3 fois cette semaine, c'est fou ce que les males humains peuvent ??tre irresponsables en ce moment :D\"\n<:liu:908754674449018890> : \"... Il en reste d??j?? plus tant que ??a tu va pas tous leurs piquer leurs ??mes en trois mois quand m??me...\"",
    "<:ruby:958786374759251988> : \"Julie, tu sais que tu as l'autorisation de porter ce que tu veux tant que c'est rouge en ??t??, n'est-ce pas ?\"\n<:julie:910185448951906325> : \"Bien s??r Madame, mais je me sens moins ?? l'aise lors de mon travail si je ne porte pas mon uniforme\"\n<:ruby:958786374759251988> : \"Tu es s??r ? Tu dois ??tre en sueur toute la journ??e avec pourtant\"\n<:julie:910185448951906325> : \"`Avec une courbette` ??a ne me d??range pas, Madame. Et puis ??a rend le bain du soir que plus agr??bale\"",
    "{lena} : \"Arr??tez de vous plaindre ??a fait ?? peine une heure qu'on est en randonn??. Et est-ce que Cl??mence s'est plainte elle ? `Se retourne vers le groupe` Huh\"\n{sixtine} : \"`Soul??ve sa casquette humide pour r??v??ler la chauve-souris en train de faire l'??toile de mer dans ses cheveux` Elle a fait une insolation d??s les dix premi??res minutes...\"\n{lena} : `Soupir`\n<:edelweiss:918451422939451412> : \"Si vous voulez il y a un lac ombrag?? pas trop loin pas trop loin\"\n{lena} : \"Oh bonjour Edelweiss. Et je pense que c'est un bon endroit pour faire une pause effectivement...\"",
    "{helene} : \"Cl??mence vous me donnez chaud ?? ??tre aussi v??tue...\"\n{clemence} : \"La seule chaleur que je ressent est celle des UV du soleil donc ??a va t'??tonnner mais je me sens plut??t au frais actuellement\"",
    "<:lio:908754690769043546> : `Regarde Alice et Sixtine essayer d'apprendre ?? nager ?? Shushi depuis le fond de son lac`\n{feli} : \"Coucou !\"\n<:lio:908754690769043546> : `Sursaute (peut-??tre vraiment parler de sursaut quand on flotte dans l'eau ?)` \"Oh c'est toi... J'oublie toujours que tu peux respirer sous l'eau aussi...\"\n{feli} : \"??a t'arrive jamais de sortir de ton lac de temps en temps ? Enfin ?? part pour ralonger nos combats\"\n<:lio:908754690769043546> : \"Mais j'aime bien mon lac moi... et puis il y a trop de probl??mes l?? haut... Et pour ton deuxi??me point, les combats sont plus interressant contre vous qu'avec. C'est toujours trop rapide avec vous...\"\n{feli} : \"Oula, ?? ne pas sortir du contexte celle-l??\"\n<:lio:908754690769043546> : \"Oh hum... d??sol??e...\"",
    "{gweny} : `S'??croule dans son lit` \"J'en peut plus de ces canicules je dois changer de tee-shirts trois fois par jours...\"\n{karai} : `Ricane depuis l'??tag??re` \"Tu as toujours eu ce genre de probl??me Gweny\"\n{gweny} : \"??a m'aide pas vraiment ??a Kara??...\"",
    "{alice} : `Regarde Iliana sous sa forme de chat en train de faire l'??toile de mer par terre` \"Hum... Tu... tu sais que tu aurais moins chaud en forme humaine... ? Enfin... moins de fourure et la sudation tout ??a tout ??a...\"\n{iliana} : \"Lena pourra plus me saquer si elle me voit sous forme humaine pendant tout l'??t??... Et j'ai nul part autre o?? aller...\"\n{alice} : \"...\" `Monte dans sa chambre et reviens quelques secondes plus tard avec un petit ventilateur qu'elle branche ?? c??t?? de la chatte, puis elle s'assoit ?? c??t??`\n{iliana} : \"... Merci...\"",
    "{lena} : \"H?? Iliana, tu pourrais me rendre un service ?\"\n{iliana} : \"Mui ?\"\n{lena} : \"Tu as d??j?? entendu parler d'un certain Schr??dinger ?\"\n{iliana} : \"... Oh zut j'ai totalement oubli?? ! Alice m'avait propos?? de les accompagner ?? la plage, il faut que je me trouve un maillot de bain !\"",
    "{luna} : `Regarde Shushi et Shihu faire de la calligraphie, en controlant chacune leur main dominante respective`\n{lena} : \"Tu sais, si tu veux passer du temps avec elle il suffit de le dire hein\"\n{luna} : `Soupir` ?? quoi bon. Elle me consid??re s??rment m??me plus comme sa m??re, et je suis nulle pour essayer de l'??tre\"\n{lena} : \"Tu te trompes. Quoi qu'il arrive, tu seras toujours sa m??re. Elle s'est juste faite ?? l'id??e qu'elle ne pourra pas avoir une relation \"normale\" de file-m??re avec toi, et elle essaye de l'avoir avec moi ?? la place\"\n{luna} : \"??a me motive encore moins ?? essayer, ??a Lena\"\n{lena} : \"Ce que je veux dire, c'est que ce n'est pas en restant cacher au fond de notre ??me que ??a va changer les choses, Luna\"",
    "`C'est l'heure du beach ??pisode ! Dans l'eau en face de vous vous pouvez observer le trio de soeurs et Shihu en train de jouer avec un ballon de plage dans la mer\nUn peu plus sur le c??t?? vous pouvez voir Lia et Liz qui louchent pas mal sur un groupe de surfeur en ??tant ?? moiti?? jalouses du fait que Liu est parmis eux alors qu'elle ne semble pas vraiment ??tre affectu??e par la chad attitude qu'ils lib??rent\nCeux qui font de la plong??e sous-marine peuvent voir Lio en bikini (pour une fois) en train de r??cup??rer les objets perdus par les nageurs et constater que quelques familles auront du mal ?? prendre leurs voitures sans leurs cl??s, et vous dites que voir une kitsune sortir de l'eau pour les leur rendre fait tr??s f??e sortant du lac et qui propose une version d'or ou d'argent d'un objet perdu\nAssise sur un rocher, vous pouvez retrouver Lena en train de lire les pieds dans l'eau tout en surveillant Gwen qui nage dangereusement pr??s en lui lan??ant des regards malicieux de temps en temps pour v??rifier si la jeune femme aux cheveux bleus fait attention ?? elle ou non\nEt enfin, coll??es l'une ?? l'autre, vous pouvez retrouver Cl??mence et Iliana qui, bien que toutes les deux en maillot de bain, ne veulent quitter l'ombre du parasol pour rien au monde`",
    "<:benedict:958786319776112690> : `Viens ?? la rencontre de Cl??mence qui attendait ?? la sortie de l'??glise` \"Tu es la soeur d'Alice, c'est cela ?\"\n{clemence} : \"C'est si compliqu?? ?? deviner ?\"\n<:benedict:958786319776112690> : `Croise les bras en faisant la moue` \"Il n'y a pas beaucoup de vampires qui attendrait pendant une dizaine de minutes devant un ??glise d'autant plus qu'il ne fait pas encore nuit. D'autant plus qu'Alice nous avait dit que tu viendrais la chercher apr??s le Chemin de Croix.\"\n{clemence} : \"Et je suppose que si ce n'est pas elle qui vient directement c'est parcequ'il s'est pass?? quelque chose ?\"\n<:benedict:958786319776112690> : \"Elle a perdu connaissance en milieu d'apr??s-midi et ne s'est toujours pas r??veill?? depuis. Je pense que le soleil de plomb et la symbolique du chemin n'a pas fait du bien ?? ses... origines, aussi... r??sistante soit-elle. Peut-??tre que toi qui t'y connais un peu mieux sur ce sujet pourrait la r??veiller. Si c'est le cas, je t'autorise ?? rentrer dans l'??glise pour aller la voir.\"\n{clemence} : `Soupir` \"Si un jour on m'aurait dit qu'on m'inviterais ?? rentrer dans une ??glise...\"",
    "{clemence} : \"Hum... O?? est Alice ?\"\n{feli} : \"Elle ??tait avec nous non ?\"\n<:anna:943444730430246933> : \"Je croyais qu'elle t'avais rejoint apr??s le Palais des Glaces Cl??mence !\"\n{clemence} : \"... Attendez... Vous avez emmen?? Alice, qui n'a aucun sens de l'orientation ni reflet dans un Palais des Glaces au beau milieu d'une f??te foraine tellement bruyante que j'ai du mal ?? ne pas me cogner contre un mur si je me fit qu'?? mes oreilles alors que je suis bien plus exp??riment?? qu'elle en echolocalisation et ne l'avez m??me pas attendue ou aid?? !?\"\n{feli} : \"Elle mettait tellement longtemps on a pens?? qu'elle ??tait d??j?? sortie '^' !\"\n{clemence} : `Facepalm`\n<:anna:943444730430246933> : `Regarde ses pieds pas tr??s fi??re d'elle et jette un coup d'oeuil ?? la vitrine la plus proche`\n<:belle:943444751288528957> : `Roule des yeux et sort du cadre de la vitrine`",
    "{iliana} : `Saute sur un lit (avec sa forme de chat) et s'instale confortablement pour la nuit mais a une r??v??lation` \"Le lit de Shushi c'est le deuxi??me depuis la porte, c'est ??a ?\"\n{alice} : `Hoche lentement la t??te en tramblant un peu`\n{iliana} : \"D-D??sol??e ! Vos deux lits se ressemblent beaucoup dans le noir et depuis le sol !\" `Se rel??ve et s'appr??te ?? sauter`\n{alice} : \"A-Attent... tu peux rester si tu veux...\"\n{iliana} : \"Tu... es s??re ?\"\n{alice} : `Hoche une nouvelle fois la t??te lentement` \"Cl??mence... veut vraiment que je fasse des efforts avec toi et... F??li n'a pas tord non plus quand elle dit que tu risques pas d'essayer de me manger, encore moins sous ma forme humaine donc... je... je veux bien... hum... te laisser une chance ?\"{iliana} : `Regarde les yeux roses d'Alice qui brillaient l??g??rement dans le noir puis viens ?? sa hauteur et se couche contre elle en ronronnant`",
    "{lena} : \"Au fait Krys, je dois te rajouter au club des hydrophobes ? T'en fais pas on mord pas. Enfin peut-??tre Iliana mais premi??rement elle le fait que si elle est vraiment ??nerv??e et de deux je pense qu'elle s'y casserais les dents avec toi.\"\n<:krys:916118008991215726> : \"Le club des quoi ?\"",
    "<:lia:908754741226520656> : \"Pourquoi c'est moi qui doit garder mes petits fr??res et soeurs !?\"\n<:kitsune:935552850686255195> : \"Parceque Lio est occup??e. Tu verras ils sont pas m??chants, par contre cette port??e l??-\"\n<:lia:908754741226520656> : \"Laisse moi deviner, adores jouer dans les queues de leur m??re ?\"\n<:kitsune:935552850686255195> : \"Pourquoi tu dis ??a sur ce ton l?? ? Toi aussi tu aimais bien le faire ?? leur ??ge ?\"\n<:lia:908754741226520656> : \"Sauf que tu as trois fois plus de queues que moi Maman >< ! On pouvait chacun avoir la notre pour s'amuser, l?? ils sont presque ?? deux ?? me tirer sur chaqu'une d'entre elles !\"\n<:kitsune:935552850686255195> : `Ricane` \"Commence par t'assoir comme ??a tu risques pas de leur tomber dessus si ils tirent trop fort. Et c'est pas tout mais je vais devoir y aller moi, bon courage. Oh et h??site pas ?? leurs montrer quelques tours. M??me si ce sont de renardaux ordinaires, ils restent plut??t sensible ?? la magie. Ta soeur qui est actuellement en train de se frotter ?? tes jambes semble avoir une affinit?? avec le vent d'ailleurs, vous devriez bien vous entendre. `Avec un ton plus bas, sans vraiment s'adresser ?? Lia` J'aimerais bien que vous passiez plus de temps avec vos fr??res et soeurs \"ordinaires\" vous savez...\""
]

shopSeasonsAutomne = []

shopRepatition = [4, 5, 8, 3]                 # Shop's item category length

# Same, but for the roll command
rollMessage = ["Selon toute vraisemblance ce sera un **{0}**", "Puisse la chance ??tre avec toi... **{0}** !", "Alors Alice tu as obtenu combien ? **{0}** ? **{0}** alors","Sur 100, les chances que la relation Akrisk tienne debout ? Hum... **{0}**", "Le nombre de lances que tu va avoir ?? esquiver est... **{0}**"]

randomEmojiFight = [
    '<:ffsad:896113677550366740>',
    '<:ffboude:875347226170384454>',
    '<:ffshrug:895280749366878258>',
    '<:ffbored:889900326902186045>'
]

lenRdmEmojiFight = len(randomEmojiFight)
mauvaisePerdante = "\n\nUnexpected situation: The enemy has won"

randChooseMsg = [
    "?? quoi bon, de toutes fa??ons tu vas choisir ce qui t'interresse vraiment\nMais bon voil??",
    "Je doute que tu tiennes compte de mon avis mais j'ai choisi",
    "Selon l'allignement des ??toiles, tu va devoir prendre",
    "D'apr??s les r??sidus de th?? dans ma tasse...",
]

tablCat = ["D??but du combat", "Comp??tence ultime", "Transcendance", "En ??liminant un ennemi", "?? la mort", "En ??tant ressucit??", "Victoire (Bleu) en ??tant en vie", "Victoire (Bleu) en ??tant mort", "D??faite (Bleu)", "Victoire (Rouge) en ??tant en vie", "Victoire (Rouge) en ??tant mort","D??faite (Rouge)", "Bloquer une grosse attaque", "R??action ?? la r??animation de plusieurs alli??s", "R??action ?? la r??animation de plusieurs ennemis", "R??animer plusieurs allier en m??me temps", "R??action ?? l'??limination d'un ennemi", "R??action ?? l'??limination d'un alli??"]

class says:
    """A class for storing the says message from a entity"""
    def __init__(self, start=None, ultimate=None, limiteBreak=None, onKill=None, onDeath=None, onResurect=None, blueWinAlive=None, blueWinDead=None, blueLoose=None, redWinAlive=None, redWinDead=None, redLoose=None, blockBigAttack=None, reactBigRaiseAllie=None, reactBigRaiseEnnemy=None, bigRaise=None, reactEnnemyKilled=None, reactAllyKilled=None, reactAllyLb=None, reactEnemyLb=None):
        self.start = start
        self.ultimate = ultimate
        self.limiteBreak = limiteBreak
        self.onKill = onKill
        self.onDeath = onDeath
        self.onResurect = onResurect
        self.blueWinAlive = blueWinAlive
        self.blueWinDead = blueWinDead
        self.blueLoose = blueLoose
        self.redWinAlive = redWinAlive
        self.redWinDead = redWinDead
        self.redLoose = redLoose
        self.blockBigAttack = blockBigAttack
        self.reactBigRaiseAllie = reactBigRaiseAllie
        self.reactBigRaiseEnnemy = reactBigRaiseEnnemy
        self.bigRaise = bigRaise
        self.reactEnnemyKilled = reactEnnemyKilled
        self.reactAllyKilled = reactAllyKilled
        self.reactAllyLb = reactAllyLb
        self.reactEnemyLb = reactEnemyLb

    def tabl(self):
        return [
            self.start,
            self.ultimate,
            self.limiteBreak,
            self.onKill,
            self.onDeath,
            self.onResurect,
            self.blueWinAlive,
            self.blueWinDead,
            self.blueLoose,
            self.redWinAlive,
            self.redWinDead,
            self.redLoose,
            self.blockBigAttack,
            self.reactBigRaiseAllie,
            self.reactBigRaiseEnnemy,
            self.bigRaise,
            self.reactEnnemyKilled,
            self.reactAllyKilled
        ]

    def fromTabl(self, tabl: list):
        self.start = tabl[0]
        self.ultimate = tabl[1]
        self.limiteBreak = tabl[2]
        self.onKill = tabl[3]
        self.onDeath = tabl[4]
        self.onResurect = tabl[5]
        self.blueWinAlive = tabl[6]
        self.blueWinDead = tabl[7]
        self.blueLoose = tabl[8]
        self.redWinAlive = tabl[9]
        self.redWinDead = tabl[10]
        self.redLoose = tabl[11]
        self.blockBigAttack = tabl[12]
        self.reactBigRaiseAllie = tabl[13]
        self.reactBigRaiseEnnemy = tabl[14]
        self.bigRaise = tabl[15]
        self.reactEnnemyKilled = tabl[16]
        self.reactAllyKilled = tabl[17]

        return self

lenaSays = says(
    start="Lena, par??e ?? faire feu.",
    ultimate="Hey {target} ! J'ai un {skill} avec ton nom dessus !",
    limiteBreak="It's now or never ! {skill} !",
    onDeath="Tps.",
    onResurect="J'te revaudrais ??a {target}",
    blueWinAlive="Une victoire en bonne uniforme",
    redWinAlive="Vous avez encore des progr??s ?? faire",
    redWinDead="Pas mal. Mais pas suffisant",
    redLoose="Ahah, pas trop mal cette fois-ci. Mais ce n'??tait qu'un entrainement",
    reactBigRaiseAllie="Bien jou?? {caster}",
    reactBigRaiseEnnemy="Je dois avouer qu'il ??tait pas mal celui-l??. Je suppose que j'ai qu'?? donner le meilleur de moi-m??me de nouveau",
    reactEnnemyKilled="Pas trop mal {killer}",
    reactAllyKilled="T'en fais pas {downed}, je m'en charge.",
    blockBigAttack="H?? Luna ! Un brisage de l'Espace Temps ??a te dis ?\"*\n<:luna:909047362868105227> : \*\"C'est pas d??j?? ce que l'on ??tait en train de faire ?",
    reactEnemyLb="`Ricane` Si ??a vous chante",reactAllyLb="Belle {skill}, {caster}"
)

aliceSays = says(
    start="Ok, je vais faire de mon mieux, vous allez voir ??????(?????????) !",
    onDeath="Kya ??????(>???<) !",
    redWinAlive="Viii (?????????) !",
    redWinDead="?????????(???><???)?????????",
    ultimate="Aller tous avec moi ! {skill} !",
    blueWinAlive="Alors, vous en avez dit quoi (?????????) ?",
    onKill="J'aime pas la m??thode direct (?????????)...",
    onResurect="Pr??te pour le rappel ??????(?????????)!",
    reactBigRaiseEnnemy="Je peux le faire aussi {caster}... Pas de quoi s'en venter...",
    bigRaise="Alors alors (?????????)?",
    reactEnnemyKilled="En voil?? un qui sera pas l?? pour mon final",
    reactAllyKilled="T'en fais pas {downed} !",
    reactAllyLb="Mow, je voulais terminer en apoth??ose moi :<",
    reactEnemyLb="Pff, tu appelles ??a une d??monstration, {caster} ?",
    limiteBreak="C'est l'heure de terminer en apoth??ose !"
)

clemSays = says(
    start="`Ferme son livre` Ok allons-y",
    ultimate="J'esp??re que tu es pr??t pour te prendre un {skill} dans la face, {target} !",
    onDeath="Je t'ai sous estim?? manifestement...",
    onResurect="Merci du coup de main",
    redWinAlive="Et bah alors, on abandonne d??j?? ?",
    blueWinAlive="??a sera tout pour moi",
    reactEnnemyKilled="Pas trop {killer}",
    redLoose="Pas la peine de prendre la grosse t??te.",
    limiteBreak="Vous commencez s??rieusement ?? m'ennuyer.",
    reactAllyLb="J'aurais p?? le faire moi-m??me {caster}."
)

ailillSays = says(
    start="Tss, encore vous ?",
    onKill="Venez autant que vous ??tes, ??a changera rien",
    onDeath="Tu... paie rien pour attendre...",
    redWinAlive="Vous appelez ??a un combat ?",
    reactBigRaiseEnnemy="Parceque vous pensez que ??a changera quelque chose ?",
    reactEnemyLb="Juste une ??gratinure..."
)

jevilSays = says(
    start="Let's play a number game ! If you're HP drop to 0, I win !",
    onDeath="THIS BODY CANNOT BE KILLED !",
    redWinAlive="SUCH FUN !",
    redLoose="Such fun ! I'm exausted !"
)

lunaBossSays = says(
    start="Vous tenez tant que ??a ?? vous mettre en travers de mon chemin ?\nSoit. Je vais vous montrer qu'un pr??tresse des T??n??bres peut faire !",
    onKill="Disparait dans les ombres.",
    onDeath="Aha-",
    redWinAlive="Vous n'??tes pas les premiers. Et certainement pas les derniers.",
    redLoose="Mhf... Quand cesserez vous de suivre aveugl??ment cette Lumi??re corruptrice...",
    reactBigRaiseEnnemy="Vous devez en venir ?? l?? ? Soit !"
)

lunaDesc = """Luna est la conscience qu'ont aquis les T??n??bres inject??s dans Lena par Gaster, dans leur dimension origielle (?? Gaster et Luna, pas ?? Lena vu qu'elle vient d'ailleurs)

Dans cette dimension, les rapports entre la Lumi??re et les T??n??bres ??taient invers??s. C'??tait ces derniers qui permettaient aux habitants de voir et vitre, tandis que la Lumi??re repr??sentait ce que nous apellons \"Obscurit??\"
Luna a h??rit?? du d??sir de destruction du monde corrompu qu'??tait le leur de Gaster lorsque celui-ci a utilis??e Lena comme moyen de sortir de cette boucle g??nocidaire engag??e par Chara, et le moins qu'on puisse dire c'est qu'elle y ai parvenu

Avec une puissance d??passant toutes les simulations de Gaster (qui n'avait pas prit en compte le status de personnage principal de Lena mais ??a il pouvait pas savoir), Luna a effectivement bris?? l'emprise que portait Le Premier Humain sur la dimention, mais a ??norm??ment d??s??quilibr?? l'??quilibre entre les T??n??bres et la Lumi??re de cette derni??re, ce qui causa plusieurs perturbations dans l'Espace Temps lui-m??me qui d??chir??rent la dimension.
Cependant, puisqu'elle n'avait ??t?? cr??e que dans un seul but, la r??alisation de celui-ci n'arr??ta pas du tout Luna, qui commen??a ?? voir la Lumi??re et dimensions qui l'idolait comme une corruption de l'??quilibre du multi-verse, qu'elle estime ??tre son devoir en temps que Pr??tresse des T??n??bres de supprimer.

Bien que Lena soit parcevenu ?? reprendre le contr??le, Luna n'en a pas abandonn?? des dessins pour autant, et son manque de consistance ainsi que son caract??re t??tu et compulsif l'emp??che de vraiment se concentrer tr??s longtemps sur autre chose, au dame de sa propre fille"""

shushiAltSays = says(
    start="D??zol?? Miman... Mais on peut pa ti laizer fire.",
    onKill="Zi te plait...",
    onDeath="D-D??zol??e !",
    blueLoose="Ze ferais miheu... la prozaine fois...",
    blueWinAlive="Wiiii !",
    reactBigRaiseAllie="Bien zou?? {caster}"
)

shushiSays = says(
    start="Je vais te montrer ce que je peux faire Miman !",
    ultimate="C'est maintenant ou jamais !",
    onKill="Tu m'en voudras pas hein ? ?",
    onDeath="Miman !",
    onResurect="Ze veux encore dodo...",
    blueWinAlive="`Petite danse de la victoire` ?",
    blueWinDead="Bien zou?? !",
    blueLoose="Je vais devoir faire mieux la prochaine fois !",
    redWinAlive="Alors alors ?",
    redWinDead="Peux mieux faire !",
    redLoose="Oh..."
)

lunaSays = says(
    start="Ok, on va bien voir si vous continuez de faire les malins",
    ultimate="??a va ??tre tout noiiiiiire !",
    onKill="J'ai vu des brindilles plus solides que toi...",
    onDeath="Je retiens.",
    blueWinAlive="Et sans bavures !",
    redWinAlive="C'est eux que tu comptes recruter Lena ? Ne me fais pas rire"
)

shihuSays = says(
    start="J'essayerai de pas tout casser !",
    redWinAlive="Boum Boum",
    ultimate="Pr??parez vous ?? ressentir le pouvoir des T??n??bes !",
    onKill="Tu risques de broyer du noir pendant un moment, d??zol??e !"
)

temSays = says(
    start="HoIIII !",
    onDeath="Ayayaya !"
)

spamtonSays = says(
    start="HEY EVERY       ! IT'S ME, SPAMTON G. SPAMTON!",
    redWinAlive="DON'T FORGET TO [[Like and Subscribe](https://gfycat.com/fr/gifs/search/youtube+subscribe+button+green+screen)] FOR MORE [[Hyperlink Blocked]]!",
    redLoose="THIS IS [[One Purchase](https://www.m6boutique.com/?adlgid=c|g||383715070314|b&gclid=Cj0KCQjwlOmLBhCHARIsAGiJg7lgxkpj8jJSOEZZ_q1URCeEWFW_SmyGcVeiKz8wUmO0-LCAE9Sz4SsaAgsvEALw_wcB)] YOU WILL [[Regret](https://www.youtube.com/watch?v=u617RilV5wU)] FOR THE REST OF YOUR LIFE!",
    onKill="HOW'S AN INNOCENT GUY LIKE ME SUPPOSED TO [[Rip People Off](https://www.youtube.com/watch?v=nIxMX6uyuAI)] WHEN KIDS LIKE YOU ARE [[Beating People Up](https://www.youtube.com/watch?v=4c_eEd-ReiY)]",
    reactEnemyLb="DON'T YOU WANNA BE A [[Big Shot(https://www.youtube.com/watch?v=-8p8VowCmgE)]]!?"
)

powehiSays = says(
    start="Un nouveau cycle commence...",
    limiteBreak="Qui vous a dit que je vous laisserais faire ?",
    onDeath="Kya !",
    onResurect="Mourir, c'est toujours pas dr??le",
    reactBigRaiseAllie="On peut dire que tu sais y faire {caster}",
    reactEnemyLb="C'est beau de s'acharner inutilement..."
)

randomWaitingMsg = [
    "<a:bastuno:720237296322084905> Baston inkoming !",
    "<a:explosion:882627170944573471> Simulation de l'an??antissement ?? venir...",
    "<:invisible:899788326691823656> Erreur 404 : Blague non trouv??e",
    "{alice} \"Conseil gratuit : Les OctoBooms font mal\"",
    "<a:giveup:902383022354079814>",
    "<a:Braum:760825014836002826> I am faster than you~"
]

johnSays = says(
    start="(Courage John. Montre lui que tu as appris ?? devenir un combattant.)"
)

liaSays = says(
    start="??a vous dirait de danser avec moi ?",
    onKill="Oh d??j??... ?",
    onDeath="Hii ! Compris compris !",
    redWinAlive="C'??tait marrant !",
    redLoose="Vous savez pas rire...",
    reactBigRaiseAllie="Toujours aussi jouissif {caster}",
    reactEnemyLb="Mow, je crois qu'ils sont un peu en col??re"
)

liuSays = says(
    start="H?? ! Une course d'endurance vous en pensez quoi ?",
    onKill="Va falloir mieux g??rer ta fatigue la prochaine fois",
    onResurect="Une seconde course ?",
    redLoose="H?? bah... Finalement c'est moi qui ai mordu la poussi??re",
    limiteBreak="Pas si vite !",
    reactEnemyLb="C'est bon tu as fini {caster} ?"
)

lioSays = says(
    start="Oh... Heu... Bonjour...",
    onKill="J- J'y suis all?? trop fort ?",
    onResurect="Merci...",
    onDeath="Humf ! J'aurais du rester dans la for??t...",
    redWinAlive="Le monde des humains est... perturbant...",
    bigRaise="On lache rien...",
    reactBigRaiseEnnemy="Je peux faire ??a aussi, tu sais...",
    reactAllyKilled="Vous commencez ?? me taper sur les nerfs...",
)

lizSays = says(
    start="Tiens donc, des nouvelles braises",
    ultimate="Allez quoi, d??clarez moi votre flamme !",
    onKill="Woops, j'y suis all?? trop fort manifestement",
    onDeath="Pff, vous ??tes pas dr??le",
    redLoose="Waw, je me suis jamais faite autant refroidir rapidement...",
    reactEnemyLb="T'enflamme pas trop vite {caster}."
)

julieSays = says(
    start="J'ai pas le temps pour ??a ! Je dois encore faire la cuisine, nettoyer le hall, faire tourner une machine ?? laver et repasser les robes de Madame !",
    ultimate="Pas le choix...",
    limiteBreak="Courage vous autre !",
    onDeath="M-Madame... d??sol??e...",
    onResurect="E-elle en saura rien, hein ?",
    bigRaise="Le temps joue contre nous ! Foncez !"
)

sixtineSays = says(
    start="`Baille en s'??tirant`",
    ultimate="Laissez moi tranquille...",
    redWinAlive="Je retourne dessiner maintenant...",
    redLoose="Zzz...",
    reactBigRaiseAllie="Waw...",
    reactAllyLb="C'??tait joli ?? regarder..."
)

randomMaxDmg = [
    "Apparament, {icon} __{name}__ aurait r??ussi ?? inflig?? **{value}** d??g??ts en un seul combat, ce mois-ci ???(?????????)???",
    "H?? tu sais quoi {icon} __{name}__ ? Ton record de d??g??ts mensuel en un seul combat est de **{value}**",
    "Hum... le record de d??g??ts de {icon} __{name}__ est que de **{value}** ce mois-ci ? Pas ouf",
    "Voyons voir... Ce mois-ci, {icon} __{name}__ a fait au maximum **{value}** en un combat",
    "Une ?? droite et une ?? gauche ! {icon} __{name}__ a r??ussi ?? faire **{value}** d??g??ts avec des beignes bien plac??es ce mois-ci !"
]

randomTotalDmg = [
    "H?? {icon} __{name}__ ! Tu veux savoir combien de d??g??ts tu as fait au total ? **{value}**",
    "Aufaite, tu voulais savoir combien de d??g??ts tu a fait {icon} __{name}__ au total ? **{value}**",
    "Tu veux savoir combien de d??g??ts tu as fait {icon} __{name}__ ? Hum... **{value}** ???(?????????)???",
    "Pour {icon} __{name}__, j'ai ressenc?? **{value}** d??g??ts inflig??s jusqu'?? pr??sent"
]

randomMaxHeal = [
    "Alors voyons voir si {icon} __{name}__ est un bon healer... Son record de soins est de **{value}**, ce mois-ci",
    "Au maximum, tu as soign?? **{value}** PV en un combat {icon} __{name}__ ce mois-ci",
    "Apparament, le record personnel de soins mensuel de {icon} __{name}__ est de **{value}**, ni plus ni moins ???(?????????)???",
    "Savoir s'adapter ?? toutes les situations est crucial. Et {icon} __{name}__ a du avoir de bon r??flexe pour avoir soign?? **{value}** points de vie ce mois-ci"
]

randomTotalHeal = [
    "Au total, tu as soign?? **{value}** PV {icon} __{name}__",
    "Tu as r??ussi ?? annuler **{value}** d??g??ts subis par tes alli??s {icon} __{name}__, c'est pas trop mal (?????????)! ",
    "Si j'en crois mes observations, {icon} __{name}__ aurait soign?? un total de **{value}** PV... J'ai du mal regarder (??? ???)",
    "Tu n'aimes pas les barres de vies qui frittent avec le 0, n'est-ce pas {icon} __{name}__ ? Tu en est ?? **{value}** PV soign??s, actuellement"
]

randomMaxRes = [
    "En un seul combat ce mois-ci, {icon} __{name}__ a r??ussi ?? ressuciter jusqu'?? **{value}** alli??s, quel ange gardien (??? ???)",
    "La mort c'est surc??t?? tu trouves pas {icon} __{name}__ ^^ ? Tu as ressucit?? jusqu'?? **{value}** alli??s en un seul combat durant le courant du mois"
]

randomTotalRes = [
    "La mort c'est juste une mauvaise grippe ??????(?????????). Que {icon} __{name}__ a soign?? **{value}** fois",
    "(???.???)???zzz {icon} __{name}__... r??su... **{value}** fois...",
    "{icon} __{name}__ ?? l'air de bien maitriser les gestes de premiers secours, {il} a r??anim?? **{value}** fois un alli??"
]

randomMaxTank = [
    "H?? bah ! {icon} __{name}__ a subis un maximum de **{value}** d??g??ts en un combat ce mois-ci ? J'esp??re que ses supports ont suivi (?????????)",
    "{icon} __{name}__ pr??f??re voir les ennemis dans le blanc des yeux apparament. En tous cas, c'est pas ses **{value}** d??g??ts subis en un combat qui le contesteront",
    "Je me demande ce qu'il y a dans la t??te de {icon} __{name}__ pour s'??tre expos?? ?? **{value}** d??g??ts ce mois-ci... A-t-{il} encore sa t??te au moins ?"
]

randomTotalTank = [
    "Tiens donc ? {icon} __{name}__ aurait subi un total de **{value}** ? ??a fait pas mal quand m??me, je compatis pour ses soigneurs (??? ???|||)",
    "{icon} __{name}__, tu serais pas un peu mazo par hasard (??? ???|||) ? Tu es quand m??me ?? **{value}** d??g??ts totaux subis l??..."
]

randomMaxArmor = [
    "L'important c'est de savoir quand utiliser ses capacit??s ??????(?????????).\nRegardez {icon} __{name}__ : Son record d'armure donn??e mensuel est ?? **{value}**",
    "Je suis plus partisante du \"Ils peuvent pas nous taper si ils sont morts\", mais bon au cas o?? je pourrais compter sur {icon} __{name}__.\nSon record d'armure donn??e ce mois-ci est ?? **{value}** ???(?????????)???",
    "{icon} __{name}__ n'aime pas vous voir subir des d??g??ts il faut croire. Ce mois-ci, {il} a donn?? au maximum **{value}** points d'armure en un combat"
]

randomTotalArmor = [
    "Il semblerais que {icon} __{name}__ pr??f??re pr??venir que gu??rir... Son total d'armure donn?? s'??l??ve ?? **{value}**",
    "Le total d'armure donn??e par {icon} __{name}__ s'??l??ve ?? **{value}**, sans plus ni moins ???(?????????)???",
    "H?? bah ! On peut dire que {icon} __{name}__ s'y connais en armure, {il} en a donn?? **{value}** points jusqu'?? pr??sent"
]

randomMaxKill = [
    "{icon} __{name}__ est une veritable terreur avec son record mensuel de **{value}** ??liminations en un combat (???_???????????????",
    "Va falloir que je me souvienne d'??tre particulirement prudente avec {icon} __{name}__ ( . .)??...\nSon record d'??limination est de **{value}**...",
    "Toujours droit au but n'est-ce pas {icon} __{name}__ ? Tu as ??limin?? au maximum **{value}** ennemis ce mois-ci"
]

randomTotalKill = [
    "Le nombre de victimes de {icon} __{name}__ est de **{value}**.\n\nNon j'ai pas de commentaire ?? faire (??????0???)",
    "Le nombre de victimes de {icon} __{name}__ est de **{value}**.",
    "Si j'ai bien compt??, le nombre total d'??limiation par {icon} __{name}__ est ?? **{value}** (??? ???)\nFaites ce que vous voulez de cette information",
    "{icon} __{name}__ a ??limin?? au total **{value}** adversaires. J'esp??re qu'{il} garde en t??te qu'{il} n'y est pas arriv?? seul{e}"
]

randomRecordMsg = [
    "C'est cependant loin du record mensuel qui est de **{value}**, d??tenu par {icon} __{name}__",
    "Va falloir mieux faire si tu veux d??passer {icon} __{name}__, le sien est ?? **{value}** ??????(?????????)",
    "Allez courage ! {icon} __{name}__ n'est qu'?? **{value}** (^.~)???",
    "Si tu veux viser les ??toiles, sache que {icon} __{name}__ est ?? **{value}** ???( ?? ??? ?? )???",
    "Tu veux pas essayer de prendre le record ? Pour le moment c'est {icon} __{name}__ qui le d??tient avec **{value}**",
    "La concurence est dure par contre. Si tu cherches le haut du podium, il va falloir faire mieux que {icon} __{name}__ et ses **{value}**"
]

randomPurcenMsg = [
    "??a fait quoi... **{purcent}** % du total de son ??quipe ?",
    "Hum... Je crois que ??a doit faire... **{purcent}** % du total de son ??quipe ?",
    "D'apr??s ma calculatrice, ??a fait **{purcent}**% du total de son ??quipe"
]

randomTotalSupp = [
    "Qu'est-ce que ferais ton ??quipe sans toi {icon} __{name}__ ? Ton score de Soutien est ?? **{value}**",
    "Tiens donc, il semblerait que le score de Soutien de {icon} __{name}__ soit ?? **{value}**"
]

randomMaxSupp = [
    "On ne m??nage pas ses efforts ?? ce que je vois {icon} __{name}__ ! En un combat, tu as r??ussi ?? obtenir un maximum de **{value}** points de Soutien durant ce mois",
    "Taper c'est bien beau, mais sans {icon} __{name}__, vous n'auriez pas tap?? ??norm??ment. Son record de Soutien mensuel est de **{value}**"
]

aliceStatsNothingToShow = [
    ["Hum... Il semblerait que personna dans ton ??quipe a fait de d??g??ts jusqu'?? pr??sent ?"],
    ["H?? bah, ??a vole pas haut niveau ??limiation chez vous..."],
    ["On a qu'une seule vie comme on dit. Enfin particuli??rement chez vous, o?? personne a r??anim?? personne","Conseil d'amie : Vous feriez mieux d'avoir quelqu'un qui puisse r??animer dans votre ??quipe, et pas toujours vous reposer sur nous pour vous sauver le post??rieur"],
    ["Vous avez vraiment r??ussi ?? subir aucuns d??g??ts jusqu'?? l?? ?"],
    ["Faut croire que vous aimer vous faire maraver la figure, personne a soign?? personne dans votre ??quipe"],
    ["Vous savez qu'avoir un peu d'armure peu pas vous faire de mal, hein ?"],
    ["Je sais que le role de Support n'est pas particuli??rement attractif, mais bon il reste quand m??me utile d'en avoir un"]
]

clemPosSays = says(
    start="J'en ai ma claque des gens de votre genre.",
    onKill="Un de plus, un de moins. Quelle importance",
    redWinAlive="Restez ?? votre place.",
    redLoose="Que..."
)

aliceExSays = says(
    start="Cl??mence...",
    onKill="...",
    onResurect="Merci...",
    blueWinAlive="??a... ??a va mieux ?",
    bigRaise="Je y arriver probablement pas... S'il vous pla??t..."
)

def createTmpChangeDict(level: int, changeWhat: int, change: list, to: list, proba=100):
    """ChangeWhat : 0 == skills"""
    if len(change) != len(to):
        raise AttributeError(
            "Change list and To list don't have the same length")
    if proba > 100:
        raise AttributeError("Proba > 100")
    elif proba < 1:
        raise AttributeError("Proba < 1")

    return {"level": level, "changeWhat": changeWhat, "change": change, "to": to, "proba": proba}

# ["Berserkeur","Observateur","Poids plume","Idole","Pr??voyant","T??te brul??e","Mage","Altruiste","Invocateur","Enchanteur","Protecteur"]
limitBeakGif = [
    'https://cdn.discordapp.com/attachments/927195778517184534/932778559150391366/20220118_002840.gif',  # Ber
    'https://cdn.discordapp.com/attachments/927195778517184534/932775385043709952/20220118_001608.gif',  # Obs
    'https://cdn.discordapp.com/attachments/927195778517184534/932774912391782490/20220118_001411.gif',  # PPlu
    'https://cdn.discordapp.com/attachments/927195778517184534/932776578058965102/20220118_002049.gif',  # Ido
    'https://cdn.discordapp.com/attachments/927195778517184534/932778559502700594/20220118_002719.gif',  # Pr??
    'https://cdn.discordapp.com/attachments/927195778517184534/932777330605178920/20220118_002344.gif',  # TBru
    'https://cdn.discordapp.com/attachments/927195778517184534/932773655732158525/20220118_000607.gif',  # Mage
    'https://cdn.discordapp.com/attachments/927195778517184534/932773655342104606/20220118_000858.gif',  # Alt
    'https://cdn.discordapp.com/attachments/927195778517184534/932773655732158525/20220118_000607.gif',  # Enc
    'https://cdn.discordapp.com/attachments/927195778517184534/932777330978488391/20220118_002225.gif'  # Pro
]

lenaTipsMsgTabl = [
    "Est-ce que quelqu'un lit vraiment ??a ?",
    "Si vous r??alisez la commande /fight normal alors qu'il vous reste moins de 10 minutes de repos, votre combat sera mis en file d'attente et se lancera automatiquement une fois le d??compte ??coul??",
    "Une fois le tour 20 atteint en combat, il est plus possible de r??animer un combattant et tout le monde subis des d??g??ts en fonction de ses PVs Maximums",
    "H?? vous voulez un conseil de chargement inutile que tout le monde ne lit qu'une fois puis oubli leur existance ? En voil?? un",
    "En fin de combat, vous gagnez de l'exp??rience en fonction des ennemis vaincu. Si un ennemi a ??t?? r??anim?? mais n'a pas ??t?? vaincu une seconde fois, il ne donne que la moiti?? de l'exp??rience qu'il devait donner",
    "En g??n??ral, les combattants de derni??re ligne font plus de d??g??ts que leurs camarades en m??l??e, mais sont bien plus fragile",
    "Si une entit?? repouss??e rencontre un obstacle, elle subit des d??g??ts Harmonie d'une puissance de 10 multipli??e par le nombre de cases qu'il lui restait ?? parcourir",
    "Si une entit?? ne peux pas se t??l??porter parceque toutes les cases adjacantes ?? la cible sont occup??es, elle s'inflige des d??g??ts Harmonie d'une puissance de 20",
    "L'Harmonie est une statistique sp??ciale qui est juste un beau mot pour dire \"Statistique la plus ??lev??e\"",
    "L'Harmonie ne prend pas en compte les statistiques d'actions, mais ceux-ci sont cependant bien rajout?? ?? la statistique d'Harmonie apr??s sa d??finition",
    "Les Trancendances prennent en compte la statistique principale la plus ??lev??e du lanceur, mais ??galement sa meilleur statistique d'action, ind??pendamant de l'action en question",
    "Les comp??tences de r??animations prennent en compte la statistique d'action la plus ??lev??e parmis les Soins, Armures ou Bonus",
    "Chaque r??animation accorde une armure absolue ??quivalente ?? 20% des PVs maximums du r??anim?? ?? ce dernier",
    "Les armures absolues prot??gent de tous types de d??g??ts ?? l'exeption de la Mort Subite et des co??ts en PV des comp??tences d??moniques",
    "Les armures absolues et normales absorbent des d??g??ts suppl??mentaires lorsqu'elles sont d??truites. Par d??faut, cette valeur est ??gale ?? votre niveau, mais certaines comp??tences peuvent influer dessus",
    "Donner une armure normale ou l??g??re ?? un combattant qui poss??de d??j?? une armure normale ou absolue r??duit la valeur de cette nouvelle armure. Par d??faut, la r??duction est de 50%, mais certaines comp??tences peuvent influer dessus",
    "Kiku et les Zombies commencent tous leurs combats avec le status \"R??anim??e\"",
    "Certains ennemis comme l'OctoBOOM ne peuvent pas ??tre r??anim??s",
    "Les Berserkeur ont besoin de pouvoir infliger des d??g??ts pour ??tre des tanks efficace. Par cons??quent leur donner un autre second role que DPT est pas vraiment une bonne id??e",
    "Les statistiques des Idoles leur permettent prendre un role secondaire de soingneur, l?? o?? les Innovateurs peuvent se tourner vers l'armure si ils le d??sirent",
    "Les statistiques des Altruistes ainsi que leurs comp??tences propres en fond de tr??s bon soigneur, mais avec les bons ??quipements ils peuvent aussi ??tre de bon booster d'??quipe",
    "Les Mages b??nificent principalement de l'utilisation de comp??tence ultime, mais comme leur bonus dure 2 tours, ils peuvent le cumuler avec les comp??tences avec un tour de chargement",
    "Les Poids Plumes ont naturellement une endurance et une force relativement faible, mais cela est compens?? par leur grande agilit?? qui leur permet d'esquiver ou d'infliger des coups critiques plus souvent que ses concurants de m??l??e\nDe plus, ?? l'instar des Observateurs, leurs coups critiques infligent plus de d??g??ts",
    "Le taux d'esquive est calcul?? en fonction de la diff??rence entre la pr??cision de l'attaquant et l'agilit?? de l'attaqu??.\nSi l'attaqu?? est plus agile, le taux de r??ussite de l'attaque est diminu??e jusqu'au maximum la moiti?? de sa valeur\n?? contratio, une pr??cision plus ??lev??e de l'attaquant peut lui donner jusqu'?? deux fois plus de chances de toucher",
    "Le 19 de chaques mois, les records mensuels sont r??nitialis??s",
    "Il se peut que vous obtenez une r??compense si vous poss??dez un certain pourcentage des objets obtenables dans le magasin ou en butin",
    "Lors d'un raid, vous ??tes associ?? ?? une ??quipe dont le niveau moyen est similaire ?? celle de la votre. Cependant, cette ??quipe tierce n'obtient aucune r??compense",
    "Vous vous souvenez de l'aspiration \"Strat??ge\" ? Ouais moi non plus",
    "Funfact : Tout ?? commenc?? sur une aire d'autoroute pendant que L??na??c s'ennuyait ?? attendre que sa famille revienne de sa pause pipi",
    "Les Sorciers cr??ent de petites d??tonnations quand ils ??liminent un ennemi. Celles-ci prennent en compte les statistiques de Magie et de D??g??ts indirects",
    "Les T??tes Brul??es r??duisent petit ?? petit les PV maximums de leurs cibles, ce qui les rends particuli??rement efficaces contre les ennemis qui se soignent beaucoup",
    "Utiliser des comp??tences divines vous fait peu ?? peu perdre votre prise sur la r??alit?? au fil du combat. Cela est repr??sent?? par des pertes de PV maximums lors de l'utilisation de ces derni??res",
    "Utiliser des comp??tences d??moniaques requi??re une quantit?? d'??nergie si importe que vous perdrez une partie de vos PV courrants",
    "En lan??ant des combats normaux, vous avez une petite chance de revivre un combat pass?? qu'?? v??cu un des alli??s temporaires\nCes combats sont appel??s \"Combat par procuration\"",
    "Certaines comp??tences comme Mort Vivant ou Bolide peuvent rendre leur utilisateur invuln??rable ou impossible ?? vaincre pendant un cours instant, permettant aux soigneurs d'essayer de leur sauver la mise",
    "Certaines comp??tences comme quelques transcendance ou Abn??gations ont pour effet secondaire de r??anim?? les alli??s vaincus dans la zone d'effet, si ils peuvent encore l'??tre",
    "Les Protecteurs, Vigilants et Enchanteurs sont trois aspirations qui tirent partie de leur capacit??s ?? attirer (et encaisser) les attaques adverses",
    "La R??sistance Soin progresse plus rapidement si plusieurs soigneurs sont pr??sents dans la m??me ??quipe",
    "Repose en paix, aspiration Invocateur",
    "Une intelligence ??lev??e permet, en plus de pouvoir donner une bonne quantit?? d'armure, d'avoir une bonne probabilit?? d'effectuer des d??g??ts indirects critiques tout en diminuant la probabilit?? d'en recevoir",
    "Les statistiques de Cl??mence, F??licit??, Sixtine et Alice augmente l??g??rement si plusieurs d'entre elles sont dans le m??me combat",
    "Lohica est plut??t mauvaise perdante et infligera __Poison d'Estialba__ ?? son ??liminateur lorsque ses PVs tombent ?? 0",
    "Les Sorciers infligent des d??g??ts indirects critiques plus ??lev??s que les autres aspirations",
    "Le Charisme de Liu, Lia, Liz et Lio augmente l??g??rement si au moins deux d'entre elles sont dans le m??me combat",
    "Alice n'aime pas vraiment que quelqu'un monte sur sc??ne en sa pr??sence",
    "Les comp??tences \"Haima\" et \"Pandaima\" ont une tr??s bonne synergie avec l'une des comp??tences qui augmente le nombre de PAr suppl??mentaire des armures lorsqu'elles sont d??truites. Elles peuvent ainsi d??clancher leurs effets 5 fois, r??sultant en une r??duction de d??g??ts encore plus cons??quante",
    "Lors d'un combat normal contre les alli??s temporaires, certains ont des malus sp??cifiques pour diminuer un peu leur efficacit?? au combat",
    "Par d??faut, chaque combattant ne peut voler un nombre de PV sup??rieur ?? 45 fois leur niveau avec une m??me attaque. Cette limite est surtout l?? pour ??viter que certain boss se soigne d'une quantit?? astronomique de PV lorsqu'ils attaquent.\nCependant, la limite de vol de vie de Cl??mence Poss??d??e et Cl??mence Exalt??e est ?? 100 fois la valeur de son niveau.",
    "En obtenant 75% du shop, vous obtiendrez une comp??tence dont l'effet est diff??rent pour chaque aspiration. D?? ?? quelques soucis technique, cette comp??tence n'est pas affich??e dans les listes de /inventory destination:comp??tence. Il faut donc utiliser /inventory nom:Transcendance ou /inventory nom:lb pour arriver directement sur sa page d'information",
    "Toutes les aspirations de supports, de soins et d'armures voient leur probabilit?? d'utiliser des options offensives augmenter lorsqu'ils n'ont plus beaucoup de DPT alli??s en vie ou que le combat se rapproche du tour 20.",
    "Les d??g??ts de Mors Subite sont r??duits de 90% sur les boss",
    "Les armes runiques, le passif Maitrise El??mentaire ainsi les comp??tences Convertion El??mentaire et Concentration El??mentaire sont le meilleur moyen de gagner des effets ??l??mentaires.\nCes effets augmentent de 5% la puissance des comp??tences exclusives ?? leur ??l??ment et certaines comp??tences les consommes pour obtenir des effets suppl??mentaires.",
    "Les Sorciers et les Attentifs infligent des d??g??ts indirects critiques plus ??lev??es que les autres aspirations.",
    "Les effets de d??g??ts indirects des Attentifs ont pour effet secondaire de r??duire les soins re??us par leur cible en fonction de leur puissance.",
    "Les redirections de d??g??ts ne redirigent que les d??g??ts directs, ?? l'exeption des pattes de The Giant Ennemi Spider; bien que rien n'est affich??, cette derni??re subit bien l'int??gralit?? des d??g??ts indirects re??us par ses pattes",
    "Les d??buts de combat sont les moments o?? les Idoles et les Innovateurs octroient des bonus plus puissant qu'?? l'accoutum??. Cependant, ceux des Idoles voient leur puissance diminuer au fur et ?? mesure que leur ??quipe se fait vaincre tandis que ceux des Innovateurs d??p??rissent en m??me temps que l'??quipe adverse"
]

ilianaSaysNormal = says(
    start="Puisse ce combat ??tre b??n??fique pour tous !",
    ultimate="Qu'est-ce que vous pensez du pouvoir de la Lumi??re ?",
    limiteBreak="Que la Lumi??re nous prot??ge !",
    onKill="Je d??cline toute responsabilit?? en cas de tache blanche incrust??e dans ta r??nite",
    onDeath="Humf !",
    reactAllyKilled="J'aurais du faire plus attention, d??sol??e",
    reactBigRaiseAllie="On reprend ses esprits et on y retourne"
)

ilianaSaysVsLuna = says(
    start="Tu nous fais encore une crise ?",
    ultimate="On tiens le bon bou, lachez rien !",
    onKill="T'en fait pas Luna !",
    onDeath="Ish...",
    onResurect="Merci bien",
    blueWinAlive="`S'assoit ?? c??t?? de Luna, qui est trop fatigu??e pour bouger, lui met la t??te sur ses genoux puis caresse cette derni??re en ronronnant`\"\n<:luna:909047362868105227> : \"Ili'...\"\n<:Iliana:926425844056985640> : \"Tu ferais la m??me chose si c'??tait moi, et tu t'es faite battre ?? plate couture, tu es pas en droit de contester\"\n<:luna:909047362868105227> : \"... `Ferme les yeux et s'endort peut de temps apr??s`",
    blockBigAttack="Si tu crois que tu va m'avoir avec ??a !",
    reactBigRaiseAllie="Je m'occupe des T??n??bres qui paralyse votre ??me vous en faites pas !"
)

kitsuneSays = says(
    start="Mais c'est que vous ??tes bien nombreux dites donc ^^",
    onKill="C'??tait trop intense pour toi ? Mais on a m??me pas encore commenc?? !",
    redWinAlive="C'??tait amusant, vous trouvez pas ?",
    reactBigRaiseEnnemy="Vos ??mes m'appartiennent d??j??, pourquoi r??sister ?"
)

lySays = says(
    start="Arf, mon truc c'est plut??t les squelettes et les zombies, vous savez ?",
    ultimate="Pr??ts pour le feu d'artifice ?",
    onDeath="Je suis pas assez bien pay??e pour ce genre de trucs...",
    onResurect="Je savais que j'aurais du prendre un totem de r??surection... Mais merci",
    blueWinAlive="J'ai le droit de garder le loot ?",
    redWinAlive="Vous avez un lit qui vous attend",
    reactBigRaiseAllie="Si on doit en arriver ?? cette extremit??, ??a n'a pas vraiment l'air d'??tre bien parti...",
    reactBigRaiseEnnemy="Je doute que ??a suffira ?? inverser la tendance !",
    reactEnnemyKilled="Tu as oubli?? ton totem de r??surrection, {downed} ?"
)
gwenySays = says(start="Tachons de faire ??a rapidement, ??a vous vas ?",ultimate="Ok ??a suffit l?? !",limiteBreak="Ok l?? vous m'avez ??nerv??e !",reactAllyLb="Esp??ront que ??a changera la donne",reactAllyKilled="Je suppose que j'ai une nouvelle cible maintenant",reactBigRaiseEnnemy="En quoi c'est juste ??a Lena !?\"*\n<:lena:909047343876288552> : \"*Vous pouvez le faire aussi, arr??te de te plaindre",onKill="Tu m'en diras des nouvelles.",redWinAlive="Vous en revoulez ?")
klikliSays = says(start="Ok. Je vais m'en occuper rapidement",limiteBreak="OK, VOIL?? POUR VOUS !",onKill="Si tu veux revenir, j't'ai pas encore montrer tout ce dont je suis capable.",reactEnnemyKilled="Pff, j'peux le faire toute seule tu sais ?",ultimate="J'esp??re que tu as les yeux grands ouverts {target} !",redWinAlive="J'esp??re que vous en avez pris de la graine.")
altySays = says(start="'K, je vais faire de mon mieux",onKill="D??sol??e...",onResurect="Ok, second round !",reactAllyKilled="{downed} !",redWinAlive="Oul??, ??a va aller ? Je crois qu'on y est all?? un peu fort...",redWinDead="`Rigole` Bien jou?? tout le monde !")

shehisaSays = says(start="Ok, si on suit le plan, tout se passera bien",onKill="Tu aurais pu attendre que je soit partie avant de creuver quand m??me.",onDeath="Humf, c'??tait pas pr??vu ??a...",reactAllyKilled="On lache rien !",reactBigRaiseEnnemy="C'??tait trop beau pour ??tre vrai",reactAllyLb="Wowowo tu nous as fait quoi l?? {caster} ?",blueWinAlive="Tout s'est d??roul?? comme pr??vu",redWinAlive="Tout s'est d??roul?? selon le plan")

# Procur Temp stuff
procurTempStuff = {
    "Shushi Cohabit??e":[0,
        ["Barr??te de la cohabitation","dualHat","<:coaBar:911659734812229662>"],
        ["Robe de la cohabitation","dualDress",'<:coaDress:911659797076660294>'],
        ["Bottines de la cohabitation","dualBoost",'<:coaBoots:911659778995007528>'],
        [[0,0],[5,0.2],[2,0.3],[0.5,1],[0.5,1],[3,0.8],[3.6,0.8],[1,0.2],[0.5,0.3],[0.8,0.2]]
    ],
    "Luna pr??.":[250,
        ["Boucle d'oreille ombrale",'lunaDarkPendant','<:linapendant:890599104902754326>'],
        ["Robe de soubrette ombrale ",'lunaDarkMaidDress','<:linadress:890598423152185364>'],
        ["Ballerines ombrales",'lunaDarkFlats','<:linaflats:890598400624586763>'],
        [[1.2,2.55],[1.15,0.4],[0.8,0.5],[1,1.2],[1,0.6],[0.2,0.3],[0,0],[0.25,0.35],[0.25,0.35],[0,0]]
    ],
    "Iliana pr??.":[250,
        ["Casque de la neko de la lueur ultime", 'ilianaPreHead','<:zenithHead:913170464581484554>'],
        ["Armure de la neko de la lueur ultime", 'ilianaPreArmor','<:zenithArmor:913170492452646922>'],
        ["Sorolets de la neko de la lueur ultime", 'ilianaPreBoots','<:zenithBoots:913170512564334623>'],
        [[0.2,0.1],[1,2.5],[1,3],[0.5,0.9],[1.2,0.3],[3,0.05],[5,0.05],[1.2,0.2],[1,0.05],[1,0.05]]
    ],
    "Cl??mence Exalt??e":[500,
        ["Boucles d'oreilles runiques","clemRune",'<:clemEarRings:920297359848636458>'],
        ["Veste sanguine",'clemRune','<:clemVeste:920300283068833874>'],
        ["Bottes sanguines","clemRune","<:clemBoots:920297554330157056>"],
        [[0.6,0.2],[1.25,1],[0.5,0.5],[2,.05],[1,0.3],[1.2,0.8],[1.7,1],[0.5,0.25],[1,0.031],[1,0.0005]]
    ],
    "Alice Exalt??e":[0,
        ["Noeud en ruban chauve-souris","aliceExHat","<:batRuban:887328511222763593>"],
        ["Veste et jupe rose p??le","aliceExDress",'<:VesteEtJupeRose:877658944045219871>'],
        ["Ballerines roses p??les","aliceExShoes",'<:pinkFlat:867158156139692042>'],
        [[0.1,0.05],[0.5,0.4],[1.1,1.5],[0.8,0.25],[0.65,0.2],[1,1.35],[0.6,0.4],[1.2,0.15],[0.5,0.1],[1,0.1]]
    ]
}

lunaPreSays = says(
    start="C'est votre derni??re chance de prendre la poudre d'escampette.",
    onKill="Quoi tu es surpris ? C'est pas faute d'avoir pr??venu pourtant.",
    blueWinAlive="Pas la peine de revenir me faire chier, le r??sulta sera le m??me",
    reactBigRaiseEnnemy="Vous me faites une fleur vous savez, que vais pouvoir vous maraver la gueule une seconde fois sans m??nagement",
    blockBigAttack="Chaton, c'est pas ?? toi de le faire d'habitude ?"
)

ilianaPreSays = says(
    start="J'esp??re que tu es en forme Luna...\"\n<:luna:909047362868105227> : \"Je suis toujours pr??te pour ce genre de trucs",
    ultimate="Oh on en a pas encore termin?? !",
    reactEnnemyKilled="On a pas encore fini",
    blueWinAlive="`S'??tire` Ce genre d'informit??s deviens de plus en plus r??current...\"\n<:luna:909047362868105227> : \"Ca ne pr??sage rien de bon..."
)

alphaTabl=["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
def getAutoId(id:str,reverse=False):
    idTabl = []
    for letter in id:
        idTabl.append(letter)
    for cmpt in range(len(idTabl)).__reversed__():
        if not(reverse):
            if idTabl[cmpt] == alphaTabl[-1]:
                idTabl[cmpt] = alphaTabl[0]
            else:
                for cmpt2 in range(len(alphaTabl)):
                    if idTabl[cmpt] == alphaTabl[cmpt2]:
                        idTabl[cmpt] = alphaTabl[cmpt2+1]
                        break
                break
        else:
            if idTabl[cmpt] == alphaTabl[0]:
                idTabl[cmpt] = alphaTabl[-1]
            else:
                for cmpt2 in range(len(alphaTabl)):
                    if idTabl[cmpt] == alphaTabl[cmpt2]:
                        idTabl[cmpt] = alphaTabl[cmpt2-1]
                        break
                break
    toReturn = ""
    for letter in idTabl:
        toReturn += letter
    return toReturn

def getArrayAutoId(start:str,iteration:int,reverse=False):
    """Return a tuple of auto generated ids for stuffs and skills"""
    toReturn, cmpt = [], 0
    while cmpt < iteration:
        tempId = getAutoId(start,reverse)
        toReturn.append(tempId)
        start=tempId
        cmpt += 1
    return tuple(toReturn)

