from classes import *
from constantes import *
from advObjects.advSkills import *

batWeap = weapon("Griffe","aaa",RANGE_MELEE,AREA_CIRCLE_1,56,100,0,emoji='<:griffe:884889931359596664>',use=AGILITY)
carbunTWeap = weapon("Griffe","aaa",RANGE_MELEE,AREA_CIRCLE_1,56,100,0,emoji='<:griffe:884889931359596664>',use=ENDURANCE)
carbunE = weapon("Coup de vent","aab",RANGE_LONG,AREA_CIRCLE_5,40,70,0,emoji='<:vent:884889843681853460>',area=AREA_CIRCLE_1,use=MAGIE)
carbunSkill = skill("Rafale","aac",TYPE_DAMAGE,0,100,area=AREA_CIRCLE_2,sussess=55,emoji='<:rafale:884889889445912577>',use=MAGIE,cooldown=4)
carbunTSKill = skill("Eclat de Topaze","aad",TYPE_DAMAGE,0,100,AREA_MONO,area=AREA_CIRCLE_2,sussess=80,cooldown=4,emoji="<:eclattopaze:884889967397056512>",use=ENDURANCE)
feeWeap = weapon("Embrassement","aae",RANGE_DIST,AREA_CIRCLE_4,30,100,0,type=TYPE_HEAL,use=CHARISMA,emoji="<:feerie:885076995522834442>",target=ALLIES,area=AREA_CIRCLE_1)
feeEffect = effect("Murmure de l'aurore","aaf",CHARISMA,type=TYPE_INDIRECT_HEAL,power=15,emoji=uniqueEmoji('<:feerie:885076995522834442>'),trigger=TRIGGER_START_OF_TURN,turnInit=2,stackable=True)
feeSkill = skill("Murmure de l'aurore","aag",TYPE_INDIRECT_HEAL,0,0,AREA_MONO,cooldown=3,area=AREA_CIRCLE_3,emoji="<:feerie:885076995522834442>",effect=feeEffect)
titWeap = weapon("Magical Bonk","aah",RANGE_MELEE,AREA_CIRCLE_3,20,70,0,0,0,0,0,0,0,0,0,0,0,repetition=3,emoji='<:magicalBonk:886669168408137749>',area=AREA_CONE_2) 
lapinoWeap = weapon("Murmure de guérison","aai",RANGE_DIST,AREA_CIRCLE_3,25,100,0,0,0,0,0,0,0,0,0,0,0,'<:defHeal:885899034563313684>',use=CHARISMA,type=TYPE_HEAL,target=ALLIES,message="{0} encourage doucement {1} :")
lapinoSkill = skill("Murmure de dévoument","aaj",TYPE_HEAL,0,50,emoji='<:defHeal:885899034563313684>',cooldown=4)
batSkill = skill("Cru-aile","aak",TYPE_DAMAGE,0,50,AREA_CIRCLE_2,emoji='<:defDamage:885899060488339456>',use=AGILITY)
autoWeap = weapon("NoneWeap","aal",RANGE_MELEE,AREA_CIRCLE_1,0,0,0,emoji="<:empty:866459463568850954>")
autoEff = effect("Explosé","aam",trigger=TRIGGER_END_OF_TURN,type=TYPE_INDIRECT_DAMAGE,power=9999,emoji=emojiMalus,silent=True)
autoSkill = skill("Explosion","aan",TYPE_DAMAGE,0,75,AREA_MONO,emoji='<:defDamage:885899060488339456>',area=AREA_CIRCLE_1,effectOnSelf=autoEff)
cutyBatSkill1Eff = effect("Motivé Bis","batMotivEff",stat=CHARISMA,strength=10,magie=10,charisma=10,intelligence=10)
cutyBatSkill1 = skill("Motivation de la Chauve-Souris","batMotiv",TYPE_BOOST,0,0,AREA_MONO,area=AREA_DONUT_2,use=CHARISMA,cooldown=4,effect=cutyBatSkill1Eff)
cutyBatSkill2Eff = effect("Renforcement Bis","batRenforceEff",stat=INTELLIGENCE,endurance=10,resistance=10,emoji=uniqueEmoji('<:egide:887743268337619005>'))
cutyBatSkill2 = skill("Renforcement de la Chauve-Souris","batRenforce",TYPE_BOOST,0,0,range=AREA_DONUT_5,cooldown=3,emoji='<:egide:887743268337619005>',effect=cutyBatSkill2Eff)
cutyBatSkill3Eff = effect("Echolocalisé","batEchoEff",CHARISMA,agility=-10,type=TYPE_MALUS)
cutyBatSkill3 = skill("Echolocalisation","batEcho",TYPE_MALUS,0,0,AREA_MONO,area=AREA_DONUT_5,effect=cutyBatSkill3Eff,cooldown=3)
cutyBatWeap = weapon("Onde sonore","batWeap",RANGE_DIST,AREA_CIRCLE_5,32,100,effectOnUse=incur[1],use=CHARISMA)
carbunRWeap = weapon("Griffe enflammé","rubyWeap",RANGE_MELEE,AREA_CIRCLE_1,56,100,use=MAGIE,emoji=batWeap.emoji)
carbunRSkill1 = skill("Pyrotechnie du Carbuncle","rubySkill",TYPE_DAMAGE,0,70,AREA_CIRCLE_2,cooldown=3,use=MAGIE)
curbunRSkill2Eff = effect("Flamme éternelle","fire",MAGIE,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN,power=25,lvl=2,turnInit=2)
carbunRSkill2 = skill("Flammes éternelles","rubySkill2",TYPE_DAMAGE,0,50,AREA_CIRCLE_3,effect=curbunRSkill2Eff,cooldown=3)

batInvoc = invoc("Chauve-Souris",aspiration=TETE_BRULE,strength=[PURCENTAGE,0.5],endurance=[PURCENTAGE,0.3],charisma=[PURCENTAGE,0.5],agility=[PURCENTAGE,0.7],precision=[PURCENTAGE,0.7],intelligence=[PURCENTAGE,0.5],magie=[PURCENTAGE,0.5],resistance=20,percing=0,critical=30,icon=["<:bat1:884519906819862568>","<:bat2:884519927208357968>"],gender=GENDER_FEMALE,weapon=batWeap,description="Une invocation de mêlée peu resistante, mais sans temps de rechargement",skill=[batSkill],element=ELEMENT_AIR)
carbuncleE = invoc("Carbuncle Emeraude",[PURCENTAGE,0.5],[PURCENTAGE,0.5],[PURCENTAGE,0.5],[PURCENTAGE,0.5],[PURCENTAGE,0.5],[PURCENTAGE,0.5],[PURCENTAGE,0.7],20,10,[PURCENTAGE,2],TETE_BRULE,["<:ce1:884889724114841610>","<:ce2:884889693374775357>"],carbunE,[carbunSkill],description="Une invocation utilisant des compétences de zone pour vaincre des groupes d'ennemis de loin",element=ELEMENT_AIR)
carbuncleT = invoc("Carbuncle Topaze",[PURCENTAGE,0.5],[PURCENTAGE,0.7],[PURCENTAGE,0.5],[PURCENTAGE,0.7],[PURCENTAGE,0.7],[PURCENTAGE,0.5],[PURCENTAGE,0.5],[PURCENTAGE,0.1],0,10,PROTECTEUR,["<:ct1:884889748274028666>","<:ct2:884889807111749662>"],carbunTWeap,[carbunTSKill],description="Une invocation résistante qui n'a pas froid au yeux et viendra sauter dans la mêlée",element=ELEMENT_EARTH)
feeInv = invoc("Fée soignante",[PURCENTAGE,0.5],[PURCENTAGE,0.5],[PURCENTAGE,0.7],[PURCENTAGE,0.7],[PURCENTAGE,0.5],[PURCENTAGE,0.5],[PURCENTAGE,0.7],10,0,0,ALTRUISTE,["<:fee1:885076945333805086>","<:fee2:885076961695760386>"],feeWeap,[feeSkill],gender=GENDER_FEMALE,description="Une fée qui soigne ses alliés grace à sa magie curative",element=ELEMENT_LIGHT)
titania = invoc("Titania",[HARMONIE],[HARMONIE],[PURCENTAGE,1],[PURCENTAGE,1],[PURCENTAGE,1],[PURCENTAGE,1],[PURCENTAGE,0.5],25,10,25,OBSERVATEUR,["<:tita1:886663550796431390>","<:tita2:886663565220651028>"],titWeap,[],GENDER_FEMALE,ELEMENT_AIR)
lapino = invoc("Lapino",[PURCENTAGE,0.5],[PURCENTAGE,0.5],[PURCENTAGE,0.7],[PURCENTAGE,0.3],[PURCENTAGE,0.5],[PURCENTAGE,0.5],[PURCENTAGE,0.5],10,0,0,ALTRUISTE,['<:lapino1:885899366966112266>','<:lapino2:885899382539571221>'],lapinoWeap,[lapinoSkill,eting],description="Fidèle Lapino d'Hélène, il la suit partout là où elle aura besoin de lui",element=ELEMENT_LIGHT)
autoBomb = invoc("Bombe Robot",[PURCENTAGE,0.8],50,0,0,0,0,0,20,0,0,INVOCATEUR,["<:auto1:887747795497394267>","<:auto2:887747819866312735>"],autoWeap,[autoSkill])
darkness = invoc("Conviction des Ténèbres",0,-25,0,0,0,0,0,0,0,0,INVOCATEUR,['<:infiniteDarkness:898497770531455008>','<:infiniteDarkness:898497770531455008>'],autoWeap,gender=GENDER_FEMALE,element=ELEMENT_DARKNESS)
cutyBat = invoc("Chauve-Souris II",strength=[PURCENTAGE,0.5],endurance=[PURCENTAGE,0.3],charisma=[PURCENTAGE,0.7],agility=[PURCENTAGE,0.7],precision=[PURCENTAGE,0.5],intelligence=[PURCENTAGE,0.7],magie=[PURCENTAGE,0.5],resistance=[PURCENTAGE,1],percing=0,critical=0,aspiration=IDOLE,icon=['<:bat2B:904368975952085012>','<:bat2R:904368991710101515>'],weapon=cutyBatWeap,skill=[cutyBatSkill1,cutyBatSkill2,cutyBatSkill3],gender=GENDER_FEMALE,description="Une chauve-souris spécialisée dans le soutiens")
carbunR = invoc("Carbuncle Rubis",strength=[PURCENTAGE,0.5],endurance=[PURCENTAGE,0.7],charisma=[PURCENTAGE,0.5],agility=[PURCENTAGE,0.7],precision=[PURCENTAGE,0.7],intelligence=[PURCENTAGE,0.5],magie=[PURCENTAGE,0.7],resistance=[PURCENTAGE,1],percing=[PURCENTAGE,1],critical=25,aspiration=POIDS_PLUME,icon=['<:carbunRB:904368034200834089>','<:carbunRR:904368049547776010>'],weapon=carbunRWeap,skill=[carbunRSkill1,carbunRSkill2],description="Un carbuncle de mêlée",element=ELEMENT_FIRE)