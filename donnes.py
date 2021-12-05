from constantes import maxChar,maxStrength,maxAgi,maxEndur,maxIntel,maxPreci,maxMagie

manPage0 = ["Manuel de l'Aventure - Par Lena","**__Sommaire :__**"]

manPage1 = ["Généralités","L'Aventure consiste à la réaliser plusieurs missons réparties en plusieurs chapitres.\n\nCes missions sont scénarisés et consistes en une succession d'événements prédéfinies qui vont mettre vos statistiques à l'épreuve"]
manPage2 = ["Statistiques Principales","Les statistiques principales sont au nombre de 7 :\n\n__**Force :**__ Influence la puissance des armes et compétences physiques\n\n__**Endurance :**__ Influence les Pv maximums, l'armure reçu et les soins reçus\n\n__**Charisme :**__ Influence les soins réalisées ainsi que certaines compétences de bonus ou de malus\n\n__**Agilité**__ et __**Précision**__ : Définnissent le taux de réussite de l'attaque ainsi que le taux de coup critique\n\n__**Intelligence :**__ Influance l'Armure donné ainsi que certaines compétences de bonus ou malus\n\n__**Magie :**__ Influence la puissance des armes et compétences magiques"]
manPage3 = ["Statistiques Secondaires","Les statistiques secondaires sont au nombre de 3\nContrairement aux statistiques principales, seuls les équipements ainsi que les bonus de compétences peuvent infliger dessus\n\n__**Résistance :**__ Chaque point réduit de **1%** les dégâts reçu. La réduction est cappé à 95%\n\n__**Pénétration d'Armure :**__ Contre-balance la résistance de l'adversaire. Si la pénétration est supérieur à la résistance adverse, augmente vos dégâts\n\n__**Critique :**__ Chaque point augmente de **1%** votre taux de coup critique"]
manPage4 = ["Statistiques d'Actions","Les statistiques d'actions se rajoute ou se soustraient à vos statistiques lorsque vous réalisez l'action correspondante\nSeul les équipements peuvent influer dessus"]
manPage5 = ["Présentation des combats","Une chose que vous serez souvent ammené durant votre aventure est à vous battre\n\nLors de ceux-ci, vous et toute votre équipe affronterez une équipe d'adversaire pouvant être prédéfinie ou aléatoire, suivant les missions\n\nAu début de chaque combat, un check-in sera réalisé. Les membres de votre équipe n'ayant pas réagit avant la fin du délais seront considérés comme des combattants automatiques\n\nLes combats se déroulent au tour part tour\nBien que la timeline soit une alternation entre Membre de l'Equipe 1 et Membre de l'Equipe 2, l'odre dans laquelle les personnages jouront est aléatoire\n\nUn combat se termine quand tous les membres d'une équipe ont été éliminés"]
manPage6 = ["L'Arme","__**En combat :**__\nChaque personnage utilise en combat l'arme qu'il a équippé\nLes armes determinent les placements au début du combat\n\nPour utilier votre arme, il faut que votre cible se trouve à portée et que vous ayez une ligne de vue dessus\n\nChaque arme tir un nombre prédéfinie de fois et possède une précision par défaut, affecté par la **Précision** et l'**Agilité** de votre cible\nSi l'attaque porte, vous lui infligez des dégâts dépendant de votre **Force** entre-autres\n\nChaque tir peut réaliser un **Coup Critque** qui augmente ses dégâts de 35%. Le taux de coup critique est définie par les statistiques\n\nCertaines armes peuvent accorder des effets passifs, qui sont attribués au début du combat\n\n__**Obtention :**__\nVous pouvez vous procurrez des armes au **Magasin** ou les looter en fin de combat\n\n__Exemple de page d'information d'une arme :__","https://media.discordapp.net/attachments/771410084961058836/871140947155644467/Capture_decran_de_2021-07-31_23-22-28.jpg"]
manPage7 = ["Les Compétences","**__En combat :__**\nLorsque vous utilisez les compétences que vous avez équipés, divers effets peuvent se produire, décrit dans la page d'information du sort\n\nSi votre sort est un sort de **__Dégâts__**, ceux-ci sont produits instantannément en tant que dégâts directs et prennent bien souvent la **Force** comme statistiques de base\n\nL'**__Armure__** donnés par certaines compétences augmente temporairement la santé de la cible. Si des dégâts font tomber les PV de l'armure à 0, celle-ci absorbe encore 50 dégâts avant de disparaitre\nGénéralement, la puissance de l'armure est augmentée par le **__Charisme__** ou l'**__Intelligence__** du lanceur ainsi que l'**__Endurance__** de votre cible\n\nLes compétences de **__Boost__** donnent des statistiques supplémentaires aux alliés ciblés ou dans la zone d'effet. Cepandant, la plupart de ces effets disparaissent au début de votre prochain tour\nLes compétences de boosts sont augmentés par le **__Charisme__** ou l'**__Intelligence__** suivant la compétence\n\nLes compétences de __**Debuff**__ sont simillaires aux compétences de Boost, mais donne des malus de statistiques aux adversaires\n\nLes compétences de __**Soins**__... soignent. La puissance des soins est affecté par le **__Charisme__**\n\nPour finir, les compétences de __**Dégâts Indirects**__ infligent des dégâts sous condition. Les dégâts indirects ne déclanchent pas les effets s'activant sur dégâts reçus et passe sous l'armure. Leur puissance est augmente par l'**__Intelligence__**\n\n__**Obtention :**__\nVous pouvez vous procurrez des compétences au **Magasin** ou les looter en fin de combat\n\n__Exemple de page d'information de compétence :__",'https://media.discordapp.net/attachments/771410084961058836/871139294092345344/Capture_decran_de_2021-07-31_23-15-13.png']
manPage8 = ["Vos personnages","Chaque joueur a un personnage unique qui est partagé entre tous les serveurs. Si vous n'avez pas encore le votre, vous pouvez le créer à l'aide de la commande l!start après avoir lu ce chapitre\n\nLe personnage sera ammené à combattre mais pas seulement ! Pour cela il possède une page d'aptitudes, de compétence et d'équipement !\n\n__Les aptitudes (ou statistiques) :__\nLa base de votre personnage. Durant l'aventure, vous serez amené à gagner en niveau et vos statistiques en feront tout autant !\nMais pour qu'il y ai un peu de disparité, chaque statistique évolu différament selon votre **aspiration**.\nPtdrCKoi ? Et bah tournons la page"]

manPage9 = ["Aspiration Berskeur","Tank - DPT\nLes berserkeurs ne font pas dans la finess ! Plus à l'aide à la ligne de front, ils frappent les ennemis sans répis avec leurs armes et utilise peu leurs compétences, si celles-ci ne tapent pas instantanément.\n\n__**Passif d'Aspiration :**__\nAu début du combat, réduit de **20%** leur endurance en échange d'un taux de **Vol de Vie** proportionnel à l'Endurance perdue\n\n__**Stats de base au niveau 50 :**__\nForce : {0}\nEndurance : {1}\nCharisme : {2}\nAgilité : {3}\nPrécision : {4}\nIntelligence : {5}\nMagie : {6}".format(maxStrength[0],maxEndur[0],maxChar[0],maxAgi[0],maxPreci[0],maxIntel[0],maxMagie[0])]
manPage10 = ["Aspiration Observateur","Distance - DPT\nLes observateurs préfères rester loins des combats, et c'est là qu'ils sont le plus efficace !\n\n__**Passif d'Aspiration :**__\nÀ chaques tirs touchés, le taux de critique des Observateurs augmente de **3%**. Le bonus est rénitialisé en cas de coup critique réalisée grâce à ce bonus et diminue de 20% à chaque attaque ratée\nLes coups critiques infligent plus de dégâts\n__**Stats de base au niveau 50 :**__\nForce : {0}\nEndurance : {1}\nCharisme : {2}\nAgilité : {3}\nPrécision : {4}\nIntelligence : {5}\nMagie : {6}".format(maxStrength[1],maxEndur[1],maxChar[1],maxAgi[1],maxPreci[1],maxIntel[1],maxMagie[1])]
manPage11 = ["Aspiration Poids Plume","Tank - DPT\nLes Poids Plumes aiment bien danser sous les tirs adverses, tout en portant des coups là où ça fait mal !\n\n__**Passif d'Aspiration :**__\nPour chaque esquive réalisée, le taux de critique des Poids Plumes augmente de 3%. Le bonus est réniatilsé en cas de coup critique réalisé grace à ce bonus et est divisé par 2 en fin de tour du Poids Plume\nLes coups critiques infligent plus de dégâts\n\n__**Stats de base au niveau 50 :**__\nForce : {0}\nEndurance : {1}\nCharisme : {2}\nAgilité : {3}\nPrécision : {4}\nIntelligence : {5}\nMagie : {6}".format(maxStrength[2],maxEndur[2],maxChar[2],maxAgi[2],maxPreci[2],maxIntel[2],maxMagie[1])]
manPage12 = ["Aspiration Idole","Distance - Support\nLes idoles sont de bon soutiens pour leur équipe mais compte également sur elle pour faire le reste du boulot à leur place\n\n__**Passif d'Aspiration :**__\nLa puissance boost qu'ils donnent augmente en fonction du nombre d'allié\n\n__**Stats de base au niveau 50 :**__\nForce : {0}\nEndurance : {1}\nCharisme : {2}\nAgilité : {3}\nPrécision : {4}\nIntelligence : {5}\nMagie : {6}".format(maxStrength[3],maxEndur[3],maxChar[3],maxAgi[3],maxPreci[3],maxIntel[3],maxMagie[3])]
manPage13 = ["Aspiration Prévoyant","Distance - Support\nLes Prévoyants n'ont pas leur pareil pour protéger leurs coéquipiers à l'aide de leurs bouclier, ou pour réduire les statistiques de leurs ennemis\n\n__**Passif d'Aspiration :**__\nLa puissance des boucliers des Prevoyants est plus élevée au début du combat\n\n__**Stats de base au niveau 50 :**__\nForce : {0}\nEndurance : {1}\nCharisme : {2}\nAgilité : {3}\nPrécision : {4}\nIntelligence : {5}\nMagie : {6}".format(maxStrength[4],maxEndur[4],maxChar[4],maxAgi[4],maxPreci[4],maxIntel[4],maxMagie[4])]
manPage14 = ["Aspiration Tête Brulée","Distance - DPT\nLes Têtes Brûlées n'aiment pas faire comme les autres et estiment que tout équipement est bon à prendre\n\n__**Passif d'Aspiration :**__\nEn début du combat, réduit la Force, Charisme, Intelligence et Magie de **20%**, et augmente toutes les statistiques d'actions de **35%**\n\n__**Stats de base au niveau 50 :**__\nForce : {0}\nEndurance : {1}\nCharisme : {2}\nAgilité : {3}\nPrécision : {4}\nIntelligence : {5}\nMagie : {6}".format(maxStrength[5],maxEndur[5],maxChar[5],maxAgi[5],maxPreci[5],maxIntel[5],maxMagie[5])]
manPage15 = ["Aspiration Mage","Distance - Magie\nLes mages ont préféré délaisser les armes conventionnelles pour s'attarder sur une autre source de dégâts : La magie\n\n__**Passif d'Aspiration :**__\nLors de l'utilisation d'une compétence devant être chargée, la Magie augmente de **15%**\n__**Stats de base au niveau 50 :**__\nForce : {0}\nEndurance : {1}\nCharisme : {2}\nAgilité : {3}\nPrécision : {4}\nIntelligence : {5}\nMagie : {6}".format(maxStrength[6],maxEndur[6],maxChar[6],maxAgi[6],maxPreci[6],maxIntel[6],maxMagie[6])]
manPage16 = ["Aspiration Altruiste","Distance - Support\nLes altruistes vont préférer se focaliser sur leurs alliés plutôt que sur eux-même\n\n__**Passif d'Aspiration :**__\nLa puissance des boosts et soins donnés à leurs alliés est augmentée, mais ceux réalisé sur soi-même est diminuée\n\n__**Stats de base au niveau 50 :**__\nForce : {0}\nEndurance : {1}\nCharisme : {2}\nAgilité : {3}\nPrécision : {4}\nIntelligence : {5}\nMagie : {6}".format(maxStrength[7],maxEndur[7],maxChar[7],maxAgi[7],maxPreci[7],maxIntel[7],maxMagie[7])]
manPage17 = ["Aspiration Invocateur","Neutre\nLes aventuriers n'ont pas vraiment envie de se spécialiser et font ce qu'il leur plait pour s'adapter à toutes situations\n\n__**Passif d'Aspiration :**__\nLes statistiques des invocations des invocateurs sont augmentées de 20%\n\n__**Stats de base au niveau 50 :**__\nForce : {0}\nEndurance : {1}\nCharisme : {2}\nAgilité : {3}\nPrécision : {4}\nIntelligence : {5}\nMagie : {6}".format(maxStrength[8],maxEndur[8],maxChar[8],maxAgi[8],maxPreci[8],maxIntel[8],maxMagie[9])]
manPage18 = ["Aspiration Enchanteur","Tank - Magie\nLes Enchanteurs veulent démontrer que la Magie n'est pas uniquement réservée à ceux qui restent bien au chaud à l'arrière\n\n__**Passif d'Aspiration :**__\nÀ chaque attaque subie, la Magie augmente de 3 (Cumulable, Fixe)\nLe bonus est rénitialisé en fin de tour\n\n__**Stats de base au niveau 50 :**__\nForce : {0}\nEndurance : {1}\nCharisme : {2}\nAgilité : {3}\nPrécision : {4}\nIntelligence : {5}\nMagie : {6}".format(maxStrength[9],maxEndur[9],maxChar[9],maxAgi[9],maxPreci[9],maxIntel[9],maxMagie[9])]
manPage19 = ["Aspiration Protecteur","Tank - Support\nLes protecteurs protègent leur équipe en se mettant face à l'ennemi. Ils sont plutôt doué également pour booster leurs alliés ou poser des malus aux ennemis\n\n__**Passif d'Aspiration :**__\nÀ chaque attaque subie, diminue la Force et la Magie de l'attaquant de 10 (Non cumulable, Fixe)\n\n__**Stats de base au niveau 50 :**__\nForce : {0}\nEndurance : {1}\nCharisme : {2}\nAgilité : {3}\nPrécision : {4}\nIntelligence : {5}\nMagie : {6}".format(maxStrength[10],maxEndur[10],maxChar[10],maxAgi[10],maxPreci[10],maxIntel[10],maxMagie[10])]

manPage20 = ["Combats pour les nuls","Reçamment, vous avez vu les bases des combats, mais avant de vous lancer tête baissée dans la mêlée, il y a certaines choses que vous devez voir, histoire de ne pas être totalement déboussolées"]
manPage21 = ["Résistance Soins, Friabilité, Résurrection récente et Mort Subite","Ce sont les noms de trois mécaniques que vous risquez de souvent buter contre, même sans vous en rendre compte\n\n__Résistance Soins__ :\nChaques soins que vous recevez augmentera petit à petit votre Résistance Soins, qui réduit la puissance des prochains effets curatifs que vous receverez.\nCette dernière augmente en fonction de vos PV maximum. Par consquéquent, plus vous avez de PV, moins la Résistance Soins viendra vous embêter\nCertains soins fixes (comme les vols de vie) ignorent la Résistance Soins.\n\n__Friabilité :__\nÀ partir d'un moment, la valeur des armures reçus va commencer à diminuer jusuq'à atteindre une valeur quasi nulle. Le seul moyen d'y échapper est de terminer le combat avant que cette mécanique ai trop d'effet\n\n__Résurection Récente :__\nChaque Résurection donne en plus une **Armure Absolue** de **20%** des PV maxmimum du revenant.\nLes armures absolues ne sont pas affectés par le malus d'armures consécutives ou les multiplicateurs de dégâts sur armure.\n\n__Mort Subite :__\nÀ partir du **Tour 16**, tous les combattants encore en vie perdent une partie de leurs PV, calculés en fonction de leurs PV maximums respectifs\nChaques tours passés en Mort Subite entraînent des dégâts de plus en plus conséquent.\nÀ noter qu'en cas de morts simultanées des derniers survivants de chaques équipes, c'est l'équipe Bleue qui gagne"]
manPage22 = ["Alliés Temporaires (ou \"Temp's\")","Si votre équipe comporte moins de **4 joueurs** lors du lancement d'un combat, cette dernière sera comblée avec des PNJ nommés les \"Alliés Temporaires\" (ou \"Temp's\" pour faire plus cours)\nLeur liste peut être visualisée dans l'encyclopédie\nLes alliés temporaires s'adaptent au niveau de l'équipe qu'ils rejoignent, ainsi qu'aux roles vacants.\n\nLorsqu'une équipe comporte **4 membres ou plus**, elle a désormais une probabilité d'affronter une équipe composée de Temp's en combat afin de ne pas être bloqué pour les succès en rapports avec ces derniers.\n\nCertains Temp's ont une probabilitée d'être remplacés par d'autre Temp's similaires (nommés \"Variants\"), et d'autres sont exclusifs à quelques combats spéciaux"]
manPage23 = ["Combats spéciaux","Chaques combats a une probabilité de déclancher un événement spécials :\n\n__Combat contre les Temp's :__\nComme indiqué sur la page précédente, il suffit d'avoir une équipe composée d'au moins 4 joueurs pour pouvoir déclancher cet événement.\nDurant ceux-ci, vous devrez affronter une équipe composée d'Alliés Temporaires, qui possèdent des sets adaptés à leurs rôles, et certains ont même quelques interractions entre eux\n\n__Combat de boss \"All vs One\" :__\nDurant ces combats, vous affronterez un ennemi unique, possédant souvent ses propres mécaniques.\nLes statistiques de ces ennemis sont diminués contre les petites équipes\n\n__Combats de boss :__\nUn ennemi notable a une chance de se glisser dans l'équipe adverse. À vous de l'éliminer avant que l'inverse se produise"]
manPage24 = ["Taux de danger","Selon les récentes performances de votre équipe, vous pourrez être affectés à des ennemis plus ou moins puissants, et ce grâce au **Taux de Danger**\n\nCe dernier influ sur les PV maximum, les dégâts, les soins, les armures ainsi que sur l'Agilité, la Précision et la Résistance de vos ennemis.\nUn taux de victoire récentes élevée vous permettra d'affronter des équipes au taux de Danger élevé, et à contrario, trop de défaite vous fera affronter des ennemis plus faibles.\n\nLe taux de danger influ très légèrement sur l'expérience gagné en fin de combat"]

tablPage = [
    manPage0,manPage1,manPage2,manPage3,manPage4,manPage5,manPage6,manPage7,manPage8,manPage9,manPage10,manPage11,manPage12,manPage13,manPage14,manPage15,manPage16,manPage17,manPage18,manPage19,manPage20,manPage21,manPage22,manPage23,manPage24]
chapter = [
    [manPage0],
    [manPage1,manPage2,manPage3,manPage4,manPage5,manPage6,manPage7],
    [manPage8,manPage9,manPage10,manPage11,manPage12,manPage13,manPage14,manPage15,manPage16,manPage17,manPage18,manPage19],
    [manPage20,manPage21,manPage22,manPage23,manPage24]
]
chapterName = [None,"Combat B.A.BA","Les personnages","Combat : Les subtilités"]
lenChapter = [0,1,8,20]

for a in range(1,len(chapter)):
    manPage0[1] += f"\n**__Chapitre {a}__: {chapterName[a]}**\n\n"
    for b in range(0,len(chapter[a])):
        manPage0[1] += f"{lenChapter[a]+b} - {chapter[a][b][0]}\n"