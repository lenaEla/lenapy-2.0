from attr import Attribute
from adv import *

# Parameters :
# tm# : Return the name of teammate number #. The order of the teammates is randomize when starting the commande
# tm#il : Return "il" if the teamate number # is a boy or a non-binary. "elle" if it's a girl
# tm#Il : Return "Il" if the teamate number # is a boy or a non-binary. "Elle" if it's a girl
# tm#e : Return "e" if the teamate number # is a girl. "" else
# tfils : Return "elles" if all the teammates are girls. "ils" else
# tfIls : Return "Elles" if all the teammates are girls. "Ils" else
# tfe : Return "e" il all the teamates are girls. "" else
# su : Return the name of the succesfull teammate
# suil : Return "elle" if the succesfull teammate is a girl. "il" else
# sue : Return "e" if the succesfull teammate is a girl. "" else

# Event involved teamMate ========================================
SOLO_ALL:int = 0            # All teammates tries to resolve the event
SOLO_SOLO:int = 1           # Only one teammate is allowed to try
ALL_TEAM:int = 2            # The event takes all the stats of all the teammates

# Event Wanted ===================================================
STATS = 0               # The chance of winning the event depend of the stats of the teammate
ASPIRATION = 1          # If the teammate have the good aspiration, they have twice chance to succed
SKILL = 2               # If the teammate have a skill in the list, they have twice chance de succed

class expeditionEvent:
    """The class for a expedition event"""
    def __init__(self,name:str,involved:int,wantedType:int,wantedStats:Union[int,List[skill]],wantedValue:int,intro:List[str],success:List[str],failure:List[str],staminaReduceIfSuccess:int,staminaReduceIfFailure:int,lootBonus:int=1,addTemp:Union[str,None]=None):
        self.name, self._involved, self._wantedType, self._wantedStats, self._wantedValue, self.intro, self.success, self.failure, self.staminaReduceIfSuccess, self.staminaReduceIfFailure,self.lootBonus, self.addTemp = name, involved, wantedType, wantedStats, wantedValue, intro, success, failure, staminaReduceIfSuccess, staminaReduceIfFailure,lootBonus,addTemp

    @property
    def involved(self):
        """Solo_all, Solo_solo or Team_All"""
        return self._involved

    @property
    def wantedType(self):
        """Stats, Aspiration or Skill"""
        return self._wantedType

    @property
    def wantedStats(self):
        """
        If wantedType == Stats :\n
        A `int` presenting the selected stats. Can be a `list(int)`
        """
        return self._wantedStats
    
    @property
    def wantedValue(self):
        """
        If wantedType == Stats :\n
        The value expedted for a 100% at lvl 50
        """
        return self._wantedValue

class expedition:
    """The class for the expedition"""
    def __init__(self,name:str,intro:List[str],events:List[expeditionEvent],notAllowed:Union[None,List[str]]=None):
        self.name, self.intro, self.events, self.notAllowed = name, intro, events, notAllowed

listExpedition:List[expedition] = [
    expedition(
        name="Temple en ruines",
        intro=[
            "Apr??s plusieurs dizaines de minutes ?? marcher vers le soleil levant, **{tm1}** et ses co??quipiers finirent par tomber sur un vieux temple en ruine. La v??g??tation avait sacr??ment reprit ses droits, les lianes et la mousse ayant recouvert la quasi totalit?? du b??timent.\nApr??s quelques minutes de d??lib??ration, l'??quipe d??cida de que ce serait l?? qu'elle ferait son exp??dition et s'engouffra dans les ruines.",
            "Alors qu'ils se demandaient dans quelle direction aller, **{tm4}** informa de reste de l'??quipe qu'{tm4il} avait entendu parler d'une rumeur ?? propos d'un vieu temple en ruine dans les environs de l'auberge o?? ils s??journaient.\nLa perspective d'une aventure dans un lieu abandonn?? depuis des si??cles envahis par des miriades d'insectes et araign??s n'avait pas trop l'air d'enchanter **{tm2}**, mais {tm2il} pris sur {tm2il}-m??me et le choix f??t fait.\n\nTrouver le temple f??t plus simple que ce qu'{tfils} avaient ??sp??r??s, mais ce n'??tait pas pour leur d??plaire. L'??ditfice ??tait cach?? au fond d'une for??t profonde et {tfils} avaient du pas mal crapahuter pour y arriver, mais maintenant {tfils} ??taient l??. Apr??s une grande inspiration collective, {tfils} s'engoufr??re ?? l'int??rieur des Ruines.",
            "Pendant que **{tm8}** et son ??quipe explorait une sombre for??t, **{tm5}** se mit ?? se plaindre qu'{tm5il} commen??ait s??rieusement ?? avoir envie d'aller au petit coin. L'??quipe s'arr??ta donc pour faire une pause d??jeun??e et **{tm5}** prit un peu de distance pour aller faire son affaire pendant que le reste de ses co??quipiers s'occupait de sortir les sandwitchs.\n\nCes derniers eurent cependant la d??sagrable surprise de l'entendre crier et lorsque **{tm7}** vint voir ce qui se passait, {tm7il} vit que **{tm5}** ??tait pass?? au travers d'un sol grandement friable et ??tait tomb?? dans une sorte de couloir. Apr??s avoir appel?? le reste de l'??quipe, {tfils} d??sid??re d'explorer les ruines qui s'ouvraient ?? eux..."
        ],
        events=[
            expeditionEvent(
                "M??canisme endurant",
                SOLO_ALL,STATS,ENDURANCE,350,
                ["Peu de temps apr??s ??tre entr??{tfe} dans l'??difice, {tfils} se retrouv??rent fasse ?? une impasse. Dans le mur se trouvait une sorte de levier, et **{tm1}** esseya de tirer dessus et se rendit compte qu'il opposait une forte r??sistance. D'autant plus, une sorte de son de m??canisme se fit entendre lorsqu'{tm1il} essaya.\n\n{tm1Il} en conclu qu'il fallait r??ussir ?? tirer sur le levier suffisament longtemps pour ouvrir le chemin.","Apr??s plusieurs tours et d??tours dans ce d??dale, {tfils} se retrouv??rent fasse ?? une impasse. Cependant, **{tm3}** d??couvrit qu'une pierre du mur semblait pouvoir bouger et tenta d'appuyer dessus.\nLa pierre semblait vouloir retourner d'elle m??me dans sa position d'origine, mais plus {tm3il} la maintenait pouss??e, plus les pierres autour semblaient bouger. L'??quipe en d??duit qu'elle fallait r??ussir ?? pousser la pierre suffisament longtemps pour ouvrir le chemin"],
                ["Apr??s plusieurs tentatives, ce f??t au final __**{su}**__ qui arrivea ?? activer le m??canisme suffisament longtemps. Avec plusieurs cliquetis, le mur s'ouvrit, leur r??v??lant un nouveau passage."],
                ["Malgr?? leurs efforts, personne ne r??ussi cependant ?? actionner le m??canisme suffisament longtemps. {tfIls} d??sid??rent que ??a ne servait ?? rien de s'acharner et rebrouss??rent chemin pour essayer de trouver un autre chemin."],
                5,12
            ),
            expeditionEvent(
                "Un bon sens de l'observation",
                SOLO_ALL,STATS,PRECISION,350,
                ["L'??quipe marcha un moment dans les ruines. Le lieu ??tait un vrai d??dale, et **{tm7}** ??tait passion??{tm7e} par les anciennes gravures qui s'??tandait ?? perte de vue"],
                ["Au bout d'un moment cependant, __**{su}**__ remarqua que l'un des murs ne semblait pas aussi normal que les autre et lorsqu'{suil} en approcha la main, {suil} d??couvrit qu'il s'agissait en r??alit?? d'une illusion d'optique caus?? par le manque d'??clairage et qu'il s'agissait en r??alit?? du mur d'un couloir adjacent\n\nApr??s avoir port?? sa d??couverte au reste de l'??quipe, cette derni??re d??cida de s'y avanturer."],
                ["Cela semblait cependant bien moins interresser **{tm2}**."],
                0,2
            ),
            expeditionEvent("Un combat d'envergure",ALL_TEAM,STATS,[STRENGTH,ENDURANCE,MAGIE,INTELLIGENCE],5000,
                [
                    "En explorant les ruines, l'??quipe fini par se retrouver dans une grande salle o?? {tfils} eurent la surprise de trouver **Alice** qui ??tait assise devant un mur.\nElle semblait avoir l'air abscente, ne les ayant m??me pas entendu lorsqu'{tfils} la rejoignirent et sursauta quand **{tm7}** lui toucha l'??paule.\n\n{alice} : \"Oh c'est vous... ... Hum... c'est surment pas le moment ou le lieu pour mais hum... j'aurais besoin d'un coup de main...\nPour... certaines raisons, je me suis aventur??e dans ces ruines et je me suis faites attaqu??e par des araign??es... Hum... pas des araign??es particuli??res hein... juste... des araign??es... normales... et hum... j'ai perdu un de mes rubans qu'elles ont emport??es dans leur nid...\"\n\nElle pointa de la t??te un petit trou dans le mur.\n\n{alice} : \"Vous... pouvez allez me le r??cup??rer s'il vous plait... j'y tiens beaucoup, ?? celui-la...\"\n\n**{tm4}** lui fit remarquer qu'{tfils} ??taient un peu grand pour rentrer dans le trou\n\n{alice} : \"Oh heu... c'est pas vraiment un probl??me ??a... Je... je peux changer la taille des gens... Je... je pourrais y aller moi-m??me mais... araign??es...\"\n\nL'??quipe accepta de l'aider ?? r??cup??rer son ruban. Alice se releva doucement, prit une inspiration puis ouvrit la main. Plusieurs boules lumineuses sortir??rent se sa paume et all??rent se loger dans la poitrine des membres de l'??quipes.\nLorsqu'{tfils} ouvrirent les yeux, {tfils} constat??rent qu'{tfils} ne mesurait qu'une dizaine de centim??tres. Alice les prit doucement dans ses mains, leur souhaita bonne chance et les amena ?? hauteur du trou."
                ],
                [
                    "Apr??s un combat acharn?? contre des dizaines arachn??s, l'??quipe r??ussi ?? s'en sortir vainqueuse. {tfIls} soufl??rent un bon coup puis se mirent ?? chercher le ruban. Il ne fut pas vraiment compliqu?? ?? trouver, car plusieurs cristaux taill??s en forme de coeurs ou de chauve-souris refl??tant la lumi??re ??taient fix??s ?? ses extr??mit??s. {tfIls} trouv??rent ??galement d'autres objets interressant.\n\nLors qu'{tfils} all??rent ?? l'extr??mit?? du nid, Alice sourit lorsqu'{tfils} rendirent son ruban qu'elle rattacha dans ses cheveux avant de les faire redescendre sur le plancher des vaches et leur rendre leur taille normale\n\n{alice} : \"Merci, j'aurais surment d?? faire une croix dessus si vous ??tiez pas pass?? dans le coins ^^' ... Ils n'y avait pas tant d'araign??s que ??a '-' ? Une c'est d??j?? trop... Mais bref qu'est-ce que vous faites ici en faite ? Vous ??tes en exp??dition pour l'Escadron ? Vous permettez que vous accompagne ^^ ? J'ai plus rien ?? faire ici et puis... si jamais il y a d'autres araign??es... Hum... N'y pensons pas ^^'\""
                ],
                [
                    "Malgr?? tous leurs effors, l'??quipe ne parvint pas ?? d??faire les multitudes de vagues d'araign??s, et d?? battre en retraite. Alice ??tait d????u mais elle fit de son mieux pour pas le montrer, elle qui ne pouvait pas faire grand chose en premiers lieux.\nElle les fit descendre du mur et leur rendit leur taille normal, puis d??cida de les accompagner, puisque ??a restera toujours plus utilse que de rester plant??e devant un mur ?? ne rien faire"
                ],
                15,25,3,"Alice"
                )
        ],
        notAllowed=["Alice"]
    )
]
