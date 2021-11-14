from classes import *
from constantes import *
from advObjects.advSkills import *

armor = effect("Armure d'Encre","la",INTELLIGENCE,overhealth=70,emoji=sameSpeciesEmoji('<:armor1:866828463751036929>','<:armor2:866828487038205962>'),description="Donne de l'armure à tous les alliés",trigger=TRIGGER_DAMAGE)
coffee = effect("Caféiné","lb",2,strength=10,endurance=10,reject=["mc"],description="Boost la force et l'endurance de tous les alliés",emoji=uniqueEmoji("<:coffee:867538582846963753>"))
the = effect("Théiné","lc",2,intelligence=10,magie=10,reject=["mc"],description="Boost l'agilité et la précision de tous les alliés",emoji=uniqueEmoji('<:the:867538602644602931>'))
encrifugeEff = effect("Tenue encrifugée - Armure","ld",overhealth=1,turnInit=2,trigger=TRIGGER_DAMAGE)
gpEffect = effect("Potion tonifiante","le",5,5,5,5,5,5,0,5,5,5,turnInit=2,description="Vos connaissances en alchimie vous permettent de booster toutes vos statistiques pour le prochain tour")
bpEffect = effect("Potion étrange","lf",5,-5,-5,-5,-5,-5,-5,-5,-5,-5,turnInit=1,description="Vos connaissances en alchimie vous permettent de baisser toutes les statistiques d'un adversaire pendant un tour",emoji = emojiMalus)
deterEff1 = effect("Détermination","lg",emoji=uniqueEmoji('<:determination:867894180851482644>'),turnInit=-1,description="Sur le points de mourir, votre volonté vous permet de tenir jusqu'à votre prochain tour",trigger=TRIGGER_DEATH,callOnTrigger="lh",power=1,type=TYPE_INDIRECT_REZ)
undying = effect("Undying","lh",reject=["li","lj"],turnInit=2,trigger=TRIGGER_END_OF_TURN,onTrigger=[0,9999,DAMAGE_FIXE],immunity=True,description="Vos dernières forces pour rendent insensible à toutes attaques.\nMais à la fin de votre tour, vous mourrerez, pour de bon.",callOnTrigger="li",type=TYPE_INDIRECT_DAMAGE,power=9999,ignoreImmunity=True)
onceButNotTwice = effect("Une fois mais pas deux","li",emoji=uniqueEmoji('<:notTwice:867536068110057483>'),description="La mort ne vous laissera pas filer une seconde fois",turnInit=-1,silent=True)
zelianR = effect("Chronoshift","lj",PURCENTAGE,trigger=TRIGGER_DEATH,description = "Si le porteur venait à mourir tant qu'il porte cet effet, il est réssucité avec la moitié de sa vie",emoji=[['<:chronoshift1:867877564864790538>','<:chronoshift2:867877584518905906>'],['<:chronoshift1:867877564864790538>','<:chronoshift2:867877584518905906>']],reject=["lh","li"],type=TYPE_INDIRECT_REZ,power=50)
courageE = effect("Motivé","lk",2,15,emoji=sameSpeciesEmoji('<:charge1:866832660739653632>','<:charge2:866832677512282154>'))
nostalgiaE = effect("Nostalgie","lm",5,-10,resistance=-10,emoji=emojiMalus)
afterShockDmg = effect("Contre coup","ln",MAGIE,turnInit=1,power=25,aggro=10,lvl=3,trigger=TRIGGER_DAMAGE,type=TYPE_INDIRECT_DAMAGE,emoji=sameSpeciesEmoji('<:aftershock1:882889524122898452>','<:aftershock2:882889538886852650>'))
octoshield = effect("Bouclier Octarien","lo",agility=-100,overhealth=200,turnInit=-1,trigger=TRIGGER_DAMAGE,type=TYPE_ARMOR)
inkBrellaEff = effect("Toile du para-encre","lp",None,-10,agility=-10,overhealth=100,turnInit=-1,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,emoji=uniqueEmoji('<:splatbrellareverse:876079630749147196>'),description="Commencez le combat avec un peu d'armure !\nCependant, vous subirez un malus d'agilité et de force tant que celle-ci est active")
stopAttacking = effect("Stop attacking or draw 25","lq",None,trigger=TRIGGER_DEALS_DAMAGE,type=TYPE_INDIRECT_DAMAGE,power=25,emoji=emojiMalus,description="Vous jouez votre jocker !\nSi le porteur de l'état attaque, il subit 25 dégâts fixe")
poidPlumeEff = effect("Poids Plume","lr",None,trigger=TRIGGER_END_OF_TURN,silent=True,lvl=0,type=TYPE_UNIQUE,unclearable=True,turnInit=-1,emoji=uniqueEmoji(aspiEmoji[POIDS_PLUME]))
hunter = effect("Chasseur","ls",None,emoji=uniqueEmoji('<:chasseur:871097673334276096>'),trigger=TRIGGER_DEATH,type=TYPE_UNIQUE,description="Un chasseur sachant chasser sans son chien a toujours une dernière carte à jouer",turnInit=-1)
hunterBuff = effect("Hunterbuff","lt",None,critical=100,precision=500,silent=True)
menthe = effect("Mentiné","lu",INTELLIGENCE,percing=5,resistance=5,critical=10,reject=["mc"],description="Boost la résistance, la pénétration et le critique de vos alliés",emoji=uniqueEmoji('<:menthe:867538622797054042>'))
badaboum = effect("Ça fait bim bam boum","lv",MAGIE,emoji=emojiMalus,aggro=10,turnInit=2,trigger=TRIGGER_DEATH,power=100,type=TYPE_INDIRECT_DAMAGE,area=AREA_CIRCLE_2)
charme = effect("Sous le charme","lw",CHARISMA,-10,resistance=-10,magie=-10,description="Heu peut-être plus tard la description",type=TYPE_MALUS,emoji=sameSpeciesEmoji("<:CharmeB:908793556435632158>","<:charmeR:908793574437584956>"))
jetlag = effect("Jetlag",'jetLag',None,emoji=uniqueEmoji('<:jetlag:872181671372402759>'),silent=True,description="Le porteur de cet effet est insenssible aux sorts/armes de type \"Sablier\"")
hourglass1 = effect("Rollback","lx",None,trigger=TRIGGER_ON_REMOVE,type=TYPE_UNIQUE,emoji=hourglassEmoji,description="Lorsque l'initiateur de cet effet commence son prochain tour, le porteur récupèrera 75% des PV perdues depuis que cet effet est actif",reject=[jetlag])
lightAuraEffect = effect("Aura de Lumière I","ly",CHARISMA,turnInit=-1,power=10,type=TYPE_INDIRECT_HEAL,trigger=TRIGGER_END_OF_TURN,emoji=sameSpeciesEmoji("<:AdL1:873549174052892672>","<:AdL2:873549232601182249>"),description="Bénissez vos alliés proches et offrez leur des soins sur plusieurs tours",area=AREA_CIRCLE_2,reject=["idoOHEff","proOHEff","altOHEff"])
flumEffect = effect("Douce lueur","lz",None,power=10,turnInit=-1,trigger=TRIGGER_START_OF_TURN,type=TYPE_INDIRECT_HEAL,emoji=uniqueEmoji('<:flum:876079513954557952>'))
dephased = effect("Déphasée","ma",None,emoji=uniqueEmoji('<a:dephasee:882042949494525973>'),description="Ailill n'aime pas affronter trop d'ennemi à la fois, ni ceux qui essaye de l'avoir de loin",type=TYPE_UNIQUE,turnInit=-1)
stuned = effect("Etourdi","mb",emoji=uniqueEmoji('<:stun:882597448898474024>'),turnInit=2,stun=True,description="L'utilisation d'un gros sort magique vous a vidé de votre énergie")
defensive = effect("Orbe défensif","md",emoji=sameSpeciesEmoji('<:orbe1:873725384359837776>','<:orbe2:873725400730202123>'),overhealth=50,description='Donne de l\'armure à un allié',stat=INTELLIGENCE,trigger=TRIGGER_DAMAGE,turnInit=1)
cafeine = effect("Désaltéré","mc",emoji=uniqueEmoji('<:cafeine:883253781024870401>'),turnInit = 4, description = "L'abus de caféine (ou théine c' est la même chose) est dangereureux pout la santé",silent=True)
estal = effect("Poison d'Estialba","me",emoji=uniqueEmoji('<:estialba:884223390804766740>'),turnInit=3,stat=MAGIE,description="Un virulant poison, faisant la sinistre renommée des fées de cette île",trigger=TRIGGER_START_OF_TURN,stackable=True,power=25,type=TYPE_INDIRECT_DAMAGE,lvl=3)
missiles = effect("Ciblé","mf",emoji=uniqueEmoji('<:tentamissile:884757344397951026>'),stat=STRENGTH,description="Au début de son tour, le ciel tombera sur la tête du Ciblé et ses alliés proches !",trigger=TRIGGER_START_OF_TURN,power=25,type=TYPE_INDIRECT_DAMAGE,area=AREA_CIRCLE_1,stackable=True)
octoboum = effect("Explosion à venir !!","mg",emoji=uniqueEmoji('<a:explosion:882627170944573471>'),turnInit=3,aggro=20)
think = effect("REFLECHIS !","mh",CHARISMA,intelligence=10)
iThink = effect("Philosophé","mi",intelligence=15,magie=15,turnInit=3)
blinde = effect("Blindé","mj",resistance=35,description="Réduit les degâts subis de 35% jusqu'à votre prochain tour")
const = effect("Constitution","mk",emoji=uniqueEmoji('<:constitution:888746214999339068>'),description="Augmente de 20 les PV max de base de toute votre équipe",turnInit = -1)
isoled = effect("Isolé","ml",emoji=uniqueEmoji('<:selfProtect:887743151027126302>'),description="S'isoler mentalement pôur ne pas faire attention au dégâts",overhealth=100,stat=INTELLIGENCE,trigger=TRIGGER_DAMAGE)
nouil = effect("Œuil de Linx","mm",emoji=uniqueEmoji('<:noeuil:887743235131322398>'),precision=30,critical=10)
lostSoul = effect("Âme en peine","mn",emoji=uniqueEmoji('<:lostSoul:887853918665707621>'),turnInit=3,trigger=TRIGGER_ON_REMOVE,silent=True,type=TYPE_UNIQUE)
oneforallbuff = effect("Un pour tous - Bonus","mo",resistance=10,stat=CHARISMA,description="Vos capacités défensives sont augmentées au détriment de celle du lanceur de cette compétence",emoji=sameSpeciesEmoji('<:one4allB:905243401157476423>','<:one4allR:905243417846636555>'))
oneforalldebuff = effect("Un pour tous - Malus","mp",resistance=-33,type=TYPE_MALUS,emoji=emojiMalus,description="Vos capacités défenses sont dimunuées pour augmenter celles de vos alliés")
secondSuneff = effect("Insomnie","mq",CHARISMA,agility=-10,precision=-10,type=TYPE_MALUS,emoji=uniqueEmoji('<:MyEyes:784226383018328115>'),description="Vous êtes en train d'expérimenter la joie d'avoir un lampadaire devant une fênetre sans rideau")
onstageeff = effect("Euphorie","mr",CHARISMA,10,10,10,10,10,10,10,5,3,3,description="C'est le moment de tout donner !",emoji=uniqueEmoji('<:alice:893463608716062760>'))
innerdarknessEff = effect("Ténèbres intérieurs","ms",MAGIE,power=65,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN,emoji=uniqueEmoji('<:innerdarkness:902008902776938628>'))
lightspellshield = effect("Bouclier de lumière","mt",INTELLIGENCE,overhealth=10,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,emoji=uniqueEmoji('<:lightspellbook:892963432222036018>'))
lighteff = effect("Illuminé","mu",INTELLIGENCE,overhealth=50,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,emoji=uniqueEmoji('<:illumi1:902008944887746611>'))
lightHealeff = effect("Illuminé","mv",CHARISMA,power=50,type=TYPE_INDIRECT_HEAL,trigger=TRIGGER_START_OF_TURN,emoji=uniqueEmoji('<:illumi2:902008962134712380>'))
darkspellbookeff = effect("Eclair sombre","mw",MAGIE,power=50,area=AREA_CIRCLE_1,trigger=TRIGGER_START_OF_TURN,type=TYPE_INDIRECT_DAMAGE,emoji=uniqueEmoji('<:darkspellbook:892963455773048914>'))
hemoragie = effect("Hémoragie","mx",STRENGTH,power=25,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN,turnInit=3,stackable=True,lvl=3,emoji=uniqueEmoji('<:bleeding:887743186095730708>'))
affaiEffect = effect("Affaiblissement","my",INTELLIGENCE,-10,endurance=-10,resistance=-5,type=TYPE_MALUS,emoji=emojiMalus)
stupid = effect("Provoqué","mz",INTELLIGENCE,charisma=-20,intelligence=-20,type=TYPE_MALUS,emoji=emojiMalus)
castExplo = effect("Cast - Explosion","na",turnInit=2,silent=True,emoji=dangerEm,replique=explosion)
pigmaCast = effect("Cast - Pigmalance","nb",turnInit=2,silent=True,emoji=uniqueEmoji('<:castStingray:899243733835456553>'),replique=stingray2)
derobadeBonus = effect("Dérobade - Bonus","nc",ENDURANCE,resistance=5,aggro=20,description="Un de vos alliés vous a gentiment inviter à prendre les coups à sa place",turnInit=2)
derobadeMalus = effect("Dérobade - Malus","nd",ENDURANCE,aggro=-20,description="Vous avez fuis vos responsabilitées",type=TYPE_MALUS,turnInit=2)
ferociteEff = effect("Férocité","ne",magie=10,aggro=15,resistance=10,turnInit=-1,emoji=uniqueEmoji('<:ferocite:899790356315512852>'),description="Vos grands airs augmentent les chances d'être attaqué par les ennemis",unclearable=True,reject=["nf","ng","nh","ol"])
defiEff = effect("Défi","nf",strength=10,aggro=15,resistance=10,turnInit=-1,emoji=uniqueEmoji('<:defi:899793973873360977>'),description="Vos grands airs augmentent les chances d'être attaqué par les ennemis",unclearable=True,reject=["ne","ng","nh","ol"])
royaleGarde = effect("Garde Royale","ng",intelligence=10,aggro=15,resistance=10,turnInit=-1,emoji=uniqueEmoji('<:gardeRoyale:899793954315321405>'),description="Vos grands airs augmentent les chances d'être attaqué par les ennemis",unclearable=True,reject=["nf","ne","nh","ol"])
ironWill = effect("Volontée de Fer","nh",charisma=10,aggro=15,resistance=10,turnInit=-1,emoji=uniqueEmoji('<:ironwill:899793931762565251>'),description="Vos grands airs augmentent les chances d'être attaqué par les ennemis",unclearable=True,reject=["nf","ng","ne","ol"])
encrifugeEff2 = effect("Tenue Encrifugée","ni",callOnTrigger="ld",emoji=uniqueEmoji('<:encrifuge:871878276061212762> '),trigger=TRIGGER_START_OF_TURN,turnInit=-1,lvl=99,description="Une fois par tour, vous protège de 50 dégâts")
dissimulationEff = effect("Dissimulé","nj",strength=-15,charisma=-15,intelligence=-15,magie=-15,aggro=-10,turnInit=-1,unclearable=True,description="Vous permet de réduire les chances d'être attaqué, mais réduit vos statistiques offensives et supports",emoji=sameSpeciesEmoji("<:dissiB:900130199826497536>","<:dissiR:900130215806779433>"))
convertEff = effect("Convertion","nk",power=50,type=TYPE_BOOST,trigger=TRIGGER_AFTER_DAMAGE,stat=INTELLIGENCE,description="Lorsque le porteur de l'effet inflige des dégâts directs, **{0}**% de ces dégâts lui sont rendue en Armure\nL'Intelligence du lanceur de la compétence influ sur le pourcentage de convertion",emoji=uniqueEmoji('<:convertion:900311843938115614>'))
convertArmor = effect("Convertion - Armure","nl",type=TYPE_ARMOR,turnInit=3,emoji=uniqueEmoji('<:converted:902527031663788032>'),trigger=TRIGGER_DAMAGE)
vampirismeEff = effect("Vampirisme","no",power=66,type=TYPE_HEAL,stat=CHARISMA,trigger=TRIGGER_AFTER_DAMAGE,description="Lorsque le porteur de l'effet inflige des dégâts directs, **{0}**M de ces dégâts lui sont rendue en PV\nLe Charisme du lanceur de la compétence influ sur le pourcentage de convertion",emoji=sameSpeciesEmoji('<:vampireB:900313575913062442>','<:vampireR:900313598130282496>'))
heriteEstialbaEff = effect("Héritage - Estialba","np",turnInit=-1,unclearable=True,description="Grâce aux enseignements de Lohica, vous êtes de plus en plus rodé en terme de poison\n\nLorsque vous donnez l'effet __<:estialba:884223390804766740> Poison d'Estialba__ à un ennemi, lui confère également l'effet __<:estialba2:900329155974008863> Poison d'Estialba II__\n\n__<:estialba2:900329155974008863> Poison d'Estialba II :__ Dégâts indirects, 33% de la puissance de __<:estialba:884223390804766740> Poison d'Estialba__, ne dure qu'un tour",emoji=sameSpeciesEmoji('<:heriteEstialbaB:900318783661559858>','<:heriteEstialbaR:900318753156390962>'),reject=["ns"])
estal2 = effect("Poison d'Estialba II","nq",MAGIE,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN,power=int(estal.power/3),emoji=uniqueEmoji('<:estialba2:900329155974008863>'),stackable=True)
hemoragie2 = effect("Hémoragie II","nr",STRENGTH,power=int(hemoragie.power/3),type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN,stackable=True,emoji=uniqueEmoji('<:bleeding2:900329311955984456>'))
heriteLesathEff = effect("Héritage - Lesath","ns",turnInit=-1,unclearable=True,description="Grâce aux enseignements de Shehisa, vous en connaissez un peu plus sur les points faibles de vos adversaires\n\nLorsque vous donnez l'effet __<:bleeding:887743186095730708> Hémorragie__ à un ennemi, lui confère également l'effet __<:bleeding2:900329311955984456> Hémorragie II__\n\n____<:bleeding2:900329311955984456> Hémorragie II :__ Dégâts indirects, 33% de la puissance de __<:bleeding:887743186095730708> Hémorragie__, ne dure qu'un tour",emoji=sameSpeciesEmoji('<:hetiteLesathB:900322804124229642>','<:heriteLesathR:900322774202089512>'),reject=["np"])
darkFlumEff = effect("Fleur ténèbreuse","nt",turnInit=-1,description="En subissant des dégâts, applique l'effet \"Ténèbres floraux\" sur l'attaquant",emoji=uniqueEmoji('<:darkFlum:901849622685814814>'),callOnTrigger="nu",trigger=TRIGGER_DAMAGE)
darkFlumPoi = effect("Ténèbres floraux","nu",MAGIE,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN,emoji='<:darkFlum:901849622685814814>',power=5,stackable=True,turnInit=2,lvl=1)
ondeEff = effect("Onde","nv",INTELLIGENCE,type=TYPE_ARMOR,overhealth=35,turnInit=5,emoji=uniqueEmoji('<:onde:902526595842072616>'),trigger=TRIGGER_DAMAGE)
etingEff = effect("Marque Eting","nw",CHARISMA,power=20,turnInit=3,stackable=True,trigger=TRIGGER_START_OF_TURN,emoji=uniqueEmoji('<:eting:902525771074109462>'),type=TYPE_INDIRECT_HEAL)
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
infection = effect("Infection","oh",INTELLIGENCE,power=15,trigger=TRIGGER_START_OF_TURN,type=TYPE_INDIRECT_DAMAGE,lvl=2,reject=["oi"],description="Un effet infligeant des dégâts indirects\n\nL'infection se propage sur les ennemis autour du porteur lorsque l'effet se déclanche",emoji=uniqueEmoji("<:infect:904164445268369428>"),turnInit=2)
infectRej = effect("Guérison récente","oi",silent=True,turnInit=3,description="Une guérison récente empêche une nouvelle infection")
ConcenEff = effect("Concentration",'oj',redirection=35,trigger=TRIGGER_DAMAGE,emoji=sameSpeciesEmoji('<:redirectB:905245642643877889>','<:redirectR:905245726253142106>'),turnInit=1,description="Une partie des dégâts directs reçu par le porteur de l'effet sont redirigé vers le combattant qui a donné l'effet")
inkBrella2Eff = copy.deepcopy(inkBrellaEff)
inkBrella2Eff.id, inkBrella2Eff.emoji = "ok",uniqueEmoji("<:inkBrellaAltShield:905283041155514379>")
blackHoleEff = effect("Singularité","ol",aggro=35,turnInit=-1,unclearable=True,reject=["nf","ng","ne","nh"],description="Augmente considérablement les chances d'être pris pour cible par l'adversaire",emoji='<:blackHole:906195944406679612>')
blackHoleEff2 = effect("Singularité II","om",aggro=15,reject=["ol"],description="Les chances d'être la cible des adversaires sont augmentés",emoji='<:blackHole2:906195979332640828>')
blackHoleEff3 = effect("Horizon des événements","on",redirection=50,description="Quelqu'un attire les dégâts sur lui")
fireCircleEff = effect("Foyer","oo",MAGIE,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN,power=35,emoji='<:fireCircle:906219518760747159>')
waterCircleEff = effect("Syphon","op",MAGIE,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN,power=50,emoji='<:waterCircle:906219492135276594>')
airCircleEff = effect("Oeuil de la tempête","oq",MAGIE,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN,power=35,emoji='<:airCircle:906219469200842752>')
earthCircleEff = effect("Epicentre","or",MAGIE,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN,power=50,emoji='<:earthCircle:906219450129317908>')
idoOHEff = effect("Apothéose","idoOHEff",emoji=uniqueEmoji('<:IdoOH:909278546172719184>'),turnInit=-1,power=10,description="Vous motivez vos alliés plus que jamais !\n\n**{0}**% de vos sur-soins sont donnés en armure\n\n__<:idoOHArmor:909278702783836170> Overheath - Idole :__\nArmure Légère : Les armures légères n'absorbent pas de dégâts supplémentaires lors de leurs destructions\nEffet Remplaçable : Les effets remplaçables sont remplassés si le même effet avec une meilleure puissance est donné",unclearable=True,reject=["ly"])
proOHEff = effect("Sur-Protection","proOHEff",emoji=uniqueEmoji('<:proOH:909278525528350720>'),turnInit=-1,power=10,description="Vous avez réusi à surpasser vos limites !\n\n**{0}**% de vos sur-soins sont donnés en armure\n\n__<:proOHArmor:909278718575394837> Overheath - Protecteur :__\nArmure Légère : Les armures légères n'absorbent pas de dégâts supplémentaires lors de leurs destructions\nEffet Remplaçable : Les effets remplaçables sont remplassés si le même effet avec une meilleure puissance est donné",unclearable=True,reject=["ly"])
altOHEff = effect("Sur-Soins","altOHEff",emoji=uniqueEmoji('<:altOH:909278509145395220>'),turnInit=-1,power=20,description="Votre dévotion pour vos alliés vous permet de passer à la vitesse supérieur !\n\n**{0}**% de vos sur-soins sont donnés en armure\n\n__<:altOHArmor:909278749143490601> Overheath - Altruiste :__\nArmure Légère : Les armures légères n'absorbent pas de dégâts supplémentaires lors de leurs destructions\nEffet Remplaçable : Les effets remplaçables sont remplassés si le même effet avec une meilleure puissance est donné",unclearable=True,reject=["ly"])

enchant = effect("Enchanté","na",None,turnInit=-1,silent=True,type=TYPE_UNIQUE,unclearable=True,trigger=TRIGGER_DAMAGE,emoji=uniqueEmoji(aspiEmoji[ENCHANTEUR]))
proMalus = effect("Protecteur - Malus","nb",None,strength=-20,magie=-20,type=TYPE_MALUS,silent=True,stackable=True,emoji=uniqueEmoji('<:proMalus:903137298001047573>'))
astralShield = effect("Armure Astrale","astShield",type=TYPE_ARMOR,turnInit=99,emoji=uniqueEmoji('<:astralShield:907467906483367936>'),trigger=TRIGGER_DAMAGE,lightShield=True)
timeShield = effect("Armure Temporelle","timeShield",type=TYPE_ARMOR,turnInit=99,emoji=uniqueEmoji('<:tempoShield:907467936975945758>'),trigger=TRIGGER_DAMAGE,lightShield=True)
idoOHArmor = effect("Overhealth - Idole","idoOHArmor",overhealth=1,type=TYPE_ARMOR,turnInit=3,trigger=TRIGGER_DAMAGE,lightShield=True,emoji='<:idoOHArmor:909278702783836170>')
proOHArmor = effect("Overhealth - Protecteur","proOHArmor",overhealth=1,type=TYPE_ARMOR,turnInit=3,trigger=TRIGGER_DAMAGE,lightShield=True,emoji='<:proOHArmor:909278718575394837>')
altOHArmor = effect("Overhealth - Altruiste","altOHArmor",overhealth=1,type=TYPE_ARMOR,turnInit=3,trigger=TRIGGER_DAMAGE,lightShield=True,emoji='<:altOHArmor:909278749143490601>')

effTB2 = [effect("Tête Brûlée","effTB",None,turnInit=-1,silent=True,type=TYPE_UNIQUE,unclearable=True,emoji=uniqueEmoji(aspiEmoji[TETE_BRULE]))]
effMag2 = [effect("Mage","effMage",None,turnInit=-1,silent=True,type=TYPE_UNIQUE,unclearable=True,emoji=uniqueEmoji(aspiEmoji[MAGE]))]
chaosEff = effect("Boîte à malice","chaosed",STRENGTH,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN,emoji=uniqueEmoji('<:surprise:904916065778274304>'))

chaosProhib = [undying,deterEff1,poidPlumeEff,dephased,cafeine,octoboum,const,lostSoul,onceButNotTwice,zelianR,octoshield]
