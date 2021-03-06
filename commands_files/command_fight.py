from commands_files.command_fight_add import *

async def fight(bot : discord.Client , team1 : list, team2 : list ,ctx : SlashContext, auto:bool = True,contexte:list=[],octogone:bool=False,bigMap:bool=False, procurFight = False, msg=None):
    try:
        """
            Base command for the fights\n
            \n
            Parameters :
            bot : the bot's discord client
            team1 : A list of Char objects
            team2 : A list of Char objects. Unlike team1, can be empty
            ctx : The context of the command, for know where to send the messages
            auto : Does the fight is a quick fight or a normal one ? Default ``True``
            contexte : A list of some parameters for the fight. Default ``[]``
                . exemple :
                    [TEAM1,<effect>] -> Give to the blue team the <effect> at the start of the fight
            octogone : If at ``False``, enable the loots and exp gains of the fight and lock the Fighting status of the team. Default ``False``
            slash : Does the command is slashed ? Default ``False``
        """
        if procurFight:
            user = loadCharFile("./userProfile/{0}.prof".format(ctx.author_id))
            team1[0].owner = user.owner
            team1[0].team = user.team
        now, mainUser, skillToUse = datetime.now(), None, None
        teamJaugeDict = [{},{}]

        for user in team1:
            if int(user.owner) == int(ctx.author_id):
                mainUser = user
                break

        if mainUser == None:
            mainUser = team1[0]

        # Base vars declalation
        listImplicadTeams, listFasTeam, tablAllieTemp, enableMiror, footerText, playOfTheGame, logs, haveError, dangerLevel, errorNb, optionChoice = [mainUser.team], [[],[]], copy.deepcopy(tablAllAllies), True, "", [1500,None,None], "[{0}]\n".format(now.strftime("%H:%M:%S, %d/%m/%Y")),False, [65,70,75,80,85,90,100,110,120,135,150], 0, None

        # dictIsNpcVar creation
        dictIsNpcVar = copy.deepcopy(primitiveDictIsNpcVar)

        print(ctx.author.name + " a lanc?? un combat")
        cmpt,tablAllCells,tour,danger,tablAliveInvoc,longTurn,longTurnNumber,haveMultipleHealers, oneVAll = 0,[],0,100,[0,0],False,[], [False,False], False

        for a in [0,1,2,3,4,5]:             # Creating the board
            for b in [[0,1,2,3,4],[0,1,2,3,4,5,6]][bigMap]:
                tablAllCells += [cell(a,b,cmpt,tablAllCells)]
                cmpt += 1

        allEffectInFight = []
        addEffect,tablEntTeam, ressurected = [],[],[[],[]]

        class entity:
            """Base class for the entities"""
            def __init__(self,identifiant : int, perso : Union[char,tmpAllie,octarien], team : int, player=True, auto=True, danger=100,summoner=None,dictInteraction:dict=None):
                """
                    Parameters :\n
                    .identifiant : A unique identifiant for a entity. Between ``0`` and ``15``
                        -> A summon share the same id than his summoner
                    .perso : A ``Char, TmpAllie`` or ``octarien`` object. The entity is generated from this parameter
                    .team : The team of the entity. ``0`` for the Blue Team, ``1`` for the Red Team
                    .player : Does the entity is a player ? Default ``True`` (Where this is use ?)
                    .auto : Does the entity is a manual or a automatic player ? Default ``True`` (Automatic)
                    .danger : A ``int`` use for uping the entity hp if it's a ``octarien``. Default ``100``
                    .summoner : The summoner of the entity. ``None`` if the entity isn't a summon, and by default
                """
                self.id = identifiant
                self.char = perso
                self.team = team
                self.type = player
                self.auto = auto
                self.weapon, self.chained = self.char.weapon, False
                if not(self.char.isNpc("Kiku") or self.char.isNpc("Zombie")):
                    self.status = STATUS_ALIVE
                else:
                    self.status = STATUS_RESURECTED

                if type(perso) != invoc:
                    self.icon = perso.icon
                else:
                    self.icon = perso.icon[team]

                self.stun = False
                self.summoner = summoner
                self.silent = False
                if not(self.char.isNpc("Kiku")):
                    self.raiser = None
                else:
                    self.raiser = self.icon
                self.specialVars = {"osPro":False,"osPre":False,"osIdo":False,"ohAlt":False,"ohPro":False,"ohIdo":False,"heritEstial":False,"heritLesath":False,"haveTrans":False,"tankTheFloor":False,"clemBloodJauge":None,"clemMemCast":False,"aspiSlot":None,"damageSlot":None,"summonerMalus":False,"finalTech":False,"foullee":False,"partner":None,"preci":False,"ironHealth":False,"fascination":None}

                if self.char.aspiration in [OBSERVATEUR, POIDS_PLUME]:
                    self.specialVars["aspiSlot"] = 0
                if type(perso) not in [invoc,octarien]:
                    baseHP,HPparLevel = 130,15
                elif type(perso) == invoc:
                    baseHP, HPparLevel, perso.level = 70, 8, summoner.char.level
                elif not(perso.oneVAll):
                    baseHP,HPparLevel = 90,10
                else:
                    baseHP,HPparLevel = 500,115

                self.effect: List[fightEffect] = []
                self.ownEffect =  []
                self.cell = None

                self.leftTurnAlive = 999
                if type(self.char) == invoc:
                    self.leftTurnAlive = 3

                self.strength,self.endurance,self.persoisma,self.agility,self.precision,self.intelligence,self.magie = 0,0,0,0,0,0,0
                self.resistance,self.percing,self.critical = 0,0,0
                self.negativeHeal, self.negativeBoost, self.negativeShield, self.negativeDirect, self.negativeIndirect = 0,0,0,0,0
                self.ressurectable = False
                self.cooldowns = [0,0,0,0,0,0,0]

                for a in [0,1,2,3,4,5,6]:
                    if type(self.char.skills[a]) == skill:
                        if self.char.skills[a].id == trans.id and self.char.skills[a].name == trans.name:
                            self.char.skills[a] = lb3Tabl[self.char.aspiration]
                            self.specialVars["haveTrans"] = True

                        elif self.char.skills[a].id == mageUlt.id:
                            if self.char.element in [ELEMENT_FIRE,ELEMENT_AIR,ELEMENT_SPACE]:
                                temp = mageUltZone
                            elif self.char.element in [ELEMENT_WATER,ELEMENT_EARTH,ELEMENT_TIME]:
                                temp = mageUltMono
                            else:
                                temp = mageUlt

                            self.char.skills[a] = temp

                        elif self.char.skills[a].id == finalTech.id:
                            self.specialVars["finalTech"] = True
                        self.cooldowns[a] = int(self.char.skills[a].ultimate)*2+self.char.skills[a].initCooldown

                self.stats = statTabl()
                self.medals = [0,0,0]
                self.healResist = 0
                self.missedLastTurn = False
                self.translucide = False
                self.untargetable = False
                self.invisible = False
                self.immune = False
                self.name = self.char.name
                self.aspiration = self.char.aspiration
                self.level = self.char.level
                self.block = 0

                self.dmgUp, self.critDmgUp, self.healUp, self.critHealUp = 0,0,0,0

                finded = False
                self.IA = AI_AVENTURE

                if self.char.aspiration in [BERSERK,OBSERVATEUR,POIDS_PLUME,TETE_BRULE,ATTENTIF]:
                    self.IA = AI_DPT

                elif self.char.aspiration in [IDOLE,INOVATEUR]:
                    self.IA = AI_BOOST

                elif self.char.aspiration in [ALTRUISTE,VIGILANT]:
                    self.IA = AI_ALTRUISTE

                elif self.char.aspiration in [MAGE,SORCELER]:
                    self.IA = AI_MAGE
                
                elif self.char.aspiration == ENCHANTEUR:
                    self.IA = AI_ENCHANT

                elif self.char.aspiration in [PREVOYANT,PROTECTEUR]:
                    self.IA = AI_SHIELD

                elif self.IA == AI_AVENTURE:
                    offSkill,SuppSkill,healSkill,armorSkill,invocSkill = 0,0,0,0,0
                    for b in [self.char.weapon]+self.char.skills:
                        if type(b) in [weapon,skill]:
                            if b.type in [TYPE_DAMAGE,TYPE_INDIRECT_DAMAGE]:
                                offSkill += 1
                            elif b.type in [TYPE_BOOST,TYPE_MALUS,TYPE_ARMOR]:
                                SuppSkill += 1
                            elif b.type in [TYPE_HEAL]:
                                healSkill += 1
                            elif b.type in [TYPE_SUMMON]:
                                invocSkill += 1
                        
                    if max(offSkill,SuppSkill,healSkill,armorSkill,invocSkill) == offSkill:
                        self.IA = AI_OFFERUDIT
                    elif max(offSkill,SuppSkill,healSkill,armorSkill,invocSkill) == SuppSkill:
                        self.IA = AI_BOOST
                    elif max(offSkill,SuppSkill,healSkill,armorSkill,invocSkill) == healSkill:
                        self.IA = AI_ALTRUISTE
                    elif max(offSkill,SuppSkill,healSkill,armorSkill,invocSkill) == armorSkill:
                        self.IA = AI_BOOST
                    elif max(offSkill,SuppSkill,healSkill,armorSkill,invocSkill) == invocSkill:
                        self.IA = AI_AVENTURE

                if type(self.char) != invoc:
                    baseStats = {STRENGTH:self.char.strength+self.char.majorPoints[0],ENDURANCE:self.char.endurance+self.char.majorPoints[1],CHARISMA:self.char.charisma+self.char.majorPoints[2],AGILITY:self.char.agility+self.char.majorPoints[3],PRECISION:self.char.precision+self.char.majorPoints[4],INTELLIGENCE:self.char.intelligence+self.char.majorPoints[5],MAGIE:self.char.magie+self.char.majorPoints[6],RESISTANCE:self.char.majorPoints[7],PERCING:self.char.majorPoints[8],CRITICAL:self.char.majorPoints[9],10:self.char.majorPoints[10],11:self.char.majorPoints[11],12:self.char.majorPoints[12],13:self.char.majorPoints[13],14:self.char.majorPoints[14]}
                    for obj in [self.char.weapon,self.char.stuff[0],self.char.stuff[1],self.char.stuff[2]]:
                        valueElem = 1
                        if obj.affinity == self.char.element :
                            valueElem = 1.1
                        
                        baseStats[0] += int(obj.strength*valueElem)
                        baseStats[1] += int(obj.endurance*valueElem)
                        baseStats[2] += int(obj.charisma*valueElem)
                        baseStats[3] += int(obj.agility*valueElem)
                        baseStats[4] += int(obj.precision*valueElem)
                        baseStats[5] += int(obj.intelligence*valueElem)
                        baseStats[6] += int(obj.magie*valueElem)
                        baseStats[7] += int(obj.resistance*valueElem)
                        baseStats[8] += int(obj.percing*valueElem)
                        baseStats[9] += int(obj.critical*valueElem)
                        baseStats[10] += int(obj.negativeHeal)
                        baseStats[11] += int(obj.negativeBoost)
                        baseStats[12] += int(obj.negativeShield)
                        baseStats[13] += int(obj.negativeDirect)
                        baseStats[14] += int(obj.negativeIndirect)

                else:
                    baseStats = {STRENGTH:self.char.majorPoints[0],ENDURANCE:self.char.majorPoints[1],CHARISMA:self.char.majorPoints[2],AGILITY:self.char.majorPoints[3],PRECISION:self.char.majorPoints[4],INTELLIGENCE:self.char.majorPoints[5],MAGIE:self.char.majorPoints[6],RESISTANCE:self.char.majorPoints[7],PERCING:self.char.majorPoints[8],CRITICAL:self.char.majorPoints[9],10:self.char.majorPoints[10],11:self.char.majorPoints[11],12:self.char.majorPoints[12],13:self.char.majorPoints[13],14:self.char.majorPoints[14]}
                    temp = self.char.allStats()+[self.char.resistance,self.char.percing,self.char.critical]
                    temp2 = self.summoner.allStats()+[self.summoner.resistance,self.summoner.percing,self.summoner.critical]
                    adv = 0
                    for a in range(0,len(temp)):
                        if type(temp[a]) == list:
                            if temp[a][0] == PURCENTAGE:
                                baseStats[a] += int(temp2[a]*(temp[a][1]+adv))
                            elif temp[a][0] == HARMONIE:
                                harmonie = 0
                                for b in temp2:
                                    harmonie = max(harmonie,b)
                                baseStats[a] += harmonie*adv
                        else:
                            baseStats[a] = temp[a]

                if self.char.element in [ELEMENT_FIRE, ELEMENT_UNIVERSALIS_PREMO]:
                    baseStats[7] += 5
                elif self.char.element in [ELEMENT_WATER, ELEMENT_UNIVERSALIS_PREMO]:
                    baseStats[PRECISION] += 10
                elif self.char.element in [ELEMENT_AIR, ELEMENT_UNIVERSALIS_PREMO]:
                    baseStats[AGILITY] += 10
                elif self.char.element in [ELEMENT_EARTH, ELEMENT_UNIVERSALIS_PREMO]:
                    baseStats[6] += 5

                valueToBoost =  min(1,self.char.level / 50)
                baseStats[ENDURANCE] += int(30*valueToBoost)
                baseStats[RESISTANCE] += int(15*valueToBoost)

                if danger > 100 and type(self.char) == octarien:
                    add = int(danger/135 * 20)
                    for cmpt in [AGILITY,PRECISION,RESISTANCE]:
                        baseStats[cmpt] += add

                if self.char.weapon.id in eternalInkWeaponIds:
                    summation = 0
                    for stat in range(10,15):
                        if baseStats[stat] > 0:
                            summation = int(baseStats[stat]*0.7)
                            baseStats[stat] = 0

                    baseStats[self.char.weapon.use] += summation

                if self.char.aspiration == BERSERK:
                    self.specialVars["aspiSlot"] = BERS_LIFE_STEAL
                elif self.char.aspiration in [PROTECTEUR,VIGILANT,ENCHANTEUR]:
                    self.specialVars["aspiSlot"] = []

                # Specials interractions ---------------------------------------------------
                # Kitsunes Sisters
                if self.char.isNpc("Liu") or self.char.isNpc("Lia") or self.char.isNpc("Liz") or self.char.isNpc("Lio"):
                    baseStats[CHARISMA] = int(baseStats[CHARISMA] * (0.9 + 0.1 * (dictInteraction["Liu"]+dictInteraction["Lia"]+dictInteraction["Liz"]+dictInteraction["Lio"])))

                # Alice : Increase stats by sisters in the fight
                elif self.char.isNpc("Alice"):
                    baseStats[CHARISMA] = int(baseStats[CHARISMA] * (1 + 0.05 * (dictInteraction["Sixtine"]+dictInteraction["F??licit??"]+dictInteraction["Cl??mence"])))

                # F??licit?? : Increase stats by sisters in the fight
                elif self.char.isNpc("F??licit??"):
                    baseStats[STRENGTH] = int(baseStats[STRENGTH] * (1 + 0.05 * (dictInteraction["Sixtine"]+dictInteraction["Alice"]+dictInteraction["Cl??mence"])))

                # Sixtine : Increase stats by sisters in the fight
                elif self.char.isNpc("Sixtine"):
                    baseStats[INTELLIGENCE] = int(baseStats[INTELLIGENCE] * (1 + 0.05 * (dictInteraction["F??licit??"]+dictInteraction["Alice"]+dictInteraction["Cl??mence"])))

                # Cl??mence : Increase stats by sisters in the fight
                elif self.char.isNpc("Cl??mence"):
                    baseStats[MAGIE] = int(baseStats[MAGIE] * (1 + 0.05 * (dictInteraction["Sixtine"]+dictInteraction["Alice"]+dictInteraction["F??licit??"])))

                # John : Increase stats if Clemence is in the figth
                elif self.char.isNpc("John"):
                    baseStats[STRENGTH], baseStats[ENDURANCE] = int(baseStats[STRENGTH] * (1 + 0.1 * dictInteraction["Cl??mence"])), int(baseStats[ENDURANCE] * (1 + 0.1 * dictInteraction["Cl??mence"]))

                self.baseStats = baseStats
                self.maxHp = round((baseHP+perso.level*HPparLevel)*((baseStats[ENDURANCE])/100+1))

                if type(self.char) == octarien:
                    self.maxHp = round(self.maxHp * danger / 100)
                self.hp = copy.deepcopy(self.maxHp)

                if type(self.char) == invoc:
                    self.specialVars["osPro"] = summoner.specialVars["osPro"]
                    self.specialVars["osPre"] = summoner.specialVars["osPre"]
                    self.specialVars["osIdo"] = summoner.specialVars["osIdo"]
                    self.specialVars["ohAlt"] = summoner.specialVars["ohAlt"]
                    self.specialVars["ohPro"] = summoner.specialVars["ohPro"]
                    self.specialVars["ohIdo"] = summoner.specialVars["ohIdo"]

            def allStats(self):
                """Return the mains 7 stats"""
                return [self.strength,self.endurance,self.charisma,self.agility,self.precision,self.intelligence,self.magie]

            def move(self,cellToMove:Union[cell,None]=None ,x:Union[int,None]=None ,y:Union[int,None]=None):
                """Move the entity on the given coordonates"""
                if self.chained:
                    return ""
                if cellToMove == x == y == None:
                    raise Exception("Argument error : No parameters given")
                actCell = self.cell
                if cellToMove == None:
                    destination = findCell(x,y,tablAllCells)
                else:
                    destination = findCell(cellToMove.x,cellToMove.y,tablAllCells)
                self.cell = destination
                destination.on = self
                if actCell != None:
                    actCell.on = None

            def valueBoost(self,target = 0,heal=False,armor=False):
                """
                    Return the bonus multiplier for any Buff, Debuff or Healing action\n
                    Parameter :\n
                    .target : A ``entity``.
                        -> Use for the Altruistic malus on their-self
                    .heal : Does the action is a Heal action ? Default ``False``
                """

                if target == 0:
                    raise Exception("No target given")

                if self.char.aspiration == ALTRUISTE:           # Altruistic : Better heals and buff on others
                    if heal:
                        if target == self:
                            return 1
                        else:
                            return 1.2
                    else:
                        if target == self:
                            return 0.8
                        else:
                            return 1.2

                elif self.char.aspiration == IDOLE and not(heal) and not(armor):             # Idol : The more alive allies they got, the more their buff a heals or powerfull
                    alice = 0
                    for a in tablEntTeam[self.team]:
                        if a.hp > 0 and type(a.char) != invoc:
                            alice += 1

                    return 0.9 + alice*0.05
                
                elif self.char.aspiration == INOVATEUR and not(heal) and not(armor):             # Idol : The more alive allies they got, the more their buff a heals or powerfull
                    alice = 0
                    for a in tablEntTeam[not(self.team)]:
                        if a.hp > 0 and type(a.char) != invoc:
                            alice += 1

                    return 0.9 + alice*0.05

                elif self.char.aspiration in [PREVOYANT,PROTECTEUR] and armor:
                    if self.char.aspiration == PREVOYANT:
                        return 1.2
                    else:
                        return 1 + 0.05 * len(self.specialVars["aspiSlot"])

                elif self.char.aspiration == VIGILANT and heal:
                    return 1 + 0.05 * len(self.specialVars["aspiSlot"])

                else:
                    return 1

            def effectIcons(self):
                """Return a ``string`` with alls ``fightEffects`` icons, names and values on the entity"""
                temp,allReadySeenId,allReadySeenName,allReadySeenNumber = "", [], [], []
                if self.effect != []:
                    for a in self.effect:
                        if a.effect.stackable and a.effect.id in allReadySeenId and a.effect.id not in [vulne.id,dmgUp.id,dmgDown.id,defenseUp.id,kikuRaiseEff.id,kikuUnlifeGift.id]:
                            for cmpt in range(len(allReadySeenId)):
                                if a.effect.id == allReadySeenId[cmpt]:
                                    allReadySeenNumber[cmpt] += 1
                        elif a.effect.stackable and a.effect.id not in allReadySeenId and a.effect.id not in [vulne.id,dmgUp.id,dmgDown.id,defenseUp.id,kikuRaiseEff.id,kikuUnlifeGift.id]:
                            allReadySeenId.append(a.effect.id)
                            allReadySeenNumber.append(1)
                            allReadySeenName.append("{0} {1}".format(a.icon,a.effect.name))
                        else:
                            name = a.effect.name
                            if name.endswith("??"):
                                name += self.accord()
                            if a.type == TYPE_ARMOR:
                                temp += f"{a.icon} {name} ({a.value} PAr)\n"
                            elif a.effect.id in [vulne.id,dmgUp.id,dmgDown.id,defenseUp.id,kikuRaiseEff.id,kikuUnlifeGift.id]:
                                power = round(a.effect.power,2)
                                temp += f"{a.icon} {name} ({power}%)\n"
                            elif a.effect.turnInit > 0:
                                pluriel = ""
                                if a.turnLeft > 1:
                                    pluriel = "s"
                                temp += f"{a.icon} {name} ({a.turnLeft} tour{pluriel})\n"
                            elif a.effect.id == eventFas.id:
                                temp += f"{a.icon} {name} ({a.value})\n"
                            else:
                                temp += f"{a.icon} {name}\n"
                    if allReadySeenId != []:
                        for cmpt in range(len(allReadySeenId)):
                            temp += "{0}{1}\n".format(allReadySeenName[cmpt],[""," x{0}".format(allReadySeenNumber[cmpt])][allReadySeenNumber[cmpt]>1])
                else:
                    temp = "Pas d'effet sur la cible"

                if len(temp) > 1024:
                    temp = completlyRemoveEmoji(temp)
                if len(temp) > 1024:
                    temp = "OVERLOAD"
                return temp

            def recalculate(self,ignore=None):
                """
                    Recalculate the entity stats with all their ``fightEffects``\n
                    - Parameter :
                        - ignore : A ``fightEffect`` to ignore. Default ``None``
                """
                self.dmgUp, self.critDmgUp, self.healUp, self.critHealUp, self.silent, self.translucide, self.untargetable, self.invisible, self.immune, self.stun, self.block, baseStats = 0,0,0,0, False, False, False, False, False, False, 0, self.baseStats
                sumStatsBonus, self.chained = copy.deepcopy(baseStats), False

                for eff in self.effect:
                    if eff != ignore:
                        if eff.effect.stat != None and eff.effect.overhealth == 0:
                            tablEffStats = eff.allStats()
                            for cmpt in range(9):
                                sumStatsBonus[cmpt] += tablEffStats[cmpt]

                        else:
                            sumStatsBonus[0] += eff.effect.strength 
                            sumStatsBonus[1] += eff.effect.endurance 
                            sumStatsBonus[2] += eff.effect.charisma
                            sumStatsBonus[3] += eff.effect.agility
                            sumStatsBonus[4] += eff.effect.precision
                            sumStatsBonus[5] += eff.effect.intelligence
                            if eff.effect.id == "tem":
                                sumStatsBonus[6] += int(self.char.level * 2.5)
                            else:
                                sumStatsBonus[6] += eff.effect.magie
                            sumStatsBonus[7] += eff.effect.resistance
                            sumStatsBonus[8] += eff.effect.percing
                            sumStatsBonus[9] += eff.effect.critical
                            self.block += eff.effect.block
                    if eff.stun:
                        self.stun = True
                    if eff.effect.invisible:
                        self.translucide = True
                        self.untargetable = True
                        self.invisible = True
                    if eff.effect.translucide:
                        self.translucide = True
                    if eff.effect.untargetable:
                        self.untargetable = True
                    if eff.effect.immunity:
                        self.immune = True
                    if eff.effect.id == silenceEff.id:
                        self.silent = True
                    elif eff.effect.id == chained.id:
                        self.chained = True
                    self.dmgUp, self.critDmgUp, self.healUp, self.critHealUp = self.dmgUp+eff.effect.dmgUp, self.critDmgUp+eff.effect.critDmgUp, self.healUp+eff.effect.healUp, self.critHealUp+eff.effect.critHealUp
                if type(self.char) != invoc:
                    tRes = sumStatsBonus[7]+self.char.resistance
                else:
                    tRes = sumStatsBonus[7]

                t1 = max(0,tRes - 100)
                t2 = min(max(0,tRes - 40),60)
                t3 = min(tRes,40)

                sumStatsBonus[7] = int(t3 + t2//3 + t1//5)

                if type(self.char) in [char,tmpAllie] and sumStatsBonus[7] < 50:
                    sumStatsBonus[7] = max(5 + int(15/50*self.char.level)+sumStatsBonus[7],5 + int(15/50*self.char.level))

                for temp in range(len(sumStatsBonus)):
                    sumStatsBonus[temp] = round(sumStatsBonus[temp])
                if ignore == None:
                    self.strength,self.endurance,self.charisma,self.agility,self.precision,self.intelligence,self.magie, self.resistance,self.percing,self.critical, self.negativeHeal, self.negativeBoost, self.negativeShield, self.negativeDirect, self.negativeIndirect = sumStatsBonus[0], sumStatsBonus[1], sumStatsBonus[2], sumStatsBonus[3], sumStatsBonus[4] ,sumStatsBonus[5] ,sumStatsBonus[6], sumStatsBonus[7], sumStatsBonus[8],sumStatsBonus[9],sumStatsBonus[10],sumStatsBonus[11],sumStatsBonus[12],sumStatsBonus[13],sumStatsBonus[14]
                else:
                    if type(self.char) != invoc:
                        return [
                            round(self.char.strength+sumStatsBonus[0]),round(self.char.endurance+sumStatsBonus[1]),round(self.char.charisma+sumStatsBonus[2]),round(self.char.agility+sumStatsBonus[3]),round(self.char.precision+sumStatsBonus[4]),round(self.char.intelligence+sumStatsBonus[5]),round(self.char.magie+sumStatsBonus[6]),
                            sumStatsBonus[7],round(self.char.percing+sumStatsBonus[8]),round(self.char.critical+sumStatsBonus[9]),
                            sumStatsBonus[10],sumStatsBonus[11],sumStatsBonus[12],sumStatsBonus[13],sumStatsBonus[14]]
                    else:
                        return [
                            round(sumStatsBonus[0]),round(sumStatsBonus[1]),round(sumStatsBonus[2]),round(sumStatsBonus[3]),round(sumStatsBonus[4]),round(sumStatsBonus[5]),round(sumStatsBonus[6]),
                            sumStatsBonus[7],round(sumStatsBonus[8]),round(sumStatsBonus[9]),
                            sumStatsBonus[10],sumStatsBonus[11],sumStatsBonus[12],sumStatsBonus[13],sumStatsBonus[14]
                        ]

            def refreshEffects(self):
                """Add the ``fightEffects`` into the waiting list and remove the obcelettes ones"""
                for eff in self.effect[:]:
                    if eff.remove:
                        self.effect.remove(eff)
                        try:
                            eff.caster.ownEffect.remove({self:eff.id})
                        except:
                            pass

                        if eff.effect.id == lunaInfiniteDarknessShield.id:
                            self.specialVars["clemBloodJauge"] = None
                        
                        elif eff.effect.id in [clemStunEffect.id,aliceStunEffect.id]:
                            self.specialVars["clemBloodJauge"].value = 100

                for a in addEffect[:]:
                    self.effect.append(a)
                    a.caster.ownEffect.append({self:a.id})
                    addEffect.remove(a)
                    if type(a) != fightEffect:
                        raise AttributeError("Except fightEffect, but get {0} insted".format(type(a)))
                self.recalculate()

            def indirectAttack(self,target=0,value=0,icon="",ignoreImmunity=False,name='',hideAttacker=False,canCrit=True) -> str:
                """
                Method for when the entity is attacking undirectly another.\n
                /!\ Unlike .attack(), the damage need to be pre-calculated\n
                Parameters :\n
                .target : Another ``entity`` who's receving damage
                .value : The amount of damage deal. Default ``0``
                .icon : The ``string`` to use as the icon of the attack. Default ``""``
                .ignoreImmunity : Does the attack ignore any immune effect ? Default ``False``
                .name : The ``string`` to use as the name of the attakc. Default ``""``
                """
                popopo, hasCrit = "", ""
                if canCrit:
                    if random.randint(0,99) < self.intelligence/200*25 * (1-(target.intelligence/100*10)/100):
                        if self.char.aspiration == SORCELER:
                            value = value * 1.25
                            hasCrit = " !!"
                        else:
                            value = value * 1.15
                            hasCrit = " !"

                value = round(value)
                if target.hp > 0 and not(target.immune):
                    # Looking for a absolute shield
                    maxResist, vulnePower = 0, 0
                    for eff in target.effect:
                        if eff.effect.immunity == True and not(ignoreImmunity):
                            value = 0
                        if eff.effect.absolutShield and eff.value > 0:
                            dmg = min(value,eff.value)
                            if not(hideAttacker):
                                popopo += f"{self.icon} {icon} ??? {eff.icon}{eff.on.icon} -{dmg} PV\n"
                            else:
                                popopo += f"{eff.icon}{eff.on.icon} -{dmg} PV\n"
                            popopo += eff.decate(value=dmg)
                            self.stats.damageOnShield += dmg
                            if eff.value <= 0:
                                reduc = eff.on.char.level
                                if eff.effect.lightShield:
                                    reduc = 0
                                value = max(0,dmg-reduc)
                            else:
                                value = 0

                    if type(target.char) == invoc and target.char.name.startswith("Patte de The Giant Enemy Spider"):
                        value = int(value * GESredirect.redirection/100)
                        target.summoner.hp -= value
                        if self != target:                  # If the damage is deal on another target, increase the correspondings stats
                            self.stats.damageDeal += value
                            self.stats.indirectDamageDeal += value
                            target.stats.damageRecived += value
                        if target.summoner.hp <= 0:
                            popopo += target.death(killer=self)
                        value = 0

                    # If the number of damage is still above 0
                    if value > 0:
                        target.hp -= value
                        if self != target:                  # If the damage is deal on another target, increase the correspondings stats
                            self.stats.damageDeal += value
                            self.stats.indirectDamageDeal += value
                            target.stats.damageRecived += value
                        else:                               # Else, increase the selfBurn stats
                            self.stats.selfBurn += value
                        if name != '':
                            name = ' ({0})'.format(name)
                        if not(hideAttacker):
                            popopo += f"{self.icon} {icon} ??? {target.icon} -{value} PV{hasCrit}{name}\n"
                        else:
                            popopo += f"{target.icon} -{value} PV{hasCrit}{name}\n"
                        if self.isNpc("Liz") or (self.isNpc("Kitsune") and type(target.char != classes.invoc) and ((skillToUse != None and skillToUse.id != kitsuneSkill4.id)or(skillToUse == None))):
                            popopo += add_effect(self,target,charming,skillIcon=self.char.weapon.effect.emoji[0][0])
                            target.refreshEffects()

                        if target.hp <= 0:
                            popopo += target.death(killer=self)
                            if self == target:
                                self.stats.sufferingFromSucess = True

                        if self.isNpc("Cl??mence pos."):
                            self.specialVars["clemBloodJauge"].value = min(100,self.specialVars["clemBloodJauge"].value+int(value * (0.03*(1+self.level/100))))

                return popopo

            def death(self,killer = 0,trueDeath=False) -> str:
                """
                    The death method, to use when the entity dies.\n
                    Parameter :\n
                    .killer : The ``entity`` who have kill the entity
                """

                for eff in self.effect:
                    if not(trueDeath):
                        if eff.effect.id in [undeadEff2.id,holmgangEff.id] and eff.turnLeft > 0:
                            self.hp = 1
                            return "{0} ne peut pas ??tre vaincu{1} ({2})\n".format(self.name,self.accord(),eff.effect.name)
                        elif eff.effect.id == undeadEff.id:
                            ballerine = groupAddEffect(self,self,AREA_MONO,eff.effect.callOnTrigger,skillIcon=eff.icon)
                            ballerine += eff.decate(value=1)
                            self.refreshEffects()
                            self.hp = 1
                            return "{4} transcende la mort !\n{0} {1} ??? {0} +{2} __{3}__\n".format(self.icon, eff.icon, eff.effect.callOnTrigger.emoji[self.char.species-1][self.team],eff.effect.callOnTrigger.name,self.name)
                        elif eff.effect.id == kikuRaiseEff.id:
                            self.status = STATUS_RESURECTED
                            actMaxHp = self.maxHp
                            self.maxHp = int(self.maxHp*(100+eff.effect.power)/100)
                            self.hp = int(self.maxHp*0.75)
                            eff.decate(value=99)
                            shieldValue = int(self.maxHp*0.2)
                            add_effect(eff.caster,self,classes.effect("R??surection r??cente","susRez",overhealth=shieldValue,turnInit=3,absolutShield=True,emoji=sameSpeciesEmoji('<:naB:908490062826725407>','<:naR:908490081545879673>')),ignoreEndurance=True)
                            tempEff,healBuffPerma = copy.deepcopy(dmgUp), copy.deepcopy(absEff)
                            tempEff.power, tempEff.turnInit, healBuffPerma.power, healBuffPerma.turnInit, healBuffPerma.silent = eff.effect.power, -1, eff.effect.power, -1, True
                            add_effect(eff.caster,self,tempEff)
                            add_effect(eff.caster,self,healBuffPerma)
                            self.refreshEffects()
                            self.raiser = eff.caster.icon
                            eff.caster.stats.allieResurected += 1
                            return "{4} ({0}) est vaincu{5} !\n<:kiku:962082466368213043> <:mortVitaEst:916279706351968296> ??? <:renisurection:873723658315644938> {0} +{1} PV +{6} PvMax {2} +{3} PAr\n".format(self.icon,self.hp,['<:naB:908490062826725407>','<:naR:908490081545879673>'][self.team],shieldValue,self.char.name,self.accord(),int(self.maxHp-actMaxHp))
                        elif eff.effect.id == mve2Eff.id:
                            if self.status == STATUS_ALIVE:
                                self.status = STATUS_RESURECTED
                                self.hp = int(self.maxHp*eff.effect.power/100)
                                eff.decate(value=99)
                                shieldValue = int(self.maxHp*0.2)
                                add_effect(eff.caster,self,classes.effect("R??surection r??cente","susRez",overhealth=shieldValue,turnInit=3,absolutShield=True,emoji=sameSpeciesEmoji('<:naB:908490062826725407>','<:naR:908490081545879673>')),ignoreEndurance=True)
                                self.refreshEffects()
                                self.raiser = eff.caster.icon
                                eff.caster.stats.allieResurected += 1
                                return "{4} ({0}) est vaincu{5} !\n{0} <:mortVitaEst:916279706351968296> ??? <:renisurection:873723658315644938> {0} +{1} PV {2} +{3} PAr\n".format(self.icon,self.hp,['<:naB:908490062826725407>','<:naR:908490081545879673>'][self.team],shieldValue,self.char.name,self.accord())

                if self.isNpc("Aformit?? incarn??e") and dictIsNpcVar["Luna pr??."]:
                    if not(killer.isNpc("Luna pr??.")):
                        self.hp = 1
                        return ""
                    else:
                        add_effect(self,killer,classes.effect("Borgne","lunaBlinded",precision=-50,stat=MAGIE,turnInit=-1,unclearable=True))
                        killer.refreshEffects()

                pipistrelle = f"{self.char.name} ({self.icon}) est vaincu{self.accord()} !\n"
                if self.status == STATUS_RESURECTED:
                    pipistrelle = f"{self.char.name} ({self.icon}) est vaincu{self.accord()} (pour de bon) !\n"
                    self.status=STATUS_TRUE_DEATH

                if type(self.char) != invoc and killer != self and killer.char.says.onKill != None and random.randint(0,99)<33:
                    try:
                        if killer.isNpc("Ailill"):
                            pipistrelle += "{0} : *\"{1}\"*\n".format('<a:Ailill:882040705814503434>','??a manque de sang qui gicle partout ??a')
                        elif killer.isNpc("Luna pr??.") or killer.isNpc("Luna ex."):
                            msgPerElement = [None,None,None,None,None,"La lumi??re ne peut pas toujours avoir raison de l'ombre.","Reviens donc quand tu auras compris ce que sont les vrais T??n??bres.","L'Espace peut tr??s bien ??tre bris??.","Essaye donc de gagner du Temps l?? dessus.","Tu as tous les ??l??ments et tu n'est m??me pas capable de t'en sortir ?"]
                            if msgPerElement[self.char.element] != None:
                                pipistrelle += "{0} : *\"{1}\"*\n".format(killer.icon,msgPerElement[self.char.element])
                            else:
                                pipistrelle += "{0} : *\"{1}\"*\n".format(killer.icon,killer.char.says.onKill.format(target=self.char.name,caster=killer.char.name))
                        elif killer.isNpc("Ly") and self.isNpc("Zombie"):
                            pipistrelle += "{0} : *\"Tu peux ramner tous tes potes si tu veux, je connais un pr??tre qui est toujours pr??t ?? me racheter de la rotten flesh\"*\n".format(killer.icon,killer.char.says.onKill.format(target=self.char.name,caster=killer.char.name))
                        elif killer.isNpc("Shehisa") and not(actTurn.isNpc("Shehisa")):
                            pipistrelle += "{0} : *\"Tu devrais faire plus attention o?? tu met les pieds la prochaine fois\"*\n".format(killer.icon)
                        elif killer.isNpc("Lohica") and not(actTurn.isNpc("Lohica")):
                            pipistrelle += "{0} : *\"Alors, ??a t'a coup?? le souffle hein ?\"*\n".format(killer.icon)
                        elif killer.isNpc("Cl??mence Exalt??e"):
                            pipistrelle += "{0} : *\"{1}\"*\n".format(killer.icon,clemExKillReact[self.char.aspiration].format(target=self.char.name,caster=killer.char.name))
                        elif killer.hp > 0:
                            pipistrelle += "{0} : *\"{1}\"*\n".format(killer.icon,killer.char.says.onKill.format(target=self.char.name,caster=killer.char.name))
                    except:
                        pipistrelle += "__Error whith the onKill message__\n"
                        log = format_exc()
                        if len(log) > 50:
                            pipistrelle += "{0}\n".format(log[-50:])
                        else:
                            pipistrelle += "{0}\n".format(log)

                if self.isNpc("Alice") and random.randint(0,99) < 1:
                    pipistrelle += "{0} : *\"{1}\"*\n".format(self.icon,"Tss... J'aurais du tous vous ??craser quand je l'aurais pu...")
                    alicePing = True

                elif (self.isNpc("Shushi") or self.isNpc("Shihu")) and dictIsNpcVar["Lena"]:
                    pipistrelle += "{0} : *\"{1}\"*\n".format('<:lena:909047343876288552>','Shu- Ok l?? on va s??rieusement commencer ?? se calmer.')
                    for ent in tablEntTeam[self.team]:
                        if ent.isNpc("Lena"):
                            mater = classes.effect("Instinct maternelle","ohFuckYou",critDmgUp=10,critical=5,percing=10,turnInit=-1,emoji=uniqueEmoji('<:angry:862321601978040350>'),stackable=True)
                            pipistrelle += add_effect(ent,ent,mater)
                            ent.refreshEffects()
                            break

                elif self.isNpc("Alice Exalt??e") and killer.isNpc("Cl??mence pos."):
                    pipistrelle += "<a:aliceExalte:914782398451953685> : \"Cl??...\"\n<a:clemPos:914709222116175922> : \"... ?\""
                    effect = classes.effect("R??veil subconsicent","clemAwakening",magie=-int((killer.baseStats[MAGIE]*0.3)),turnInit=-1,unclearable=True,type=TYPE_MALUS)
                    pipistrelle += add_effect(killer,killer,effect)
                    killer.char.exp = 35

                elif self.isNpc("Lohica") and killer != self:
                    pipistrelle += "{0} : *\"Ok {1}, qu'est-ce que tu dis de ??a ?\"*\n".format(self.icon,killer.char.name) + add_effect(self,killer,estal)
                    killer.refreshEffects()

                elif self.isNpc("Amary") and killer != self and dictIsNpcVar["Lohica"]:
                    lohica = None
                    for team in (0,1):
                        for ent in tablEntTeam[team]:
                            if ent.isNpc("Lohica") and ent.hp > 0:
                                lohica = ent
                                break

                    if lohica != None:
                        pipistrelle += "{0} : *\"Tu vas payer pour ??a.\"*\n".format(lohica.icon) + add_effect(lohica,killer,estal,effPowerPurcent=[100,150][lohica.team != killer.team])
                        killer.refreshEffects()
                elif random.randint(0,99)<33:
                    if self.isNpc("Hina") and dictIsNpcVar["Lohica"]:
                        pipistrelle += "{0} : *\"{1}\"*\n".format('<:lohica:919863918166417448>','Ts. Encore par terre toi ?')
                    elif self.isNpc("Edelweiss") and dictIsNpcVar["Lohica"]:
                        pipistrelle += "{0} : *\"{1}\"*\n".format('<:lohica:919863918166417448>','Am-')
                    elif self.isNpc("Cl??mence") and dictIsNpcVar["John"]:
                        pipistrelle += "{0} : *\"{1}\"*\n".format('<:john:908887592756449311>','Cl??mence !')
                    elif self.isNpc("F??licit??") and dictIsNpcVar["Alice"]:
                        pipistrelle += "{0} : *\"{1}\"*\n".format('<:alice:908902054959939664>','F??li ! On se retrouve ?? la maison !')
                    elif self.char.says.onDeath != None:
                        try:
                            pipistrelle += "{0} : *\"{1}\"*\n".format(self.icon,self.char.says.onDeath.format(target=self.char.name,caster=killer.char.name))
                        except:
                            pipistrelle += "__Error whith the death message__\n"
                            log = format_exc()
                            if len(log) > 50:
                                pipistrelle += "{0}\n".format(log[-50:])
                            else:
                                pipistrelle += "{0}\n".format(log)

                try:                # Reactions
                    if self.isNpc("Stella") and dictIsNpcVar["Alice"]:
                        for ent in tablEntTeam[int(not(self.team))]:
                            if ent.isNpc("Alice") and ent.hp > 0:
                                pipistrelle += "{0} : *\"J'ai m??me pas envie d'exprimer une once d'empatie.\"\n".format(ent.icon)
                                break
                    
                    elif self.isNpc("Alice") and dictIsNpcVar["Stella"]:
                        for ent in tablEntTeam[int(not(self.team))]:
                            if ent.isNpc("Stella") and ent.hp > 0:
                                pipistrelle += "{0} : *\"M??me pas capable de supporter quelques d??g??ts et tu esp??res me concurrencer ?\"\n".format(ent.icon)
                                break

                    elif self.isNpc("S??r??na") and dictIsNpcVar["Lohica"]:
                        for ent in tablEntTeam[int(not(self.team))]:
                            if ent.isNpc("Lohica") and ent.hp > 0:
                                pipistrelle += "{0} : *\"J'esp??re que tu passeras bien le restant de tes jours ?? croupir aux enfers.\"\n".format(ent.icon)
                                break

                    elif self.isNpc("Lohica") and dictIsNpcVar["S??r??na"]:
                        for ent in tablEntTeam[int(not(self.team))]:
                            if ent.isNpc("S??r??na") and ent.hp > 0:
                                pipistrelle += "{0} : *\"T'en fais pas, je me rappellerais de comment tu as vainnement essay?? de me tenir t??te quand je consulterais ta fleur d??s??ch??e dans mon herbier\"\n".format(ent.icon)
                                break

                    elif random.randint(0,99) < 20 and type(self.char) != invoc:
                        tablAllInterract = []
                        for ent in tablEntTeam[self.team]:
                            if ent.char.says.reactAllyKilled != None and ent != self and ent.hp > 0:
                                tablAllInterract.append("{0} : *\"{1}\"*\n".format(ent.icon,ent.char.says.reactAllyKilled.format(killer=killer.char.name,downed=self.char.name)))
                        for ent in tablEntTeam[not(self.team)]:
                            if ent.char.says.reactEnnemyKilled != None and ent != killer and ent.hp > 0:
                                tablAllInterract.append("{0} : *\"{1}\"*\n".format(ent.icon,ent.char.says.reactEnnemyKilled.format(killer=killer.char.name,downed=self.char.name)))

                        if len(tablAllInterract) == 1:
                            pipistrelle += tablAllInterract[0]
                        elif len(tablAllInterract) > 1:
                            pipistrelle += tablAllInterract[random.randint(0,len(tablAllInterract)-1)]

                except:
                    pipistrelle += "__Error whith the death reaction message__\n"
                    log = format_exc()
                    if len(log) > 50:
                        pipistrelle += "{0}\n".format(log[-50:])
                    else:
                        pipistrelle += "{0}\n".format(log)

                allreadyexplose = False
                for fEffect in self.effect:
                    if fEffect.trigger == TRIGGER_DEATH:
                        pipistrelle += fEffect.triggerDeath(killer)

                    if fEffect.effect.id == estal.id and fEffect.caster.char.weapon.id == secretum.id and not(allreadyexplose):
                        summationPower = 0
                        for eff in self.effect:
                            if eff.effect.id == estal.id and eff.turnLeft > 0:
                                summationPower += eff.effect.power * secretum.effect.power / 100 * eff.turnLeft
                                eff.decate(turn=99,value=99)
                        self.refreshEffects()

                        stat,damageBase,allReadySeen, killCount, dmgDict, beforeDmg, tempMsg, nbHit = fEffect.caster.allStats()[MAGIE]-fEffect.caster.negativeIndirect,summationPower,[], 0 , "", copy.deepcopy(killer.stats.indirectDamageDeal), "", 0
                        for a in self.cell.getEntityOnArea(area=secretum.effect.area,team=self.team,wanted=ALLIES,directTarget=False,fromCell=actTurn.cell):
                            reduc = 1
                            if a != self:
                                reduc = max(AOEMINDAMAGE,1-self.cell.distance(a.cell)*AOEDAMAGEREDUCTION)

                            damage = indirectDmgCalculator(killer,self,summationPower,MAGIE,[100,danger][killer.team==1],AREA_CIRCLE_2)*reduc

                            tempMsg += fEffect.caster.indirectAttack(a,value=damage,icon = secretum.emoji,name=secretum.effect.name)

                            if a.hp <= 0:
                                killCount += 1
                            else:
                                dmgDict += a.icon
                                nbHit += 1
                            
                        if killCount == 0 and nbHit > 0:
                            pipistrelle += "{0} {1} ??? {2} -??? {3} {4}\n".format(killer.icon, killer.char.weapon.emoji, dmgDict, (killer.stats.indirectDamageDeal-beforeDmg)//nbHit,secretum.effect.name)
                        else:
                            pipistrelle += tempMsg
        
                        if fEffect.caster.hp > 0:
                            pipistrelle += groupAddEffect(killer,self,allReadySeen,fEffect.caster.char.weapon.effect.emoji[0][0],effPurcent=secretum.effect.power)
                        allreadyexplose = True

                    elif fEffect.effect.id == reaperEff.id:
                        pipistrelle += fEffect.caster.heal(fEffect.caster,fEffect.icon,None,int(fEffect.caster.maxHp*fEffect.effect.power/100), effName = fEffect.effect.name,danger=danger, mono = True, useActionStats = None)[0]
                    if fEffect.trigger == TRIGGER_ON_REMOVE:
                        pipistrelle += fEffect.decate(turn=99)
                    else:
                        fEffect.decate(turn=99)
                self.refreshEffects()

                if killer.char.aspiration == SORCELER and type(self.char) != invoc and killer != self:
                    for a in self.cell.getEntityOnArea(area=AREA_CIRCLE_1,team=self.team,wanted=ALLIES,directTarget=False,fromCell=actTurn.cell):
                        reduc = 1
                        if a != self:
                            reduc = max(AOEMINDAMAGE,1-self.cell.distance(a.cell)*AOEDAMAGEREDUCTION)
                        damage = indirectDmgCalculator(killer,a,max(5,killer.char.level),MAGIE,[100,danger][killer.team==1],AREA_CIRCLE_1)*reduc

                        pipistrelle += killer.indirectAttack(a,value=damage,icon = aspiEmoji[SORCELER])

                if self.status == STATUS_ALIVE:
                    if self.ressurectable:
                        if type(self.char) != octarien or (type(self.char) == octarien and self.char.rez):
                            self.status = STATUS_DEAD
                        else:
                            self.status = STATUS_TRUE_DEATH
                    else:
                        self.status = STATUS_TRUE_DEATH

                if type(self.char) != invoc and self.status != STATUS_RESURECTED:
                    if self.char.deadIcon == None:
                        if type(self.char) != char:
                            self.icon = [None,'<:spIka:866465882540605470>','<:spTako:866465864399323167>','<:spOcta:866465980586786840>'][self.char.species]
                        else:
                            self.icon = [
                                ['<:spIka:866465882540605470>','<:spTako:866465864399323167>'][self.char.species-1],
                                ['<:oci:930481536564879370>','<:oct:930481523096969237>'][self.char.species-1],
                                '<:komoriOut:930798849969246208>',
                                '<:birdOut:930906560811646996>',
                                '<:outSkeleton:930910463951249479>',
                                ['<:fairyOut:935335430814068786>','<:fairy2Out:935336513242292324>'][self.char.species-1]
                            ][self.char.iconForm]
                    else:
                        self.icon = self.char.deadIcon

                elif self.status == STATUS_RESURECTED:
                    add_effect(self,self,onceButNotTwice)

                if self.status == STATUS_DEAD:
                    effect = lostSoul
                    if self.specialVars["tankTheFloor"]:
                        effect = copy.deepcopy(lostSoul)
                        effect.turnInit += 1
                    add_effect(killer,self,effect)
                    
                    self.refreshEffects()

                elif self.status == STATUS_TRUE_DEATH and killer.isNpc("Kitsune"):
                    pipistrelle += killer.heal(killer,"",CHARISMA,60, effName = "??me consumm??e",danger=100, mono = True, useActionStats = ACT_HEAL)[0]


                if type(self.char) != invoc and killer != self or killer.team != self.team:
                    killer.stats.ennemiKill += 1
                elif type(self.char) != invoc and killer != self and killer.team == self.team:
                    killer.stats.friendlyfire += 1
                return pipistrelle

            def attack(self,target=0,value = 0,icon = "",area=AREA_MONO,sussess=None,use=STRENGTH,onArmor = 1,effectOnHit = None, useActionStats = ACT_DIRECT, setAoEDamage = False, lifeSteal:int = 0, erosion = 0, skillPercing = 0, execution = False) -> str:
                """
                    The method for when a entity attack.\n
                    Unlike .indirectAttack(), the targets, damages and triggered effects are all calculated in this method\n
                    - Parameters :
                        - target : The ``entity`` targeted by the entity
                        - value : The base power of the attack.
                            - If the value is at ``0``, no ``string`` is return
                        - icon : The ``string`` to use as the icon of the attack. Default ``""``
                        - area : The area of the attack. See ``constantes``. Default ``AREA_MONO``
                        - sussess : The base precision of the attack. If at ``None`` (Default), use the sussess rate of the entity weapon insted
                        - use : The base stat to take for the attack. See ``constantes``
                        - onArmor : The multiplier of damage to deal on armors effects. Default ``1``
                        - effectOnHit : Does the attack give a `effect` on the targets ? Default ``None``
                """
                if sussess==None: # If no success is gave, use the weapon success rate
                    sussess=self.char.weapon.sussess

                if value > 0 and self.specialVars["damageSlot"] != None and ((self.specialVars["damageSlot"].effect.id == physicRuneEff.id and use in [STRENGTH,PRECISION,AGILITY]) or (self.specialVars["damageSlot"].effect.id == magicRuneEff.id and use in [MAGIE,CHARISMA,INTELLIGENCE])):
                    value = value * (self.specialVars["damageSlot"].effect.power/100+1)

                if useActionStats == None:
                    useActionStats = ACT_DIRECT

                sumDamage, deathCount = 0, 0

                popipo,critMsg = "",""

                if type(target) != int and value > 0: # If the target is valid
                    dangerMul, tmpBalancing, dodgeMul = 1, 0, 1
                    if danger != None and self.team: # get danger value
                        dangerMul = danger/100

                    popipo,aoeFactor,dmgUpPower,eroTxt, damageMul, isDepha, lifeStealBonus = "",1, 0+5*int(not(self.auto)),["",aspiEmoji[TETE_BRULE]][self.char.aspiration == TETE_BRULE], 1, False, 0
                    if erosion != 0:
                        eroTxt += icon
                    if self.char.aspiration == TETE_BRULE:
                        erosion += 35

                    for a in self.effect: # Does the attacker trigger a effect
                        if a.trigger == TRIGGER_DEALS_DAMAGE and value > 0:
                            temp = a.triggerDamage(value = a.effect.power,icon=a.icon,onArmor=onArmor)
                            value = temp[0]
                            popipo += temp[1]
                        elif a.effect.id == dmgDown.id:
                            dmgUpPower -= a.effect.power
                        elif a.effect.id == dmgUp.id:
                            dmgUpPower += a.effect.power
                        elif a.effect.id == kikuUnlifeGift.id:
                            dmgUpPower += kikuUnlifeGift.power * tour
                        elif a.effect.id == areaDmgReductionTmp.id:
                            tmpBalancing = 1
                        elif a.effect.id == monoDmgReductionTmp.id:
                            tmpBalancing = 2
                        elif a.effect.id == lbRdmBlind.id:
                            dodgeMul -= lbRdmBlind.power/100  
                            pass
                        elif a.effect.id == jetLagEff.id:
                            isDepha = True
                        elif a.effect.id == upgradedLifeSteal.id:
                            lifeStealBonus += a.effect.power
                    damageMul = damageMul + (dmgUpPower/100)
                    damageMul = max(0.05,damageMul)

                    if self.hp > 0: # Does the attacker still alive ?
                        critMalusCmpt = 0
                        for entityInArea in target.cell.getEntityOnArea(area=area,team=self.team,wanted=ENEMIES,directTarget=False,fromCell=actTurn.cell): # For eatch ennemis in the area
                            self.stats.totalNumberShot += 1
                            if entityInArea.hp > 0: # If the target is alive
                                # Dodge / Miss
                                attPre,targetAgi, dodgeMul = self.precision,entityInArea.agility, dodgeMul - (foulleeEff.power/100*int(entityInArea.specialVars['foullee']))

                                if attPre < 0:                                              # If the attacker's precision is negative
                                    targetAgi += abs(attPre)                                        # Add the negative to the target's agility
                                    attPre = 0
                                elif targetAgi < 0:                                         # Same if the target's agility is negative, add it to the attacker's precision
                                    attPre += abs(targetAgi)
                                    targetAgi = 1

                                if attPre < targetAgi:                                      # If the target's agility is (better ?) than the attacker's precision
                                    successRate = 1 - min((targetAgi-attPre)/100,1)*0.5 * dodgeMul             # The success rate is reduced to 50% of the normal
                                else:
                                    successRate = 1 + min((attPre-targetAgi)/100,1) * dodgeMul                 # The success rate is increased up to 200% of the normal

                                # It' a hit ?
                                if random.randint(0,99)<successRate*sussess:
                                    pp = 0
                                    if self.char.aspiration in [POIDS_PLUME,OBSERVATEUR]: # Apply "Poids Plume" critical bonus
                                        pp = actTurn.specialVars["aspiSlot"]

                                    # Get the stat used
                                    if use == HARMONIE:
                                        temp = 0
                                        for a in self.allStats():
                                            temp = max(a,temp)
                                        used = temp
                                    else:
                                        used = self.allStats()[use]
                                        if use == MAGIE and self.char.aspiration == ENCHANTEUR:
                                            used = int(used * 0.95+(0.05)*len(self.specialVars["aspiSlot"]))

                                    if entityInArea.immune:
                                        damage = 0
                                    else:
                                        if self.team == 0 or octogone:
                                            dangerValue = 100
                                        else:
                                            dangerValue = danger
                                        damage = dmgCalculator(self, entityInArea, value, use, useActionStats, dangerValue, area, typeDmg = TYPE_DAMAGE, skillPercing = 0)

                                    # AoE reduction factor
                                    if target.cell.distance(entityInArea.cell) == 0 or setAoEDamage:
                                        if tmpBalancing == 2 and entityInArea == target:
                                            aoeFactor = 1 - monoDmgReductionTmp.power/100
                                        else:
                                            aoeFactor = 1
                                    else:
                                        aoeFactor = 1-(min(1-AOEMINDAMAGE,(target.cell.distance(entityInArea.cell)-int(target==self))*AOEDAMAGEREDUCTION))
                                        if tmpBalancing == 1:
                                            aoeFactor = max(0.1,aoeFactor-(areaDmgReductionTmp.power/100))

                                    # Damage reduction
                                    vulnePower, defenseUpPower, tempToReturn, noneArmorMsg, reaperDmgBoost, lifeSavor = 0, 0, "", "", 0, []
                                    if not(entityInArea.immune):
                                        for a in entityInArea.effect:
                                            if a.trigger == TRIGGER_DAMAGE:
                                                temp = a.triggerDamage(value = damage,declancher=self,icon=icon,onArmor=onArmor)
                                                damage = temp[0]
                                                if a.effect.overhealth > 0 or a.effect.redirection > 0:
                                                    if self.icon not in tempToReturn:
                                                        tempToReturn = f"{self.icon} {icon} ??? "+temp[1]
                                                    else:
                                                        tempToReturn += temp[1]
                                                else:
                                                    noneArmorMsg += temp[1]

                                            if a.effect.id in [vulne.id,kikuRaiseEff.id]:
                                                vulnePower += a.effect.power
                                            elif a.effect.id == kikuUnlifeGift.id:
                                                defenseUpPower += min(80,kikuUnlifeGift.power/2 * tour)
                                            elif a.effect.id == defenseUp.id:
                                                defenseUpPower += a.effect.power
                                            elif a.effect.id == reaperEff.id and a.caster == self:
                                                reaperDmgBoost = 0.1
                                            elif a.effect.id in [deterEff1.id,zelianR.id,fairyGardeEff.id]:
                                                lifeSavor.append(a)

                                    entityInArea.refreshEffects()
                                    vulnePower -= defenseUpPower
                                    vulnePower = max(vulnePower,-90)

                                    # Critical
                                    critRoll, critBonus, critDmgMul = random.randint(0,99), 0.15 * int(self.char.weapon.id in [ElitherScope.id]), 1
                                    critMsg, hasCrit = "", False
                                    critRate = int((self.agility+self.precision)/200*35)+self.critical
                                    if critRoll < critRate and damage > 0:
                                        if self.char.aspiration not in [POIDS_PLUME, OBSERVATEUR]:
                                            critMsg = " !"
                                            critDmgMul = 1.25 + critBonus
                                        else:
                                            critMsg = " !!"
                                            critDmgMul = (1.35 + critBonus)
                                        self.stats.crits += 1
                                        critMalusCmpt += 1
                                        critDmgMul += self.critDmgUp / 100
                                        hasCrit = True
                                    elif critRoll < critRate + pp and self.char.aspiration in [POIDS_PLUME,OBSERVATEUR] and damage > 0:
                                        critDmgMul = (1.45 + critBonus)
                                        critMsg = " !!!"
                                        self.specialVars["aspiSlot"] = 0
                                        self.stats.crits += 1
                                        critMalusCmpt += 1
                                        pp = 0
                                        critDmgMul += self.critDmgUp / 100
                                        hasCrit = True
                                    else:
                                        critDmgMul += self.dmgUp / 100

                                    blocked = False
                                    if random.randint(0,99) > 100-entityInArea.block :
                                        critMsg += " (Blocage !)"
                                        blocked = True

                                    secElemMul = 1
                                    if entityInArea.char.secElement == ELEMENT_LIGHT or (entityInArea.char.secElement == ELEMENT_SPACE and area != AREA_MONO) or (entityInArea.char.secElement == ELEMENT_TIME and area == AREA_MONO):
                                        secElemMul += 0.05
                                    if self.char.secElement == ELEMENT_LIGHT or (self.char.secElement == ELEMENT_SPACE and area != AREA_MONO) or (self.char.secElement == ELEMENT_TIME and area == AREA_MONO):
                                        secElemMul += 0.05
                                    if entityInArea.char.secElement == ELEMENT_DARKNESS:
                                        secElemMul -= 0.05
                                    if self.char.secElement == ELEMENT_DARKNESS:
                                        secElemMul -= 0.05

                                    effectiveDmg = round(damage*aoeFactor*secElemMul*critDmgMul)
                                    beforeDamageMul = copy.deepcopy(effectiveDmg)
                                    effectiveDmg, dephaReducedDmg = round(damage*aoeFactor*secElemMul*critDmgMul*(100+vulnePower)/100*(damageMul+reaperDmgBoost)),0
                                    blockDamage = int(effectiveDmg*0.35)

                                    if self.isNpc("Cl??mence pos.") and entityInArea.hp - effectiveDmg <= 0 and entityInArea.hp / entityInArea.maxHp >= 0.2:
                                        effectiveDmg = entityInArea.hp - int(entityInArea.maxHp * (random.randint(1,5)/100))

                                    if entityInArea.isNpc("Cl??mence Exalt??e"):
                                        effectiveDmg = min(effectiveDmg,int(entityInArea.maxHp/12))
                                    if blocked:
                                        effectiveDmg -= blockDamage
                                        entityInArea.stats.blockCount += 1
                                        entityInArea.stats.damageBlocks += blockDamage

                                    if isDepha:
                                        dephaReducedDmg = int(effectiveDmg * jetLagEff.power / 100)
                                        effectiveDmg -= dephaReducedDmg

                                    if execution:           # If the attack is a execution, the damage or equal to target's max hp for exploding the "damage receved" stat
                                        effectiveDmg = entityInArea.maxHp

                                    self.stats.shootHited += 1
                                    if entityInArea != self:
                                        self.stats.damageDeal += effectiveDmg
                                        entityInArea.stats.damageRecived += effectiveDmg
                                    else:
                                        self.stats.selfBurn += effectiveDmg

                                    sumDamage += effectiveDmg
                                    entityInArea.stats.numberAttacked += 1
                                    if not execution:
                                        if lifeSavor != []:
                                            for eff in lifeSavor:
                                                if entityInArea.hp - effectiveDmg <= 0:
                                                    healMsg, why = eff.caster.heal(entityInArea,eff.icon,None,eff.value,eff.name,mono=True)
                                                    popipo += healMsg
                                                    eff.decate(value=99999999)
                                                
                                        entityInArea.refreshEffects()
                                        entityInArea.hp -= effectiveDmg
                                    else:
                                        entityInArea.hp = 0

                                    if erosion != 0 and effectiveDmg > 0:
                                        lostHp = int(effectiveDmg * erosion/100)
                                        self.stats.maxHpReduced += lostHp
                                        entityInArea.maxHp -= lostHp

                                    # Damage bosted
                                    if use not in [None,HARMONIE] and not execution:
                                        for statBoost in self.effect:
                                            tstats = statBoost.allStats()

                                            if (tstats[use] != 0 or tstats[PERCING] != 0) and statBoost.caster != self: # If the stat was boosted by someone esle
                                                used = self.allStats()[use] - tstats[use]

                                                tempDmg = round(value * (used+100-self.actionStats()[useActionStats])/100 * (1-(min(95,entityInArea.resistance*(1-(self.percing-tstats[PERCING])/100))/100))*dangerMul*self.getElementalBonus(target=entityInArea,area=area,type=TYPE_DAMAGE)*(1+(0.01*self.level)))
                                                tempDmg = round(tempDmg*aoeFactor*critDmgMul*secElemMul*(100+vulnePower)/100*(damageMul+reaperDmgBoost))

                                                dif = effectiveDmg - tempDmg
                                                if dif > 0:
                                                    statBoost.caster.stats.damageBoosted += abs(dif)
                                                    self.stats.underBoost += abs(dif)
                                                else:
                                                    statBoost.caster.stats.damageDogded += abs(dif)

                                            elif statBoost.effect.id == dmgDown.id and beforeDamageMul-effectiveDmg > 0:
                                                statBoost.caster.stats.damageDogded += int(beforeDamageMul-effectiveDmg)
                                            elif statBoost.effect.id == dmgUp.id and beforeDamageMul-effectiveDmg < 0:
                                                statBoost.caster.stats.damageBoosted += int(beforeDamageMul-effectiveDmg)*-1
                                                entityInArea.stats.underBoost += int(beforeDamageMul-effectiveDmg)*-1

                                        for statBoost in entityInArea.effect:
                                            tstats = statBoost.allStats()
                                            if tstats[RESISTANCE] != 0 and statBoost.caster != self: # If the stat was boosted by someone esle
                                                used = self.allStats()[use]
                                                tempDmg = round(value * (used+100-self.actionStats()[useActionStats])/100 * (1-(min(95,(entityInArea.resistance-tstats[RESISTANCE])*(1-self.percing/100))/100))*dangerMul*self.getElementalBonus(target=entityInArea,area=area,type=TYPE_DAMAGE)*(1+(0.01*self.level)))
                                                tempDmg = round(tempDmg*aoeFactor*secElemMul*critDmgMul*(100+vulnePower)/100*(damageMul+reaperDmgBoost))
                                                dif = effectiveDmg - tempDmg
                                                if dif < 0:
                                                    statBoost.caster.stats.damageBoosted += abs(dif)
                                                    self.stats.underBoost += abs(dif)
                                                else:
                                                    statBoost.caster.stats.damageDogded += abs(dif)

                                            elif statBoost.effect.id == vulne.id and beforeDamageMul-effectiveDmg < 0:
                                                statBoost.caster.stats.damageBoosted += abs(beforeDamageMul-effectiveDmg)
                                                entityInArea.stats.underBoost += abs(beforeDamageMul-effectiveDmg)
                                            elif statBoost.effect.id == defenseUp.id and beforeDamageMul-effectiveDmg > 0:
                                                statBoost.caster.stats.damageDogded += abs(beforeDamageMul-effectiveDmg)

                                    # Damage message
                                    popipo += noneArmorMsg
                                    if not(execution):
                                        if effectiveDmg > 0 and tempToReturn == "":
                                            popipo += f"{self.icon} {icon} ??? {entityInArea.icon} -{separeUnit(effectiveDmg)} PV{critMsg}\n"
                                        else:
                                            popipo += tempToReturn + f" {entityInArea.icon} -{separeUnit(effectiveDmg)} PV{critMsg}\n"
                                    else:
                                        popipo += "{0} {2} ??? <:sacrified:973313400056725545> {1}\n".format(self.icon,entityInArea.icon,icon)

                                    if erosion != 0 and effectiveDmg > 0:
                                        popipo += f"{self.icon} {eroTxt} ??? {entityInArea.icon} -{lostHp} PV max\n"

                                    if entityInArea.hp <= 0:
                                        popipo += entityInArea.death(killer = self,trueDeath=execution)
                                        deathCount += 1
                                        if execution:
                                            entityInArea.status, entityInArea.icon = STATUS_TRUE_DEATH, ["","<:aillilKill1:898930720528011314>","<:ailillKill2:898930734063046666>","<:ailillKill2:898930734063046666>"][entityInArea.char.species]

                                    if isDepha:
                                        eff = copy.deepcopy(jetLagDmgEff)
                                        eff.power = dephaReducedDmg
                                        popipo += groupAddEffect(self, entityInArea, AREA_MONO, [eff], skillIcon=["<:jetLagB:984519444082610227>","<:jetLagR:984519461111472228>"][self.team])
                                    if effectOnHit != None and entityInArea == target and entityInArea.hp > 0:
                                        effectOnHit = findEffect(effectOnHit)
                                        popipo += add_effect(self,target,effectOnHit,skillIcon=icon)

                                        entityInArea.refreshEffects()

                                    if hasCrit:
                                        for jaugeEnt, jaugeEff in teamJaugeDict[self.team].items():
                                            if jaugeEnt == self and jaugeEnt.hp > 0 and jaugeEff.effect.id == pasTech.id:
                                                jaugeEff.value = min(jaugeEff.value+5,100)
                                            elif jaugeEff.effect.id == eventFas.id and jaugeEnt.hp > 0:
                                                jaugeEff.value += 10
                                                if jaugeEff.value >= 100:
                                                    popipo += add_effect(jaugeEnt,jaugeEnt,jaugeEff.effect.callOnTrigger,skillIcon=eventFas.emoji[0][0],setReplica=entityInArea)
                                                    jaugeEnt.refreshEffects()
                                                    for cpmt in range(len(jaugeEnt.cooldowns)):
                                                        tempi = findSkill(jaugeEnt.char.skills[cmpt])
                                                        if tempi != None and findSkill(jaugeEnt.char.skills[cmpt]).id == fascination.id:
                                                            jaugeEnt.cooldowns[cmpt] = 0
                                                    jaugeEff.value = 0

                                    # After damage
                                    if entityInArea.char.aspiration in [PROTECTEUR,VIGILANT,ENCHANTEUR] and self.id not in entityInArea.specialVars["aspiSlot"]:
                                        entityInArea.specialVars["aspiSlot"].append(self.id)

                                    elif self.char.aspiration == OBSERVATEUR:
                                        self.specialVars["aspiSlot"] += 3

                                    if entityInArea.isNpc("Liu") or (entityInArea.isNpc("Kitsune") and type(actTurn.char != classes.invoc)):
                                        popipo += add_effect(entityInArea,actTurn,charming,skillIcon = entityInArea.weapon.effect.emoji[0][0])
                                        actTurn.refreshEffects()
                                    if actTurn.isNpc("Liz") or (actTurn.isNpc("Kitsune") and type(entityInArea.char != classes.invoc) and ((skillToUse != None and skillToUse.id != kitsuneSkill4.id)or skillToUse == None)):

                                        popipo += add_effect(actTurn,entityInArea,charming,skillIcon = actTurn.weapon.effect.emoji[0][0])
                                        actTurn.refreshEffects()

                                    for eff in entityInArea.effect:
                                        if eff.effect.id in [lightAura2ActiveEff.id, tintabuleEff.id]:                                 # Aura de lumi??re 2
                                            sumHeal, sumEnt = 0,[]
                                            for ent in entityInArea.cell.getEntityOnArea(area=eff.effect.area,team=entityInArea.team,wanted=ALLIES,directTarget=False,fromCell=actTurn.cell):
                                                useless, tempi = eff.caster.heal(ent,eff.icon,eff.effect.stat,eff.effect.power,eff.effect.name,danger)
                                                if tempi > 0:
                                                    sumHeal += tempi
                                                    sumEnt.append(ent.icon)

                                            temp = ""
                                            for i in sumEnt:
                                                temp += i
                                            if len(sumEnt) > 0:
                                                popipo += "{0} {1} ??? {5} +{2} {3} PV ({4})\n".format(eff.caster.icon,eff.icon,["","???"][len(sumEnt)>1],int(sumHeal/len(sumEnt)),eff.effect.name, temp)
                                            popipo += eff.decate(value=1)
                                            entityInArea.refreshEffects()
                                        elif eff.effect.id == flambe.id and use in [STRENGTH,ENDURANCE,AGILITY,PRECISION]:                         # Flambage
                                            eff.effect.power += flambe.power
                                        elif eff.effect.id == magAch.id and use == [MAGIE,CHARISMA,INTELLIGENCE,HARMONIE]:                            # Magia
                                            eff.effect.power += magAch.power
                                        elif eff.effect.id == rosesPhysiEff.id and use == STRENGTH:
                                            popipo += eff.triggerDamage(value = damage,declancher=self,icon=icon,onArmor=onArmor)[1]
                                        elif eff.effect.id == rosesMagicEff.id and use == MAGIE:
                                            popipo += eff.triggerDamage(value = damage,declancher=self,icon=icon,onArmor=onArmor)[1]
                                        elif eff.effect.id in [haimaEffect.id,pandaimaEff.id]:
                                            finded = False
                                            for sndEff in entityInArea.effect:
                                                if sndEff.effect.id == eff.effect.callOnTrigger.id:
                                                    finded = True
                                                    break

                                            if not(finded):
                                                popipo += add_effect(eff.caster,entityInArea,eff.effect.callOnTrigger)
                                                popipo += eff.decate(value = 1)
                                                entityInArea.refreshEffects()
                                        elif eff.effect.id in [mattSkill4Eff.id,lightLameEff.id,astralLameEff.id,timeLameEff.id]:
                                            popipo += eff.triggerDamage(value = damage,declancher=self,icon=icon,onArmor=onArmor)[1]

                                else:
                                    popipo += f"{entityInArea.char.name} esquive l'attaque\n"
                                    entityInArea.stats.dodge += 1
                                    entityInArea.stats.numberAttacked += 1
                                    if entityInArea.char.aspiration == POIDS_PLUME:
                                        entityInArea.specialVars["aspiSlot"] += 3
                                    elif self.char.aspiration == OBSERVATEUR:
                                        self.specialVars["aspiSlot"] = int(self.specialVars["aspiSlot"] * 0.5)
                                    if entityInArea.isNpc("Lia") or (entityInArea.isNpc("Kitsune") and type(self.char) != classes.invoc):
                                        popipo += add_effect(entityInArea,actTurn,charming,skillIcon = entityInArea.weapon.effect.emoji[0][0])
                                        entityInArea.refreshEffects()

                    if sumDamage > 0:
                        sumLifeSteal, lifeStealEmote = 0, ""
                        for eff in self.effect:
                            if eff.effect.id == convertEff.id :                         # Convertion :
                                valueToAdd = int(sumDamage * (convertEff.power/100 * (1+(self.allStats()[convertEff.stat]/100))))
                                
                                alreadyHaveArmorEff = False
                                for eff2 in self.effect:
                                    if eff2.effect.id == convertArmor.id:
                                        alreadyHaveArmorEff = True
                                        eff2.value += valueToAdd
                                        popipo += "{0} ??? {1}{2} +{3} PV\n".format(eff2.caster.icon,eff2.icon,self.icon,valueToAdd)
                                        break

                                if not(alreadyHaveArmorEff):
                                    effect = convertArmor
                                    effect.overhealth = valueToAdd
                                    popipo += add_effect(eff.caster,self,effect,ignoreEndurance=True)
                                    
                                    self.refreshEffects()
                            elif eff.effect.id in [vampirismeEff.id,aliceExWeapEff.id,undeadEff2.id,holmgangEff.id]:
                                sumLifeSteal += eff.effect.power
                                lifeStealEmote += eff.icon
                        if self.char.aspiration == BERSERK:
                            sumLifeSteal += self.specialVars["aspiSlot"]
                            lifeStealEmote += aspiEmoji[BERSERK]
                        if lifeSteal > 0:
                            sumLifeSteal += lifeSteal
                            lifeStealEmote += icon
                        if self.isNpc("Cl??mence pos."):
                            sumLifeSteal += 33
                            lifeStealEmote += vampirismeEff.emoji[1][1]
                            self.specialVars["clemBloodJauge"].value = min(100,self.specialVars["clemBloodJauge"].value+int(sumDamage * (0.01*(1+self.level/100))))
                            if self.specialVars["clemMemCast"]:
                                self.specialVars["clemMemCast"] = False
                        elif self.isNpc("Cl??mence Exalt??e"):
                            sumLifeSteal += 20
                            lifeStealEmote += vampirismeEff.emoji[1][1]

                        if sumLifeSteal > 0:
                            healPowa = min(self.maxHp - self.hp, min(sumDamage * sumLifeSteal / 100,self.level*45*(1+lifeStealBonus/100)))
                            temp, useless = self.heal(self,lifeStealEmote,None,healPowa)
                            popipo += temp
                
                return popipo, deathCount

            def startOfTurn(self,tablEntTeam="tabl") -> str:
                """
                    The method to call when a entity start his turn.\n
                    Reduce the duration of all their own ``fightEffects`` and return a ``string`` with the effectives changes
                """
                toReturn = ""
                allReadySeen = []
                for a in self.effect:
                    # Any normals effects --------------------------------
                    if a.trigger == TRIGGER_START_OF_TURN and (not(a.effect.stackable) or a.effect.type != TYPE_INDIRECT_DAMAGE):
                        toReturn += a.triggerStartOfTurn(danger)

                    # Stackable indirect damages effects -----------------
                        # Those effects are temporary merge into one for don't spam the action's windows
                    elif a.trigger == TRIGGER_START_OF_TURN and a.effect.stackable and a.effect.type == TYPE_INDIRECT_DAMAGE and {a.caster.id:a.effect.id} not in allReadySeen :
                        primalPower,nbOfDecate = a.effect.power,0
                        for eff in self.effect:                 # Adding the power of all sames effects by the same caster to one to have one to rule them all
                            if eff.effect.id == a.effect.id and eff.caster.id == a.caster.id:
                                a.effect.power += eff.effect.power

                        a.effect.power -= primalPower           # Deducing the base power, 'cause we are at [NbEffect]+1 * power
                        toReturn += a.triggerStartOfTurn(danger,decate=False)
                        a.effect.power = primalPower
                        
                        for eff in self.effect:
                            if eff.effect.id == a.effect.id and eff.caster.id == a.caster.id:
                                temporaty = eff.decate(value=1)
                                if temporaty != "":
                                    nbOfDecate += 1

                        if nbOfDecate > 1:                      # Regrouping all the decate messages as well
                            toReturn += "__{0}__ ne subit plus sous {1} effets de __{2}__\n".format(self.char.name,nbOfDecate,a.effect.name)
                        elif nbOfDecate == 1:
                            toReturn += temporaty

                        allReadySeen.append({a.caster.id:a.effect.id})

                    elif a.effect.id == gwenCoupeEff.id:
                        if random.randint(0,99) < 15:
                            effect = intargetable
                            toReturn += add_effect(self,self,effect)

                    if a.effect.id == kikuRaiseEff.id and tour >= 16:
                        self.stats.lauthingAtTheFaceOfDeath = True
                
                    elif a.effect.id == clemUltShield.id:
                        a.decate(turn=99)
                        effect = copy.deepcopy(dmgUp)
                        effect.power, effect.turnInit = 50, 2
                        toReturn += add_effect(caster=self,target=self,effect=effect, start = a.name, danger=danger, skillIcon=a.icon)

                allReadySeenID, unAffected, effNames, allReadySeenCharId = [], [], [], []

                for dictElem in self.ownEffect[:]:
                    for on, eff in dictElem.items():
                        for effOn in on.effect:
                            if effOn.id == eff:
                                temp = effOn.decate(turn=1)
                                if temp != "" and effOn.effect.trigger != TRIGGER_ON_REMOVE:
                                    if effOn.effect.id not in allReadySeenID:
                                        allReadySeenID.append(effOn.effect.id)
                                        unAffected.append([on.icon])
                                        effNames.append(effOn.effect.name)
                                        allReadySeenCharId.append([on.id])
                                    else:
                                        for cmpt in range(len(allReadySeenID)):
                                            if allReadySeenID[cmpt] == effOn.effect.id and on.id not in allReadySeenCharId[cmpt]:
                                                unAffected[cmpt].append(on.icon)
                                                allReadySeenCharId[cmpt].append(on.id)
                                else:
                                    toReturn += temp

                                on.refreshEffects()
                                break

                ultimateTemp = ""

                for cmpt in range(len(allReadySeenID)):
                    tempLen = len(unAffected[cmpt])
                    if tempLen > 1:
                        for cmpt2 in range(tempLen):
                            ultimateTemp += unAffected[cmpt][cmpt2]
                        ultimateTemp += " ??? ~~{0}~~\n".format(effNames[cmpt])
                    elif tempLen == 1:
                        ultimateTemp += "{0} ??? ~~{1}~~\n".format(unAffected[cmpt][0],effNames[cmpt])

                toReturn += ultimateTemp

                for a in range(7):
                    if self.cooldowns[a] > 0:
                        self.cooldowns[a] -= 1

                for jaugeEnt, jaugeEff in teamJaugeDict[self.team].items():
                    if jaugeEnt == self: 
                        if jaugeEff.effect.id == pasTech.id:
                            jaugeEff.value = min(jaugeEff.value+15,100)
                        elif jaugeEff.effect.id == jaugeButLight.id:
                            jaugeEff.value = min(jaugeEff.value+10,100)

                if (self.isNpc("Luna ex.") or self.isNpc("Luna pr??.")) and self.specialVars["clemBloodJauge"] == None:
                    toRoll, roll = 20+(1-(actTurn.hp/actTurn.maxHp))*100, random.randint(0,99)
                    if roll < toRoll:
                        toReturn += add_effect(self,self,lunaQuickFightEff)

                self.refreshEffects()

                if self.isNpc("Jevil"):
                    nb = 1
                    if self.hp/self.maxHp < 0.5:
                        nb += 1
                    if self.hp/self.maxHp < 0.3:
                        nb += 1
                    cmpt = 0
                    while cmpt < nb:
                        effect = copy.deepcopy(chaosEff)

                        effect.power = [1,10,15,20,25,30][random.randint(0,5)]
                        randoma = random.randint(0,5)
                        effect.area = [AREA_CIRCLE_1,AREA_CONE_2,AREA_DIST_3,AREA_DONUT_2,AREA_LINE_2,AREA_MONO][randoma]
                        effect.name += " - {0}".format(["La croix","Le c??ne","L'anneau","Le cercle","La ligne","Le point"][randoma])

                        ent = tablEntTeam[0][random.randint(0,len(tablEntTeam[0])-1)]
                        if ent.hp > 0:
                            toReturn += add_effect(self,ent,effect)
                            ent.refreshEffects()
                            
                        cmpt += 1

                if self.char.weapon.id == astroGlobe.id and self.hp > 0:
                    temp = []
                    for ent in tablEntTeam[self.team]:
                        if ent.hp > 0 and type(ent.char) != invoc :
                            temp.append(ent)

                    if len(temp) > 0:
                        temp = temp[random.randint(0,len(temp)-1)]
                        toReturn += add_effect(self,temp,cardAspi[temp.char.aspiration]," ({0})".format(self.weapon.name),skillIcon = self.weapon.effect.emoji[0][0])
                        temp.refreshEffects()

                elif self.weapon.id == miltrilPlanisphere.id and self.hp > 0:
                    temp = []
                    for a in (0,1):
                        for b in tablEntTeam[a]:
                            if b.hp > 0:
                                temp.append(b)

                    if len(temp) > 1:
                        temp = temp[0]
                    else:
                        temp = random.randint(0,len(temp)-1)

                    toReturn += add_effect(self,temp,[miltrilPlanisftEffDebuff,miltrilPlanisftEffBuff][temp.team == self.team], " ({0})".format(self.weapon.name),skillIcon=self.weapon.effect.emoji[0][0])
                    temp.refreshEffects()
                return toReturn

            def endOfTurn(self,danger) -> str:
                """
                    The method to call when eff entity end their turn\n
                    Return eff ``string`` with all the correspondings actions
                """
                toReturn,allReadySeen  = "",[]
                for eff in self.effect:
                    if eff.trigger == TRIGGER_END_OF_TURN and (not(eff.effect.stackable) or eff.effect.type != TYPE_INDIRECT_DAMAGE):
                        toReturn += eff.triggerEndOfTurn(danger)

                    # Stackable indirect damages effects -----------------
                        # Those effects are temporary merge into one for don't spam the action's windows
                    elif eff.trigger == TRIGGER_END_OF_TURN and eff.effect.stackable and eff.effect.type == TYPE_INDIRECT_DAMAGE and {eff.caster.id:eff.effect.id} not in allReadySeen :
                        primalPower,nbOfDecate = eff.effect.power,0
                        for eff2 in self.effect:                 # Adding the power of all sames effects by the same caster to one to have one to rule them all
                            if eff2.effect.id == eff.effect.id and eff2.caster.id == eff.caster.id:
                                eff.effect.power += eff2.effect.power

                        eff.effect.power -= primalPower           # Deducing the base power, 'cause we are at [NbEffect]+1 * power
                        toReturn += eff.triggerEndOfTurn(danger,decate=False)
                        eff.effect.power = primalPower
                        
                        for eff2 in self.effect:
                            if eff2.effect.id == eff.effect.id and eff2.caster.id == eff.caster.id:
                                temporaty = eff.decate(value=1)
                                if temporaty != "":
                                    nbOfDecate += 1

                        if nbOfDecate > 1:                      # Regrouping all the decate messages as well
                            toReturn += "__{0}__ ne subit plus sous {1} effets de __{2}__\n".format(self.char.name,nbOfDecate,eff.effect.name)
                        elif nbOfDecate == 1:
                            toReturn += temporaty

                        allReadySeen.append({eff.caster.id:eff.effect.id})
                    
                    if eff.effect.id == tablWeapExp[0].id:
                        try:
                            if random.randint(0,99) < [20,100][optionChoice==OPTION_WEAPON]:
                                for eff2 in tablWeapExp:
                                    if eff.name == eff2.name:
                                        toReturn += add_effect(self,self,eff.effect.callOnTrigger,skillIcon=eff.icon)
                                        break
                        except:
                            print_exc()

                for skilly in self.char.skills:
                    if findSkill(skilly) != None and findSkill(skilly).id == horoscope.id:
                        tablHorEff = []
                        for eff in horoscopeEff:
                            tablHorEff.append(copy.deepcopy(eff[0]))
                        for eff in self.effect:
                            for toCompare in tablHorEff[:]:
                                if eff.effect.id == toCompare.id:
                                    tablHorEff.remove(toCompare)
                                    break
                        if len(tablHorEff) > 0:
                            if len(tablHorEff) == 1:
                                randy = 0
                            else:
                                randy = random.randint(0,len(tablHorEff)-1)
                            toReturn += add_effect(self,self,tablHorEff[randy],skillIcon=skilly.emoji)
                        self.refreshEffects()
                        break

                self.refreshEffects()
                if self.char.aspiration in [PROTECTEUR,VIGILANT,ENCHANTEUR]:
                    self.specialVars["aspiSlot"] = []

                if type(self.char) == invoc and not(self.char.name.startswith("Patte de The Giant Enemy Spider")):
                    self.leftTurnAlive -= 1
                    if self.leftTurnAlive <= 0:
                        self.hp = 0
                        toReturn += "\n{0} est d??sinvoqu??{1}".format(self.char.name,self.accord())
                return toReturn

            def atRange(self):
                """Return the entity in range of the main weapon"""
                atRangeVar = self.cell.getEntityOnArea(area=self.char.weapon.effectiveRange,team=self.team,wanted=self.char.weapon.target,lineOfSight= True,directTarget=True,ignoreInvoc=self.char.weapon.type==TYPE_HEAL,fromCell=self.cell)
                surrondingsEnnemis = self.cell.getEntityOnArea(area=self.char.weapon.effectiveRange,team=self.team,wanted=ENEMIES,directTarget=True,fromCell=self.cell)
                return atRangeVar

            def quickEffectIcons(self):
                temp = f"{self.icon} {self.char.name} : {separeUnit(self.hp)}/{separeUnit(self.maxHp)} "
                if self.effect != []:
                    allReadySeenIcon, allReadySeenNumber = [], []
                    temp += "("
                    for a in self.effect:
                        if a.effect.stackable and a.icon in allReadySeenIcon:
                            for cmpt in range(len(allReadySeenIcon)):
                                if allReadySeenIcon[cmpt] == a.icon:
                                    allReadySeenNumber[cmpt] += 1
                        elif a.effect.stackable and a.icon not in allReadySeenIcon:
                            allReadySeenIcon.append(a.icon)
                            allReadySeenNumber.append(1)
                        else:
                            temp += a.icon
                    if allReadySeenIcon != []:
                        for cmpt in range(len(allReadySeenIcon)):
                            if allReadySeenNumber[cmpt] > 1:
                                temp += "{0}x{1}".format(allReadySeenIcon[cmpt],allReadySeenNumber[cmpt])
                            else:
                                temp += allReadySeenIcon[cmpt]
                    temp += ")\n"
                else:
                    temp += "\n"

                return temp

            def lightQuickEffectIcons(self):
                if type(self.char) != octarien or (type(self.char) == octarien and not(self.char.oneVAll)):
                    temp = f"{self.icon} : "
                    stackableAlreaySeen = []
                    if self.effect != [] and self.status != STATUS_TRUE_DEATH:
                        for eff in self.effect:
                            if eff.effect.id == "giveup":
                                return f"{self.icon} : {eff.icon} {eff.effect.name}\n"

                        if self.status == STATUS_DEAD:
                            return f"{self.icon} : <:lostSoul:887853918665707621>\n"

                        for a in self.effect:
                            if a.effect.id == lunaInfiniteDarknessStun.id:
                                return f"{self.icon} : {a.icon} {a.effect.name}\n"

                            if (a.icon not in ['<:co:888746214999339068>','<:le:892372680777539594>','<:to:905169617163538442>','<:lo:887853918665707621>','<:co:895440308257558529>']+aspiEmoji) and not(a.effect.silent and a.effect.replica == None) and a.effect.id not in [lightAura2PassiveEff.id] and a.effect.jaugeValue == None:
                                if a.effect.replica != None or a.effect.stun:
                                    if a.effect.id != lunaInfiniteDarknessShield.id:
                                        return f"{self.icon} : {a.icon} {a.effect.name}\n"
                                    else:
                                        return f"{self.icon} : {a.icon} {a.effect.name} ({a.value})\n"

                                if a.effect.stackable and (a.effect.id not in stackableAlreaySeen):
                                    number = 0
                                    for ent in self.effect:
                                        if ent.effect.id == a.effect.id:
                                            number += 1
                                    if number > 1:
                                        if a.icon == '<:pa:930051729523879966>':
                                            temp += ['<:pt1:930051729523879966>','<:pt2:930534069576544256>','<:pt3:930534084432756738>','<:pt4:930534100324978708>','<:pt5:930534126640046118>'][number-1]
                                        else:
                                            temp += a.icon+f"({number})"
                                    else:
                                        temp += a.icon

                                    stackableAlreaySeen.append(a.effect.id)
                                elif not(a.effect.stackable):
                                    if not(a.effect.id == eventFas.id):
                                        temp += a.icon
                                        if a.effect.id in [flambe.id,magAch.id]:
                                            temp += "("+str(a.effect.power//flambe.power)+")"
                                    else:
                                        if a.value < 20:
                                            a.icon = '<:fas0:952539840157712454>'
                                        elif a.value < 40:
                                            a.icon = '<:fas20:952539890233528340>'
                                        elif a.value < 60:
                                            a.icon = '<:fas40:952539915843956796>'
                                        elif a.value < 80:
                                            a.icon = '<:fas60:952539943236935781>'
                                        else:
                                            a.icon = ["<a:fas80B:952540002011729921>","<a:fas80R:952539982680166460>"][self.team]
                                        temp += a.icon +"("+str(a.value)+")"

                        if temp != f"{self.icon} : ":
                            if self.invisible and "<:in:899788326691823656>" not in temp:
                                temp += "<:invisible:899788326691823656>"
                            if self.translucide and "<:tr:914232635176415283>" not in temp:
                                temp += "<:translucide:914232635176415283>"
                            if self.untargetable and "<:un:899610264998125589>" not in temp:
                                temp += "<:untargetable:899610264998125589>"
                            if self.immune and "<:im:914232617660981249>" not in temp:
                                temp += "<:immunite:914232617660981249>"

                            temp += "\n"
                            return temp
                        else:
                            return ""
                    else:
                        return ""
                else:
                    temp, temp2 = "{0} __{1}__ :\n({2} Pv /{3})\n".format(self.icon,self.char.name,separeUnit(self.hp),separeUnit(self.maxHp)), ""
                    stackableAlreaySeen, highlightEff = [], ""

                    for a in self.effect:
                        if (a.icon not in ['<:co:888746214999339068>','<:le:892372680777539594>','<:to:905169617163538442>','<:lo:887853918665707621>','<:co:895440308257558529>']+aspiEmoji) and not(a.effect.silent and a.effect.replica == None) and a.effect.id not in [lightAura2PassiveEff.id] and a.effect.jaugeValue == None:
                            if a.effect.replica != None or a.effect.stun:
                                if a.effect.id != lunaInfiniteDarknessShield.id:
                                    highlightEff += f"{a.icon} {a.effect.name}\n"
                                else:
                                    highlightEff+= f"{a.icon} {a.effect.name} ({a.value})\n"

                            elif a.effect.stackable and (a.effect.id not in stackableAlreaySeen):
                                number = 0
                                for ent in self.effect:
                                    if ent.effect.id == a.effect.id:
                                        number += 1
                                if number > 1:
                                    if a.icon == '<:pa:930051729523879966>':
                                        temp2 += ['<:pt1:930051729523879966>','<:pt2:930534069576544256>','<:pt3:930534084432756738>','<:pt4:930534100324978708>','<:pt5:930534126640046118>'][number-1]
                                    else:
                                        temp2 += a.icon+f"({number})"
                                else:
                                    temp2 += a.icon

                                stackableAlreaySeen.append(a.effect.id)
                            elif not(a.effect.stackable):
                                if not(a.effect.id == eventFas.id):
                                    temp2 += a.icon
                                    if a.effect.id in [flambe.id,magAch.id]:
                                        temp2 += "("+str(a.effect.power//flambe.power)+")"
                                else:
                                    if a.value < 20:
                                        a.icon = '<:fas0:952539840157712454>'
                                    elif a.value < 40:
                                        a.icon = '<:fas20:952539890233528340>'
                                    elif a.value < 60:
                                        a.icon = '<:fas40:952539915843956796>'
                                    elif a.value < 80:
                                        a.icon = '<:fas60:952539943236935781>'
                                    else:
                                        a.icon = ["<a:fas80B:952540002011729921>","<a:fas80R:952539982680166460>"][self.team]
                                    temp2 += a.icon +"("+str(a.value)+")"
                    if temp2 != "":
                        temp += highlightEff + temp2
                    else:
                        temp += "Aucun effet sur l'entit??"
                    return temp

            def accord(self):
                if self.char.gender == GENDER_FEMALE:
                    return "e"
                else:
                    return ""

            async def getIcon(self,bot):
                if type(self.char) == char:
                    self.icon = await getUserIcon(bot,self.char)
                else:
                    self.icon = self.char.icon
                return self.icon

            def getMedals(self,array):
                respond = ""
                tabl = [["<:topDpt:884337213670838282>","<:secondDPT:884337233241448478>","<:thirdDPT:884337256905732107>"],["<:topHealer:884337335410491394>","<:secondHealer:884337355262160937>","<:thirdHealer:884337368407093278>"],["<:topArmor:884337281547272263>","<:secondArmor:884337300975276073>","<:trdArmor:911071978163675156>"],["<:topSupp:911071783787065375>","<:sndSupp:911071803424788580>","<:trdSupp:911071819388313630>"]]
                for z in range(0,len(array)):
                    for a in (0,1,2,3):
                        try:
                            if self == array[z][a]:
                                respond+=tabl[z][a]
                                self.medals[a] += 1
                        except:
                            pass

                if respond != "":
                    return " ("+respond+")"
                else:
                    return ""

            def summon(self,summon : invoc ,timeline, cell : cell, tablEntTeam : list,tablAliveInvoc : list, ignoreLimite=False,dictInteraction:dict=None):
                funnyTempVarName = ""
                summon = copy.deepcopy(summon)
                team = self.team
                summon.color = self.char.color
                if tablAliveInvoc[team] < 3 or ignoreLimite:
                    sumEnt = entity(self.id,summon,team,False,summoner=self,dictInteraction=dictInteraction)
                    sumEnt.move(cellToMove=cell)
                    tablEntTeam[self.team].append(sumEnt)

                    if summon.name.startswith("Patte de The Giant Enemy Spider"):
                        add_effect(self,sumEnt,GESredirect)

                    if sumEnt.aspiration == POIDS_PLUME:
                        add_effect(sumEnt,sumEnt,poidPlumeEff)

                    elif sumEnt.aspiration == OBSERVATEUR:
                        add_effect(sumEnt,sumEnt,obsEff)

                    sumEnt.refreshEffects()

                    if self.id != timeline.timeline[0].id:
                        found = False
                        for cmpt in range(len(timeline.timeline)):
                            if self.id == timeline.timeline[cmpt].id and type(timeline.timeline[cmpt].char) != invoc:
                                whereToInsert = cmpt+1
                                break
                    else:
                        whereToInsert = 1

                    timeline.timeline.insert(whereToInsert,sumEnt)

                    accord = ""
                    if summon.gender == GENDER_FEMALE:
                        accord="e"
                    funnyTempVarName = f"{self.char.name} invoque un{accord} {summon.name}"
                    tablAliveInvoc[team] += 1
                    return tablEntTeam,tablAliveInvoc,timeline,funnyTempVarName

            def getElementalBonus(self,target,area : int,type : int):
                """Return the elemental damage bonus"""
                if type not in [TYPE_HEAL,TYPE_INDIRECT_HEAL,TYPE_ARMOR,TYPE_INDIRECT_DAMAGE]:
                    if self.char.element in [ELEMENT_FIRE, ELEMENT_UNIVERSALIS_PREMO] and area != AREA_MONO and self.cell.distance(target.cell) > 2:
                        return 1.1
                    elif self.char.element in [ELEMENT_WATER, ELEMENT_UNIVERSALIS_PREMO] and area == AREA_MONO and self.cell.distance(target.cell) > 2:
                        return 1.1
                    elif self.char.element in [ELEMENT_AIR, ELEMENT_UNIVERSALIS_PREMO] and area != AREA_MONO and self.cell.distance(target.cell) <= 2:
                        return 1.1
                    elif self.char.element in [ELEMENT_EARTH, ELEMENT_UNIVERSALIS_PREMO] and area == AREA_MONO and self.cell.distance(target.cell) <= 2:
                        return 1.1
                elif type in [TYPE_HEAL,TYPE_INDIRECT_HEAL,TYPE_ARMOR] and self.char.element == ELEMENT_LIGHT:
                    return 1.1
                elif type == TYPE_INDIRECT_DAMAGE and self.char.element == ELEMENT_DARKNESS:
                    return 1.1

                return 1

            async def resurect(self,target,value : int, icon : str,danger=danger):
                if tour <= 20:
                    if self.team == 1:
                        value = int(value * (danger/100))
                    value = min(value,target.maxHp)
                    self.stats.allieResurected += 1
                    self.stats.heals += value
                    target.hp = value
                    target.status = STATUS_RESURECTED
                    if type(target.char) != char:
                        target.icon = target.char.icon
                    else:
                        target.icon = await getUserIcon(bot,target.char)

                    add_effect(self,target,onceButNotTwice)

                    for eff in target.effect:
                        if eff.effect.id == lostSoul.id:
                            eff.decate(turn=99)

                    target.refreshEffects()

                    shieldValue, raiseShieldEmoji = int(target.maxHp*0.2), ['<:naB:908490062826725407>','<:naR:908490081545879673>'][target.team]
                    rep = f"{self.icon} {icon} ??? <:renisurection:873723658315644938> {raiseShieldEmoji} +{shieldValue} PAr, {target.icon} +{value} PV\n"

                    if target.char.says.onResurect != None:
                        try:
                            rep += "{0} : *\"{1}\"*\n".format(target.icon,target.char.says.onResurect.format(target=self.char.name,caster=target.char.name))
                        except:
                            rep += "__Error whith the onResurect message__\n"
                            log = format_exc()
                            if len(log) > 50:
                                rep += "{0}\n".format(log[-50:])
                            else:
                                rep += "{0}\n".format(log)

                    target.raiser = self.icon

                    # Recent Rez shield
                    notDeadYet = classes.effect("R??surection r??cente","susRez",overhealth=int(target.maxHp*0.2),turnInit=3,absolutShield=True,emoji=sameSpeciesEmoji('<:naB:908490062826725407>','<:naR:908490081545879673>'))
                    add_effect(self,target,notDeadYet,ignoreEndurance=True)
                    if target.isNpc("Akira"):
                        mater = classes.effect("Rage Inhumaine","Akiki",strength=int(target.char.level*1.5),turnInit=-1,emoji="<a:menacing:917007335220711434>",stackable=True)
                        rep += add_effect(target,target,mater)
                    target.refreshEffects()
                    ressurected[target.team].append(target)

                    return rep
                else:
                    return ""

            def getAggroValue(self,target):
                """Return the aggro value agains the target. Made for be use as a key for sort lists"""
                if not(target.untargetable):
                    aggro = [20,0][type(target.char)==invoc]                                          # Base aggro value. Maybe some skills will influe on it later
                    if target.char.weapon.id == grav.id:
                        aggro += self.stats.survival

                    for eff in target.effect:                           # Change the aggro
                        aggro += eff.effect.aggro

                        if eff.effect.replica != None:
                            aggro += 25
                            break

                    distance = self.cell.distance(target.cell)          # Distance factor.
                    aggro += 40-max(distance*10,40)                     # The closer the target, the greater the aggro will be.

                    if target.char.aspiration in [BERSERK,POIDS_PLUME,ENCHANTEUR,PROTECTEUR]:       # The tanks aspirations generate more aggro than the others
                        aggro += 15

                    aggro += target.stats.damageDeal//500*5             # The more the target have deals damage, the mort aggro he will generate
                    aggro += target.stats.heals//500*5                  # The more the target have deals heals, the mort aggro he will generate
                    aggro += target.stats.shieldGived//1000*5            # The more the target have gave armor, the mort aggro he will generate

                    if self.isNpc("Luna ex."): 
                        if target.char.element == ELEMENT_DARKNESS:
                            aggro = aggro * 1.1
                        if target.char.element == ELEMENT_LIGHT or target.char.secElement in [ELEMENT_DARKNESS,ELEMENT_LIGHT]:
                            aggro = aggro * 1.05
                    elif self.isNpc("Kiku") and target.status == STATUS_ALIVE:
                        aggro = aggro * 1.2

                    return int(aggro)
                else:
                    return -111

            def heal(self,target, icon : str, statUse : Union[int,None], power : int, effName = None,danger=danger, mono = False, useActionStats = ACT_HEAL):
                overheath, aff, toReturn, healPowa, critMsg, diing, healBuffer, statUsed = 0, target.hp < target.maxHp, "", 0, "", None, {"total":0}, copy.deepcopy(statUse)
                if power > 0 and target.hp > 0:
                    if useActionStats == None:
                        useActionStats = ACT_HEAL
                    if statUse not in [None,FIXE]:
                        if statUse == HARMONIE:
                            temp, selfStats = 0, self.allStats()
                            for cmpt in range(len(selfStats)):
                                if selfStats[cmpt] > temp:
                                    temp = selfStats[cmpt]
                                    statUsed = cmpt
                            statUse = temp

                        else:
                            statUse = self.allStats()[statUse]

                        dangerBoost = 1
                        if self.team == 1:
                            dangerBoost = danger/100

                        secElemMul = 1
                        if self.char.secElement in [ELEMENT_FIRE, ELEMENT_UNIVERSALIS_PREMO]:
                            secElemMul += 0.05
                        elif self.char.secElement in [ELEMENT_WATER, ELEMENT_UNIVERSALIS_PREMO]:
                            secElemMul -= 0.05
                        if target.char.secElement in [ELEMENT_FIRE, ELEMENT_UNIVERSALIS_PREMO]:
                            secElemMul += 0.05
                        elif target.char.secElement in [ELEMENT_WATER, ELEMENT_UNIVERSALIS_PREMO]:
                            secElemMul -= 0.05

                        healPowa = round(power * secElemMul * (1+(max(-65,statUse-self.actionStats()[useActionStats]))/100+(target.endurance/1000))* self.valueBoost(target = target,heal=True)*self.getElementalBonus(target,area = AREA_MONO,type = TYPE_HEAL) * dangerBoost)

                        if random.randint(0,99) < self.calHealCrit(target) * 100:
                            healPowa = int(healPowa) * (1.25 + (preciChiEff.power * int(self.specialVars["preci"]) + ironHealthEff.power * int(target.specialVars["ironHealth"])) * 0.01)
                            critMsg = " !"
                            self.stats.critHeal += 1
                        self.stats.nbHeal += 1
                        healPowaInit = copy.deepcopy(healPowa)

                        incurableValue, healBonus, attIncurPower = 0, 1+(5/100*int(not(self.auto))), 0
                        for eff in target.effect:
                            if eff.effect.id == incurable.id:
                                incurableValue = max(incurableValue,eff.effect.power)
                            elif eff.effect.id == undeadEff2.id:
                                healBonus += eff.effect.power/100
                                diing = eff
                            elif eff.effect.id == healReciveReductionTmp:
                                healBonus -= healReciveReductionTmp.power/100
                            elif eff.effect.type == TYPE_INDIRECT_DAMAGE and eff.caster.char.aspiration == ATTENTIF:
                                attIncurPower += eff.effect.power
                            elif eff.effect.id in [absEff.id,holmgangEff.id]:
                                healBonus += eff.effect.power/100
                                finded = False
                                for key in healBuffer:
                                    if key == eff.caster:
                                        healBuffer[key][0] += eff.effect.power
                                        finded = True
                                        break
                                if not(finded):
                                    healBuffer[eff.caster] = [eff.effect.power,0]
                                healBuffer["total"] += eff.effect.power
                        for eff in self.effect:
                            if eff.effect.id == healReductionTmp.id:
                                healBonus -= healReductionTmp.power/100
                            elif eff.effect.id == healDoneBonus.id:
                                healBonus += healReductionTmp.power/100
                            if eff.effect.allStats()[statUsed] > 0:
                                diff = round(power * secElemMul * (1+(max(-65,(statUse-eff.effect.allStats()[statUsed])-self.actionStats()[useActionStats]))/100+(target.endurance/1000))* self.valueBoost(target = target,heal=True)*self.getElementalBonus(target,area = AREA_MONO,type = TYPE_HEAL) * dangerBoost)
                                finded = False
                                for key in healBuffer:
                                    if key == eff.caster:
                                        healBuffer[key][1] += round(diff/healPowaInit*100)
                                        finded = True
                                        break
                                if not(finded):
                                    healBuffer[eff.caster] = [0,eff.effect.power]

                        healBonus -= (incurableValue/100 + min(attIncurPower/1000,0.3))
                        healBonus = max(healBonus,0.1)

                        healPowa = int(healPowa * (100-target.healResist)/100 * (1 + HEALBONUSPERLEVEL*self.level) * healBonus)
                        overheath = max(0,healPowa - (target.maxHp-target.hp))
                        healPowa = min(target.maxHp-target.hp,healPowa)

                        for ent in healBuffer:
                            if ent != "total":
                                ent.stats.healIncreased += int(healPowa*(100-target.healResist)/100*(1 + 0.004*self.level)-healPowaInit*(100-target.healResist)/100*(1 + 0.004*self.level)*healBuffer[ent][0]/100) + int(healPowaInit*(1 + 0.004*self.level)*healBuffer[ent][1]/100)

                        if type(self.char) != octarien:
                            target.healResist += int(healPowa/target.maxHp/2.5*100*(1+0.2*int(haveMultipleHealers[team])))
                        else:
                            target.healResist += int(healPowa/target.maxHp/1.5*100)

                        if self.isNpc("Alice Exalt??e"):
                            self.specialVars["clemBloodJauge"].value = min(100,self.specialVars["clemBloodJauge"].value+int(healPowa * 0.035))
                    else:
                        incurableValue = 0
                        for eff in target.effect:
                            if eff.effect.id == incurable.id:
                                incurableValue = max(incurableValue,eff.effect.power)
                            elif eff.effect.id == undeadEff2.id:
                                diing = eff

                        healPowa = int(power*(100-incurableValue)/100)
                        healPowaInit = copy.deepcopy(healPowa)

                        if type(self.char) != octarien:
                            target.healResist += int(healPowa/target.maxHp/2.5*100)
                        else:
                            target.healResist += int(healPowa/target.maxHp/1.5*100)

                    self.stats.heals += healPowa
                    target.hp += healPowa
                    if diing != None:
                        toReturn += diing.decate(value=healPowa)
                        target.refreshEffects()

                    add = ""
                    if effName != None:
                        add = " ({0})".format(effName)

                    if healPowa > 0:
                        toReturn = f"{self.icon} {icon} ??? {target.icon} +{separeUnit(healPowa)} PV{critMsg}\n"

                        try:
                            if teamJaugeDict[self.team][self].effect.id == uberJauge.id:
                                teamJaugeDict[self.team][self].value = min(100,teamJaugeDict[self.team][self].value+healPowa//([THEALNEEDEDFORUBER,TINDHNEEDFORUBER][actTurn!=self]/100))
                        except KeyError:
                            pass

                    if self.char.aspiration in [IDOLE,VIGILANT,ALTRUISTE] and overheath > 0:
                        tabli,tabla = [idoOHArmor,proOHArmor,altOHArmor],[self.specialVars["ohIdo"],self.specialVars["ohPro"],self.specialVars["ohAlt"]]
                        for carillon in (0,1,2):
                            if tabla[carillon]:
                                effect = tabli[carillon]
                                effect.overhealth = int(overheath * ([idoOHEff.power,proOHEff.power,altOHEff.power][carillon]/100))
                                toReturn += add_effect(self,target,effect,[idoOHEff.name,proOHEff.name,altOHEff.name][carillon],True)
                                target.refreshEffects()
                                return toReturn, 0

                    if self.isNpc("Lio") or (self.isNpc("Kitsune") and type(target.char != classes.invoc)):
                        toReturn += add_effect(self,target,charming2,self.char.weapon.effect.emoji[0][0],skillIcon=self.char.weapon.effect.emoji[0][0])
                        target.refreshEffects()

                    for eff in target.effect:
                        if eff.effect.id == shareTabl[0].id and mono:
                            entEmList = ""
                            for ent in target.cell.getEntityOnArea(area=eff.effect.area,team=target.team,wanted=ALLIES,directTarget=False,fromCell=actTurn.cell):
                                tempHeal = int(min(ent.maxHp-ent.hp,healPowa*eff.effect.power/100))
                                eff.caster.stats.heals += tempHeal
                                ent.hp += tempHeal
                                add = " (Partage)"
                                if tempHeal > 0:
                                    entEmList += ent.icon
                            if entEmList != "":
                                toReturn += f"{eff.caster.icon} {eff.icon} ??? {entEmList} +{int(healPowa*eff.effect.power/100)} PV{add}\n"
                        elif eff.effect.id == zelianR.id:
                            eff.value += int(healPowa * eff.effect.power / 100)

                if aff:
                    return toReturn, healPowa
                else:
                    return "", healPowa

            def isNpc(self, name : str) -> bool:
                """Return if the entity is a temp's with the name given"""
                return self.char.isNpc(name)

            def getCellToMove(self):
                tablOfEnt = self.cell.getEntityOnArea(area=AREA_ALL_ENEMIES-int(self.char.weapon.target==ALLIES),team=self.team,wanted=self.char.weapon.target,lineOfSight=self.char.weapon.target==ENEMIES,fromCell=actTurn.cell,ignoreInvoc = True,directTarget=True)
                if len(tablOfEnt) == 0:
                    return None
                surrondings = self.cell.surrondings()
                canMove = [surrondings[0] != None and surrondings[0].on == None, surrondings[1] != None and surrondings[1].on == None, surrondings[2] != None and surrondings[2].on == None, surrondings[3] != None and surrondings[3].on == None]

                tablOfEnt.sort(key=lambda ent:self.cell.distance(ent.cell))
            
                if self.cell.x - tablOfEnt[0].cell.x > 0 and canMove[0]:                # If the target is forward and we can move forward
                    return surrondings[0]
                elif self.cell.x - tablOfEnt[0].cell.x < 0 and canMove[1]:              # Elif the target is behind and we can move behind
                    return surrondings[1]
                elif self.cell.y - tablOfEnt[0].cell.y > 0 and canMove[2]:              # Elif the target is above and we can move up
                    return surrondings[2]
                elif self.cell.y - tablOfEnt[0].cell.y < 0 and canMove[3]:              # Elif the target is under and we can move down
                    return surrondings[3]
                else:
                    if canMove[2]:                                                      # Else, if we can move up, go up
                        return surrondings[2]
                    elif canMove[3]:                                                    # Else, if we can move down, go down
                        return surrondings[3]

                    else:
                        return None                                                     # Else, give up

            def knockback(self, target, power:int):
                toReturn = ""
                if target.chained:
                    return toReturn
                cellDif, axis = (self.cell.x - target.cell.x, self.cell.y - target.cell.y), getDirection(target.cell,self.cell)

                posArea = []
                for cellule in tablAllCells:
                    temp = (target.cell.x - cellule.x, target.cell.y - cellule.y)
                    if (temp[0] == 0 or temp[1] == 0) and (temp[0] != temp[1]):
                        temp2 = [temp[0] < 0, temp[0] > 0, temp[1] < 0, temp[1] > 0]
                        tablLineTeamGround = [FROM_LEFT,FROM_RIGHT,FROM_UP,FROM_DOWN]
                        for cmpt in (0,1,2,3):
                            if temp2[cmpt] and axis == tablLineTeamGround[cmpt] and target.cell.distance(cellule) <= power:
                                posArea.append(cellule)
                                break

                if len(posArea) > 0:
                    posArea.sort(key=lambda dist:target.cell.distance(dist))

                cmpt = 0
                cellToPush = target.cell
                while cmpt < len(posArea) and posArea[cmpt].on == None:
                    cellToPush = posArea[cmpt]
                    cmpt += 1

                initTagetCell = target.cell
                if cellToPush != target.cell:
                    target.move(cellToMove=cellToPush)
                toReturn = "__{0} ({1})__ est repouss??{3} de {2} case{4} en arri??re\n".format(target.char.name,target.icon,power,target.accord(),["","s"][int(power>1)])

                if cmpt < power:
                    lastingPower = power-initTagetCell.distance(cellToPush)

                    stat,damageBase = -100,10*lastingPower

                    for stats in self.allStats():
                        if not(type(self.char) == octarien and self.char.oneVAll and stats == self.allStats()[ENDURANCE]):
                            stat = max(stats,stat)

                    badaboum = [target]
                    if cmpt < len(posArea) and posArea[cmpt].on != None:
                        badaboum.append(posArea[cmpt].on)
                    for boom in badaboum:
                        damage = indirectDmgCalculator(self,boom,damageBase,HARMONIE,[100,danger][self.team==1],AREA_MONO)
                        toReturn += self.indirectAttack(boom,value=damage,name="Collision")

                return toReturn

            def jumpBack(self, power:int, fromCell:cell):
                toReturn = ""
                if self.chained:
                    return toReturn

                cellDif, axis = (self.cell.x - fromCell.x, self.cell.y - fromCell.y), getDirection(fromCell,self.cell)
                posArea = []
                for cellule in tablAllCells:
                    temp = (fromCell.x - cellule.x, fromCell.y - cellule.y)
                    if (temp[0] == 0 or temp[1] == 0) and (temp[0] != temp[1]):
                        temp2 = [temp[0] < 0, temp[0] > 0, temp[1] < 0, temp[1] > 0]
                        tablLineTeamGround = [FROM_RIGHT,FROM_LEFT,FROM_DOWN,FROM_UP]
                        for cmpt in (0,1,2,3):
                            if temp2[cmpt] and axis == tablLineTeamGround[cmpt] and fromCell.distance(cellule) <= power:
                                posArea.append(cellule)
                                break

                if len(posArea) > 0:
                    posArea.sort(key=lambda dist:self.cell.distance(dist))

                cmpt = 0
                cellToPush = self.cell
                while cmpt < len(posArea) and posArea[cmpt].on == None:
                    cellToPush = posArea[cmpt]
                    cmpt += 1

                initTagetCell = self.cell
                if cellToPush != self.cell:
                    self.move(cellToMove=cellToPush)
                toReturn = "\n__{0} ({1})__ saute de {2} case{4} en arri??re\n".format(self.char.name,self.icon,power,self.accord(),["","s"][int(power>1)])

                return toReturn

            def pull(self, target, power:int):
                toReturn = ""
                if target.chained:
                    return toReturn
                cellDif, axis = (self.cell.x - target.cell.x, self.cell.y - target.cell.y), getDirection(target.cell,self.cell)

                posArea = []
                for cellule in tablAllCells:
                    temp = (target.cell.x - cellule.x, target.cell.y - cellule.y)
                    if (temp[0] == 0 or temp[1] == 0) and (temp[0] != temp[1]):
                        temp2 = [temp[0] > 0, temp[0] < 0, temp[1] > 0, temp[1] < 0]
                        tablLineTeamGround = [FROM_LEFT,FROM_RIGHT,FROM_UP,FROM_DOWN]
                        for cmpt in (0,1,2,3):
                            if temp2[cmpt] and axis == tablLineTeamGround[cmpt] and target.cell.distance(cellule) <= power:
                                posArea.append(cellule)
                                break

                if len(posArea) > 0:
                    posArea.sort(key=lambda dist:target.cell.distance(dist))

                cmpt = 0
                cellToPush = target.cell
                while cmpt < len(posArea) and posArea[cmpt].on == None:
                    cellToPush = posArea[cmpt]
                    cmpt += 1

                initTagetCell = target.cell
                if cellToPush != target.cell:
                    target.move(cellToMove=cellToPush)
                if cmpt > 0:
                    toReturn = "\n__{0} ({1})__ est attir??{3} vers {4}\n".format(target.char.name,target.icon,power,target.accord(),self.char.name)

                return toReturn

            def quickEvent(self, stat:int, required:int,danger:int=100, effIfFail: classes.effect = None, fromEnt=None):
                toReturn = "\n__Maneuvre Critique !__"

                required = required*0.2 + (required*0.8/50*self.char.level)
                sussessTaux = min(1000,1000 * (self.allStats()[stat]/required))

                if random.randint(0,999) < sussessTaux:
                    toReturn += "\n{0} a r??ussi sa maneuvre critique !".format(self.char.name)
                    return toReturn, True
                else:
                    toReturn += "\n{0} a ??chou?? sa maneuvre critique...\n".format(self.char.name)
                    if effIfFail != None:
                        toReturn += add_effect(fromEnt,self,effIfFail,danger=danger)
                        self.refreshEffects()
                        return toReturn, False

            def actionStats(self):
                return [self.negativeHeal, self.negativeBoost, self.negativeShield, self.negativeDirect, self.negativeIndirect]

            def calHealCrit(self,target):
                """Return the crit rate (on 1), for a crit shield or heal"""
                bonus = (preciChiEff.power * int(self.specialVars["preci"]) + ironHealthEff.power * int(target.specialVars["ironHealth"])) * 0.01
                return self.precision * 0.002 + self.critical * 0.01 + target.endurance * 0.001 + bonus

        class fightEffect:
            """Classe plus pous??e que Effect pour le combat"""
            def __init__(self,id,effect : classes.effect, caster : entity, on : entity, turnLeft : int, trigger : int, type : int, icon : str, value=1, effReducPurcent:Union[None,int]=None):
                """self.id : int -> Id de l'effet
                self.effect : effect -> L'effet de base
                self.caster : entity -> L'entit?? qui donne l'effet
                self.on : entity -> L'entit?? sur laquel se trouve cet effet
                self.turnLeft : int -> Nombre de tour restant ?? l'effet
                self.trigger : const -> L'??v??nement qui d??clanche l'effet
                self.icon : str -> L'id de l'emoji correspondant ?? l'effet"""
                self.effect: classes.effect = copy.deepcopy(effect)

                if effReducPurcent != None:
                    self.effect.power = int(self.effect.power*effReducPurcent/100)
                else:
                    effReducPurcent = 100
                self.caster:entity = caster
                self.on:entity = on
                self.turnLeft = turnLeft
                self.trigger = trigger
                self.type = type
                if value != 1:
                    self.value = value
                else:
                    self.value = [1,0][self.effect.unclearable]

                if self.effect.id == deterEff1.id:
                    self.value = int(on.maxHp * self.effect.power / 100)

                self.id = id
                self.icon = icon
                self.remove = False
                self.stun:bool = effect.stun
                self.name = effect.name
                self.replicaTarget: Union[None,entity] = None

                tablTemp = [0,0,0,0,0,0,0,0,0]

                if self.caster.char.element == ELEMENT_TIME and self.effect.type == TYPE_INDIRECT_HEAL:
                    self.effect.power = int(self.effect.power*1.2)

                if self.effect.stat != None:
                    if self.effect.stat is not HARMONIE:
                        temp = self.caster.allStats()[self.effect.stat]
                    else:
                        temp = -111
                        for a in self.caster.allStats():
                            temp = max(temp,a)

                    valueBoost, valueResis = (1 + min(self.caster.char.level,200)//10/10 - 1 + caster.valueBoost(on)) * (temp+100-self.caster.negativeBoost)/100, caster.valueBoost(on) * (temp+100-self.caster.negativeShield)/100

                else:
                    valueBoost, valueResis = 1, 1

                secElemMul = 0

                if caster.char.secElement in [ELEMENT_AIR, ELEMENT_UNIVERSALIS_PREMO]:
                    secElemMul += 0.05
                if on.char.secElement in [ELEMENT_AIR, ELEMENT_UNIVERSALIS_PREMO]:
                    secElemMul += 0.05

                if caster.char.element in [ELEMENT_SPACE]:
                    secElemMul += 0.1
                elif on.char.element in [ELEMENT_SPACE] and caster.team == on.team:
                    secElemMul += 0.05
                elif on.char.element in [ELEMENT_SPACE] and caster.team != on.team:
                    secElemMul -= 0.05

                valueBoost += secElemMul

                tablTemp[0] += self.effect.strength * valueBoost * effReducPurcent * 0.01
                tablTemp[1] += self.effect.endurance * valueBoost * effReducPurcent * 0.01
                tablTemp[2] += self.effect.charisma * valueBoost * effReducPurcent * 0.01
                tablTemp[3] += self.effect.agility * valueBoost * effReducPurcent * 0.01
                tablTemp[4] += self.effect.precision * valueBoost * effReducPurcent * 0.01
                tablTemp[5] += self.effect.intelligence * valueBoost * effReducPurcent * 0.01
                tablTemp[6] += self.effect.resistance * valueBoost * effReducPurcent * 0.01
                tablTemp[7] += self.effect.percing * valueBoost * effReducPurcent * 0.01
                tablTemp[8] += self.effect.critical * valueBoost * effReducPurcent * 0.01

                for cmpt in range(8):
                    tablTemp[cmpt] = [min(tablTemp[cmpt],0),max(tablTemp[cmpt],0)][self.effect.type == TYPE_BOOST]

                self.inkResistance = min(effect.inkResistance * valueResis,effect.inkResistance*3)

                self.tablAllStats = tablTemp
                self.strength,self.endurance,self.charisma,self.agility,self.precision,self.intelligence,self.resistance,self.percing,self.critical = tuple(tablTemp)

                if self.effect.id in [vulne.id,dmgDown.id,dmgUp.id,defenseUp.id] and self.effect.stat != None:
                    power = self.effect.power
                    secElemMul = 1
                    if caster.char.secElement in [ELEMENT_AIR, ELEMENT_UNIVERSALIS_PREMO]:
                        secElemMul += 0.05
                    if on.char.secElement in [ELEMENT_AIR, ELEMENT_UNIVERSALIS_PREMO]:
                        secElemMul += 0.05
                    self.effect.power = min(power * (100+caster.allStats()[self.effect.stat]-caster.negativeBoost)/100 * (self.caster.char.level//10/10 - 1 + caster.valueBoost(on)), power * 10)
                elif self.effect.id in [vampirismeEff.id] and self.effect.stat != None:
                    power = self.effect.power
                    secElemMul = 1
                    if caster.char.secElement in [ELEMENT_FIRE, ELEMENT_UNIVERSALIS_PREMO]:
                        secElemMul += 0.05
                    if on.char.secElement in [ELEMENT_WATER, ELEMENT_UNIVERSALIS_PREMO]:
                        secElemMul += 0.05
                    if self.effect.stat == HARMONIE:
                        maxStats = max(caster.allStats())
                    else:
                        maxStats = caster.allStats()[self.effect.stat]
                    self.effect.power = power * (100+maxStats-caster.negativeHeal)/100 * (1 + caster.valueBoost(on,heal=True))

            def decate(self,turn=0,value=0) -> str:
                """R??duit le turnLeft ou value de l'effet"""
                self.turnLeft -= turn
                self.value -= value
                temp = ""

                if (self.turnLeft <= 0 and self.effect.turnInit > 0) or self.value <= 0 and not(self.effect.unclearable):
                    if self.trigger == TRIGGER_ON_REMOVE:
                        temp += self.triggerRemove()
                    self.remove = True
                    if not(self.effect.silent) and self.on.hp > 0 and self.effect.id not in (astralShield.id,timeShield.id):
                        temp += f"__{self.on.char.name}__ n'est plus sous l'effet __{self.effect.name}__\n"

                    if self.effect.id == undeadEff2.id and self.turnLeft == 0:
                        self.on.hp = 0
                        temp += self.on.death(killer=self.on)
                    elif self.effect.id == elemShieldEff.id and self.value <= 0:
                        temp += groupAddEffect(self.caster, self.on, self.effect.callOnTrigger,self.effect.area,self.icon,ACT_SHIELD)
                return temp

            def triggerDamage(self,value=0,icon="",declancher = 0,onArmor = 1) -> list:
                """D??clanche l'effet"""
                value = round(value)
                temp2 = [value,""]
                if self.type == TYPE_ARMOR and value >0:
                    valueT = valueT2 = round(value)
                    if not(self.effect.absolutShield):
                        secElemMul = 1
                        if self.on.char.secElement in [ELEMENT_EARTH, ELEMENT_UNIVERSALIS_PREMO]:
                            secElemMul += 0.05
                        if self.caster.char.secElement in [ELEMENT_EARTH, ELEMENT_UNIVERSALIS_PREMO]:
                            secElemMul += 0.05
                        valueT2 = round(value * onArmor * secElemMul)

                    value = round(min(valueT2,self.value))
                    self.decate(value=value)
                    declancher.stats.damageOnShield += value
                    self.caster.stats.armoredDamage += value
                    if self.value <= 0:
                        reduc = self.on.char.level
                        if self.caster.specialVars["osPre"]:
                            reduc = reduc + self.caster.char.level * (preOSEff.power/100)
                        elif self.caster.specialVars["osIdo"] or self.caster.specialVars["osPro"]:
                            reduc = reduc + self.caster.char.level * (idoOSEff.power/100)
                        if self.effect.lightShield:
                            reduc = 0
                        reduc = int(reduc)
                        ratio = valueT/valueT2
                        funnyTempVarName = valueT2 - value - reduc
                        funnyTempVarNameButTheSecond = int(funnyTempVarName * ratio)
                        temp2 = [max(0,funnyTempVarNameButTheSecond), ["<:abB:934600555916050452> ","<:abR:934600570633867365> "][self.on.team] + "-" + str(value)+" PAr "]
                    elif value > 0:
                        temp2 = [0,f"{self.icon} -{value} PAr "]
                    else:
                        temp2 = [0,self.icon]

                elif self.effect.redirection > 0 and value > 0 and self.caster.hp > 0:
                    valueT = value
                    redirect = int(valueT * self.effect.redirection/100)
                    valueT = valueT - redirect
                    declancher.indirectAttack(target=self.caster,value=redirect,icon=icon,ignoreImmunity=False,name=self.effect.name,canCrit=False)
                    temp2 = [valueT,"{0} -{1} PV".format(self.caster.icon,redirect)]

                elif (self.type == TYPE_INDIRECT_DAMAGE or self.effect.id in [rosesPhysiEff.id,rosesMagicEff.id,lightLameEff.id,astralLameEff.id,timeLameEff.id,mattSkill4Eff.id]) and self.value>0:
                    if self.effect.onDeclancher:
                        target = declancher
                    else:
                        target = self.on

                    variable = ""
                    damageBase = self.effect.power
                    if self.effect.stat == None:
                        stat = None
                    else:
                        stat = self.caster.allStats()[self.effect.stat]-self.caster.negativeIndirect

                    whoTarget = ALLIES
                    if target.team == self.caster.team and target != self.caster:
                        whoTarget = ENEMIES

                    for a in target.cell.getEntityOnArea(area=self.effect.area,team=target.team,wanted=whoTarget,directTarget=False,fromCell=actTurn.cell):
                        reduc = 1
                        if a != target:
                            reduc = max(AOEMINDAMAGE,1-target.cell.distance(a.cell)*AOEDAMAGEREDUCTION)

                        variable += self.caster.indirectAttack(a,value=indirectDmgCalculator(self.caster, self.on, self.effect.power*reduc, self.effect.stat, danger, area=self.effect.area),icon = self.icon,name=self.effect.name,canCrit=self.effect.stat!=None)
                    temp2[1] = f"{variable}{self.decate(value=1)}"

                elif self.type == TYPE_UNIQUE:
                    if self.effect.id == enchant.id :
                        self.effect.magie += 5

                if self.effect.callOnTrigger != None:
                    temp2[1] = ""
                    if self.effect.id != "nt":
                        for a in [0,1]:
                            for b in tablEntTeam[a]:
                                if type(b.char) != invoc and b.id == self.on.id:
                                    temp2[1] += add_effect(self.caster,b,findEffect(self.effect.callOnTrigger),skillIcon=self.icon)
                                    
                                    b.refreshEffects()
                                    break
                        temp2[1] += f"{self.decate(value=1)}"
                    else:
                        temp2[1] += add_effect(self.caster,declancher,findEffect(self.effect.callOnTrigger))
                        
                        declancher.refreshEffects()

                return temp2

            def triggerDeath(self,killer=None) -> str:
                """D??clanche l'effet"""
                toReturn = ""
                if self.type==TYPE_INDIRECT_REZ:
                    self.on.status = STATUS_RESURECTED
                    self.caster.stats.allieResurected += 1

                    if self.effect.stat == None:
                        heal = self.effect.power

                    elif self.effect.stat == PURCENTAGE:
                        heal = round(self.on.maxHp * self.effect.power /100)

                    self.on.hp = heal
                    self.caster.stats.heals += heal
                    toReturn += f"{self.on.char.name} ({self.on.icon}) est r??anim??{self.on.accord()} !\n{self.caster.icon} {self.icon}??? {self.on.icon} +{heal} PV\n"
                    self.decate(value=1)

                elif self.type == TYPE_INDIRECT_DAMAGE and self.value>0:
                    variable = ""

                    for a in self.on.cell.getEntityOnArea(area=self.effect.area,team=self.on.team,wanted=[ALLIES,ENEMIES][self.caster.team != self.on.team],fromCell=actTurn.cell,directTarget=False):
                        reduc = 1
                        if a != self.on:
                            reduc = max(AOEMINDAMAGE,1-self.on.cell.distance(a.cell)*AOEDAMAGEREDUCTION)

                        variable += self.caster.indirectAttack(a,value=indirectDmgCalculator(self.caster, self.on, self.effect.power*reduc, self.effect.stat, danger, area=self.effect.area),icon = self.icon,name=self.effect.name,canCrit=self.effect.stat!=None)

                elif self.type == TYPE_UNIQUE:
                    if self.effect == hunter:
                        add_effect(self.on,self.on,hunterBuff)
                        self.on.refreshEffects()
                        tempi, useless = self.on.attack(target=killer,value = self.on.char.weapon.power,icon = self.on.char.weapon.emoji,onArmor=self.on.char.weapon.onArmor)
                        toReturn += tempi

                if self.effect.callOnTrigger != None:
                    toReturn += add_effect(self.on,self.on,findEffect(self.effect.callOnTrigger))
                    
                self.decate(value=1)

                return toReturn

            def triggerStartOfTurn(self,danger,decate=True) -> str:
                """D??clanche l'effet"""
                funnyTempVarName=""
                if self.type == TYPE_INDIRECT_HEAL and self.on.hp > 0:              # Heal Indirect
                    if self.effect.area == AREA_MONO:
                        funnyTempVarName, useless = self.caster.heal(self.on,self.icon,self.effect.stat,self.effect.power,self.effect.name,danger,mono=True)
                    else:
                        for a in self.on.cell.getEntityOnArea(area=self.effect.area,team=self.caster.team,wanted=ALLIES,directTarget=False,fromCell=actTurn.cell):
                            funnyTempVarName, useless = self.caster.heal(a,self.icon,self.effect.stat,self.effect.power,self.effect.name,danger)

                elif self.type == TYPE_INDIRECT_DAMAGE and self.value > 0 and ((self.effect.area==AREA_MONO and self.on.hp > 0) or self.effect.area != AREA_MONO):            # Damage indirect
                    variable,damage = "",0
                    if self.effect.stat != None:
                        for a in self.on.cell.getEntityOnArea(area=self.effect.area,team=self.on.team,wanted=[ALLIES,ENEMIES][self.caster.team == self.on.team],directTarget=False,fromCell=actTurn.cell):
                            reduc = 1
                            if a != self.on:
                                reduc = max(AOEMINDAMAGE,1-self.on.cell.distance(a.cell)*AOEDAMAGEREDUCTION)
                            damage = indirectDmgCalculator(self.caster, self.on, self.effect.power*reduc, self.effect.stat, danger, area=self.effect.area)
                            if self.effect.id == bleeding.id:
                                for eff in self.on.effect:
                                    if eff.effect.id == ShiHemophilie.id:
                                        damage = int(damage*(100+eff.effect.power)/100)
                            variable += self.caster.indirectAttack(a,value=damage,icon = self.icon,name=self.effect.name)

                            if self.effect.id == estal.id and damage != 0:
                                self.caster.stats.estialba += damage
                            elif self.effect.id == bleeding.id and damage != 0:
                                self.caster.stats.bleeding += damage

                        funnyTempVarName = variable

                        if decate:
                            funnyTempVarName += self.decate(value=1)
                    else:
                        for a in self.on.cell.getEntityOnArea(area=self.effect.area,team=self.caster.team,wanted=ENEMIES,directTarget=False,fromCell=actTurn.cell):
                            damage = self.effect.power
                            variable += self.caster.indirectAttack(a,value=damage,icon = self.icon,name=self.effect.name,canCrit=self.effect.stat!=None)
                        
                        funnyTempVarName = variable
                        if decate:
                            funnyTempVarName += self.decate(value=1)

                    if self.effect.id == lieSkillEff.id and self.value > 0:
                        effTemp = lieSkillEff
                        effTemp.turnInit,effTemp.lvl = self.turnLeft, self.value

                        funnyTempVarName += add_effect(self.caster,self.on,effTemp)
                        self.on.refreshEffects()

                    if self.effect.id == infection.id:                              # If it's the infection poisonnus effect
                        tempTabl = self.on.cell.getEntityOnArea(area=AREA_DONUT_1,team=self.on.team,wanted=ALLIES,effect=[infection],directTarget=False,fromCell=actTurn.cell)
                        if len(tempTabl) > 0:
                            funnyTempVarName += "L'infection se propage...\n"
                            for ent in tempTabl:
                                funnyTempVarName += add_effect(self.caster,ent,infection)
                                add_effect(self.caster,ent,infectRej)
                                ent.refreshEffects()

                elif self.type == TYPE_BOOST and self.on.hp > 0:                    # Indirect Armor
                    funnyTempVarName += add_effect(self.caster,self.on,findEffect(self.effect.callOnTrigger))
                    self.on.refreshEffects()
                return funnyTempVarName

            def triggerEndOfTurn(self,danger,decate=True) -> str:
                """Trigger the effect"""
                temp = ""
                if self.type == TYPE_INDIRECT_DAMAGE:                               # The only indirect damage effect for now is a insta death
                    if self.effect.stat == None:
                        temp += self.caster.indirectAttack(target=self.on,ignoreImmunity=self.effect.ignoreImmunity ,value=self.effect.power, canCrit=False)
                        if decate:
                            self.decate(value=1)
                    elif self.value > 0 and ((self.effect.area==AREA_MONO and self.on.hp > 0) or self.effect.area != AREA_MONO):
                        variable,damage = "",0
                        if self.effect.stat != HARMONIE:
                            stat,damageBase = self.caster.allStats()[self.effect.stat]-self.caster.negativeIndirect,self.effect.power
                        else:
                            stat = -100
                            for staty in self.caster.allStats():
                                stat = max(stat,staty)
                            damageBase = self.effect.power
                        whoTarget = ALLIES
                        if self.on.team == self.caster.team:
                            whoTarget = ENEMIES

                        for ent in self.on.cell.getEntityOnArea(area=self.effect.area,team=self.on.team,wanted=whoTarget,directTarget=False,fromCell=actTurn.cell):
                            reduc = 1
                            if ent != self.on:
                                reduc = max(AOEMINDAMAGE,1-self.on.cell.distance(ent.cell)*AOEDAMAGEREDUCTION)
                            damage = indirectDmgCalculator(self.caster, self.on, self.effect.power*reduc, self.effect.stat, danger, area=self.effect.area)
                            variable += self.caster.indirectAttack(ent,value=damage,icon = self.icon,name=self.effect.name)

                        if decate:
                            temp = variable + self.decate(value=1)
                        else:
                            temp = variable

                elif self.type == TYPE_UNIQUE:                                      # Poids Plume effect bonus reduce
                    if self.effect == poidPlumeEff:
                        self.value = self.value//2

                elif self.type == TYPE_INDIRECT_HEAL and self.on.hp > 0:            # End of turn healing (aka Light Aura 1)
                    for a in self.on.cell.getEntityOnArea(area=self.effect.area,team=self.caster.team,wanted=ALLIES,directTarget=False,fromCell=actTurn.cell):
                        tempi, useless = self.caster.heal(a,self.icon,self.effect.stat,self.effect.power,self.effect.name,danger)
                        temp += tempi

                if self.effect.callOnTrigger != None:
                    temp += groupAddEffect(self.caster, self.on, self.effect.area, self.effect.callOnTrigger, self.icon, actionStats=[ACT_BOOST,ACT_SHIELD][self.effect.callOnTrigger.type == TYPE_ARMOR])
                return temp

            def triggerRemove(self) -> str:
                """Trigger the effect when it's removed\n
                For now, only unique effect activly use it, but some boost effect use it to"""
                message = ""

                if self.type == TYPE_UNIQUE:                    
                    if self.effect.id == lostSoul.id:                                   # Remove the body effect
                        if self.on.status == STATUS_DEAD:
                            self.on.status = STATUS_TRUE_DEATH
                            message="{0} en avait marre d'attendre une r??surection et a quitt?? le combat\n".format(self.on.char.name)

                elif self.type == TYPE_INDIRECT_DAMAGE:
                    for badGuys in self.on.cell.getEntityOnArea(area=self.effect.area,team=self.on.team,wanted=[ALLIES,ENEMIES][self.caster.team == self.on.team],directTarget=False,fromCell=actTurn.cell):
                        reduc = 1
                        if reduc != self.on:
                            reduc = max(AOEMINDAMAGE,1-self.on.cell.distance(badGuys.cell)*AOEDAMAGEREDUCTION)
                        damage = indirectDmgCalculator(self.caster,badGuys,self.effect.power*reduc,self.effect.stat,danger,self.effect.area)
                        message += self.caster.indirectAttack(badGuys,value=damage,icon = self.icon,name=self.effect.name,canCrit=self.effect.stat!=None)

                elif self.type == TYPE_INDIRECT_HEAL and self.on.hp > 0:
                    if self.effect.id == zelianR.id:
                        if self.value > 0:
                            message += self.caster.heal(self.on, self.icon, FIXE, self.value, self.name, mono = True)[0]
                    else:
                        for a in self.on.cell.getEntityOnArea(area=self.effect.area,team=self.caster.team,wanted=ALLIES,directTarget=False,fromCell=actTurn.cell):
                            message, useless = self.caster.heal(a,self.icon,self.effect.stat,self.effect.power,self.effect.name,danger)

                if self.effect.callOnTrigger != None:                               # If the effect give another effect when removed, give that another effect
                    message += groupAddEffect(self.caster, self.on, self.effect.area, self.effect.callOnTrigger, skillIcon=self.icon)
                    if findEffect(self.effect.callOnTrigger).id == temNativTriggered.id:
                        self.on.icon, self.on.char.icon = '<:colegue:895440308257558529>','<:colegue:895440308257558529>'

                return message

            def allStats(self):
                return self.tablAllStats

        def add_effect(caster: entity,target: entity,effect: classes.effect,start: str = "", ignoreEndurance=False, danger=danger, setReplica : Union[None,entity] = None, effPowerPurcent=100, useActionStats = ACT_SHIELD, skillIcon=""):
            """M??thode qui rajoute l'effet Effet ?? l'entity Target lanc?? par Caster dans la liste d'attente des effets"""
            if type(target) == entity:
                valid,id,popipo = False,0,""
                valid = True
                turn = caster.stats.survival
                if effect.id == elemEff.id:
                    effect = tablElemEff[target.char.element]

                # Does the effect can be applied ?
                if effect.reject != None:                                           # The effect reject other effects
                    for a in effect.reject:
                        for b in target.effect:
                            if a == b.effect.id:
                                popipo = f"{caster.icon} {effect.emoji[caster.char.species-1][caster.team]} ??? ????{findEffect(a).emoji[caster.char.species-1][caster.team]} {target.icon}\n"
                                valid = False
                                break
                        if not(valid):
                            break
                for a in target.effect:
                    if a.effect.id == effect.id and not(effect.stackable):          # The effect insn't stackable
                        if a.effect.id == incurable.id:                                 # But is't Healn't
                            if a.effect.power < effect.power:                               # A better Healn't
                                diff = effect.power - a.effect.power
                                a.effect.power = effect.power
                                a.caster = caster
                                popipo = f"{caster.icon} ??? {a.effect.emoji[caster.char.species-1][caster.team]}+{diff} {target.icon}\n"
                            valid = False

                        elif a.effect.id in [idoOHArmor.id,proOHArmor.id,altOHArmor.id]:  # Overhealth Shield
                            if a.value < effect.overhealth:                               # A better Overhealth shield
                                diff = effect.overhealth - a.value
                                a.value = effect.overhealth
                                a.caster = caster
                                a.turnLeft = effect.turnInit
                                popipo = f"{caster.icon} {effect.emoji[caster.char.species-1][caster.team]} ??? {a.effect.emoji[caster.char.species-1][caster.team]}+{diff} {target.icon}\n"
                            valid = False

                        elif not(effect.silent):                                        # It's not Healn't
                            popipo = f"{caster.icon} {effect.emoji[caster.char.species-1][caster.team]} ??? ????{a.effect.emoji[caster.char.species-1][caster.team]} {target.icon}\n"
                            valid = False

                        else:
                            valid = False

                if valid:
                    valid = False
                    while not(valid):                                               # Why L??na. Why ?
                        id = random.randint(0,maxsize)                  # Ok, I use them now
                        valid = id not in allEffectInFight

                    icon = effect.emoji[caster.char.species-1][caster.team]
                    if effect.id == darkFlumPoi.id:
                        effect = darkFlumPoi
                        effect.power = int(caster.char.level * 0.2)

                    if effect.overhealth > 0:                                       # Armor Effect
                        temp = caster.allStats()
                        value, critMsg = effect.overhealth, ""
                        if effect.id == chaosArmorEff.id:
                            value = random.randint(10,50)
                        friablility = max(1-(turn / 30),0.1)                   # Reduct over time
                        if useActionStats == None:
                            useActionStats = ACT_SHIELD

                        dangerBoost = 1
                        if caster.team == 1:
                            dangerBoost = danger/100

                        secElemMul = 1
                        if caster.char.secElement in [ELEMENT_FIRE, ELEMENT_UNIVERSALIS_PREMO]:
                            secElemMul -= 0.05
                        elif caster.char.secElement in [ELEMENT_WATER, ELEMENT_UNIVERSALIS_PREMO]:
                            secElemMul += 0.05
                        if target.char.secElement in [ELEMENT_FIRE, ELEMENT_UNIVERSALIS_PREMO]:
                            secElemMul -= 0.05
                        elif target.char.secElement in [ELEMENT_WATER, ELEMENT_UNIVERSALIS_PREMO]:
                            secElemMul += 0.05

                        if effect.stat != None:                                         # Classical armor effect
                            if effect.stat == HARMONIE:
                                maxi = -100
                                for randomVar in temp:
                                    maxi = max(maxi,randomVar)

                                value = round(effect.overhealth * secElemMul * caster.valueBoost(target=target,armor=True) * (maxi-caster.actionStats()[useActionStats] +100)*((target.endurance+1250)/1250)/100 * friablility * dangerBoost * (0.8 + 0.01*caster.level))
                            else:
                                value = round(value * secElemMul * caster.valueBoost(target=target,armor=True) * (temp[effect.stat]-caster.actionStats()[useActionStats] +100)*((target.endurance+1250)/1250)/100 * friablility * dangerBoost * (min((1-ARMORMALUSATLVL0/100) + ARMORLBONUSPERLEVEL*caster.level,3)))

                            if random.randint(0,99) < caster.calHealCrit(target) * 100:
                                value = int(value * (1.25 + (preciChiEff.power * int(caster.specialVars["preci"]) + ironHealthEff.power * int(target.specialVars["ironHealth"])) * 0.01))
                                critMsg = " !"
                                caster.stats.critHeal += 1
                            caster.stats.nbHeal += 1
                        else:                                                           # Fixe armor effect
                            value = round(effect.overhealth)

                        if not(effect.absolutShield):
                            for a in target.effect:
                                if a.type == TYPE_ARMOR and not(effect.lightShield):
                                    reduc = 0.5
                                    if caster.specialVars["osPre"]:
                                        reduc = reduc + reduc * (preOSEff.power/2/100)
                                    elif caster.specialVars["osIdo"] or caster.specialVars["osPro"]:
                                        reduc = reduc + reduc * (idoOSEff.power/2/100)

                                    value = round(value*reduc)
                                    break

                        tmpBalancing = 1
                        for eff in caster.effect:
                            if eff.effect.id == armorReductionTmp.id:
                                tmpBalancing -= armorReductionTmp.power/100
                        value = int(value*tmpBalancing)
                        caster.stats.shieldGived += value

                        toAppend = fightEffect(id,effect,caster,target,effect.turnInit,effect.trigger,TYPE_ARMOR,icon,value)
                        if setReplica != None:
                            toAppend.replicaTarget = setReplica

                        addEffect.append(toAppend)

                        if not(effect.silent):
                            tempTurn = effect.turnInit+int(caster.char==ELEMENT_TIME)
                            popipo = f"{caster.icon} {skillIcon} ??? {target.icon} {icon} +{separeUnit(value)} PAr{critMsg}\n"

                    else:                                                           # Any other effect
                        if effect.id == kikuRaiseEff.id and type(target.char)==octarien and (not(target.char.rez) or target.status == STATUS_RESURECTED):
                            effect = kikuUnlifeGift
                        
                        if effPowerPurcent == 100:
                            effPowerPurcent = None
                        toAppend = fightEffect(id,effect,caster,target,effect.turnInit,effect.trigger,effect.type,icon,effect.lvl,effPowerPurcent)
                        if setReplica != None:
                            toAppend.replicaTarget = setReplica
                        if effect.id == undeadEff2.id:
                            toAppend.value = target.maxHp
                        addEffect.append(toAppend)

                        if effect.id == "clemBloodJauge":
                            caster.specialVars["clemBloodJauge"] = toAppend

                        if not(effect.silent):
                            power = ["", " ({0}%)".format(effPowerPurcent)][effPowerPurcent!=None]
                            popipo = f"{caster.icon} {skillIcon} ??? {target.icon} +{icon} __{effect.name}__{power}\n"

                        target.refreshEffects()

                        tablTemp = [altOHEff.id,proOHEff.id,idoOHEff.id,idoOSEff.id,proOSEff.id,preOSEff.id,heriteEstialbaEff.id,heriteLesathEff.id,floorTanking.id,summonerMalus.id,foulleeEff.id,preciChiEff.id,ironHealthEff.id]
                        nameTemp = ["ohAlt","ohPro","ohIdo","osIdo","osPro","osPre","heritEstial","heritLesath","tankTheFloor","summonerMalus","foullee","preci","ironHealth"]
                        tablTempEff = [physicRuneEff.id,magicRuneEff.id, eventFas.id]
                        nameTempEff = ["damageSlot","damageSlot","fascination"]

                        for funnyVarName in range(len(tablTemp)):
                            if effect.id == tablTemp[funnyVarName]:
                                target.specialVars["{0}".format(nameTemp[funnyVarName])] = True
                                break

                        for funnyVarName in range(len(tablTempEff)):
                            if effect.id == tablTempEff[funnyVarName]:
                                target.specialVars["{0}".format(nameTempEff[funnyVarName])] = toAppend
                                break

                        if effect.id == estal.id and caster.specialVars["heritEstial"]:                               # If is the Estialba effect
                            effect = estal2
                            icon = effect.emoji[caster.char.species-1][caster.team]

                            popipo += f"{caster.icon} {heriteEstialba.emoji} ??? {target.icon} +{icon} __{effect.name}__\n"
                            target.refreshEffects()

                        elif effect.id == bleeding.id and caster.specialVars["heritLesath"] :                         # If is the hemorragic effect
                            effect=bleeding2
                            icon = effect.emoji[caster.char.species-1][caster.team]
                            addEffect.append(fightEffect(id,effect,caster,target,effect.turnInit,effect.trigger,effect.type,icon,effect.lvl))

                            popipo += f"{caster.icon} {heriteLesath.emoji} ??? {target.icon} +{icon} __{effect.name}__\n"
                            target.refreshEffects()

                        elif effect.id == bloodPactEff.id:
                            caster.specialVars["aspiSlot"] = bloodPactEff.power
                        elif effect.id == partnerIn.id:
                            tempTabl = tablEntTeam[caster.team]
                            tempTabl.sort(key=lambda chocolatine: getPartnerValue(chocolatine.char),reverse=True)


                            if tempTabl[0] == caster:
                                tempTabl.remove(caster)

                            if len(tempTabl) > 0:
                                effect, icon = partnerOut, partnerOut.emoji[0][0]
                                addEffect.append(fightEffect(id,effect,caster,tempTabl[0],effect.turnInit,effect.trigger,effect.type,icon,effect.lvl))
                                popipo += f"{caster.icon} {partner.emoji} ??? {tempTabl[0].icon} +{icon} __{effect.name}__\n"
                                tempTabl[0].refreshEffects()
                                caster.specialVars["partner"] = tempTabl[0]
                        elif effect.id == eventFas.id:
                            listFasTeam[target.team].append(target)
                        elif effect.id in [haimaEffect.id,pandaimaEff.id]:
                            temp, eff = caster.allStats(), effect.callOnTrigger
                            value, critMsg = eff.overhealth, ""
                            friablility = max(1-(turn / 30),0.1)                   # Reduct over time
                            useActionStats = ACT_SHIELD

                            dangerBoost = 1
                            if caster.team == 1:
                                dangerBoost = danger/100

                            secElemMul = 1
                            if caster.char.secElement in [ELEMENT_FIRE, ELEMENT_UNIVERSALIS_PREMO]:
                                secElemMul -= 0.05
                            elif caster.char.secElement in [ELEMENT_WATER, ELEMENT_UNIVERSALIS_PREMO]:
                                secElemMul += 0.05
                            if target.char.secElement in [ELEMENT_FIRE, ELEMENT_UNIVERSALIS_PREMO]:
                                secElemMul -= 0.05
                            elif target.char.secElement in [ELEMENT_WATER, ELEMENT_UNIVERSALIS_PREMO]:
                                secElemMul += 0.05

                            value = round(value * secElemMul * caster.valueBoost(target=target,armor=True) * (temp[eff.stat]-caster.actionStats()[useActionStats] +100)*((target.endurance+1250)/1250)/100 * friablility * dangerBoost * (min((1-ARMORMALUSATLVL0/100) + ARMORLBONUSPERLEVEL*caster.level,3)))

                            if random.randint(0,99) < caster.calHealCrit(target) * 100:
                                value = int(value * (1.25 + (preciChiEff.power * int(caster.specialVars["preci"]) + ironHealthEff.power * int(target.specialVars["ironHealth"])) * 0.01))
                                critMsg = " !"
                                caster.stats.critHeal += 1
                            caster.stats.nbHeal += 1

                            for a in target.effect:
                                if a.type == TYPE_ARMOR:
                                    reduc = 0.5
                                    if caster.specialVars["osPre"]:
                                        reduc = reduc + reduc * (preOSEff.power/2/100)
                                    elif caster.specialVars["osIdo"] or caster.specialVars["osPro"]:
                                        reduc = reduc + reduc * (idoOSEff.power/2/100)

                                    value = round(value*reduc)
                                    break

                            tmpBalancing = 1
                            for eff2 in caster.effect:
                                if eff2.effect.id == armorReductionTmp.id:
                                    tmpBalancing -= armorReductionTmp.power/100
                            value = int(value*tmpBalancing)
                            caster.stats.shieldGived += value
                            toAppend = fightEffect(id,eff,caster,target,eff.turnInit,eff.trigger,TYPE_ARMOR,eff.emoji[caster.char.species-1][caster.team],value)
                            if setReplica != None:
                                toAppend.replicaTarget = setReplica

                            addEffect.append(toAppend)
                            target.refreshEffects()

                            if not(eff.silent):
                                tempTurn = eff.turnInit+int(caster.char==ELEMENT_TIME)
                                popipo = f"{caster.icon} {skillIcon} ??? {target.icon} {icon} +{separeUnit(value)} PAr{critMsg}\n"

                if target.hp > 0:
                    return popipo
                else:
                    return ''
            else:
                return ""

        def groupAddEffect(caster:entity, target:entity,area:Union[int,List[entity]],effect:List[classes.effect],skillIcon="",actionStats=ACT_BOOST,effPurcent=100):
            tablName, tablEff, tablIcon, toReturn = [], [], [], ""
            if type(effect) != list:
                effect = [effect]

            for c in effect:
                eff = findEffect(c)
                if eff != None:
                    if type(area) == int:
                        tablToSee = target.cell.getEntityOnArea(area=area,team=caster.team,wanted=[ENEMIES,ALLIES][eff.type in [TYPE_BOOST,TYPE_ARMOR,TYPE_INDIRECT_HEAL,TYPE_INDIRECT_REZ]],directTarget=False,fromCell=actTurn.cell)
                    else:
                        tablToSee = area
                    for ent in tablToSee:
                        ballerine = add_effect(caster,ent,eff,useActionStats=actionStats,skillIcon=skillIcon,effPowerPurcent=effPurcent)
                        if eff.type == TYPE_ARMOR:
                            toReturn += ballerine
                        else:
                            if '????' not in ballerine and ballerine != "":
                                if eff.name not in tablEff:
                                    tablEff.append(eff.name)
                                    tablIcon.append(eff.emoji[caster.char.species-1][caster.team])
                                    tablName.append(ent.icon)
                                else:
                                    for cmpt in range(len(tablEff)):
                                        if tablEff[cmpt] == eff.name:
                                            tablName[cmpt]+=ent.icon
                                            break
                        ent.refreshEffects()

            if tablEff != []:
                temp = ""
                if effPurcent != 100 and effPurcent != None:
                    temp = " ({0}%)".format(int(effPurcent))
                for cmpt in range(len(tablEff)):
                    toReturn += "{1} {2} ??? {3} +{0} __{4}__{5}\n".format(tablIcon[cmpt],caster.icon,skillIcon,tablName[cmpt],tablEff[cmpt],temp)

            return toReturn

        # =============================================== Pre fight things ================================================

        logs += "Fight triggered by {0}\n".format(ctx.author.name)
        logs += "\n=========\nTeams filling phase\n=========\n\n"

        for tmp in team1:   # dictIsNpcVar actualisation
            if type(tmp) == tmpAllie:
                for cmpt in tablIsNpcName:
                    if tmp.isNpc(cmpt):
                        dictIsNpcVar[f"{cmpt}"] = True
                        break

        # Teams generations -----------------------------------------------
        if len(team1) < [8,16][bigMap] and not(octogone) and not(procurFight): # Remplisage de la team1
            aleaMax = len(tablAllAllies)-1
            alreadyFall = []
            lvlMax = 0

            for a in team1:
                lvlMax = max(lvlMax,a.level)

            while len(team1) < [8,16][bigMap]:
                vacantRole = ["DPT1","DPT2","Healer","Booster"]

                for perso in team1:
                    if perso.aspiration in [BERSERK,TETE_BRULE,OBSERVATEUR,POIDS_PLUME,ENCHANTEUR,MAGE] and ("DPT1" in vacantRole):
                        vacantRole.remove("DPT1")
                    elif perso.aspiration in [BERSERK,TETE_BRULE,OBSERVATEUR,POIDS_PLUME,ENCHANTEUR,MAGE] and ("DPT2" in vacantRole):
                        vacantRole.remove("DPT2")
                    elif perso.aspiration in [IDOLE,INOVATEUR] and ("Booster" in vacantRole):
                        vacantRole.remove("Booster")
                    elif perso.aspiration in [PREVOYANT,ALTRUISTE,VIGILANT,PROTECTEUR] and ("Healer" in vacantRole):
                        vacantRole.remove("Healer")

                tablToSee = []
                if len(vacantRole) <= 0:
                    tablToSee = tablAllieTemp
                else:
                    for role in vacantRole:
                        if role in ["DPT1","DPT2"]:
                            for allie in tablAllieTemp:
                                if allie.aspiration in [BERSERK,TETE_BRULE,OBSERVATEUR,POIDS_PLUME,ENCHANTEUR,MAGE]:
                                    tablToSee.append(allie)
                        elif role == "Healer":
                            for allie in tablAllieTemp:
                                if allie.aspiration in [PREVOYANT,ALTRUISTE,VIGILANT,PROTECTEUR]:
                                    tablToSee.append(allie)
                        elif role == "Booster":
                            for allie in tablAllieTemp:
                                if allie.aspiration in [IDOLE,INOVATEUR]:
                                    tablToSee.append(allie)

                temp = random.randint(0,len(tablToSee)-1)
                alea = tablToSee[temp]
                tablAllieTemp.remove(alea)

                if alea.isNpc("Lena") and random.randint(0,99) < 25:
                    alea = copy.deepcopy(findAllie("Luna"))
                elif alea.isNpc("Gwendoline"):
                    bidule = random.randint(0,99)
                    if bidule < 33:
                        alea = copy.deepcopy(findAllie("Klironovia"))
                    elif bidule < 66:
                        alea = copy.deepcopy(findAllie("Altikia"))
                elif alea.isNpc("Shushi") and random.randint(0,99) < 25:
                    alea = copy.deepcopy(findAllie("Shihu"))
                elif alea.isNpc("Anna") and random.randint(0,99) < 25 and enableMiror:
                    alea = copy.deepcopy(findAllie("Belle"))
                elif alea.isNpc("Alice") and random.randint(0,99) < 35:
                    alea = copy.deepcopy(findAllie("Alice alt."))

                if alea.name in ["Alice","Alice alt.","Ruby","Cl??mence"]:
                    enableMiror = False
                elif alea.name == "Belle":
                    for allies in tablAllieTemp[:]:
                        if allies.name in ["Alice","Cl??mence"]:
                            try:
                                tablAllieTemp.remove(allies)
                            except:
                                logs += "\nCouldn't remove Alice or Clemence from the list, somehow"

                for cmpt in tablIsNpcName:
                    if alea.isNpc(cmpt):
                        dictIsNpcVar[f"{cmpt}"] = True
                        break

                alea.changeLevel(lvlMax)
                autoHead = getAutoStuff(alea.stuff[0],alea)
                autoBody = getAutoStuff(alea.stuff[1],alea)
                autoShoe = getAutoStuff(alea.stuff[2],alea)
                alea.stuff = [autoHead,autoBody,autoShoe]
                if alea.level < 10:
                    alea.element = ELEMENT_NEUTRAL
                elif alea.level < 20 and alea.element in [ELEMENT_SPACE,ELEMENT_TIME,ELEMENT_LIGHT,ELEMENT_DARKNESS]:
                    alea.element = ELEMENT_NEUTRAL

                team1 += [alea]

                logs += "{0} have been added into team1 ({1}, {2}, {3})\n".format(alea.name,autoHead.name,autoBody.name,autoShoe.name)

        team1.sort(key=lambda star: star.stars, reverse = True)
        starLevel = team1[0].stars
        team1.sort(key=lambda star: star.level, reverse = True)

        if team2 == []: # G??n??ration de la team 2
            lvlMax = team1[0].level
            if team1[0].isNpc("Cl??mence Exalt??e"):
                lvlMax -= 200
            elif len(team1) > 1 and (team1[0].isNpc("Iliana pr??.") or team1[1].isNpc("Iliana pr??.")):
                lvlMax += 100
            winStreak = teamWinDB.getVictoryStreak(team1[0])

            # random.randint(0,99) > 10+winStreak
            if random.randint(0,99) > 10+winStreak or team1[0].isNpc("Cl??mence Exalt??e"): # Vs normal team
                danger = dangerLevel[winStreak] + (starLevel * DANGERUPPERSTAR)

                tablOctaTemp:List[octarien] = copy.deepcopy(tablAllEnnemies)
                oneVAll = False

                tablTeamOctaPos = [0,0,1,1,2,2]+[random.randint(0,2),random.randint(0,2)]
                tablTeamOctaComp = [4,2,2]

                random.shuffle(tablTeamOctaPos)
                if len(team2) < len(team1) and lvlMax >= 15:
                    if random.randint(0,99) < 35:               # Boss ?
                        temp = random.randint(0,len(tablBoss)-1)
                        alea = copy.deepcopy(tablBoss[temp])
                        while team1[0].isNpc("Cl??mence Exalt??e") and alea.isNpc("Cl??mence pos."):
                            temp = random.randint(0,len(tablBoss)-1)
                            alea = copy.deepcopy(tablBoss[temp])

                        #alea = copy.deepcopy(findEnnemi("Cl??mence pos."))          

                        oneVAll = alea.oneVAll

                        alea.changeLevel(lvlMax)
                        team2.append(alea)
                        logs += "{0} have been added into team2\n".format(alea.name)

                        if alea.isNpc("Luna ex."):
                            alea = copy.deepcopy(findAllie("Shushi Cohabit??e"))
                            procurData = procurTempStuff["Shushi Cohabit??e"]
                            alea.changeLevel(lvlMax)

                            alea.stuff = [
                                stuff(procurData[1][0],procurData[1][1],0,0,int(procurData[4][0][0]*procurData[4][0][1]*lvlMax),int(procurData[4][1][0]*procurData[4][1][1]*lvlMax),int(procurData[4][2][0]*procurData[4][2][1]*lvlMax),int(procurData[4][3][0]*procurData[4][3][1]*lvlMax),int(procurData[4][4][0]*procurData[4][4][1]*lvlMax),int(procurData[4][5][0]*procurData[4][5][1]*lvlMax),int(procurData[4][6][0]*procurData[4][6][1]*lvlMax),int(procurData[4][7][0]*procurData[4][7][1]*lvlMax),int(procurData[4][8][0]*procurData[4][8][1]*lvlMax),int(procurData[4][9][0]*procurData[4][9][1]*lvlMax),emoji=procurData[1][2]),
                                stuff(procurData[2][0],procurData[2][1],1,0,int(procurData[4][0][0]*procurData[4][0][1]*lvlMax),int(procurData[4][1][0]*procurData[4][1][1]*lvlMax),int(procurData[4][2][0]*procurData[4][2][1]*lvlMax),int(procurData[4][3][0]*procurData[4][3][1]*lvlMax),int(procurData[4][4][0]*procurData[4][4][1]*lvlMax),int(procurData[4][5][0]*procurData[4][5][1]*lvlMax),int(procurData[4][6][0]*procurData[4][6][1]*lvlMax),int(procurData[4][7][0]*procurData[4][7][1]*lvlMax),int(procurData[4][8][0]*procurData[4][8][1]*lvlMax),int(procurData[4][9][0]*procurData[4][9][1]*lvlMax),emoji=procurData[2][2]),
                                stuff(procurData[3][0],procurData[3][1],0,0,int(procurData[4][0][0]*procurData[4][0][1]*lvlMax),int(procurData[4][1][0]*procurData[4][1][1]*lvlMax),int(procurData[4][2][0]*procurData[4][2][1]*lvlMax),int(procurData[4][3][0]*procurData[4][3][1]*lvlMax),int(procurData[4][4][0]*procurData[4][4][1]*lvlMax),int(procurData[4][5][0]*procurData[4][5][1]*lvlMax),int(procurData[4][6][0]*procurData[4][6][1]*lvlMax),int(procurData[4][7][0]*procurData[4][7][1]*lvlMax),int(procurData[4][8][0]*procurData[4][8][1]*lvlMax),int(procurData[4][9][0]*procurData[4][9][1]*lvlMax),emoji=procurData[2][2])
                            ]

                            team1.append(alea)
                            logs += "{0} have been added into team1\n".format(alea.name)

                            alea = copy.deepcopy(findAllie("Iliana"))
                            alea.changeLevel(lvlMax)
                            alea.stuff = [getAutoStuff(alea.stuff[0],alea),getAutoStuff(alea.stuff[1],alea),getAutoStuff(alea.stuff[2],alea)]
                            alea.says = ilianaSaysVsLuna

                            team1.append(alea)
                            logs += "{0} have been added into team1\n".format(alea.name)

                        elif alea.isNpc("Cl??mence pos."):
                            alea = copy.deepcopy(findAllie("Alice Exalt??e"))
                            procurData = procurTempStuff["Alice Exalt??e"]
                            alea.changeLevel(lvlMax)

                            alea.stuff = [
                                stuff(procurData[1][0],procurData[1][1],0,0,int(procurData[4][0][0]*procurData[4][0][1]*lvlMax),int(procurData[4][1][0]*procurData[4][1][1]*lvlMax),int(procurData[4][2][0]*procurData[4][2][1]*lvlMax),int(procurData[4][3][0]*procurData[4][3][1]*lvlMax),int(procurData[4][4][0]*procurData[4][4][1]*lvlMax),int(procurData[4][5][0]*procurData[4][5][1]*lvlMax),int(procurData[4][6][0]*procurData[4][6][1]*lvlMax),int(procurData[4][7][0]*procurData[4][7][1]*lvlMax),int(procurData[4][8][0]*procurData[4][8][1]*lvlMax),int(procurData[4][9][0]*procurData[4][9][1]*lvlMax),emoji=procurData[1][2]),
                                stuff(procurData[2][0],procurData[2][1],1,0,int(procurData[4][0][0]*procurData[4][0][1]*lvlMax),int(procurData[4][1][0]*procurData[4][1][1]*lvlMax),int(procurData[4][2][0]*procurData[4][2][1]*lvlMax),int(procurData[4][3][0]*procurData[4][3][1]*lvlMax),int(procurData[4][4][0]*procurData[4][4][1]*lvlMax),int(procurData[4][5][0]*procurData[4][5][1]*lvlMax),int(procurData[4][6][0]*procurData[4][6][1]*lvlMax),int(procurData[4][7][0]*procurData[4][7][1]*lvlMax),int(procurData[4][8][0]*procurData[4][8][1]*lvlMax),int(procurData[4][9][0]*procurData[4][9][1]*lvlMax),emoji=procurData[2][2]),
                                stuff(procurData[3][0],procurData[3][1],0,0,int(procurData[4][0][0]*procurData[4][0][1]*lvlMax),int(procurData[4][1][0]*procurData[4][1][1]*lvlMax),int(procurData[4][2][0]*procurData[4][2][1]*lvlMax),int(procurData[4][3][0]*procurData[4][3][1]*lvlMax),int(procurData[4][4][0]*procurData[4][4][1]*lvlMax),int(procurData[4][5][0]*procurData[4][5][1]*lvlMax),int(procurData[4][6][0]*procurData[4][6][1]*lvlMax),int(procurData[4][7][0]*procurData[4][7][1]*lvlMax),int(procurData[4][8][0]*procurData[4][8][1]*lvlMax),int(procurData[4][9][0]*procurData[4][9][1]*lvlMax),emoji=procurData[2][2])
                            ]

                            team1.append(alea)
                            logs += "{0} have been added into team1\n".format(alea.name)

                for octa in tablOctaTemp[:]:
                    if octa.baseLvl > lvlMax:
                        tablOctaTemp.remove(octa)

                octoRolesNPos = [[[],[],[]],[[],[],[]],[[],[],[]]] # 0 : Dmg; 1 : Heal/Armor; 2 : Buff/Debuff

                for octa in tablOctaTemp:
                    if octa.aspiration in [BERSERK, POIDS_PLUME, MAGE, ENCHANTEUR, OBSERVATEUR, TETE_BRULE,SORCELER,ATTENTIF]:
                        roleId = 0
                    elif octa.aspiration in [ALTRUISTE, PREVOYANT]:
                        roleId = 1
                    elif octa.aspiration in [IDOLE,INOVATEUR, PROTECTEUR, VIGILANT]:
                        roleId = 2
                    else:
                        roleId = random.randint(0,2)

                    octoRolesNPos[roleId][octa.weapon.range].append(octa)

                for octa in team2:
                    if octa.aspiration in [BERSERK, POIDS_PLUME, MAGE, ENCHANTEUR, OBSERVATEUR, TETE_BRULE]:
                        roleId = 0
                    elif octa.aspiration in [ALTRUISTE, PREVOYANT]:
                        roleId = 1
                    elif octa.aspiration in [IDOLE,INOVATEUR, PROTECTEUR, VIGILANT]:
                        roleId = 2
                    else:
                        roleId = random.randint(0,2)

                    tablTeamOctaComp[roleId] -= 1
                    try:
                        tablTeamOctaPos.remove(octa.weapon.range)
                    except:
                        pass

                if lvlMax > 20 and not(procurFight):
                    while len(team2) < min(8,len(team1)) and not(oneVAll):
                        alea = None
                        for tempCmpt in range(len(tablTeamOctaComp)):
                            if tablTeamOctaComp[tempCmpt] > 0 and len(octoRolesNPos[tempCmpt][tablTeamOctaPos[0]]) > 0:
                                break

                        for secondCmpt in range(len(tablTeamOctaPos)):
                            if len(octoRolesNPos[tempCmpt][tablTeamOctaPos[secondCmpt]]) > 0:
                                break

                        if len(octoRolesNPos[tempCmpt][tablTeamOctaPos[secondCmpt]]) > 1:
                            alea = octoRolesNPos[tempCmpt][tablTeamOctaPos[secondCmpt]][random.randint(0,len(octoRolesNPos[tempCmpt][tablTeamOctaPos[secondCmpt]])-1)]
                        else:
                            try:
                                alea = octoRolesNPos[tempCmpt][tablTeamOctaPos[secondCmpt]][0]
                            except:
                                pass
                        
                        if alea != None:
                            octoRolesNPos[tempCmpt][tablTeamOctaPos[secondCmpt]].remove(alea)
                            tablTeamOctaPos.remove(tablTeamOctaPos[secondCmpt])
                            tablTeamOctaComp[tempCmpt] -= 1

                            if alea.isNpc("Octaling"):
                                alea = copy.deepcopy(alea)
                                alea.weapon = weapons[random.randint(0,len(weapons)-1)]
                                alea.aspiration = random.randint(0,len(inspi)-1)
                                temp2 = copy.deepcopy(skills)
                                for cmpt in range(7):
                                    rand = random.randint(0,len(temp2)-1)
                                    alea.skills[cmpt] = temp2[rand]
                                    temp2.remove(temp2[rand])
                                alea.element = random.randint(0,len(elemNames)-1)

                            alea.changeLevel(lvlMax)
                            
                            team2.append(alea)
                            logs += "{0} have been added into team2\n".format(alea.name)

                else:
                    while len(team2) < [8,12][team1[0].isNpc("Cl??mence Exalt??e")] and not(oneVAll) and len(tablOctaTemp)>0:
                        if len(tablOctaTemp) > 1:
                            alea = tablOctaTemp[random.randint(0,len(tablOctaTemp)-1)]
                        else:
                            alea = tablOctaTemp[0]              
                        tablOctaTemp.remove(alea)

                        if alea.isNpc("Octaling"):
                            alea = copy.deepcopy(alea)
                            alea.weapon = weapons[random.randint(0,len(weapons)-1)]
                            alea.aspiration = random.randint(0,len(inspi)-1)
                            temp2 = copy.deepcopy(skills)
                            for cmpt in range(7):
                                rand = random.randint(0,len(temp2)-1)
                                alea.skills[cmpt] = temp2[rand]
                                temp2.remove(temp2[rand])
                            alea.element = random.randint(0,len(elemNames)-1)

                        alea.changeLevel(lvlMax)
                        
                        team2.append(alea)
                        logs += "{0} have been added into team2\n".format(alea.name)

            else: # Vs temp ally team
                lvlMax, temp = 0, team1
                temp.sort(key=lambda funnyTempVarName: funnyTempVarName.level,reverse=True)

                leniAllie, danger, lvlMax =  len(team1), altDanger[winStreak] + (starLevel * DANGERUPPERSTAR), min(temp[0].level,55)
                
                tablTeamAlliePos = [0,0,1,1,2,2]+[random.randint(0,2),random.randint(0,2)]
                tablTeamAllieComp = [4,2,2]

                random.shuffle(tablTeamAlliePos)
                allieRolesNPos = [[[],[],[]],[[],[],[]],[[],[],[]]] # 0 : Dmg; 1 : Heal/Armor; 2 : Buff/Debuff

                for allie in tablAllieTemp:
                    if allie.aspiration in [BERSERK, POIDS_PLUME, MAGE, ENCHANTEUR, OBSERVATEUR, TETE_BRULE, SORCELER, ATTENTIF]:
                        roleId = 0
                    elif allie.aspiration in [ALTRUISTE, PREVOYANT, PROTECTEUR, VIGILANT]:
                        roleId = 1
                    elif allie.aspiration in [IDOLE, INOVATEUR]:
                        roleId = 2
                    else:
                        roleId = random.randint(0,2)

                    allieRolesNPos[roleId][allie.weapon.range].append(allie)

                while len(team2) < 8:
                    for tempCmpt in range(len(tablTeamAllieComp)):
                        if tablTeamAllieComp[tempCmpt] > 0 and len(allieRolesNPos[tempCmpt][tablTeamAlliePos[0]]) > 0:
                            break

                    for secondCmpt in range(len(tablTeamAlliePos)):
                        if len(allieRolesNPos[tempCmpt][tablTeamAlliePos[secondCmpt]]) > 0:
                            break

                    alea = None
                    if len(allieRolesNPos[tempCmpt][tablTeamAlliePos[secondCmpt]]) > 1:
                        alea = allieRolesNPos[tempCmpt][tablTeamAlliePos[secondCmpt]][random.randint(0,len(allieRolesNPos[tempCmpt][tablTeamAlliePos[secondCmpt]])-1)]
                    else:
                        try:
                            alea = allieRolesNPos[tempCmpt][tablTeamAlliePos[secondCmpt]][0]
                        except:
                            pass

                    if alea != None:
                        allieRolesNPos[tempCmpt][tablTeamAlliePos[secondCmpt]].remove(alea)
                        tablTeamAlliePos.remove(tablTeamAlliePos[secondCmpt])
                        tablTeamAllieComp[tempCmpt] -= 1
                    else:
                        logs += "\nHum... Something gone wrong... So hum... emergency procedure"
                        if len(tablAllieTemp) > 1:
                            alea=tablAllieTemp[random.randint(0,len(tablAllieTemp)-1)]
                        else:
                            alea=tablAllieTemp[0]
                    tablAllieTemp.remove(alea)

                    if alea.isNpc("Lena") and random.randint(0,99) < 25:
                        alea = copy.deepcopy(findAllie("Luna"))
                    elif alea.isNpc("Shushi") and random.randint(0,99) < 25:
                        alea = copy.deepcopy(findAllie("Shihu"))
                    elif alea.isNpc("Gwendoline"):
                        alea = copy.deepcopy(findAllie(["Gwendoline","Klironovia","Altikia"][random.randint(0,2)]))
                    elif alea.isNpc("Anna") and random.randint(0,99) < 25 and enableMiror:
                        alea = copy.deepcopy(findAllie("Belle"))
                    elif alea.isNpc("Alice") and random.randint(0,99) < 35:
                        alea = copy.deepcopy(findAllie("Alice alt."))
                    alea.changeLevel(lvlMax)

                    alea.stuff = [getAutoStuff(alea.stuff[0],alea),getAutoStuff(alea.stuff[1],alea),getAutoStuff(alea.stuff[2],alea)]
                    if alea.name in ["Alice alt","Alice","Cl??mence","Ruby"]:
                        enableMiror = False
                    elif alea.name == "Belle":
                        for allies in tablAllieTemp[:]:
                            if allies.name in ["Alice","Cl??mence","Ruby"]:
                                try:
                                    tablAllieTemp.remove(allies)
                                except:
                                    logs += "\nCouldn't remove Alice or Clemence from the list, somehow"

                    team2.append(alea)
                    logs += "{0} have been added into team2\n".format(alea.name)

            for enemy in team2:
                for cmpt in tablIsNpcName:
                    if enemy.isNpc(cmpt):
                        dictIsNpcVar[f"{cmpt}"] = True
                        break
        elif bigMap:
            for enemy in team2:
                for cmpt in tablIsNpcName:
                    if enemy.isNpc(cmpt):
                        dictIsNpcVar[f"{cmpt}"] = True
                        break
            danger = 100 + 5*starLevel
        # Temp Anniversary Add
        if not(octogone) and not(procurFight):
            today = (now.day,now.month)
            for tmp in tablAllAllies:
                if today == tmp.birthday:
                    ent = copy.deepcopy(tmp)
                    ent.changeLevel(55+random.randint(0,14))
                    team1.append(ent)

        # Updating the Danger and Team Fighting status
        if octogone:
            danger=100
        else:
            winStreak = teamWinDB.getVictoryStreak(team1[0])

        tablTeam,tablEntTeam,cmpt = [team1,team2],[[],[]],0
        readyMsg,cmpt,nbHealers = None,0, [0,0]

        for a in [0,1]:                 # Entities generations and stats calculations
            for b in tablTeam[a]:
                if auto == False and b.species != 3:
                    try:
                        await bot.fetch_user(b.owner)
                        ent = entity(cmpt,b,a,auto=False,dictInteraction=dictIsNpcVar)
                    except:
                        ent = entity(cmpt,b,a,danger=danger,dictInteraction=dictIsNpcVar)
                else:  
                    ent = entity(cmpt,b,a,danger=danger,dictInteraction=dictIsNpcVar)

                tablEntTeam[a].append(ent)
                ent.recalculate()
                await ent.getIcon(bot=bot)

                if not(haveMultipleHealers[a]) and type(ent.char) not in [octarien, invoc]:
                    nbSkill, nbHealSkill = 0,0
                    for skilly in ent.char.skills:
                        if type(skilly) == classes.skill:
                            nbSkill += 1
                            if skilly.type in [TYPE_HEAL, TYPE_INDIRECT_HEAL]:
                                nbHealSkill += 1
                    
                    if nbHealSkill >= nbSkill//2:
                        nbHealers[a] += 1
                        if nbHealers[a] >= [2,4][bigMap]:
                            haveMultipleHealers[a] = True
                cmpt+=1

        emby = await getRandomStatsEmbed(bot,team1,text=["Chargement...","Combat rapide en cours de g??n??ration..."][int(auto)])
        if msg == None:
            try:
                msg = await ctx.send(embed = await getRandomStatsEmbed(bot,team1,text=["Chargement...","Combat rapide en cours de g??n??ration..."][int(auto)]))
            except:
                timeWHoraire = now + horaire
                footerText = "/fight de {0}#{1} ({2}:{3})".format(ctx.author.name,ctx.author.discriminator,["0{0}".format(timeWHoraire.hour),timeWHoraire.hour][timeWHoraire.hour>9],["0{0}".format(timeWHoraire.minute),timeWHoraire.minute][timeWHoraire.minute>9])
                msg = await ctx.channel.send(embed = emby.set_footer(text=footerText,icon_url=ctx.author.avatar_url))

        else:
            if ctx.channel.last_message_id != msg.id and not(auto):
                await msg.delete()
                timeWHoraire = now + horaire
                footerText = "/fight de {0}#{1} ({2}:{3})".format(ctx.author.name,ctx.author.discriminator,["0{0}".format(timeWHoraire.hour),timeWHoraire.hour][timeWHoraire.hour>9],["0{0}".format(timeWHoraire.minute),timeWHoraire.minute][timeWHoraire.minute>9])
                msg = await ctx.channel.send(embed = emby.set_footer(text=footerText,icon_url=ctx.author.avatar_url))
            else:
                await msg.edit(embed = await getRandomStatsEmbed(bot,team1,text=["Chargement...","Combat rapide en cours de g??n??ration..."][int(auto)]))

        if not(auto):                   # Send the first embed for the inital "Vs" message and start generating the message
            if not(octogone):
                for team in listImplicadTeams:
                    teamWinDB.changeFighting(team,msg.id,ctx.channel.id,team2)

            logs += "\n"
            versus = ""
            for a in [0,1]:
                logs += "\nTeam {0} composition :\n".format(a+1)
                versus+=f"\n__Equipe {a+1} :__\n"
                for b in tablEntTeam[a]:
                    versus+=f"{b.icon} {b.char.name}\n"
                    logs += "{0}\n".format(b.char.name)

        for ent in tablEntTeam[0]:
            if type(ent.char) == tmpAllie:
                for tmpName, tmpStats in procurTempStuff.items():
                    if ent.char.name == tmpName:
                        tempMsg, allStats = "\n{0} (lvl {1})\n".format(ent.char.name,ent.char.level), ent.allStats()+[ent.resistance,ent.percing,ent.critical]
                        for cmpt in range(len(allStats)):
                            tempMsg += "{0} : {1}".format(allStatsNames[cmpt][:3],allStats[cmpt])
                            if cmpt != len(allStats) - 1:
                                tempMsg += ", "
                        logs += tempMsg

        # Placement phase -----------------------------------------------------
        logs += "\n=========\nInitial placements phase\n=========\n\n"
        tablLineTeamGround, placementlines, allAuto, maxPerLine = [[0,1,2],[3,4,5]], [[[],[],[]],[[],[],[]]], True, [5,7][bigMap]

        for actTeam in [0,1]:               # Sort the entities and place them
            melee, dist, snipe, lenMel, lenDist, lenSnip = [],[],[],0,0,0

            for b in tablEntTeam[actTeam]:
                verif = b.char.weapon.range
                if verif == 0:
                    melee += [b]
                    lenMel += 1
                elif verif == 1:
                    dist += [b]
                    lenDist += 1
                else:
                    snipe += [b]
                    lenSnip += 1

            tablEntOnLine,tablNbEntOnLine = [[snipe,dist,melee],[melee,dist,snipe]][actTeam],[[lenSnip,lenDist,lenMel],[lenMel,lenDist,lenSnip]][actTeam]

            for b in [[2,1],[0,1]][actTeam]:
                if tablNbEntOnLine[b] > maxPerLine:
                    tablEntOnLine[b+[-1,1][actTeam]] += tablEntOnLine[b][maxPerLine-1:]
                    tablEntOnLine[b] = tablEntOnLine[b][0:maxPerLine]

            if tablNbEntOnLine[[0,2][actTeam]] > maxPerLine:
                tablEntOnLine[1] += tablEntOnLine[[0,2][actTeam]][maxPerLine-1:]
                tablEntOnLine[[0,2][actTeam]] = tablEntOnLine[[0,2][actTeam]][:maxPerLine]

                if len(tablEntOnLine[1]) > maxPerLine:
                    random.shuffle(tablEntOnLine[1])
                    tablEntOnLine[[2,0][actTeam]] += tablEntOnLine[1][maxPerLine-1:]
                    tablEntOnLine[1] = tablEntOnLine[1][:maxPerLine]
            
            if actTeam == 0:
                placementlines[actTeam]=[snipe,dist,melee]
            else:
                placementlines[actTeam]=[melee,dist,snipe]

            tablNbEntOnLine[0],tablNbEntOnLine[1],tablNbEntOnLine[2],lineVal, unplaced = len(tablEntOnLine[0]),len(tablEntOnLine[1]),len(tablEntOnLine[2]),0, []

            for xLinePos in tablLineTeamGround[actTeam]:
                random.shuffle(tablEntOnLine[lineVal])

                if not(bigMap):
                    if (actTeam == 1 and xLinePos % 3 == 0) or (actTeam == 0 and xLinePos % 3 == 2):
                        tablSetPos = [
                                [],
                                [2],
                                [1,3],
                                [1,2,3],
                                [0,1,3,4],
                                [0,1,2,3,4]
                            ]

                        try:
                            if len(tablEntOnLine[lineVal]) != len(tablSetPos[len(tablEntOnLine[lineVal])]):
                                raise Exception((len(tablEntOnLine[lineVal]),len(tablSetPos[len(tablEntOnLine[lineVal])])))
                        except:
                            first = "\nlen(tablEntOnLine[lineVal]) = "
                            if lineVal < len(tablEntOnLine):
                                first += str(len(tablEntOnLine[lineVal]))
                            else:
                                first += "__OoR__"
                            second = "\nlen(tablSetPos[len(tablEntOnLine[lineVal])]) = "
                            if lineVal < len(tablEntOnLine) and len(tablEntOnLine[lineVal]) < len(tablSetPos):
                                second += str(len(tablSetPos[len(tablEntOnLine[lineVal])]))
                            else:
                                second += "__OoR__"
                            await msg.edit(embed=discord.Embed(title="__Error during placement phase__",description=format_exc()+"\ncmpt = {0}\nlen(tablEntOnLine) = {1}\nlen(tablSetPos) = {2}{3}{4}\n\nFinghting status reset".format(lineVal,len(tablEntOnLine),len(tablSetPos),first,second)))
                            for team in listImplicadTeams:
                                teamWinDB.changeFighting(team,0)
                            return 0
                        for pos in range(len(tablSetPos[len(tablEntOnLine[lineVal])])):
                            tablEntOnLine[lineVal][pos].move(y=tablSetPos[len(tablEntOnLine[lineVal])][pos],x=xLinePos)
                            logs += "{0} moved from {1}:{2} to {3}:{4}\n".format(tablEntOnLine[lineVal][pos].char.name,0,0,xLinePos,tablSetPos[len(tablEntOnLine[lineVal])][pos])

                    else:
                        if tablNbEntOnLine[lineVal] == 1:
                            tablEntOnLine[lineVal][0].move(y=random.randint(1,3),x=xLinePos)
                            logs += "{0} moved from {1}:{2} to {3}:{4}\n".format(tablEntOnLine[lineVal][0].char.name,0,0,xLinePos,2)

                        else:
                            tabl = [0,1,2,3,4]

                            for cmpt2 in range(tablNbEntOnLine[lineVal]):
                                if len(tabl) > 1:
                                    rand = random.randint(0,len(tabl)-1)
                                else:
                                    rand = 0
                                if len(tabl) <= 0:
                                    unplaced.append(tablEntOnLine[lineVal][cmpt2])
                                else:
                                    ruby = tabl[rand]
                                    tabl.remove(ruby)
                                    tablEntOnLine[lineVal][cmpt2].move(y=ruby,x=xLinePos)
                                    logs += "{0} has been place at {1}:{2}\n".format(tablEntOnLine[lineVal][0].char.name,xLinePos,ruby)

                    if len(unplaced) > 0:
                        emptyCells = [[],[]]
                        for celly in tablAllCells:
                            if celly.on == None:
                                emptyCells[celly.x > 2].append(celly)

                        for ent in unplaced:
                            if len(emptyCells[ent.team]) > 1:
                                rdmCell = emptyCells[ent.team][random.randint(0,len(emptyCells[ent.team])-1)]
                            else:
                                rdmCell = emptyCells[ent.team][0]
                            
                            ent.move(cellToMove=rdmCell)
                            emptyCells[ent.team].remove(rdmCell)
                            logs += "{0} has been randomly placed at {1}:{2}\n".format(ent.char.name,rdmCell.x,rdmCell.y)
                else:
                    prePos = [
                        [   # Team 1 set pos
                            [[0,3],[1,2],[2,1],[3,0],[1,4],[2,5],[3,6]],
                            [[1,3],[2,2],[3,1],[4,0],[2,4],[3,5],[4,6]],
                            [[2,3],[3,2],[4,1],[5,0],[3,4],[4,5],[5,6]]
                        ],
                        [   # Team 2 set pos
                            [[3,3]],
                            [[4,3]],
                            [[5,3]]
                        ]
                    ][actTeam]

                    for cmpt in range(len(tablEntOnLine[lineVal])):
                        if len(prePos[lineVal]) > 1:
                            rand = random.randint(0,len(prePos[lineVal])-1)
                        else:
                            rand = 0
                        ruby = prePos[lineVal][rand]
                        prePos[lineVal].remove(ruby)
                        tablEntOnLine[lineVal][cmpt].move(y=ruby[1],x=ruby[0])
                        logs += "{0} has been place at {1}:{2}\n".format(tablEntOnLine[lineVal][0].char.name,ruby[0],ruby[1])

                lineVal += 1

        if not(auto):                       # Edit the Vs embed for his message
            repEmb = discord.Embed(title = "__Ce combat oppose :__",color = light_blue, description="{0}\n\n__Carte__ :\n{1}".format(versus,map(tablAllCells,bigMap)))
            repEmb.add_field(name = "__Taux de danger :__",value=danger,inline=False)
            if footerText != "":
                repEmb.set_footer(text=footerText,icon_url=ctx.author.avatar_url)
            await msg.edit(embed = repEmb)

        choiceMsg = 0
        if not(auto):                       # User there ?
            allReady = False
            already, awaited,awaitedChar = [],[],[]

            readyMsg = await ctx.channel.send(embed= await getRandomStatsEmbed(bot,team1))

            for a in tablEntTeam: # G??n??ration du tableau des utilisateurs devant confirmer leur pr??sence
                for b in a:
                    if b.auto == False:
                        owner = None
                        try:
                            owner = await ctx.guild.fetch_member(b.char.owner)
                        except:
                            b.auto = True
                        
                        if owner != None:
                            awaitedChar += [b]
                            awaited += [owner]

            dateLimite = datetime.now() + timedelta(seconds=15)
            while not(allReady): # Demande aux utilisateurs de confirmer leur pr??sence
                readyEm = discord.Embed(title = "Combat manuel",color=light_blue)
                readyEm.set_footer(text="Les utilisateurs n'ayant pas r??agis dans les 15 prochaines secondes seront consid??r??s comme combattant automatiques")
                temp,temp2 = "",""
                for a in already:
                    temp2+= a.mention + ", "
                    
                if temp2 == "":
                    temp2 = "-"

                for a in awaited:
                    temp += a.mention + ", "

                readyEm.add_field(name = "Pr??ts :",value = temp2,inline = False)
                readyEm.add_field(name = "En attente de :",value = temp,inline = False)
                await readyMsg.edit(embed = readyEm)
                await readyMsg.add_reaction(emoji.check)

                def checkIsIntendedUser(reaction,user):
                    mes = reaction.message == readyMsg and str(reaction) == emoji.check

                    for a in awaited:
                        if user == a and mes:
                            return True

                try:
                    timeLimite = (dateLimite - datetime.now()).total_seconds()
                    react = await bot.wait_for("reaction_add",timeout = timeLimite,check = checkIsIntendedUser)
                except:
                    break

                awaited.remove(react[1])
                already += [react[1]]
                allAuto = False

                if choiceMsg == 0:
                    choiceMsg = await ctx.channel.send(embed=await getRandomStatsEmbed(bot,team1,"Fen??tre de s??lection de l'action"))

                if awaited == []:
                    allReady = True


            await readyMsg.clear_reactions()
            temp,awaitNum,temp2= "",len(awaited),""
            if awaitNum == 1:
                temp = awaited[0].mention
            elif awaitNum == 2:
                temp = f"{awaited[0].mention} et {awaited[1].mention}"
            elif awaitNum != 0:
                for a in range(0,awaitNum-2):
                    temp+=f"{awaited[a].mention}, "
                temp += f"{awaited[a+1].mention} et {awaited[a+2].mention}"
            else:
                temp = "-"

            if awaitNum != 0:
                temp2 = f"\n\n{temp} seront consid??r??s comme combattants automatiques"
            statingEmb = discord.Embed(title = "Initialisation",color = light_blue,description = f"Le combat va commencer {emoji.loading}{temp2}")

            await readyMsg.edit(embed = statingEmb)

            for z in awaitedChar:
                for b in awaited:
                    if b.id == int(z.char.owner):
                        z.auto = True
                        break

        # Timeline's initialisation -----------------------------------------
        tempTurnMsg = "__D??but du combat :__"
        if not(auto):
            turnMsg = readyMsg
            await turnMsg.clear_reactions()
        time = timeline()
        time, tablEntTeam = time.init(tablEntTeam)

        logs += "\n=========\nStuffs passives effects phase\n=========\n\n"
        for team in [0,1]:                                  # Says Start
            for ent in tablEntTeam[team]:
                if tablEntTeam[1][0].isNpc("The Giant Enemy Spider") and (ent.isNpc("Alice") or ent.isNpc("F??licit??") or ent.isNpc("Lohica")):
                    tempTurnMsg += "\n{0} : *\"{1}\"*".format(ent.icon,"!?")
                    arch = classes.effect("Arachnophobie","archacnophobia",type=TYPE_MALUS,strength=-int(ent.baseStats[STRENGTH]*0.2),charisma=-int(ent.baseStats[CHARISMA]*0.2),magie=-int(ent.baseStats[MAGIE]*0.2),agility=-int(ent.baseStats[AGILITY]*0.2),intelligence=-int(ent.baseStats[INTELLIGENCE]*0.2),turnInit=-1,unclearable=True)
                    tempTurnMsg += add_effect(tablEntTeam[1][0],ent,arch)
                    ent.refreshEffects()

                elif ent.char.says.start != None and random.randint(0,99)<33:
                    if ent.isNpc("Alice"):                          # Alice specials interractions
                        if dictIsNpcVar["H??l??ne"]:                                    # Helene in the fight
                            tempTurnMsg += "\n{0} : *\"{1}\"*".format(ent.icon,"__Arf, pourquoi je dois faire ??quipe avec elle d??j?? (??????0???) ?__")
                            if dictIsNpcVar["Cl??mence"]:
                                if random.randint(0,99) < 50:
                                    tempTurnMsg += "\n{0} : *\"{1}\"*".format('<:clemence:908902579554111549>',"__S'il te plait Alice, commence pas... Elle fait m??me pas le m??me taff que toi.__")
                                    if dictIsNpcVar["Lena"]:
                                        tempTurnMsg += "\n{0} : *\"{1}\"*".format('<:lena:909047343876288552>',"Je sais que c'est tentant de se parler avec des ultra-sons quand on a votre ou??e, mais si vous p??uviez plut??t vous concentrer sur le combat ce sera cool")
                                else:
                                    tempTurnMsg += "\n{0} : *\"{1}\"*".format('<:clemence:908902579554111549>',"Je l'ai entendue celle l?? !")
                    
                        elif dictIsNpcVar["F??licit??"] and dictIsNpcVar["Sixtine"] and dictIsNpcVar["Cl??mence"]:         # All sisters in the fight
                            tempTurnMsg += "\n{0} : *\"{1}\"*".format(ent.icon,"Allez ! Un p'tit combat en famille !")

                        elif dictIsNpcVar["F??licit??"] or dictIsNpcVar["Sixtine"]:                         # A sister in the fight (except Cl??mence)
                            tempMsg = "Allez F??li ! On fonce !"
                            if dictIsNpcVar["Sixtine"]:
                                tempMsg = "Courrage Sixtine ! ??a va aller !"

                            tempTurnMsg += "\n{0} : *\"{1}\"*".format(ent.icon,tempMsg)
                        elif dictIsNpcVar["Stella"]:
                            tempTurnMsg += "\n{0} : *\"Il est hors de question que je la laise gagner.\"*".format(ent.icon)
                        elif dictIsNpcVar["Anna"]:
                            tempTurnMsg += "\n{0} : *\"Tiens coucou Anna. Tu passeras le bonjour de ma part ?? ta soeur !\"*".format(ent.icon)
                            if random.randint(0,99) < 50:
                                tempTurnMsg += "\n<:anna:943444730430246933> : *\"Elle sera contente\"*"
                            else:
                                tempTurnMsg += "\n<:anna:943444730430246933> : *\"Elle aura pr??f??r?? que ton reflet le fasse directement, mais je lui passerais le message, t'en fais pas\"*"
                        else:
                            tempTurnMsg += "\n{0} : *\"{1}\"*".format(ent.icon,ent.char.says.start)

                    elif ent.isNpc("Cl??mence"):                     # Cl??mence specials interractions
                        if dictIsNpcVar["Alice"] or dictIsNpcVar["F??licit??"] or dictIsNpcVar["Sixtine"]:          # With her sisters
                            tempTabl = []
                            if dictIsNpcVar["Alice"]:
                                tempTabl.append("H?? Alice, ??a va ??tre le moment de tester tes comp??tences non ?")
                            if dictIsNpcVar["F??licit??"]:
                                tempTabl.append("Surtout, oublie pas de *pas* en faire trop F??li")
                            if dictIsNpcVar["Sixtine"]:
                                tempTabl.append("Sixtine, je devrais avoir ramenn?? des vielles peintures, ??a t'interresse de regarder ??a apr??s le combat ?")

                            rand = tempTabl[random.randint(0,len(tempTabl)-1)]
                            tempTurnMsg += "\n{0} : *\"{1}\"*\n".format(ent.icon,rand)

                            if rand == "Sixtine, je devrais avoir ramenn?? des vielles peintures, ??a t'interresse de regarder ??a apr??s le combat ?":
                                if random.randint(0,99) < 50:
                                    tempTurnMsg += "{0} : *\"{1}\"*\n".format('<:sixtine:908819887059763261>',"Oh heu... Je comptais plut??t faire une sieste apr??s moi...")
                                    tempTurnMsg += "{0} : *\"{1}\"*\n".format(ent.icon,"Pas de soucis")
                                else:
                                    tempTurnMsg += "{0} : *\"{1}\"*\n".format('<:sixtine:908819887059763261>',"Oh heu... Pourquoi pas...")

                        elif dictIsNpcVar["Ruby"]:
                            tempTurnMsg += "\n{0} : *\"Oh Madame Ruby, j'esp??re que vous comptez pas juger mes comp??tences durant ce combat\"*".format(ent.icon)
                            randy = random.randint(0,99)
                            if randy < 33:
                                tempTurnMsg += "\n<:ruby:958786374759251988> : *\"`Ricane` Tu as peur que je pense que tu as r??gr??ss?? ?\"*"
                            elif randy < 66:
                                tempTurnMsg += "\n<:ruby:958786374759251988> : *\"Tu sais bien que je suis toujours interres??e par tes progr??s\"*"
                            elif dictIsNpcVar["John"]:
                                tempTurnMsg += "\n<:ruby:958786374759251988> : *\"Je suis plut??t l?? pour surveiller un certain loup garou aujourd'hui\"*"
                                if random.randint(0,99) < 60:
                                    tempTurnMsg += "\n<:john:908887592756449311> : *`Ne se sens pas vraiment ?? l'aise avec les auras des deux puissantes vampires cotes ?? cotes`*"
                        else:
                            tempTurnMsg += "\n{0} : *\"{1}\"*".format(ent.icon,ent.char.says.start)

                    elif ent.isNpc("Shushi"):                       # Shushi specials interractions
                        if dictIsNpcVar["Lena"]:
                            tempTurnMsg += "\n{0} : *\"{1}\"*".format(ent.icon,"Allez Miman ! Ti va touz les d??fonzer !")
                            if random.randint(0,99) < 50:
                                if random.randint(0,99) < 50:
                                    tempTurnMsg += "\n{0} : *\"{1}\"*".format('<:lena:909047343876288552>',"Voyons Shushi, c'est quoi ce language ?")
                                else:
                                    tempTurnMsg += "\n{0} : *\"{1}\"*".format('<:lena:909047343876288552>',"`Ricane`")

                        else:
                            tempTurnMsg += "\n{0} : *\"{1}\"*".format(ent.icon,ent.char.says.start)

                    elif ent.isNpc("Shihu"):                        # Shihu specials interractions
                        if dictIsNpcVar["Lena"]:
                            tempTurnMsg += "\n{0} : *\"{1}\"*".format(ent.icon,"Z'est le doit au Boum Boum ?")
                            tempTurnMsg += "\n{0} : *\"{1}\"*".format('<:lena:909047343876288552>',"`Ricane` Allez vas-y")
                        else:
                            tempTurnMsg += "\n{0} : *\"{1}\"*".format(ent.icon,ent.char.says.start)

                    elif ent.isNpc("John") and dictIsNpcVar["Cl??mence"] and random.randint(0,99) < 50:
                        tempTurnMsg += "\n{0} : *\"{1}\"*".format(ent.icon,"D-Dit Cl??mence, ??a te dirais une balade sous la pleine lune avec moi apr??s ??a ?")
                        tempTurnMsg += "\n<:clemence:908902579554111549> : *\"Hum ? Oh heu... Pourquoi pas ??coute\"*"

                    elif ent.isNpc("Stella") and dictIsNpcVar["Alice"]:
                        tempTurnMsg += "\n{0} : *\"Va te faire voir toi, c'est mon terrain de jeu ici !\"*".format(ent.icon)

                    else:
                        tempTurnMsg += "\n{0} : *\"{1}\"*".format(ent.icon,ent.char.says.start)

        if tempTurnMsg != "__D??but du combat :__":
            tempTurnMsg += "\n"

        nbLB, LBBars = [8,8], [[0,0],[0,0]]

        # Passives skills and stuffs effects ---------------------------------
        for team in [0,1]:
            teamHasLb = False
            for ent in tablEntTeam[team]:
                listEffGiven, listEffGiver = [],[]                
                if not(octogone) and type(ent.char) == tmpAllie and ent.team == 1:
                    for allyTmpName, allyBalancingEff in tmpBalancingDict.items():
                        if ent.char.name.lower() == allyTmpName.lower():
                            add_effect(ent,ent,allyBalancingEff)
                            listEffGiven.append(allyBalancingEff.emoji[ent.char.species][ent.team])
                            listEffGiver.append('<:lenapy:979953598807031918>')

                for skil in ent.char.skills:
                    if type(skil) == skill:
                        if skil.type == TYPE_PASSIVE or skil.jaugeEff != None:               # If the entity have a passive
                            effect=[findEffect(skil.effectOnSelf),findEffect(skil.jaugeEff)][skil.jaugeEff!=None]
                            temp = add_effect(ent,ent,effect," ({0})".format(skil.name),danger=danger)
                            if '????' not in temp:
                                listEffGiven.append(effect.emoji[ent.char.species-1][ent.team])
                                listEffGiver.append(skil.emoji)
                                logs += "{0} get the {1} effect from {2}\n".format(ent.char.name,effect.name,skil.name)

                        if skil.id == trans.id:
                            teamHasLb = True

                        elif skil.id == divineAbne.id:
                            ent.maxHp = int(ent.maxHp * (1-skil.power/100))
                            ent.hp = copy.deepcopy(ent.maxHp)
                        elif skil.id == plumRem.id:
                            ent.char.weapon = plume2
                for equip in [ent.char.weapon,ent.char.stuff[0],ent.char.stuff[1],ent.char.stuff[2]]:       # Look at the entity stuff to see if their is a passive effect
                    if equip.effect != None:
                        if equip.effect == "mk":            # Constitution
                            effect=const
                            for z in tablEntTeam[ent.team]:
                                z.maxHp = int(z.maxHp*(1+const.power/100))
                                z.hp = z.maxHp

                                add_effect(ent,z,effect," ({0} - {1})".format(equip.name,ent.char.name))
                                
                                logs += "{0} gave the {1} effect at {2} for {3} turn(s)\n".format(ent.char.name,effect.name,z.char.name,effect.turnInit)
                                z.refreshEffects()

                            tempTurnMsg += "\n{0} ({1}) a donn?? l'effet de __{2}__ (<:co:888746214999339068>) ?? son ??quipe ({3})".format(ent.char.name,ent.icon,effect.name,equip.name)
                        else:                           # Any other effects
                            effect=findEffect(equip.effect)
                            temp = add_effect(ent,ent,effect," ({0})".format(equip.name),danger=danger)
                            if '????' not in temp:
                                listEffGiven.append(effect.emoji[ent.char.species-1][ent.team])
                                listEffGiver.append(equip.emoji)
                                logs += "{0} get the {1} effect from {2}\n".format(ent.char.name,effect.name,equip.name)

                if ent.char.name in upLifeStealNames:
                    for cmpt in range(len(upLifeStealNames)):
                        if ent.char.name == upLifeStealNames[cmpt]:
                            add_effect(ent,ent, upLifeStealEff[cmpt],danger=danger)

                ent.refreshEffects()
                if listEffGiven != []:
                    tempTurnMsg += "\n{0} ".format(ent.icon)
                    for equip in listEffGiver:
                        tempTurnMsg += equip
                    tempTurnMsg += " ??? "
                    for equip in listEffGiven:
                        tempTurnMsg += equip

                for bosses in tablBoss+tablRaidBoss:
                    if bosses.name == ent.name:
                        LBBars[0][0] += 1
                        if ent.char.oneVAll:
                            LBBars[0][0] += 1
            if type(tablEntTeam[team][0].char) in [tmpAllie,char]:
                LBBars[team][0] = int(len(tablEntTeam[team])>=8)+int(len(tablEntTeam[team])>=16)+int(type(tablEntTeam[not(team)][0].char) in [tmpAllie,char])
            elif teamHasLb:
                LBBars[team][0] = 1

        if tablEntTeam[1][0].isNpc("The Giant Enemy Spider"):           # Giant Enemy Spider's legs summoning
            surrondingsCells = [findCell(tablEntTeam[1][0].cell.x-1,tablEntTeam[1][0].cell.y-1,tablAllCells),findCell(tablEntTeam[1][0].cell.x-1,tablEntTeam[1][0].cell.y,tablAllCells),findCell(tablEntTeam[1][0].cell.x-1,tablEntTeam[1][0].cell.y+1,tablAllCells),findCell(tablEntTeam[1][0].cell.x,tablEntTeam[1][0].cell.y-1,tablAllCells),findCell(tablEntTeam[1][0].cell.x,tablEntTeam[1][0].cell.y+1,tablAllCells),findCell(tablEntTeam[1][0].cell.x+1,tablEntTeam[1][0].cell.y-1,tablAllCells),findCell(tablEntTeam[1][0].cell.x+1,tablEntTeam[1][0].cell.y,tablAllCells),findCell(tablEntTeam[1][0].cell.x+1,tablEntTeam[1][0].cell.y+1,tablAllCells)]
            tablTemp = [TGESL1,TGESL2]
            for cmpt in range(8):
                toSummon = copy.deepcopy(tablTemp[cmpt//4])
                toSummon.name += " {0}".format(cmpt)
                tablEntTeam, tablAliveInvoc, time, funnyTempVarName = tablEntTeam[1][0].summon(toSummon,time,surrondingsCells[cmpt],tablEntTeam,tablAliveInvoc,ignoreLimite=True)
                logs += "\n"+funnyTempVarName

        elif tablEntTeam[1][0].isNpc("Jevil"):                          # Jevil Confusiong effect
            for teamCmpt in [0,1]:
                for ent in tablEntTeam[teamCmpt]:
                    add_effect(tablEntTeam[1][0],ent,jevilEff)
                    ent.refreshEffects()

        elif dictIsNpcVar["Kiku"]:
            kikuEnt = None
            for ent in tablEntTeam[1]:
                if ent.isNpc("Kiku"):
                    kikuEnt=ent
                    break
            for teamCmpt in [0,1]:
                for ent in tablEntTeam[teamCmpt]:
                    add_effect(kikuEnt,ent,kikuRaiseEff)
                    ent.refreshEffects()

        elif dictIsNpcVar["OctoTour"]:
            octoTour = None
            for ent in tablEntTeam[1]:
                if ent.isNpc("OctoTour"):
                    octoTour = ent
                    break

            for ent in tablEntTeam[1]:
                if ent != octoTour:
                    add_effect(octoTour,ent,octoTourEff2)                                        
                    logs += "{0} gave the {1} effect at {2} for {3} turn(s)\n".format(octoTour.char.name,effect.name,ent.char.name,effect.turnInit)
                    ent.refreshEffects()
    
        if contexte != []:                                              # If a contexte list is given
            for a in contexte:                      # Contexte need to be a list of lists
                if a[0] == ALL:
                    for b in [0,1]:
                        for c in tablEntTeam[b]:
                            tempTurnMsg += add_effect(c,c,findEffect(a[1]))
                            
                            c.refreshEffects()

                elif a[0] == TEAM1:
                    for b in tablEntTeam[0]:
                        tempTurnMsg += add_effect(b,b,findEffect(a[1]))
                        
                        b.refreshEffects()

                elif a[0] == TEAM2:
                    for b in tablEntTeam[1]:
                        tempTurnMsg += add_effect(b,b,findEffect(a[1]))
                        
                        b.refreshEffects()

        for team in [0,1]:                                                 # Raise skills verifications
            for ent in tablEntTeam[team]:
                for skilly in ent.char.skills + ent.effect:
                    if type(skilly)==skill:
                        if skilly.type in [TYPE_INDIRECT_REZ,TYPE_RESURECTION] or (skilly.effectAroundCaster != None and skilly.effectAroundCaster[0] == TYPE_RESURECTION):
                            for ent2 in tablEntTeam[team]:
                                ent2.ressurectable = True
                            break

                for eff in ent.effect:
                    if eff.effect.jaugeValue != None :
                        teamJaugeDict[team][ent] = eff
                        break

        if not(auto):                               # Send the turn 0 msg
            if tempTurnMsg == "__D??but du combat :__":
                tempTurnMsg += "\n -"
            emby = discord.Embed(title=f"__Tour {tour}__",description=tempTurnMsg,color = light_blue)
            if footerText != "":
                emby.set_footer(text=footerText,icon_url=ctx.author.avatar_url)
            await turnMsg.edit(embed = emby)
            await asyncio.sleep(2+(min(len(tempTurnMsg),2000)/2000*5))

        fight, ennemi = True, tablEntTeam[1][0]
        # Effective Fight Start --------------------------------------------------------------------------
        try:
            while fight:
                everyoneDead = [True,True]
                actTurn = time.getActTurn()
                nextNotAuto,lastNotAuto = 0,0

                everyoneStillThere = False
                for a in time.timeline : # Looking for the next not auto player
                    if not(a.auto):
                        everyoneStillThere = True
                        if a.hp > 0:
                            nextNotAuto = a
                            break

                if not(everyoneStillThere):
                    allAuto = True

                if nextNotAuto != actTurn and not(auto) and not(allAuto):
                    if lastNotAuto != nextNotAuto:
                        await choiceMsg.edit(embed = discord.Embed(title = "Fen??tre de selection de l'action", color=nextNotAuto.char.color,description = f"En attente du tour de {nextNotAuto.char.name} {emoji.loading}"),components=[])
                        lastNotAuto = nextNotAuto
                    elif nextNotAuto == 0:
                        await choiceMsg.edit(embed = discord.Embed(title = "Fen??tre de selection de l'action", color=light_blue,description = f"Il n'y a plus de combattants manuels en vie"),components=[])
                        lastNotAuto = nextNotAuto

                if allAuto and choiceMsg != 0:
                    await choiceMsg.delete()
                    choiceMsg = 0

                if actTurn.hp > 0:
                    tempTurnMsg = f"__D??but du tour de {actTurn.char.name} :__\n"

                # Sudden death verifications and damages ----------------------------
                if actTurn == time.begin:
                    funnyTempVarName = ""
                    tour += 1
                    logs += "\n\n=========\nTurn {0}\n=========".format(tour)

                    for team in [0,1]:
                        for ent in tablEntTeam[team]:
                            if ent.hp > 0:
                                ent.stats.survival += 1

                                if ent.cell != None:
                                    if ent.cell.on != ent and ent.cell.on == None:
                                        ent.cell.on = ent
                                        print("{0} n'??tait pas sur sa cellule, apparament".format(ent.char.name))
                                else:
                                    raise Exception("{0} n'est pas sur une cellule !!".format(ent.char.name))
                            if dictIsNpcVar["Kiku"] and tour > 1:
                                for eff in ent.effect:
                                    if eff.effect.id == kikuRaiseEff.id:
                                        eff.effect.power = min(round(eff.effect.power*1.2,2),200)

                        if LBBars[team][0] > 0:
                            LBBars[team][1] = min(LBBars[team][1]+1,LBBars[team][0]*3)
                    if tour == 16 and dictIsNpcVar["Kiku"]:
                        kikuEnt = None
                        for b in tablEntTeam[1]:
                            if b.isNpc("Kiku"):
                                kikuEnt = b
                                break
                        for a in [0,1]:
                            for b in tablEntTeam[a]:
                                if b.hp > 0:
                                    for eff in b.effect:
                                        if eff.effect.id == kikuRaiseEff.id:
                                            ballerine, chocolatine = kikuEnt.attack(target=b,value = 999,icon = eff.icon,area=AREA_MONO,sussess=666,use=MAGIE,onArmor = 100, execution = True)
                                            funnyTempVarName += ballerine

                        if not(auto):
                            if len(funnyTempVarName) > 4096:
                                funnyTempVarName = unemoji(funnyTempVarName)
                                if len(funnyTempVarName) > 4096:
                                    funnyTempVarName = "OVERLOAD"
                            await turnMsg.edit(embed = discord.Embed(title=f"__Tour {tour}__",description=funnyTempVarName))
                            await asyncio.sleep(2+(min(len(funnyTempVarName),2000)/2000*5))

                    if tour >= 21:
                        funnyTempVarName += f"\n__Mort subite !__\nTous les combattants perdent **{SUDDENDEATHDMG*(tour-20)}%** de leurs PV maximums\n"
                        for a in [0,1]:
                            for b in tablEntTeam[a]:
                                if b.hp > 0:
                                    if type(b.char) == octarien and b.char.oneVAll:
                                        lose = int(b.maxHp*((SUDDENDEATHDMG/1000)*(tour-20)))
                                    else:
                                        lose = int(b.maxHp*((SUDDENDEATHDMG/100)*(tour-20)))
                                    funnyTempVarName += "{0} : -{1} PV\n".format(b.icon,lose)
                                    b.hp -= lose
                                    b.stats.selfBurn += lose
                                    if b.hp <= 0:
                                        funnyTempVarName += b.death(killer=b,trueDeath=True)
                                    for skil in range(len(b.char.skills)):
                                        if type(b.char.skills[skil]) == skill and b.char.skills[skil].type in [TYPE_RESURECTION,TYPE_INDIRECT_REZ]:
                                            b.cooldowns[skil] = 99

                        if not(auto):
                            if len(funnyTempVarName) > 4096:
                                funnyTempVarName = unemoji(funnyTempVarName)
                                if len(funnyTempVarName) > 4096:
                                    funnyTempVarName = "OVERLOAD"
                            await turnMsg.edit(embed = discord.Embed(title=f"__Tour {tour}__",description=funnyTempVarName))
                            await asyncio.sleep(2+(min(len(funnyTempVarName),2000)/2000*5))

                        logs += funnyTempVarName
                # Dead team check --------------------------------
                for c in [0,1]:
                    for d in tablEntTeam[c]:
                        if d.hp > 0 and type(d.char) != invoc:
                            everyoneDead[c] = False
                            break

                if everyoneDead[0] or everyoneDead[1]:
                    break

                # Random fight emoji roll -----------------------
                if random.randint(0,99) <= 10:
                    rdmEmoji= randomEmojiFight[random.randint(0,lenRdmEmojiFight-1)]
                else:
                    rdmEmoji= '<:turf:810513139740573696>'

                # Generating the first part of the main message -
                if not(auto):
                    embInfo = discord.Embed(title = "__Combat {0} (D.{1})__".format(rdmEmoji,danger),color = mainUser.color,description="__Carte__ :\n{0}\n__Timeline__ :\n{1}\n<:em:866459463568850954>".format(map(tablAllCells,bigMap),time.icons()))
                    if footerText != "":
                        embInfo.set_footer(text=footerText,icon_url=ctx.author.avatar_url)

                # Start of the turn ---------------------------------------------------------------------------------
                wasAlive = actTurn.hp > 0
                temp,atRange = "",actTurn.atRange()
                nbTargetAtRange = len(atRange)
                if wasAlive:
                    logs += "\n\nTurn {0} - {1}:".format(tour,actTurn.char.name)
                potgDamages,potgKills,potgHeal,potgRaises, potgArmored = [], [], [], [], []
                for cmpt in (0,1,2,3,4):
                    for team in (0,1):
                        temp = []
                        for ent in tablEntTeam[team]:
                            if type(ent.char)!=invoc:
                                temp.append((ent.id,copy.deepcopy([ent.stats.damageDeal,ent.stats.ennemiKill,ent.stats.heals,ent.stats.allieResurected,ent.stats.armoredDamage][cmpt])))
                        temp = dict(temp)
                        [potgDamages,potgKills,potgHeal,potgRaises,potgArmored][cmpt].append(temp)

                funnyTempVarName = actTurn.startOfTurn(tablEntTeam=tablEntTeam)
                tempTurnMsg += funnyTempVarName
                logs += "\n"+funnyTempVarName
                deathCount = bigRaiseCount = 0

                # Main messages statistics generation ---------------------------------------------------------------
                if not(auto) and (wasAlive or actTurn.hp > 0):
                    infoOp,cmpt,temp = [],0, ""
                    for a in [0,1]:     # Generating the Hp's select menu
                        for b in tablEntTeam[a]:
                            if type(b.char) != invoc:
                                raised = ""
                                if b.status == STATUS_RESURECTED:
                                    raised = " (R??anim??{0})".format(["","e"][b.char.gender == GENDER_FEMALE])
                                armorValue = 0
                                for eff in b.effect:
                                    if eff.type == TYPE_ARMOR:
                                        armorValue += eff.value
                                
                                armorTxt, armorPurcent = "", ""
                                if armorValue > 0:
                                    armorTxt = " +{0} PAr".format(separeUnit(armorValue))
                                    armorPurcent = " +{0}%".format(int(armorValue/b.maxHp*100))
                                infoOp += [create_select_option(unhyperlink(b.char.name),str(cmpt),getEmojiObject(b.icon),f"{separeUnit(max(0,b.hp))} PV{armorTxt} ({max(0,round(b.hp/b.maxHp*100))}%{armorPurcent}), R.S. : {b.healResist}%{raised}")]
                            cmpt+=1
                    infoSelect = create_select(infoOp,placeholder="Voir les PVs des combattants")

                    temp2 = actTurn.allStats()+[actTurn.resistance,actTurn.percing]
                    critRate = int((actTurn.agility+actTurn.precision)/200*35)+actTurn.critical
                    temp2 += [critRate]
                    for a in range(0,len(allStatsNames)):               # Generating the stats field of the main message
                        if a == 7:
                            temp += f"\n\n__R??duction de d??g??ts__ : {temp2[a]}%"
                        elif a == 8:
                            temp += f"\n__Taux p??n??tration d'armure__ : {temp2[a]}%"
                        elif a == 9:
                            if actTurn.char.aspiration in [POIDS_PLUME,OBSERVATEUR]:
                                temp2[a] += actTurn.specialVars["aspiSlot"]
                            temp += f"\n__Taux de coup critique__ : {temp2[a]}%"
                        else:
                            temp += f"\n__{allStatsNames[a]}__ : {temp2[a]}"

                    level = str(actTurn.char.level) + ["","<:littleStar:925860806602682369>{0}".format(actTurn.char.stars)][actTurn.char.stars>0]
                    embInfo.add_field(name = f"__{actTurn.icon} {unhyperlink(actTurn.char.name)}__ (Niveau {level})",value=f"PV : {max(0,actTurn.hp)} / {actTurn.maxHp}",inline = False)
                    embInfo.add_field(name = "__Liste des effets :__",value=actTurn.effectIcons(),inline = True)
                    embInfo.add_field(name = "__Statistiques :__",value = temp,inline = True)
                    embInfo.add_field(name = "<:empty:866459463568850954>",value='**__Liste des effets :__**',inline=False)

                    adds = ""

                    for team in [0,1]:                                  # Generating the effects fields of the main message
                        teamView, lbCd = "", 0
                        if LBBars[team][0] > 0:
                            teamView = ["<:noLb:984574607942098964>","<:lb:886657642553032824>"][LBBars[team][0]>0 and LBBars[team][1]>=3]
                            lbCd, barsLb = LBBars[team][1], 0
                            while barsLb < 4:
                                if barsLb < LBBars[team][0]:
                                    if lbCd>=3:
                                        teamView += "<:l3:983450379205378088>"
                                    elif lbCd > 0:
                                        teamView += ["<:l3:983450379205378088>","<:l1:983450416010371183>","<:l2:983450398645977218>"][lbCd%3]
                                    else:
                                        teamView += "<:l0:983450435404849202>"
                                    lbCd = max(0,lbCd-3)
                                else:
                                    teamView += "<:Lbnt:984572258355924992>"
                                barsLb += 1
                            teamView += "\n"
                        teamView2 = ""
                        for ent in tablEntTeam[team]:
                            if type(ent.char) != invoc:
                                teamView2 += ent.lightQuickEffectIcons()

                        if teamView2 == "":
                            teamView += "Pas d'effets sur l'??quipe"
                        else:
                            teamView += teamView2

                        if len(teamView) > 1024:
                            teamView = ""
                            confusingConfusion = None
                            if LBBars[team][0] > 0:
                                teamView = ["<:noLb:984574607942098964>","<:lb:886657642553032824>"][LBBars[team][0]>0 and LBBars[team][1]>=3]
                                lbCd, barsLb = LBBars[team][1], 0
                                while barsLb < LBBars[team][0]:
                                    if lbCd>=3:
                                        teamView += "<:l3:983450379205378088>"
                                    elif lbCd > 0:
                                        teamView += ["<:l3:983450379205378088>","<:l1:983450416010371183>","<:l2:983450398645977218>"][lbCd%3]
                                    else:
                                        teamView += "<:l0:983450435404849202>"
                                    lbCd = max(0,lbCd-3)
                                    barsLb += 1
                                teamView += "\n"
                            for ent in tablEntTeam[team]:
                                if type(ent.char) != invoc and not(confusingConfusion):
                                    bonusCount,malusCount,damageCount,dangerCount,armorCount,healCount,stunCount = 0,0,0,0,0,0,0
                                    if ent.effect != []:
                                        nameCast = ""
                                        for eff in ent.effect:
                                            if eff.effect.id == jevilEff.id:
                                                confusingConfusion = True
                                                break
                                            if not(eff.effect.silent or eff.effect.turnInit == -1) and eff.effect.replica == None:
                                                if eff.effect.type in [TYPE_BOOST,TYPE_INDIRECT_REZ]:
                                                    bonusCount += 1
                                                elif eff.effect.type in [TYPE_INDIRECT_HEAL]:
                                                    healCount += 1
                                                elif eff.effect.type in [TYPE_MALUS]:
                                                    malusCount += 1
                                                elif eff.effect.type in [TYPE_DAMAGE,TYPE_INDIRECT_DAMAGE]:
                                                    damageCount += 1
                                                elif eff.effect.type in [TYPE_ARMOR]:
                                                    armorCount += 1
                                                
                                                if eff.effect.stun:
                                                    stunCount += 1
                                                    nameCast = eff.effect.name

                                            elif eff.effect.replica != None:
                                                dangerCount += 1
                                                nameCast = eff.effect.name

                                        if dangerCount <= 0 and stunCount <= 0 and bonusCount+malusCount+damageCount+armorCount > 0:
                                            teamView += f"{ent.icon} : "
                                            if healCount > 0:
                                                teamView += "????({0})".format(healCount)
                                            if bonusCount > 0:
                                                teamView += f"????({bonusCount})"
                                            if malusCount > 0:
                                                teamView += f"????({malusCount})"
                                            if damageCount > 0:
                                                teamView += f"????({damageCount})"
                                            if armorCount > 0:
                                                teamView += f"???????({armorCount})"
                                            teamView += "\n"
                                        elif dangerCount > 0:
                                            teamView += "{0} : ?????? {1}\n".format(ent.icon,nameCast)
                                        elif stunCount > 0:
                                            teamView += "{0} : ???? {1}\n".format(ent.icon,nameCast)

                            if confusingConfusion:
                                teamView = "<a:giveup:902383022354079814>"
                        if len(teamView) > 1024:        # Still overload
                            teamView = "OVERLOAD !"
                        embInfo.add_field(name= "__??quipe {0} :__".format(["Bleue","Rouge"][team]),value=teamView,inline=True)

                    if teamJaugeDict != [{},{}]:
                        jaugeField = ""
                        for team in [0,1]:
                            for jaugeEnt, jaugeEff in teamJaugeDict[team].items():
                                if jaugeEnt.hp > 0:
                                    jaugeField += "{0} : {1} ".format(jaugeEnt.icon,jaugeEff.icon)
                                    nbFieldEm, cmpt = len(jaugeEff.effect.jaugeValue[0]), 0
                                    nbPointPerField = 100/nbFieldEm
                                    while cmpt * nbPointPerField < jaugeEff.value:
                                        cmpt += 1

                                    if jaugeEff.value - nbPointPerField * (cmpt-1) < (nbPointPerField * cmpt/2) and cmpt > 0:
                                        cmpt -= 1
                                    
                                    jaugeField += jaugeEff.effect.jaugeValue[jaugeEff.value > 25][0]+jaugeEff.effect.jaugeValue[jaugeEff.value>=65][1]+jaugeEff.effect.jaugeValue[jaugeEff.value>=90][2]
                                    
                                    jaugeField += " **{0}**\n".format(jaugeEff.value)
                            
                        if jaugeField:
                            embInfo.add_field(name="__Jauges :__",value=jaugeField,inline=True)

                    # Editing the main message
                    nbTry = 0
                    while 1:
                        try:
                            try:
                                await msg.edit(embed = embInfo,components=[create_actionrow(infoSelect)])
                            except:
                                await msg.edit(embed = embInfo,components=[create_actionrow(create_select([create_select_option("Un ic??ne de personnage n'a pas ??t?? trouv??","0",default=True)],disabled=True))])
                                for team in [0,1]:
                                    for ent in tablEntTeam[team]:
                                        if type(ent.char) == char and ent.hp > 0:
                                            user = loadCharFile("./userProfile/{0}.prof".format(ent.char.owner))
                                            ent.icon = customIconDB.getCustomIcon(user)
                            break
                        except SocketError as e:
                            if e.errno != errno.ECONNRESET:
                                raise
                            else:
                                if nbTry < 5:
                                    await asyncio.sleep(1)
                                    nbTry += 1
                                    errorNb += 1
                                    logs += "\nConnexion error... retrying..."
                                else:
                                    logs += "\nConnexion lost"
                                    raise

                    if nextNotAuto == actTurn:
                        await turnMsg.edit(embed = discord.Embed(title=f"__Tour {tour}__",description=tempTurnMsg,color = actTurn.char.color))

                # Turn actions --------------------------------------------------------------------------------------
                nowStartOfTurn = datetime.now()
                if wasAlive and actTurn.hp <= 0:        # Died from indirect damages at the start
                    if not(auto):
                        if len(tempTurnMsg) > 4096:
                            tempTurnMsg = unemoji(tempTurnMsg)
                            if len(tempTurnMsg) > 4096:
                                tempTurnMsg = "OVERLOAD"

                        await turnMsg.edit(embed = discord.Embed(title=f"__Tour {tour}__",description=tempTurnMsg,color = actTurn.char.color))
                        if type(actTurn.char) != invoc:
                            await asyncio.sleep(2+(min(len(tempTurnMsg),1500)/1500*5))
                        else:
                            await asyncio.sleep(2+(min(len(tempTurnMsg),2000)/2000*5))

                    potgValue = (None,0)
                    for team in (0,1):
                        for ent in tablEntTeam[team]:
                            tempPotgValue = ent.stats.damageDeal-potgDamages[team][ent.id]+(ent.stats.ennemiKill-potgKills[team][ent.id])*ent.char.level*10+ent.stats.heals-potgHeal[team][ent.id]+(ent.stats.allieResurected-potgRaises[team][ent.id])*ent.char.level*10
                            if tempPotgValue > potgValue[1]:
                                potgValue = (ent,tempPotgValue)
                    if potgValue[1] > playOfTheGame[0]:
                        playOfTheGame = [potgValue[1],potgValue[0],discord.Embed(title=f"__Action du combat\nTour {tour}__",description=tempTurnMsg,color = potgValue[0].char.color)]

                # Still alive ===========================
                elif actTurn.hp > 0:
                    cmpt,iteration,replay,allyRea = 0,actTurn.char.weapon.repetition,False,actTurn.stats.allieResurected
                    unsuccess = True

                    # ========== Playing the turn ==============
                    if not(actTurn.stun):                   # The entity isn't stun, so he can play his turn
                        allReadyMove = False
                        while 1:
                            atRange, nbTargetAtRange = actTurn.atRange(), len(actTurn.atRange())
                            onReplica = False
                            for eff in actTurn.effect:
                                if eff.effect.replica != None:
                                    onReplica = eff
                                    eff.decate(turn=1)
                                    actTurn.refreshEffects()
                                    break

                            canMove,cellx,celly = [True,True,True,True],actTurn.cell.x,actTurn.cell.y
                            surrondings = actTurn.cell.surrondings()
                            for a in range(0,len(surrondings)):
                                if surrondings[a] != None:
                                    if surrondings[a].on != None and surrondings[a].on.status != STATUS_TRUE_DEATH:
                                        canMove[a] = False
                                else:
                                    canMove[a] = False

                            # The entity isn't already casting something
                            if onReplica == False:
                                if not(actTurn.auto) :                      # Manual Fighter - Action select window
                                    haveOption,unsuccess, waitingSelect, haveIterate, lbSkill = False,False, create_actionrow(create_select(options=[create_select_option("Veillez patienter...","PILLON!",'????',default=True)],disabled=True)), False, None
                                    def check(m):
                                        return int(m.author_id) == int(actTurn.char.owner) and m.origin_message.id == choiceMsg.id

                                    if LBBars[actTurn.team][0]> 0 and LBBars[actTurn.team][1]//3 >= 1:
                                        if LBBars[actTurn.team][1]//3 == 1:
                                            lbSkill = lb1Tabl[actTurn.char.aspiration]
                                        elif LBBars[actTurn.team][1]//3 == 2:
                                            lbSkill = lb2Tabl[actTurn.char.aspiration]
                                        elif LBBars[actTurn.team][1]//3 == 3:
                                            lbSkill = lb3Tabl[actTurn.char.aspiration]
                                        elif LBBars[actTurn.team][1]//3 == 4:
                                            lbSkill = lb4

                                    while not(haveOption) and not(unsuccess):
                                        choiceMsgTemp,tempTabl,tabltabl,canBeUsed = getPrelimManWindow(actTurn, LBBars, tablEntTeam)+"\n\n__Options disponibles :__\n",[actTurn.char.weapon],[0]+actTurn.cooldowns,[]

                                        if not(actTurn.silent):
                                            for a in actTurn.char.skills:
                                                if type(a) == skill:
                                                    tempTabl.append(a)
                                                else:
                                                    tempTabl.append(None)

                                        if len(actTurn.cell.getEntityOnArea(area=AREA_CIRCLE_1,team=actTurn.team,wanted=ALLIES,fromCell=actTurn.cell)) > 1:
                                            friendlyPush.emoji = ["<:movePlz:928756987532029972>","<a:sparta:928795602328903721>","<a:sparta:928796053585678337>","<a:sparta:928796223215902770>"][random.randint(0,3)]
                                            tempTabl.append(friendlyPush)
                                            tabltabl.append(0)

                                        if actTurn.specialVars["summonerMalus"]:
                                            for thing in range(len(tempTabl)):
                                                if type(tempTabl[thing]) in [skill,weapon] and tempTabl[thing].type != TYPE_SUMMON:
                                                    tempTabl[thing] = None

                                        # Generating the main menu of the window
                                        for a in range(len(tabltabl)):
                                            if tempTabl[a] != None and tabltabl[a] == 0:                                   # If the option is a valid option and the cooldown is down
                                                tablToSee = [tempTabl[a]]
                                                if type(tempTabl[a]) == skill and tempTabl[a].become != None:
                                                    tablToSee, tablEffId = [], []
                                                    for eff in actTurn.effect:
                                                        tablEffId.append(eff.effect.id)

                                                    for cmpt in range(len(tempTabl[a].become)):
                                                        if tempTabl[a].become[cmpt].needEffect == tempTabl[a].become[cmpt].rejectEffect == None:
                                                            tablToSee.append(tempTabl[a].become[cmpt])
                                                        elif tempTabl[a].become[cmpt].rejectEffect == None and tempTabl[a].become[cmpt].needEffect != None:
                                                            fullValid = True
                                                            for bidule in tempTabl[a].become[cmpt].needEffect:
                                                                if bidule.id not in tablEffId:
                                                                    fullValid = False
                                                                    break

                                                            if fullValid:
                                                                tablToSee.append(tempTabl[a].become[cmpt])
                                                        else:
                                                            fullValid = True
                                                            for bidule in tempTabl[a].become[cmpt].rejectEffect:
                                                                if bidule.id in tablEffId:
                                                                    fullValid = False
                                                                    break

                                                            if fullValid:
                                                                tablToSee.append(tempTabl[a].become[cmpt])

                                                for tempOption in tablToSee:                                            
                                                    if type(tempOption) == weapon and len(actTurn.atRange()) > 0 and actTurn.char.weapon.id not in cannotUseMainWeapon:                  # Aff. the number of targets if the option is a Weapon
                                                        canBeUsed += [tempOption]
                                                        choiceMsgTemp += f"{tempOption.emoji} {tempOption.name} (Cibles ?? port??e : {str(nbTargetAtRange)})\n"
                                                    elif type(tempOption) != weapon:
                                                        if type(tempOption) == classes.skill and tempOption.description != None:
                                                            line = tempOption.type in [TYPE_INDIRECT_DAMAGE,TYPE_MALUS,TYPE_DAMAGE,TYPE_DAMAGE]
                                                            target = [ALLIES,ENEMIES][line]
                                                            if len(actTurn.cell.getEntityOnArea(area=tempOption.range,team=actTurn.team,wanted=target,lineOfSight=line,dead=tempOption.type == TYPE_RESURECTION,fromCell=actTurn.cell)) > 0:
                                                                choiceMsgTemp += f"\n{tempOption.emoji} __{tempOption.name} :__\n"
                                                                choiceMsgTemp += "> {0}\n".format(tempOption.description.replace("\n","\n> "))
                                                                canBeUsed += [tempOption]
                                                        else:
                                                            funnyTempVarNameButTheSecond = [TYPE_INDIRECT_DAMAGE,TYPE_MALUS,TYPE_DAMAGE,TYPE_DAMAGE]
                                                            target = ALLIES
                                                            for b in funnyTempVarNameButTheSecond:
                                                                if (tempOption.type == b or tempOption.id == "InfiniteDarkness") and tempOption.id != friendlyPush.id:
                                                                    target = ENEMIES
                                                                    break

                                                            line = tempOption.type in funnyTempVarNameButTheSecond
                                                            if tempOption.range != AREA_MONO:
                                                                if (tempOption.type != TYPE_SUMMON and len(actTurn.cell.getEntityOnArea(area=tempOption.range,team=actTurn.team,wanted=target,lineOfSight=line,dead=tempOption.type == TYPE_RESURECTION,fromCell=actTurn.cell)) > 0) or (tempOption.type == TYPE_SUMMON and tablAliveInvoc[actTurn.team] <3):
                                                                    canBeUsed += [tempOption] 
                                                                    choiceMsgTemp += f"{tempOption.emoji} {tempOption.name}\n"
                                                            else:
                                                                effect = tempOption.effect
                                                                if (tempOption.type != TYPE_SUMMON and len(actTurn.cell.getEntityOnArea(area=tempOption.area,team=actTurn.team,wanted=target,lineOfSight=line,effect=effect,fromCell=actTurn.cell)) > 0) or (tempOption.type == TYPE_SUMMON and tablAliveInvoc[actTurn.team] <3):                                        
                                                                    canBeUsed += [tempOption]
                                                                    choiceMsgTemp += f"{tempOption.emoji} {tempOption.name}\n"

                                        if LBBars[actTurn.team][1]>=3:
                                            line = lbSkill.type in [TYPE_INDIRECT_DAMAGE,TYPE_MALUS,TYPE_DAMAGE,TYPE_DAMAGE]
                                            target = [ALLIES,ENEMIES][line]
                                            if len(actTurn.cell.getEntityOnArea(area=lbSkill.range,team=actTurn.team,wanted=target,lineOfSight=line,dead=lbSkill.type == TYPE_RESURECTION,fromCell=actTurn.cell)) > 0:
                                                choiceMsgTemp += f"\n{lbSkill.emoji} __{lbSkill.name} :__\n"
                                                choiceMsgTemp += "> {0}\n".format(lbSkill.description.replace("\n","\n> "))
                                                canBeUsed += [lbSkill]

                                        choiceMsgTemp += "\n"
                                        if canMove[0] or canMove[1] or canMove[2] or canMove[3]:                           # If the ent. can move, add the Move option
                                            canBeUsed += [option("D??placement",'????')]
                                            choiceMsgTemp += "???? D??placement\n"

                                        canBeUsed += [option("Passer",'????')]                                               # Adding the Pass option, for the dark Sasuke who think that actualy playing the game is to much for them
                                        choiceMsgTemp += "???? Passer"

                                        mainOptions,cmpt = [],0
                                        for a in canBeUsed:                     # Generating the select menu
                                            desc = ""
                                            if type(a) != option:
                                                if type(a) != classes.skill or (type(a) == classes.skill and a.description==None):
                                                    if a.area == AREA_MONO:
                                                        desc = "Monocible"
                                                    else:
                                                        desc = "Zone"

                                                    if type(a) == weapon:
                                                        stat = a.use
                                                        if stat != None and stat != HARMONIE:
                                                            stat = nameStats[a.use]
                                                        elif stat == None:
                                                            stat = "Fixe"
                                                        elif stat == HARMONIE:
                                                            stat = "Harmonie"

                                                        multiple = [""," x{0}".format(a.repetition)][a.repetition > 1]

                                                        desc += f" - {tablTypeStr[a.type]} - {a.power}{multiple} - {stat}"
                                                    else:
                                                        powy = ""
                                                        if a.power > 0:
                                                            stat = a.use
                                                            if stat != None and stat != HARMONIE:
                                                                stat = nameStats[a.use]
                                                            elif stat == None:
                                                                stat = "Fixe"
                                                            elif stat == HARMONIE:
                                                                stat = "Harmonie"
                                                            multiple = [""," x{0}".format(a.repetition)][a.repetition > 1]
                                                            powy = f"{a.power} - {stat}{multiple}"

                                                        desc += f" - {tablTypeStr[a.type]} {powy}"
                                                else:
                                                    desc, toRemove = completlyRemoveEmoji(a.description), ["_","*","|","\n"]
                                                    for letter in toRemove:
                                                        desc = desc.replace(letter,"")
                                                    if len(desc) > 95:
                                                        desc = desc[:95] + "(...)"
                                                mainOptions += [create_select_option(unhyperlink(a.name),str(cmpt),getEmojiObject(a.emoji),desc)]
                                            else:
                                                mainOptions += [create_select_option(unhyperlink(a.name),str(cmpt),a.emoji)]
                                            cmpt += 1

                                        mainSelect = create_select(options=mainOptions,placeholder = "S??l??ctionnez une option :")

                                        if haveIterate:                         # Time limite stuff
                                            await choiceMsg.edit(embed = discord.Embed(title = f"Choix de l'option - {actTurn.icon} {actTurn.char.name}",color = actTurn.char.color,description = choiceMsgTemp),components=[waitingSelect])
                                            await asyncio.sleep(3)

                                        await choiceMsg.edit(embed = discord.Embed(title = f"Choix de l'option - {actTurn.icon} {actTurn.char.name}",color = actTurn.char.color,description = choiceMsgTemp),components=[create_actionrow(mainSelect)])
                                        haveIterate = True

                                        validoption = False
                                        def checkMainOption(m):
                                            return int(m.author.id) == actTurn.char.owner
                                        while not(validoption):
                                            try:
                                                react = await wait_for_component(bot,messages=choiceMsg,check=checkMainOption,timeout = 30)
                                            except:
                                                unsuccess = True
                                                break

                                            mainSelect = create_actionrow(getChoisenSelect(mainSelect,react.values[0]))
                                            react = canBeUsed[int(react.values[0])]
                                            validoption = True

                                        choiceMsgTemp = ""

                                        # Second Menu generating
                                        if type(react) == weapon:
                                            viArea = actTurn.cell.getArea(area=actTurn.char.weapon.effectiveRange,team=actTurn.team,fromCell=actTurn.cell)
                                            for celly in viArea[:]:
                                                if celly.on != None and (celly.on in atRange and celly.on.team != actTurn.team):
                                                    direction = getDirection(actTurn.cell,celly)
                                                    if direction == FROM_LEFT:
                                                        cellToFind = findCell(celly.x+1,celly.y,tablAllCells)
                                                        if cellToFind != None:
                                                            for celly2 in cellToFind.getArea(area=AREA_CONE_7,fromCell=actTurn.cell):
                                                                if celly2 in viArea:
                                                                    viArea.remove(celly2)
                                                    elif direction == FROM_RIGHT:
                                                        cellToFind = findCell(celly.x-1,celly.y,tablAllCells)
                                                        if cellToFind != None:
                                                            for celly2 in cellToFind.getArea(area=AREA_CONE_7,fromCell=actTurn.cell):
                                                                if celly2 in viArea:
                                                                    viArea.remove(celly2)
                                                    elif direction == FROM_UP:
                                                        cellToFind = findCell(celly.x,celly.y+1,tablAllCells)
                                                        if cellToFind != None:
                                                            for celly2 in cellToFind.getArea(area=AREA_CONE_7,fromCell=actTurn.cell):
                                                                if celly2 in viArea:
                                                                    viArea.remove(celly2)
                                                    elif direction == FROM_RIGHT:
                                                        cellToFind = findCell(celly.x,celly.y-1,tablAllCells)
                                                        if cellToFind != None:
                                                            for celly2 in cellToFind.getArea(area=AREA_CONE_7,fromCell=actTurn.cell):
                                                                if celly2 in viArea:
                                                                    viArea.remove(celly2)

                                            weapOptions, choiceMsgTemp = [], "__Carte :__\n{0}\n\n__Combattants ?? port??e :__\n".format(map(tablAllCells,bigMap,actTurn.cell.getArea(area=actTurn.char.weapon.effectiveRange,team=actTurn.team,fromCell=actTurn.cell),fromEnt=actTurn,wanted=actTurn.char.weapon.target,numberEmoji=atRange))
                                            for a in range(0,nbTargetAtRange):
                                                choiceMsgTemp += f"{listNumberEmoji[a]} - {atRange[a].quickEffectIcons()}"
                                                desc = f"PV : {int(atRange[a].hp/atRange[a].maxHp*100)}%, Pos : {atRange[a].cell.x} - {atRange[a].cell.y}"
                                                if react.area != AREA_MONO:
                                                    desc += f", Zone : {len(atRange[a].cell.getEntityOnArea(area=actTurn.char.weapon.area,team=actTurn.team,wanted=actTurn.char.weapon.target,directTarget=False,fromCell=actTurn.cell))}"
                                                weapOptions += [create_select_option(listNumberEmoji[a] + " "+unhyperlink(atRange[a].char.name),str(a),getEmojiObject(atRange[a].icon),desc)]

                                            weapOptions += [create_select_option("Retour",str(a+1),emoji.backward_arrow)]
                                            weapSelect = create_select(options=weapOptions,placeholder="S??lectionnez une cible :")

                                            if len(weapOptions) == 2:
                                                temp,cmpt =[],0
                                                for a in weapOptions:
                                                    temp+=[create_button(1+cmpt,a["label"],a["emoji"],a["value"])]
                                                    cmpt += 1
                                                weapSelect = [create_actionrow(temp[0],temp[1])]
                                                await choiceMsg.edit(embed = discord.Embed(title = f"Choix de l'option - {react.name}",color = actTurn.char.color,description = choiceMsgTemp),components=[mainSelect]+weapSelect)

                                            elif choiceMsgTemp != "":
                                                await choiceMsg.edit(embed = discord.Embed(title = f"Choix de l'option - {react.name}",color = actTurn.char.color,description = choiceMsgTemp),components=[mainSelect,waitingSelect])
                                                await asyncio.sleep(3)
                                                await choiceMsg.edit(embed = discord.Embed(title = f"Choix de l'option - {react.name}",color = actTurn.char.color,description = choiceMsgTemp),components=[mainSelect,create_actionrow(weapSelect)])

                                            try:
                                                react = await wait_for_component(bot,messages=choiceMsg,check=check,timeout=timeLimite)
                                            except:
                                                unsuccess = True
                                                await choiceMsg.clear_reactions()
                                                break

                                            if len(weapOptions) > 2:
                                                selectedOptionSelect = [getChoisenSelect(weapSelect,react.values[0])]
                                            else:
                                                selectedOptionSelect = None

                                            optionChoice = OPTION_WEAPON
                                            try:
                                                value = int(react.values[0])
                                            except:
                                                value = int(react.custom_id)
                                            if value<len(atRange):
                                                ennemi = atRange[value]
                                                haveOption = True

                                        elif type(react) == skill:
                                            skillToUse,targetAtRangeSkill,a, funnyTempVarName, funnyTempVarNameButTheSecond = react,[],-1, [TYPE_ARMOR,TYPE_BOOST,TYPE_INDIRECT_HEAL,TYPE_INDIRECT_REZ,TYPE_RESURECTION,TYPE_HEAL],[TYPE_INDIRECT_DAMAGE,TYPE_MALUS,TYPE_DAMAGE]

                                            if skillToUse.type == TYPE_UNIQUE:
                                                targetAtRangeSkill = actTurn.cell.getEntityOnArea(area=skillToUse.area,team=actTurn.team,wanted=ALL,fromCell=actTurn.cell)
                                            elif skillToUse.range != AREA_MONO:
                                                if skillToUse.type in funnyTempVarName or skillToUse.id == friendlyPush.id:
                                                    targetAtRangeSkill = actTurn.cell.getEntityOnArea(area=skillToUse.range,team=actTurn.team,wanted=ALLIES,dead=skillToUse.type == TYPE_RESURECTION,fromCell=actTurn.cell)
                                                elif skillToUse.type in funnyTempVarNameButTheSecond:
                                                    targetAtRangeSkill = actTurn.cell.getEntityOnArea(area=skillToUse.range,team=actTurn.team,wanted=ENEMIES,lineOfSight=True,fromCell=actTurn.cell)

                                            else:
                                                if skillToUse.type in funnyTempVarName:
                                                    targetAtRangeSkill = actTurn.cell.getEntityOnArea(area=skillToUse.area,team=actTurn.team,wanted=ALLIES,directTarget=False,fromCell=actTurn.cell)
                                                elif skillToUse.type in funnyTempVarNameButTheSecond:
                                                    targetAtRangeSkill = actTurn.cell.getEntityOnArea(area=skillToUse.area,team=actTurn.team,wanted=ENEMIES,directTarget=False,fromCell=actTurn.cell)

                                            viArea, altViArea = actTurn.cell.getArea(area=[skillToUse.range,skillToUse.area][skillToUse.range==AREA_MONO],team=actTurn.team,fromCell=actTurn.cell), actTurn.cell.getArea(area=[skillToUse.range,skillToUse.area][skillToUse.range==AREA_MONO],team=actTurn.team,fromCell=actTurn.cell)
                                            if skillToUse.range != AREA_MONO and skillToUse.type in [TYPE_DAMAGE,TYPE_MALUS,TYPE_INDIRECT_DAMAGE]:
                                                for celly in viArea[:]:
                                                    if celly.on != None and (celly.on in atRange and celly.on.team != actTurn.team):
                                                        direction = getDirection(actTurn.cell,celly)
                                                        if direction == FROM_RIGHT:
                                                            cellToFind = findCell(celly.x+1,celly.y,tablAllCells)
                                                            if cellToFind != None:
                                                                for celly2 in cellToFind.getArea(area=AREA_CONE_7,fromCell=actTurn.cell):
                                                                    try:
                                                                        viArea.remove(celly2)
                                                                    except:
                                                                        pass
                                                        elif direction == FROM_LEFT:
                                                            cellToFind = findCell(celly.x-1,celly.y,tablAllCells)
                                                            if cellToFind != None:
                                                                for celly2 in cellToFind.getArea(area=AREA_CONE_7,fromCell=actTurn.cell):
                                                                    try:
                                                                        viArea.remove(celly2)
                                                                    except:
                                                                        pass
                                                        elif direction == FROM_DOWN:
                                                            cellToFind = findCell(celly.x,celly.y+1,tablAllCells)
                                                            if cellToFind != None:
                                                                for celly2 in cellToFind.getArea(area=AREA_CONE_7,fromCell=actTurn.cell):
                                                                    try:
                                                                        viArea.remove(celly2)
                                                                    except:
                                                                        pass
                                                        elif direction == FROM_UP:
                                                            cellToFind = findCell(celly.x,celly.y-1,tablAllCells)
                                                            if cellToFind != None:
                                                                for celly2 in cellToFind.getArea(area=AREA_CONE_7,fromCell=actTurn.cell):
                                                                    try:
                                                                        viArea.remove(celly2)
                                                                    except:
                                                                        pass

                                            skillOptions, choiceMsgTemp = [], "__Carte :__\n{0}\n\n__Combattants ?? port??e :__\n".format(map(tablAllCells,bigMap,viArea,fromEnt=actTurn,wanted=[ENEMIES,ALLIES][skillToUse.type in funnyTempVarName],numberEmoji=targetAtRangeSkill,fullArea=altViArea))

                                            if skillToUse.type != TYPE_SUMMON:
                                                nbTargetAtRangeSkill = len(targetAtRangeSkill)

                                                for a in range(nbTargetAtRangeSkill):
                                                    choiceMsgTemp += f"{listNumberEmoji[a]} - {targetAtRangeSkill[a].quickEffectIcons()}"
                                                    desc = f"PV : {int(targetAtRangeSkill[a].hp/targetAtRangeSkill[a].maxHp*100)}%, Pos : {targetAtRangeSkill[a].cell.x} - {targetAtRangeSkill[a].cell.y}"
                                                    if react.area not in [AREA_MONO,AREA_ALL_ALLIES,AREA_ALL_ENEMIES,AREA_ALL_ENTITES]:
                                                        if react.type in funnyTempVarName:
                                                            wanted = ALLIES
                                                        else:
                                                            wanted = ENEMIES
                                                        desc += f", Zone : {len(targetAtRangeSkill[a].cell.getEntityOnArea(area=react.area,team=actTurn.team,wanted=wanted,directTarget=False,fromCell=actTurn.cell))}"
                                                    skillOptions += [create_select_option(listNumberEmoji[a] + " "+unhyperlink(targetAtRangeSkill[a].char.name),str(a),getEmojiObject(targetAtRangeSkill[a].icon),desc)]
                                                
                                                if react.area in [AREA_ALL_ALLIES,AREA_ALL_ENEMIES,AREA_ALL_ENTITES] or react.range == AREA_MONO:
                                                    skillOptions = [create_select_option("Valider",'???','???')]

                                            else:
                                                choiceMsgTemp =f"Voulez vous invoquer {skillToUse.invocation} ?"
                                                skillOptions = [create_select_option("Valider",'???','???')]
                                                a = 0

                                            skillOptions += [create_select_option("Retour",str(a+1),emoji.backward_arrow)]
                                            skillSelect = create_select(options=skillOptions)

                                            if len(skillOptions) == 2:
                                                temp,cmpt =[],0
                                                for a in skillOptions:
                                                    tipe = 1
                                                    if a["label"] == 'Valider':
                                                        tipe = 3
                                                    elif a["label"] == "Retour":
                                                        tipe = 2
                                                    temp+=[create_button(tipe,a["label"],a["emoji"],a["value"])]
                                                    cmpt += 1
                                                skillSelect = [create_actionrow(temp[0],temp[1])]
                                                await choiceMsg.edit(embed = discord.Embed(title = f"Choix de l'option - {react.name}",color = actTurn.char.color,description = choiceMsgTemp),components=[mainSelect]+skillSelect)

                                            elif choiceMsgTemp != "":
                                                await choiceMsg.edit(embed = discord.Embed(title = f"Choix de l'option - {react.name}",color = actTurn.char.color,description = choiceMsgTemp),components=[mainSelect,waitingSelect])
                                                await asyncio.sleep(3)
                                                await choiceMsg.edit(embed = discord.Embed(title = f"Choix de l'option - {react.name}",color = actTurn.char.color,description = choiceMsgTemp),components=[mainSelect]+[create_actionrow(skillSelect)])

                                            try:
                                                react = await wait_for_component(bot,messages=choiceMsg,timeout = 30,check=check)
                                            except:
                                                unsuccess = True
                                                await choiceMsg.clear_reactions()
                                                break

                                            if len(skillOptions) > 2:
                                                selectedOptionSelect = [getChoisenSelect(skillSelect,react.values[0])]
                                            else:
                                                selectedOptionSelect = None

                                            optionChoice = OPTION_SKILL
                                            try:
                                                value = react.values[0]
                                            except:
                                                value = react.custom_id[0]

                                            if value == '???':
                                                ennemi = actTurn
                                                optionChoice = OPTION_SKILL
                                                haveOption = True
                                                break
                                            elif int(value) < len(targetAtRangeSkill):
                                                ennemi = targetAtRangeSkill[int(value)]
                                                optionChoice = OPTION_SKILL
                                                haveOption = True
                                                break

                                        elif type(react) == option:
                                            if react.emoji == '????':
                                                optionChoice = OPTION_SKIP
                                                unsuccess=False
                                                ennemi = actTurn
                                                haveOption=True

                                            elif react.emoji == '????':
                                                movingOption = [None,None,None,None]
                                                actCell = actTurn.cell
                                                for cmpt in range(0,4):
                                                    if surrondings[cmpt] != None:
                                                        movingOption[cmpt] = create_button(style=ButtonStyle.grey,label="Aller sur {0}:{1}".format(surrondings[cmpt].x,surrondings[cmpt].y),emoji=moveEmoji[cmpt],custom_id=moveEmoji[cmpt],disabled=not(canMove[cmpt]))
                                                    else:
                                                        movingOption[cmpt] = create_button(style=ButtonStyle.grey,label="Aller en dehors du monde",emoji=moveEmoji[cmpt],custom_id=moveEmoji[cmpt],disabled=True)

                                                allMouvementOptions = create_actionrow(movingOption[0],movingOption[1],movingOption[2],movingOption[3])
                                                tablSurrendCells = [[findCell(actCell.x-1,actCell.y-1,tablAllCells),findCell(actCell.x-0,actCell.y-1,tablAllCells),findCell(actCell.x+1,actCell.y-1,tablAllCells)],[findCell(actCell.x-1,actCell.y,tablAllCells),findCell(actCell.x-0,actCell.y,tablAllCells),findCell(actCell.x+1,actCell.y,tablAllCells)],[findCell(actCell.x-1,actCell.y+1,tablAllCells),findCell(actCell.x-0,actCell.y+1,tablAllCells),findCell(actCell.x+1,actCell.y+1,tablAllCells)]]
                                                mapLike = ""
                                                for litTabl in tablSurrendCells:
                                                    for cmpt in range(len(litTabl)):
                                                        if litTabl[cmpt] == None:
                                                            mapLike += '???'
                                                        elif litTabl[cmpt].on != None:
                                                            mapLike += litTabl[cmpt].on.icon
                                                        else:
                                                            finded = False
                                                            for cmptBis in (0,1,2,3):
                                                                if litTabl[cmpt] == surrondings[cmptBis]:
                                                                    mapLike += moveEmoji[cmptBis]
                                                                    finded=True
                                                                    break

                                                            if not(finded):
                                                                mapLike += '<:empty:866459463568850954>'

                                                        if cmpt != 2:
                                                            mapLike += "|"
                                                    mapLike += "\n"

                                                await choiceMsg.edit(embed = discord.Embed(title = f"Choix de l'option - {actTurn.icon} {actTurn.char.name}",color = actTurn.char.color,description = "Dans quelle direction voulez vous aller ?\n\n"+mapLike),components=[cancelButton,allMouvementOptions])

                                                choiceToMove = None
                                                while choiceToMove == None:
                                                    try:
                                                        choiceMove = await wait_for_component(bot,messages=choiceMsg,timeout=30,check=check)
                                                    except:
                                                        unsuccess = True
                                                        break
                                                    if choiceMove.custom_id == "return":
                                                        break
                                                    else:
                                                        for a in range(0,4):
                                                            if choiceMove.custom_id == moveEmoji[a]:
                                                                choiceToMove = surrondings[a]
                                                                optionChoice = OPTION_MOVE
                                                                break

                                                        unsuccess=False
                                                        ennemi = actTurn
                                                        haveOption=True

                                    try:
                                        logs += "\nManual fighter. Option selected : {0}".format(["Use Weapon","Use Skill","Move","Skip"][optionChoice])
                                    except:
                                        logs += "\nManual fighter, but no option selected"
                                    await choiceMsg.clear_reactions()
                                    try:
                                        if selectedOptionSelect != None:
                                            await choiceMsg.edit(embed = discord.Embed(title = f"Choix de l'option - {actTurn.icon} {actTurn.char.name}",color = actTurn.char.color,description = "Tour en cours "+emoji.loading),components=[mainSelect]+selectedOptionSelect)
                                        else:
                                            await choiceMsg.edit(embed = discord.Embed(title = f"Choix de l'option - {actTurn.icon} {actTurn.char.name}",color = actTurn.char.color,description = "Tour en cours "+emoji.loading),components=[mainSelect])
                                    except:
                                        await choiceMsg.edit(embed = discord.Embed(title = f"Choix de l'option - {actTurn.icon} {actTurn.char.name}",color = actTurn.char.color,description = "Tour en cours "+emoji.loading),components=[])

                                if not(actTurn.auto) and unsuccess:
                                    if actTurn.missedLastTurn == False:
                                        actTurn.missedLastTurn = True

                                    else:
                                        actTurn.auto = True
                                        nowStartOfTurn = datetime.now()

                                elif not(actTurn.auto) and not(unsuccess):
                                    actTurn.missedLastTurn = False

                                if unsuccess or type(ennemi)==int: # AI's stuffs
                                    team2maxHp, team2Hp, team1maxHp, team1Hp = 0, 0, 0, 0
                                    for ent in tablEntTeam[int(not(actTurn.team))]:
                                        team2maxHp, team2Hp = team2maxHp+ent.maxHp, team2Hp+ent.hp
                                    for ent in tablEntTeam[actTurn.team]:
                                        team1maxHp, team1Hp = team1maxHp+ent.maxHp, team1Hp+ent.hp

                                    ennemiesdying, alliesdying = team2Hp / team2maxHp <= 0.3, team1Hp / team1maxHp <= 0.4
                                    
                                    # D??finition du type d'IA :
                                    choisenIA = actTurn.IA

                                    if actTurn.char.aspiration in [IDOLE, INOVATEUR, PREVOYANT, VIGILANT]:
                                        allyDPTAlive = 0
                                        for ent in tablEntTeam[actTurn.team]:
                                            if ent.char.aspiration in [BERSERK,OBSERVATEUR,POIDS_PLUME,TETE_BRULE,MAGE,ENCHANTEUR,ATTENTIF,SORCELER] and ent.hp > 0:
                                                allyDPTAlive += 1

                                        if allyDPTAlive <= 2 or ennemiesdying or tour > 15:
                                            choisenIA = AI_OFFERUDIT

                                    logs += "\nAuto Fighter. Selected AI : {0}".format(["AI Damage","AI Booster","AI Shield","AI Aventurer","AI Healer","AI Agressive Supp","AI Mage","AI Enchant",][choisenIA])
                                    
                                    # D??finition des probabilit??s :
                                    # [DPT_PHYS,BOOST,SHIELD,AVENTURE,ALTRUISTE,OFFERUt,MAGE,ECHANT]

                                    probaAtkWeap = [60,50,50,50,50,60,60,60] 
                                    probaHealWeap = [20,60,30,30,70,30,20,20]
                                    probaReaSkill = [50,220,200,30,200,100,50,50]
                                    probIndirectReacSkill = [30,150,100,30,150,80,30,30]
                                    probaAtkSkill = [100,65,70,50,50,100,100,100]
                                    probaIndirectAtkSkill = [50,40,40,30,40,120,100,100]
                                    probaHealSkill = [30,100,70,30,130,50,30,30]
                                    probaBoost = [30,130,50,30,70,50,30,50]
                                    probaMalus = [45,40,100,30,50,50,50,50]
                                    probaArmor = [35,100,150,30,70,50,50,35]
                                    probaInvoc = [50,50,50,50,50,50,50,50]

                                    # There is a ennemi casting ?
                                    ennemiCast = False
                                    for ent in tablEntTeam[int(not(actTurn.team))]:
                                        for eff in ent.effect:
                                            if eff.effect.replica != None and eff.effect.id != clemultCastEffect.id:
                                                skillFinded = findSkill(eff.effect.replica)
                                                if (skillFinded.effectOnSelf == None and skillFinded.type in [TYPE_DAMAGE]) or (skillFinded.effectOnSelf != None and findEffect(skillFinded.effectOnSelf).replica == None) and skillFinded.area != AREA_MONO:
                                                    ennemiCast = True
                                                    break

                                    if ennemiCast:
                                        logs += "\nA ennemi is casting !"
                                        probaArmor[actTurn.IA] = int(probaArmor[choisenIA] *2)
                                    if alliesdying and not(ennemiesdying):
                                        probaHealSkill[choisenIA] = int(probaHealSkill[choisenIA] * 1.25)                                 
                                    
                                    # Weapons proba's ----------------------------------
                                    if actTurn.char.weapon.name.lower() == "noneweap" or actTurn.char.weapon.id.lower() == "noneweap" or (actTurn.char.weapon.id in cannotUseMainWeapon and len(actTurn.atRange()) > 0):
                                        probaHealWeap = [0,0,0,0,0,0,0,0]
                                        probaAtkWeap = [0,0,0,0,0,0,0,0]
                                    else:
                                        if actTurn.char.weapon.type == TYPE_DAMAGE:
                                            probaHealWeap = [0,0,0,0,0,0,0,0]
                                        elif actTurn.char.weapon.type == TYPE_HEAL:
                                            probaAtkWeap = [0,0,0,0,0,0,0,0]
                                            if len(actTurn.cell.getEntityOnArea(area=actTurn.char.weapon.effectiveRange,team=actTurn.team,wanted=ALLIES,directTarget=True,ignoreInvoc=True,lifeUnderPurcentage=90,fromCell=actTurn.cell)) == 0 and len(actTurn.cell.getEntityOnArea(area=actTurn.char.weapon.effectiveRange,team=actTurn.team,wanted=ALLIES,directTarget=True,ignoreInvoc=True,fromCell=actTurn.cell)) > 0:
                                                probaHealWeap = [0,0,0,0,0,0,0,0]

                                    surron = actTurn.cell.surrondings()
                                    if len(actTurn.atRange()) == 0 and (surron[0] != None and surron[0].on != None) and (surron[1] != None and surron[1].on != None) and (surron[2] != None and surron[2].on != None) and (surron[3] != None and surron[3].on != None):
                                        probaAtkWeap = [0,0,0,0,0,0,0,0]

                                    if actTurn.isNpc("Alice Exalt??e") and actTurn.specialVars["clemBloodJauge"].value <= 40:
                                        probaHealWeap[actTurn.IA] = int(probaHealWeap[actTurn.IA]*1.35)
                                        probaBoost[actTurn.IA] = int(probaBoost[actTurn.IA]*0.6)
                                        probaHealSkill[actTurn.IA] = int(probaHealSkill[actTurn.IA] * 0.9)
                                        probaAtkSkill[actTurn.IA] = int(probaAtkSkill[actTurn.IA] * 0.7)

                                    elif actTurn.isNpc("Luna ex.") and len(atRange) > 0:
                                        probaAtkSkill[actTurn.IA] = probaAtkSkill[actTurn.IA] * 2

                                    elif actTurn.isNpc("Lio"):
                                        downedAllies = 0
                                        for ent in tablEntTeam[actTurn.team]:
                                            if ent.hp <= 0:
                                                downedAllies += 1
                                        probaAtkSkill[choisenIA] = probaAtkSkill[choisenIA] * (1 + downedAllies/7)
                                
                                    elif actTurn.isNpc("S??r??na"):
                                        probaAtkWeap[choisenIA] = probaAtkWeap[choisenIA] * 0.7
                                    
                                    if actTurn.char.weapon.id in [whiteSpiritWings.id,bleuSpiritWings.id,fleau.id]:
                                        probaAtkWeap[actTurn.IA] = int(probaAtkWeap[actTurn.IA] * 1.5)

                                    # Do we have a big buff ? If yes, maybe we should consider using skills if we can't attack
                                    bigbuffy, dmgUpValue = actTurn.allStats()[actTurn.char.weapon.use] >= actTurn.baseStats[actTurn.char.weapon.use] * 1.1, 0
                                    if not(bigbuffy):
                                        for a in actTurn.effect:
                                            if a.effect.id == dmgUp.id:
                                                dmgUpValue += a.effect.power
                                    bigbuffy = dmgUpValue >= max(5,actTurn.level / 5)

                                    if bigbuffy:
                                        logs += "\nDmg or stat buff detected"                                    

                                    if bigbuffy and nbTargetAtRange < 0:
                                        logs += " but no target in the range of the weapon is found"
                                        haveOffSkills = False
                                        for a in range(7):
                                            if actTurn.cooldowns[a] <= 0 and type(actTurn.skills[a]) == skill:
                                                if actTurn.skills[a].type == TYPE_DAMAGE:
                                                    if (actTurn.skills[a].range == AREA_MONO and len(actTurn.cell.getEntityOnArea(area=actTurn.skills[a].area,team=actTurn.team,wanted=ENEMIES,effect=actTurn.skills[a].effect,fromCell=actTurn.cell))> 0) or (actTurn.skills[a].range != AREA_MONO and len(actTurn.cell.getEntityOnArea(area=actTurn.skills[a].range,team=actTurn.team,wanted=ENEMIES,fromCell=actTurn.cell,effect=actTurn.skills[a].effect))> 0):
                                                        haveOffSkills = True
                                                        break

                                        if haveOffSkills:
                                            probaHealWeap = [0,0,0,0,0,0,0,0]
                                            probaAtkWeap = [0,0,0,0,0,0,0,0]
                                            logs += "\nSomes offensives skills with targets at range have been found. Weapon's proba neutralized"
                                        else:
                                            logs += "\nNo available offensives skills have been found"

                                    qCast = False
                                    for eff in actTurn.effect:
                                        if eff.effect.id == quickCastEff.id:
                                            qCast = True
                                            probaHealWeap[actTurn.IA] = 0
                                            probaAtkWeap[actTurn.IA] = 0
                                            break

                                    healSkill,atkSkill,reaSkill,indirectReaSkill,indirectAtkSkill,boostSkill,malusSkill,armorSkill,invocSkill = [],[],[],[],[],[],[],[],[]

                                    for a in range(7): # Cat??gorisation des sorts
                                        actSkill = actTurn.char.skills[a]
                                        if actTurn.cooldowns[a] == 0 and type(actSkill) == skill and not(actTurn.silent) and actSkill.id != "lb":
                                            if actSkill.become == None:
                                                tablToLook = [actSkill]
                                            else:
                                                tablToLook, tablEffId = [], []
                                                for eff in actTurn.effect:
                                                    tablEffId.append(eff.effect.id)

                                                for cmpt in range(len(actSkill.become)):
                                                    if actSkill.become[cmpt].needEffect == actSkill.become[cmpt].rejectEffect == None:
                                                        tablToLook.append(actSkill.become[cmpt])
                                                    elif actSkill.become[cmpt].rejectEffect == None and actSkill.become[cmpt].needEffect != None:
                                                        fullValid = True
                                                        for bidule in actSkill.become[cmpt].needEffect:
                                                            if bidule.id not in tablEffId:
                                                                fullValid = False
                                                                break

                                                        if fullValid:
                                                            tablToLook.append(actSkill.become[cmpt])
                                                    else:
                                                        fullValid = True
                                                        for bidule in actSkill.become[cmpt].rejectEffect:
                                                            if bidule.id in tablEffId:
                                                                fullValid = False
                                                                break

                                                        if fullValid:
                                                            tablToLook.append(actSkill.become[cmpt])

                                            for actSkill in tablToLook:
                                                if actSkill.range == AREA_MONO:                                     # If the skill is launch on self
                                                    allieAtRange,ennemiAtRange = len(actTurn.cell.getEntityOnArea(area=actSkill.area,team=actTurn.team,wanted=ALLIES,effect=actSkill.effect,ignoreInvoc=True,directTarget=False,fromCell=actTurn.cell))> 1,len(actTurn.cell.getEntityOnArea(area=actSkill.area,team=actTurn.team,wanted=ENEMIES,effect=actSkill.effect,fromCell=actTurn.cell,directTarget=False))> 0
                                                    if actSkill.type in [TYPE_HEAL,TYPE_INDIRECT_HEAL] and len(actTurn.cell.getEntityOnArea(area=actSkill.area,team=actTurn.team,wanted=ALLIES,effect=actSkill.effect,lifeUnderPurcentage=90,ignoreInvoc = True,directTarget=False))> 0 and actSkill.id not in ["lb","ul",abnegation.id]:
                                                        if qCast and actSkill.effectOnSelf != None and findEffect(actSkill.effectOnSelf).replica != None:
                                                            atkSkill.append(actSkill)
                                                        else:
                                                            if actSkill.id not in [secondWind.id,dissi.id]:                                   # If the skill isn't Second Wind
                                                                healSkill.append(actSkill)
                                                            elif actSkill.id == secondWind.id and actTurn.hp/actTurn.maxHp <= 0.25:                          # Else, if the fighter is dying
                                                                healSkill.append(actSkill)
                                                            else:
                                                                for ent in tablEntTeam[actTurn.team]:
                                                                    if type(ent.char) == invoc and ent.id == actTurn.id:
                                                                        healSkill.append(actSkill)
                                                                        break
                                                    elif actSkill.type == TYPE_DAMAGE and ennemiAtRange:            # Damage skills
                                                        hasBeenApprouved = False
                                                        if qCast and actSkill.effectOnSelf != None and findEffect(actSkill.effectOnSelf).replica != None:
                                                            atkSkill.append(actSkill)
                                                            hasBeenApprouved = True
                                                        elif not(qCast):
                                                            if actSkill.id == trans.id and actTurn.isNpc("Liz"):
                                                                nbCharm, nbKitsune = 0, 1+int(dictIsNpcVar["Lia"])+int(dictIsNpcVar["Liu"])
                                                                for ent in tablEntTeam[not(actTurn.team)]:
                                                                    for eff in ent.effect:
                                                                        if eff.id == charming.id:
                                                                            nbCharm += 1
                                                                if nbCharm >= nbKitsune*10:
                                                                    cmpt = 0
                                                                    while cmpt*10 < nbKitsune*10:
                                                                        atkSkill.append(actSkill)
                                                                        cmpt += 1
                                                            else:
                                                                atkSkill.append(actSkill)
                                                                hasBeenApprouved = True

                                                        if hasBeenApprouved and actSkill.needEffect != None:
                                                            atkSkill.append(actSkill)
                                                            probaAtkSkill[actTurn.IA] = probaAtkSkill[actTurn.IA]*1.2
                                                    elif actSkill.type == TYPE_RESURECTION and len(actTurn.cell.getEntityOnArea(area=actSkill.area,team=actTurn.team,wanted=ALLIES,dead=True,fromCell=actTurn.cell)) > 0 and not(qCast):                         # Resu skills (none lol)
                                                            reaSkill.append(actSkill)
                                                    elif actSkill.type == TYPE_INDIRECT_REZ and allieAtRange and not(qCast):       # Indirect Resu skills (Zelian R)
                                                        indirectReaSkill.append(actSkill)
                                                    elif actSkill.type == TYPE_INDIRECT_DAMAGE and ennemiAtRange and not(qCast):   # Indirect damage skills
                                                        if actSkill.id != serenaSpe.id:
                                                            indirectAtkSkill.append(actSkill)
                                                        else:
                                                            poisonCount = 0
                                                            for ent in tablEntTeam[int(not(actTurn))]:
                                                                for eff in ent.effect:
                                                                    if eff.effect.id == estal.id:
                                                                        poisonCount += 1

                                                            if poisonCount >= 5:
                                                                indirectAtkSkill.append(actSkill)

                                                    elif actSkill.type == TYPE_BOOST and actSkill.area != AREA_MONO and allieAtRange:              # Buff skills
                                                        if actSkill.id != trans or nbLB[actTurn.team] == 1:
                                                            if qCast and actSkill.effectOnSelf != None and findEffect(actSkill.effectOnSelf).replica != None:
                                                                atkSkill.append(actSkill)
                                                            elif len(actTurn.cell.getEntityOnArea(area=actSkill.area,team=actTurn.team,wanted=ALLIES,effect=actSkill.effect,ignoreInvoc=True,directTarget=False)) >= len(actTurn.cell.getEntityOnArea(area=actSkill.area,team=actTurn.team,wanted=ALLIES,ignoreInvoc=True,directTarget=False))*0.5:
                                                                boostSkill.append(actSkill)
                                                        else:
                                                            nbWorth, nbDown = 0, 0
                                                            for ent in tablEntTeam[actTurn.team]:
                                                                if ent.hp > 0:
                                                                    for cmpt in len(ent.cooldowns):
                                                                        if ent.cooldowns[cmpt] == 0 and type(ent.char.skills[cmpt]) == skill and (ent.char.skills[cmpt].cooldown >= 7 or ent.char.skills[cmpt].ultimate) and ent.char.skills[cmpt].type in [TYPE_DAMAGE, TYPE_INDIRECT_DAMAGE]:
                                                                            nbWroth += 1
                                                                            break
                                                                elif ent.status == STATUS_DEAD:
                                                                    nbDown += 1
                                                            if nbWorth >= 3:
                                                                boostSkill.append(actSkill)
                                                            
                                                            if (actTurn.char.aspiration == IDOLE and nbDown >= 3) or (actTurn.char.aspiration == INOVATEUR and ennemiCast):
                                                                boostSkill.append(actSkill)
                                                                boostSkill.append(actSkill)

                                                    elif actSkill.type == TYPE_BOOST and actSkill.area == AREA_MONO and not(qCast):
                                                        if actSkill.id not in [quickCast.id,invincible.id,holmgang.id,bolide.id]:
                                                            boostSkill.append(actSkill)
                                                        elif actSkill.id in [invincible.id,holmgang.id,bolide.id]:
                                                            hpRatio = actTurn.hp/actTurn.maxHp
                                                            if hpRatio < 0.2:
                                                                boostSkill.append(actSkill)
                                                                boostSkill.append(actSkill)
                                                                boostSkill.append(actSkill)
                                                                probaBoost[actTurn.IA] = probaBoost[actTurn.IA] * 2
                                                            elif hpRatio < 0.5:
                                                                boostSkill.append(actSkill)
                                                    elif actSkill.type == TYPE_MALUS and ennemiAtRange and not(qCast):             # Debuff skills
                                                        if actSkill.id not in ["lb"] or (actSkill.id == "lb" and nbLB[actTurn.team] == 1):
                                                            malusSkill.append(actSkill)
                                                        elif ennemiCast or len(actTurn.cell.getEntityOnArea(area=actSkill.area,team=actTurn.team,wanted=ENEMIES,ignoreInvoc = True, directTarget=False,ignoreAspiration = None,fromCell=actTurn.cell)) > 3 :
                                                            malusSkill.append(actSkill)
                                                    elif actSkill.type == TYPE_ARMOR and actSkill.area != AREA_MONO and allieAtRange and not(qCast):              # Armor skills
                                                        if actSkill.id not in ["lb"] or (actSkill.id == "lb" and nbLB[actTurn.team] == 1):
                                                            armorSkill.append(actSkill)
                                                        elif ennemiCast:
                                                            armorSkill.append(actSkill)

                                                        if ennemiCast and actSkill.area == AREA_ALL_ALLIES: # Si l'ennemi cast et que la comp??tence touche tous les alli??s : Proba augment??e
                                                            armorSkill.append(actSkill)
                                                        if ennemiCast and actSkill.area != AREA_MONO: # Si l'ennemi cast et que la comp??tence est pas mono : Proba augment??e
                                                            armorSkill.append(actSkill)
                                                    elif actSkill.type == TYPE_ARMOR and actSkill.area == AREA_MONO and actTurn.hp / actTurn.maxHp <= 0.5 and not(qCast):
                                                        armorSkill.append(actSkill)
                                                    elif actSkill.type == TYPE_UNIQUE and not(qCast):                              # Other
                                                        if actSkill in [chaos]:                                         # Boost
                                                            boostSkill.append(actSkill)

                                                    elif actSkill.type == TYPE_SUMMON and len(actTurn.cell.getEmptyCellsInArea(area=actSkill.range,team=actTurn.team,fromCell=actTurn.cell))>0 and not(qCast): # Invocation
                                                        temp = actTurn.cell.getEmptyCellsInArea(area=actSkill.range,team=actTurn.team)
                                                        for b in temp[:]:
                                                            if actTurn.team == 0:
                                                                if b.x > 2:
                                                                    temp.remove(b)
                                                            elif b.x < 3:
                                                                temp.remove(a)

                                                        invocSkill.append(actSkill)

                                                    elif actSkill.id in ["ul",abnegation.id] and not(qCast): 
                                                        sumHp,sumMaxHp = 0,0
                                                        for b in tablEntTeam[actTurn.team]:
                                                            sumHp += max(0,b.hp)
                                                            sumMaxHp += b.maxHp
                                                        if sumHp / sumMaxHp <= 0.6:
                                                            healSkill.append(actSkill)
                                                            healSkill.append(actSkill)
                                                            for num in range(len(probaHealSkill)):
                                                                probaHealSkill[num] = probaHealSkill[num] *1.2
                                                        if sumHp / sumMaxHp <= 0.4:
                                                            healSkill.append(actSkill)
                                                            healSkill.append(actSkill)
                                                            for num in range(len(probaHealSkill)):
                                                                probaHealSkill[num] = probaHealSkill[num] *1.5

                                                else: # The skill is cast on others
                                                    ennemiTabl = actTurn.cell.getEntityOnArea(area=actSkill.range,team=actTurn.team,wanted=ENEMIES,fromCell=actTurn.cell,lineOfSight = True,effect=actSkill.effect,ignoreInvoc = (actSkill.effectOnSelf == None or (actSkill.effectOnSelf != None and findEffect(actSkill.effectOnSelf).replica != None)))
                                                    ennemiTabl.sort(key=lambda ballerine: actTurn.getAggroValue(ballerine),reverse=True)
                                                    allieTabl = actTurn.cell.getEntityOnArea(area=actSkill.range,team=actTurn.team,fromCell=actTurn.cell,wanted=ALLIES,effect=actSkill.effect,ignoreInvoc = True)
                                                    allieTablHeal = actTurn.cell.getEntityOnArea(area=actSkill.range,team=actTurn.team,fromCell=actTurn.cell,wanted=ALLIES,lifeUnderPurcentage=90,effect=actSkill.effect,ignoreInvoc = True)
                                                    allieAtRange,ennemiAtRange = len(allieTabl)> 0,len(ennemiTabl)> 0
                                                    allieTablHeal.sort(key=lambda allie: getHealAggro(allie, actSkill),reverse=True)
                                                    if len(allieTablHeal) > 0:
                                                        mostLiklyHealedAllie = allieTablHeal[0]

                                                    if (actSkill.type == TYPE_HEAL or actSkill.type == TYPE_INDIRECT_HEAL) and len(allieTablHeal)> 0 and not(qCast):
                                                        if actSkill.id not in [vampirisme.id,uberCharge.id]:
                                                            healSkill.append(actSkill)
                                                        elif actSkill.id in [uberCharge.id]:
                                                            try:
                                                                if teamJaugeDict[actTurn.team][actTurn].effect.id == uberJauge.id and teamJaugeDict[actTurn.team][actTurn].value > 75:
                                                                    healSkill.append(actSkill)

                                                                elif teamJaugeDict[actTurn.team][actTurn].effect.id == uberJauge.id and teamJaugeDict[actTurn.team][actTurn].value > 25:
                                                                    healSkill.append(actSkill)
                                                                
                                                                elif teamJaugeDict[actTurn.team][actTurn].effect.id != uberJauge.id:
                                                                    healSkill.append(actSkill)
                                                            except KeyError:
                                                                healSkill.append(actSkill)

                                                        elif mostLiklyHealedAllie.char.aspiration not in [ALTRUISTE,VIGILANT,PREVOYANT,IDOLE,INOVATEUR,PROTECTEUR]:
                                                            healSkill.append(actSkill)
                                                    elif actSkill.type == TYPE_DAMAGE and ennemiAtRange:
                                                        hasBeenApprouved = False
                                                        if qCast and actSkill.effectOnSelf != None and findEffect(actSkill.effectOnSelf).replica != None:
                                                            atkSkill.append(actSkill)
                                                            hasBeenApprouved = True
                                                        elif not(qCast):
                                                            if actSkill.id == finalTech.id:
                                                                try:
                                                                    for jaugeEnt, jaugeEff in teamJaugeDict[actTurn.team].items():
                                                                        if jaugeEnt == actTurn and jaugeEff.effect.id == pasTech.id and jaugeEff.value >= 90:
                                                                            atkSkill.append(actSkill)
                                                                            atkSkill.append(actSkill)
                                                                            probaAtkSkill[actTurn.IA] = probaAtkSkill[actTurn.IA]*3
                                                                            break
                                                                except:
                                                                    print_exc()
                                                            else:
                                                                atkSkill.append(actSkill)
                                                                hasBeenApprouved = True
                                                                if actSkill.id in importantSkills:
                                                                    atkSkill.append(actSkill)

                                                        if hasBeenApprouved and actSkill.needEffect != None:
                                                            atkSkill.append(actSkill)
                                                            probaAtkSkill[actTurn.IA] = probaAtkSkill[actTurn.IA]*1.2
                                                    elif actSkill.type == TYPE_RESURECTION and len(actTurn.cell.getEntityOnArea(area=actSkill.range,fromCell=actTurn.cell,team=actTurn.team,wanted=ALLIES,dead=True)) > 0 and not(qCast):
                                                        reaSkill.append(actSkill)
                                                    elif actSkill.type == TYPE_INDIRECT_REZ and allieAtRange and not(qCast):
                                                        indirectReaSkill.append(actSkill)
                                                    elif actSkill.type == TYPE_INDIRECT_DAMAGE and ennemiAtRange: # Indirect damge
                                                        if not(qCast):
                                                            if actSkill.id not in [poisonus.id,bleedingTrap.id]:
                                                                indirectAtkSkill.append(actSkill)
                                                            elif actSkill.id == poisonus.id:
                                                                if actTurn.char.weapon.effectOnUse != None and findEffect(actTurn.char.weapon.effectOnUse).id == estal.id:
                                                                    target = sorted(ennemiTabl,key=lambda ent:actTurn.getAggroValue(ent))[0]
                                                                    if len(target.cell.getEntityOnArea(area=actSkill.area,team=actTurn.team,wanted=ENEMIES,lineOfSight = True)) > 1:
                                                                        indirectAtkSkill.append(actSkill)
                                                                else:
                                                                    indirectAtkSkill.append(actSkill)
                                                            elif actSkill.id == bleeding.id:
                                                                if actTurn.char.weapon.effectOnUse != None and findEffect(actTurn.char.weapon.effectOnUse).id == bleeding.id:
                                                                    target = sorted(ennemiTabl,key=lambda ent:actTurn.getAggroValue(ent))[0]
                                                                    if len(target.cell.getEntityOnArea(area=actSkill.area,team=actTurn.team,wanted=ENEMIES,lineOfSight = True)) > 1:
                                                                        indirectAtkSkill.append(actSkill)
                                                            else:
                                                                indirectAtkSkill.append(actSkill)
                                                        elif actSkill.effectOnSelf != None and findEffect(actSkill.effectOnSelf).replica != None:
                                                            indirectAtkSkill.append(actSkill)
                                                    elif actSkill.type == TYPE_BOOST and allieAtRange and not(qCast):
                                                        effect = findEffect(actSkill.effect[0])
                                                        if effect.turnInit >= 2 and actSkill.id != derobade.id:
                                                            boostSkill.append(actSkill)
                                                        elif len(actTurn.cell.getEntityOnArea(area=actSkill.range,team=actTurn.team,wanted=ALLIES,effect=actSkill.effect,ignoreInvoc = True)) > 1:
                                                            if actSkill.id != derobade.id:                          # Any skills
                                                                boostSkill.append(actSkill)
                                                            elif actTurn.hp/actTurn.maxHp <= 0.25:                  # D??robade
                                                                boostSkill.append(actSkill)
                                                    elif actSkill.type == TYPE_MALUS and ennemiAtRange and not(qCast):
                                                        if actSkill not in [boom]: 
                                                            malusSkill.append(actSkill)
                                                        else: # Si il ne reste qu'un ennemi, ne pas prendre en compte R??action en cha??ne
                                                            team2see = tablEntTeam[int(not(actTurn.team))][:]
                                                            for b in team2see[:]:
                                                                if b.hp <= 0:
                                                                    team2see.remove(b)

                                                            if len(team2see) > 1:
                                                                malusSkill.append(boom)
                                                    elif actSkill.type == TYPE_ARMOR and len(allieTablHeal)>0 and not(qCast):
                                                        if actSkill.id != convert.id:
                                                            if ennemiCast and actSkill.area == AREA_ALL_ALLIES: # Si l'ennemi cast et que la comp??tence touche tous les alli??s : Proba augment??e
                                                                armorSkill.append(actSkill)
                                                            if ennemiCast and actSkill.area != AREA_MONO: # Si l'ennemi cast et que la comp??tence est pas mono : Proba augment??e
                                                                armorSkill.append(actSkill)
                                                            armorSkill.append(actSkill)

                                                        elif mostLiklyHealedAllie.char.aspiration not in [ALTRUISTE,VIGILANT,PREVOYANT,IDOLE,INOVATEUR,PROTECTEUR]:
                                                            armorSkill.append(actSkill)
                                                    elif actSkill.type == TYPE_UNIQUE and not(qCast):
                                                        for b in [chaos]: # Boost
                                                            if b == actSkill:
                                                                boostSkill.append(b)
                                                    elif actSkill.type == TYPE_SUMMON and actTurn.cell.getCellForSummon(area=actSkill.range, team=actTurn.team, summon= findSummon(actSkill.invocation), summoner=actTurn) != None and not(qCast):
                                                        if nbLB[actTurn.team] == 0:
                                                            invocSkill.append(actSkill)
                                                            if actSkill.ultimate:
                                                                probaInvoc[choisenIA] = probaInvoc[choisenIA]*2
                                                                invocSkill.append(actSkill)
                                                                invocSkill.append(actSkill)

                                    if LBBars[actTurn.team][0]> 0 and LBBars[actTurn.team][1]//3 >= 1 and type(actTurn.char) not in [invoc,octarien]:
                                        if LBBars[actTurn.team][1]//3 == 1:
                                            lbSkill = lb1Tabl[actTurn.char.aspiration]
                                        elif LBBars[actTurn.team][1]//3 == 2:
                                            lbSkill = lb2Tabl[actTurn.char.aspiration]
                                        elif LBBars[actTurn.team][1]//3 == 3:
                                            lbSkill = lb3Tabl[actTurn.char.aspiration]
                                        elif LBBars[actTurn.team][1]//3 == 4:
                                            lbSkill = lb4
                                        
                                        lbPrio = LBBars[actTurn.team][1]//3 == LBBars[actTurn.team][0]
                                        if lbSkill.type == TYPE_DAMAGE and lbPrio:
                                            ennemiTabl = actTurn.cell.getEntityOnArea(area=lbSkill.range,team=actTurn.team,wanted=ENEMIES,fromCell=actTurn.cell,lineOfSight = True,ignoreInvoc = True)
                                            ennemiTabl.sort(key=lambda ballerine: actTurn.getAggroValue(ballerine),reverse=True)

                                            if lbSkill.area == AREA_MONO:
                                                ennemiNb = 0
                                                for ent in tablEntTeam[not(actTurn.team)]:
                                                    if type(ent.char) != invoc and ent.hp > 0:
                                                        ennemiNb += 1
                                                if ennemiNb <= 2:
                                                    atkSkill.append(lbSkill)
                                                    atkSkill.append(lbSkill)
                                            elif len(ennemiTabl) > 0 and (not dictIsNpcVar["The Giant Enemy Spider"] and not dictIsNpcVar["[[Spamton Neo](https://deltarune.fandom.com/wiki/Spamton)]"]):
                                                if len(ennemiTabl[0].cell.getEntityOnArea(area=lbSkill.area,team=actTurn.team,wanted=ENEMIES,fromCell=actTurn.cell,ignoreInvoc = True)) >= [2,3][lbSkill.area==lb1AoE.area]:
                                                    atkSkill.append(lbSkill)
                                                    atkSkill.append(lbSkill)
                                            elif dictIsNpcVar["The Giant Enemy Spider"] or dictIsNpcVar["[[Spamton Neo](https://deltarune.fandom.com/wiki/Spamton)]"]:
                                                atkSkill.append(lbSkill)
                                                if lbSkill.area==lb1AoE.area:
                                                    atkSkill.append(lbSkill)
                                                    atkSkill.append(lbSkill)

                                        elif lbSkill.type == TYPE_HEAL:
                                            aliveAlliesHp, aliveAlliesMaxHp, rezableAllies = 0, 0,0
                                            for ent in tablEntTeam[actTurn.team]:
                                                if type(ent.char) != invoc and ent.hp > 0:
                                                    aliveAlliesHp += ent.hp
                                                    aliveAlliesMaxHp += ent.maxHp
                                                elif ent.hp <= 0 and ent.status == STATUS_DEAD:
                                                    rezableAllies += 1
                                            hpRatio = aliveAlliesHp/aliveAlliesMaxHp

                                            if hpRatio <= 0.25:
                                                probaHealSkill[choisenIA] = probaHealSkill[choisenIA] * 1.2
                                                healSkill.append(lbSkill)
                                            if hpRatio <= 0.15:
                                                probaHealSkill[choisenIA] = probaHealSkill[choisenIA] * 1.2
                                                healSkill.append(lbSkill)

                                            if LBBars[actTurn.team][1]//3 >= 2 and rezableAllies >=3 :
                                                probaHealSkill[choisenIA] = probaHealSkill[choisenIA] * 1.2
                                                healSkill.append(lbSkill)
                                                healSkill.append(lbSkill)
                                        elif lbSkill.type == TYPE_ARMOR and ennemiCast:
                                            armorSkill.append(lbSkill)
                                        elif lbSkill.type == TYPE_BOOST:
                                            alliesCastingDpsSkill = 0
                                            for ent in tablEntTeam[actTurn.team]:
                                                for eff in ent.effect:
                                                    if eff.effect.replica != None and (findSkill(eff.effect.replica).effectOnSelf == None or findEffect(findSkill(eff.effect.replica).effectOnSelf).replica == None) and findSkill(eff.effect.replica).type in [TYPE_DAMAGE,TYPE_INDIRECT_DAMAGE]:
                                                        alliesCastingDpsSkill += 1
                                                        break
                                            if 6 - LBBars[actTurn.team][1]//3 <= alliesCastingDpsSkill:
                                                boostSkill.append(lbSkill)
                                                boostSkill.append(lbSkill)
                                    isTMinDanger = False
                                    for a in tablEntTeam[actTurn.team]:
                                        if a.hp / a.maxHp <= 0.35:
                                            isTMinDanger = True
                                            break

                                    if not(isTMinDanger):
                                        probIndirectReacSkill = [0,0,0,0,0,0,0,0]
                                    else:
                                        probaHealSkill = [30,120,40,50,150,150,150,150,150]

                                    if actTurn.specialVars["summonerMalus"]:
                                        probaAtkWeap = probaHealWeap = probaReaSkill = probIndirectReacSkill = probaAtkSkill = probaIndirectAtkSkill = probaHealSkill = probaBoost = probaMalus = probaArmor = [0,0,0,0,0,0,0,0] 

                                    probTabl, analyse = [copy.copy(probaReaSkill),copy.copy(probIndirectReacSkill),copy.copy(probaAtkSkill),copy.copy(probaIndirectAtkSkill),copy.copy(probaHealSkill),copy.copy(probaBoost),copy.copy(probaMalus),copy.copy(probaArmor)], [reaSkill,indirectReaSkill,atkSkill,indirectAtkSkill,healSkill,boostSkill,malusSkill,armorSkill]
                                    for cmpt in range(0,8):
                                        if len(analyse[cmpt]) == 0:
                                            probTabl[cmpt][choisenIA] = 0

                                    if not(len(invocSkill) > 0 and tablAliveInvoc[actTurn.team]<3):
                                        probaInvoc[choisenIA] = 0

                                    totalProba = probaAtkWeap[choisenIA]+probaHealWeap[choisenIA]

                                    for tabl in probTabl:
                                        totalProba+= tabl[choisenIA]

                                    nbIte, optionChoice = 0, OPTION_WEAPON
                                    atRange = actTurn.atRange()
                                    nbTargetAtRange = len(atRange)
                                    if not(actTurn.char.weapon.name.lower() == "noneweap" or actTurn.char.weapon.id.lower() == "noneweap" or (actTurn.char.weapon.id in cannotUseMainWeapon and len(actTurn.atRange()) > 0)):
                                        if actTurn.char.weapon.target == ENEMIES:
                                            if nbTargetAtRange > 0:
                                                atRange.sort(key=lambda ent:actTurn.getAggroValue(ent),reverse=True)
                                                optionChoice,ennemi = OPTION_WEAPON,atRange[0]

                                            else:
                                                optionChoice,choiceToMove = OPTION_MOVE, actTurn.getCellToMove()
                                                if choiceToMove == None:
                                                    optionChoice=OPTION_SKIP

                                        else:
                                            if nbTargetAtRange > 0:
                                                optionChoice,ennemi = OPTION_WEAPON,getHealTarget(atRange,actTurn.char.weapon)
                                            else:
                                                optionChoice,choiceToMove = OPTION_MOVE, actTurn.getCellToMove()
                                                if choiceToMove == None:
                                                    optionChoice=OPTION_SKIP
                                    else:
                                        optionChoice,choiceToMove = OPTION_MOVE, actTurn.getCellToMove()
                                        if choiceToMove == None:
                                            optionChoice=OPTION_SKIP
                                    subWeapon = 0
                                    while nbIte <= 2:                       
                                        totalProba += probaInvoc[choisenIA] - subWeapon
                                        try:
                                            probaRoll = random.randint(0,totalProba)
                                        except:
                                            probaRoll = 0
                                        logs += "\nTotal Proba : {0} - ProbaRoll : {1}".format(totalProba,probaRoll)

                                        optionChoisen = False

                                        if probaRoll <= probaAtkWeap[choisenIA] and probaAtkWeap[choisenIA] > 0: #Attaque ?? l'arme
                                            logs += "\nSelected option : Damage with weapon\nTargets at range : {0}\n".format(nbTargetAtRange)
                                            if optionChoice == OPTION_MOVE:          
                                                for cmpt in range(len(actTurn.char.skills)):
                                                    if type(actTurn.char.skills[cmpt]) == skill and actTurn.cooldowns[cmpt] == 0 and actTurn.char.skills[cmpt].tpCac == True:
                                                        atRange2 = actTurn.cell.getEntityOnArea(area=actTurn.char.skills[cmpt].range,fromCell=actTurn.cell,team=actTurn.team,wanted=ENEMIES,lineOfSight=True)
                                                        if len(atRange2)>0:
                                                            atRange2.sort(key=lambda ent:actTurn.getAggroValue(ent),reverse=True)
                                                            optionChoice = OPTION_SKILL
                                                            skillToUse = actTurn.char.skills[cmpt]
                                                            try:
                                                                ennemi = atRange[0]
                                                                compromis = True
                                                            except:
                                                                pass
                                                            break
                                            if optionChoice != OPTION_SKIP:
                                                optionChoisen = True
                                            else:
                                                logs += "\nSkipping ? No, try again"
                                                if probaRoll - probaAtkWeap[choisenIA] > 0:
                                                    subWeapon = probaAtkWeap[choisenIA]
                                        else:
                                            probaRoll -= probaAtkWeap[choisenIA]

                                        if probaRoll <= probaHealWeap[choisenIA] and probaHealWeap[choisenIA] > 0 and not(optionChoisen): #Soins ?? l'arme
                                            logs += "\nSelected option : Heal with weapon"
                                            optionChoisen = True
                                        elif not(optionChoisen):
                                            probaRoll -= probaHealWeap[choisenIA]

                                        if probaRoll <= probTabl[0][choisenIA] and probTabl[0][choisenIA] > 0 and not(optionChoisen): # R??surection
                                            logs += "\nSelected option : Resurection Skill"
                                            if len(reaSkill) > 1:
                                                skillToUse = reaSkill[random.randint(0,len(reaSkill)-1)]
                                            else:
                                                skillToUse = reaSkill[0]

                                            if skillToUse.range != AREA_MONO:
                                                for a in tablEntTeam[actTurn.team]:
                                                    if a.status == STATUS_DEAD:
                                                        optionChoice = OPTION_SKILL
                                                        ennemi = a
                                                        break

                                            else:
                                                optionChoice = OPTION_SKILL
                                                ennemi = actTurn

                                            optionChoisen=True
                                        elif not(optionChoisen):
                                            probaRoll -= probTabl[0][choisenIA]

                                        if probaRoll <= probTabl[1][choisenIA] and probTabl[1][choisenIA] > 0 and not(optionChoisen): # R??surection indirect:
                                            logs += "\nSelected option : Indirect resurection skill"
                                            for a in tablEntTeam[actTurn.team]:
                                                if a.hp <= 0.3 and a.hp > 0:
                                                    optionChoice = OPTION_SKILL
                                                    if len(indirectReaSkill) > 1:
                                                        skillToUse = indirectReaSkill[random.randint(0,len(reaSkill)-1)]
                                                    else:
                                                        skillToUse = indirectReaSkill[0]
                                                    ennemi = a
                                                    optionChoisen = True
                                                    break

                                            optionChoisen = True
                                        elif not(optionChoisen):
                                            probaRoll -= probTabl[1][choisenIA]

                                        if probaRoll <= probTabl[2][choisenIA] and probTabl[2][choisenIA] > 0 and not(optionChoisen): # Sort de d??g??ts
                                            logs += "\nSelected option : Damage skill"
                                            if len(atkSkill) > 1:
                                                randomSkill = atkSkill[random.randint(0,len(atkSkill)-1)]
                                            else:
                                                randomSkill = atkSkill[0]

                                            if randomSkill.range != AREA_MONO:
                                                atRange = actTurn.cell.getEntityOnArea(area=randomSkill.range,fromCell=actTurn.cell,team=actTurn.team,wanted=ENEMIES,lineOfSight = True,effect=randomSkill.effect,ignoreInvoc = (randomSkill.effectOnSelf == None or (randomSkill.effectOnSelf != None and findEffect(randomSkill.effectOnSelf).replica != None)))
                                                atRange.sort(key=lambda ent:actTurn.getAggroValue(ent),reverse=True)

                                                if len(atRange) > 0:
                                                    optionChoice = OPTION_SKILL
                                                    skillToUse = randomSkill
                                                    ennemi = atRange[0]
                                                else:
                                                    optionChoice = OPTION_SKIP

                                            else:
                                                optionChoice = OPTION_SKILL
                                                skillToUse = randomSkill
                                                ennemi = actTurn

                                            optionChoisen=True
                                        elif not(optionChoisen):
                                            probaRoll -= probTabl[2][choisenIA]

                                        if probaRoll <= probTabl[3][choisenIA] and probTabl[3][choisenIA] > 0 and not(optionChoisen): # D??g??ts indirects
                                            logs += "\nSelected option : Indirect damage skill"
                                            finded = True
                                            while 1:
                                                if len(indirectAtkSkill) > 1:
                                                    randomSkill = indirectAtkSkill[random.randint(0,len(indirectAtkSkill)-1)]
                                                elif len(indirectAtkSkill) == 0:
                                                    randomSkill = indirectAtkSkill[0]
                                                else:
                                                    finded = False
                                                    break

                                                atRange = actTurn.cell.getEntityOnArea(area=[randomSkill.range,randomSkill.area][randomSkill.range == AREA_MONO],team=actTurn.team,fromCell=actTurn.cell,wanted=ENEMIES,lineOfSight=randomSkill.range != AREA_MONO)
                                                if len(atRange) > 0:
                                                    break
                                                else:
                                                    logs += "\nNo target at range finded w/ {0}, retrying...".format(randomSkill.name)
                                                    indirectAtkSkill.remove(randomSkill)

                                            if finded:
                                                if randomSkill.range != AREA_MONO:
                                                    atRange.sort(key=lambda ent:actTurn.getAggroValue(ent),reverse=True)
                                                    optionChoice, skillToUse, ennemi = OPTION_SKILL, randomSkill, atRange[0]
                                                else:
                                                    optionChoice, skillToUse, ennemi = OPTION_SKILL, randomSkill, actTurn

                                                optionChoisen=True
                                        elif not(optionChoisen):
                                            probaRoll -= probTabl[3][choisenIA]

                                        if probaRoll <= probTabl[4][choisenIA] and probTabl[4][choisenIA] > 0 and not(optionChoisen): # Heal
                                            logs += "\nSelected option : Healing skill"
                                            if len(healSkill) > 1:
                                                randomSkill = healSkill[random.randint(0,len(healSkill)-1)]
                                            else:
                                                randomSkill = healSkill[0]

                                            if randomSkill.range != AREA_MONO:
                                                if randomSkill.id != vampirisme.id:
                                                    tablAtRange = actTurn.cell.getEntityOnArea(area=randomSkill.range,team=actTurn.team,fromCell=actTurn.cell,wanted=ALLIES,lifeUnderPurcentage=90,effect=randomSkill.effect)
                                                else:
                                                    tablAtRange = actTurn.cell.getEntityOnArea(area=randomSkill.range,team=actTurn.team,fromCell=actTurn.cell,wanted=ALLIES,lifeUnderPurcentage=90,effect=randomSkill.effect,ignoreAspiration=[ALTRUISTE,PROTECTEUR,PREVOYANT,IDOLE])
                                        
                                                optionChoice = OPTION_SKILL
                                                skillToUse = randomSkill
                                                ennemi = getHealTarget(tablAtRange,skillToUse)

                                            else:
                                                if len(actTurn.cell.getEntityOnArea(area=randomSkill.area,team=actTurn.team,wanted=ALLIES,fromCell=actTurn.cell,effect=randomSkill.effect,directTarget=False)) > 0 or (randomSkill == trans and actTurn.char.aspiration in [ALTRUISTE,IDOLE]):
                                                    optionChoice = OPTION_SKILL
                                                    skillToUse = randomSkill
                                                    ennemi = actTurn
                                            
                                            optionChoisen = True
                                        elif not(optionChoisen):
                                            probaRoll -= probTabl[4][choisenIA]

                                        if probaRoll <= probTabl[5][choisenIA] and probTabl[5][choisenIA] > 0 and not(optionChoisen): # Boost
                                            logs += "\nSelected option : Buff skill"
                                            if len(boostSkill) > 1:
                                                randomSkill = boostSkill[random.randint(0,len(boostSkill)-1)]
                                            else:
                                                randomSkill = boostSkill[0]

                                            if randomSkill.range != AREA_MONO: # Targeted Boost Spell
                                                atRange = actTurn.cell.getEntityOnArea(area=randomSkill.range,fromCell=actTurn.cell,team=actTurn.team,wanted=ALLIES,effect=randomSkill.effect,ignoreInvoc = True)
                                                effect = findEffect(randomSkill.effect[0])
                                                if effect.id not in [dmgUp.id,defenseUp.id,absEff.id]:
                                                    if effect.turnInit < 2 and actTurn in atRange:
                                                        atRange.remove(actTurn)
                                                    effectBoost = effect.allStats()+[effect.resistance,effect.percing,effect.critical]
                                                    boost = 0
                                                    for a in range(0,9):
                                                        if effectBoost[a] > effectBoost[boost]:
                                                            boost = a

                                                    atRange.sort(key=lambda ally: (ally.allStats()+[ally.resistance,ally.percing,ally.critical])[boost],reverse=True)
                                                elif effect.id in [dmgUp.id]:
                                                    allieValue = {}
                                                    for ent in atRange:
                                                        allieValue[ent] = ent.strength + ent.magie + ent.critical * 3 + ent.percing * 3
                                                        for cmpt in range(len(ent.cooldowns)):
                                                            if ent.cooldowns[cmpt] == 0:
                                                                skilly = findSkill(ent.char.skills[cmpt])
                                                                if skilly != None and skilly.type == TYPE_DAMAGE:
                                                                    allieValue[ent] += skilly.cooldown * 10 + int(skilly.ultimate) * 30
                                                    atRange.sort(key=lambda ally: allieValue[ent],reverse=True)
                                                elif effect.id in [defenseUp.id]:
                                                    atRange.sort(key=lambda ally: ally.endurance + ally.resistance,reverse=True)
                                                elif effect.id in [absEff.id]:
                                                    atRange.sort(key=lambda ally: ally.hp/ally.maxHp)

                                                optionChoice = OPTION_SKILL
                                                skillToUse = randomSkill
                                                ennemi = atRange[0]

                                            else:
                                                if len(actTurn.cell.getEntityOnArea(area=randomSkill.area,fromCell=actTurn.cell,team=actTurn.team,wanted=ALLIES,effect=randomSkill.effect,directTarget=False)) > 0:
                                                    optionChoice = OPTION_SKILL
                                                    skillToUse = randomSkill
                                                    ennemi = actTurn

                                            optionChoisen = True
                                        elif not(optionChoisen):
                                            probaRoll -= probTabl[5][choisenIA]

                                        if probaRoll <= probTabl[6][choisenIA] and probTabl[6][choisenIA] > 0 and not(optionChoisen): # Malus
                                            logs += "\nSelected option : Debuff skill"
                                            if len(malusSkill) > 1:
                                                randomSkill = malusSkill[random.randint(0,len(malusSkill)-1)]
                                            else:
                                                randomSkill = malusSkill[0]

                                            if randomSkill.range != AREA_MONO:
                                                atRange = actTurn.cell.getEntityOnArea(area=randomSkill.range,fromCell=actTurn.cell,team=actTurn.team,wanted=ENEMIES,effect=randomSkill.effect,ignoreInvoc = True)
                                                effect = findEffect(randomSkill.effect[0])
                                                effectBoost = effect.allStats()+[effect.resistance,effect.percing,effect.critical]
                                                boost = 0
                                                for a in range(0,9):
                                                    if effectBoost[a] > effectBoost[boost]:
                                                        boost = a

                                                atRange.sort(key=lambda ennemi: ennemi.allStats()[boost],reverse=True)
                                                optionChoice = OPTION_SKILL
                                                skillToUse = randomSkill
                                                try:
                                                    ennemi = atRange[0]
                                                except:
                                                    logs += "\nError : No valid target find"
                                                    optionChoice = OPTION_SKIP

                                            else:
                                                if len(actTurn.cell.getEntityOnArea(area=randomSkill.area,team=actTurn.team,fromCell=actTurn.cell,wanted=ENEMIES,effect=randomSkill.effect,directTarget=False)) > 0:
                                                    optionChoice = OPTION_SKILL
                                                    skillToUse = randomSkill
                                                    ennemi = actTurn

                                            optionChoisen=True
                                        elif not(optionChoisen):
                                            probaRoll -= probTabl[6][choisenIA]

                                        if probaRoll <= probTabl[7][choisenIA] and probTabl[7][choisenIA] > 0 and not(optionChoisen): # Armure
                                            logs += "\nSelected option : Armor skill"
                                            if len(armorSkill) > 1:
                                                randomSkill = findSkill(armorSkill[random.randint(0,len(armorSkill)-1)])
                                            else:
                                                randomSkill = findSkill(armorSkill[0])

                                            if randomSkill.range != AREA_MONO:
                                                if randomSkill.id != convert.id:
                                                    tablAtRange = actTurn.cell.getEntityOnArea(area=randomSkill.range,fromCell=actTurn.cell,team=actTurn.team,wanted=ALLIES,effect=randomSkill.effect)
                                                else:
                                                    tablAtRange = actTurn.cell.getEntityOnArea(area=randomSkill.range,team=actTurn.team,wanted=ALLIES,fromCell=actTurn.cell,effect=randomSkill.effect,ignoreAspiration=[ALTRUISTE,PREVOYANT,PROTECTEUR,IDOLE])
                                                
                                                tablAtRange.sort(key=lambda fepacho: fepacho.hp/fepacho.maxHp)

                                                optionChoice = OPTION_SKILL
                                                skillToUse = randomSkill
                                                ennemi = tablAtRange[0]

                                            else:
                                                if len(actTurn.cell.getEntityOnArea(area=randomSkill.area,team=actTurn.team,fromCell=actTurn.cell,wanted=ALLIES,effect=randomSkill.effect,directTarget=False)) > 0:
                                                    optionChoice = OPTION_SKILL
                                                    skillToUse = randomSkill
                                                    ennemi = actTurn
                                            
                                            optionChoisen = True
                                        elif not(optionChoisen):
                                            probaRoll -= probTabl[7][choisenIA]

                                        if probaRoll <= probaInvoc[choisenIA] and probaInvoc[choisenIA] > 0 and not(optionChoisen): #Invocation
                                            logs += "\nSelected option : Summon skill"
                                            if len(invocSkill) > 1:
                                                randomSkill = invocSkill[random.randint(0,len(invocSkill)-1)]
                                            else:
                                                randomSkill = invocSkill[0]

                                            optionChoice = OPTION_SKILL
                                            skillToUse = randomSkill
                                            optionChoisen = True
                                        elif not(optionChoisen):
                                            probaRoll -= probaInvoc[choisenIA]

                                        if probaRoll == -1 and probaAtkWeap[choisenIA] == probaHealWeap[choisenIA] == 0 and actTurn.char.weapon.emoji != '<:noneWeap:917311409585537075>' and not(optionChoisen):     # Can't use anything
                                            logs += "\nNo target at range. Trying to move"
                                            optionChoice,choiceToMove = OPTION_MOVE, actTurn.getCellToMove()
                                            optionChoisen = True

                                            if choiceToMove == None:
                                                optionChoice = OPTION_SKIP
                                                logs += "\nNo valid cells found. Skipping the turn"

                                        if not(optionChoisen):
                                            nbIte += 1
                                        else:
                                            break

                                    # Boss unique skills
                                    if actTurn.isNpc("S??r??na") and actTurn.cooldowns[2] == 0:
                                        poisonCount = 0
                                        for ent in tablEntTeam[int(not(actTurn.team))]:
                                            for eff in ent.effect:
                                                if eff.effect.id == estal.id:
                                                    poisonCount += 1

                                        if poisonCount >= 8:
                                            optionChoice = OPTION_SKILL
                                            skillToUse = serenaSpe
                                            ennemi = actTurn

                                    elif actTurn.isNpc("Ailill") and actTurn.cooldowns[0] == 0:
                                        atRangeAilill = actTurn.cell.getEntityOnArea(area=ailillSkill.range,team=actTurn.team,fromCell=actTurn.cell,wanted=ENEMIES,lineOfSight=True,effect=ailillSkill.effect,ignoreInvoc = (ailillSkill.effectOnSelf == None or (ailillSkill.effectOnSelf != None and findEffect(ailillSkill.effectOnSelf).replica != None)))
                                        if len(atRange) > 0:
                                            optionChoice = OPTION_SKILL
                                            skillToUse = ailillSkill
                                            atRangeAilill.sort(key=lambda ent:actTurn.getAggroValue(ent),reverse=True)
                                            ennemi = atRange[0]

                                    elif (actTurn.isNpc("Luna pr??.") or actTurn.isNpc("Luna ex.")) and (actTurn.cooldowns[0] == 0 or (actTurn.hp/actTurn.maxHp <= 0.25 and actTurn.cooldowns[0] < 10)):
                                        optionChoice = OPTION_SKILL
                                        skillToUse = lunaSpeCast
                                        for ent in tablEntTeam[int(not(actTurn.team))]:
                                            if ent.isNpc("Iliana") and ent.hp > 0:
                                                ennemi = ent
                                                break

                                        if ennemi == None:
                                            atRange = actTurn.cell.getEntityOnArea(area=AREA_ALL_ENEMIES,fromCell=actTurn.cell,team=actTurn.team,wanted=ENEMIES)
                                            atRange.sort(key=lambda ent:actTurn.getAggroValue(ent),reverse=True)
                                            ennemi = atRange[0]

                                    elif actTurn.isNpc("Cl??mence pos.") and actTurn.cooldowns[2] == 0 and (tour >= 7 or actTurn.hp/actTurn.maxHp <= 0.35):
                                        optionChoice = OPTION_SKILL
                                        skillToUse = clemUltCast
                                        ennemi = actTurn

                                    elif actTurn.isNpc("Akira H.") and actTurn.hp/actTurn.maxHp <= 0.2:
                                        optionChoice = OPTION_SKILL
                                        skillToUse = akikiEnrageCastInit
                                        ennemi = actTurn
                            # ==========================================
                            else:
                                logs += "\nReplica found"
                                skilly = findSkill(onReplica.effect.replica)
                                if onReplica.replicaTarget.hp > 0:
                                    optionChoice = OPTION_SKILL
                                    skillToUse = skilly
                                    ennemi = onReplica.replicaTarget
                                else:
                                    logs += "\nInitial target down, taking another target at range"
                                    skilly = copy.deepcopy(skilly)
                                    skilly.power = int(skilly.power * (0.7-0.2*int(skilly.area != AREA_MONO)))
                                    skilly.name = skilly.name + " 0.5"
                                    skilly.effPowerPurcent = [100, skilly.effPowerPurcent][skilly.effPowerPurcent != None] * (0.7-0.2*int(skilly.area != AREA_MONO))

                                    atRange = actTurn.cell.getEntityOnArea(area=skilly.range,fromCell=actTurn.cell,team=actTurn.team,wanted=ENEMIES,lineOfSight=True,effect=skilly.effect,ignoreInvoc = True)

                                    if len(atRange) <= 0:
                                        atRange = actTurn.cell.getEntityOnArea(area=AREA_CIRCLE_7,team=actTurn.team,fromCell=actTurn.cell,wanted=ENEMIES,lineOfSight=True,ignoreInvoc = True)
                                        logs += "\nNo fucking target at range. The ennemi in line of sight with the more aggro will be targeted, but the power will be cut again"
                                        skilly.power = int(skilly.power*0.7)
                                        skilly.effPowerPurcent = skilly.effPowerPurcent * 0.7
                                    
                                    if len(atRange) > 0:
                                        atRange.sort(key=lambda ent:actTurn.getAggroValue(ent),reverse=True)

                                        optionChoice = OPTION_SKILL
                                        skillToUse = skilly
                                        ennemi = atRange[0]
                                    else:
                                        optionChoice = OPTION_SKIP

                            lunaUsedQuickFight = ""

                            if not(actTurn.char.canMove) and optionChoice == OPTION_MOVE:
                                optionChoice = OPTION_SKIP

                            if optionChoice == OPTION_WEAPON: #Option : Weapon
                                for eff in actTurn.effect:
                                    if eff.effect.id == lunaQuickFightEff.id:
                                        replay = True
                                        lunaUsedQuickFight += eff.decate(1)
                                        needRefresh = True
                                        actTurn.refreshEffects()
                                        break

                                if actTurn.char.weapon.say != "":
                                    if type(actTurn.char.weapon.say) == str:
                                        tempTurnMsg += f"\n{actTurn.icon} : *\"{actTurn.char.weapon.say}\"*"
                                    else:
                                        if len(actTurn.char.weapon.say) > 0:
                                            tempTurnMsg += "\n{0} : *\"{1}\"*".format(actTurn.icon,actTurn.char.weapon.say[random.randint(0,len(actTurn.char.weapon.say)-1)])
                                        else:
                                            tempTurnMsg += "\n{0} : *\"{1}\"*".format(actTurn.icon,actTurn.char.weapon.say[0])
                                if actTurn.char.weapon.type in [TYPE_DAMAGE,TYPE_INDIRECT_DAMAGE]: # Agressive Weapon
                                    logs += "\n{0} is attacking {1} with their weapon\n".format(actTurn.char.name,ennemi.char.name)
                                    cmpt = 0
                                    while cmpt < iteration:
                                        isAlive = ennemi.hp > 0
                                        if not(isAlive) :
                                            break
                                        if cmpt == 0:
                                            if actTurn.char.weapon.message == None:
                                                tempTurnMsg += f"\n__{actTurn.char.name} attaque {ennemi.char.name} avec son arme :__\n"
                                            else:
                                                tempTurnMsg += "\n__"+actTurn.char.weapon.message.format(actTurn.char.name,ennemi.char.name)+"__\n"
                                        else:
                                            tempTurnMsg += "\n"
                                        power = actTurn.char.weapon.power

                                        funnyTempVarName, deathCount = actTurn.attack(target=ennemi,value=power,icon=actTurn.char.weapon.emoji,area=actTurn.char.weapon.area,use=actTurn.char.weapon.use,onArmor=actTurn.char.weapon.onArmor,effectOnHit=actTurn.char.weapon.effectOnUse)
                                        logs+= funnyTempVarName
                                        tempTurnMsg += funnyTempVarName
                                        cmpt += 1

                                        if actTurn.char.weapon.id == flyfishweap.id:
                                            tempTabl = copy.copy(tablEntTeam[0])
                                            try:
                                                temp.remove(ennemi)
                                            except:
                                                pass

                                            for ent in tempTabl[:]:
                                                if ent.hp <= 0:
                                                    tempTabl.remove(ent)

                                            tempTabl.sort(key=lambda ent: ent.stats.damageDeal,reverse=True)
                                            if len(tempTabl) > 0:
                                                ennemi2 = tempTabl[0]
                                                funnyTempVarName = add_effect(actTurn,ennemi2,findEffect(actTurn.char.weapon.effectOnUse),skillIcon=flyfishweap.emoji,effPowerPurcent=70)
                                                
                                                logs+= funnyTempVarName
                                                tempTurnMsg += funnyTempVarName
                                                ennemi2.refreshEffects()

                                    if actTurn.char.weapon.power > 0 and actTurn.specialVars["damageSlot"] != None:
                                        loose = int(actTurn.maxHp * (15/100))
                                        tempTurnMsg += "{0} : -{1} PV ({2})\n".format(actTurn.icon,loose,actTurn.specialVars["damageSlot"].effect.name)
                                        actTurn.hp -= loose
                                        if actTurn.hp <= 0:
                                            tempTurnMsg += actTurn.death(killer=actTurn)

                                        actTurn.refreshEffects()

                                elif actTurn.char.weapon.type in [TYPE_HEAL,TYPE_INDIRECT_HEAL]: # None agressive Weapon
                                    logs += "\n\n{0} is healing {1} with their weapon\n".format(actTurn.char.name,ennemi.char.name)
                                    if actTurn.char.weapon.message == None:
                                        if actTurn != ennemi:
                                            tempTurnMsg += f"\n__{actTurn.char.name} soigne {ennemi.char.name} avec son arme :__\n"
                                        else:
                                            tempTurnMsg += "\n__{0} utilise son arme sur {1}-m??me :__\n".format(actTurn.char.name,["lui","elle"][actTurn.char.gender == GENDER_FEMALE])
                                    else:
                                        tempTurnMsg += "\n__"+actTurn.char.weapon.message.format(actTurn.char.name,ennemi.char.name)+"__\n"

                                    for a in ennemi.cell.getEntityOnArea(area=actTurn.char.weapon.area,team=actTurn.team,fromCell=actTurn.cell,wanted=ALLIES,directTarget=False):
                                        funnyTempVarName, useless = actTurn.heal(a, actTurn.char.weapon.emoji, actTurn.char.weapon.use, actTurn.char.weapon.power,danger=danger,mono=actTurn.char.weapon.area == AREA_MONO)
                                        tempTurnMsg += funnyTempVarName
                                        logs += funnyTempVarName

                                    if actTurn.char.weapon.effectOnUse != None:
                                        funnyTempVarName = add_effect(actTurn,ennemi,findEffect(actTurn.char.weapon.effectOnUse),danger=danger)
                                        
                                        logs+= funnyTempVarName
                                        tempTurnMsg += funnyTempVarName

                                        ennemi.refreshEffects()

                                if actTurn.char.weapon.id in [whiteSpiritWings.id,bleuSpiritWings.id]:
                                    tempTabl = []
                                    for ent in tablEntTeam[actTurn.team]:
                                        if ent.hp > 0:
                                            tempTabl.append(ent)

                                    if len(tempTabl) > 0:
                                        tempTabl.sort(key=lambda chaton: chaton.hp/chaton.maxHp)
                                        if actTurn.char.weapon.id in [whiteSpiritWings.id]:
                                            funnyTempVarName, useless = actTurn.heal(tempTabl[0], actTurn.char.weapon.effect.emoji[0][0], actTurn.char.weapon.use, actTurn.char.weapon.effect.power, danger=danger, effName = actTurn.char.weapon.effect.name, mono=actTurn.char.weapon.area == AREA_MONO)
                                            tempTurnMsg += funnyTempVarName
                                            logs += funnyTempVarName

                                        else:
                                            funnyTempVarName = add_effect(actTurn,tempTabl[0],findEffect(actTurn.char.weapon.effect.callOnTrigger),danger=danger,start=actTurn.char.weapon.effect.name,skillIcon = actTurn.weapon.effect.emoji[0][0])
                                            logs+= funnyTempVarName
                                            tempTurnMsg += funnyTempVarName
                                            tempTabl[0].refreshEffects()

                                elif actTurn.char.weapon.id == fleau.id:
                                    tablName = []
                                    for ent in actTurn.cell.getEntityOnArea(area=actTurn.char.weapon.effect.area,fromCell=actTurn.cell,team=actTurn.team,wanted=ALLIES,directTarget=False):
                                        eff = actTurn.char.weapon.effect.callOnTrigger
                                        ballerine = add_effect(actTurn,ent,eff,danger=danger)
                                        if '????' not in ballerine and ballerine != "":
                                            tablName.append(ent.icon)
                                            ent.refreshEffects()

                                    if tablName != []:
                                        temp = "{0} {1} ??? ".format(actTurn.icon,actTurn.weapon.effect.emoji[0][0])
                                        for cmpt in tablName:
                                            temp += cmpt

                                        tempTurnMsg += temp + " +{0} __{1}__\n".format(actTurn.weapon.effect.emoji[0][0],actTurn.weapon.effect.name)
                                        logs += temp

                                elif actTurn.char.weapon.id in [micPurple.id,micRed.id,micPink.id]:
                                    tablName, eff = [], actTurn.weapon.effect.callOnTrigger
                                    for ent in actTurn.cell.getEntityOnArea(area=actTurn.weapon.effect.area,fromCell=actTurn.cell,team=actTurn.team,wanted=ALLIES,directTarget=False):
                                        ballerine = add_effect(actTurn,ent,eff,danger=danger,useActionStats=ACT_BOOST,skillIcon = actTurn.weapon.emoji)
                                        if '????' not in ballerine and ballerine != "":
                                            tablName.append(ent.icon)
                                        ent.refreshEffects()

                                    if tablName != []:
                                        temp = ""
                                        for cmpt2 in tablName:
                                            temp += cmpt2

                                        temp = "{1} {2} ??? {3} +{0} __{4}__\n".format(eff.emoji[actTurn.char.species-1][actTurn.team],actTurn.icon,actTurn.char.weapon.emoji,temp,eff.name)
                                        tempTurnMsg += temp
                                        logs += temp

                            elif optionChoice == OPTION_MOVE: #Option : D??placement
                                logs += "\n{0} is moving".format(actTurn.char.name)
                                temp = actTurn.cell
                                actTurn.move(cellToMove=choiceToMove)
                                logs += "\n{0} have been moved from {1}:{2} to {3}:{4}".format(actTurn.char.name,temp.x,temp.y,choiceToMove.x,choiceToMove.y)
                                tempTurnMsg+= "\n"+actTurn.char.name+" se d??place\n"

                            elif optionChoice == OPTION_SKIP: #Passage de tour
                                logs += "\n{0} is skipping their turn".format(actTurn.char.name)
                                tempTurnMsg += f"\n{actTurn.char.name} passe son tour\n"
                                actTurn.stats.turnSkipped += 1

                            elif optionChoice == OPTION_SKILL: #Skill
                                qCast, needRefresh, useEffElem = False, False, 0

                                if skillToUse.id == finFloLaunchBase.id:
                                    skillToUse, listEff, allReadySeen, golden = copy.deepcopy(finFloLaunchBase), [], [], 0
                                    for eff in actTurn.effect:
                                        if eff.effect.id in tablRosesId and eff.effect.id not in allReadySeen:
                                            if eff.effect.id == roseRed.id:
                                                listEff.append(finFloEffList[0])
                                            elif eff.effect.id == roseDarkBlu.id:
                                                listEff.append(finFloEffList[1])
                                            elif eff.effect.id == roseBlue.id:
                                                listEff.append(finFloEffList[2])
                                            elif eff.effect.id == roseGreen.id:
                                                skillToUse.effectOnSelf = finFloEffList[3]
                                            elif eff.effect.id == roseYellow.id:
                                                golden = 2
                                            elif eff.effect.id == rosePink.id:
                                                golden = 1
                                            eff.decate(value=99)
                                            allReadySeen.append(eff.effect.id)
                                    actTurn.refreshEffects()

                                    if golden == 1:
                                        for eff in listEff:
                                            eff.turnInit += 1
                                    elif golden == 2:
                                        skillToUse.effPowerPurcent = 130

                                    if listEff != []:
                                        skillToUse.effect = listEff
                                elif skillToUse.id == horoscope.id:
                                    skillToUse, horoEff, tablStats = copy.deepcopy(horoscope), classes.effect("Horoscope","horoscope",INTELLIGENCE,turnInit=3,emoji=sameSpeciesEmoji('<:horoscope:960312586371477524>','<:horoscope:960312676469321838>')), [0,0,0,0,0,0,0]
                                    for eff in actTurn.effect:
                                        for effy in horoscopeEff:
                                            if eff.effect.id == effy[0].id:
                                                for staty in effy[1]:
                                                    tablStats[staty[0]] += staty[1]
                                                eff.decate(value=99)
                                    needRefresh = True
                                    horoEff.strength, horoEff.endurance, horoEff.charisma, horoEff.agility, horoEff.precision, horoEff.intelligence, horoEff.magie = tuple(tablStats)
                                    bestStat = [[0,horoEff.strength],[1, horoEff.endurance],[2, horoEff.charisma],[3, horoEff.agility],[4, horoEff.precision],[5, horoEff.intelligence],[6, horoEff.magie]]
                                    bestStat.sort(key=lambda astralSign: astralSign[1],reverse=True)
                                    horoEff.name += " " + hroscopeNickNames[bestStat[0][0]]
                                    skillToUse.effect = [horoEff]

                                for eff in actTurn.effect:
                                    if eff.effect.id == quickCastEff.id:
                                        qCast = True
                                    elif eff.effect.id == lunaQuickFightEff.id:
                                        replay = True
                                        lunaUsedQuickFight += eff.decate(1)
                                        needRefresh = True
                                    elif skillToUse.id in useElemEffId+elemArrowId+elemRuneId and eff.effect.id in [tablElemEff[actTurn.char.element].id,tablElemEff[ELEMENT_UNIVERSALIS_PREMO].id]:
                                        eff.decate(turn=99)
                                        useEffElem += 1
                                        needRefresh = True
                                if needRefresh:
                                    actTurn.refreshEffects()
                                
                                if skillToUse.id in useElemEffId+elemArrowId+elemRuneId:
                                    skillToUse = copy.deepcopy(skillToUse)
                                    skillToUse.name = skillToUse.name + " +{0}".format(useEffElem)

                                if qCast and skillToUse.effectOnSelf != None and findEffect(skillToUse.effectOnSelf).replica != None:
                                    skillToUse = copy.deepcopy(findSkill(findEffect(skillToUse.effectOnSelf).replica))
                                    skillToUse.power, skillToUse.effPowerPurcent = int(skillToUse.power*0.7), skillToUse.effPowerPurcent * 0.7

                                if skillToUse.effectOnSelf != None and findEffect(skillToUse.effectOnSelf).replica != None and actTurn.auto:
                                    for cmpt in (0,1,2,3,4):
                                        if type(actTurn.char.skills[cmpt]) == skill and actTurn.cooldowns[cmpt] == 0 and actTurn.char.skills[cmpt].id == quickCast.id:
                                            skillToUse = quickCast
                                            ennemi = actTurn
                                            break

                                if skillToUse.needEffect != None:
                                    for needed in skillToUse.needEffect:
                                        for eff in actTurn.effect:
                                            if needed.id == eff.effect.id:
                                                eff.decate(turn=99)
                                                break
                                    actTurn.refreshEffects()

                                try:
                                    logs += "\n\n{0} is using {1} on {2}\n".format(actTurn.char.name,skillToUse.name,ennemi.char.name)
                                except:
                                    logs += "\n\nError on writing into the logs"
                                if skillToUse.say != "":
                                    if type(skillToUse.say) == str:
                                        tempTurnMsg += f"\n{actTurn.icon} : *\"{skillToUse.say}\"*"
                                    else:
                                        if len(skillToUse.say) > 0:
                                            tempTurnMsg += "\n{0} : *\"{1}\"*".format(actTurn.icon,skillToUse.say[random.randint(0,len(skillToUse.say)-1)])
                                        else:
                                            tempTurnMsg += "\n{0} : *\"{1}\"*".format(actTurn.icon,skillToUse.say[0])

                                # Say Ultimate
                                if actTurn.char.says.ultimate != None and skillToUse.ultimate and not(skillToUse.effectOnSelf != None and findEffect(skillToUse.effectOnSelf).replica != None and skillToUse.power == 0 and skillToUse.effect == [None]):
                                    try:
                                        tempTurnMsg += "\n{0} : *\"{1}\"*".format(actTurn.icon,actTurn.char.says.ultimate.format(target=ennemi.char.name,caster=actTurn.char.name,skill=skillToUse.name))
                                    except:
                                        tempTurnMsg += "\n__Error with the ultimate message.__ See logs for more informations"
                                        logs += "\n"+format_exc()

                                # Say Limite Break
                                if actTurn.char.says.limiteBreak != None and skillToUse.id == trans.id:
                                    try:
                                        tempTurnMsg += "\n{0} : *\"{1}\"*".format(actTurn.icon,actTurn.char.says.limiteBreak.format(target=ennemi.char.name,caster=actTurn.char.name,skill=skillToUse.name))
                                    except:
                                        tempTurnMsg += "\n__Error with the Limite Break message.__ See logs for more informations"
                                        logs += "\n"+format_exc()

                                # Skill base message
                                if skillToUse.message == None:
                                    tempTurnMsg += f"\n__{actTurn.char.name} utilise la comp??tence {skillToUse.name} :__\n"
                                else: 
                                    tempTurnMsg += "\n__"+ skillToUse.message.format(actTurn.char.name,skillToUse.name,ennemi.char.name)+"__\n"

                                # Set the cooldown
                                for a in range(7):
                                    if type(actTurn.char.skills[a]) == skill:
                                        if skillToUse.id == actTurn.char.skills[a].id:
                                            actTurn.cooldowns[a] = skillToUse.cooldown
                                        if skillToUse.id == "lb" and actTurn.char.skills[a].ultimate and actTurn.cooldowns[a] < 2:          # Anti LB in Ult combo
                                            actTurn.cooldowns[a] = 2
                                        if skillToUse.id == "lb":
                                            LBBars[actTurn.team][1] = 0

                                # Share cooldown
                                if skillToUse.shareCooldown:
                                    for a in tablEntTeam[actTurn.team]:
                                        if a.char.team == actTurn.char.team:
                                            for b in range(0,len(a.char.skills)):
                                                if type(a.char.skills[b]) == skill:
                                                    if a.char.skills[b].id == skillToUse.id:
                                                        a.cooldowns[b] = skillToUse.cooldown

                                # Mors Vita Est set share cooldown
                                # tpCac
                                if skillToUse.tpCac and actTurn.cell.distance(ennemi.cell) > 1:
                                    surrond = ennemi.cell.surrondings()
                                    for a in surrond[:]:
                                        if a == None or (a != None and a.on != None):
                                            surrond.remove(a)

                                    if len(surrond) > 0:
                                        surrond.sort(key=lambda celly:actTurn.cell.distance(celly))
                                        actTurn.move(cellToMove=surrond[0])
                                        tempTurnMsg += "__{0}__ se t??l??porte au corps ?? corps de __{1}__\n".format(actTurn.name,ennemi.name)

                                    elif not(actTurn.isNpc('Ailill')):
                                        tempTurnMsg += "__{0}__ essaye de se t??l??porte au corps ?? corps de __{1}__, mais cela ??choue\n".format(actTurn.name,ennemi.name)
                                        stat,damageBase = -100,20

                                        for stats in actTurn.allStats():
                                            stat = max(stats,stat)

                                        damage = damageBase * (1+(stat/100)) * (1-(min(95,actTurn.resistance*(1-actTurn.percing/100))/100)) * actTurn.getElementalBonus(actTurn,AREA_MONO,TYPE_INDIRECT_DAMAGE) * (1+(0.01*actTurn.level))
                                        temp = actTurn.indirectAttack(actTurn,value=damage,name="Fissure spacio-temporelle")
                                        tempTurnMsg += temp
                                        logs += temp

                                    else:
                                        surrond = ennemi.cell.surrondings()
                                        for a in surrond[:]:
                                            if a == None or (a != None and a.on == None):
                                                surrond.remove(a)
                                        if len(surrond) > 1:
                                            unlucky = surrond[0].on
                                        else:
                                            unlucky = surrond[random.randint(0,len(surrond)-1)].on
                                        stat,damageBase = -100,20

                                        for stats in actTurn.allStats():
                                            stat = max(stats,stat)

                                        damage = damageBase * (1+(stat/100)) * (1-(min(95,unlucky.resistance*(1-actTurn.percing/100))/100)) * actTurn.getElementalBonus(unlucky,AREA_MONO,TYPE_INDIRECT_DAMAGE) * (1+(0.01*actTurn.level))
                                        temp = actTurn.cell
                                        actTurn.move(cellToMove=unlucky.cell)
                                        unlucky.move(cellToMove=temp)

                                        tempTurnMsg += "__{0}__ ??change de place avec __{2}__ pour ??tre au corps ?? corps de __{1}__\n".format(actTurn.name,ennemi.name,unlucky.name)
                                        temp = actTurn.indirectAttack(unlucky,value=damage,name="Fissure spacio-temporelle")
                                        tempTurnMsg += temp
                                        logs += temp

                                    if skillToUse.areaOnSelf:
                                        ennemi = actTurn

                                # Luna and Iliana Head to Head
                                if skillToUse.id == lunaSpe.id:
                                    if not(ennemi.isNpc("Luna pr??.") or ennemi.isNpc("Cl??mence Exalt??e")):
                                        if actTurn.specialVars["clemBloodJauge"] == None:
                                            actTurn.specialVars["clemBloodJauge"] = 0

                                            cellToCheck, actCell = findCell(actTurn.cell.x+1,actTurn.cell.y,tablAllCells), actTurn.cell
                                            if cellToCheck != None and cellToCheck.on == None:
                                                actTurn.move(cellToMove=cellToCheck)
                                                ennemi.move(cellToMove=actCell)

                                            elif actCell.distance(ennemi.cell) > 1:
                                                surron = actCell.surrondings()
                                                for celly in surron[1:4]:
                                                    if celly != None and celly.on == None:
                                                        ennemi.move(cellToMove=celly)
                                                        break

                                        mainPower = lunaSpe.power * (0.7+(0.3*actTurn.specialVars["clemBloodJauge"])+0.25*int(ennemi.char.element!=ELEMENT_LIGHT))
                                        secondaryPower = lunaSpe.power * 0.2 * (0.7+(0.3*actTurn.specialVars["clemBloodJauge"])+0.25*int(ennemi.char.element!=ELEMENT_LIGHT))

                                        isThereAShield = False
                                        for fightEff in actTurn.effect:
                                            if fightEff.effect.id == lunaInfiniteDarknessShield.id:
                                                isThereAShield = True
                                                fightEff.replicaTarget = ennemi
                                                break
                                        if not(isThereAShield):
                                            ballerine = add_effect(actTurn,actTurn,lunaInfiniteDarknessShield,danger=danger,setReplica=ennemi)
                                            tempTurnMsg += ballerine
                                            logs += "\n"+ballerine
                                            actTurn.refreshEffects()

                                        # Iliana main damage taking
                                        if actTurn.specialVars["clemBloodJauge"] == 0 and ennemi.char.says.blockBigAttack != None:
                                            try:
                                                tempTurnMsg += "{0} : *\"{1}\"*\n".format(ennemi.icon,ennemi.char.says.blockBigAttack.format(target=ennemi.char.name,caster=actTurn.char.name,skill=skillToUse.name))
                                            except:
                                                tempTurnMsg += "\n__Error with the BlockBigAttack.__ See logs for more informations"
                                                logs += "\n"+format_exc()
                                        funnyTempVarName, deathCount = actTurn.attack(target=ennemi,value=mainPower,icon='<:lunaSecDamage:929705185016692786>',area=AREA_MONO,sussess=500,use=skillToUse.use,onArmor=skillToUse.onArmor)
                                        tempTurnMsg += funnyTempVarName
                                        logs += "\n"+funnyTempVarName

                                        # If she's still alive, the other allies takes less damages
                                        if ennemi.hp > 0 and actTurn.specialVars["clemBloodJauge"] != None:
                                            funnyTempVarName, deathCount = actTurn.attack(target=ennemi,value=secondaryPower,icon='<a:lunaHeadToHead:929707180943355914>',area=AREA_DONUT_7,sussess=500,use=skillToUse.use,onArmor=skillToUse.onArmor,setAoEDamage=True)
                                            tempTurnMsg += funnyTempVarName
                                            logs += "\n"+funnyTempVarName

                                            actTurn.specialVars["clemBloodJauge"] += 1

                                            logs += "\n"+add_effect(actTurn,ennemi,lunaInfiniteDarknessStun)
                                            ennemi.refreshEffects()

                                        # But she's dead, so everybody take tarif
                                        else:
                                            funnyTempVarName, deathCount = actTurn.attack(target=actTurn,value=mainPower,icon='<:lunaFinal:929705208085381182>',area=AREA_ALL_ENEMIES,sussess=500,use=skillToUse.use,onArmor=int(skillToUse.onArmor*1.2),setAoEDamage=True)
                                            tempTurnMsg += funnyTempVarName
                                            logs += "\n"+funnyTempVarName

                                            for fightEff in actTurn.effect:
                                                if fightEff.effect.id == lunaInfiniteDarknessShield.id:
                                                    fightEff.decate(value=99999999999999999999)
                                                    actTurn.refreshEffects()
                                                    actTurn.specialVars["clemBloodJauge"] = None
                                                    break
                                    
                                    else:
                                        funnyTempVarName, temp = actTurn.attack(target=ennemi,value=skillToUse.power*1.5,icon=skillToUse.emoji,area=skillToUse.area,sussess=500,use=skillToUse.use,onArmor=skillToUse.onArmor,useActionStats=actionStats,setAoEDamage=skillToUse.setAoEDamage,lifeSteal = skillToUse.lifeSteal,erosion = skillToUse.erosion, skillPercing = skillToUse.percing, execution=skillToUse.execution)
                                        tempTurnMsg += funnyTempVarName
                                        logs += "\n"+funnyTempVarName
                                        deathCount += temp

                                elif skillToUse.id == plumRem.id:
                                    for ent in ennemi.cell.getEntityOnArea(area=skillToUse.area,team=actTurn.team,wanted=ENEMIES,ignoreInvoc = True, directTarget=False,fromCell=actTurn.cell):
                                        nbPlume = 0
                                        for eff in ent.effect:
                                            if eff.effect.id == plumRemEff.id:
                                                temp, temp2 = actTurn.attack(target=ent,value = eff.effect.power,icon = eff.icon ,area=AREA_MONO,sussess=200)
                                                logs += temp
                                                tempTurnMsg += temp
                                                eff.decate(turn=99)
                                                nbPlume += 1
                                        if nbPlume == 0:
                                            tempTurnMsg += "Cela n'affecte pas {0}\n".format(ent.name)
                                        else:
                                            ent.refreshEffects()
                                        
                                # ======================== Any other skill ========================
                                else:
                                    if skillToUse.effectOnSelf != None and skillToUse.effBeforePow:
                                        effect = findEffect(skillToUse.effectOnSelf)
                                        tempTurnMsg = [tempTurnMsg[:-1],tempTurnMsg][skillToUse.type != TYPE_HEAL] + add_effect(actTurn,actTurn,effect,effPowerPurcent=skillToUse.effPowerPurcent,skillIcon = skillToUse.emoji)
                                        logs += "\n{0} gave the {1} effect at {2} for {3} turn(s)".format(actTurn.char.name,effect.name,ennemi.char.name,effect.turnInit)
                                    if skillToUse.type in [TYPE_BOOST,TYPE_ARMOR,TYPE_INDIRECT_HEAL,TYPE_INDIRECT_REZ] and skillToUse.effect != [None]:
                                        if skillToUse.id != clemUltCast.id:
                                            if skillToUse.id == bolide.id:
                                                tempTurnMsg += "{0} {1} ??? {0} -{2} PV\n".format(actTurn.icon,skillToUse.emoji,actTurn.hp -1)
                                                actTurn.stats.selfBurn += actTurn.hp -1
                                                actTurn.hp = 1
                                            ballerine = groupAddEffect(caster=actTurn, target=ennemi, area=skillToUse.area, effect=skillToUse.effect, skillIcon=skillToUse.emoji, actionStats=skillToUse.useActionStats, effPurcent = skillToUse.effPowerPurcent)
                                            tempTurnMsg += ballerine
                                            logs += ballerine

                                            if skillToUse.type == TYPE_BOOST and skillToUse.range == AREA_MONO and actTurn.specialVars["partner"] != None and actTurn.specialVars["partner"].hp > 0:
                                                initArea = actTurn.cell.getEntityOnArea(area=skillToUse.area,team=actTurn.team,wanted=ALLIES,directTarget=False)
                                                secondArea = actTurn.specialVars["partner"].cell.getEntityOnArea(area=skillToUse.area,fromCell=actTurn.cell,team=actTurn.team,wanted=ALLIES,directTarget=False)

                                                for ent in secondArea[:]:
                                                    if ent in initArea or ent == actTurn:
                                                        secondArea.remove(ent)

                                                if len(secondArea) > 0:
                                                    effPower = [skillToUse.effPowerPurcent,100][skillToUse.effPowerPurcent == None]
                                                    ballerine = groupAddEffect(caster=actTurn, target=actTurn.specialVars["partner"], area=secondArea, effect=skillToUse.effect, skillIcon=partner.emoji, actionStats=skillToUse.useActionStats, effPurcent = [effPower * partnerIn.power * 0.01,effPower][findEffect(skillToUse.effect[0]).id == tangoEndEff.id])
                                                    tempTurnMsg += ballerine
                                                    logs += ballerine

                                        else:
                                            effect = skillToUse.effect[0]
                                            tempVal, clemShieldBefore = max(actTurn.specialVars["clemBloodJauge"].value-1,30), actTurn.stats.shieldGived
                                            effect.overhealth = tempVal * 2
                                            tempTurnMsg += add_effect(actTurn,actTurn,effect,danger=danger)
                                            logs += "\nClemClem gave herself her ult shield with {2} PAr (base power : {0} ({1} * 2))".format(effect.overhealth,tempVal, actTurn.stats.shieldGived-clemShieldBefore)
                                            actTurn.refreshEffects()

                                            actTurn.specialVars["clemBloodJauge"].value = 1
                                            actTurn.specialVars["clemMemCast"] = True

                                    elif skillToUse.type in [TYPE_INDIRECT_DAMAGE,TYPE_MALUS]:
                                        if skillToUse.id != serenaSpe.id:
                                            ballerine = groupAddEffect(caster=actTurn, target=ennemi, area=skillToUse.area, effect=skillToUse.effect, skillIcon=skillToUse.emoji, actionStats=skillToUse.useActionStats, effPurcent = skillToUse.effPowerPurcent)
                                            tempTurnMsg += ballerine
                                            logs += ballerine
                                        else:
                                            for ent in tablEntTeam[int(not(actTurn.team))]:
                                                if ent.hp > 0:
                                                    sumPower = 0
                                                    for eff in ent.effect:
                                                        if eff.effect.id == estal.id:
                                                            sumPower += int(eff.effect.power*eff.turnLeft*(skillToUse.power/100))
                                                            eff.decate(value=100)

                                                    if sumPower > 0:
                                                        ent.refreshEffects()
                                                        sumPower += estal.power * estal.turnInit * (skillToUse.power/100)
                                                        temp = actTurn.indirectAttack(target=ent,value=indirectDmgCalculator(actTurn, ent, sumPower, skillToUse.use, danger, skillToUse.area),icon=skillToUse.emoji)
                                                    else:
                                                        temp = "Cela a aucun effet sur __{0}__\n".format(ent.name)
                                                    tempTurnMsg += temp
                                                    logs += temp

                                        if skillToUse.id == cwUlt.id:
                                            power = 0
                                            for eff in ennemi.effect:
                                                if eff.effect.type == TYPE_INDIRECT_DAMAGE:
                                                    if eff.effect.id == coroWind.id:
                                                        power += skillToUse.power * eff.turnLeft/eff.effect.turnInit
                                                    else:
                                                        power += skillToUse.power * eff.turnLeft/eff.effect.turnInit * 1.35
                                                        eff.decate(turn=99)
                                            
                                            if power > 0:
                                                ballerine = actTurn.indirectAttack(ennemi,value=indirectDmgCalculator(actTurn, ennemi, power, skillToUse.use, danger, area=skillToUse.area),icon = skillToUse.emoji)
                                                tempTurnMsg += ballerine
                                                logs += ballerine
                                                ennemi.refreshEffects()

                                        elif skillToUse.id == propag.id:
                                            listTarget = []
                                            sumPower = 0
                                            for eff in ennemi.effect:
                                                if eff.effect.id in [estal.id] and eff.value > 0:
                                                    sumPower += eff.effect.power * ([propag.power,propag.power//2][int(eff.caster==actTurn)])/100

                                            effTabl, tablName, effTabl2 = [estal],[[]],[estal2]
                                            for ent in ennemi.cell.getEntityOnArea(area=AREA_DONUT_2,team=actTurn.team,wanted=ENEMIES,fromCell=actTurn.cell,directTarget=False):
                                                if sumPower > 0:
                                                    add_effect(actTurn,ent,effTabl[0],effPowerPurcent=int((sumPower/effTabl[0].power)*100))
                                                    tablName[0].append("{0}".format(ent.icon))
                                                    ent.refreshEffects()

                                            temp = ""
                                            if len(tablName[0]) == 1:
                                                temp = "\n{2} {4} ??? {0} +{1} ({3}%)".format(tablName[0][0],effTabl[0].emoji[0][0],actTurn.icon,int((sumPower/effTabl[0].power)*100),skillToUse.emoji)
                                            elif len(tablName[0]) > 1:
                                                temp = ""
                                                for cmpt in range(len(tablName[0])):
                                                    temp += tablName[0][cmpt]

                                                temp = "\n{2} {4} ??? {0} +{1} ({3}%)".format(temp,effTabl[0].emoji[0][0],actTurn.icon,int((sumPower/effTabl[0].power)*100),skillToUse.emoji)
                                            if actTurn.specialVars["heritEstial"]:
                                                if len(tablName[0]) == 1:
                                                    temp += "\n{0} subit l'effet {1} {2} pendant 3 tours".format(tablName[0][0],effTabl2[0].emoji[0][0],effTabl2[0].name,int((sumPower/effTabl2[0].power)*100))
                                                elif len(tablName[0]) > 1:
                                                    temp += "\n"
                                                    for cmpt in range(len(tablName[0])):
                                                        temp += tablName[0][cmpt]
                                                        if cmpt < len(tablName[0])-2:
                                                            temp += ", "
                                                        elif cmpt == len(tablName[0])-2:
                                                            temp += " et "
                                                    temp += "subissent l'effet {0} {1} pendant 3 tours".format(effTabl2[0].emoji[0][0],effTabl2[0].name,int((sumPower/effTabl2[0].power)*100))
                                            tempTurnMsg += temp
                                            logs += temp
                                            tempTurnMsg += "\n"
                                            logs += "\n"

                                    elif skillToUse.type == TYPE_HEAL:
                                        logs += "\n"
                                        if ennemi.hp > 0:
                                            elemPowBonus = 0
                                            if skillToUse.condition[:2] == [0,2]:
                                                for eff in actTurn.effect:
                                                    if eff.effect.id in [tablElemEff[skillToUse.condition[2]],tablElemEff[ELEMENT_UNIVERSALIS_PREMO]]:
                                                        elemPowBonus += eff.effect.power
                                            statUse = skillToUse.use
                                            if statUse == None:
                                                statUse = 0
                                            elif statUse == HARMONIE:
                                                temp = actTurn.allStats()
                                                for a in temp:
                                                    statUse = max(a,statUse)
                                            else:
                                                statUse = actTurn.allStats()[statUse]

                                            if skillToUse.id not in [dissi.id]:                  # Any normal healing skill
                                                if skillToUse.id == trans.id:
                                                    actionStats, entActStats = 0, actTurn.actionStats()
                                                    for cmpt in (0,1,2,3,4):
                                                        if entActStats[cmpt] > entActStats[actionStats]:
                                                            actionStats = cmpt
                                                else:
                                                    actionStats = ACT_HEAL
                                                if skillToUse.effect != [None] and skillToUse.effBeforePow:
                                                    ballerine = groupAddEffect(caster=actTurn, target=ennemi, area=skillToUse.area, effect=skillToUse.effect, skillIcon=skillToUse.emoji, actionStats=skillToUse.useActionStats, effPurcent = skillToUse.effPowerPurcent)
                                                    tempTurnMsg = tempTurnMsg + ballerine
                                                    logs += ballerine

                                                if skillToUse.id == uberCharge.id:
                                                    skillToUse = copy.deepcopy(skillToUse)
                                                    try:
                                                        if teamJaugeDict[actTurn.team][actTurn].effect.id == uberJauge.id:
                                                            uberValue = teamJaugeDict[actTurn.team][actTurn].value
                                                            teamJaugeDict[actTurn.team][actTurn].value = 0
                                                        else:
                                                            uberValue = 0
                                                    except KeyError:
                                                        uberValue = 0
                                                    skillToUse.power = skillToUse.power * (1+(uberValue/100))
                                                    if uberValue >= 100:
                                                        skillToUse.effect[0] = uberImune
                                                    else:
                                                        skillToUse.effect[0] = copy.deepcopy(defenseUp)
                                                        skillToUse.effect[0].power = 5 + (70/100*uberValue)

                                                    print("{0} a ??bercharge avec {1} jp, r??sultant en un soins avec une puissance de {2} et une r??duction de {3}% de d??g??ts".format(actTurn.name,uberValue,skillToUse.power,skillToUse.effect[0].power))

                                                for a in ennemi.cell.getEntityOnArea(area=skillToUse.area,team=actTurn.team,fromCell=actTurn.cell,wanted=ALLIES,directTarget=False):
                                                    funnyTempVarName, useless = actTurn.heal(a, skillToUse.emoji, skillToUse.use, int(skillToUse.power* (1+elemPowBonus/100)),danger=danger, mono = skillToUse.area == AREA_MONO, useActionStats = skillToUse.useActionStats)
                                                    tempTurnMsg += funnyTempVarName
                                                    logs += funnyTempVarName

                                                if skillToUse.effect != [None] and not(skillToUse.effBeforePow):
                                                    ballerine = groupAddEffect(caster=actTurn, target=ennemi, area=skillToUse.area, effect=skillToUse.effect, skillIcon=skillToUse.emoji, actionStats=skillToUse.useActionStats, effPurcent = skillToUse.effPowerPurcent)
                                                    tempTurnMsg += ballerine
                                                    logs += ballerine
                                            else:
                                                nbSummon = 0
                                                for ent in tablEntTeam[actTurn.team]:
                                                    if type(ent.char) == invoc and ent.id == actTurn.id:
                                                        nbSummon += 1
                                                        tempTurnMsg += "{0} est d??sinvoqu??\n".format(ent.char.name)
                                                        ent.hp = 0

                                                power = skillToUse.power*nbSummon
                                                
                                                for a in ennemi.cell.getEntityOnArea(area=skillToUse.area,fromCell=actTurn.cell,team=actTurn.team,wanted=ALLIES,directTarget=False):
                                                    funnyTempVarName, useless = actTurn.heal(a, skillToUse.emoji, skillToUse.use, power,danger=danger,mono=skillToUse.area == AREA_MONO)
                                                    tempTurnMsg += funnyTempVarName
                                                    logs += funnyTempVarName

                                    elif skillToUse.type == TYPE_SUMMON:
                                        if skillToUse.id not in [autoBombRush.id,killerWailUltimate.id,spamSkill3.id]:
                                            tablEntTeam, tablAliveInvoc, time, funnyTempVarName = actTurn.summon(findSummon(skillToUse.invocation),time,actTurn.cell.getCellForSummon(skillToUse.range,actTurn.team,findSummon(skillToUse.invocation),actTurn),tablEntTeam,tablAliveInvoc)
                                            tempTurnMsg += funnyTempVarName+"\n"
                                            logs += "\n"+funnyTempVarName
                                        else:
                                            toSummon, cmpt, limit = findSummon(skillToUse.invocation), 0, 1
                                            if skillToUse.id in [autoBombRush.id,spamSkill3.id]:
                                                limit = 3
                                            elif skillToUse.id == killerWailUltimate.id:
                                                limite = 5
                                            elif skillToUse.id == sumLightButterfly.id:
                                                for jaugeEnt, jaugeEff in teamJaugeDict[actTurn.team].items():
                                                    if jaugeEff.effect.id == jaugeButLight.id and jaugeEnt == actTurn:
                                                        limite = 1 + jaugeEff.value//40
                                                        jaugeEff.value = int(jaugeEff.value%40)

                                            while cmpt < [3,5][skillToUse.id==killerWailUltimate.id]:
                                                cellToSummon = actTurn.cell.getCellForSummon(skillToUse.range,actTurn.team,toSummon,actTurn)
                                                if cellToSummon != None:
                                                    tablEntTeam, tablAliveInvoc, time, funnyTempVarName = actTurn.summon(toSummon,time,cellToSummon,tablEntTeam,tablAliveInvoc,ignoreLimite=True)
                                                    tempTurnMsg += funnyTempVarName+"\n"
                                                    logs += "\n"+funnyTempVarName
                                                cmpt += 1

                                    elif skillToUse.type == TYPE_UNIQUE:
                                        if skillToUse.id == chaos.id:
                                            chaosTabl = effects[:]
                                            for a in chaosTabl[:]:
                                                if a in chaosProhib:
                                                    chaosTabl.remove(a)

                                            lenChaos = len(chaosTabl)-1
                                            for a in [0,1]:
                                                for b in tablEntTeam[a]:
                                                    if b.hp > 0:
                                                        effect = chaosTabl[random.randint(0,lenChaos)]
                                                        tempTurnMsg += add_effect(actTurn,b,effect)
                                                        
                                                        logs += "\n{0} gave the {1} effect at {2} for {3} turn(s)".format(actTurn.char.name,effect.name,b.char.name,effect.turnInit)
                                                        b.refreshEffects()

                                    elif skillToUse.type == TYPE_RESURECTION:
                                        if skillToUse.id == aliceRez.id:
                                            nbDown = 0
                                            for ent in tablEntTeam[actTurn.team]:
                                                if ent.status == STATUS_DEAD:
                                                    nbDown += 1

                                            if nbDown >= len(team1)//2:
                                                skillToUse = aliceRez2

                                        stat, resTabl = skillToUse.use, []

                                        for a in ennemi.cell.getEntityOnArea(area=skillToUse.area,fromCell=actTurn.cell,team=actTurn.team,wanted=ALLIES,dead=True,directTarget=False,ignoreInvoc=True):
                                            if stat not in [PURCENTAGE,None]:
                                                if stat != HARMONIE:
                                                    statUse = actTurn.allStats()[stat]
                                                else:
                                                    temp = actTurn.allStats()
                                                    for b in temp:
                                                        statUse = max(b,statUse)

                                                healPowa = min(
                                                    a.maxHp-a.hp, round(
                                                        skillToUse.power * (1+(statUse-max(actTurn.negativeHeal,actTurn.negativeShield,actTurn.negativeBoost))/100+(a.endurance/1000))
                                                        * actTurn.valueBoost(target=a,heal=True)
                                                        *actTurn.getElementalBonus(a,area=AREA_MONO,type=TYPE_HEAL)
                                                        *(1 + 0.006*actTurn.level)
                                                    )
                                                )

                                            elif stat == PURCENTAGE:
                                                healPowa = round(a.maxHP * skillToUse.power/100 * (100-a.healResist)/100)

                                            elif stat == None:
                                                healPowa = skillToUse.power

                                            funnyTempVarName = await actTurn.resurect(a,healPowa,skillToUse.emoji,danger=danger)
                                            tempTurnMsg += funnyTempVarName
                                            logs += funnyTempVarName
                                            resTabl.append(a)


                                        for eff in skillToUse.effect:
                                            if eff != None:
                                                ballerine = groupAddEffect(actTurn, actTurn, resTabl , eff, skillIcon=skillToUse.emoji)
                                                tempTurnMsg += ballerine
                                                logs += ballerine

                                    else: # Damage
                                        power, elemPowBonus = skillToUse.power, 0
                                        if skillToUse.ultimate and actTurn.char.aspiration == MAGE:
                                            power = int(power*1.2)

                                        if skillToUse.condition[:2] == [0,2]:
                                            for eff in actTurn.effect:
                                                if eff.effect.id in [tablElemEff[skillToUse.condition[2]],tablElemEff[ELEMENT_UNIVERSALIS_PREMO]]:
                                                    elemPowBonus += eff.effect.power
                                        if elemPowBonus > 0:
                                            power = power * (1+(elemPowBonus/100))

                                        if skillToUse.id == memClemCastSkill.id:
                                            effect = classes.effect("Bouclier vampirique","clemMemSkillShield",overhealth=(actTurn.hp-1)//2,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,emoji=uniqueEmoji('<:clemMemento2:902222663806775428>'),absolutShield=True)
                                            tempTurnMsg += "{0} : - {1} PV\n".format(actTurn.icon,actTurn.hp-1)
                                            actTurn.hp = 1
                                            actTurn.maxHp, actTurn.healResist = actTurn.maxHp//2,actTurn.healResist//2
                                            tempTurnMsg += add_effect(actTurn,actTurn,effect,ignoreEndurance=True)
                                            defIncur50 = incur[5]
                                            defIncur50.turnInit, defIncur50.unclearable = -1,True
                                            tempTurnMsg += add_effect(actTurn,actTurn,defIncur50)
                                        elif skillToUse.id == krysUlt.id:
                                            totalArmor = 0
                                            for eff in ennemi.effect:
                                                if eff.effect.type == TYPE_ARMOR and not(eff.effect.absolutShield):
                                                    reduc = eff.value // 2
                                                    eff.value -= reduc
                                                    totalArmor += reduc
                                                    tempTurnMsg += "{0} {1} ??? -{2}{3}{4} ({5})\n".format(actTurn.icon,skillToUse.emoji,reduc,eff.icon,ennemi.icon,skillToUse.name)

                                            if totalArmor > 0:
                                                effect = classes.effect("R??assembl??","krysShieldy",overhealth=totalArmor,type=TYPE_ARMOR,turnInit=99,trigger=TRIGGER_DAMAGE)
                                                tempTurnMsg += add_effect(actTurn,actTurn,effect,ignoreEndurance=True)
                                                actTurn.refreshEffects()
                                        elif skillToUse.id == finalTech.id:
                                            for jaugeEnt, jaugeEff in teamJaugeDict[actTurn.team].items():
                                                if jaugeEnt == actTurn and jaugeEff.effect.id == pasTech.id:
                                                    power = power * (1 + 150*jaugeEff.value/100/100)
                                                    jaugeEff.value = 0
                                        elif skillToUse.id in akikiSkillRageList:
                                            for cmpt in range(len(akikiSkillRageList)):
                                                if skillToUse.id == akikiSkillRageList[cmpt]:
                                                    power = int(power * (100+(akikiSkillRageBonus[cmpt]*((1-actTurn.hp/actTurn.maxHp)*100)))/100)
                                                    break
                                        elif skillToUse.id == theEnd.id:
                                            for eff in ennemi.effect:
                                                if eff.effect.id == reaperEff.id:
                                                    power = int(power*1.2)
                                                    break
                                        elif skillToUse.id == blueShell.id:
                                            tempTabl = tablEntTeam[int(not(actTurn.team))][:]
                                            for ent in tempTabl[:]:
                                                if ent.hp <= 0:
                                                    tempTabl.remove(ent)

                                            tempTabl.sort(key=lambda chocolatine: chocolatine.stats.damageDeal, reverse=True)
                                            if len(tempTabl) > 0:
                                                ennemi = tempTabl[0]
                                                ennemi.stats.sufferingFromSucess = True
                                        elif skillToUse.id == bleedingConvert.id:
                                            bleedingNumber = 0
                                            for eff in ennemi.effect:
                                                if eff.effect.id == bleeding.id:
                                                    bleedingNumber += eff.effect.power/bleeding.power * eff.turnLeft * 0.1
                                                    eff.decate(turn=99)
                                            power = power * (bleedingNumber+1)
                                        elif skillToUse.id == kikuSkill2.id and ennemi.status == STATUS_ALIVE:
                                            power = int(power*2)
                                        elif skillToUse.id == lizLB.id:
                                            nbCharm = 0
                                            for ent in tablEntTeam[not(actTurn.team)]:
                                                for eff in ent.effect:
                                                    if eff.effect.id == charming.id:
                                                        nbCharm += 1
                                                        eff.decate(turn=99)
                                                ent.refreshEffects()
                                            power += LIZLBPOWERGAINPERCHARM*nbCharm
                                        elif skillToUse.id in elemArrowId+elemRuneId:
                                            power += INCREASEPOWERPURCENTBYELEMEFF * useEffElem
                                        elif skillToUse.id in [klikliStrike.id,gwenyStrike.id]:
                                            hpConsumed = actTurn.hp - 1
                                            actTurn.stats.selfBurn += hpConsumed
                                            actTurn.hp = 1
                                            tempTurnMsg += "Les PVs de {0} sont r??duits ?? 1 !\n".format(actTurn.hp)
                                            power += skillToUse.power * 3 * (hpConsumed/actTurn.maxHp)
                                        if skillToUse.id == trans.id:
                                            actionStats, entActStats = 0, actTurn.actionStats()
                                            for cmpt in (0,1,2,3,4):
                                                if entActStats[cmpt] > entActStats[actionStats]:
                                                    skillToUse.useActionStats = cmpt

                                        else:
                                            actionStats = skillToUse.useActionStats

                                        if skillToUse.effect!=[None] and skillToUse.effBeforePow:
                                            tempTurnMsg += "\n"
                                            for a in skillToUse.effect:
                                                effect = findEffect(a)
                                                tempTurnMsg = tempTurnMsg[:-1] + add_effect(actTurn,ennemi,effect,effPowerPurcent=skillToUse.effPowerPurcent)

                                        cmpt = 0
                                        while cmpt < skillToUse.repetition and ennemi.hp > 0 and skillToUse.power > 0:
                                            funnyTempVarName, temp = actTurn.attack(target=ennemi,value=power,icon=skillToUse.emoji,area=skillToUse.area,sussess=skillToUse.sussess,use=skillToUse.use,onArmor=skillToUse.onArmor,useActionStats=actionStats,setAoEDamage=skillToUse.setAoEDamage,lifeSteal = skillToUse.lifeSteal,erosion = skillToUse.erosion, skillPercing = skillToUse.percing, execution=skillToUse.execution)
                                            tempTurnMsg += funnyTempVarName
                                            logs += "\n"+funnyTempVarName
                                            deathCount += temp
                                            cmpt += 1
                                            if cmpt < skillToUse.repetition:
                                                tempTurnMsg += "\n"

                                        if skillToUse.effect!=[None] and not(skillToUse.effBeforePow):
                                            tempTurnMsg += "\n"
                                            for a in skillToUse.effect:
                                                effect = findEffect(a)
                                                tempTurnMsg += add_effect(actTurn,ennemi,effect,effPowerPurcent=skillToUse.effPowerPurcent)
                                                logs += "\n{0} gave the {1} effect at {2} for {3} turn(s)".format(actTurn.char.name,effect.name,ennemi.char.name,effect.turnInit)

                                        if skillToUse.power > 0 and actTurn.specialVars["damageSlot"] != None:
                                            loose = int(actTurn.maxHp * (15/100))
                                            funnyTempVarName = "\n{0} : -{1} PV ({2})\n".format(actTurn.icon,loose,actTurn.specialVars["damageSlot"].effect.name)
                                            tempTurnMsg += funnyTempVarName
                                            logs + funnyTempVarName
                                            actTurn.hp -= loose
                                            actTurn.stats.selfBurn += loose
                                            if actTurn.hp <= 0:
                                                tempTurnMsg += actTurn.death(killer=actTurn)

                                            actTurn.refreshEffects()

                                        if actTurn.isNpc("Ailill") and skillToUse.id == "headnt":
                                            ennemi.stats.headnt = True
                                        if skillToUse.execution:
                                            ennemi.status = STATUS_TRUE_DEATH
                                # =================================================================
                                # Knockback
                                if skillToUse.knockback > 0:
                                    tablEnt = ennemi.cell.getEntityOnArea(area=skillToUse.area,team=actTurn.team,wanted=[ENEMIES,ALLIES][skillToUse.id == friendlyPush.id],directTarget=False,fromCell=actTurn.cell)
                                    tablEnt.sort(key=lambda ent: actTurn.cell.distance(ent.cell),reverse=True)
                                    for ent in tablEnt:
                                        temp = actTurn.knockback(ent,skillToUse.knockback)
                                        tempTurnMsg += temp
                                        logs += temp
                                
                                if skillToUse.pull > 0:
                                    tablEnt = ennemi.cell.getEntityOnArea(area=skillToUse.area,team=actTurn.team,wanted=ENEMIES,directTarget=False,fromCell=actTurn.cell)
                                    tablEnt.sort(key=lambda ent: actTurn.cell.distance(ent.cell))
                                    for ent in tablEnt:
                                        temp = actTurn.pull(ent,skillToUse.pull)
                                        tempTurnMsg += temp
                                        logs += temp

                                # JumpBack
                                if skillToUse.jumpBack > 0:
                                    temp = actTurn.jumpBack(skillToUse.jumpBack,ennemi.cell)
                                    tempTurnMsg += temp
                                    logs += temp

                                # Does the skill give a effect on the caster ?
                                if skillToUse.effectAroundCaster != None:
                                    if skillToUse.effectAroundCaster[0] == TYPE_HEAL:
                                        for a in actTurn.cell.getEntityOnArea(area=skillToUse.effectAroundCaster[1],fromCell=actTurn.cell,team=actTurn.team,wanted=ALLIES,directTarget=False):
                                            funnyTempVarName, useless = actTurn.heal(a, skillToUse.emoji, skillToUse.use, skillToUse.effectAroundCaster[2],danger=danger, mono = skillToUse.area == skillToUse.effectAroundCaster[1], useActionStats = skillToUse.useActionStats)
                                            tempTurnMsg += funnyTempVarName
                                            logs += funnyTempVarName
                                    elif skillToUse.effectAroundCaster[0] == TYPE_DAMAGE:
                                        funnyTempVarName, temp = actTurn.attack(target=ennemi,value=skillToUse.effectAroundCaster[2],icon=skillToUse.emoji,area=skillToUse.effectAroundCaster[1],sussess=skillToUse.sussess,use=skillToUse.use,onArmor=skillToUse.onArmor,useActionStats=actionStats,setAoEDamage=skillToUse.setAoEDamage,lifeSteal = skillToUse.lifeSteal)
                                        tempTurnMsg += funnyTempVarName
                                        logs += "\n"+funnyTempVarName
                                    elif type(skillToUse.effectAroundCaster[2]) == classes.effect:
                                        ballerine = groupAddEffect(actTurn, actTurn , skillToUse.effectAroundCaster[1], skillToUse.effectAroundCaster[2], skillToUse.emoji, effPurcent=[skillToUse.effPowerPurcent,liaLB.effPowerPurcent/5][skillToUse.id == trans.id and actTurn.isNpc("Lia")])
                                        tempTurnMsg += ballerine
                                        logs += ballerine

                                    elif skillToUse.effectAroundCaster[0] == TYPE_RESURECTION:
                                        stat = skillToUse.use

                                        for a in actTurn.cell.getEntityOnArea(area=skillToUse.effectAroundCaster[1],fromCell=actTurn.cell,team=actTurn.team,wanted=ALLIES,dead=True,directTarget=False):
                                            if stat != HARMONIE:
                                                statUse = actTurn.allStats()[stat]
                                            else:
                                                temp = actTurn.allStats()
                                                for b in temp:
                                                    statUse = max(b,statUse)

                                            healPowa = min(
                                                a.maxHp-a.hp, round(
                                                    skillToUse.effectAroundCaster[2] * (1+(statUse-max(actTurn.negativeHeal,actTurn.negativeShield,actTurn.negativeBoost))/100+(a.endurance/1000))
                                                    * actTurn.valueBoost(target=a,heal=True)
                                                    *actTurn.getElementalBonus(a,area=AREA_MONO,type=TYPE_HEAL)
                                                    *(1 + 0.006*actTurn.level)
                                                )
                                            )

                                            funnyTempVarName = await actTurn.resurect(a,healPowa,skillToUse.emoji,danger=danger)
                                            tempTurnMsg += funnyTempVarName
                                            logs += funnyTempVarName
                                            bigRaiseCount += 1

                                if skillToUse.effectOnSelf != None and not(skillToUse.effBeforePow):
                                    if not(findEffect(skillToUse.effectOnSelf).silent):
                                        if tempTurnMsg[-1] == "\n":
                                            tempTurnMsg += "\n"
                                        else:
                                            tempTurnMsg += "\n\n"
                                    eff = findEffect(skillToUse.effectOnSelf)
                                    if eff.replica != None:
                                        tempTurnMsg += add_effect(actTurn,actTurn,eff,setReplica=ennemi)
                                    else:
                                        tempTurnMsg += add_effect(actTurn,actTurn,eff,skillIcon = skillToUse.emoji,effPowerPurcent=skillToUse.selfEffPurcent)
                                    actTurn.refreshEffects()

                                if skillToUse.id in useElemEffId and useEffElem > 0:
                                    if skillToUse.id == useElemEffId[0]:
                                        burn = classes.effect("Br??lure","catFireEff",MAGIE,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_END_OF_TURN,power=int(skillToUse.power*0.33),turnInit=useEffElem,lvl=useEffElem)
                                        ballerine = groupAddEffect(actTurn, ennemi, skillToUse.area, burn, skillToUse.emoji)
                                        logs += ballerine
                                        tempTurnMsg += ballerine
                                    elif skillToUse.id == useElemEffId[5]:
                                        burn = classes.effect("Flamme sombre","catDarkEff",MAGIE,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_END_OF_TURN,area=skillToUse.area,power=int(skillToUse.power*0.5),turnInit=useEffElem,lvl=useEffElem)
                                        ballerine = groupAddEffect(actTurn, ennemi, AREA_MONO, burn, skillToUse.emoji)
                                        logs += ballerine
                                        tempTurnMsg += ballerine
                                    elif skillToUse.id == useElemEffId[4]:
                                        burn = classes.effect("R??g??n??ration de lumi??re","catLightEff",INTELLIGENCE,type=TYPE_INDIRECT_HEAL,trigger=TRIGGER_END_OF_TURN,power=int(skillToUse.effect[0].overhealth*0.2),turnInit=3)
                                        ballerine = groupAddEffect(actTurn, ennemi, skillToUse.area, burn, skillToUse.emoji, effPurcent = 100 * useEffElem)
                                        logs += ballerine
                                        tempTurnMsg += ballerine
                                    elif skillToUse.id == useElemEffId[7]:
                                        burn = classes.effect("Armure temporelle","catTimeEff",CHARISMA,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,overheath=int(skillToUse.power*0.2*useEffElem),turnInit=3)
                                        ballerine = groupAddEffect(actTurn, ennemi, skillToUse.area, burn, skillToUse.emoji)
                                        logs += ballerine
                                        tempTurnMsg += ballerine
                                    elif skillToUse.id == useElemEffId[2]:
                                        burn = classes.effect("Br??lure du vent","catAirEff",MAGIE,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_END_OF_TURN,power=int(skillToUse.power*0.40),turnInit=useEffElem,lvl=useEffElem)
                                        ballerine = groupAddEffect(actTurn, actTurn, AREA_MONO, burn, skillToUse.emoji)
                                        logs += ballerine
                                        tempTurnMsg += ballerine
                                    elif skillToUse.id == useElemEffId[1]:
                                        cmpt = 0
                                        while cmpt < useEffElem:
                                            ballerine, why = actTurn.attack(ennemi,int(skillToUse.power*0.15),skillToUse.emoji,AREA_MONO,skillToUse.sussess,use=MAGIE,skillPercing=skillToUse.percing)
                                            logs += ballerine
                                            tempTurnMsg += ballerine
                                            cmpt += 1
                                    elif skillToUse.id == useElemEffId[3]:
                                        ballerine, why = actTurn.attack(actTurn,int(skillToUse.power*0.2*useElemEffId),skillToUse.emoji,AREA_DONUT_2,skillToUse.sussess,use=MAGIE,skillPercing=skillToUse.percing)
                                        logs += ballerine
                                        tempTurnMsg += ballerine
                                    else:
                                        tablTargets = ennemi.cell.getEntityOnArea(area=skillToUse.area,fromCell=actTurn.cell,team=actTurn.team,wanted=ENEMIES,directTarget=False)
                                        cmpt = 0
                                        while cmpt < useEffElem and len(tablTargets) > 0:
                                            if len(tablTargets) > 1:
                                                target = tablTargets[random.randint(0,len(tablTargets)-1)]
                                            else:
                                                target = tablTargets[0]

                                            ballerine, why = actTurn.attack(target,int(skillToUse.power*0.30),skillToUse.emoji,AREA_CIRCLE_1,skillToUse.sussess,use=MAGIE,skillPercing=skillToUse.percing)
                                            logs += ballerine
                                            tempTurnMsg += "\n"+ballerine
                                            if target.hp <= 0:
                                                tablTargets.remove(target)
                                            cmpt += 1

                                # Blood cost
                                if actTurn.isNpc("Cl??mence pos.") or actTurn.isNpc("Alice Exalt??e"):
                                    for skillID, cost in clemBJcost.items():
                                        if skillToUse.id == skillID:
                                            actTurn.specialVars["clemBloodJauge"].value = max(0,actTurn.specialVars["clemBloodJauge"].value - cost)
                                            if actTurn.specialVars["clemBloodJauge"].value == 0:
                                                tempTurnMsg += "\nLa Jauge de Sang se brise !\n"
                                                if actTurn.isNpc("Cl??mence pos."):
                                                    tempTurnMsg += add_effect(actTurn, actTurn, clemStunEffect)
                                                    temp = copy.deepcopy(vulneTabl[3])
                                                    temp.turnInit = 3
                                                    tempTurnMsg += add_effect(actTurn, actTurn, temp)
                                                else:
                                                    tempTurnMsg += add_effect(actTurn, actTurn, aliceStunEffect)
                                                
                                                loose = actTurn.maxHp // 10
                                                tempTurnMsg += "{0} : -{1} PV\n".format(actTurn.icon,loose)
                                                actTurn.hp -= loose
                                                if actTurn.hp <= 0:
                                                    tempTurnMsg += actTurn.death(killer=actTurn)

                                                actTurn.refreshEffects()
                                            break

                                    if skillToUse.id == clemUltLauch.id:
                                        for ent in tablEntTeam[int(not(actTurn.team))]:
                                            if ent.isNpc("Alice Exalt??e"):
                                                for eff in ent.effect:
                                                    if eff.effect.id == aliceStunEffect.id:
                                                        tempTurnMsg += eff.decate(turn=99)

                                if skillToUse.maxHpCost > 0:
                                    diff = actTurn.maxHp - int(actTurn.maxHp * (1-(skillToUse.maxHpCost/100)))
                                    actTurn.maxHp = int(actTurn.maxHp * (1-(skillToUse.maxHpCost/100)))
                                    diff2 = min(0,actTurn.maxHp-actTurn.hp)
                                    actTurn.hp = min(actTurn.hp,actTurn.maxHp)
                                    tempTurnMsg += "\n{0} : -{1} PV max\n".format(actTurn.icon,diff)
                                    actTurn.stats.selfBurn += abs(diff2)

                                if skillToUse.hpCost > 0:
                                    diff = actTurn.hp - int(actTurn.hp * (1-(skillToUse.hpCost/100)))
                                    actTurn.hp -= diff
                                    tempTurnMsg += "\n{0} : -{1} PV\n".format(actTurn.icon,diff)
                                    actTurn.stats.selfBurn += diff

                                    if actTurn.hp <= 0:
                                        tempTurnMsg += actTurn.death(killer=actTurn)

                                if skillToUse.replay:
                                    replay = skillToUse.replay

                                if skillToUse.condition[:2] == [0,2] and random.randint(0,99) < mEP:
                                    for eff in actTurn.effect:
                                        if eff.effect.id == matriseElemEff.id:
                                            ballerine = add_effect(actTurn,actTurn,matriseElemEff.callOnTrigger,skillIcon=matriseElemEff.emoji[0][0])
                                            actTurn.refreshEffects()
                                            tempTurnMsg += ballerine
                                            logs += ballerine

                                elif skillToUse.condition[:2] == [0,2] and skillToUse.condition[2] == ELEMENT_LIGHT:
                                    for jaugeEnt, jaugeEff in teamJaugeDict[actTurn.team].items():
                                        if jaugeEff.effect.id == jaugeButLight.id and jaugeEnt == actTurn:
                                            jaugeEff.value = min(jaugeEff.value+10,100)
                                # ============================= Interactions =============================
                                if skillToUse.id == strengthOfWill.id and actTurn.isNpc("F??licit??") and dictIsNpcVar["Cl??mence"]:       # F??li / Clem
                                    tempTurnMsg += "<:felicite:909048027644317706> : *\"Alors Cl??mence :D ? Combien combien ?\"*\n<:clemence:908902579554111549> : *\"Hum... {0} sur 20\"*\n<:felicite:909048027644317706> : :D\n".format(random.randint(15,22))

                                if skillToUse.ultimate and skillToUse.effect != [None] and skillToUse.type == TYPE_BOOST and dictIsNpcVar["Alice"] and not(actTurn.isNpc("Alice")):               # Alice
                                    alice = None
                                    for team in [0,1]:
                                        for ent in tablEntTeam[team]:
                                            if ent.isNpc("Alice"):
                                                alice = ent
                                                break
                                        if alice != None:
                                            break

                                    damage = indirectDmgCalculator(alice, actTurn, [15,25][skillToUse.id == onstage.id], CHARISMA, 100, area=AREA_MONO)
                                    murcialago = "\n"+alice.indirectAttack(target=actTurn,value=damage,icon="",ignoreImmunity=True,name='Coup bas',hideAttacker=True)
                                    tempTurnMsg += murcialago
                                    logs += "\nAlice wasn't verry happy about that\n"+murcialago
                                    if actTurn.isNpc("Amary") and dictIsNpcVar["Lohica"]:
                                        lohica = None
                                        for team in [0,1]:
                                            for ent in tablEntTeam[team]:
                                                if ent.isNpc("Lohica"):
                                                    lohica = ent
                                                    break
                                            if lohica != None:
                                                break

                                        damage = indirectDmgCalculator(lohica, alice, 15, MAGIE, 100, area=AREA_MONO)
                                        murcialago = "\n"+lohica.indirectAttack(target=lohica,value=damage,icon="",ignoreImmunity=True,name='Coup bas',hideAttacker=True)
                                        tempTurnMsg += murcialago
                                        logs += "\nLohica wasn't verry happy about that\n"+murcialago

                                if skillToUse.effectOnSelf != None and findEffect(skillToUse.effectOnSelf).replica != None and skillToUse.power == 0 and skillToUse.effect == [None]:
                                    tempTurnMsg += "{0} charge la comp??tence __{1}__\n".format(actTurn.name,skillToUse.name)

                                if skillToUse.id == unHolly.id and (ennemi.isNpc("Liu") or ennemi.isNpc("Lia") or ennemi.isNpc("Liz") or ennemi.isNpc("Lio") or ennemi.isNpc("Kitsune")):
                                    funnyMsg, funnyMsgTabl, tablKitsunes, tablEffectGiven = "", ["Oh tu veux jouer ?? ??a ?","Oh ^^ Mon tour maintenant !","C'est mignon x) Mais tu va apprendre ?? un vieux singe ?? faire la grimace","Tu l'as cherch??...","^^ Laisse moi te montrer comment il faut faire"], [ennemi.isNpc("Liu"),ennemi.isNpc("Lia"),ennemi.isNpc("Liz"),ennemi.isNpc("Lio"),ennemi.isNpc("Kitsune")], [3,5,5,3,10]
                                    for cmpt in range(5):
                                        if tablKitsunes[cmpt]:
                                            tempTurnMsg += "\n{0} : *\"{1}\"*".format(ennemi.icon,funnyMsgTabl[cmpt])
                                            for cmpt2 in range(tablEffectGiven[cmpt]):
                                                add_effect(ennemi,actTurn,charming)
                                            tempTurnMsg += "\n{0} ??? {1} +{2} x{3}".format(ennemi.icon,actTurn.icon,charming.emoji[0][1],tablEffectGiven[cmpt])
                                            break

                                elif skillToUse.id in tablRosesSkillsId and skillToUse.effectOnSelf == None: # Final Floral On Self
                                    for skilly in actTurn.char.skills:
                                        if type(skilly) == classes.skill and skilly.id == finalFloral.id:
                                            roseCount = 0
                                            for eff in actTurn.effect:
                                                if eff.effect.id in tablRosesId:
                                                    roseCount += 1

                                            if roseCount < 3:
                                                if skillToUse.id in [onstage.id,floraisonFinale.id]:
                                                    roseToAdd = rosePink
                                                elif skillToUse.id in [crimsomLotus.id]:
                                                    roseToAdd = roseYellow
                                                elif skillToUse.id in [corGraFinal.id,petalisation.id]:
                                                    roseToAdd = roseDarkBlu
                                                elif skillToUse.id in [aliceDanceFinal.id,danceFas.id]:
                                                    roseToAdd = roseRed
                                                
                                                tempMsg = groupAddEffect(actTurn,actTurn,AREA_MONO,roseToAdd,skillToUse.emoji)
                                                tempTurnMsg += tempMsg
                                                logs += tempMsg
                                                roseCount += 1
                                                if roseCount == 3:
                                                    tempMsg = add_effect(actTurn,actTurn,finFloCast,setReplica=actTurn,skillIcon=finFloEff.emoji[0][actTurn.team])
                                                    tempTurnMsg += tempMsg
                                                    logs += tempMsg
                                            break

                                elif skillToUse.id in finFloOtherSkillsId: # Final Floral on others
                                    for ent in tablEntTeam[actTurn.team]:
                                        rosesNb, haveFinFlo = 0, False
                                        for eff in ent.effect:
                                            if eff.effect.id == finFloEff.id:
                                                haveFinFlo = True
                                            elif eff.effect.id in tablRosesId:
                                                rosesNb += 1
                                        
                                        if haveFinFlo and rosesNb <= 2:
                                            if skillToUse.id in [finalTech.id,croissance.id]:
                                                roseToAdd = roseBlue
                                            elif skillToUse.id in [valse.id,roseeHeal.id]:
                                                roseToAdd = roseGreen
                                            tempMsg = groupAddEffect(ent,ent,AREA_MONO,roseToAdd,skillToUse.emoji)
                                            tempTurnMsg += tempMsg
                                            logs += tempMsg

                                            rosesNb += 1
                                            if rosesNb == 3:
                                                tempMsg = add_effect(ent,ent,finFloCast,setReplica=ent,skillIcon=finFloEff.emoji[0][ent.team])
                                                tempTurnMsg += tempMsg
                                                logs += tempMsg

                                elif skillToUse.id in [astrodyn.id,cercleCon.id]:
                                    LBBars[actTurn.team][1] = min(LBBars[actTurn.team][1]+3,LBBars[actTurn.team][0]*3)
                                
                                elif skillToUse.id in [plumeCel.id,hinaUlt.id,plumePers.id,pousAviaire.id]:
                                    for skilly in actTurn.char.skills:
                                        skillo = findSkill(skilly)
                                        if skillo != None and skillo.id == plumRem.id:
                                            tablSuccess, tablEnt = [], ennemi.cell.getEntityOnArea(area=skillToUse.area,team=actTurn.team,wanted=ENEMIES,ignoreInvoc = True, directTarget=False,fromCell=actTurn.cell)
                                            for ent in tablEnt:
                                                if random.randint(0,99) < skillo.power:
                                                    tablSuccess.append(ent)
                                            if len(tablSuccess) > 0:
                                                temp = groupAddEffect(actTurn, ennemi, tablSuccess, [plumRemEff], skillIcon=skillo.emoji)
                                                tempTurnMsg += "\n"+temp
                                                logs += temp
                                            break

                                try:                # Big raise
                                    if actTurn.stats.allieResurected - allyRea >= 3:
                                        if actTurn.char.says.bigRaise != None:
                                            tempTurnMsg += "\n{0} : *\"{1}\"*".format(actTurn.icon,actTurn.char.says.bigRaise.format(skill=skillToUse.name))
                                        tablReact = []
                                        for team in [0,1]:
                                            for ent in tablEntTeam[team]:
                                                if ent.hp > 0 and ent != actTurn and [ent.char.says.reactBigRaiseEnnemy,ent.char.says.reactBigRaiseAllie][ent.team == actTurn.team] != None and (ent not in ressurected[ent.team]):
                                                    tablReact.append([ent.icon,[ent.char.says.reactBigRaiseEnnemy,ent.char.says.reactBigRaiseAllie][ent.team == actTurn.team]])

                                        if len(tablReact) != 0:
                                            if len(tablReact) == 1:
                                                rand = 0
                                            else:
                                                rand = random.randint(0,len(tablReact)-1)
                                            tempTurnMsg += "\n{0} : *\"{1}\"*".format(tablReact[rand][0],tablReact[rand][1].format(caster=actTurn.char.name,skill=skillToUse.name))
                                except:
                                    tempTurnMsg += "\n__Error with the BigRaisesReaction.__ See logs for more informations"
                                    logs += "\n"+format_exc()

                                try:                # LB React
                                    if skillToUse.id == trans.id:
                                        tablReact = []
                                        for team in [0,1]:
                                            for ent in tablEntTeam[team]:
                                                if ent.hp > 0 and ent != actTurn and [ent.char.says.reactEnemyLb ,ent.char.says.reactAllyLb][ent.team == actTurn.team] != None:
                                                    tablReact.append([ent.icon,[ent.char.says.reactEnemyLb ,ent.char.says.reactAllyLb][ent.team == actTurn.team]])

                                        if len(tablReact) != 0:
                                            if len(tablReact) == 1:
                                                rand = 0
                                            else:
                                                rand = random.randint(0,len(tablReact)-1)
                                            tempTurnMsg += "\n{0} : *\"{1}\"*".format(tablReact[rand][0],tablReact[rand][1].format(caster=actTurn.char.name,skill=skillToUse.name))
                                except:
                                    tempTurnMsg += "\n__Error with the LBs reactions.__ See logs for more informations"
                                    logs += "\n"+format_exc()

                            if actTurn.stats.fullskip and optionChoice != OPTION_SKIP:
                                actTurn.stats.fullskip = False

                            if actTurn.isNpc("Luna pr??.") and optionChoice == OPTION_SKILL and skillToUse.id in [lunaSpe.id,lunaSpeCast.id]:
                                replay = False

                            if not(replay or (optionChoice == OPTION_MOVE and not(allReadyMove))):
                                break
                            else:
                                replay, isCasting = False, False
                                if optionChoice != OPTION_MOVE:
                                    for eff in actTurn.effect:
                                        if eff.effect.replica != None:
                                            isCasting = True
                                            break
                                    
                                tempTurnMsg += lunaUsedQuickFight
                                if optionChoice == OPTION_MOVE and not(allReadyMove):
                                    allReadyMove = True
                                    logs += "\n"

                                if not(auto) and not(actTurn.auto):   # Sending the Turn message
                                    if len(tempTurnMsg) > 4096:
                                        tempTurnMsg = unemoji(tempTurnMsg)
                                        if len(tempTurnMsg) > 4096:
                                            tempTurnMsg = "OVERLOAD"
                                    await turnMsg.edit(embed = discord.Embed(title=f"__Tour {tour}__",description=tempTurnMsg,color = actTurn.char.color))
                                    if not(isCasting):
                                        await asyncio.sleep(3)
                                    else:
                                        await asyncio.sleep(1)
                    
                                for team in [0,1]:                      # Does a team is dead ?
                                    for ent in tablEntTeam[team]:
                                        if ent.hp > 0 and type(ent.char) != invoc:
                                            everyoneDead[team] = False
                                            break

                                if everyoneDead[0] or everyoneDead[1]:  # If Yes, ending the fight
                                    fight = False
                                    break
                    # ==========================================
                    # Else, the entity is stun
                    else:                                   # The entity is, in fact, stun
                        temp = ""
                        if tablEntTeam[1][0].isNpc("Luna pr??.") or tablEntTeam[1][0].isNpc("Luna ex."):
                            for eff in actTurn.effect:
                                if eff.effect.id == lunaInfiniteDarknessStun.id:
                                    temp = actTurn.quickEvent(stat=ENDURANCE, required=int(250*(1+0.3*int(actTurn.char.element != ELEMENT_LIGHT))), danger=danger, effIfFail=lunaVulne, fromEnt=tablEntTeam[1][0])[0]
                                    break
                            if temp == "":
                                temp = f"\n{actTurn.char.name} est ??tourdi{actTurn.accord()} !\n"
                        else:
                            temp = f"\n{actTurn.char.name} est ??tourdi{actTurn.accord()} !\n"
                        tempTurnMsg += temp
                        logs += "{0} is stun\n".format(actTurn.name)
                        optionChoice = OPTION_SKIP

                    funnyTempVarName, ressurected = "\n__Fin du tour__\n"+actTurn.endOfTurn(danger), [[],[]]
                    logs += funnyTempVarName
                    tempTurnMsg += funnyTempVarName
                    timeNow = (datetime.now() - nowStartOfTurn)/timedelta(microseconds=1000)
                    logs += "Turn duration : {0} ms{1}\n ----------".format(timeNow,[" (Manual fighter)",""][int(actTurn.auto)])
                    if timeNow > 500 and actTurn.auto:
                        longTurn = True
                        longTurnNumber.append({"turn":tour,"ent":actTurn.char.name,"duration":timeNow})

                    if not(auto):   # Sending the Turn message
                        if len(tempTurnMsg) > 4096:
                            tempTurnMsg = unemoji(tempTurnMsg)
                            if len(tempTurnMsg) > 4096:
                                tempTurnMsg = "OVERLOAD"

                        nbTry = 0
                        while 1:
                            emby = embed = discord.Embed(title=f"__Tour {tour}__",description=tempTurnMsg,color = actTurn.char.color)
                            if footerText != "":
                                emby.set_footer(text=footerText,icon_url=ctx.author.avatar_url)
                            try:
                                if optionChoice == OPTION_SKILL and skillToUse.url != None:
                                    await turnMsg.edit(embed = emby.set_image(url=skillToUse.url))
                                else:
                                    await turnMsg.edit(embed = emby)
                                break
                            except SocketError as e:
                                if e.errno not in [errno.ECONNRESET,503]:
                                    raise
                                else:
                                    if nbTry < 5:
                                        await asyncio.sleep(1)
                                        nbTry += 1
                                        errorNb += 1
                                        logs += "\nConnexion error... retrying..."
                                    else:
                                        logs += "\nConnexion lost"
                                        raise

                        if type(actTurn.char) != invoc:
                            await asyncio.sleep(2-([0,0.5][int(bigMap or not(allAuto))])+(min(len(tempTurnMsg),2500)/2500*5))
                        else:
                            await asyncio.sleep(1+(min(len(tempTurnMsg),3500)/3500*5))

                    potgValue = (None,0)

                    for team in (0,1):
                        for ent in tablEntTeam[team]:
                            tempPotgValue = (ent.stats.damageDeal-potgDamages[team][ent.id])*0.7+(ent.stats.ennemiKill-potgKills[team][ent.id])*ent.char.level*10+(ent.stats.heals-potgHeal[team][ent.id])*0.6+(ent.stats.allieResurected-potgRaises[team][ent.id])*ent.char.level*15+ent.stats.armoredDamage-potgArmored[team][ent.id]+500*int(optionChoice==OPTION_SKILL and skillToUse.id == "lb")-1000*int(type(actTurn.char)==octarien)
                            if tempPotgValue > potgValue[1]:
                                potgValue = (ent,tempPotgValue)

                    if potgValue[1] > playOfTheGame[0]:
                        if optionChoice == OPTION_SKILL and skillToUse.url != None:
                            playOfTheGame = [potgValue[1],potgValue[0],discord.Embed(title=f"__Action du combat\nTour {tour}__",description=tempTurnMsg,color = potgValue[0].char.color).set_image(url=skillToUse.url)]
                        else:
                            playOfTheGame = [potgValue[1],potgValue[0],discord.Embed(title=f"__Action du combat\nTour {tour}__",description=tempTurnMsg,color = potgValue[0].char.color)]
                        
                        if playOfTheGame[2].__len__() > 4000:
                            playOfTheGame[2] = discord.Embed(title=f"__Action du combat\nTour {tour}__",description=unemoji(tempTurnMsg),color = potgValue[0].char.color)
                            if playOfTheGame[2].__len__() > 4000:
                                tempVeryCut, tempLine = "", ""
                                for letter in tempTurnMsg:
                                    if letter == "\n":
                                        if "\"" not in tempLine and "rejoue son tour" not in tempLine:
                                            tempVeryCut += tempLine + "\n"
                                        tempLine = ""
                                    else:
                                        tempLine += letter
                                if "\"" not in tempLine:
                                    tempVeryCut += tempLine
                                playOfTheGame[2] = discord.Embed(title=f"__Action du combat\nTour {tour}__",description=tempVeryCut,color = potgValue[0].char.color)
                                if playOfTheGame[2].__len__() > 4000 :
                                    tempVeryCut = '(...)\n'+tempVeryCut[-4000:]
                                    playOfTheGame[2] = discord.Embed(title=f"__Action du combat\nTour {tour}__",description=tempVeryCut,color = potgValue[0].char.color)

                # =========================================

                # End of the turn - timeline stuff ------------------------------------------------------------------
                tablEntTeam,tablAliveInvoc = time.endOfTurn(tablEntTeam,tablAliveInvoc)

                for team in [0,1]:                      # Does a team is dead ?
                    for ent in tablEntTeam[team]:
                        if ent.hp > 0 and type(ent.char) != invoc:
                            everyoneDead[team] = False
                            break

                if everyoneDead[0] or everyoneDead[1]:  # If Yes, ending the fight
                    fight = False

            # End of the fight ============================
            logs += "\n\n================= End of the fight ================="
        except:
            for team in listImplicadTeams:
                teamWinDB.changeFighting(team,0)
            logs += "\n"+format_exc()
            date = datetime.now()+horaire
            date = date.strftime("%H%M")
            fich = open("./data/fightLogs/ERROR_{0}_{1}.txt".format(ctx.author.name,date),"w",encoding='utf-8')
            if not(isLenapy):
                try:
                    fich.write(unemoji(logs))
                except:
                    print_exc()

            else:
                fich.write(unemoji(logs))
            fich.close()
            opened = open("./data/fightLogs/ERROR_{0}_{1}.txt".format(ctx.author.name,date),"rb")
            await asyncio.sleep(1)
            desc = format_exc()

            desc += "\n__Variables :__\n__ActTurn :__ "
            try:
                desc += actTurn.char.name
            except:
                desc += ":x:"
            desc += "\n__SkillToUse :__ "
            try:
                desc += skillToUse.name
            except:
                desc += ":x:"
            desc += "\n__Ennemi :__ "
            try:
                desc += ennemi.char.name
            except:
                desc += ":x:"            

            try:
                await ctx.send(content="{0} : Une erreur est survenue".format(ctx.author.mention),file=discord.File(fp=opened),embed=discord.Embed(title=["Descriptif de l'erreur","Une erreur de communication prolong??e est survenue"]["aiohttp.client_exceptions.ClientOSError: [Errno 104] Connection reset by peer" in logs],description=desc))
            except:
                await ctx.channel.send(file=discord.File(fp=opened),embed=discord.Embed(title=["Une erreur est survenue durant le combat","Une erreur de communication prolong??e est survenue"]["aiohttp.client_exceptions.ClientOSError: [Errno 104] Connection reset by peer" in logs],description=desc))
            opened.close()

            if isLenapy:
                chan = await bot.fetch_channel(808394788126064680)
                opened = open("./data/fightLogs/ERROR_{0}_{1}.txt".format(ctx.author.name,date),"rb")
                await asyncio.sleep(1)
                await chan.send("Une erreur est survenue durant le combat",file=discord.File(fp=opened))
                opened.close()
            haveError = True
        # ===============================================================================================
        #                                       Post Fight Things
        # ===============================================================================================
        if not(haveError):
            print(ctx.author.name + " a fini son combat")

            for a in range(0,len(tablEntTeam[0])):      # Reload the char files (in case of changes)
                if type(tablEntTeam[0][a].char) == char:
                    tablEntTeam[0][a].char = loadCharFile(absPath + "/userProfile/" + str(tablEntTeam[0][a].char.owner) + ".prof")

            for a in range(0,len(tablEntTeam[1])):      # Reload the char files (in case of changes)
                if type(tablEntTeam[1][a].char) == char:
                    tablEntTeam[1][a].char = loadCharFile(absPath + "/userProfile/" + str(tablEntTeam[1][a].char.owner) + ".prof")

            if not(everyoneDead[1] and everyoneDead[0]):        # The winning team. 0 -> Blue, 1 -> Red
                winners, nullMatch = int(not(everyoneDead[1])), False
            else:
                winners, nullMatch = 1, True

            if not(octogone and team2[0].isNpc('Lena') and len(team2) == 1 and not(winners)):               # None Special fights
                for z in (0,1):
                    for a in tablEntTeam[z]:
                        if type(a.char) == invoc:
                            a.hp = 0

                tablEntTeam,tablAliveInvoc = time.endOfTurn(tablEntTeam,tablAliveInvoc) 

                temp = tablEntTeam[0][:]+tablEntTeam[1][:]

                dptClass = sorted(temp,key=lambda student: student.stats.damageDeal,reverse=True)
                for a in dptClass[:]:
                    if a.stats.damageDeal < 1:
                        dptClass.remove(a)
                healClass = sorted(temp,key=lambda student: student.stats.heals,reverse=True)
                for a in healClass[:]:
                    if a.stats.heals < 1:
                        healClass.remove(a)
                shieldClass = sorted(temp,key=lambda student: student.stats.armoredDamage,reverse=True)
                for a in shieldClass[:]:
                    if a.stats.shieldGived < 1:
                        shieldClass.remove(a)
                suppClass = sorted(temp,key=lambda student: student.stats.damageBoosted + student.stats.damageDogded,reverse=True)
                for a in suppClass[:]:
                    if a.stats.damageBoosted + a.stats.damageDogded < 1:
                        suppClass.remove(a)

                listClassement = [dptClass,healClass,shieldClass,suppClass]

                if not(octogone):           # Add result to streak
                    teamWinDB.addResultToStreak(mainUser,not(everyoneDead[0]))
                if isLenapy and not(octogone):
                    teamWinDB.refreshFightCooldown(mainUser.team,auto,fromTime=now)

                tablSays = []
                temp= ["",""]
                for a in [0,1]:             # Result msg character showoff
                    for b in tablEntTeam[a]:
                        if type(b.char) != char:
                            icon = b.char.icon
                        else:
                            icon = await getUserIcon(bot,b.char)

                        raised = ""
                        if b.status == STATUS_RESURECTED and b.raiser != None:
                            raised = " ({1}{0})".format(b.raiser,['<:rezB:907289785620631603>','<:rezR:907289804188819526>'][b.team])
                        elif b.status == STATUS_TRUE_DEATH and b.raiser != None:
                            raised = " ({0})".format(['<:diedTwiceB:907289950301601843>','<:diedTwiceR:907289935663485029>'][b.team])

                        temp[a] += f"{b.icon} {b.char.name}{b.getMedals(listClassement)}{raised}\n"
                        if type(b.char) == octarien and b.char.oneVAll:
                            if a == 1 and winners and b.char.says.redWinAlive != None and b.hp > 0:
                                for cmpt in (0,1,2,3,4,5):
                                    tablSays += ["{0} : *\"{1}\"*".format(icon,b.char.says.redWinAlive)]

                            elif a == 1 and not(winners) and b.char.says.redLoose != None:
                                for cmpt in (0,1,2,3):
                                    tablSays += ["{0} : *\"{1}\"*".format(icon,b.char.says.redLoose)]

                        else:
                            if a == 0 and not(winners) and b.char.says.blueWinAlive != None and b.hp > 0:
                                for cmpt in (0,1):
                                    tablSays += ["{0} : *\"{1}\"*".format(icon,b.char.says.blueWinAlive)]
                            elif a == 0 and not(winners) and b.char.says.blueWinDead != None and b.hp <= 0:
                                tablSays += ["{0} : *\"{1}\"*".format(icon,b.char.says.blueWinDead)]
                            elif a == 0 and winners and b.char.says.blueLoose != None:
                                tablSays += ["{0} : *\"{1}\"*".format(icon,b.char.says.blueLoose)]
                            elif a == 1 and winners and b.char.says.redWinAlive != None and b.hp > 0:
                                for cmpt in (0,1):
                                    tablSays += ["{0} : *\"{1}\"*".format(icon,b.char.says.redWinAlive)]
                            elif a == 1 and winners and b.char.says.redWinDead != None and b.hp <= 0:
                                tablSays += ["{0} : *\"{1}\"*".format(icon,b.char.says.redWinDead)]
                            elif a == 1 and not(winners) and b.char.says.redLoose != None:
                                tablSays += ["{0} : *\"{1}\"*".format(icon,b.char.says.redLoose)]

                    if len(temp[a]) > 1024:
                        tabl = ["<:topDpt:884337213670838282>","<:secondDPT:884337233241448478>","<:thirdDPT:884337256905732107>","<:topHealer:884337335410491394>","<:secondHealer:884337355262160937>","<:thirdHealer:884337368407093278>","<:topArmor:884337281547272263>","<:secondArmor:884337300975276073>","<:trdArmor:911071978163675156>","<:topSupp:911071783787065375>","<:sndSupp:911071803424788580>","<:trdSupp:911071819388313630>","<:rezB:907289785620631603>","<:rezR:907289804188819526>","<:diedTwiceB:907289950301601843>","<:diedTwiceR:907289935663485029>"]
                        tablName = ["1stDpt","2ndDPT","3rdDPT","1stHealer","2ndHealer","3rdHealer","1stArmor","2ndArmor","3rdArmor","1stSupp","2ndSupp","3rdSupp","R??a: ","R??a: ","D.D","D.D"]
                        for cmpt in range(len(tabl)):
                            temp[a] = temp[a].replace(tabl[cmpt],tablName[cmpt])
                    
                    if len(temp[a]) > 1024:
                        temp[a] = ""
                        for b in tablEntTeam[a]:
                            if type(b.char) != char:
                                icon = b.char.icon
                            else:
                                icon = await getUserIcon(bot,b.char)
                            temp[a] += f"{b.icon} {b.char.name}\n"

                say = ""
                if len(tablSays) > 1:
                    say = "\n\n{0}".format(tablSays[random.randint(0,len(tablSays)-1)])
                elif len(tablSays) == 1:
                    say = "\n\n{0}".format(tablSays[0])
        
                duree = datetime.now()
                nowTemp = duree - now
                nowTemp = str(nowTemp.seconds//60) + ":" + str(nowTemp.seconds%60)

                if not(octogone):       # Add the "next fight" field
                    nextFigth = now + timedelta(hours=1+(2*auto)) + horaire
                    nextFightMsg = "\n__Prochain combat {0}__ : {1}".format(["normal","rapide"][auto],nextFigth.strftime("%Hh%M"))
                else:
                    nextFightMsg = ""

                if not(nullMatch):
                    color = [[0x2996E5,0x00107D][danger<100],red][winners]
                else:
                    color = 0x818181

                resultEmbed = discord.Embed(title = "__R??sultats du combat :__",color = color,description="__Danger :__ {0}\n__Nombre de tours :__ {1}\n__Dur??e :__ {2}{4}{3}".format(danger,tour,nowTemp,say,nextFightMsg))
                resultEmbed.add_field(name="<:empty:866459463568850954>\n__Vainqueurs :__",value=temp[winners],inline=True)
                resultEmbed.add_field(name="<:empty:866459463568850954>\nPerdants :",value=temp[not(winners)],inline=True)
                if footerText != "":
                    resultEmbed.set_footer(text=footerText,icon_url=ctx.author.avatar_url)

                if longTurn:
                    resultEmbed.set_footer(text="{0} tour{1} anormalement long{1} {2} ??t?? d??tect??{1} durant le combat. Un rapport va ??tre envoy??".format(len(longTurnNumber),["",'s'][int(len(longTurnNumber) > 1)],["a","ont"][int(len(longTurnNumber) > 1)]))

                endOfFightStats = copy.deepcopy(tablEntTeam)
                if procurFight:
                    team1 = []
                    user = loadCharFile("./userProfile/{0}.prof".format(ctx.author_id))
                    if user.team != 0:
                        for a in userTeamDb.getTeamMember(user.team):
                            team1 += [loadCharFile(absPath + "/userProfile/{0}.prof".format(a))]
                    else:
                        team1 = [user]

                    tablEntTeam[0], cmpt = [], 0
                    for user in team1:
                        tablEntTeam[0].append(entity(cmpt,user,0,danger=danger,dictInteraction=dictIsNpcVar))
                        cmpt+=1

                # Gain rolls and defenitions -------------------------------------------------
                if not(octogone):
                    gainExp, gainCoins, allOcta, gainMsg, listLvlUp = tour,tour*20,True,"", []
                    # Base Exp Calculation
                    for a in tablEntTeam[1]:
                        if type(a.char) == octarien:
                            if a.hp <= 0:
                                gainExp += a.char.exp
                            elif a.status == STATUS_RESURECTED:
                                gainExp += int(a.char.exp/2)
                        elif type(a.char) == tmpAllie:
                            if a.hp <= 0:
                                gainExp += 8
                            elif a.status == STATUS_RESURECTED:
                                gainExp += 4
                        else:
                            allOcta = False

                    truc = 0
                    logs += "\n\n"

                    # Win streak little exp boost
                    try:
                        if winStreak > 7:
                            truc = (winStreak-7) * 0.05
                    except:
                        pass

                    # None complete team exp boost
                    if not(procurFight):
                        multi = max(1,8/len(team1)+truc)
                    else:
                        multi = 1

                    gainInit = str(gainExp)
                    gainExp = int(gainExp*multi)
                    if winners:
                        gainCoins = gainCoins//2

                    logs += "Gains exp : {0} ({1} * {2})\n".format(gainExp,gainInit,multi)
                    gainMsg = f"Pi??ces : {gainCoins}"

                    maxLevel = -1
                    for players in tablEntTeam[0]:
                        maxLevel = max(players.char.level, maxLevel)

                    for a in tablEntTeam[0]: #Attribution de l'exp et loot
                        tempLevel = tablEntTeam[0][:]
                        tempLevel.sort(key=lambda sorting : sorting.char.level, reverse=True)
                        maxLevlDiff = tempLevel[0].char.level - tempLevel[len(tempLevel)-1].char.level
                        if type(a.char) == char and a.char.team == mainUser.team:
                            path = absPath + "/userProfile/" + str(a.char.owner) + ".prof"

                            veryLate = 1 + (int(maxLevel-a.char.level > 10 and winners) * 0.5)
                            if a.char.level < 55:
                                baseGain = gainExp+(a.medals[0]*3)+(a.medals[1]*2)+(a.medals[2]*1)+int((maxLevel-a.char.level)/2)
                            else:
                                baseGain = 0
                            effectiveExpGain = int(baseGain*(1+0.02*(min(10,maxLevel-a.char.level)))*veryLate*[1,1.5][a.char.stars > 0 and a.char.level <=30] * (1+(maxLevlDiff <= 5 * 0.2)+(a.auto*0.1)))
                            temp = (a.char.level, a.char.stars)
                            a.char = await addExpUser(bot,path,ctx,exp=effectiveExpGain,coins=gainCoins,send=False)

                            if (a.char.level, a.char.stars) != temp:
                                listLvlUp.append("{0} : Niv. {1}{2} ??? Niv. {3}{4}\n".format(await a.getIcon(bot),temp[0],["","<:littleStar:925860806602682369>{0}".format(temp[1])][temp[1]>0],a.char.level,["","<:littleStar:925860806602682369>{0}".format(a.char.stars)][a.char.stars>0]))

                            if effectiveExpGain > 0:
                                gainMsg += "\n{0} ??? <:exp:926106339799887892> +{1}".format(await getUserIcon(bot,a.char),effectiveExpGain)

                            if baseGain != effectiveExpGain:
                                logs += "\n{0} got a {1}% exp boost (total : +{2} exp)".format(a.char.name,int((effectiveExpGain/baseGain-1)*100),effectiveExpGain)

                            userShop = userShopPurcent(a.char)
                            stuffRoll, skillRoll = constStuffDrop[userShop//10*10], constSkillDrop[userShop//10*10]
                            if allOcta:             # Loots
                                if not(winners):
                                    if random.randint(0,99) < stuffRoll:                   # Drop Stuff
                                        logs += "\n{0} have loot :".format(a.char.name)
                                        drop = listAllBuyableShop[:]
                                        for b in drop[:]:
                                            if a.char.have(obj=b) or type(b) not in [classes.weapon,classes.stuff]:
                                                drop.remove(b)

                                        if len(drop) > 0:
                                            rand = drop[random.randint(0,len(drop)-1)]
                                            newTemp = whatIsThat(rand)
                                            logs += " {0}".format(rand.name)

                                            if newTemp == 0:
                                                a.char.weaponInventory += [rand]
                                            elif newTemp == 2:
                                                a.char.stuffInventory += [rand]

                                            saveCharFile(path,a.char)
                                            usrIcon = await getUserIcon(bot,a.char)
                                            if usrIcon in gainMsg:
                                                gainMsg += f", {rand.emoji} {rand.name}"
                                            else:
                                                gainMsg += "\n{0} ??? {1} {2}".format(usrIcon,rand.emoji,rand.name)

                                        elif len(drop) == 0:
                                            gainTabl = [5,35,50,69,11,100,150,666,111,13,1,256,128,64,32]

                                            for comp in a.char.skills+a.char.stuff:                             # Dans toutes les comp??tences du personnage + ses ??quipementd
                                                if type(comp) == skill and comp.name == "Truc pas catho":       # Si On sais quoi est ??quip??
                                                    gainTabl = [69]                                             # Tu peux gagner que 69 pi??ces
                                                    break
                                                elif type(comp) == stuff and comp.name == "Tenue Provocante":   # Sinon, si On sait quoi 2 est ??quip??
                                                    gainTabl = [69]                                             # Tu peux gagner que 69 pi??ces aussi
                                                    break

                                            gain = gainTabl[random.randint(0,len(gainTabl)-1)]
                                            logs += " {0} pi??ces".format(gain)
                                            a.char.currencies += gain
                                            saveCharFile(path,a.char)
                                            if await getUserIcon(bot,a.char) in gainMsg:
                                                gainMsg += f", {gain} <:coins:862425847523704832>"
                                            else:
                                                gainMsg += "\n{0} ??? {1} <:coins:862425847523704832>".format(await getUserIcon(bot,a.char),gain)

                                    if random.randint(0,99) < skillRoll:
                                        logs += "\n{0} have loot :".format(a.char.name)
                                        drop = listAllBuyableShop[:]

                                        for b in drop[:]:
                                            if type(b) != classes.skill or a.char.have(obj=b):
                                                drop.remove(b)

                                        if len(drop) > 0:
                                            rand = drop[random.randint(0,len(drop)-1)]
                                            a.char.skillInventory += [rand]

                                            saveCharFile(path,a.char)
                                            usrIcon = await getUserIcon(bot,a.char)
                                            if usrIcon in gainMsg:
                                                gainMsg += f", {rand.emoji} {rand.name}"
                                            else:
                                                gainMsg += "\n{0} ??? {1} {2}".format(usrIcon,rand.emoji,rand.name)

                                        elif len(drop) == 0:
                                            gainTabl = [5,35,50,69,11,100,150,666,111,13,1,256,128,64,32]

                                            for comp in a.char.skills+a.char.stuff:                             # Dans toutes les comp??tences du personnage + ses ??quipementd
                                                if type(comp) == skill and comp.name == "Truc pas catho":       # Si On sais quoi est ??quip??
                                                    gainTabl = [69]                                             # Tu peux gagner que 69 pi??ces
                                                    break
                                                elif type(comp) == stuff and comp.name == "Tenue Provocante":   # Sinon, si On sait quoi 2 est ??quip??
                                                    gainTabl = [69]                                             # Tu peux gagner que 69 pi??ces aussi
                                                    break

                                            gain = gainTabl[random.randint(0,len(gainTabl)-1)]
                                            logs += " {0} pi??ces".format(gain)
                                            a.char.currencies += gain
                                            saveCharFile(path,a.char)
                                            if await getUserIcon(bot,a.char) in gainMsg:
                                                gainMsg += f", {gain} <:coins:862425847523704832>"
                                            else:
                                                gainMsg += "\n{0} ??? {1} <:coins:862425847523704832>".format(await getUserIcon(bot,a.char),gain)

                                    elif mainUser.owner == a.char.owner:
                                        if random.randint(0,999) < 334:
                                            aliceStatsDb.updateJetonsCount(mainUser,1)
                                            logs += "\n{0} a obtenu un jeton de roulette".format(mainUser.name)
                                            usrIcon = await getUserIcon(bot,a.char)
                                            if usrIcon in gainMsg:
                                                gainMsg += f", <:jeton:917793426949435402> Jeton de roulette"
                                            else:
                                                gainMsg += "\n{0} ??? <:jeton:917793426949435402> Jeton de roulette".format(usrIcon)
                                elif userShop < 35:
                                    if random.randint(0,99) < constLooseStuffDrop[int(userShop//10)]:
                                        logs += "\n{0} have loot :".format(a.char.name)
                                        drop = listAllBuyableShop[:]
                                        for b in drop[:]:
                                            if not(type(b) in [classes.weapon,classes.stuff,classes.skill] and not(a.char.have(obj=b))):
                                                if not(type(b) in [classes.weapon,classes.skill] or (type(b) == classes.stuff and b.minLvl < a.char.level)):
                                                    drop.remove(b)

                                        if len(drop) > 0:
                                            rand = drop[random.randint(0,len(drop)-1)]
                                            newTemp = whatIsThat(rand)
                                            logs += " {0}".format(rand.name)

                                            if newTemp == 0:
                                                a.char.weaponInventory += [rand]
                                            elif newTemp == 1:
                                                a.char.stuffInventory += [rand]                                            
                                            elif newTemp == 2:
                                                a.char.stuffInventory += [rand]

                                            saveCharFile(path,a.char)
                                            usrIcon = await getUserIcon(bot,a.char)
                                            if usrIcon in gainMsg:
                                                gainMsg += f", {rand.emoji} {rand.name}"
                                            else:
                                                gainMsg += "\n{0} ??? {1} {2}".format(usrIcon,rand.emoji,rand.name)

                                        elif len(drop) == 0:
                                            gainTabl = [5,35,50,69,11,100,150,666,111,13,1,256,128,64,32]

                                            for comp in a.char.skills+a.char.stuff:                             # Dans toutes les comp??tences du personnage + ses ??quipementd
                                                if type(comp) == skill and comp.name == "Truc pas catho":       # Si On sais quoi est ??quip??
                                                    gainTabl = [69]                                             # Tu peux gagner que 69 pi??ces
                                                    break
                                                elif type(comp) == stuff and comp.name == "Tenue Provocante":   # Sinon, si On sait quoi 2 est ??quip??
                                                    gainTabl = [69]                                             # Tu peux gagner que 69 pi??ces aussi
                                                    break

                                            gain = gainTabl[random.randint(0,len(gainTabl)-1)]
                                            logs += " {0} pi??ces".format(gain)
                                            a.char.currencies += gain
                                            saveCharFile(path,a.char)
                                            if await getUserIcon(bot,a.char) in gainMsg:
                                                gainMsg += f", {gain} <:coins:862425847523704832>"
                                            else:
                                                gainMsg += "\n{0} ??? {1} <:coins:862425847523704832>".format(await getUserIcon(bot,a.char),gain)

                    for ent in tablEntTeam[1]:
                        if type(ent.char) != char:
                            aliceStatsDb.addEnemyStats(enemy=ent.char, tablStats=ent.stats, winner=winners)

                    if len(gainMsg)>1000:
                        gainMsg = gainMsg.replace("<:exp:926106339799887892>","exp")
                    resultEmbed.add_field(name="<:em:866459463568850954>\n__Gains de l'??quipe joueur :__",value = gainMsg,inline=False)

                    if listLvlUp != []:
                        temp = ""
                        for a in listLvlUp:
                            temp+=a
                        await ctx.channel.send(embed=discord.Embed(title="__Mont??e de niveau__",color=light_blue,description="Le{0} personnage{0} suivant{0} {1} mont?? de niveau !\n".format(["","s"][len(listLvlUp)>1],["a","ont"][len(listLvlUp)>1])+temp))

                if errorNb > 0:
                    resultEmbed.add_field(name="<:empty:866459463568850954>\nDebugg :",value="{0} erreurs de connexions ont survenu durant ce combat",inline=False)

            else:
                logs += mauvaisePerdante
                for team in listImplicadTeams:
                    teamWinDB.changeFighting(team,0)
                logs += "\n"+format_exc()
                date = datetime.now()
                date = date.strftime("%H_%M")
                fich = open("./data/{0}_{1}.txt".format(ctx.author.name,date),"w",encoding='utf-8')
                if not(isLenapy):
                    try:
                        fich.write(unemoji(logs))
                    except:
                        print_exc()

                else:
                    fich.write(unemoji(logs))
                fich.close()
                opened = open("./data/{0}_{1}.txt".format(ctx.author.name,date),"rb")

                try:
                    msg = await ctx.send("Une erreur est survenue durant le combat",file=discord.File(fp=opened))
                except:
                    msg = await ctx.channel.send("Une erreur est survenue durant le combat",file=discord.File(fp=opened))

                opened.close()
                os.remove("./data/{0}_{1}.txt".format(ctx.author.name,date))
                haveError = True

            if not(haveError):
                if not(auto):
                    await turnMsg.delete()
                    if not(allAuto):
                        await choiceMsg.delete()
                startMsg = globalVar.getRestartMsg()
                if startMsg == 0:
                    await msg.edit(embed = resultEmbed,components=[create_actionrow(create_button(ButtonStyle.grey,"Chargement...",getEmojiObject('<a:loading:862459118912667678>'),"????",disabled=True))])
                else:
                    await msg.edit(embed = resultEmbed,components=[])
                if not(octogone):
                    for team in listImplicadTeams:
                        teamWinDB.changeFighting(team,0)
            # ------------ Succ??s -------------- #
            if not(octogone):
                for team in [0,1]:
                    for ent in tablEntTeam[team]:
                        if type(ent.char) == char and ent.char.team == mainUser.team:
                            achivements = achivement.getSuccess(ent.char)
                            if not(ent.auto): # Ivresse du combat
                                ent.char = await achivements.addCount(ctx,ent.char,"fight")

                            tablAchivNpcName = ["Alice","Cl??mence","Akira","Gwendoline","H??l??ne","Icealia","Shehisa","Powehi","F??licit??","Sixtine","Hina","Julie","Krys","Lio","Liu","Liz","Lia","Iliana","Stella","Kiku","Kitsune","Ailill","Altikia","Klironovia"]
                            tablAchivNpcCode = ["alice","clemence","akira","gwen","helene","icea","sram","powehi","feli","sixtine","hina","julie","krys","lio","liu","liz","lia","light","stella","kiku1","momKitsune","ailill2","alty","klikli"]

                            for cmpt in range(len(tablAchivNpcName)):
                                if dictIsNpcVar["{0}".format(tablAchivNpcName[cmpt])]: # Temp or enemy presence sussesss
                                    ent.char = await achivements.addCount(ctx,ent.char,tablAchivNpcCode[cmpt])

                            if dictIsNpcVar["Iliana"] and (dictIsNpcVar["Luna"] or dictIsNpcVar["Shihu"]):
                                ent.char = await achivements.addCount(ctx,ent.char,"lightNShadow")
                            if dictIsNpcVar["Luna"] or dictIsNpcVar["Shihu"]:
                                ent.char = await achivements.addCount(ctx,ent.char,"fullDark")
                            if tablEntTeam[1][0].isNpc("Luna ex."):
                                ent.char = await achivements.addCount(ctx,ent.char,"luna")
                            if tablEntTeam[1][0].isNpc("Cl??mence pos."):
                                ent.char = await achivements.addCount(ctx,ent.char,"clemMem")

                            # Act achivements
                            tablStatToSee = [ent.stats.headnt,ent.stats.sufferingFromSucess,ent.stats.lauthingAtTheFaceOfDeath]
                            tablCode = ["ailill","suffering","kiku2"]
                            for cmpt in range(len(tablStatToSee)):
                                if tablStatToSee[cmpt]:
                                    ent.char = await achivements.addCount(ctx,ent.char,tablCode[cmpt])

                            if ent.stats.friendlyfire > 0:
                                ent.char = await achivements.addCount(ctx,ent.char,"fratere")


                            if auto and int(ctx.author.id) == int(ent.char.owner): # Le temps c'est de l'argent
                                ent.char = await achivements.addCount(ctx,ent.char,"quickFight")

                            # Je ne veux pas d'??coli??re pour d??fendre nos terres
                            ent.char = await achivements.addCount(ctx,ent.char,"school")

                            # Elementaire
                            if ent.char.level >= 10:
                                ent.char = await achivements.addCount(ctx,ent.char,"elemental")

                            if not(winners) and ent.healResist >= 80 and ent.hp > 0:
                                ent.char = await achivements.addCount(ctx,ent.char,"dangerous")

                            if not(winners) and ent.stats.fullskip:
                                ent.char = await achivements.addCount(ctx,ent.char,"still")

                            if winners and danger == (dangerLevel[0] + (starLevel * DANGERUPPERSTAR)):
                                ent.char = await achivements.addCount(ctx,ent.char,"loose")

                            # Dimentio
                            if ent.char.level >= 20:
                                ent.char = await achivements.addCount(ctx,ent.char,"dimentio")

                            # Soigneur de compette
                            ent.char = await achivements.addCount(ctx,ent.char,"greatHeal",ent.stats.heals)

                            # La meilleure d??fense c'est l'attaque
                            ent.char = await achivements.addCount(ctx,ent.char,"greatDps",ent.stats.damageDeal-ent.stats.indirectDamageDeal)

                            # Notre pire ennemi c'est nous m??me
                            ent.char = await achivements.addCount(ctx,ent.char,"poison",ent.stats.indirectDamageDeal)

                            # Savoir utiliser ses atouts
                            ent.char = await achivements.addCount(ctx,ent.char,"estialba",int(ent.stats.estialba))

                            # Il faut que ??a sorte
                            ent.char = await achivements.addCount(ctx,ent.char,"lesath",int(ent.stats.bleeding))

                            if ent in dptClass[:3] and ent.stats.indirectDamageDeal == ent.stats.damageDeal:
                                ent.char = await achivements.addCount(ctx,ent.char,"dirty")
                            if ent == dptClass[0] and ent.stats.ennemiKill == 0:
                                ent.char = await achivements.addCount(ctx,ent.char,"delegation")

                            aliceStatsDb.addStats(ent.char,ent.stats)
                            saveCharFile(absPath + "/userProfile/"+str(ent.char.owner)+".prof",ent.char)

            timeout = False
            date, actuTeam, actuEntity, started, prec, logsAff = datetime.now()+horaire,0,0,False,None,False
            date = date.strftime("%H%M")
            fich = open("./data/fightLogs/{0}_{1}.txt".format(ctx.author.name,date),"w",encoding='utf-8')
            if not(isLenapy):
                try:
                    fich.write(unemoji(logs))
                except:
                    print_exc()
            else:
                fich.write(unemoji(logs))
            fich.close()

            def check(m):
                return m.origin_message.id == msg.id

            logsButton = create_button(ButtonStyle.grey,"Voir les logs","????","????")
            startMsg, potgMsg = globalVar.getRestartMsg(),None
            startMsg = startMsg == 0

            if longTurn:
                for team in listImplicadTeams:
                    teamWinDB.changeFighting(team,0)
                logs += "\n"+format_exc()
                date = datetime.now()+horaire
                date = date.strftime("%H%M")
                fich = open("./data/fightLogs/{0}_{1}.txt".format(ctx.author.name,date),"w",encoding='utf-8')
                if not(isLenapy):
                    try:
                        fich.write(unemoji(logs))
                    except:
                        print_exc()

                else:
                    fich.write(unemoji(logs))
                fich.close()
                opened = open("./data/fightLogs/{0}_{1}.txt".format(ctx.author.name,date),"rb")
                await asyncio.sleep(1)

                chan = await bot.fetch_channel(808394788126064680)

                desc = ""
                for temp in longTurnNumber:
                    desc += "Tour : {0} - {1} ({2} ms)\n".format(temp["turn"],temp["ent"],temp["duration"])

                await chan.send("Un tour anormalement long a ??t?? d??tect?? sur ce combat :",file=discord.File(fp=opened),embed=discord.Embed(title="__Tours mis en causes :__",description=desc))
                opened.close()

            potgIcon = None
            potg = []

            if playOfTheGame[1] != None:
                try:
                    potgIcon = await playOfTheGame[1].getIcon(bot)
                    potg = [create_actionrow(create_button(ButtonStyle.grey,"Action du combat",getEmojiObject(potgIcon),"potg"))]
                except:
                    pass

            while startMsg: # Tableau des statistiques
                options = []
                for team in [0,1]:
                    for num in range(len(endOfFightStats[team])):
                        ent = endOfFightStats[team][num]
                        options.append(create_select_option(ent.name,"{0}:{1}".format(team,num),getEmojiObject(await ent.getIcon(bot)),default=started and team == actuTeam and num == actuEntity))

                select = create_select(options,placeholder="Voir les statistiques d'un combattant")
                await msg.edit(embed = resultEmbed, components=[create_actionrow(select),create_actionrow(logsButton)]+potg)

                try:
                    interact = await wait_for_component(bot,msg,check=check,timeout=60)
                except:
                    toAff = []
                    if logsAff:
                        toAff.append(create_actionrow(logsButton))
                    if potgMsg != None:
                        toAff.append(create_actionrow(create_button(ButtonStyle.URL,"Action du combat",getEmojiObject(playOfTheGame[1].icon),url=potgMsg.jump_url)))

                    await msg.edit(embed = resultEmbed, components=toAff)
                    if prec != None:
                        await prec.delete()
                    return 1

                if interact.component_type == ComponentType.button:
                    if interact.custom_id == "????":
                        opened = open("./data/fightLogs/{0}_{1}.txt".format(ctx.author.name,date),"rb")
                        logsMsg = await interact.send("`Logs, {0} ?? {1}:{2}`".format(ctx.author.name,date[0:2],date[-2:]),file=discord.File(fp=opened))
                        opened.close()
                        logsButton = create_button(ButtonStyle.URL,"Voir les logs","????",url=logsMsg.jump_url)
                        logsAff = True
                    else:
                        potgMsg = await interact.send(embed = playOfTheGame[2].set_footer(icon_url="https://cdn.discordapp.com/emojis/{0}.png".format(getEmojiObject(potgIcon)["id"]),text="Action du combat"))
                        potg = [create_actionrow(create_button(ButtonStyle.URL,"Action du combat",getEmojiObject(potgIcon),url=potgMsg.jump_url))]
                else:
                    inter = interact.values[0]
                    haveTriggered = False
                    actuTeam,actuEntity = "",""
                    for letter in inter:
                        if letter != ":" and not(haveTriggered):
                            actuTeam += letter
                        elif letter != ":":
                            actuEntity += letter
                        else:
                            haveTriggered = True
                    actuTeam,actuEntity = int(actuTeam),int(actuEntity)
                    actu = endOfFightStats[actuTeam][actuEntity]
                    stats = actu.stats

                    if type(actu.char) == char:
                        userIcon = await getUserIcon(bot,actu.char)
                    else:
                        userIcon = actu.char.icon

                    descri = f"{actu.char.weapon.emoji}"

                    if type(actu.char) in [char,tmpAllie]:
                        descri += f" | {actu.char.stuff[0].emoji} {actu.char.stuff[1].emoji} {actu.char.stuff[2].emoji}"

                    skillTmp = ""
                    for a in actu.char.skills:
                        if type(a) == skill:
                            if skillTmp == "":
                                skillTmp = " |"
                            skillTmp += " {0}".format(a.emoji)

                    descri+=skillTmp
                    statsEm = discord.Embed(title = "__Statistiques de "+ userIcon +" "+actu.char.name+"__",color=actu.char.color,description=descri)

                    precisePurcent,dodgePurcent,critPurcent = "-","-","-"
                    if stats.totalNumberShot > 0:
                        precisePurcent = str(round(stats.shootHited/stats.totalNumberShot*100)) +"%"
                        critPurcent = str(round(stats.crits/stats.totalNumberShot*100)) +"%"
                    if stats.numberAttacked > 0:
                        dodgePurcent = str(round(stats.dodge/stats.numberAttacked*100)) +"%"

                    statsCatNames = ["__Statistiques offensives <:baleyette:873924668963291147> :__","__Statistiques d??fensives <:blindage:897635682367971338> :__","__Statistiques de soutiens <:roses:932612186130493450> :__","__Autres :__"]

                    tempDesc = "__D??g??ts totaux inflig??s :__ {0}\n> - D??g??ts indirects : {1}\n> - D??g??ts sous boost : {2}\n> - D??g??ts spirituels : {3}\n> - D??g??ts sur armure : {5}\n> - D??g??ts boost??s (Support) : {6}\n__Coups de gr??ce :__ {4}\n\n__Pr??cision :__ ".format(
                        highlight(separeUnit(actu.stats.damageDeal)),highlight(separeUnit(actu.stats.indirectDamageDeal)),highlight(separeUnit(actu.stats.underBoost)),highlight(separeUnit(actu.stats.maxHpReduced)),highlight(separeUnit(actu.stats.ennemiKill)),highlight(separeUnit(actu.stats.damageOnShield)),highlight(separeUnit(actu.stats.damageBoosted))
                        )
                    if actu.stats.totalNumberShot > 0:
                        tempDesc += "{0}%".format(round(actu.stats.shootHited/actu.stats.totalNumberShot*100))
                    else:
                        tempDesc += "-"

                    tempDesc += "\n__Taux Critique (D??g??ts) :__ "
                    if actu.stats.shootHited > 0:
                        tempDesc += "{0}%".format(round(actu.stats.crits/actu.stats.shootHited*100))
                    else:
                        tempDesc += "-"

                    statsEm.add_field(name=statsCatNames[0],value=tempDesc,inline=False)

                    tempDesc = "__Tours surv??cus :__ {0}\n__D??g??ts re??us :__ {1}\n> - D??g??ts r??sist??s : {2}\n> - D??g??ts bloqu??s : {3}\n> - D??g??ts r??duits (Support) : {4}\n\n__Taux d'esquives :__ ".format(actu.stats.survival,highlight(separeUnit(actu.stats.damageRecived)),highlight(separeUnit(int(actu.stats.damageResisted))),highlight(separeUnit(actu.stats.damageBlocks)),highlight(separeUnit(actu.stats.damageDogded)))
                    if actu.stats.numberAttacked > 0:
                        tempDesc += "{0}%".format(round(actu.stats.dodge/actu.stats.numberAttacked*100))
                    else:
                        tempDesc += "-"

                    tempDesc += "\n__Taux de blocage :__ "
                    if actu.stats.numberAttacked > 0:
                        tempDesc += "{0}%".format(round(actu.stats.blockCount/actu.stats.numberAttacked*100))
                    else:
                        tempDesc += "-"

                    statsEm.add_field(name="<:empty:866459463568850954>\n"+statsCatNames[1],value=tempDesc,inline=False)

                    tempDesc = "__{0} r??anim??s :__ {1}\n__Soins effectu??s :__ {2}\n> - Soins augment??es : {3}\n\n__Armure donn??e :__ {4}\n> - D??g??ts prot??g??s : {5}\n".format(
                        ["Combattants","Alli??s"][not(actu.isNpc("Kiku"))],highlight(actu.stats.allieResurected),highlight(separeUnit(actu.stats.heals)),highlight(separeUnit(actu.stats.healIncreased)),highlight(separeUnit(actu.stats.shieldGived)),highlight(separeUnit(actu.stats.armoredDamage))
                    )
                    
                    tempDesc += "\n__Taux critique (Soins et Armures) :__ "
                    if actu.stats.nbHeal > 0:
                        tempDesc += "{0}%".format(round(actu.stats.critHeal/actu.stats.nbHeal*100))
                    else:
                        tempDesc += "-"

                    statsEm.add_field(name="<:empty:866459463568850954>\n"+statsCatNames[2],value=tempDesc,inline=False)

                    tempDesc = "__Tours pass??s :__ {0}\n__D??g??ts sur soi-m??me :__ {1}".format(actu.stats.turnSkipped,highlight(separeUnit(actu.stats.selfBurn)))

                    statsEm.add_field(name="<:empty:866459463568850954>\n"+statsCatNames[3],value=tempDesc,inline=False)

                    statsEm.set_thumbnail(url="https://cdn.discordapp.com/emojis/{0}.png".format(getEmojiObject(await actu.getIcon(bot))["id"]))

                    if prec != None:
                        await prec.edit(embed = statsEm)
                    else:
                        prec = await interact.send(embed = statsEm)
                    started = True
    except:
        emby = embed=discord.Embed(title="__Uncatch error raised__",description=format_exc().replace("*",""))
        try:
            if footerText != "":
                emby.set_footer(text=footerText,icon_url=ctx.author.avatar_url)
        except:
            pass
        if msg == None:
            await ctx.channel.send(embed=emby,components=[])
        else:
            await msg.edit(embed=emby,components=[])

        teamWinDB.changeFighting(mainUser.team,0)
