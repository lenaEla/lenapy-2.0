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

areaNames = ["Monocible", "Cercle de rayon 1", "Cercle de rayon 2", "Cercle de rayon 3", "Cercle de rayon 4", "Cercle de rayon 5", "Cercle de rayon 6", "Cercle de rayon 7", "Tous les alliés", "Tous les ennemis", "Tous les combattants", "Cone simple", "Cone Large", "Cone Large", "Cone Large", "Cone Large", "Cone Large", "Ligne de 2 de longueur", "Ligne de 3 de longueur", "Ligne de 4 de longueur", "Ligne de 5 de longueur", "Ligne de 6 de longueur", "Donut de 1 de rayon", "Donut de 2 de rayon", "Donut de 3 de rayon", "Donut de 4 de rayon","Donut de 5 de rayon", "Donut de 6 de rayon", "Donut de 7 de rayon", "Anneau Distance de 1 de largeur", "Anneau Distance de 2 de largeur", "Anneau Distance de 3 de largeur", "Anneau Distance de 4 de largeur", "Anneau Distance de 5 de largeur", "Arc de Cercle de 1 de rayon", "Arc de Cercle de 2 de rayon", "Arc de Cercle de 3 de rayon", "1 ennemi aléatoire", "2 ennemis aléatoires", "3 ennemis aléatoires", "4 ennemis aléatoires", "5 ennemis aléatoires", "Croix de 2 cases", "Croix de 3 cases", "Croix de 4 cases", "Crois de 5 cases"]
allArea = range(0, 46)
listNumberEmoji = ["0️⃣","1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟","▶️","⏸️","⏯️","⏹️","⏺️","⏭️","⏮️","⏩","⏪","⏫","⏬","◀️","🔼","🔽","➡️","⬅️","⬆️","⬇️","↗️","↘️","↙️","↖️","↕️","↔️"]
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
    "lorsque le porteur reçoit des dégâts directs",
    "à la fin du tour du porteur",
    "à la mort du porteur",
    "lorsque le porteur inflige des dégâts directs",
    "lors de la pose de cet effet",
    "au début du tour du porteur",
    "lors du retrait de cet effet",
    "après que le porteur ai infligé des dégâts directs"
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

tablTypeStr = ["Armure", "Dégâts indirects", "Soins Indirects", "Résurection indirecte","Boost", "Resurection", "Dégâts", "Malus", "Soins", "Unique", "Invocation", "Passif"]
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

nameStats, nameStats2 = ["Force", "Endurance", "Charisme", "Agilité","Précision", "Intelligence", "Magie"], ["Résistance", "Pénétration", "Critique"]
allStatsNames = nameStats+nameStats2

# Status for entities
STATUS_ALIVE, STATUS_DEAD, STATUS_RESURECTED, STATUS_TRUE_DEATH = 0, 1, 2, 3

DANGERUPPERSTAR = 5

# Aspirations
BERSERK, OBSERVATEUR, POIDS_PLUME, IDOLE, PREVOYANT, TETE_BRULE, MAGE, ALTRUISTE, ENCHANTEUR, PROTECTEUR, VIGILANT, SORCELER, INOVATEUR, ATTENTIF, ASPI_NEUTRAL = 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14
inspi = ["Berserkeur", "Observateur", "Poids plume", "Idole", "Prévoyant", "Tête brulée", "Mage","Altruiste", "Enchanteur", "Protecteur", "Vigilant", "Sorcier", "Inovateur", "Attentif", "Neutre"]
aspiEmoji = ["<:ber:985007311997263932>","<:obs:985007736360165407>","<:pplume:985007345648148541>","<:ido:985007596656275476>","<:pre:985007771613274133>","<:tbrule:985007436538740766>","<:ma:985010178900500561>","<:alt:985007803322224720>","<:enc:985007558156755004>","<:pro:985009037546487850>","<:vig:985009013097910302>","<:sor:985007632639205458>","<:inov:985007247656632360>","<:att:985007703707500555>","<:neutral:985011113458536538>"]
lbNames = ["Lames de l'Ombre","Odre de Tir : Drône 3.4.8 Alpha","Frappe de Silicia","Apothéose planétaire","Armure Galactique","Fracture Dimentionnelle","Colère de Nacialisla","Bénédiction de Nacialisla","Desctruction Silicienne","Pousée d'Espoir","Grandeur de Nacialisla","Cataclysme Powehien","Avenir Prometeur","Chef d'Oeuvre Balistique"]
lbDesc = ["Inflige des dégâts à l'ennemi ciblé et vous soigne d'une partie des dégâts infligés","Inflige des dégâts à l'ennemi ciblé et augmente vos statistiques","Inflige des dégâts à l'ennemi ciblé et le repousse violament","Augmente les statistiques des alliés à portée et réanime ceux qui sont vaincus","Octroi une armure aux alliés à portée et augmente leurs statistiques offensives","Inflige des dégâts à l'ennemi ciblé et réduit ses PV max","Inflige dégâts dans une large zone autour de l'ennemi ciblé","Soigne les alliés à portée et leur donne un effet de régénération tout en réanimant ceux qui étaient vaincus","Inflige des dégâts dans une large zone autour de l'ennemi ciblé et vous octroit une armure","Octroi une armure aux alliés à portée et augmente leurs statistiques défensives","Soigne les alliés à portée en réanimant ceux vaincus tout en réduisant vos dégâts subis","Inflige des dégâts dans une large zone autour de l'ennemi ciblé et lui inflige un effet de dégâts indirects multi-cibles","Augmente les statistiques des alliés à portée et réduit leurs dégâts subis pendant la même durée","Inflige des dégâts en ligne droite sur l'ennemi ciblé et augmente vos statistiques"]
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
    # Prévoyant
    [25, 35, 35, 35, 35, 75, 35],
    # Tête Brulée
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
DPT_PHYS, HEALER, BOOSTER, DPT_MAGIC, SHIELDER = "Bers, Obs, P.Plu, T.Bru, Att.", "Vig., Alt", "Ido, Inv.", "Enc, Mag, Sor.", "Pro., Pré."

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
    "L'élément Neutre ({0}) est l'élément le plus apprécié des nouvelles recrues.\nSans spécialisations particulière, cet élément permet de tout faire sans trop se casser la tête".format(elemEmojis[0]),
    "L'élément Feu ({0}) est en général préféré par ceux qui aiment tirer sans distinction et faire carnage sans pareil.\nLes dissicles de l'élément Feu infligent un peu plus de dégâts avec les armes et capacité de zone en distance.".format(elemEmojis[1]),
    "L'élément Eau ({0}) est plus propice à la concentration et la sérénité.\nLes adeptes de cet élément inflige plus de dégâts avec les armes ou capacités monocible à distance.".format(elemEmojis[2]),
    "L'élément Air ({0}) a pour réputation d'être assez capricieu et imprévisible.\nC'est pour cela que ses partisants filent tel le vent pour frapper plusieurs ennemis simultanément.".format(elemEmojis[3]),
    "L'élément Terre ({0}) permet de ressentir la puissance des courants d'énergie télurique et d'en tirer le meilleur parti.\nLes habitués de cet élément infligent des dégâts monocibles en mêlée plus conséquents.".format(elemEmojis[4]),
    "L'élément Lumière ({0}) permet d'entrevoir l'espoir là où les autres ne voit que les ombres.\nLes soins et armures de ces illuminés sont plus conséquents que ceux de leurs congénaires.".format(elemEmojis[5]),
    "L'élément Ténèbre ({0}) n'a pas son pareil pour exploiter les zones d'ombres de leurs adversaires.\nLes dégâts indirects de ces individues sont plus conséquents que ceux de leurs congénères.".format(elemEmojis[6]),
    "L'élément Astral ({0}) utilise la puissance cosmique à son aventage. Car rien ne se perd, rien ne se créait, tout se transforme.".format(elemEmojis[7]),
    "L'élément Temporel ({0}) permet de prévoire les coups, car avoir une longueur d'avance est toujours bienvenue.".format(elemEmojis[8])
]
elemNames = ["Neutre", "Feu", "Eau", "Air", "Terre", "Lumière","Ténèbre", "Astral", "Temporel", "Universalis Premera"]
elemMainPassifDesc = [
    "Aucun passif principal",
    "Pénétration : + 5\nDégâts zones et distance simultanément : +10%",
    "Précision : + 10\nDégâts monocible et distance simultanément : +10%",
    "Agilité : + 10\nDégâts zones et mêlée simultanément : +10%",
    "Résistance : + 5\nDégâts monocible et mêlée simultanément : +10%",
    "Soins et armures : +10%",
    "Dégâts indirects : + 10%",
    "Puissance des boosts et malus donnés : +10%\nPuissance des boost reçu d'autrui : +5%\nPuissance des malus reçus d'autrui : -5%",
    "Puissance des effets de soins indirects : +20%"
]
elemSecPassifDesc = [
    "Aucun passif secondaire",
    "Soins donnés et reçus : +5%\nArmures données et reçues : -5%",
    "Armures données et reçues : +5%\nSoins données et reçus : -5%",
    "Puissance des bonus et malus données et reçus : +5%",
    "Dégâts sur Armure infligés et reçus : +5%",
    "Dégâts directs infligés et reçus : +5%",
    "Dégâts directs infligés et reçus : -5%",
    "Dégâts directs de zone infligées et reçus : +5%",
    "Dégâts directs monocibles infligés et reçus : +5%"
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
skillGroupNames = ["neutre", "divine", "démoniaque"]

# Tabl of random messages for the shop
shopRandomMsg = [
    "<:ikaBlue:866459319049650206> : `Sit down and eat pop-corns`\n{shushi} : `Regarde les pop-corns avec un air interresée`",
    "<:soria:977183253255557140> : \"Flum POWA !\"\n{clemence} : \"Les coquelicots c'est mieux je trouve\"\n{alice} : \"N'importe quoi ! Ce sont les roses les plus jolies !\"\n{lena} : \"Vous trois, vous pourriez arrêter de débattre dans mon shop, s'il vous plait ?\"",
    '{clemence} : "Hum... j\'ai trouvé des trucs qui pourrait t\'interresser lors de ma dernière escapade dans les ruines d\'Elidyn, Lena"\n{lena} : "Ow ? Montre pour voir ?"',
    '{alice} : "Mooow tu sais que tu es trop mignone toi ?"\n{shushi} : "Heu... gwa ?"',
    '{shihu} : "Tu en pense qwa de cette coupe de cheveux ?"\n{shushi} : "Hum... Pi vraiment convaincue..."\n{shihu} : "Oh..."\n{shushi} : "Mais après, je peux toujours en faire un queue de cheval regarde !\n{shihu} : :0',
    '{feli} : "Hé Clémence ! Je peux t\'accompagner pour ta prochaine aventure ? Je te promet que je te gênerais pas !"\n{clemence} : "Tu va pas lacher hein... Si tu y tiens. Mais je suis pas responsable si Lena te gronde pour ça, compris ?"\n{feli} : :D',
    '<:akira:909048455828238347> : ...\n{shihu} : ...\n<:akira:909048455828238347> {shihu} : ^^\n\n{lena} : <:LenaWhat:760884455727955978>',
    '{helene} : "Tu es au courant que mourir par hémorragie est tout sauf une mort agréable hein ?"\n{shehisa} : "Je vois pas où est la différence avec les infections que tu donnes à tes adversaires. Je suis peut-être pas une soigneuse, mais Papa m\'a suffisament initiée pour savoir que les maladies que tu leur refile sont tous sauf agréable"',
    '{shehisa} : "Tu me reproche d\'avoir suivi la voie de Maman, mais tu devrais voir comment tu te comporte face à un ennemi quand tu veux lui faire avaler la pilule"\n<:helene:906303162854543390> : "Qu\'est-ce que tu insinue par là ?"\n{shehisa} : "Que je suis pas la seule à avoir héritée des talents de Maman"',
    '{shehisa} : "Toujours rassurant de te savoir dans les parages, Icealia"\n{icelia} : "Et moi je suis toujours rasurée de te savoir dans mon camp..."',
    '<:determination:867894180851482644> : "Alors Féli, tu as fais des progrès sur ta maitrise de la Détermination ?"\n{feli} : "Ouais :D ! Regarde ça !"',
    '<:ruby:958786374759251988> : "Clémence, ça va mieux avec ta cicatrice en ce moment ?"\n{clemence} : "À part qu\'elle me brûle quand j\'utilise trop mes pouvoirs vampiriques ou quand il y a un Alpha dans le coin, rien à déclarer"\n<:ruby:958786374759251988> : "Tss. Ces loups garoux..."\n{clemence} : "Pas la peine de prendre ce regard assassin Madame Ruby. J\'ai appris à faire avec maintenant"',
    '`Alice surgit au coins du couloir en courant et vous rentre dedans, ne vous ayant pas vu`\n\n{alice} : "Dé-désolée !"\n\n`Elle ramasse rapidement les cahiers qu\'elle portait dans ses bras et repart aussi vite qu\'elle est venue.\nVous constatez qu\'elle a oublié une feuille, qui a du se retrouver sous elle quand elle est tombée`\n\n📄 [Devoir d\'astronomie sur les trous noirs](https://bit.ly/3kh8xP3)',
    '{alice} : "Maraiiiiiiiiine ?"\n{lena} : "Il y a un peu trop de "i" pour moi..."\n{alice} : "C\'est quoi ça."\n\n`Elle sortie son téléphone et le mit directement devant le visage de Lena`\n\n📱 [Photographie d\'une feuille de papier](https://bit.ly/3o74aal)\n\n{lena} : "... Merde. Et comment ça, tu es allé fouiller dans ma chambre !?"',
    '{lena} : "Tu sais que tu va finir par traumatiser des gens avec tes \"Boum boum\" toi ?"\n{shihu} : "Mais c\'est drole les Boum Boum..."',
    '{clemence} : "Hé Powehi, je me suis retrouvée avec plein de Rotten Flesh lors de ma dernière expédition, tu veux que je te les passes ?"\n<:powehi:909048473666596905> : "Oh que oui !"',
    '{gweny} : "Toujours à regarder les étoiles ?"\n<:powehi:909048473666596905> : "J\'ai une question Gwendoline... Tu réagirais comment si tu étais bloquée dans ce monde après ta mort et ne pouvais que regarder les autres être vivant te fuir dès que tu t\'approches trop d\'eux ?"\n{gweny} : "Oh heu... Je sais pas vraiment désolée. Compliqué de se mettre à ta place, j\'en ai bien peur"\n<:powehi:909048473666596905> : "C\'est pas grave, merci quand même..."',
    '`En entrant dans une pièce présumée vide, vous êtes surpris de voir des reflets lumineux dans un coin. En allant l\'examiner, vous découvrez Shushi et Sixtine qui dorment l\'une contre l\'autre. Au sol se trouve un lecteur de musique`\n\n📱 [Liste de musique en file d\'attente](https://bit.ly/3D6Ltdh)',
    "<:john:908887592756449311> : \"A-Alice, toi qui la connais bien tu... saurais ce que je pourrais faire pour... qu'elle me voit comme autre chose qu'un... ami ?\"\n{alice} : \"Commence par être un peu plus sûr de toi. Là, elle continue de voir le louvetau naïf qui essayait de se coucher à ses pieds au lieu de fuir\"\n<:john:908887592756449311> : \"Mais je-\"\n{alice} : \"Passe ton temps avec elle sous ta forme de loup à être couché à ses pieds. Si tu veux qu'elle te vois comme autre chose qu'un chien de compagnie, va falloir que tu arrête de te comporter tel quel.\"",
    "<:lio:908754690769043546> : \"H-hm !? Oh c'est toi...\"\n{feli} : \"Tiens tu es là toi aussi ?\"\n<:lio:908754690769043546> : \"J'ai pas trouvé d'autres points d'eau dans le coin donc oui... je suppose...\"",
    "{gweny} : \"Eh bien... On... fatigue déjà... Liu... ?\"\n<:liu:908754674449018890> : \"Cer... Certainement pas... Je... pourrais courir... comme ça... pendant encore des kilomètres...\"",
    "<:lia:908754741226520656> : \"Hé Alice ! Tu penses quoi de ces fleurs là ?\"\n{alice} : \"Hum... un peu trop jaune à mon goût...\"",
    "{shushi} : \"Hé hé Madame des neiges ! J'ai touvé ça part terre, y a maqué quoi deçu ?\"\n{icelia} : \"Montre moi pour voir ^^ ?\"\n\n📃 [Page de papier à l'encre rose](https://bit.ly/3DgXk8v)",
    "{lena} : \"La vache c'est bien plus compliqué que je le pensais de lancer ces plumes enfaites...\"\n<:hina:908820821185810454> : \"C'est qu'une question d'habitude ^^ Hônnetement... J'arriverai même pas à tenir un de tes fusils donc bon ^^'\"",
    "{sixtine} : \"...\"\n<:krys:916118008991215726> : ?\"\n{sixtine} : \"...\"\n<:krys:916118008991215726> : \"?.? Je peux t'aider ?\"\n{sixtine} : \"Oh heu... Je me demandais juste si tu avais un coeur de pierre...\"\n<:krys:916118008991215726> : \"??.??\"",
    "{iliana} : \"Cl-Clméence... ? Hum... tu sais pourquoi ta soeur m'évite toi... ?\"\n{clemence} : \"Si tu parles d'Alice, elle a eu quelques porblèmes avec un chat quand elle était plus jeune donc elle en est un peu traumatisée\"\n{iliana} : \"Oh... la pauvre...\"",
    "{sixtine} : \"Par curiosité Alice... tu as quoi comme info sur Iliana ?\"\n{alice} : \"Hum... Laisse moi voir... Tiens voilà\"\n\n[Feuille de papier froisée](https://docs.google.com/document/d/1SUVmdch_lQ-Ub_zoTJKOtxTkwZMqyLD8xrbCq8CTcDQ/edit?usp=drivesdk)\n\n{sixtine} : \"Même sur ça tu as fais d'efforts... ?\"\n{alice} : S-Sixtine ! Tu sais bien que je peux juste... pas...",
    "{sixtine} : `Regarde le crusifix et le livre religieux à côté du lit d'Alice` \"Comment tu arrives à dormir à côté de ça... Clémence ne supporte même pas d'être à proximité d'une croix...\"\n{alice} : `Fait une petite moue`\" C'est elle qui s'est définie en temps qu'ennemi du divin souss prétexte que c'est sa nature. Mais ce genre de discipline tiens sa puissance en la Foi. Tant que tu l'as, qu'importe que ce tu es",
    "{clemence} : \"... Je sais que tu as la manie de dormir partout Sixtine... Mais dans mon cercueil tout en étant claustrophobe ?\"\n{sixtine} : `Dort à point fermé`",
    "{lena} : \"Contente que tu ai changé d'avis\"\n<:ly:943444713212641310> : \"J'avais besoin de changer d'horizon\"",
    "<:edelweiss:918451422939451412> : \"... Je peux t'aider ? On le dirait pas comme ça mais je me débrouille plutôt bien en soins\"\n<:lohica:919863918166417448> : \"Tu me rappelle juste quelqu'un, c'est tout... Et ton truc c'est pas plutôt la protection ?\"\n<:edelweiss:918451422939451412> : `Hausse les épaules` \"Je le fais parcequ'il y a déjà pas mal de personnes qui soignent ici, c'est tout\"",
    "{feli} : \"Dit Maraine, tu peux jouer ça au violon ?\"\n{lena} : \"Hum laisse moi voir ? Si Do# Mi Fa# Mi Ré# Do# Si Fa#... Oh. Je vois où tu veux en venir\"",
    "{lena} : \"Merci du coup de main Lio. Bon maintenant Shihu. Qu'est-ce que j'ai dit à propos de l'utilisation de la magie à la maison ?\"\n{shihu} : \"De... Pas utiliser la magie à la maison...\"\n{lena} : \"Et donc pourquoi on a du s'y mettre à trois pour éteindre les flammes noires dans votre chambre ?\"\n{shihu} : \"Mais il y avait un moustique...\"\n{lena} : \"Et tu penses sérieusement que risquer de réduire la maison en cendre pour un moustique est une bonne idée ?\"\n{shihu} : \"... au moins je l'ai eu...\"\n{lena} : \"... Vous êtes toutes les deux privées de dessins animés et de dessert pour une semaine.\"\n{shushi} : \"Mais j'ai rien fait moi !\"\n{lena} : \"Justement.\"",
    "{shihu} : \"Lena ne va pas du tout être contente quand elle vera que tu as pris un de ses pistolets d'airsoft...\"\n{shushi} : \"Elle n'en saura rien !\"\n{shihu} : \"Tu as même pas pris de protections..\"\n\n`Shushi visa une canette vide et tira, sans grand succès. La bille rebondit cependant sur le mur derrière et explosa contre un bouclier lumineux qui s'était formée devant la petite fille avant qu'elle n'ai eu le temps de bouger. Cette dernière regarda un peu confuse autour d'elle puis elle remarqua la chatte blanche assise à côté d'elle qui la regardait fixement`\n\n{shushi} : \"... s'il te plait le dis pas à Miman...\"\n{iliana} : \"Si tu ranges ça, peut-être\"\n{shihu} : \"(Pff, elle fait juste ça pour pas que Lena la tienne responsable également)\"",
    "{alice} : `Carresse très lentement Iliana en étant relativement tendue`\n{iliana} : `Se contente de ronronner sans bouger pour éviter de l'effrayer. Et puis elle aime bien les caresses`\n{alice} : `Se met à lui caresser le ventre en voyant qu'elle s'est mise sur le dos`\n{iliana} : `Essaye le plus possible d'ignorer son instinct de félin qui lui hurle d'essayer de mordiller cette main qui se balade sur son ventre, parcequ'elle n'a pas envie que cette même main la projette contre un mur dans un mouvement brusque avec toute la force d'une jeune vampire paniquée. Quelque chose lui dit que plusieurs de ses os ne l'appréciraient pas trop`",
    "{shushi} : \"Maman tu fais quoi ?\"\n{lena} : \"Hum ? Oh rien d'important\" `Glisse une feuille de papier derrière elle`\n{shushi} : \"Tu peux m'aider pour mes devoirs :< ? J'y arrive pas\"\n{lena} : \"Oh oui bien sûr ^^\"\n\n`Les deux quittèrent la pièce en laissant la dite feuille sur le bureau`\n\n:page_with_curl: [Feuille de papier](https://docs.google.com/spreadsheets/d/1l6csj2GjnaHMPYhPgqaji6Hs7bU68eb4XC_Ss2oxT-4/edit?usp=drivesdk)",
    "<:benedict:958786319776112690> : \"Bon j'ai fais ce que tu m'as demandé et selon mon correspondant, effectivement il a bien constaté qu'une âme incomplete est coincée au purgatoire depuis plusieurs décinies\"\n{shehisa} : \"Merci\"\n<:benedict:958786319776112690> : \"Juste merci :< ?\"\n{shehisa} : \"Merci Bénédicte d'avoir fait jouer tes relations surnaturelles afin de répondre à ma question\"\n<:benedict:958786319776112690> : \":< ça ira je suppose...\"",
    "{shehisa} : \"Tiens ça me fait penser, mais tu avais pas dit que tu libérais tes morts-vivants si ils était plus en état de se déplacer correctement ?\"\n<:kiku:962082466368213043> : \"C'est le cas\"\n{shehisa} : \"Bah heu... \" `Jette un oeuil à une goule qui n'avait plus qu'un tron`\n<:kiku:962082466368213043> : \"C'est pas ce que tu crois. C'est lui qui veut pas que je le libère\"",
    "{alice}<:stella:958786101940736061> : \"いや嘘だよ hihihiA, hihihiB, hihihiC, D, E !\"\n{shushi} : \"Elles ont pas bientôt finie... ? J'ai mal aux oreilles...\"\n{clemence} : \"Techniquement la chanson est finie, mais je doute qu'elles s'en arrêtent là malheureusement...",
    "{shehisa} : \"What is going on here? I'm a little out of sorts, I've been contemplating, Fallacies and things that scare me. Why not try to let go? I've been feeling out of order, I'm allowing change so, Take a good look, this is me. This is what I've come to be\"",
    "{lena} : \"FM comes in different colors, I believe... In the sewing machine, I've lost myself... Memories inside my heart are there to grieve... Color-coded by the love she gave to me...\"\n{luna} : \"Nostalgique ?\"\n{lena} : \"En quelques sortes, je suppose...\"",
    "{sixtine} : `Arrête de dessiner` Hum... Enfaite Anna... heu... comme tu est une fantôme tu peux posséder des gens ?\"\n<:anna:943444730430246933> : \"À vrai dire, pas vraiment... par contre Belle...\"\n`Les deux se tournèrent vers le miroir le plus proche où le reflet de Sixtine n'était absolument pas là où il devrait être, mais en train de fouiller dans le reflet de la boîte à bijoux d'Alice`\n{sixtine} : \"... C'est bien ce qu'il me semblait...\"",
    "{gweny} : \"Hey Clémence ! Tu veux faire une partie de paintball avec moi ce soir ?\"\n{clemence} : \"Pourquoi pas, mais il y aura Lena ?\"\n{gweny} : \"Hum...\"\n{clemence} : \"...\"\n{gweny} : \"...\"\n{clemence} : \"Je vais mettre plusieurs couches de tee-shirts\"\n{gweny} : \"Bonne idée, je vais faire de même\"",
    "{clemence} : \"Hé Ly. Il faut qu'on parle.\"\n<:ly:943444713212641310> : \"A-Ah ?\"\n{clemence} : `La fixe du regard en croisant les bras pendants de longues secondes` \"Oh et au final nan j'ai pas envie. J'espère juste pour toi que tu fais un minimum attention au passé de ceux que tu élimines et que tu ne te t'attaques pas à ceux qui se contente de vivre leur vie où aident les humains. Sinon tu risques d'avoir une vampire légèrement plus corriaces que les autres sur les bras.\"",
    "{clemence} : \"Hé Shihu, tu veux un conseil gratuis ? Si tu créais une formule, arrange toi pour que tu n'ai pas à la regréter quand tu seras plus grande\"\n{shihu} : \"Genre pas \"Turlututu et Tralala\" ?\"\n{clemence} : \"Exactement\"\n{alice} : \"Ca reste tout de même mieux que \"Magicabou la magicabou et magici magica bou\"\"",
    "{alice} : \"Tu veux que je te dise UΛ-BB4, chez moi tu es une tueuse en série qui a terrorisé la capitale pendant une décénie avant de disparaitre dans la nature avec le titre de personne la plus recherchée de la dimension\"\n{lena} : \"Si tu veux jouer à ce jeu, chez moi tu es une vampire qui a arrêté de grandir à l'âge de 11 ans et demi\"\n{alice} : \"Oh la poisse\"",
    "{lena} : \"UΛ-BB4, vu que tu te débrouille plutôt bien à longue distance, tu sais comment faire pour shotter un snipeur qui arrête pas de nous faire chier ?\"\n{lena} : \"Hé bah tu peux toujours essayer de combattre le feu par le feu, il me semble que tu as des snipeurs dans l'EEV3 AΣ-E9A, non ?\"\n{lena} : \"Ils se font tous surpasser malheureusement...\"\n{lena} : `Soupir` \"Soit. Je m'en occupe. Tu peux me montrer la direction stp ? Ca fait un moment que je suis pas allé dans le secteur AΣ du multivers\"",
    "{gweny} : \"Tiens Karaï ça faisait un moment\"\n`La poupée vint hug la jambe de Gwen sans rien dire`\n{gweny} : \"Ah. Je vois `Gwendoline prit la poupée des ses bras en lui caressant doucement la tête` Vas-y je t'écoute...\"\n{karai} : \"Pourquoi est-ce que je dois endurer tout ça... 300 ans à attendre pour qu'au final ma place soit prise par une autre version de moi-même... Et par dessus ça je peux même pas en finir...\"\n{gweny} : \"... Je n'ai pas de réponse à t'apporter malheureusement...\"\n\n{karai} : \"Prend soins de ton père pour moi s'il te plaît...\"\n{gweny} : \"Honnêtement je ne pense pas qu'il ai vraiment besoin que je veille sur lui mais j'y penserais\"\n{karai} : \"Merci...\"",
    "`Gwen était assise sur son lit en étant en train de surfer en ligne avec son ordinateur portable quand un mouvement dans le coin de la chambre attira son attention`\n{karai} : \"... Bonsoir Klironovia...\"\n{klikli} : \"Tiens, Karaï, ma poupée préférée `Elle prit la poupée et la plaça sur ses jambes tout en continuant sa navigation` Qu'est-ce qui t'amène donc ?\"\n{karai} : \"Oh hum... je voulais savoir si je pouvait dormir avec vous ce soir... Si ça vous dérange pas...\"\n{klikli} : \"Moi ça me va, et je pense pas que ça dérange les autres non plus. Mais je décline toute responsabilité au cas ou tu te retrouve sous moi durant la nuit\"\n{karai} : \"C'est un risque que je suis prête à prendre...\"",
    "{karai} : \"Ainsi donc avec Clara tu es devenue une soigneuse Alty...\"\n{alty} : \"ça pose un problème particulier ?\"\n{karai} : \"Oh heu non évidammant ! C'est juste que... dans ma timeline tu était plutôt du genre shinobi... ça me fait bizarre c'est tout...\"\n{alty} : \"Si j'en crois que ce les autres m'ont dit ce changement est plus ou moins... logique\"",
    "{alty} : \"Et voilà ^^ Et évite de courir trop vite la prochaine fois sinon tu vas retomber\"\n{shushi} : \":< Je veux un bisou magique !\"\n{alty} : \"Oh. `Fait un bisou sur le genou de Shushi` Et voilà ^^\"\n{shushi} : \"Viiii :D\"",
    "{luna} : \"Hé Gwen, je me demandais, mais on peut échanger nos épées pour quelques minutes s'il te plaît ?\"\n{klikli} : \"Hum, si tu veux mais pourquoi ?\"\n{luna} : \"Tester.\"",
    "<:stella:958786101940736061> : \"Oh Nacia' ! Tu te débrouilles avec ton réchauffement atmosphérique en ce moment ?\"\n<:nacialisla:985933665534103564> : \"On peut pas vraiment dire que tu m'aide Stella...\"",
    "<:kitsune:935552850686255195> : \"Oh c'est toi. Ta vandetta est toujours dans tes projets ? Il me semble que la population d'humains à quand même sacrément diminuée ces dernières années. Enfin... pas que les humains.\"\n<:nacialisla:985933665534103564> : \"On fait pas d'omelette sans casser des oeufs. Et pour répondre à ta question, j'ai tout de même prévu de leur faire quelques piqûres de rappels de temps en temps\"\n<:kitsune:935552850686255195> : \"J'aimerais juste que tu te souvienne qu'il y a pas que ces primates qui souffres de tes crises.\"\n<:nacialisla:985933665534103564> : \"Et je te rappelle que le génocide de tes décendantes n'a rien à voir avec moi.\"\n<:kitsune:935552850686255195> : \"Oh je ne parlais pas que pour mon \"espèce\" tu sais.\"",
    "<:lia:908754741226520656> : `Est couchée dans l'herbe avec ses soeurs à regarder les nuages` \"Dites... Vous pensez qu'on a combien de soeurs, nièces, petites nièces etceteras... ?\"\n<:lie:908754710121574470> : \"Hum... Tu connais très bien la réponse Lia...\"\n<:lia:908754741226520656> : `Lève un bras au ciel comme pour essayer d'attraper les étoiles en soupirant` \"Je reformule... Vous pensez qu'elles sont combien là haut ?\"\n<:lio:908754690769043546> : \"... J'aurais voulu les connaîtres aussi...\"\n<:lie:908754710121574470> : `Se redresse en regardant ses soeurs` \"ça ne sert à rien de s'apitoyer sur leurs sorts. Oui plus d'un millier d'années nous sépare de la mort de la dernière représentante de notre espèce, mais le fait est que Maman a réussi à se libérer et que nous as donné naissance. On est peut-être les kitsunes les plus jeunes à l'heure actuelle, mais de nous a le potenciel pour augmenter dragstiquement notre démographie\"\n<:liu:908754674449018890> : \"ça me fait bizarre de penser qu'on est en même temps tout en bas de l'arbre généalogique mais en même temps tout en haut...\"\n<:lie:908754710121574470> : `Secoue la tête` \"On est ni en bas ni en haut. On est une nouvelle branche à part entière\"",
    "<:rdmEvilGuy:866459027562954762> : \"Rien ni personne ne pourra m'arrêter ! Mon plan est parfait et j'ai anticipé toutes les possibilités ! Lorsque j'aurais assujeti le monde, personne ne remettra mes idées en question et je serais enfin reconnu pour mon génie ! Puis je le détruirais après avoir terminé mon vaiseau galactique et j'ira asurjetir la galaxie ! Et lorsque ça sera fait, je la détruirais également parceque je le peux et que j'en ai les moyens ! Mon armée de robot est invincible et vous allez toutes mourirs dans d'affreuses souf-ARG !\"\n<:helene:906303162854543390> : \"Shehisa !\"\n<:shehisa:919863933320454165> : \"Oh vous comptiez écouter son discourt pendant encore longtemps ? Vous savez pas comment c'est stressant de rester invisible derrière les gens en attendant le moment parfait pour les planter une dague dans la nuque...\"\n<:icealia:909065559516250112> : \"Oh non tu as bien fais je commençais à en avoir marre aussi\"",
    "<:benedict:958786319776112690> : \"Même si cette idée me plaît toujours pas, je dois avouer que tu fais une bonne enfant de coeur, tu as une plutôt bonne bouille quand tu as pas la bouche grande ouverte\"\n{alice} : M-merci ma Soeur, je suppose...\"",
    "<:benedict:958786319776112690> : \"Alice, même si je le conçois tu chantes très bien, est-ce que tu pourrais essayer de ne pas couvrir les autres à la chorale ? C'est un coeur, pas un solo\"\n{alice} : \"D-Désolée je m'en rend pas compte...\"",
    "{shihu} : \"Il me faut des cristaux magiques sinon je vais jamais y arriver...\"\n{shushi} : \"Tu en fais trop Shihu... Tu t'épuises pour rien, c'est pas grave si on y arrive pas...\"\n{shihu} : \"On doit y arriver sans l'aide de personne... On en peut plus de se faire rabaissée par Clémence dès qu'elle en a l'occasion, je veux lui montrer qu'on est capacle de réussir là où elle a échoué et lui rabatre le clapet... Pour une fois...\"\n{shushi} : \"Clémence a plus de quatre fois notre âge... On peut pas rivaliser !\"\n{shihu} : \"Mais on a quelque chose qu'elle n'a pas : Une réserve presque infinie de l'une des quatres énergies qui régient l'univers.\"\n{shushi} : \"T-Tu va finir par disparaitre si tu continue comme ça... J'ai... j'ai pas envie de me retrouver seule...\"\n{shihu} : \"... ça serait peut-être mieux ainsi... Ma simple existance a débilement compliqué la tienne...\"\n{shushi} : `Prend spontanément le controle de sa main droite pour se gifler elle-même` \"Je t'interdis de penser ce genre de truc tu m'entends !?\""
]

shopEventEndYears = [
    "{lena} : \"Alors Shu' tu as des résolutions pour l'année à venir ^^ ?\"\n{shushi} : \"Ré...so...lu... quoi ?\"",
    "{clemence} : \"Tu t'es surpassée pour ta robe de noël cette année Alice\"\n{alice} : \"Tu trouves ^^ ?\"\n{clemence} : \"Puisque je te le dis x)\"",
    "{feli} : `Fait des calins à tous le monde` \"Bonne année ^°^ !\"",
    "{shihu} : \"Mmg pourquoi il y a tout qui brille en ce moment... j'y vois rien...\"",
    "{icelia} : \"Vous avez prévu un truc pour cette fin d'année, vous ?\"\n{shehisa} : \"Oh on comptait juste aller voir nos parents, ça fais un moment qu'on n'est pas allé leur faire un coucou",
    "{sixtine} : \"Mais puisque je te dis que ce pull me va très bien...\"\n{alice} : \"Alleeeeez :<\"",
    "{alice} : `Regarde les babies roses à ruban que lui a offert Iliana` ...\n{sixtine} : \"Elle veut juste devenir ton amie... tu sais...",
]

shopEventOneDay = [
    {"date": (19, 1),
     "tabl": [
        "{shushi} : \"Joyeux naniversaire Miman !\" `Lui donne un joli dessin fait avec Sixtine`\n{lena} : \"Oh ^^ Merci Shu'\"",
        "{lena} : \"Hé Léna ! J'ai le droit à un jour de congé pour mon anniversaire ?\"\nC'est pas comme si tu étais un OC super occupée...",
        "{feli} : \"Joyeux anniversaire Maraine ^°^\"\n{lena} : \"Merci Féli ^^\"",
        "{lena} : \"Le temps passe mine de rien... Et c'est pas parceque je n'ai pas de forme physique que je ne le ressent pas\"\nSi je peux me permettre, tu as quand même grandit depuis ton premier chara-desing\n{lena} : \"Tu me fais toujours de la même taille qu'Alice par contre.\"",
        "{lena} : `Regarde Shushi courir après des ballons de baudruche` \"Parfois je me demande à quoi ressemble une vraie enfance...\"\nTu n'en a pas eu une super désagréable pourtant\n{lena} : `Soupir` \"Tu sais très bien que la seule enfance que j'ai ce sont les souvenirs que tu m'en a donné\"",
        "{lena} : \"J'aurais pensé que tu te ferais plus présente aujourd'hui tout de même. Techniquement, c'est ton anniversaie aussi\"\n{luna} : \"Je comprend pas vraiment ce délire des \"anniversaires\"\""
    ]
    },
    {"date": (14, 2),
     "tabl": [
        "{lena} : `Soupir` \"Je dirais pas non à un petit chocolat chaud aujourd'hui...\"",
        "{clemence} : \"Alors Alice, prête à être la boureau des coeurs du colège ?\"\n{alice} : \"Si tu crois que ça m'amuse...\"",
        "{lena} : `Regarde Ly dormir sous un arbre à l'aurée de la forêt` Je sais pas pourquoi je l'aurais pensé plus active aujourd'hui...",
        "<:john:908887592756449311> : \"Hum... Clémence ? J'ai... des chocolats pour toi...\"\n{clemence} : \"Hum, désolée, mais je dirgère pas trop les chocolats ^^'\"\n{alice} : `Facepalm derrière le dos de la vampire`"
    ]
    },
    {"date": (17, 4),
     "tabl": [
        "{alice} : \"Hé Clémence :D Regarde tous les oeufs que j'ai trouvés !\"\n{clemence} : \"Effectivement c'est beaucoup\"",
        "{sixtine} : \"Clémence... ? Hum... Tu veux partager un oeuf en chocolat... ?\"\n{clemence} : \"Désolée Sixtine... tu sais bien que je digère pas le chocolat...\"",
        "{lena} : \"J'ai jamais compris pourquoi les gens cachent des oeufs en chocolat pour Pâques\"\n{luna} : \"Ça ne t'empêches pas de le faire quand même\"\n{lena} : \"En même temps, même toi tu ne peux pas être insensibles à toutes leurs bouilles heureuses\"\n{luna} : \"Évite de parler en mon nom s'il te plaît... Mais oui\"",
        "{feli} : \"Aller Clémence viens chercher avec nous !\"\n{clemence} : \"Avec une main ça va être compliqué\"\n{feli} : '^' \"Tu n'as qu'à porter le panier !\""
    ]
    }
]

shopSeasonWinter = [
    "{clemence} : `Lit un grimoire en étant assise sur un fauteuil devant la cheminée`",
    "{lena} : \"Féli, si tu pouvais arrêter de dormir dans le feu ça m'arrangerais pas mal\"\n{feli} : \"Bah pourquoi :< ?\"\n{lena} : \"Parceque après tes soeurs et Shushi veulent faire la même chose. Et elles, elles ne sont pas fireproof.\"\n{feli} : \"Oh\"",
    "{alice} : `Boit un chocolat chaud en étant assise sur un fauteuil devant la cheminée`\n{sixtine} : `Arrive dans le salon avec sa couette sur les épaules et monte dans le fauteuil pour se blottir contre Alice`\n{alice} : \"ça va pas ?\"\n{sixtine} : \"Juste un cauchemar...\"\n{alice} : `patpat`",
    "{clemence} : `Regarde Félicité de haut en bas` \"Toi tu as encore dormi dans la cheminée\"\n{feli} : \"D: Non c'est faux !\"\n{clemence} : \"Tu es pleine de cendres, s'il te plaît x)\"",
    "{lena} : `Descend dans le salon à 3h du matin pour prendre un verre d'eau et voit une boule de poils blancs devant la cheminée` \"C'est pour ça qu'on porte des vêtements, Lio\"\n<:lio:908754690769043546> : `Eternue dans son sommeil`\n{lena} : `Soupir, remet une buche dans la cheminée puis pose une couverture sur la grosse boule de poils`",
    "{lena} : \"`Aide Altikia à ranger les courses` Dit-moi... elles t'ont fait un truc les vampirettes ou comment ça se passe ?\"\n{alty} : \"Hum ? Oh tu parles des gouses d'ails ? Bah Alice dort chez une amie et Clémence a dit qu'elle passerait la nuit à la bibliothèque donc je me suis dit que c'était l'occasion de changer un peu le menu ^^\"\n{lena} : \"Il va falloir passer un sacré coup de déodorisant...\"",
    "{gweny} : \"Ta mère ne va pas être contente si elle te choppe en train de fouiller dans son atelier\"\n{shushi} : \"Gwen, tu sais pourquoi Miman a autant de balles incendiaires ? Son élément c'est plutôt la glace, non ?\"\n{gweny} : \"Détourne pas le sujet. Mais pour répondre à ta question, je pense que ça remonte à l'époque où j'était encore flic à la ville. L'une des membres de la mafia locale était d'élément Métal Pur et il me semble que ta mère et elle se connaissaient personnellement. Et c'était pas l'amour fou entre les deux. Il me semble même que c'est la seule personne que Lena craind encore aujourd'hui, même si ça fait des années qu'elle n'a pas donné signe de vie. Et tu connais ta mère, quand quelque chose la contrari elle préfère contre attaquer, d'où le fait qu'elle ai passé pas mal de temps à mettre au point ces balles\"\n\n`Gwendoline se pencha pour prendre l'une des balles et l'observa attentivement pendant quelques secondes`\n\n{gweny} : \"Si je n'abuse, celle-là est prévu pour pénétrer un blindage ultra-épais et exploser à l'intérieur en libérant des sharpels explosifs. De quoi te descendre un élicoptère blindé d'une balle au vu de la puissance du fusil de Lena, si tu veux mon avis\"\n{shushi} : \"Wow...\"\n{shihu} : \"Je comprend mieux pourquoi elle veut pas nous voir jouer ici...\"",
    "{helene} : \"Ah Shi' ! Je t'ai fait une nouvelle tenue en fourure tu en pense quoi ?\"\n{shehisa} : `Prend la tenue et va se changer, puis se regarde dans un miroir` \"Hum... elle me plait bien. Et c'est vrai que je me sensait un peu... sous-vêtue ces derniers temps\"\n{helene} : \"Quelle idée de porter des trucs aussi cours en hiver aussi...\"",
    "`Gwen descendit dans le séjour pour aller préparer le petit déjeuné quand elle vit Lena en train de dormir sur le canapé. Sur la table se trouve plusieurs pièces de ce qu'elle devina être un nouveau fusil longue portée et en déduit que l'inkling a encore veillé jusqu'à point d'heure pour mettre au point un nouveau joujou\nEn approchant, elle vit Shushi assise à côté de sa mère en train d'essayer de résoudre un Rubik's cube silencieusement. En la voyant arriver, celle-ci mit doucement un doigt sur ses lèvres. Gwen lui sourit gentiment puis alla dans la cuisine`",
    "{clemence} : `Attend le trio de soeur en lisant assise (à l'ombre) à la terrasse d'un café tout en discutant avec Gwen, quand elle vit Sixitine venir seule` \"Comment ça tu es toute seule Sixtine ? Où sont Féli et Alice ?\"\n{sixtine} : \"Féli a dit qu'elle voulait aller voir la dernière expédition sur les dieux de la Grèce Antique et Alice a... dit un truc à propos de l'Eglise je crois...\"\n{clemence} : \"... Gweny, tu veux bien t'occuper d'aller chercher Alice et je me charge de Féli ?\"\n{gweny} : \"Je suis pas vraiment la bienvenue dans les églises catholiques aussi tu sais ?\"\n{clemence} : \"Déjà moins que moi...\"\n{sixtine} : \"Je peux y aller moi si vous voulez... Je suis qu'humaine...\"",    
]

shopSeasonSpring = [
    "{alice} : `Est assise sur une commode devant une fênetre et regarde la pluie arroser ses fleurs`",
    "{alice} : `Plante des fleurs dans le jardins tandis que Sixtine regarde les nuages`",
    "{luna} : \"Dans notre ancien chez nous les fleurs mourraient si elles avaient trop de Lumière\"\n{iliana} : \"Vraiment toutes ? Même ici il y a des fleurs qui vivent dans l'ombre\"\n{luna} : \"À quelques exeptions près, effectivement\"",
    "{lena} : \"Surtout tu oublie pas ton parapluie !\"\n{shushi} : \"Mais il fait grand soleil !\"\n{lena} : \"Il peut très rapidement se mettre à pleuvoir à cette saison, Shu'\"",
    "{alice} : \"J'ai hate que l'été arrive ! Tu viendras avec nous à la plage Clémence :D ?\"\n{clemence} : \"Hum, tu veux dire sous un soleil de plomb en maillot de bain avec la mer qui fait ses remous juste à côté alors que je déteste l'eau et arrive à me chopper des coups de soleil en hiver et sans reflets sur la neige ?\"\n{alice} : \"... Désolée c'était stupide...\"",
    "<:anna:943444730430246933> : \"Hé Alice, tu en penses quoi de cet ensemble... ?\"\n{alice} : \"Un peu viellot, mais ça te va bien\"",
    "{lena} : \"Oh est surtout, évitez de traîner trop avec Lia s'il vous plaît. Le printemps est sa saison de prédilection\"",
    "<:determination:867894180851482644> :\"`S'étire` C'est un chouette printemps que nous avons là\"\n{alice} : \"Dis Chara... tu avais promis de m'aider avec mes fleurs :<\"\n<:determination:867894180851482644> : \"Oh mais je l'ai fais, pourquoi crois-tu qu'il y a une golden flower au milieu ?\"\n{alice} : \"Oh heu... c'est pas vraiment ce que je voulais dire par là mais... merci quand même\"\n<:determination:867894180851482644> : \"`Facepalm` Ah tu demandais des conseils en jardinage normal, c'est ça ?\"\n{alice} : `Hoche la tête`",
    "<a:Ailill:882040705814503434> : \"Est-ce que tu t'es déjà demandée quel goût avait le sang ?\"\n{lena} : \"Non merci, et si vraiment j'ai envie de savoir, je préfère demander aux vampirettes plutôt qu'à toi.\"\n<a:Ailill:882040705814503434> : \"Tu es pas drôle tu sais\"",
    "{sixtine} : `Regarde les étoiles dans une prairie, puis remarque qu'elle n'est pas seule` \"... toi aussi tu brillais autant à l'époque où tu étais une étoile aussi... ?\"\n<:powehi:909048473666596905> : \"Et comment ! J'étais la plus grande, la plus chaude et la plus brillante de ma région...\"\n{sixtine} : \"Tu avais un système planétaire aussi ?\"\n<:powehi:909048473666596905> : \"Trois. Elles étaient plutôt sympatiques, et l'une d'entre elle abritait même la vie mais... `Soupir` Elles...\"\n{sixtine} : \"... Au moins je suis sûre qu'elles ont bien aimée ta supernova...\"\n<:powehi:909048473666596905> : \"Je... je pense... Leurs représentations se tenaient les mains sans vraiment avoir l'air effrayées...\""
]

shopSeasonsSummer = [
    "{alty} : \"Tu devrais aller dormir, Lena\"\n{lena} : \"C'est pas parceque tu fait deux têtes de plus que moi que tu es sensé agir comme ma mère Altikia\"\n{alty} : \"Lena... Tu as dormis que 3h en deux jours... Et regarde moi ce nombre de canettes de Coca... Je sais pas ce que tu fais, mais je suis sûre que ça peut attendre une bonne nuit de sommeil\"\n{lena} : \"ça va, t'en fais pas\"\n{alty} : \"ça fait deux fois que tu dévise et revise la même vis dans le même trou depuis qu'on parle\"\n{lena} : \"Peut-être qui si tu arrêtais de me parler je serais plus concentrée, effectivement.\"\n{alty} : \"`Soupir` Tu es en train de te défoncer la santé et je doute fortement que le jeu en vale la chandelle. Maintenant tu va aller te coucher ou sinon tu va voir que mes deux têtes supplémentaire vont faire une bonne différence quand je vais te forcer à y aller.\"\n{lena} : \"`Se lève d'un coup pour aller confrontrer Altikia, ce qui fût une erreur puisque qu'elle fût immédiatement prise de vertige et ses jambes se dérobèrent sous elle. Puis elle soupira` Tu as peut-être pas tord au fond...\"\n{alty} : \"Tu vois ?\"",
    "{alice} : \"Clémeeeence ? Tu peux venir nous surveiller pendant qu'on se baigne dans le lac s'il te plaît :< ? On voudrait apprendre à Shushi à nager\"\n{clemence} : \"Hum... Tu me demande ça à moi alors qu'il n'y a pas un nuage dans le ciel ?\"\n{alice} : \"Tu te doute bien que si je le fais c'est qu'il n'y a pas d'autres options... Gwen et Lena sont en ville aujourd'hui\"\n{clemence} : \"`Soupir` Je vais chercher des lunettes de soleils et le plus grand parasol de que je peux trouver alors... Mais si il arrive quoi que ce soit dans l'eau, c'est Féli qui s'en charge.\"\n{feli} : \"Capiche !\"\n{alice} : \"Viiii ^°^ Merci Clémence\"",
    "{sixtine} : \"`Fixe le plafond en arrivant pas à dormir lorsqu'elle entendit un bâtement d'ailes et senti une chauve-souris se blotir contre sa tête` Un chauchemar ?\"\n{alice} : `Répond par un petit couinement affirmatif`\n{sixtine} : `La prend doucement dans ses mains et la place contre sa poitrine en lui carressant la tête avec son pouce`\n{alice} : `Finit par se rendormir bercée par les bâtements de coeurs de sa soeur et ses caresses`",
    "<:liu:908754674449018890> : \"C'est pas parcequ'il fait chaud que tu dois porter encore moins de vêtements Liz tu sais ?\"\n<:lie:908754710121574470> : \"Je vois pas pourquoi tu me reproche ça alors que tu dis rien à Lio. Et puis c'est la mode en ce moment\"\n<:liu:908754674449018890> : \"Ton short est tellement bas qu'on voit ta culotte...\"\n<:lie:908754710121574470> : \"Et ? C'est dans notre nature tu sais d'être attrayante\"\n<:liu:908754674449018890> : \"C'est pas de l'attrayance ça c'est de la provocation, tu va finir par te faire vi... Ah. C'est exactement ce que tu veux enfaite, n'est-ce pas ?\n<:lie:908754710121574470> : \"Déjà 3 fois cette semaine, c'est fou ce que les males humains peuvent être irresponsables en ce moment :D\"\n<:liu:908754674449018890> : \"... Il en reste déjà plus tant que ça tu va pas tous leurs piquer leurs âmes en trois mois quand même...\"",
    "<:ruby:958786374759251988> : \"Julie, tu sais que tu as l'autorisation de porter ce que tu veux tant que c'est rouge en été, n'est-ce pas ?\"\n<:julie:910185448951906325> : \"Bien sûr Madame, mais je me sens moins à l'aise lors de mon travail si je ne porte pas mon uniforme\"\n<:ruby:958786374759251988> : \"Tu es sûr ? Tu dois être en sueur toute la journée avec pourtant\"\n<:julie:910185448951906325> : \"`Avec une courbette` ça ne me dérange pas, Madame. Et puis ça rend le bain du soir que plus agrébale\"",
    "{lena} : \"Arrêtez de vous plaindre ça fait à peine une heure qu'on est en randonné. Et est-ce que Clémence s'est plainte elle ? `Se retourne vers le groupe` Huh\"\n{sixtine} : \"`Soulève sa casquette humide pour révéler la chauve-souris en train de faire l'étoile de mer dans ses cheveux` Elle a fait une insolation dès les dix premières minutes...\"\n{lena} : `Soupir`\n<:edelweiss:918451422939451412> : \"Si vous voulez il y a un lac ombragé pas trop loin pas trop loin\"\n{lena} : \"Oh bonjour Edelweiss. Et je pense que c'est un bon endroit pour faire une pause effectivement...\"",
    "{helene} : \"Clémence vous me donnez chaud à être aussi vêtue...\"\n{clemence} : \"La seule chaleur que je ressent est celle des UV du soleil donc ça va t'étonnner mais je me sens plutôt au frais actuellement\"",
    "<:lio:908754690769043546> : `Regarde Alice et Sixtine essayer d'apprendre à nager à Shushi depuis le fond de son lac`\n{feli} : \"Coucou !\"\n<:lio:908754690769043546> : `Sursaute (peut-être vraiment parler de sursaut quand on flotte dans l'eau ?)` \"Oh c'est toi... J'oublie toujours que tu peux respirer sous l'eau aussi...\"\n{feli} : \"ça t'arrive jamais de sortir de ton lac de temps en temps ? Enfin à part pour ralonger nos combats\"\n<:lio:908754690769043546> : \"Mais j'aime bien mon lac moi... et puis il y a trop de problèmes là haut... Et pour ton deuxième point, les combats sont plus interressant contre vous qu'avec. C'est toujours trop rapide avec vous...\"\n{feli} : \"Oula, à ne pas sortir du contexte celle-là\"\n<:lio:908754690769043546> : \"Oh hum... désolée...\"",
    "{gweny} : `S'écroule dans son lit` \"J'en peut plus de ces canicules je dois changer de tee-shirts trois fois par jours...\"\n{karai} : `Ricane depuis l'étagère` \"Tu as toujours eu ce genre de problème Gweny\"\n{gweny} : \"ça m'aide pas vraiment ça Karaï...\"",
    "{alice} : `Regarde Iliana sous sa forme de chat en train de faire l'étoile de mer par terre` \"Hum... Tu... tu sais que tu aurais moins chaud en forme humaine... ? Enfin... moins de fourure et la sudation tout ça tout ça...\"\n{iliana} : \"Lena pourra plus me saquer si elle me voit sous forme humaine pendant tout l'été... Et j'ai nul part autre où aller...\"\n{alice} : \"...\" `Monte dans sa chambre et reviens quelques secondes plus tard avec un petit ventilateur qu'elle branche à côté de la chatte, puis elle s'assoit à côté`\n{iliana} : \"... Merci...\"",
    "{lena} : \"Hé Iliana, tu pourrais me rendre un service ?\"\n{iliana} : \"Mui ?\"\n{lena} : \"Tu as déjà entendu parler d'un certain Schrödinger ?\"\n{iliana} : \"... Oh zut j'ai totalement oublié ! Alice m'avait proposé de les accompagner à la plage, il faut que je me trouve un maillot de bain !\"",
    "{luna} : `Regarde Shushi et Shihu faire de la calligraphie, en controlant chacune leur main dominante respective`\n{lena} : \"Tu sais, si tu veux passer du temps avec elle il suffit de le dire hein\"\n{luna} : `Soupir` À quoi bon. Elle me considère sûrment même plus comme sa mère, et je suis nulle pour essayer de l'être\"\n{lena} : \"Tu te trompes. Quoi qu'il arrive, tu seras toujours sa mère. Elle s'est juste faite à l'idée qu'elle ne pourra pas avoir une relation \"normale\" de file-mère avec toi, et elle essaye de l'avoir avec moi à la place\"\n{luna} : \"ça me motive encore moins à essayer, ça Lena\"\n{lena} : \"Ce que je veux dire, c'est que ce n'est pas en restant cacher au fond de notre âme que ça va changer les choses, Luna\"",
    "`C'est l'heure du beach épisode ! Dans l'eau en face de vous vous pouvez observer le trio de soeurs et Shihu en train de jouer avec un ballon de plage dans la mer\nUn peu plus sur le côté vous pouvez voir Lia et Liz qui louchent pas mal sur un groupe de surfeur en étant à moitié jalouses du fait que Liu est parmis eux alors qu'elle ne semble pas vraiment être affectuée par la chad attitude qu'ils libèrent\nCeux qui font de la plongée sous-marine peuvent voir Lio en bikini (pour une fois) en train de récupérer les objets perdus par les nageurs et constater que quelques familles auront du mal à prendre leurs voitures sans leurs clés, et vous dites que voir une kitsune sortir de l'eau pour les leur rendre fait très fée sortant du lac et qui propose une version d'or ou d'argent d'un objet perdu\nAssise sur un rocher, vous pouvez retrouver Lena en train de lire les pieds dans l'eau tout en surveillant Gwen qui nage dangereusement près en lui lançant des regards malicieux de temps en temps pour vérifier si la jeune femme aux cheveux bleus fait attention à elle ou non\nEt enfin, collées l'une à l'autre, vous pouvez retrouver Clémence et Iliana qui, bien que toutes les deux en maillot de bain, ne veulent quitter l'ombre du parasol pour rien au monde`",
    "<:benedict:958786319776112690> : `Viens à la rencontre de Clémence qui attendait à la sortie de l'église` \"Tu es la soeur d'Alice, c'est cela ?\"\n{clemence} : \"C'est si compliqué à deviner ?\"\n<:benedict:958786319776112690> : `Croise les bras en faisant la moue` \"Il n'y a pas beaucoup de vampires qui attendrait pendant une dizaine de minutes devant un église d'autant plus qu'il ne fait pas encore nuit. D'autant plus qu'Alice nous avait dit que tu viendrais la chercher après le Chemin de Croix.\"\n{clemence} : \"Et je suppose que si ce n'est pas elle qui vient directement c'est parcequ'il s'est passé quelque chose ?\"\n<:benedict:958786319776112690> : \"Elle a perdu connaissance en milieu d'après-midi et ne s'est toujours pas réveillé depuis. Je pense que le soleil de plomb et la symbolique du chemin n'a pas fait du bien à ses... origines, aussi... résistante soit-elle. Peut-être que toi qui t'y connais un peu mieux sur ce sujet pourrait la réveiller. Si c'est le cas, je t'autorise à rentrer dans l'église pour aller la voir.\"\n{clemence} : `Soupir` \"Si un jour on m'aurait dit qu'on m'inviterais à rentrer dans une église...\"",
    "{clemence} : \"Hum... Où est Alice ?\"\n{feli} : \"Elle était avec nous non ?\"\n<:anna:943444730430246933> : \"Je croyais qu'elle t'avais rejoint après le Palais des Glaces Clémence !\"\n{clemence} : \"... Attendez... Vous avez emmené Alice, qui n'a aucun sens de l'orientation ni reflet dans un Palais des Glaces au beau milieu d'une fête foraine tellement bruyante que j'ai du mal à ne pas me cogner contre un mur si je me fit qu'à mes oreilles alors que je suis bien plus expérimenté qu'elle en echolocalisation et ne l'avez même pas attendue ou aidé !?\"\n{feli} : \"Elle mettait tellement longtemps on a pensé qu'elle était déjà sortie '^' !\"\n{clemence} : `Facepalm`\n<:anna:943444730430246933> : `Regarde ses pieds pas très fière d'elle et jette un coup d'oeuil à la vitrine la plus proche`\n<:belle:943444751288528957> : `Roule des yeux et sort du cadre de la vitrine`",
    "{iliana} : `Saute sur un lit (avec sa forme de chat) et s'instale confortablement pour la nuit mais a une révélation` \"Le lit de Shushi c'est le deuxième depuis la porte, c'est ça ?\"\n{alice} : `Hoche lentement la tête en tramblant un peu`\n{iliana} : \"D-Désolée ! Vos deux lits se ressemblent beaucoup dans le noir et depuis le sol !\" `Se relève et s'apprète à sauter`\n{alice} : \"A-Attent... tu peux rester si tu veux...\"\n{iliana} : \"Tu... es sûre ?\"\n{alice} : `Hoche une nouvelle fois la tête lentement` \"Clémence... veut vraiment que je fasse des efforts avec toi et... Féli n'a pas tord non plus quand elle dit que tu risques pas d'essayer de me manger, encore moins sous ma forme humaine donc... je... je veux bien... hum... te laisser une chance ?\"{iliana} : `Regarde les yeux roses d'Alice qui brillaient légèrement dans le noir puis viens à sa hauteur et se couche contre elle en ronronnant`",
    "{lena} : \"Au fait Krys, je dois te rajouter au club des hydrophobes ? T'en fais pas on mord pas. Enfin peut-être Iliana mais premièrement elle le fait que si elle est vraiment énervée et de deux je pense qu'elle s'y casserais les dents avec toi.\"\n<:krys:916118008991215726> : \"Le club des quoi ?\"",
    "<:lia:908754741226520656> : \"Pourquoi c'est moi qui doit garder mes petits frères et soeurs !?\"\n<:kitsune:935552850686255195> : \"Parceque Lio est occupée. Tu verras ils sont pas méchants, par contre cette portée là-\"\n<:lia:908754741226520656> : \"Laisse moi deviner, adores jouer dans les queues de leur mère ?\"\n<:kitsune:935552850686255195> : \"Pourquoi tu dis ça sur ce ton là ? Toi aussi tu aimais bien le faire à leur âge ?\"\n<:lia:908754741226520656> : \"Sauf que tu as trois fois plus de queues que moi Maman >< ! On pouvait chacun avoir la notre pour s'amuser, là ils sont presque à deux à me tirer sur chaqu'une d'entre elles !\"\n<:kitsune:935552850686255195> : `Ricane` \"Commence par t'assoir comme ça tu risques pas de leur tomber dessus si ils tirent trop fort. Et c'est pas tout mais je vais devoir y aller moi, bon courage. Oh et hésite pas à leurs montrer quelques tours. Même si ce sont de renardaux ordinaires, ils restent plutôt sensible à la magie. Ta soeur qui est actuellement en train de se frotter à tes jambes semble avoir une affinité avec le vent d'ailleurs, vous devriez bien vous entendre. `Avec un ton plus bas, sans vraiment s'adresser à Lia` J'aimerais bien que vous passiez plus de temps avec vos frères et soeurs \"ordinaires\" vous savez...\""
]

shopSeasonsAutomne = []

shopRepatition = [4, 5, 8, 3]                 # Shop's item category length

# Same, but for the roll command
rollMessage = ["Selon toute vraisemblance ce sera un **{0}**", "Puisse la chance être avec toi... **{0}** !", "Alors Alice tu as obtenu combien ? **{0}** ? **{0}** alors","Sur 100, les chances que la relation Akrisk tienne debout ? Hum... **{0}**", "Le nombre de lances que tu va avoir à esquiver est... **{0}**"]

randomEmojiFight = [
    '<:ffsad:896113677550366740>',
    '<:ffboude:875347226170384454>',
    '<:ffshrug:895280749366878258>',
    '<:ffbored:889900326902186045>'
]

lenRdmEmojiFight = len(randomEmojiFight)
mauvaisePerdante = "\n\nUnexpected situation: The enemy has won"

randChooseMsg = [
    "À quoi bon, de toutes façons tu vas choisir ce qui t'interresse vraiment\nMais bon voilà",
    "Je doute que tu tiennes compte de mon avis mais j'ai choisi",
    "Selon l'allignement des étoiles, tu va devoir prendre",
    "D'après les résidus de thé dans ma tasse...",
]

tablCat = ["Début du combat", "Compétence ultime", "Transcendance", "En éliminant un ennemi", "À la mort", "En étant ressucité", "Victoire (Bleu) en étant en vie", "Victoire (Bleu) en étant mort", "Défaite (Bleu)", "Victoire (Rouge) en étant en vie", "Victoire (Rouge) en étant mort","Défaite (Rouge)", "Bloquer une grosse attaque", "Réaction à la réanimation de plusieurs alliés", "Réaction à la réanimation de plusieurs ennemis", "Réanimer plusieurs allier en même temps", "Réaction à l'élimination d'un ennemi", "Réaction à l'élimination d'un allié"]

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
    start="Lena, parée à faire feu.",
    ultimate="Hey {target} ! J'ai un {skill} avec ton nom dessus !",
    limiteBreak="It's now or never ! {skill} !",
    onDeath="Tps.",
    onResurect="J'te revaudrais ça {target}",
    blueWinAlive="Une victoire en bonne uniforme",
    redWinAlive="Vous avez encore des progrès à faire",
    redWinDead="Pas mal. Mais pas suffisant",
    redLoose="Ahah, pas trop mal cette fois-ci. Mais ce n'était qu'un entrainement",
    reactBigRaiseAllie="Bien joué {caster}",
    reactBigRaiseEnnemy="Je dois avouer qu'il était pas mal celui-là. Je suppose que j'ai qu'à donner le meilleur de moi-même de nouveau",
    reactEnnemyKilled="Pas trop mal {killer}",
    reactAllyKilled="T'en fais pas {downed}, je m'en charge.",
    blockBigAttack="Hé Luna ! Un brisage de l'Espace Temps ça te dis ?\"*\n<:luna:909047362868105227> : \*\"C'est pas déjà ce que l'on était en train de faire ?",
    reactEnemyLb="`Ricane` Si ça vous chante",reactAllyLb="Belle {skill}, {caster}"
)

aliceSays = says(
    start="Ok, je vais faire de mon mieux, vous allez voir ☆⌒(ゝ。∂) !",
    onDeath="Kya ☆⌒(>。<) !",
    redWinAlive="Viii (≧▽≦) !",
    redWinDead="｡･ﾟ(ﾟ><ﾟ)ﾟ･｡",
    ultimate="Aller tous avec moi ! {skill} !",
    blueWinAlive="Alors, vous en avez dit quoi (≧▽≦) ?",
    onKill="J'aime pas la méthode direct (〃▽〃)...",
    onResurect="Prête pour le rappel ☆⌒(ゝ。∂)!",
    reactBigRaiseEnnemy="Je peux le faire aussi {caster}... Pas de quoi s'en venter...",
    bigRaise="Alors alors (〃▽〃)?",
    reactEnnemyKilled="En voilà un qui sera pas là pour mon final",
    reactAllyKilled="T'en fais pas {downed} !",
    reactAllyLb="Mow, je voulais terminer en apothéose moi :<",
    reactEnemyLb="Pff, tu appelles ça une démonstration, {caster} ?",
    limiteBreak="C'est l'heure de terminer en apothéose !"
)

clemSays = says(
    start="`Ferme son livre` Ok allons-y",
    ultimate="J'espère que tu es prêt pour te prendre un {skill} dans la face, {target} !",
    onDeath="Je t'ai sous estimé manifestement...",
    onResurect="Merci du coup de main",
    redWinAlive="Et bah alors, on abandonne déjà ?",
    blueWinAlive="ça sera tout pour moi",
    reactEnnemyKilled="Pas trop {killer}",
    redLoose="Pas la peine de prendre la grosse tête.",
    limiteBreak="Vous commencez sérieusement à m'ennuyer.",
    reactAllyLb="J'aurais pû le faire moi-même {caster}."
)

ailillSays = says(
    start="Tss, encore vous ?",
    onKill="Venez autant que vous êtes, ça changera rien",
    onDeath="Tu... paie rien pour attendre...",
    redWinAlive="Vous appelez ça un combat ?",
    reactBigRaiseEnnemy="Parceque vous pensez que ça changera quelque chose ?",
    reactEnemyLb="Juste une égratinure..."
)

jevilSays = says(
    start="Let's play a number game ! If you're HP drop to 0, I win !",
    onDeath="THIS BODY CANNOT BE KILLED !",
    redWinAlive="SUCH FUN !",
    redLoose="Such fun ! I'm exausted !"
)

lunaBossSays = says(
    start="Vous tenez tant que ça à vous mettre en travers de mon chemin ?\nSoit. Je vais vous montrer qu'un prêtresse des Ténèbres peut faire !",
    onKill="Disparait dans les ombres.",
    onDeath="Aha-",
    redWinAlive="Vous n'êtes pas les premiers. Et certainement pas les derniers.",
    redLoose="Mhf... Quand cesserez vous de suivre aveuglément cette Lumière corruptrice...",
    reactBigRaiseEnnemy="Vous devez en venir à là ? Soit !"
)

lunaDesc = """Luna est la conscience qu'ont aquis les Ténèbres injectés dans Lena par Gaster, dans leur dimension origielle (à Gaster et Luna, pas à Lena vu qu'elle vient d'ailleurs)

Dans cette dimension, les rapports entre la Lumière et les Ténèbres étaient inversés. C'était ces derniers qui permettaient aux habitants de voir et vitre, tandis que la Lumière représentait ce que nous apellons \"Obscurité\"
Luna a hérité du désir de destruction du monde corrompu qu'était le leur de Gaster lorsque celui-ci a utilisée Lena comme moyen de sortir de cette boucle génocidaire engagée par Chara, et le moins qu'on puisse dire c'est qu'elle y ai parvenu

Avec une puissance dépassant toutes les simulations de Gaster (qui n'avait pas prit en compte le status de personnage principal de Lena mais ça il pouvait pas savoir), Luna a effectivement brisé l'emprise que portait Le Premier Humain sur la dimention, mais a énormément déséquilibré l'équilibre entre les Ténèbres et la Lumière de cette dernière, ce qui causa plusieurs perturbations dans l'Espace Temps lui-même qui déchirèrent la dimension.
Cependant, puisqu'elle n'avait été crée que dans un seul but, la réalisation de celui-ci n'arrêta pas du tout Luna, qui commença à voir la Lumière et dimensions qui l'idolait comme une corruption de l'équilibre du multi-verse, qu'elle estime être son devoir en temps que Prêtresse des Ténèbres de supprimer.

Bien que Lena soit parcevenu à reprendre le contrôle, Luna n'en a pas abandonné des dessins pour autant, et son manque de consistance ainsi que son caractère têtu et compulsif l'empêche de vraiment se concentrer très longtemps sur autre chose, au dame de sa propre fille"""

shushiAltSays = says(
    start="Dézolé Miman... Mais on peut pa ti laizer fire.",
    onKill="Zi te plait...",
    onDeath="D-Dézolée !",
    blueLoose="Ze ferais miheu... la prozaine fois...",
    blueWinAlive="Wiiii !",
    reactBigRaiseAllie="Bien zoué {caster}"
)

shushiSays = says(
    start="Je vais te montrer ce que je peux faire Miman !",
    ultimate="C'est maintenant ou jamais !",
    onKill="Tu m'en voudras pas hein ? ?",
    onDeath="Miman !",
    onResurect="Ze veux encore dodo...",
    blueWinAlive="`Petite danse de la victoire` ?",
    blueWinDead="Bien zoué !",
    blueLoose="Je vais devoir faire mieux la prochaine fois !",
    redWinAlive="Alors alors ?",
    redWinDead="Peux mieux faire !",
    redLoose="Oh..."
)

lunaSays = says(
    start="Ok, on va bien voir si vous continuez de faire les malins",
    ultimate="Ça va être tout noiiiiiire !",
    onKill="J'ai vu des brindilles plus solides que toi...",
    onDeath="Je retiens.",
    blueWinAlive="Et sans bavures !",
    redWinAlive="C'est eux que tu comptes recruter Lena ? Ne me fais pas rire"
)

shihuSays = says(
    start="J'essayerai de pas tout casser !",
    redWinAlive="Boum Boum",
    ultimate="Préparez vous à ressentir le pouvoir des Ténèbes !",
    onKill="Tu risques de broyer du noir pendant un moment, dézolée !"
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
    onResurect="Mourir, c'est toujours pas drôle",
    reactBigRaiseAllie="On peut dire que tu sais y faire {caster}",
    reactEnemyLb="C'est beau de s'acharner inutilement..."
)

randomWaitingMsg = [
    "<a:bastuno:720237296322084905> Baston inkoming !",
    "<a:explosion:882627170944573471> Simulation de l'anéantissement à venir...",
    "<:invisible:899788326691823656> Erreur 404 : Blague non trouvée",
    "{alice} \"Conseil gratuit : Les OctoBooms font mal\"",
    "<a:giveup:902383022354079814>",
    "<a:Braum:760825014836002826> I am faster than you~"
]

johnSays = says(
    start="(Courage John. Montre lui que tu as appris à devenir un combattant.)"
)

liaSays = says(
    start="Ça vous dirait de danser avec moi ?",
    onKill="Oh déjà... ?",
    onDeath="Hii ! Compris compris !",
    redWinAlive="C'était marrant !",
    redLoose="Vous savez pas rire...",
    reactBigRaiseAllie="Toujours aussi jouissif {caster}",
    reactEnemyLb="Mow, je crois qu'ils sont un peu en colère"
)

liuSays = says(
    start="Hé ! Une course d'endurance vous en pensez quoi ?",
    onKill="Va falloir mieux gérer ta fatigue la prochaine fois",
    onResurect="Une seconde course ?",
    redLoose="Hé bah... Finalement c'est moi qui ai mordu la poussière",
    limiteBreak="Pas si vite !",
    reactEnemyLb="C'est bon tu as fini {caster} ?"
)

lioSays = says(
    start="Oh... Heu... Bonjour...",
    onKill="J- J'y suis allé trop fort ?",
    onResurect="Merci...",
    onDeath="Humf ! J'aurais du rester dans la forêt...",
    redWinAlive="Le monde des humains est... perturbant...",
    bigRaise="On lache rien...",
    reactBigRaiseEnnemy="Je peux faire ça aussi, tu sais...",
    reactAllyKilled="Vous commencez à me taper sur les nerfs...",
)

lizSays = says(
    start="Tiens donc, des nouvelles braises",
    ultimate="Allez quoi, déclarez moi votre flamme !",
    onKill="Woops, j'y suis allé trop fort manifestement",
    onDeath="Pff, vous êtes pas drôle",
    redLoose="Waw, je me suis jamais faite autant refroidir rapidement...",
    reactEnemyLb="T'enflamme pas trop vite {caster}."
)

julieSays = says(
    start="J'ai pas le temps pour ça ! Je dois encore faire la cuisine, nettoyer le hall, faire tourner une machine à laver et repasser les robes de Madame !",
    ultimate="Pas le choix...",
    limiteBreak="Courage vous autre !",
    onDeath="M-Madame... désolée...",
    onResurect="E-elle en saura rien, hein ?",
    bigRaise="Le temps joue contre nous ! Foncez !"
)

sixtineSays = says(
    start="`Baille en s'étirant`",
    ultimate="Laissez moi tranquille...",
    redWinAlive="Je retourne dessiner maintenant...",
    redLoose="Zzz...",
    reactBigRaiseAllie="Waw...",
    reactAllyLb="C'était joli à regarder..."
)

randomMaxDmg = [
    "Apparament, {icon} __{name}__ aurait réussi à infligé **{value}** dégâts en un seul combat, ce mois-ci ╮(︶▽︶)╭",
    "Hé tu sais quoi {icon} __{name}__ ? Ton record de dégâts mensuel en un seul combat est de **{value}**",
    "Hum... le record de dégâts de {icon} __{name}__ est que de **{value}** ce mois-ci ? Pas ouf",
    "Voyons voir... Ce mois-ci, {icon} __{name}__ a fait au maximum **{value}** en un combat",
    "Une à droite et une à gauche ! {icon} __{name}__ a réussi à faire **{value}** dégâts avec des beignes bien placées ce mois-ci !"
]

randomTotalDmg = [
    "Hé {icon} __{name}__ ! Tu veux savoir combien de dégâts tu as fait au total ? **{value}**",
    "Aufaite, tu voulais savoir combien de dégâts tu a fait {icon} __{name}__ au total ? **{value}**",
    "Tu veux savoir combien de dégâts tu as fait {icon} __{name}__ ? Hum... **{value}** ╮(︶▽︶)╭",
    "Pour {icon} __{name}__, j'ai ressencé **{value}** dégâts infligés jusqu'à présent"
]

randomMaxHeal = [
    "Alors voyons voir si {icon} __{name}__ est un bon healer... Son record de soins est de **{value}**, ce mois-ci",
    "Au maximum, tu as soigné **{value}** PV en un combat {icon} __{name}__ ce mois-ci",
    "Apparament, le record personnel de soins mensuel de {icon} __{name}__ est de **{value}**, ni plus ni moins ╮(︶▽︶)╭",
    "Savoir s'adapter à toutes les situations est crucial. Et {icon} __{name}__ a du avoir de bon réflexe pour avoir soigné **{value}** points de vie ce mois-ci"
]

randomTotalHeal = [
    "Au total, tu as soigné **{value}** PV {icon} __{name}__",
    "Tu as réussi à annuler **{value}** dégâts subis par tes alliés {icon} __{name}__, c'est pas trop mal (〃▽〃)! ",
    "Si j'en crois mes observations, {icon} __{name}__ aurait soigné un total de **{value}** PV... J'ai du mal regarder (ᓀ ᓀ)",
    "Tu n'aimes pas les barres de vies qui frittent avec le 0, n'est-ce pas {icon} __{name}__ ? Tu en est à **{value}** PV soignés, actuellement"
]

randomMaxRes = [
    "En un seul combat ce mois-ci, {icon} __{name}__ a réussi à ressuciter jusqu'à **{value}** alliés, quel ange gardien (ᓀ ᓀ)",
    "La mort c'est surcôté tu trouves pas {icon} __{name}__ ^^ ? Tu as ressucité jusqu'à **{value}** alliés en un seul combat durant le courant du mois"
]

randomTotalRes = [
    "La mort c'est juste une mauvaise grippe ☆⌒(ゝ。∂). Que {icon} __{name}__ a soigné **{value}** fois",
    "(－.－)…zzz {icon} __{name}__... résu... **{value}** fois...",
    "{icon} __{name}__ à l'air de bien maitriser les gestes de premiers secours, {il} a réanimé **{value}** fois un allié"
]

randomMaxTank = [
    "Hé bah ! {icon} __{name}__ a subis un maximum de **{value}** dégâts en un combat ce mois-ci ? J'espère que ses supports ont suivi (〃▽〃)",
    "{icon} __{name}__ préfère voir les ennemis dans le blanc des yeux apparament. En tous cas, c'est pas ses **{value}** dégâts subis en un combat qui le contesteront",
    "Je me demande ce qu'il y a dans la tête de {icon} __{name}__ pour s'être exposé à **{value}** dégâts ce mois-ci... A-t-{il} encore sa tête au moins ?"
]

randomTotalTank = [
    "Tiens donc ? {icon} __{name}__ aurait subi un total de **{value}** ? Ça fait pas mal quand même, je compatis pour ses soigneurs (￣ ￣|||)",
    "{icon} __{name}__, tu serais pas un peu mazo par hasard (￣ ￣|||) ? Tu es quand même à **{value}** dégâts totaux subis là..."
]

randomMaxArmor = [
    "L'important c'est de savoir quand utiliser ses capacités ☆⌒(ゝ。∂).\nRegardez {icon} __{name}__ : Son record d'armure donnée mensuel est à **{value}**",
    "Je suis plus partisante du \"Ils peuvent pas nous taper si ils sont morts\", mais bon au cas où je pourrais compter sur {icon} __{name}__.\nSon record d'armure donnée ce mois-ci est à **{value}** ╮(︶▽︶)╭",
    "{icon} __{name}__ n'aime pas vous voir subir des dégâts il faut croire. Ce mois-ci, {il} a donné au maximum **{value}** points d'armure en un combat"
]

randomTotalArmor = [
    "Il semblerais que {icon} __{name}__ préfère prévenir que guérir... Son total d'armure donné s'élève à **{value}**",
    "Le total d'armure donnée par {icon} __{name}__ s'élève à **{value}**, sans plus ni moins ╮(︶▽︶)╭",
    "Hé bah ! On peut dire que {icon} __{name}__ s'y connais en armure, {il} en a donné **{value}** points jusqu'à présent"
]

randomMaxKill = [
    "{icon} __{name}__ est une veritable terreur avec son record mensuel de **{value}** éliminations en un combat (･_├┬┴┬┴",
    "Va falloir que je me souvienne d'être particulirement prudente avec {icon} __{name}__ ( . .)φ...\nSon record d'élimination est de **{value}**...",
    "Toujours droit au but n'est-ce pas {icon} __{name}__ ? Tu as éliminé au maximum **{value}** ennemis ce mois-ci"
]

randomTotalKill = [
    "Le nombre de victimes de {icon} __{name}__ est de **{value}**.\n\nNon j'ai pas de commentaire à faire (＃￣0￣)",
    "Le nombre de victimes de {icon} __{name}__ est de **{value}**.",
    "Si j'ai bien compté, le nombre total d'élimiation par {icon} __{name}__ est à **{value}** (ᓀ ᓀ)\nFaites ce que vous voulez de cette information",
    "{icon} __{name}__ a éliminé au total **{value}** adversaires. J'espère qu'{il} garde en tête qu'{il} n'y est pas arrivé seul{e}"
]

randomRecordMsg = [
    "C'est cependant loin du record mensuel qui est de **{value}**, détenu par {icon} __{name}__",
    "Va falloir mieux faire si tu veux dépasser {icon} __{name}__, le sien est à **{value}** ☆⌒(ゝ。∂)",
    "Allez courage ! {icon} __{name}__ n'est qu'à **{value}** (^.~)☆",
    "Si tu veux viser les étoiles, sache que {icon} __{name}__ est à **{value}** ┐( ˘ ､ ˘ )┌",
    "Tu veux pas essayer de prendre le record ? Pour le moment c'est {icon} __{name}__ qui le détient avec **{value}**",
    "La concurence est dure par contre. Si tu cherches le haut du podium, il va falloir faire mieux que {icon} __{name}__ et ses **{value}**"
]

randomPurcenMsg = [
    "Ça fait quoi... **{purcent}** % du total de son équipe ?",
    "Hum... Je crois que ça doit faire... **{purcent}** % du total de son équipe ?",
    "D'après ma calculatrice, ça fait **{purcent}**% du total de son équipe"
]

randomTotalSupp = [
    "Qu'est-ce que ferais ton équipe sans toi {icon} __{name}__ ? Ton score de Soutien est à **{value}**",
    "Tiens donc, il semblerait que le score de Soutien de {icon} __{name}__ soit à **{value}**"
]

randomMaxSupp = [
    "On ne ménage pas ses efforts à ce que je vois {icon} __{name}__ ! En un combat, tu as réussi à obtenir un maximum de **{value}** points de Soutien durant ce mois",
    "Taper c'est bien beau, mais sans {icon} __{name}__, vous n'auriez pas tapé énormément. Son record de Soutien mensuel est de **{value}**"
]

aliceStatsNothingToShow = [
    ["Hum... Il semblerait que personna dans ton équipe a fait de dégâts jusqu'à présent ?"],
    ["Hé bah, ça vole pas haut niveau élimiation chez vous..."],
    ["On a qu'une seule vie comme on dit. Enfin particulièrement chez vous, où personne a réanimé personne","Conseil d'amie : Vous feriez mieux d'avoir quelqu'un qui puisse réanimer dans votre équipe, et pas toujours vous reposer sur nous pour vous sauver le postérieur"],
    ["Vous avez vraiment réussi à subir aucuns dégâts jusqu'à là ?"],
    ["Faut croire que vous aimer vous faire maraver la figure, personne a soigné personne dans votre équipe"],
    ["Vous savez qu'avoir un peu d'armure peu pas vous faire de mal, hein ?"],
    ["Je sais que le role de Support n'est pas particulièrement attractif, mais bon il reste quand même utile d'en avoir un"]
]

clemPosSays = says(
    start="J'en ai ma claque des gens de votre genre.",
    onKill="Un de plus, un de moins. Quelle importance",
    redWinAlive="Restez à votre place.",
    redLoose="Que..."
)

aliceExSays = says(
    start="Clémence...",
    onKill="...",
    onResurect="Merci...",
    blueWinAlive="ça... ça va mieux ?",
    bigRaise="Je y arriver probablement pas... S'il vous plaît..."
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

# ["Berserkeur","Observateur","Poids plume","Idole","Prévoyant","Tête brulée","Mage","Altruiste","Invocateur","Enchanteur","Protecteur"]
limitBeakGif = [
    'https://cdn.discordapp.com/attachments/927195778517184534/932778559150391366/20220118_002840.gif',  # Ber
    'https://cdn.discordapp.com/attachments/927195778517184534/932775385043709952/20220118_001608.gif',  # Obs
    'https://cdn.discordapp.com/attachments/927195778517184534/932774912391782490/20220118_001411.gif',  # PPlu
    'https://cdn.discordapp.com/attachments/927195778517184534/932776578058965102/20220118_002049.gif',  # Ido
    'https://cdn.discordapp.com/attachments/927195778517184534/932778559502700594/20220118_002719.gif',  # Pré
    'https://cdn.discordapp.com/attachments/927195778517184534/932777330605178920/20220118_002344.gif',  # TBru
    'https://cdn.discordapp.com/attachments/927195778517184534/932773655732158525/20220118_000607.gif',  # Mage
    'https://cdn.discordapp.com/attachments/927195778517184534/932773655342104606/20220118_000858.gif',  # Alt
    'https://cdn.discordapp.com/attachments/927195778517184534/932773655732158525/20220118_000607.gif',  # Enc
    'https://cdn.discordapp.com/attachments/927195778517184534/932777330978488391/20220118_002225.gif'  # Pro
]

lenaTipsMsgTabl = [
    "Est-ce que quelqu'un lit vraiment ça ?",
    "Si vous réalisez la commande /fight normal alors qu'il vous reste moins de 10 minutes de repos, votre combat sera mis en file d'attente et se lancera automatiquement une fois le décompte écoulé",
    "Une fois le tour 20 atteint en combat, il est plus possible de réanimer un combattant et tout le monde subis des dégâts en fonction de ses PVs Maximums",
    "Hé vous voulez un conseil de chargement inutile que tout le monde ne lit qu'une fois puis oubli leur existance ? En voilà un",
    "En fin de combat, vous gagnez de l'expérience en fonction des ennemis vaincu. Si un ennemi a été réanimé mais n'a pas été vaincu une seconde fois, il ne donne que la moitié de l'expérience qu'il devait donner",
    "En général, les combattants de dernière ligne font plus de dégâts que leurs camarades en mêlée, mais sont bien plus fragile",
    "Si une entité repoussée rencontre un obstacle, elle subit des dégâts Harmonie d'une puissance de 10 multipliée par le nombre de cases qu'il lui restait à parcourir",
    "Si une entité ne peux pas se téléporter parceque toutes les cases adjacantes à la cible sont occupées, elle s'inflige des dégâts Harmonie d'une puissance de 20",
    "L'Harmonie est une statistique spéciale qui est juste un beau mot pour dire \"Statistique la plus élevée\"",
    "L'Harmonie ne prend pas en compte les statistiques d'actions, mais ceux-ci sont cependant bien rajouté à la statistique d'Harmonie après sa définition",
    "Les Trancendances prennent en compte la statistique principale la plus élevée du lanceur, mais également sa meilleur statistique d'action, indépendamant de l'action en question",
    "Les compétences de réanimations prennent en compte la statistique d'action la plus élevée parmis les Soins, Armures ou Bonus",
    "Chaque réanimation accorde une armure absolue équivalente à 20% des PVs maximums du réanimé à ce dernier",
    "Les armures absolues protègent de tous types de dégâts à l'exeption de la Mort Subite et des coûts en PV des compétences démoniques",
    "Les armures absolues et normales absorbent des dégâts supplémentaires lorsqu'elles sont détruites. Par défaut, cette valeur est égale à votre niveau, mais certaines compétences peuvent influer dessus",
    "Donner une armure normale ou légère à un combattant qui possède déjà une armure normale ou absolue réduit la valeur de cette nouvelle armure. Par défaut, la réduction est de 50%, mais certaines compétences peuvent influer dessus",
    "Kiku et les Zombies commencent tous leurs combats avec le status \"Réanimée\"",
    "Certains ennemis comme l'OctoBOOM ne peuvent pas être réanimés",
    "Les Berserkeur ont besoin de pouvoir infliger des dégâts pour être des tanks efficace. Par conséquent leur donner un autre second role que DPT est pas vraiment une bonne idée",
    "Les statistiques des Idoles leur permettent prendre un role secondaire de soingneur, là où les Innovateurs peuvent se tourner vers l'armure si ils le désirent",
    "Les statistiques des Altruistes ainsi que leurs compétences propres en fond de très bon soigneur, mais avec les bons équipements ils peuvent aussi être de bon booster d'équipe",
    "Les Mages bénificent principalement de l'utilisation de compétence ultime, mais comme leur bonus dure 2 tours, ils peuvent le cumuler avec les compétences avec un tour de chargement",
    "Les Poids Plumes ont naturellement une endurance et une force relativement faible, mais cela est compensé par leur grande agilité qui leur permet d'esquiver ou d'infliger des coups critiques plus souvent que ses concurants de mêlée\nDe plus, à l'instar des Observateurs, leurs coups critiques infligent plus de dégâts",
    "Le taux d'esquive est calculé en fonction de la différence entre la précision de l'attaquant et l'agilité de l'attaqué.\nSi l'attaqué est plus agile, le taux de réussite de l'attaque est diminuée jusqu'au maximum la moitié de sa valeur\nÀ contratio, une précision plus élevée de l'attaquant peut lui donner jusqu'à deux fois plus de chances de toucher",
    "Le 19 de chaques mois, les records mensuels sont rénitialisés",
    "Il se peut que vous obtenez une récompense si vous possédez un certain pourcentage des objets obtenables dans le magasin ou en butin",
    "Lors d'un raid, vous êtes associé à une équipe dont le niveau moyen est similaire à celle de la votre. Cependant, cette équipe tierce n'obtient aucune récompense",
    "Vous vous souvenez de l'aspiration \"Stratège\" ? Ouais moi non plus",
    "Funfact : Tout à commencé sur une aire d'autoroute pendant que Lénaïc s'ennuyait à attendre que sa famille revienne de sa pause pipi",
    "Les Sorciers créent de petites détonnations quand ils éliminent un ennemi. Celles-ci prennent en compte les statistiques de Magie et de Dégâts indirects",
    "Les Têtes Brulées réduisent petit à petit les PV maximums de leurs cibles, ce qui les rends particulièrement efficaces contre les ennemis qui se soignent beaucoup",
    "Utiliser des compétences divines vous fait peu à peu perdre votre prise sur la réalité au fil du combat. Cela est représenté par des pertes de PV maximums lors de l'utilisation de ces dernières",
    "Utiliser des compétences démoniaques requière une quantité d'énergie si importe que vous perdrez une partie de vos PV courrants",
    "En lançant des combats normaux, vous avez une petite chance de revivre un combat passé qu'à vécu un des alliés temporaires\nCes combats sont appelés \"Combat par procuration\"",
    "Certaines compétences comme Mort Vivant ou Bolide peuvent rendre leur utilisateur invulnérable ou impossible à vaincre pendant un cours instant, permettant aux soigneurs d'essayer de leur sauver la mise",
    "Certaines compétences comme quelques transcendance ou Abnégations ont pour effet secondaire de réanimé les alliés vaincus dans la zone d'effet, si ils peuvent encore l'être",
    "Les Protecteurs, Vigilants et Enchanteurs sont trois aspirations qui tirent partie de leur capacités à attirer (et encaisser) les attaques adverses",
    "La Résistance Soin progresse plus rapidement si plusieurs soigneurs sont présents dans la même équipe",
    "Repose en paix, aspiration Invocateur",
    "Une intelligence élevée permet, en plus de pouvoir donner une bonne quantité d'armure, d'avoir une bonne probabilité d'effectuer des dégâts indirects critiques tout en diminuant la probabilité d'en recevoir",
    "Les statistiques de Clémence, Félicité, Sixtine et Alice augmente légèrement si plusieurs d'entre elles sont dans le même combat",
    "Lohica est plutôt mauvaise perdante et infligera __Poison d'Estialba__ à son éliminateur lorsque ses PVs tombent à 0",
    "Les Sorciers infligent des dégâts indirects critiques plus élevés que les autres aspirations",
    "Le Charisme de Liu, Lia, Liz et Lio augmente légèrement si au moins deux d'entre elles sont dans le même combat",
    "Alice n'aime pas vraiment que quelqu'un monte sur scène en sa présence",
    "Les compétences \"Haima\" et \"Pandaima\" ont une très bonne synergie avec l'une des compétences qui augmente le nombre de PAr supplémentaire des armures lorsqu'elles sont détruites. Elles peuvent ainsi déclancher leurs effets 5 fois, résultant en une réduction de dégâts encore plus conséquante",
    "Lors d'un combat normal contre les alliés temporaires, certains ont des malus spécifiques pour diminuer un peu leur efficacité au combat",
    "Par défaut, chaque combattant ne peut voler un nombre de PV supérieur à 45 fois leur niveau avec une même attaque. Cette limite est surtout là pour éviter que certain boss se soigne d'une quantité astronomique de PV lorsqu'ils attaquent.\nCependant, la limite de vol de vie de Clémence Possédée et Clémence Exaltée est à 100 fois la valeur de son niveau.",
    "En obtenant 75% du shop, vous obtiendrez une compétence dont l'effet est différent pour chaque aspiration. Dû à quelques soucis technique, cette compétence n'est pas affichée dans les listes de /inventory destination:compétence. Il faut donc utiliser /inventory nom:Transcendance ou /inventory nom:lb pour arriver directement sur sa page d'information",
    "Toutes les aspirations de supports, de soins et d'armures voient leur probabilité d'utiliser des options offensives augmenter lorsqu'ils n'ont plus beaucoup de DPT alliés en vie ou que le combat se rapproche du tour 20.",
    "Les dégâts de Mors Subite sont réduits de 90% sur les boss",
    "Les armes runiques, le passif Maitrise Elémentaire ainsi les compétences Convertion Elémentaire et Concentration Elémentaire sont le meilleur moyen de gagner des effets élémentaires.\nCes effets augmentent de 5% la puissance des compétences exclusives à leur élément et certaines compétences les consommes pour obtenir des effets supplémentaires.",
    "Les Sorciers et les Attentifs infligent des dégâts indirects critiques plus élevées que les autres aspirations.",
    "Les effets de dégâts indirects des Attentifs ont pour effet secondaire de réduire les soins reçus par leur cible en fonction de leur puissance.",
    "Les redirections de dégâts ne redirigent que les dégâts directs, à l'exeption des pattes de The Giant Ennemi Spider; bien que rien n'est affiché, cette dernière subit bien l'intégralité des dégâts indirects reçus par ses pattes",
    "Les débuts de combat sont les moments où les Idoles et les Innovateurs octroient des bonus plus puissant qu'à l'accoutumé. Cependant, ceux des Idoles voient leur puissance diminuer au fur et à mesure que leur équipe se fait vaincre tandis que ceux des Innovateurs dépérissent en même temps que l'équipe adverse"
]

ilianaSaysNormal = says(
    start="Puisse ce combat être bénéfique pour tous !",
    ultimate="Qu'est-ce que vous pensez du pouvoir de la Lumière ?",
    limiteBreak="Que la Lumière nous protège !",
    onKill="Je décline toute responsabilité en cas de tache blanche incrustée dans ta rénite",
    onDeath="Humf !",
    reactAllyKilled="J'aurais du faire plus attention, désolée",
    reactBigRaiseAllie="On reprend ses esprits et on y retourne"
)

ilianaSaysVsLuna = says(
    start="Tu nous fais encore une crise ?",
    ultimate="On tiens le bon bou, lachez rien !",
    onKill="T'en fait pas Luna !",
    onDeath="Ish...",
    onResurect="Merci bien",
    blueWinAlive="`S'assoit à côté de Luna, qui est trop fatiguée pour bouger, lui met la tête sur ses genoux puis caresse cette dernière en ronronnant`\"\n<:luna:909047362868105227> : \"Ili'...\"\n<:Iliana:926425844056985640> : \"Tu ferais la même chose si c'était moi, et tu t'es faite battre à plate couture, tu es pas en droit de contester\"\n<:luna:909047362868105227> : \"... `Ferme les yeux et s'endort peut de temps après`",
    blockBigAttack="Si tu crois que tu va m'avoir avec ça !",
    reactBigRaiseAllie="Je m'occupe des Ténèbres qui paralyse votre âme vous en faites pas !"
)

kitsuneSays = says(
    start="Mais c'est que vous êtes bien nombreux dites donc ^^",
    onKill="C'était trop intense pour toi ? Mais on a même pas encore commencé !",
    redWinAlive="C'était amusant, vous trouvez pas ?",
    reactBigRaiseEnnemy="Vos âmes m'appartiennent déjà, pourquoi résister ?"
)

lySays = says(
    start="Arf, mon truc c'est plutôt les squelettes et les zombies, vous savez ?",
    ultimate="Prêts pour le feu d'artifice ?",
    onDeath="Je suis pas assez bien payée pour ce genre de trucs...",
    onResurect="Je savais que j'aurais du prendre un totem de résurection... Mais merci",
    blueWinAlive="J'ai le droit de garder le loot ?",
    redWinAlive="Vous avez un lit qui vous attend",
    reactBigRaiseAllie="Si on doit en arriver à cette extremité, ça n'a pas vraiment l'air d'être bien parti...",
    reactBigRaiseEnnemy="Je doute que ça suffira à inverser la tendance !",
    reactEnnemyKilled="Tu as oublié ton totem de résurrection, {downed} ?"
)
gwenySays = says(start="Tachons de faire ça rapidement, ça vous vas ?",ultimate="Ok ça suffit là !",limiteBreak="Ok là vous m'avez énervée !",reactAllyLb="Espéront que ça changera la donne",reactAllyKilled="Je suppose que j'ai une nouvelle cible maintenant",reactBigRaiseEnnemy="En quoi c'est juste ça Lena !?\"*\n<:lena:909047343876288552> : \"*Vous pouvez le faire aussi, arrête de te plaindre",onKill="Tu m'en diras des nouvelles.",redWinAlive="Vous en revoulez ?")
klikliSays = says(start="Ok. Je vais m'en occuper rapidement",limiteBreak="OK, VOILÀ POUR VOUS !",onKill="Si tu veux revenir, j't'ai pas encore montrer tout ce dont je suis capable.",reactEnnemyKilled="Pff, j'peux le faire toute seule tu sais ?",ultimate="J'espère que tu as les yeux grands ouverts {target} !",redWinAlive="J'espère que vous en avez pris de la graine.")
altySays = says(start="'K, je vais faire de mon mieux",onKill="Désolée...",onResurect="Ok, second round !",reactAllyKilled="{downed} !",redWinAlive="Oulà, ça va aller ? Je crois qu'on y est allé un peu fort...",redWinDead="`Rigole` Bien joué tout le monde !")

shehisaSays = says(start="Ok, si on suit le plan, tout se passera bien",onKill="Tu aurais pu attendre que je soit partie avant de creuver quand même.",onDeath="Humf, c'était pas prévu ça...",reactAllyKilled="On lache rien !",reactBigRaiseEnnemy="C'était trop beau pour être vrai",reactAllyLb="Wowowo tu nous as fait quoi là {caster} ?",blueWinAlive="Tout s'est déroulé comme prévu",redWinAlive="Tout s'est déroulé selon le plan")

# Procur Temp stuff
procurTempStuff = {
    "Shushi Cohabitée":[0,
        ["Barrête de la cohabitation","dualHat","<:coaBar:911659734812229662>"],
        ["Robe de la cohabitation","dualDress",'<:coaDress:911659797076660294>'],
        ["Bottines de la cohabitation","dualBoost",'<:coaBoots:911659778995007528>'],
        [[0,0],[5,0.2],[2,0.3],[0.5,1],[0.5,1],[3,0.8],[3.6,0.8],[1,0.2],[0.5,0.3],[0.8,0.2]]
    ],
    "Luna prê.":[250,
        ["Boucle d'oreille ombrale",'lunaDarkPendant','<:linapendant:890599104902754326>'],
        ["Robe de soubrette ombrale ",'lunaDarkMaidDress','<:linadress:890598423152185364>'],
        ["Ballerines ombrales",'lunaDarkFlats','<:linaflats:890598400624586763>'],
        [[1.2,2.55],[1.15,0.4],[0.8,0.5],[1,1.2],[1,0.6],[0.2,0.3],[0,0],[0.25,0.35],[0.25,0.35],[0,0]]
    ],
    "Iliana prê.":[250,
        ["Casque de la neko de la lueur ultime", 'ilianaPreHead','<:zenithHead:913170464581484554>'],
        ["Armure de la neko de la lueur ultime", 'ilianaPreArmor','<:zenithArmor:913170492452646922>'],
        ["Sorolets de la neko de la lueur ultime", 'ilianaPreBoots','<:zenithBoots:913170512564334623>'],
        [[0.2,0.1],[1,2.5],[1,3],[0.5,0.9],[1.2,0.3],[3,0.05],[5,0.05],[1.2,0.2],[1,0.05],[1,0.05]]
    ],
    "Clémence Exaltée":[500,
        ["Boucles d'oreilles runiques","clemRune",'<:clemEarRings:920297359848636458>'],
        ["Veste sanguine",'clemRune','<:clemVeste:920300283068833874>'],
        ["Bottes sanguines","clemRune","<:clemBoots:920297554330157056>"],
        [[0.6,0.2],[1.25,1],[0.5,0.5],[2,.05],[1,0.3],[1.2,0.8],[1.7,1],[0.5,0.25],[1,0.031],[1,0.0005]]
    ],
    "Alice Exaltée":[0,
        ["Noeud en ruban chauve-souris","aliceExHat","<:batRuban:887328511222763593>"],
        ["Veste et jupe rose pâle","aliceExDress",'<:VesteEtJupeRose:877658944045219871>'],
        ["Ballerines roses pâles","aliceExShoes",'<:pinkFlat:867158156139692042>'],
        [[0.1,0.05],[0.5,0.4],[1.1,1.5],[0.8,0.25],[0.65,0.2],[1,1.35],[0.6,0.4],[1.2,0.15],[0.5,0.1],[1,0.1]]
    ]
}

lunaPreSays = says(
    start="C'est votre dernière chance de prendre la poudre d'escampette.",
    onKill="Quoi tu es surpris ? C'est pas faute d'avoir prévenu pourtant.",
    blueWinAlive="Pas la peine de revenir me faire chier, le résulta sera le même",
    reactBigRaiseEnnemy="Vous me faites une fleur vous savez, que vais pouvoir vous maraver la gueule une seconde fois sans ménagement",
    blockBigAttack="Chaton, c'est pas à toi de le faire d'habitude ?"
)

ilianaPreSays = says(
    start="J'espère que tu es en forme Luna...\"\n<:luna:909047362868105227> : \"Je suis toujours prête pour ce genre de trucs",
    ultimate="Oh on en a pas encore terminé !",
    reactEnnemyKilled="On a pas encore fini",
    blueWinAlive="`S'étire` Ce genre d'informités deviens de plus en plus récurrent...\"\n<:luna:909047362868105227> : \"Ca ne présage rien de bon..."
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

