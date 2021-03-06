from classes import *
from constantes import *
from advObjects.advSkills import *
from advObjects.advWeapons import purpleSecretEff, critBonusEff

tankStans = ["ne","ng","nh","ol","nf"]
dptStans = ["ns","np","pacteDeSang","pacteD'âme","purpleSecrets",critBonusEff.id]
healStans = ["idoOHEff","proOHEff","altOHEff","ly","idoOSEff","proOSEff","preOSEff","lightaura2Pa"]
vulneEmoji = uniqueEmoji('<:vulne:930080488557793300> ')

armor = effect("Armure d'Encre","la",INTELLIGENCE,overhealth=70,emoji=sameSpeciesEmoji('<:armor1:866828463751036929>','<:armor2:866828487038205962>'),description="Une armure qui protège le porteur des dégâts directs",trigger=TRIGGER_DAMAGE,type=TYPE_ARMOR)
coffee = effect("Caféiné","lb",CHARISMA,strength=10,endurance=10,description="Boost la force et l'endurance de tous les alliés",emoji=uniqueEmoji("<:coffee:867538582846963753>"))
the = effect("Théiné","lc",CHARISMA,intelligence=10,magie=10,description="Boost l'agilité et la précision de tous les alliés",emoji=uniqueEmoji('<:the:867538602644602931>'))
encrifugeEff = effect("Tenue encrifugée - Armure","ld",overhealth=1,turnInit=2,trigger=TRIGGER_DAMAGE,absolutShield=True)
gpEffect = effect("Potion tonifiante","le",5,5,5,5,5,5,0,5,5,5,turnInit=2,description="Vos connaissances en alchimie vous permettent de booster toutes vos statistiques pour le prochain tour")
bpEffect = effect("Potion étrange","lf",5,-5,-5,-5,-5,-5,-5,-5,-5,-5,turnInit=1,description="Vos connaissances en alchimie vous permettent de baisser toutes les statistiques d'un adversaire pendant un tour",emoji = emojiMalus)
deterEff1 = effect("Détermination","lg",emoji=uniqueEmoji('<:determination:867894180851482644>'),turnInit=-1,description="Une fois par combat, en subissant des dégâts mortels, vous permet de transcender la mort et vous soigne de **{0}%** de vos PV max",power=35,type=TYPE_PASSIVE)
onceButNotTwice = effect("Une fois mais pas deux","li",emoji=uniqueEmoji('<:notTwice:867536068110057483>'),description="La mort ne vous laissera pas filer une seconde fois",turnInit=-1,silent=True)
zelianR = effect("Chronoshift","lj",trigger=TRIGGER_ON_REMOVE,description = "À la fin de la durée de cet effet ou si le porteur reçoit des dégâts fatals, soigne ce dernier d'une valeur égale à **{0}%** des soins qu'il a reçut depuis que l'effet est actif",emoji=sameSpeciesEmoji('<:chronoshift1:867877564864790538>','<:chronoshift2:867877584518905906>'),type=TYPE_INDIRECT_HEAL,power=50,turnInit=3)
courageE = effect("Motivé","lk",CHARISMA,15,emoji=sameSpeciesEmoji('<:charge1:866832660739653632>','<:charge2:866832677512282154>'),description="Augmente la force pendant un tour")
nostalgiaE = effect("Nostalgie","lm",INTELLIGENCE,turnInit=2,strength=-10,magie=-10,resistance=-5,emoji=emojiMalus,description='Plonge le porteur dans ses souvenirs, le rendant plus vulnérable aux attaques')
afterShockDmg = effect("Acharnement","ln",MAGIE,turnInit=1,power=30,aggro=10,lvl=5,trigger=TRIGGER_DAMAGE,type=TYPE_INDIRECT_DAMAGE,emoji=sameSpeciesEmoji('<:aftershock1:882889524122898452>','<:aftershock2:882889538886852650>'),description="Lorsque la porteur reçoit des dégâts, le lanceur de la compétence lui inflige des dégâts indirects supplémentaire")
octoshield = effect("Bouclier Octarien","lo",agility=-100,overhealth=200,turnInit=-1,trigger=TRIGGER_DAMAGE,type=TYPE_ARMOR,absolutShield=True)
inkBrellaEff = effect("Toile du para-encre","lp",None,-10,agility=-10,overhealth=100,turnInit=-1,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,emoji=uniqueEmoji('<:splatbrellareverse:876079630749147196>'),description="Commencez le combat avec un peu d'armure !\nCependant, vous subirez un malus d'agilité et de force tant que celle-ci est active")
stopAttacking = effect("Stop attacking or draw 25","lq",INTELLIGENCE,trigger=TRIGGER_DEALS_DAMAGE,type=TYPE_INDIRECT_DAMAGE,power=25,emoji=emojiMalus,description="Inflige des dégâts indirects au porteur si celui-ci attaque durant son tour")
hunter = effect("Chasseur","ls",None,emoji=uniqueEmoji('<:chasseur:871097673334276096>'),trigger=TRIGGER_DEATH,type=TYPE_UNIQUE,description="Un chasseur sachant chasser sans son chien a toujours une dernière carte à jouer",turnInit=-1)
hunterBuff = effect("Hunterbuff","lt",None,critical=100,precision=500,silent=True)
menthe = effect("Mentiné","lu",CHARISMA,percing=5,resistance=5,critical=10,description="Boost la résistance, la pénétration et le critique de vos alliés",emoji=uniqueEmoji('<:menthe:867538622797054042>'))
badaboum = effect("Ça fait bim bam boum","lv",MAGIE,aggro=10,turnInit=2,trigger=TRIGGER_DEATH,power=int(100*(1+AOEDAMAGEREDUCTION)),type=TYPE_INDIRECT_DAMAGE,area=AREA_CIRCLE_2,emoji=sameSpeciesEmoji("<:deathBoomB:915050502369214474>","<:deathBoomR:915050526436102155>"),description="Lorsque le porteur meurt, cela délanche une explosion infligeant des dégâts à ses alliés alentours")
charme = effect("Sous le charme","lw",CHARISMA,strength=-10,resistance=-5,magie=-10,description="Le porteur est distrait, ce qui diminue ses capacitées offensives et défensives",type=TYPE_MALUS,emoji=sameSpeciesEmoji("<:CharmeB:908793556435632158>","<:charmeR:908793574437584956>"),turnInit=2)
jetlag = effect("Jetlag",'jetLag',None,emoji=uniqueEmoji('<:jetlag:872181671372402759>'),silent=True,description="Le porteur de cet effet est insenssible aux sorts/armes de type \"Sablier\"")
lightAuraEffect = effect("Aura de Lumière I","ly",CHARISMA,turnInit=-1,power=15,type=TYPE_INDIRECT_HEAL,trigger=TRIGGER_END_OF_TURN,emoji=sameSpeciesEmoji("<:AdL1:873549174052892672>","<:AdL2:873549232601182249>"),description="À la fin du tour du porteur, lui et ses alliés proches reçoivent des soins",area=AREA_CIRCLE_2,reject=healStans)
flumEffect = effect("Douce lueur","lz",CHARISMA,power=10,turnInit=-1,trigger=TRIGGER_START_OF_TURN,type=TYPE_INDIRECT_HEAL,emoji=uniqueEmoji('<:flum:876079513954557952>'),description="Soigne le porteur au début de son tour")
dephased = effect("Déphasée","ma",None,emoji=uniqueEmoji('<a:dephasee:882042949494525973>'),description="Ailill n'aime pas affronter trop d'ennemi à la fois, ni ceux qui essaye de l'avoir de loin",type=TYPE_UNIQUE,turnInit=-1)

defensive = effect("Orbe défensif","md",emoji=sameSpeciesEmoji('<:orbe1:873725384359837776>','<:orbe2:873725400730202123>'),resistance=5,overhealth=55,description='Donne de l\'armure à un allié',stat=INTELLIGENCE,trigger=TRIGGER_DAMAGE,turnInit=1,type=TYPE_ARMOR)
estal = effect("Poison d'Estialba","me",emoji=uniqueEmoji('<:est:884223390804766740>'),turnInit=3,stat=MAGIE,description="Un virulant poison, faisant la sinistre renommée des fées de cette île",trigger=TRIGGER_START_OF_TURN,stackable=True,power=25,type=TYPE_INDIRECT_DAMAGE,lvl=3)
missiles = effect("Ciblé","mf",emoji=uniqueEmoji('<:tentamissile:884757344397951026>'),stat=STRENGTH,description="Au début de son tour, le ciel tombera sur la tête du Ciblé et ses alliés proches !",trigger=TRIGGER_START_OF_TURN,power=25,type=TYPE_INDIRECT_DAMAGE,area=AREA_CIRCLE_1,stackable=True)
octoboum = effect("Explosion à venir !!","mg",emoji=uniqueEmoji('<a:explosion:882627170944573471>'),turnInit=3,aggro=20)
think = effect("REFLECHIS !","mh",CHARISMA,intelligence=15,magie=15,turnInit=3)
iThink = effect("Philosophé","mi",INTELLIGENCE,intelligence=15,magie=15,turnInit=3)
blinde = effect("Blindé","mj",ENDURANCE,resistance=7,description="Réduit les degâts subis en fonction de l'Endurance du lanceur")
const = effect("Constitution","mk",emoji=uniqueEmoji('<:constitution:888746214999339068>'),description="Augmente de 5% les PV max de toute votre équipe",turnInit = -1)
isoled = effect("Isolé","ml",emoji=uniqueEmoji('<:selfProtect:887743151027126302>'),description="S'isoler mentalement pôur ne pas faire attention au dégâts",overhealth=120,stat=INTELLIGENCE,trigger=TRIGGER_DAMAGE,type=TYPE_ARMOR)
nouil = effect("Œuil de Linx","mm",PRECISION,emoji=uniqueEmoji('<:noeuil:887743235131322398>'),precision=10,block=10,critical=3,turnInit=2)
lostSoul = effect("Âme en peine","mn",emoji=uniqueEmoji('<:lostSoul:887853918665707621>'),turnInit=3,trigger=TRIGGER_ON_REMOVE,type=TYPE_UNIQUE)
oneforallbuff = effect("Un pour tous - Bonus","mo",resistance=10,stat=CHARISMA,description="Vos capacités défensives sont augmentées au détriment de celle du lanceur de cette compétence",emoji=sameSpeciesEmoji('<:one4allB:905243401157476423>','<:one4allR:905243417846636555>'))
oneforalldebuff = effect("Un pour tous - Malus","mp",resistance=-33,type=TYPE_MALUS,emoji=emojiMalus,description="Vos capacités défenses sont dimunuées pour augmenter celles de vos alliés")
secondSuneff = effect("Insomnie","mq",CHARISMA,agility=-10,precision=-10,type=TYPE_MALUS,emoji=uniqueEmoji('<:MyEyes:784226383018328115>'),reject=["sixtineUltEff"],description="Vous êtes en train d'expérimenter la joie d'avoir un lampadaire devant une fênetre sans rideau")
innerdarknessEff = effect("Ténèbres intérieurs","ms",MAGIE,power=70,stackable=True,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN,emoji=uniqueEmoji('<:innerdarkness:902008902776938628>'),turnInit=2,lvl=2,area=AREA_CIRCLE_1,description="Au début de tour, les Ténèbres de l'âme du porteur provoquent une explosion en croix, le blessant lui et ses alliés proches")
lightspellshield = effect("Bouclier de lumière","mt",INTELLIGENCE,overhealth=35,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,emoji=uniqueEmoji('<:lightspellbook:892963432222036018>'))
lighteff = effect("Illuminé","mu",INTELLIGENCE,overhealth=75,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,emoji=uniqueEmoji('<:illumi1:902008944887746611>'))
lightHealeff = effect("Illuminé","mv",CHARISMA,power=50,type=TYPE_INDIRECT_HEAL,trigger=TRIGGER_START_OF_TURN,emoji=uniqueEmoji('<:illumi2:902008962134712380>'))
darkspellbookeff = effect("Eclair sombre","mw",MAGIE,power=50,area=AREA_CIRCLE_1,stackable=True,trigger=TRIGGER_START_OF_TURN,type=TYPE_INDIRECT_DAMAGE,emoji=uniqueEmoji('<:darkspellbook:892963455773048914>'),turnInit=2,lvl=2)
bleeding = effect("Hémorragie","mx",STRENGTH,power=35,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN,turnInit=3,stackable=True,lvl=3,emoji=uniqueEmoji('<:ble:887743186095730708>'))
affaiEffect = effect("Affaiblissement","my",INTELLIGENCE,strength=-10,endurance=-10,resistance=-5,type=TYPE_MALUS,emoji=emojiMalus)
stupid = effect("Provoqué","mz",INTELLIGENCE,charisma=-20,intelligence=-20,type=TYPE_MALUS,emoji=emojiMalus)
castExplo = effect("Cast - Explosion","na",turnInit=2,silent=True,emoji=sameSpeciesEmoji('<a:boomCastB:916382499704275005>','<a:boomCastR:916382515135144008>'),replique=explosion)
pigmaCast = effect("Guide - Pigmalance","nb",turnInit=2,silent=True,emoji=uniqueEmoji('<:castStingray:899243733835456553>'),replique=stingray2)
derobadeBonus = effect("Dérobade - Bonus","nc",ENDURANCE,resistance=5,aggro=20,description="Un de vos alliés vous a gentiment inviter à prendre les coups à sa place",turnInit=2)
derobadeMalus = effect("Dérobade - Malus","nd",ENDURANCE,aggro=-20,description="Vous avez fuis vos responsabilitées",type=TYPE_MALUS,turnInit=2)
ferociteEff = effect("Férocité","ne",stat=ENDURANCE,magie=10,aggro=35,turnInit=-1,emoji=uniqueEmoji('<:ferocite:899790356315512852>'),description="Vos grands airs augmentent les chances d'être attaqué par les ennemis",unclearable=True,reject=tankStans)
defiEff = effect("Défi","nf",stat=ENDURANCE,strength=10,aggro=35,turnInit=-1,emoji=uniqueEmoji('<:defi:899793973873360977>'),description="Vos grands airs augmentent les chances d'être attaqué par les ennemis",unclearable=True,reject=tankStans)
royaleGarde = effect("Garde Royale","ng",stat=ENDURANCE,intelligence=10,aggro=35,turnInit=-1,emoji=uniqueEmoji('<:gardeRoyale:899793954315321405>'),description="Vos grands airs augmentent les chances d'être attaqué par les ennemis",unclearable=True,reject=tankStans)
ironWill = effect("Volontée de Fer","nh",stat=ENDURANCE,charisma=10,aggro=35,turnInit=-1,emoji=uniqueEmoji('<:ironwill:899793931762565251>'),description="Vos grands airs augmentent les chances d'être attaqué par les ennemis",unclearable=True,reject=tankStans)
encrifugeEff2 = effect("Tenue Encrifugée","ni",callOnTrigger="ld",emoji=uniqueEmoji('<:encrifuge:871878276061212762> '),trigger=TRIGGER_START_OF_TURN,turnInit=-1,lvl=99,description="Une fois par tour, vous protège de 50 dégâts")
dissimulationEff = effect("Dissimulé","nj",strength=-15,charisma=-15,intelligence=-15,magie=-15,aggro=-10,turnInit=-1,unclearable=True,description="Vous permet de réduire les chances d'être attaqué, mais réduit vos statistiques offensives et supports",emoji=sameSpeciesEmoji("<:dissiB:900130199826497536>","<:dissiR:900130215806779433>"))
convertEff = effect("Convertion","nk",power=50,type=TYPE_BOOST,trigger=TRIGGER_AFTER_DAMAGE,stat=INTELLIGENCE,description="Lorsque le porteur de l'effet inflige des dégâts directs, **{0}**% de ces dégâts lui sont rendue en Armure\nL'Intelligence du lanceur de la compétence influ sur le pourcentage de convertion",emoji=uniqueEmoji('<:convertion:900311843938115614>'))
convertArmor = effect("Convertion - Armure","nl",type=TYPE_ARMOR,turnInit=3,emoji=uniqueEmoji('<:converted:902527031663788032>'),trigger=TRIGGER_DAMAGE)
vampirismeEff = effect("Vampirisme","no",power=25,type=TYPE_INDIRECT_HEAL,stat=CHARISMA,trigger=TRIGGER_AFTER_DAMAGE,description="Accorde au porteur un certain pourcentage de vol de vie, augmenté par les statistiques de l'entité à l'origine de l'effet",emoji=sameSpeciesEmoji('<:vampireB:900313575913062442>','<:vampireR:900313598130282496>'))
heriteEstialbaEff = effect("Héritage - Estialba","np",turnInit=-1,unclearable=True,description="Grâce aux enseignements de Lohica, vous êtes de plus en plus rodé en terme de poison\n\nLorsque vous donnez l'effet __<:est:884223390804766740> Poison d'Estialba__ à un ennemi, lui confère également l'effet __<:estialba2:900329155974008863> Poison d'Estialba II__\n\n__<:estialba2:900329155974008863> Poison d'Estialba II :__ Dégâts indirects, 33% de la puissance de __<:est:884223390804766740> Poison d'Estialba__, ne dure qu'un tour",emoji=sameSpeciesEmoji('<:heriteEstialbaB:900318783661559858>','<:heriteEstialbaR:900318753156390962>'),reject=dptStans)
estal2 = effect("Poison d'Estialba II","nq",MAGIE,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN,power=int(estal.power/3),turnInit=3,emoji=uniqueEmoji('<:estialba2:900329155974008863>'),stackable=True,lvl=3)
bleeding2 = effect("Hémoragie II","nr",STRENGTH,power=int(bleeding.power/3),type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN,turnInit=3,stackable=True,emoji=uniqueEmoji('<:bleeding2:900329311955984456>'),lvl=3)
heriteLesathEff = effect("Héritage - Lesath","ns",turnInit=-1,unclearable=True,description="Grâce aux enseignements de Shehisa, vous en connaissez un peu plus sur les points faibles de vos adversaires\n\nLorsque vous donnez l'effet __<:ble:887743186095730708> Hémorragie__ à un ennemi, lui confère également l'effet __<:bleeding2:900329311955984456> Hémorragie II__\n\n____<:bleeding2:900329311955984456> Hémorragie II :__ Dégâts indirects, 33% de la puissance de __<:ble:887743186095730708> Hémorragie__, ne dure qu'un tour",emoji=sameSpeciesEmoji('<:hetiteLesathB:900322804124229642>','<:heriteLesathR:900322774202089512>'),reject=dptStans)
darkFlumEff = effect("Fleur ténèbreuse","nt",turnInit=-1,description="En subissant des dégâts, applique l'effet \"Ténèbres floraux\" sur l'attaquant",emoji=uniqueEmoji('<:darkFlum:901849622685814814>'),callOnTrigger="nu",trigger=TRIGGER_DAMAGE)
darkFlumPoi = effect("Ténèbres floraux","nu",MAGIE,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN,emoji=sameSpeciesEmoji("<:dfB:922100203169923144>","<:dfR:922100216415518740>"),power=1,stackable=True,turnInit=3,lvl=3,description="Inflige des dégâts avec une puissance équivalante à **20%** du niveau du lanceur au début du tour du porteur")
ondeEff = effect("Onde","nv",INTELLIGENCE,type=TYPE_ARMOR,overhealth=35,turnInit=5,emoji=uniqueEmoji('<:onde:902526595842072616>'),trigger=TRIGGER_DAMAGE,stackable=True)
etingEff = effect("Marque Eting","nw",CHARISMA,power=25,turnInit=3,stackable=True,trigger=TRIGGER_START_OF_TURN,emoji=uniqueEmoji('<:eting:902525771074109462>'),type=TYPE_INDIRECT_HEAL)
renforceEff = effect("Renforcé","nx",INTELLIGENCE,resistance=15,endurance=15,trigger=TRIGGER_ON_REMOVE,callOnTrigger="ny")
renforceEff2 = effect("Renforcé II","ny",INTELLIGENCE,resistance=10,endurance=10,trigger=TRIGGER_ON_REMOVE,callOnTrigger="nz")
renforceEff3 = effect("Renforcé III","nz",INTELLIGENCE,resistance=5,endurance=5)
steroideEff = effect("Stéroïde","oa",INTELLIGENCE,strength=10,magie=10)
gwenCoupeEff = effect("Brûme sacrée","ob",emoji=uniqueEmoji('<:gwenZ:902913176562176020>'),turnInit=-1,unclearable=True,description="Vous confère 15% de chance d'obtenir l'effet **Inciblable** pendant 1 tour lorsque vous commencez votre tour")
contrainteEff = effect("Contrain","oc",INTELLIGENCE,agility=-15,precision=-15,type=TYPE_MALUS)
troubleEff = effect("Troublé","od",CHARISMA,charisma=-15,intelligence=-15,type=TYPE_MALUS)
croissanceEff = effect("Bourgeon","oe",CHARISMA,strength=10,magie=10,resistance=5,trigger=TRIGGER_ON_REMOVE,callOnTrigger="of",emoji=uniqueEmoji('<:crois1:903976740869795910>'))
croissanceEff2 = effect("Jeune pousse","of",CHARISMA,strength=15,magie=15,resistance=10,trigger=TRIGGER_ON_REMOVE,callOnTrigger="og",emoji=uniqueEmoji('<:crois2:903976762726289520>'))
croissanceEff3 = effect("Joli plante","og",CHARISMA,strength=20,magie=20,resistance=15,emoji=uniqueEmoji('<:crois3:903976790530326578>'))
infection = effect("Infection","oh",INTELLIGENCE,power=25,trigger=TRIGGER_START_OF_TURN,type=TYPE_INDIRECT_DAMAGE,lvl=2,reject=["oi"],description="Un effet infligeant des dégâts indirects\n\nL'infection se propage sur les ennemis autour du porteur lorsque l'effet se déclanche",emoji=uniqueEmoji("<:infect:904164445268369428>"),turnInit=2)
infectRej = effect("Guérison récente","oi",silent=True,turnInit=3,description="Une guérison récente empêche une nouvelle infection")
ConcenEff = effect("Concentration",'oj',redirection=35,trigger=TRIGGER_DAMAGE,emoji=sameSpeciesEmoji('<:concenB:921763012023562280>','<:concenR:921763030960832622>'),turnInit=1,description="Une partie des dégâts directs reçu par le porteur de l'effet sont redirigé vers le combattant qui a donné l'effet")
inkBrella2Eff = copy.deepcopy(inkBrellaEff)
inkBrella2Eff.id, inkBrella2Eff.emoji = "ok",uniqueEmoji("<:inkBrellaAltShield:905283041155514379>")
blackHoleEff = effect("Singularité","ol",stat=ENDURANCE,aggro=35,inkResistance=5,turnInit=-1,unclearable=True,reject=tankStans,description="Augmente considérablement les chances d'être pris pour cible par l'adversaire et réduit légèrement les dégâts indirects reçus",emoji='<:blackHole:906195944406679612>')
blackHoleEff3 = effect("Horizon des événements","on",redirection=25,inkResistance=25,description="Quelqu'un attire les dégâts sur lui",turnInit=3,aggro=-15,emoji='<:blackHole2:906195979332640828>')
fireCircleEff = effect("Foyer","oo",MAGIE,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN,power=50,emoji='<:fireCircle:906219518760747159>')
waterCircleEff = effect("Syphon","op",MAGIE,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN,power=70,emoji='<:waterCircle:906219492135276594>')
airCircleEff = effect("Oeuil de la tempête","oq",MAGIE,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN,power=50,emoji='<:airCircle:906219469200842752>')
earthCircleEff = effect("Epicentre","or",MAGIE,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN,power=70,emoji='<:earthCircle:906219450129317908>')
idoOHEff = effect("Apothéose","idoOHEff",emoji=uniqueEmoji('<:IdoOH:909278546172719184>'),turnInit=-1,power=25,description="Vous motivez vos alliés plus que jamais !\n\n**{0}**% de vos sur-soins sont donnés en armure\n\n__<:idoOHArmor:909278702783836170> Overheath - Idole :__\nArmure Légère : Les armures légères n'absorbent pas de dégâts supplémentaires lors de leurs destructions\nEffet Remplaçable : Les effets remplaçables sont remplassés si le même effet avec une meilleure puissance est donné",unclearable=True,reject=healStans)
proOHEff = effect("Protection anticipée","proOHEff",emoji=uniqueEmoji('<:proOH:909278525528350720>'),turnInit=-1,power=25,description="Vous avez réusi à surpasser vos limites !\n\n**{0}**% de vos sur-soins sont donnés en armure\n\n__<:proOHArmor:909278718575394837> Overheath - Protecteur :__\nArmure Légère : Les armures légères n'absorbent pas de dégâts supplémentaires lors de leurs destructions\nEffet Remplaçable : Les effets remplaçables sont remplassés si le même effet avec une meilleure puissance est donné",unclearable=True,reject=healStans)
altOHEff = effect("Bénédiction","altOHEff",emoji=uniqueEmoji('<:altOH:909278509145395220>'),turnInit=-1,power=35,description="Votre dévotion pour vos alliés vous permet de passer à la vitesse supérieur !\n\n**{0}**% de vos sur-soins sont donnés en armure\n\n__<:aoa:909278749143490601>  Overheath - Altruiste :__\nArmure Légère : Les armures légères n'absorbent pas de dégâts supplémentaires lors de leurs destructions\nEffet Remplaçable : Les effets remplaçables sont remplassés si le même effet avec une meilleure puissance est donné",unclearable=True,reject=healStans)
lightAura2ActiveEff = effect("Aura de Lumière II","lightaura2Ac",CHARISMA,trigger=TRIGGER_AFTER_DAMAGE,turnInit=2,stackable=True,type=TYPE_INDIRECT_HEAL,power=10,lvl=4,description="Les 4 prochaines attaques que vous receverez déclancheront un effet de soins autour de vous",area=AREA_CIRCLE_2,emoji=lightAuraEffect.emoji)
lightAura2PassiveEff = effect("Aura de Lumière II","lightaura2Pa",CHARISMA,turnInit=-1,trigger=TRIGGER_START_OF_TURN,type=TYPE_BOOST,unclearable=True,emoji=lightAuraEffect.emoji,callOnTrigger=lightAura2ActiveEff,description="Octroi \"Charge Lumineuse\" à chaques début de tours",reject=healStans)
extraEting = copy.deepcopy(etingEff)
extraEting.name, extraEting.id, extraEting.power, extraEting.emoji = "Marque Eting +","eting+", int(extraEting.power * 1.35), sameSpeciesEmoji('<:emeB:909132040392302703>','<:emeR:909132070251536486>')
sixtineUltEff = effect("Douce nuit","sixtineUltEff",INTELLIGENCE,-10,-10,-10,-10,-10,-10,-10,-3,-3,-3,description="Le monde des rêves vous appelle...",type=TYPE_MALUS,reject=["mq"],emoji=sameSpeciesEmoji('<:snB:911735287351246929>','<:snR:911735275284230145>'))

enchant = effect("Enchanté","enchantBuffEff",None,turnInit=-1,silent=True,type=TYPE_UNIQUE,unclearable=True,trigger=TRIGGER_DAMAGE,emoji=uniqueEmoji(aspiEmoji[ENCHANTEUR]))
proMalus = effect("Protecteur - Malus","nb",HARMONIE,strength=-5,magie=-5,type=TYPE_MALUS,silent=True,emoji=uniqueEmoji('<:proMalus:903137298001047573>'),stackable=False)
astralShield = effect("Armure Astrale","astShield",type=TYPE_ARMOR,turnInit=99,emoji=uniqueEmoji('<:astralShield:907467906483367936>'),trigger=TRIGGER_DAMAGE,lightShield=True)
timeShield = effect("Armure Temporelle","timeShield",type=TYPE_ARMOR,turnInit=99,emoji=uniqueEmoji('<:tempoShield:907467936975945758>'),trigger=TRIGGER_DAMAGE,lightShield=True)
idoOHArmor = effect("Apothéose","idoOHArmor",overhealth=1,type=TYPE_ARMOR,turnInit=3,trigger=TRIGGER_DAMAGE,lightShield=True,emoji='<:idoOHArmor:909278702783836170>')
proOHArmor = effect("Protection anticipée","proOHArmor",overhealth=1,type=TYPE_ARMOR,turnInit=3,trigger=TRIGGER_DAMAGE,lightShield=True,emoji='<:proOHArmor:909278718575394837>')
altOHArmor = effect("Bénifiction","altOHArmor",overhealth=1,type=TYPE_ARMOR,turnInit=3,trigger=TRIGGER_DAMAGE,lightShield=True,emoji='<:aoa:909278749143490601> ')

chaosEff = effect("Boîte à malice","chaosed",STRENGTH,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN,emoji=uniqueEmoji('<:surprise:904916065778274304>'))

idoOSEff = effect("Clou du spectacle","idoOSEff",emoji=uniqueEmoji('<:osIdo:913885207751446544>'),turnInit=-1,power=30,description="Lorsque vous donnez une armure, réduit de **{1}**% les pertes dû au malus d'armure cumulée\nLorsque l'une de vos armures est détruite, celle-ci absorbe des dégâts supplémentaires équivalants à **{0}**% de votre niveau",unclearable=True,reject=healStans)
proOSEff = effect("Seconde Couche","proOSEff",emoji=uniqueEmoji('<:osPro:913885191800512562>'),turnInit=-1,power=30,description="Lorsque vous donnez une armure, réduit de **{1}**% les pertes dû au malus d'armure cumulée\nLorsque l'une de vos armures est détruite, celle-ci absorbe des dégâts supplémentaires équivalants à **{0}**% de votre niveau",unclearable=True,reject=healStans)
preOSEff = effect("Armures avancées","preOSEff",emoji=uniqueEmoji('<:osPre:913885175161712710>'),turnInit=-1,power=50,description="Lorsque vous donnez une armure, réduit de **{1}**% les pertes dû au malus d'armure cumulée\nLorsque l'une de vos armures est détruite, celle-ci absorbe des dégâts supplémentaires équivalants à **{0}**% de votre niveau",unclearable=True,reject=healStans)

GESredirect = effect("The Giant Enemy Spider","TheGiantEnemySpiderRedirect",turnInit=-1,unclearable=True,redirection=100)
physicRuneEff = effect("Sanguis Pact","pacteDeSang",description="Augmente la puissance de vos attaques **Physiques** et **Corporelles** de **{0}%**.\nAprès chaque utilisation d'une arme ou compétence offensive, vous inflige des dégâts non réductibles d'une valeur de **15%** de vos PV maximums",power=35,unclearable=True,reject=dptStans,emoji=uniqueEmoji('<:pacteDeSang:917096147452035102>'),turnInit=-1)
magicRuneEff = effect("Animae Foedus","pacteD'âme",description="Augmente la puissance de vos attaques **Magiques** et **Psychique** de **{0}%**.\nAprès chaque utilisation d'une arme ou compétence offensive, vous inflige des dégâts non réductibles d'une valeur de **15%** de vos PV maximums",power=35,unclearable=True,reject=dptStans,emoji=uniqueEmoji('<:pacteDame:917096164942295101>'),turnInit=-1)
purpleSecretEff.reject = critBonusEff.reject = dptStans

chaosProhib = [deterEff1,dephased,octoboum,const,lostSoul,onceButNotTwice,zelianR,octoshield]

#Effect
effects = [ironHealthEff,preciChiEff,
    critBonusEff,idoOHEff,proOHEff,altOHEff,lightAura2PassiveEff,extraEting,sixtineUltEff,idoOSEff,proOSEff,preOSEff,physicRuneEff,magicRuneEff,purpleSecretEff,fireCircleEff,waterCircleEff,airCircleEff,earthCircleEff,renforceEff,renforceEff2,renforceEff3,steroideEff,gwenCoupeEff,contrainteEff,troubleEff,croissanceEff,croissanceEff2,croissanceEff3,infection,infectRej,ConcenEff,inkBrella2Eff,blackHoleEff,blackHoleEff3,convertEff,vampirismeEff,heriteEstialbaEff,estal2,bleeding2,heriteLesathEff,darkFlumEff,darkFlumPoi,ondeEff,etingEff,encrifugeEff2,ferociteEff,defiEff,royaleGarde,ironWill,dissimulationEff,pigmaCast,derobadeBonus,derobadeMalus,castExplo,affaiEffect,stupid,bleeding,innerdarknessEff,darkspellbookeff,lighteff,lightHealeff,lightspellshield,secondSuneff,oneforallbuff,oneforalldebuff,lostSoul,nouil,isoled,const,blinde,iThink,think,octoboum,missiles,estal,defensive,flumEffect,lightAuraEffect,jetlag,charme,armor,coffee,the,encrifugeEff,gpEffect,bpEffect,deterEff1,onceButNotTwice,zelianR,afterShockDmg,octoshield,nostalgiaE,inkBrellaEff,stopAttacking,hunter,hunterBuff,menthe,badaboum,courageE
]

def findEffect(effectId) -> effect:
    if type(effectId) == effect:
        return effectId
    elif type(effectId) != str:
        
        return None
    else:
        rep,id = None,effectId
        for a in effects:
            if a.id == id or a.name.lower() == id.lower():
                rep = a
                break
    
        return rep
