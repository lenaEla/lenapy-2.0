from classes import *
from constantes import *

soupledown = skill("Choc Ténébreux","zz",TYPE_DAMAGE,500,140,range = AREA_CIRCLE_1,conditionType=["exclusive","aspiration",POIDS_PLUME],area = AREA_CIRCLE_2,sussess=70,ultimate=True,cooldown=4,emoji='<:darkdown:892350717384347648>',use=STRENGTH)
inkarmor = skill("Armure d'Encre","zy",TYPE_ARMOR,250,ultimate=True,effect="la",emoji = '<:inkArmor:866829950463246346>',area=AREA_ALL_ALLIES,cooldown=4,range=AREA_MONO)
coffeeSkill = skill("Suprématie du café","zx",TYPE_BOOST,500,effect=["lb","mc"],use=CHARISMA,conditionType=["reject","skill","zw"],area=AREA_ALL_ALLIES,emoji='<:coffee:867538582846963753>',cooldown=4,message="{0} prend le café avec ses alliés :")
theSkill = skill("Liberté du thé","zw",TYPE_BOOST,500,effect=["lc","mc"],use=CHARISMA,conditionType=["reject","skill","zx"],area=AREA_ALL_ALLIES,emoji='<:the:867538602644602931>',cooldown=4,message="{0} prend le thé avec ses alliés :")
gpotion = skill("Potion tonifiante","zv",TYPE_BOOST,200,emoji="<:bpotion:867165268911849522>",use=INTELLIGENCE,cooldown=3,effect="le",area=AREA_MONO,range=AREA_MONO)
bpotion = skill("Potion étrange","zu",TYPE_MALUS,200,cooldown=3,effect="lf",emoji="<:dpotion:867165281617182760>",use=INTELLIGENCE,area=AREA_CIRCLE_1,message="{0} lance une {1} sur {2}")
zelian = skill("R","zt",TYPE_INDIRECT_REZ,250,cooldown=5,effect="lj",emoji='<:chronoshift:867872479719456799>',use=None)
courage = skill("Motivation","zs",TYPE_BOOST,500,emoji ='<:charge:866832551112081419>',area=AREA_CIRCLE_2,use=CHARISMA,effect="lk",cooldown=3,range=AREA_MONO)
nostalgia = skill("Nostalgie","zr",TYPE_MALUS,500,emoji='<:nostalgia:867162802783649802>',effect="lm",cooldown=3,use=INTELLIGENCE)
draw25 = skill("Stop attacking or draw 25","zq",TYPE_MALUS,300,25,emoji="<:draw25:869982277701103616>",use=None,effect="lq",cooldown = 3,area=AREA_ALL_ENNEMIES,range=AREA_MONO,ultimate=True,conditionType=["exclusive","aspiration",PREVOYANT],message="{0} utilise sa carte joker !")
siropMenthe = skill("Neutralité du Sirop de Menthe","zp",TYPE_BOOST,500,effect=["lu","mc"],use=CHARISMA,area=AREA_ALL_ALLIES,emoji='<:menthe:867538622797054042>',cooldown=2,message="{0} prend un sirop de menthe avec ses alliés :")
unHolly = skill("Truc pas catho","zo",TYPE_MALUS,69,emoji='<:bravotakei:877202258348113960>',effect="lw",use=CHARISMA,message="{0} ||fait des trucs pas catho à destination de|| {2} :")
chaos = skill("Chaos Chaos !","zn",TYPE_UNIQUE,1000,range=AREA_MONO,area=AREA_ALL_ENTITES,sussess=200,emoji='<a:CHAOS:762276118224961556>',cooldown=5,ultimate=True,use=None,message="PLEASE ! JUST A SIMPLE CHAOS !")
contrecoup = skill("Contre-coup","zm",TYPE_INDIRECT_DAMAGE,250,effect="ln",cooldown=2,emoji='<:aftershock:882889694269038592>',use=MAGIE)
boom = skill("Réaction en chaîne","zl",TYPE_INDIRECT_DAMAGE,250,effect="lv",cooldown=2,emoji='<:bimbamboum:873698494874017812>',use=MAGIE)
balayette = skill("Baleyette","zk",TYPE_DAMAGE,100,90,range=AREA_MONO,area=AREA_CIRCLE_1,emoji='<:baleyette:873924668963291147>',cooldown=2)
firstheal = skill("Premiers secours","zj",TYPE_HEAL,100,35,emoji="<:bandage:873542442484396073>")
cure = skill("Guérison","zi",TYPE_HEAL,250,80,cooldown=5,emoji='<:cure:873542385731244122>')
lightAura = skill("Aura de Lumière I","zh",TYPE_PASSIVE,250,effectOnSelf="ly",emoji="<:AdL:873548073769533470>")
splatbomb = skill("Bombe splash","zg",TYPE_DAMAGE,100,cooldown=2,area=AREA_CIRCLE_1,power=55,emoji='<:splatbomb:873527088286687272>',message="{0} lance une {1} sur {2} :")
explosion = skill("Explosion","zf",TYPE_DAMAGE,1000,power=300,ultimate=True,cooldown=7,area=AREA_CIRCLE_2,sussess=80,effectOnSelf="mb",use=MAGIE,emoji='<a:explosion:882627170944573471>')
explosion2 = skill("Explosion","zf",TYPE_DAMAGE,1000,0,ultimate=True,cooldown=7,area=AREA_CIRCLE_2,sussess=500,effectOnSelf="na",use=MAGIE,emoji='<a:explosion:882627170944573471>',message="{0} rassemble son mana...")
protect = skill("Orbe défensif","ze",TYPE_ARMOR,200,emoji='<:orbeDef:873725544427053076>',effect="md",cooldown=3)
poisonus = skill("Vent empoisonné","zd",TYPE_INDIRECT_DAMAGE,500,emoji='<:estabistia:883123793730609172>',effect="me",cooldown=5,area=AREA_CIRCLE_1,use=MAGIE,message="{0} propage un {1} autour de {2} :")
invocBat = skill("Invocation - Chauve-souris","zc",TYPE_INVOC,500,invocation="Chauve-Souris",emoji="<:cutybat:884899538685530163>",shareCooldown=True,use=AGILITY)
multiMissiles = skill("Multi-Missiles","zb",TYPE_INDIRECT_DAMAGE,750,range=AREA_MONO,ultimate=True,emoji='<:tentamissile:884757344397951026>',effect="mf",cooldown=3,area=AREA_ALL_ENNEMIES)
monoMissiles = skill("Mono-Missiles","za",TYPE_INDIRECT_DAMAGE,250,range=AREA_CIRCLE_7,emoji='<:monomissile:884757360193708052>',effect="mf",cooldown=2)
splashdown = skill("Choc Chromatique","yz",TYPE_DAMAGE,500,140,AREA_MONO,ultimate=True,emoji='<:splashdown:884803808402735164>',cooldown=5,area=AREA_CIRCLE_2,damageOnArmor=5)
invocCarbE = skill("Invocation - Carbuncle Emeraude","yy",TYPE_INVOC,500,invocation="Carbuncle Emeraude",emoji="<:carbuncleE:884899235332522016>",cooldown=4,range=AREA_CIRCLE_3,shareCooldown=True,use=MAGIE)
invocCarbT = skill("Invocation - Carbuncle Topaze","yx",TYPE_INVOC,500,invocation="Carbuncle Topaze",emoji="<:carbuncleT:884899263459500053>",cooldown=4,range=AREA_CIRCLE_3,shareCooldown=True,use=ENDURANCE)
invocFee = skill("Invocation - Fée Soignante","yw",TYPE_INVOC,500,0,AREA_CIRCLE_3,cooldown=4,invocation="Fée soignante",emoji="<:selene:885077160862318602>",shareCooldown=True,use=CHARISMA)
thinkSkill = skill("Réfléchis !","yv",TYPE_BOOST,250,0,emoji="<:think:885240853696765963>",effect="mh",use=CHARISMA,cooldown = 3)
descart = skill("Je pense donc je suis","yu",TYPE_BOOST,250,range=AREA_MONO,emoji="<:descartes:885240392860188672>",effect='mi',cooldown=4,use=None,message="{0} a trouvé le sens de la vie !")
trans = skill("Transcendance","yt",TYPE_UNIQUE,0,initCooldown=3,cooldown=5,emoji="<:limiteBreak:886657642553032824>",description="Un sort particulier qui a un effet différent en fonction de l'aspiration du lanceur\n\nUtiliser Transcendance vous empêche d'utiliser une compétence ultime lors du prochain tour",use=HARMONIE,shareCooldown=True)

transMelee = copy.deepcopy(trans)
transMelee.type,transMelee.power, transMelee.name = TYPE_DAMAGE,200, transMelee.name + " - Lasers Chromanergiques Prompts, Monocible"

transLine = copy.deepcopy(trans)
transLine.type,transLine.power,transLine.area, transLine.name = TYPE_DAMAGE,180,AREA_LINE_6, transLine.name + " - Lasers Chromanergiques Prompts, Ligne"

transCircle = copy.deepcopy(trans)
transCircle.type,transCircle.power,transCircle.area,transCircle.name = TYPE_DAMAGE,160,AREA_CIRCLE_2, transCircle.name + " - Explosion Prompte"

transHeal = copy.deepcopy(trans)
transHeal.type,transHeal.power,transHeal.area,transHeal.range, transHeal.name, transHeal.cooldown = TYPE_HEAL,100,AREA_ALL_ALLIES,AREA_MONO, transHeal.name + " - Voie de l'Ange Prompte",7

transInvoc = copy.deepcopy(trans)
transInvoc.type, transInvoc.invocation, transInvoc.name  = TYPE_INVOC,"Titania", transInvoc.name + " - La lumière brille brille brille"

transShield = copy.deepcopy(trans)
effTransShield = effect("Transcendance - Armure","transArm",HARMONIE,overhealth=100,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,emoji=sameSpeciesEmoji("<a:transArmorB:900037831257358378>","<a:transArmorR:900037817449717800>"),turnInit=3)

transShield.type,transShield.area,transShield.range,transShield.effect,transShield.name, transShield.cooldown = TYPE_ARMOR,AREA_ALL_ALLIES,AREA_MONO,[effTransShield],transShield.name + " - Extra Armure d'Encre",7

burst = skill("Bombe ballon","ys",TYPE_DAMAGE,0,35,area=AREA_CIRCLE_1,sussess=60,emoji='<:burstBomb:887328853683474444>',use=HARMONIE)
lapSkill = skill("Invocation - Lapino","yr",TYPE_INVOC,0,invocation="Lapino",cooldown=4,shareCooldown=True,emoji='<:lapino:885899196836757527>',use=CHARISMA)
adrenaline = skill("Adrénaline","yq",TYPE_HEAL,250,cure.power,cooldown=5,emoji='<:adrenaline:887403480933863475>',use=INTELLIGENCE)
blindage = skill("Blindage","yp",TYPE_BOOST,350,0,AREA_MONO,effect="mj",cooldown=3,use=None,emoji="<:blindage:897635682367971338>")
secondWind = skill("Second Souffle","yo",TYPE_HEAL,350,150,AREA_MONO,emoji='<:secondWind:897634132639756310>',cooldown=99,use=ENDURANCE)
isolement = skill("Isolement","yn",TYPE_ARMOR,500,0,AREA_MONO,emoji='<:selfProtect:887743151027126302>',cooldown=5,effect="ml")
bombRobot = skill("Invocation - Bombe Robot","ym",TYPE_INVOC,500,0,AREA_CIRCLE_3,invocation="Bombe Robot",cooldown=2,shareCooldown=True,emoji='<:autobomb:887747538994745394>',use=STRENGTH)
linx = skill("Œuil de Linx","yl",TYPE_BOOST,500,range=AREA_MONO,area=AREA_CIRCLE_2,emoji='<:noeuil:887743235131322398>',effect="mm",cooldown=4)
stalactic = skill("Stalactite","yk",TYPE_DAMAGE,300,60,emoji='<:stalactit:889089667088142346>',cooldown=3,sussess=60,range=AREA_DIST_5)
uppercut = skill("Uppercut","yj",TYPE_DAMAGE,200,70,AREA_CIRCLE_1,emoji='<:uppercut:889091033718194196>',cooldown=2,message="{0} donne un {1} à {2} :")
oneforall = skill("Un pour tous","yi",TYPE_BOOST,500,range=AREA_MONO,area=AREA_DONUT_2,cooldown=5,use=CHARISMA,effect="mo",effectOnSelf="mp",description="Une compétence qui permet d'augmenter les résistances de ses alliés au détriment des siennes",conditionType=["exclusive","aspiration",ALTRUISTE],emoji='<:oneforall:893295824761663488>')
secondSun = skill("Le second Soleil","yh",TYPE_MALUS,350,0,AREA_MONO,area=AREA_ALL_ENNEMIES,cooldown=5,effect="mq",emoji='<:iwanttosleeppls:893241882484817920>',use=CHARISMA,conditionType=["exclusive","element",ELEMENT_LIGHT])
kiss = skill("Baisé divin","yg",TYPE_HEAL,69,55,AREA_DONUT_2,emoji='<:welp:893251469439008809>',message="{0} fait un gros bisou à {2} :")
onstage = skill("En scène !","yf",TYPE_BOOST,750,0,AREA_MONO,["exclusive","aspiration",IDOLE],True,effect="mr",emoji='<:alice:893463608716062760>',area=AREA_DONUT_7,use=CHARISMA,cooldown=5,message="{0} éléctrise l'ambience !")
icelance = skill("Lame glacée","ye",TYPE_DAMAGE,500,120,AREA_DIST_6,["exclusive","element",ELEMENT_WATER],True,emoji='<:emoji_47:893471252537298954>',cooldown=5,message="{0} fait appaître une lame de glace géante sous {2} :")
rocklance = skill("Lame rocheuse","yd",TYPE_DAMAGE,500,120,AREA_CIRCLE_3,["exclusive","element",ELEMENT_EARTH],True,emoji='<:emoji_46:893471231641276496>',cooldown=5,message="{0} fait appaître une lame de roche géante sous {2} :",use=MAGIE)
infinitFire = skill("Brasier","yc",TYPE_DAMAGE,500,90,AREA_DIST_5,["exclusive","element",ELEMENT_FIRE],True,emoji='<:emoji_44:893471208065101924>',cooldown=5,message="{0} déclanche un brasier autour de {2} :",area=AREA_LINE_3,use=MAGIE)
storm = skill("Ouragan","yb",TYPE_DAMAGE,500,90,AREA_CIRCLE_2,["exclusive","element",ELEMENT_AIR],True,emoji='<:emoji_44:893471179023732809>',cooldown=5,message="{0} déclanche un ouragan autour de {2} :",area=AREA_CIRCLE_2,use=MAGIE)
innerdarkness = skill("Ténèbres intérieurs","ya",TYPE_INDIRECT_DAMAGE,500,0,conditionType=["exclusive","element",ELEMENT_DARKNESS],ultimate=True,emoji='<:emoji_48:893471268957990982>',cooldown=5,effect="ms",use=MAGIE,area=AREA_CIRCLE_1)
divineLight = skill("Lumière divine",'xz',TYPE_INDIRECT_HEAL,500,conditionType=["exclusive","element",ELEMENT_LIGHT],ultimate=True,emoji='<:emoji_49:893471282815963156>',cooldown=5,effect=["mu","mv"],use=CHARISMA,area=AREA_CIRCLE_1)
swordDance = skill("Dance des sabres","xy",TYPE_DAMAGE,350,power=70,use=STRENGTH,emoji='<:sworddance:894544710952173609>',cooldown=3,area=AREA_CIRCLE_1)
shot = skill("Tir net","xx",TYPE_DAMAGE,350,75,AREA_CIRCLE_6,emoji='<:shot:894544804321558608>',cooldown=3,use=STRENGTH,damageOnArmor=1.5)
percingLance = skill("Lance Perçante","xw",TYPE_DAMAGE,350,power=70,emoji='<:percing:894544752668708884>',cooldown=3,area=AREA_LINE_2,range=AREA_CIRCLE_2)
percingArrow = skill("Flèche Perçante","wv",TYPE_DAMAGE,350,power=60,emoji='<:percingarrow:887745340915191829>',cooldown=3,area=AREA_LINE_2,range=AREA_DIST_5)
highkick = skill("HighKick","wu",TYPE_DAMAGE,350,power=100,range=AREA_CIRCLE_1,emoji='<:highkick:894544734759030825>',cooldown=3)
multishot = skill("Tir Multiple","wt",TYPE_DAMAGE,350,power=60,range=AREA_DIST_4,emoji='<:name:894544834780622868>',cooldown=3,area=AREA_CONE_2)
bleedingArrow = skill("Flèche Hémoragique","ws",TYPE_DAMAGE,350,35,AREA_DIST_5,effect='mx',emoji='<:bleedingarrow:894544820071178292>')
bleedingDague = skill("Dague Hémoragique","wr",TYPE_DAMAGE,350,45,AREA_CIRCLE_2,effect='mx',emoji='<:bleedingdague:894552391444234242>')
affaiblissement = skill("Affaiblissement","wq",TYPE_MALUS,350,effect="my",cooldown=3,use=INTELLIGENCE,emoji='<:affaiblissement:894544690400071750>')
provo = skill("Provocation","wp",TYPE_MALUS,350,emoji='<:supportnt:894544669793476688>',effect='mz',cooldown=3,use=INTELLIGENCE)
flameche = skill("Flamèche","wo",TYPE_DAMAGE,100,40,area=AREA_CONE_2,use=MAGIE,conditionType=["exclusive","element",ELEMENT_FIRE],emoji='<:flame1:897811975675969556>')
flame = skill("Flamme","wn",TYPE_DAMAGE,250,60,area=AREA_CONE_2,use=MAGIE,conditionType=["exclusive","element",ELEMENT_FIRE],cooldown=3,emoji='<:flame2:897812264185376798>')
pyro = skill("Pyrotechnie","wm",TYPE_DAMAGE,500,80,area=AREA_CONE_2,use=MAGIE,conditionType=["exclusive","element",ELEMENT_FIRE],cooldown=5,emoji='<:flame3:897812061139140651>')
ecume = skill("Ecume","wl",TYPE_DAMAGE,100,50,use=MAGIE,conditionType=["exclusive","element",ELEMENT_WATER],emoji='<:splash1:897844189184811078>')
courant = skill("Courant","wk",TYPE_DAMAGE,250,75,use=MAGIE,conditionType=["exclusive","element",ELEMENT_WATER],cooldown=3,emoji='<:splash2:897844205198659594>')
torant = skill("Torrant","wd",TYPE_DAMAGE,500,100,use=MAGIE,conditionType=["exclusive","element",ELEMENT_WATER],cooldown=5,emoji='<:splash3:897844380491202581>')
brise = skill("Brise","wj",TYPE_DAMAGE,100,40,use=MAGIE,conditionType=["exclusive","element",ELEMENT_AIR],area=AREA_CIRCLE_1,emoji='<:wind1:897845097775915038>')
storm2 = skill("Tempête","wi",TYPE_DAMAGE,250,60,use=MAGIE,conditionType=["exclusive","element",ELEMENT_AIR],area=AREA_CIRCLE_1,cooldown=3,emoji='<:wind2:897845144299110441>')
tornado = skill("Tornade","wh",TYPE_DAMAGE,500,80,use=MAGIE,conditionType=["exclusive","element",ELEMENT_AIR],area=AREA_CIRCLE_1,cooldown=5,emoji='<:wind3:897845187940868156>')
stone = skill("Caillou","wg",TYPE_DAMAGE,100,50,use=MAGIE,conditionType=["exclusive","element",ELEMENT_EARTH],emoji='<:rock1:897846015552532531>')
rock = skill("Rocher","wf",TYPE_DAMAGE,250,75,use=MAGIE,conditionType=["exclusive","element",ELEMENT_EARTH],cooldown=3,emoji="<:rock2:897846028512944138>")
mont = skill("Montagne","we",TYPE_DAMAGE,500,100,use=MAGIE,conditionType=["exclusive","element",ELEMENT_EARTH],cooldown=5,emoji='<:rock3:897846042576420874>')
stingray2 = skill("Pigmalance","wd",TYPE_DAMAGE,500,70,AREA_CIRCLE_7,ultimate=True,emoji='<:stingray:899243721378390036>',cooldown=5,area=AREA_LINE_6,sussess=70,description="Cette compétence dure **2** tours")
stingray = skill("Pigmalance","wc",TYPE_DAMAGE,500,70,AREA_CIRCLE_7,ultimate=True,emoji='<:stingray:899243721378390036>',cooldown=5,area=AREA_LINE_6,sussess=70,effectOnSelf="nb")
dark1 = skill("Cécité","wb",TYPE_DAMAGE,100,50,use=MAGIE,conditionType=["exclusive","element",ELEMENT_DARKNESS],emoji='<:dark1:899599162566410280>')
dark2 = skill("Obscurité","wa",TYPE_DAMAGE,250,75,use=MAGIE,conditionType=["exclusive","element",ELEMENT_DARKNESS],cooldown=3,emoji='<:dark2:899599147399807006>')
dark3 = skill("Pénombre","vz",TYPE_DAMAGE,500,100,use=MAGIE,conditionType=["exclusive","element",ELEMENT_DARKNESS],cooldown=5,emoji='<:dark3:899598969930399765>')
light1 = skill("Lueur","vy",TYPE_DAMAGE,100,40,use=MAGIE,conditionType=["exclusive","element",ELEMENT_LIGHT],area=AREA_CIRCLE_1,emoji='<:light1:899598879576690689>')
light2 = skill("Éclat","vx",TYPE_DAMAGE,250,60,use=MAGIE,conditionType=["exclusive","element",ELEMENT_LIGHT],area=AREA_CIRCLE_1,cooldown=3,emoji='<:light2:899598896613969970>')
light3 = skill("Éblouissement","vw",TYPE_DAMAGE,500,80,use=MAGIE,conditionType=["exclusive","element",ELEMENT_LIGHT],area=AREA_CIRCLE_1,cooldown=5,emoji='<:light3:899599232628043787>')
derobade = skill("Dérobade","vv",TYPE_BOOST,350,0,AREA_DONUT_3,cooldown=4,effectOnSelf="nd",effect="nc",emoji='<:derobade:899788297868558337>',use=INTELLIGENCE)
ferocite = skill("Férocité","vu",TYPE_PASSIVE,200,0,emoji='<:ferocite:899790356315512852>',effectOnSelf="ne",use=None)
ironWillSkill = skill("Volontée de Fer","vt",TYPE_PASSIVE,200,0,emoji='<:ironwill:899793931762565251>',effectOnSelf="nh",use=None)
royaleGardeSkill = skill("Garde Royale","vs",TYPE_PASSIVE,200,0,emoji='<:gardeRoyale:899793954315321405>',effectOnSelf="ng",use=None)
defi = skill("Défi","vr",TYPE_PASSIVE,200,0,emoji='<:defi:899793973873360977>',effectOnSelf="nf",use=None)
dissimulation = skill("Dissimulation","vq",TYPE_PASSIVE,0,effectOnSelf="nj",use=None,emoji="<:dissimulation:900083085708771349>")
bleedingTrap = skill("Piège de lacération","vp",TYPE_INDIRECT_DAMAGE,500,effect="mx",cooldown=5,area=AREA_CIRCLE_1,use=STRENGTH,message="{0} place et déclanche un {1} autour de {2} :",emoji='<:lacerTrap:900076484230774807>')
# vn already taken (Prévention)
convert = skill("Convertion","vm",TYPE_ARMOR,350,range=AREA_DONUT_5,effect="nk",cooldown=3,emoji='<:convertion:900311843938115614>')
vampirisme = skill("Vampirisme","vl",TYPE_INDIRECT_HEAL,350,range=AREA_DONUT_5,effect="no",cooldown=3,emoji='<:vampire:900312789686571018>')
heriteEstialba = skill("Héritage - Fée d'Estialba","vk",TYPE_PASSIVE,0,effectOnSelf='np',emoji='<:heriteEstialba:900318953262432306>',use=MAGIE)
heriteLesath = skill("Héritage - Famille Lesath","vj",TYPE_PASSIVE,0,effectOnSelf='ns',emoji='<:hertiteLesath:900322590168608779>')
focal = skill("Focalisation","vi",TYPE_INDIRECT_DAMAGE,1000,range=AREA_CIRCLE_3,cooldown=7,effect=["me","me","me"],effectOnSelf="me",emoji='<:focal:901852405338099793>',shareCooldown=True,use=MAGIE,description="Applique 3 effets Poison d'Estialba à la cible, mais vous en donne un également")
suppr = skill("Suppression","vh",TYPE_DAMAGE,650,100,emoji='<:suppression:889090900326744085>',cooldown=5,use=MAGIE,damageOnArmor=3,sussess=70)
revitalisation = skill("Mot revitalisant","vg",TYPE_HEAL,300,45,area=AREA_CIRCLE_1,emoji="<:revita:902525429183811655>",cooldown=2)
onde = skill("Onde","vf",TYPE_ARMOR,500,effect="nv",cooldown=4,area=AREA_CIRCLE_1,emoji='<:onde:902526595842072616>')
eting = skill("Marque Eting","ve",TYPE_INDIRECT_HEAL,350,effect="nw",emoji='<:eting:902525771074109462>')
renforce = skill("Renforcement","vd",TYPE_BOOST,500,range=AREA_DONUT_5,effect="nx",cooldown=5,description="Une compétence qui augmente la résistance d'un allié. L'effet diminue avec les tours qui passent",use=INTELLIGENCE)
steroide = skill("Stéroïdes","vc",TYPE_BOOST,500,range=AREA_DONUT_5,effect="oa",cooldown=3,area=AREA_CIRCLE_1,use=INTELLIGENCE)
renisurection = skill("Résurrection","vb",TYPE_RESURECTION,500,100,emoji='<:respls:906314646007468062>',cooldown=4,shareCooldown=True,description="Permet de ressuciter un allié (en théorie, vous vous doutez bien que c'est compliqué à tester)",use=CHARISMA)
demolish = skill("Démolition","va",TYPE_DAMAGE,650,150,AREA_CIRCLE_2,ultimate=True,cooldown=4,effect=incur[5],damageOnArmor=3,emoji='<:destruc:905051623108280330>')
contrainte = skill("Contrainte","uz",TYPE_MALUS,500,range=AREA_CIRCLE_6,effect=[incur[3],"oc"],cooldown=4,use=INTELLIGENCE)
trouble = skill("Trouble","uy",TYPE_MALUS,500,range=AREA_CIRCLE_6,effect=[incur[3],"od"],use=CHARISMA,emoji='<:trouble:904164471109468200>')
epidemic = skill("Infirmitée","ux",TYPE_MALUS,500,area=AREA_CIRCLE_5,effect=incur[2],cooldown=4,use=None,emoji='<:infirm:904164428545683457>')
croissance = skill("Croissance","uw",TYPE_BOOST,500,effect="oe",cooldown=5,description="Une compétence dont les bonus se renforce avec les tours qui passent",use=CHARISMA,range=AREA_DONUT_5,emoji='<:croissance:904164385952505886>')
destruction = skill("Météore","uu",TYPE_DAMAGE,1000,power=int(explosion.power * 1.33),ultimate=True,cooldown=7,effectOnSelf="mb",use=MAGIE,emoji='<:meteor:904164411990749194>',damageOnArmor=explosion.onArmor)
castDest = effect("Cast - Météore","nnnn",turnInit=2,silent=True,emoji=dangerEm,replique=destruction)
destruction2 = skill("Météore","uv",TYPE_DAMAGE,1000,power=0,ultimate=True,cooldown=7,effectOnSelf=castDest,use=MAGIE,emoji=destruction.emoji,message="Une ombre plane au dessus de {2}...")
infectFiole = skill("Fiole d'infection","ut",TYPE_INDIRECT_DAMAGE,350,0,effect=["oh","oi"],cooldown=3,use=INTELLIGENCE,message="{0} lance une {1} sur {2}",emoji='<:fioleInfect:904164736407597087>')
bigLaser = skill("Lasers chromanergiques - Configuration Ligne","us",TYPE_DAMAGE,0,int(transLine.power*1.1),emoji='<:uLaserLine:906027231128715344>',area=AREA_LINE_6,sussess=95,damageOnArmor=1.33,ultimate=True,cooldown=5,description="Après un tour de chargement, déployez des drones énergétiques qui tirent un puissant rayon coloré en ligne droite")
bigLaserRep = effect("Cast - {0}".format(bigLaser.name),"bigLaserEff",turnInit=2,silent=True,emoji=dangerEm,replique=bigLaser)
bigLaser2 = skill(bigLaser.name,"ur",bigLaser.type,750,0,area=bigLaser.area,emoji=bigLaser.emoji,effectOnSelf=bigLaserRep,ultimate=bigLaser.ultimate,cooldown=bigLaser.cooldown,message="{0} charge ses drones")
bigMonoLaser = skill("Lasers chromanergiques - Configuration Mono","uq",TYPE_DAMAGE,0,int(transMelee.power*1.1),emoji='<:uLaserMono:906027216989716480>',area=AREA_MONO,sussess=100,damageOnArmor=1.33,ultimate=True,cooldown=5,description="Après un tour de chargement, déployez des drones énergétiques qui tirent un puissant rayon coloré sur un adversaire depuis le ciel")
bigMonoLaserRep = effect("Cast - {0}".format(bigMonoLaser.name),"bigMonoLaserEff",turnInit=2,silent=True,emoji=dangerEm,replique=bigMonoLaser)
bigMonoLaser2 = skill(bigMonoLaser.name,"up",bigMonoLaser.type,750,0,area=bigMonoLaser.area,emoji=bigMonoLaser.emoji,effectOnSelf=bigMonoLaserRep,ultimate=bigMonoLaser.ultimate,cooldown=bigMonoLaser.cooldown,message="Les drones de {0} s'envolent")
invocBat2 = skill("Invocation - Chauve-souris II","uo",TYPE_INVOC,500,invocation="Chauve-Souris II",emoji="<:cuttybat2:904369379762925608>",shareCooldown=True,use=CHARISMA,cooldown=3)
invocCarbunR = skill("Invocation - Carbuncle Rubis","un",TYPE_INVOC,500,invocation="Carbuncle Rubis",emoji="<:carbunR:904367955507314731>",shareCooldown=True,use=MAGIE,cooldown=5)
concen = skill("Concentration","um",TYPE_BOOST,price=350,effect="oj",range=AREA_MONO,area=AREA_DONUT_2,cooldown=4,use=None)
memAliceStun = effect("Etourdi","aliceStuned",emoji=uniqueEmoji('<:stun:882597448898474024>'),turnInit=2,stun=True,description="L'utilisation d'un gros sort magique vous a vidé de votre énergie")
memAlice = skill("Memento - Voie de l'Ange","memAlice",TYPE_HEAL,1000,int(transHeal.power*1.1),AREA_MONO,shareCooldown=True,area=AREA_DONUT_4,cooldown=8,ultimate=True,use=CHARISMA,emoji='<a:memAlice2:908424319900745768>',effectOnSelf=memAliceStun)
memAliceCast = effect("Cast - {0}".format(memAlice.name),"aliceMementoCast",replique=memAlice,turnInit=2,silent=True,emoji=uniqueEmoji('<a:memAliceCast:908413832194588723>'))
memAlice2 = copy.deepcopy(memAlice)
memAlice2.id, memAlice2.power, memAlice2.effectOnSelf, memAlice2.message, memAlice2.emoji = "ul",0,memAliceCast,"{0} rassemble ses souvenirs...",'<a:memAliceCast:908413832194588723>'
blackHole = skill("Trou noir","uk",TYPE_PASSIVE,ironWillSkill.price,effectOnSelf="ol",use=None,emoji='<:blackHole:906195944406679612>')
blackHole2 = skill("Trou noir II","uj",TYPE_BOOST,0,use=None,effect=[intargetable,"on"],effectOnSelf="om",emoji='<:blackHole2:906195979332640828>',cooldown=7,initCooldown=2,description="Augmente sensiblement les chances d'être pris pour cible par l'adversaire, tout en rendant vos alliés aux corps à corps **Inciblable** et en redirigeant une partie de leurs dégâts sur vous",area=AREA_DONUT_1,range=AREA_MONO)
fireCircle = skill("Cercle de feu","ui",TYPE_DAMAGE,350,50,AREA_DIST_5,["exclusive","element",ELEMENT_FIRE],effect='oo',area=AREA_DONUT_1,cooldown=3,use=MAGIE,emoji='<:fireCircle:906219518760747159>')
waterCircle = skill("Cercle d'eau","uh",TYPE_DAMAGE,350,35,AREA_DIST_5,["exclusive","element",ELEMENT_WATER],effect='op',area=AREA_DONUT_1,cooldown=3,use=MAGIE,emoji='<:waterCircle:906219492135276594>')
airCircle = skill("Cercle d'air","ug",TYPE_DAMAGE,350,50,AREA_CIRCLE_2,["exclusive","element",ELEMENT_AIR],effect='oq',area=AREA_DONUT_1,cooldown=3,use=MAGIE,emoji='<:airCircle:906219469200842752>')
earthCircle = skill("Cercle de terre","uf",TYPE_DAMAGE,350,35,AREA_DIST_5,["exclusive","element",ELEMENT_EARTH],effect='or',area=AREA_DONUT_1,cooldown=3,use=MAGIE,emoji='<:earthCircle:906219450129317908>')
fireShot = skill("Tir Feu","ue",TYPE_DAMAGE,350,45,area=AREA_CONE_2,cooldown=3,conditionType=["exclusive","element",ELEMENT_FIRE],range=AREA_DIST_5,emoji='<:fireShot:906219594639876116>')
waterShot = skill("Tir Eau","ud",TYPE_DAMAGE,350,60,cooldown=3,conditionType=["exclusive","element",ELEMENT_WATER],range=AREA_DIST_5,emoji='<:waterShot:906219607856119868>')
airStrike = skill("Frappe Air","uc",TYPE_DAMAGE,350,45,area=AREA_CONE_2,cooldown=3,conditionType=["exclusive","element",ELEMENT_AIR],range=AREA_CIRCLE_2,emoji='<:airStrike:906219547873386526>')
earthStrike = skill("Frappe Terre","ub",TYPE_DAMAGE,350,60,cooldown=3,conditionType=["exclusive","element",ELEMENT_EARTH],range=AREA_CIRCLE_2,emoji='<:earthStrike:906219563832709142>')
space1 = skill("Naine Blanche","ua",TYPE_DAMAGE,100,40,use=MAGIE,conditionType=["exclusive","element",ELEMENT_SPACE],area=AREA_CIRCLE_1,emoji='<:ast1:907470821679824896>')
space2 = skill("Constelation","tz",TYPE_DAMAGE,250,60,use=MAGIE,conditionType=["exclusive","element",ELEMENT_SPACE],area=AREA_CIRCLE_1,cooldown=3,emoji='<:ast2:907470855402033153>')
space3 = skill("Nébuluse","ty",TYPE_DAMAGE,500,80,use=MAGIE,conditionType=["exclusive","element",ELEMENT_SPACE],area=AREA_CIRCLE_1,cooldown=5,emoji='<:ast3:907470880676917309>')
time1 = skill("Seconde","tx",TYPE_DAMAGE,100,50,use=MAGIE,conditionType=["exclusive","element",ELEMENT_TIME],emoji='<:time1:907474383034023977>')
time2 = skill("Minute","tw",TYPE_DAMAGE,250,75,use=MAGIE,conditionType=["exclusive","element",ELEMENT_TIME],cooldown=3,emoji='<:time2:907474439854235668>')
time3 = skill("Heure","tv",TYPE_DAMAGE,500,100,use=MAGIE,conditionType=["exclusive","element",ELEMENT_TIME],cooldown=5,emoji='<:time3:907474471240216658>')
timeSp = skill("Rembobinage","tu",TYPE_HEAL,500,70,use=CHARISMA,range=AREA_MONO,area=AREA_DONUT_3,conditionType=["exclusive","element",ELEMENT_TIME],cooldown=7,ultimate=True,emoji='<:rollback:907687694476378112>')
spaceSp = skill("Pluie d'étoiles","tt",TYPE_DAMAGE,500,100,use=MAGIE,conditionType=["exclusive","element",ELEMENT_SPACE],cooldown=5,area=AREA_CIRCLE_2,ultimate=True,emoji='<:starFall:907687023140302908>')
idoOH = skill("Apothéose","ts",TYPE_PASSIVE,500,effectOnSelf="idoOHEff",emoji='<:IdoOH:909278546172719184>',conditionType=["exclusive","aspiration",IDOLE],use=None)
proOH = skill("Protection Avancée","tr",TYPE_PASSIVE,500,effectOnSelf="proOHEff",emoji='<:proOH:909278525528350720>',conditionType=["exclusive","aspiration",PROTECTEUR],use=None)
altOH = skill("Soins Avancées","tq",TYPE_PASSIVE,500,effectOnSelf="altOHEff",emoji='<:altOH:909278509145395220>',conditionType=["exclusive","aspiration",ALTRUISTE],use=None)
lightAura2 = skill("Aura de Lumière II","tp",TYPE_PASSIVE,500,effectOnSelf="lightaura2Pa",emoji=lightAura.emoji,use=CHARISMA)

tripleMissilesLaunch = skill("Missiles téléguidés","tripleMissiles",TYPE_DAMAGE,750,120,ultimate=True,repetition=3,damageOnArmor=1.5,cooldown=7,emoji='<:missiles:909727253414445057>')
tripleMissilesEff2 = effect("Cast - {0}".format(tripleMissilesLaunch),"tripleMissilesEff2",turnInit=2,silent=True,emoji=sameSpeciesEmoji("<a:missileSoonB:909727376273965097>","<a:missilesSoonR:909727492510740501>"),replique=tripleMissilesLaunch)
tripleMissilesCast2 = copy.deepcopy(tripleMissilesLaunch)
tripleMissilesCast2.power, tripleMissilesCast2.message, tripleMissilesCast2.effectOnSelf, tripleMissilesCast2.id = 0,"{0} lance ses missiles",tripleMissilesEff2,"tripleMissilesCast"
tripleMissilesEff = effect("Cast - {0}".format(tripleMissilesLaunch),"tripleMissilesEff",turnInit=2,silent=True,emoji=uniqueEmoji('<:missilesCast:909727680264560690>'),replique=tripleMissilesCast2)
tripleMissiles = copy.deepcopy(tripleMissilesCast2)
tripleMissiles.effectOnSelf,tripleMissiles.message,tripleMissiles.say,tripleMissiles.id = tripleMissilesEff,"{0} calibre ses missiles","Ok, les missiles sont prêts pour le lancement !","to"

lightHeal2 = skill("Illumination","tn",TYPE_HEAL,350,55,cooldown=3,use=CHARISMA,conditionType=["exclusive","element",ELEMENT_LIGHT],emoji='<:illu:909134286203006997>')
extraEtingSkill = copy.deepcopy(eting)
extraEtingSkill.name, extraEtingSkill.id, extraEtingSkill.effect, extraEtingSkill.condition, extraEtingSkill.emoji = "Marque Eting +","tm",["eting+"],[0,2,ELEMENT_TIME],'<:emeB:909132040392302703>'

willShield = effect("Force de volonté","willShield",STRENGTH,overhealth=40,description="Votre force de volonté vous permet de vous protéger de quelques dégâts")
strengthOfWill = skill("Détermination inflexible","tl",TYPE_DAMAGE,0,power=60,cooldown=5,effectOnSelf=willShield)

sixtineUlt = skill("Douce nuit","tk",TYPE_MALUS,0,range=AREA_MONO,area=AREA_ALL_ENNEMIES,use=INTELLIGENCE,effect='sixtineUltEff',ultimate=True,cooldown=5)
hinaUlt = skill("Déluge de plume","tj",TYPE_DAMAGE,0,35,area=AREA_CONE_2,repetition=5,cooldown=7,emoji='<:featherStorm:909932475457884191>')

julieUlt = skill("Prolongation","ti",TYPE_UNIQUE,0,area=AREA_DONUT_2,range=AREA_MONO,cooldown=7,description="Augmente la durée de tous les effets des alliés alentours (bonus comme malus) de 1")