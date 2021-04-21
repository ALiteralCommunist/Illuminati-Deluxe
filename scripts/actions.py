##############################
#    List of Alignments      #      
##############################
ALLALIGNS = {'Peaceful', 'Violent', 'Government', 'Communist', 'Weird', 'Straight', 'Criminal', 'Liberal', 'Conservative', 'Fanatic'}
colorCoords = {'Red': (-258, -50), 'Blue': (-168, -50), 'Yellow': (-78, -50)}
groupCoords = {'First': (30, -75), 'Second': (135, -75), 'Third': (240, -75), 'Fourth': (345, -75), 'Fifth': (30, 7), 'Sixth': (135, 7), 'Seventh': (240, 7), 'Eighth': (345, 7)}
artCoords = {'First': (30, 80), 'Second': (103, 80), 'Third': (176, 80), 'Fourth': (249, 80), 'Fifth': (322, 80)}
illCoords = [(-50,150), (-160, 150), (60, 150), (-270, 150), (170, 150), (-380, 150), (280, 150), (-490, 150), (390, 150)]

##############################
#     Card Manipulation      #      
##############################

def shuffle(group, x = 0, y = 0):
    mute()
    group.shuffle()
    notify("{} shuffles their {}.".format(me, group.name))

def draw(group, x=0, y=0):
    mute()
    if len(group) < 1:
        return
    card = group.top()
    card.moveTo(me.hand)
    notify("{} draws a card.".format(me))

def drawShared(group, x=0, y=0):
    mute()
    if shared.Deck.controller != me: 
        whisper("It isn't your turn, you can't draw right now.")
        return
    card = shared.Deck.top()
    if card.properties['Card Type'] == "Special":
        card.moveTo(me.hand)
        notify("{} moves a Special card to their hand.".format(me))
    elif card.properties['Card Type'] == "Group":
        coords = checkCoords()
        if coords is not None: card.moveToTable(*coords)
        else: card.moveToTable(0,0)
        notify("{} moves {} to the table.".format(me, card))
    elif card.properties['Card Type'] == "Artifact":
        artifactcoords = checkArtCoords()
        if artifactcoords is not None: card.moveToTable(*artifactcoords)
        else: card.moveToTable(0,0)
        notify("{} moves {} to the table.".format(me, card))
    elif card.properties['Card Type'] == "New World Order":
        color = card.properties['NWO Color']
        x,y = colorCoords[color]
        discardAtPos(x, y)
        card.moveToTable(x, y)
        card.anchor = True
        notify("{} moves {} to the table.".format(me, card))
        drawShared(group, x=0, y=0)

def startingTargets(card, x=0, y=0):
    if card.properties['Card Type'] == "Group":
        coords = checkCoords()
        if coords is not None: card.moveToTable(*coords, forceFaceDown = True)
        else: card.moveToTable(0,0)

def grabIlluminati(group, x=0, y=0):
    mute()
    for c in table:
        if c.properties['Card Type'] == "Illuminati" and c.controller == me:
            c.moveTo(me.hand)
    notify("{} has randomly drawn an Illuminati card.".format(me))

def totalCardsAtPos(x, y):
    cards = [c for c in table if c.position == (x, y)]
    return len(cards)

def checkCoords():
    for x, y in sorted(groupCoords.values()):
        if totalCardsAtPos(x, y) == 0:
            return(x, y)

def checkArtCoords():
    for x, y in sorted(artCoords.values()):
        if totalCardsAtPos(x, y) == 0:
            return(x, y)

def checkIllCoords():
    for x, y in illCoords:
        if totalCardsAtPos(x, y) == 0:
            return(x, y)

def rotateRight(card, x = 0, y = 0):
    # Rot90, Rot180, etc. are just aliases for the numbers 0-3
    mute()
    if card.controller == me:
        card.orientation = (card.orientation + 1) % 4
        notify("{} Rotates {}.".format(me, card.Name))

def rotateLeft(card, x = 0, y = 0):
    # Rot90, Rot180, etc. are just aliases for the numbers 0-3
    mute()
    if card.controller == me:
        card.orientation = (card.orientation - 1) % 4
        notify("{} Rotates {}.".format(me, card.Name))
        
def clearTargets(group, x=0, y=0):
    notify("{} clears all targets.".format(me))
    for card in group:
        if card.controller == me:
            card.target(False)
        
def discard(card, x = 0, y = 0):
    mute()
    card.Cash = str(int(0))
    card.moveTo(shared.Discard)
    notify("{} discards {}.".format(me, card))

def discardAtPos(x, y):
    for card in table:
        if card.position == (x, y):
            discard(card)

def used(card, x=0, y=0):
    mute()
    usedFilter = "#99696969"
    if card.filter == None: 
        card.filter = usedFilter
    else: 
        card.filter = None

def flipCard(card, x = 0, y = 0):
    mute()
    if card.isFaceUp:
        notify("{} turns {} face down.".format(me, card))
        card.isFaceUp = False
    else:
        card.isFaceUp = True
        notify("{} turns {} face up.".format(me, card))

##############################
#          Random            #      
##############################
def rolldice(group, x = 0, y = 0):
    mute()
    n = rnd(1, 6)
    m = rnd(1, 6)
    notify("{} rolls {} ({} and {}).".format(me, n+m, n, m))

def rollsingle(group, x = 0, y = 0):
    mute()
    n = rnd(1, 6)
    notify("{} rolls {}.".format(me, n))

def flip(group, x = 0, y = 0):
    mute()
    n = rnd(1, 2)
    if n == 1: notify("{} flipped a coin: heads".format(me))
    else: notify("{} flipped a coin: tails.".format(me))

##############################
#        Highlights          #      
##############################

def red(card, x = 0, y = 0):
    mute()
    card.highlight = "#ff0000"

def orange(card, x = 0, y = 0):
    mute()
    card.highlight = "#ff9900"

def yellow(card, x = 0, y = 0):
    mute()
    card.highlight = "#ffff00"

def green(card, x = 0, y = 0):
    mute()
    card.highlight = "#00ff00"

def blue(card, x = 0, y = 0):
    mute()
    card.highlight = "#0000ff"

def purple(card, x = 0, y = 0):
    mute()
    card.highlight = "#9900ff"

def white(card, x = 0, y = 0):
    mute()
    card.highlight = "#ffffff"

def clear(card, x = 0, y = 0):
    mute()
    card.highlight = None


##############################
#           Money            #      
##############################

def verifyMB(card, x=0, y=0):
    if card.properties['Card Type'] not in ['Group', 'Illuminati']: return
    hasCash = ("Has MB", "e3a018e5-e87d-48b9-b47b-ba3f15ddeb81")
    if int(card.Cash) > 0: card.markers[hasCash] = 1
    else: card.markers[hasCash] = 0

def cashUp(card, x=0, y=0):
    if card.properties['Card Type'] not in ["Group", "Illuminati"]: return
    mute()
    card.Cash = str(int(card.Cash) + 1)
    verifyMB(card)
    notify("{} adds 1 MB to {}'s treasury.".format(me, card))
    
def cashDown(card, x=0, y=0):
    mute()
    if card.properties['Card Type'] not in ["Group", "Illuminati"]: return
    if int(card.Cash) >= 1:
        card.Cash = str(int(card.Cash) - 1)
        notify("{} removes 1 MB from {}'s treasury.".format(me, card))
    else:
        notify("There is no money in {}'s treasury.".format(card))
    verifyMB(card)
    
def cashUpX(card, x=0, y=0):
    mute()
    if card.properties['Card Type'] not in ["Group", "Illuminati"]: return
    count = askInteger("How many MB would you like to add?", 0)
    card.Cash = str(int(card.Cash) + count)
    verifyMB(card)
    notify("{} adds {} MB to {}'s treasury.".format(me, count, card))
    
def cashDownX(card, x=0, y=0):
    mute()
    if card.properties['Card Type'] not in ["Group", "Illuminati"]: return
    count = askInteger("How many MB would you like to remove?", 0)
    if count > int(card.Cash):
        whisper("There is only {} MB in {}'s treasury.".format((int(card.Cash)),card))
    else:
        card.Cash = str(int(card.Cash) - count)
        notify("{} removes {} MB from {}'s treasury.".format(me, count, card))
    verifyMB(card)
    
def checkTreasury(card, x=0, y=0):
    mute()
    if card.properties['Card Type'] not in ["Group", "Illuminati"]: return
    if card.controller == me:
        whisper("{} has {} MB in its treasury.".format(card, card.Cash))
    card.select(selection = False)

def collectIncome(card, x=0,y=0):
    mute()
    if card.properties['Card Type'] not in ["Group", "Illuminati"]: return
    if card.controller == me:
        if card.cardName == "I.R.S.":
            notify("The I.R.S. doesn't collect income normally. It collects tax from each other player.")
            return
        if card.cardName == "Post Office":
            notify("The Post Office doesn't collect income. Another group in its owner's Power Structure must pay.")
            return
        card.Cash = str(int(card.Cash) + int(card.Income))
        notify("{} collects income for {}.".format(me, card.Name))
    verifyMB(card)
    card.select(selection = False)

def transferCash(card, x=0, y=0):
    mute()
    whisper("Initiating transfer...")
    groupList = []
    cashList = []
    choiceList = []
    for c in table: 
        if c.controller == me and c.properties['Card Type'] != "Artifact" and c.properties['Card Type'] != "New World Order":
            groupList.append(c.cardName)
            cashList.append(c.Cash)
            choiceList.append("{} (Treasury: {} MB)".format(c.cardName, c.Cash))
    cardsAtPos = [a for a in table if a.position == (30, -75) or a.position == (135, -75) or a.position == (240, -75) or a.position == (345, -75) or a.position == (30, 7) or a.position == (135, 7) or a.position == (240, 7) or a.position == (345, 7)]
    for a in cardsAtPos:
            groupList.remove(a.cardName)
            cashList.remove(a.Cash)
            choiceList.remove("{} (Treasury: {} MB)".format(a.cardName, a.Cash))
    transFrom = askChoice("Transfer MB from:", choiceList)
    if transFrom == 0:
        whisper("Transfer aborted.")
        return
    whisper("Transferring funds from {}.".format(choiceList[transFrom-1]))
    transAmount = askInteger("How much MB would you like to transfer? (Available: {} MB)".format(cashList[transFrom-1]), 0)
    if transAmount == 0 or transAmount == None:
        whisper("Transfer aborted.")
        return
    if transAmount > int(cashList[transFrom-1]):
        whisper("Not enough funds to transfer that amount.")
        return
    whisper("Transferring {} MB. Standby.".format(transAmount))
    transTo = askChoice("Transfer MB to:", choiceList)
    if transTo == 0:
        whisper("Transfer aborted.")
        return
    whisper("Transferring to {}.".format(choiceList[transTo-1]))
    for c in table:
        if c.cardName in choiceList[transFrom-1]: c.Cash = str(int(c.Cash) - int(transAmount))
        if c.cardName in choiceList[transTo-1]: c.Cash = str(int(c.Cash) + int(transAmount))
    for c in table:
        verifyMB(c)
    notify("{} has transferred funds from {} to {}. Unable to trace precise amount.".format(me,groupList[transFrom-1],groupList[transTo-1]))
            
##############################
#           Turns            #      
##############################

def OnTurnPassedEvent(args):
  mute()
  if args.player == me:
    shared.Deck.controller = getActivePlayer()
    shared.Discard.controller = getActivePlayer()
    cardsAtPos = [a for a in table if a.position == (-258, -50) or a.position == (-168, -50) or a.position == (-78, -50) or a.position == (30, -75) or a.position == (135, -75) or a.position == (240, -75) or a.position == (345, -75) or a.position == (30, 7) or a.position == (135, 7) or a.position == (240, 7) or a.position == (345, 7) or a.position == (30, 80) or a.position == (103, 80) or a.position == (176, 80) or a.position == (249, 80) or a.position == (322, 80)]
    for a in cardsAtPos:
        a.controller = getActivePlayer()
    
def deckLoaded(args):
    mute()
    setup = 0
    if args.player == me:
        shared.Deck.controller = me
        shared.piles['Illuminati Cards'].controller = me
        shuffle(shared.Deck)
        shuffle(shared.piles['Illuminati Cards'])
        choiceList = ['Yes', 'No']
        choice = askChoice("Would you like to randomly draw Illuminati?", choiceList)
        if choice == 1: randomIlluminati(shared.piles['Illuminati Cards'])
        randomFirstPlayer(shared.Deck)

def randomFirstPlayer(group):
    mute()
    players = getPlayers()
    if len(players) <= 1:
        notify("{} is suspiciously chosen to be the first player. This must have been random... right?".format(me))
    else:
        n = rnd(0, len(players)-1)
        notify("{} is suspiciously chosen to be the first player. This must have been random... right?".format(players[n]))
        shared.Deck.controller = players[n]
        shared.Discard.controller = players[n]
        shared.piles['Illuminati Cards'].controller = players[n]
        setActivePlayer(players[n])
        
##############################
#           Goals            #      
##############################
        
def UFOgoals(card, x=0, y=0):
    if card.HiddenWinCon != "...":
        whisper("You've already chosen your special win condition. You chose {}".format(card.HiddenWinCon))
        return
    goalOptions = []
    for c in shared.piles['Illuminati Cards']: goalOptions.append("{} ({})".format(c.Nick, c.WinCon))
    choice = askChoice("Choose your secret goal:", goalOptions)
    cardChoice = shared.piles['Illuminati Cards'][choice-1]
    card.HiddenWinCon = goalOptions[choice-1]
    whisper("You selected {}.".format(card.HiddenWinCon))
    notify("The UFOs have selected their special win condition.")
    
def UFOreveal(card, x=0, y=0):
    if card.HiddenWinCon == "...": 
        whisper("You haven't yet selected your win condition.")
        return
    notify("The UFOs have revealed their secret goal! They chose {}!".format(card.HiddenWinCon))

def checkIlluminatiGoals(cards, x=0, y=0):
    notifyBar("#cc0000","                                                                                                                                                                                                                                                                                                                                                                                                ")
    number = len(players)
    if number < 4:
        basic = 13
    elif number == 4:
        basic = 12
    elif number == 5:
        basic = 10
    elif number == 6:
        basic = 9
    else:
        basic = 9
    notifyBar("#cc0000","The basic goal is to control {} groups.".format(basic))
    for c in cards:
        if c.cardName == "The Bavarian Illuminati": notifyBar("#cc0000","Bavaria's goal is to control groups with a total of 35 power including its own.")
        if c.cardName == "The Bermuda Triangle": notifyBar("#cc0000","Bermuda's goal is to control at least one group of each alignment.")
        if c.cardName == "The Discordian Society": notifyBar("#cc0000","Discordia's goal is to control 5 Weird groups.")
        if c.cardName == "The Gnomes of Zurich": notifyBar("#cc0000","Zurich's goal is to collect 150 MB in their Power Structure.")
        if c.cardName == "The Network": notifyBar("#cc0000","The Network's goal is to control groups with a total of 25 transferrable power including its own.")
        if c.cardName == "The Servants of Cthulhu": notifyBar("#cc0000","Cthulhu's goal is to destroy 8 groups.")
        if c.cardName == "The Society of Assassins": notifyBar("#cc0000","The Assassins' goal is to control 6 Violent groups.")
        if c.cardName == "The UFOs": 
            if c.controller == me: notifyBar("#cc0000","The UFO's goal is the same as {}".format(c.HiddenWinCon))
            else: notifyBar("#cc0000","The UFO's goal is unknown to you...")
        if c.cardName == "Church of the SubGenius": notifyBar("#cc0000","The Church of the SubGenius' goal is to control {} groups.".format(basic-1))
        if c.cardName == "Shangri-La": notifyBar("#cc0000","Shangri-La's goal is to control 5 Peaceful groups.")

def goalStatus(cards, x=0, y=0):
    weird = 0
    peace = 0
    violent = 0
    money = 0
    power = 0
    tpower = 0
    ownedAlign = set()
    number = len(players)
    if number < 4:
        basic = 13
    elif number == 4:
        basic = 12
    elif number == 5:
        basic = 10
    elif number == 6:
        basic = 9
    else:
        basic = 9
    genius = int(basic) - 1
    for card in cards:
        if "Weird" in card.Alignments:
            weird += 1
        if "Peaceful" in card.Alignments:
            peace += 1
        if "Violent" in card.Alignments:
            violent += 1
        money = money + int(card.Cash)
        power = power + int(card.Power)
        tpower = tpower + int(card.properties['Transferrable Power'])
        genius -= 1
        for a in card.Alignments.split(' '):
            ownedAlign.add(a)
    for card in cards:
        if card.Nick == "Discordia" or card.HiddenWinCon == "Discordia (Control 5 Weird groups)":
            whisper("You have {} Weird groups out of 5.".format(weird))
        elif card.Nick == "Shangri-La" or card.HiddenWinCon == "Shangri-La (Control 5 Peaceful groups)":
            whisper("You have {} Peaceful groups out of 5.".format(peace))
        elif card.Nick == "The Assassins" or card.HiddenWinCon == "The Assassins (Control 6 Violent groups)":\
            whisper("You have {} Violent groups out of 6.".format(violent))
        elif card.Nick == "Zurich" or card.HiddenWinCon == "Zurich (Total of 150 MB in their Power Structure)":
            whisper("You have {} MB out of 150.".format(money))
        elif card.Nick == "Bavaria" or card.HiddenWinCon == "Bavaria (Total of 35 Power)":
            whisper("You have {} Power out of 35.".format(power))
        elif card.Nick == "The Network" or card.HiddenWinCon == "The Network (Total of 25 Transferrable Power)":
            whisper("You have {} Transferrable Power out of 25.".format(tpower))
        elif card.Nick == "SubGenius" or card.HiddenWinCon == "SubGenius (Basic goal minus 1)":
            whisper("You still need {} groups out of {}.".format(genius, int(basic)-1))
        elif card.Nick == "Bermuda" or card.HiddenWinCon == "Bermuda (Control a group of every alignment)":
            whisper("You are still missing the following alignments: {}".format(list(ALLALIGNS - ownedAlign)))
        elif card.Nick == "Cthulhu" or card.HiddenWinCon == "Cthulhu (Destroy 8 groups)":
            whisper("You will need to keep track of destroyed groups on your own.")

def gnomeReveal(cards, x=0, y=0):
    money = 0
    for card in cards:
        money = money + int(card.Cash)
    notify("Zurich has a total of {} MB in their Power Structure!".format(money))
                
                
#################################
#        Defining Cards         #
#################################

def getsCash(cards, x=0, y=0):
    for c in cards:
        if c.properties['Card Type'] != "Group" and c.properties['Card Type'] != "Illuminati":
            return False
    return True
    
def isIlluminati(cards, x=0, y=0):
    for c in cards:
        if c.properties['Card Type'] == "Illuminati":
            return True
    return False

def isUFO(cards, x=0, y=0):
    for c in cards:
        if c.cardName == "The UFOs":
            if c.controller == me:
                return True
    return False

def isGnome(cards, x=0, y=0):
    for c in cards:
        if c.cardName == "The Gnomes of Zurich" or c.HiddenWinCon == "Zurich (Total of 150 MB in their Power Structure)":
            if c.controller == me:
                return True
    return False

#################################
#          Automation           #
#################################

def randomIlluminati(group, x=0, y=0):    
    notify("Generating shadowy superpowers, please stand by...")
    players = getPlayers()
    n = len(players)
    while n > 0:
        illuminaticoords = checkIllCoords()
        card = shared.piles['Illuminati Cards'].top()
        if illuminaticoords is not None: 
            card.moveToTable(*illuminaticoords, forceFaceDown = True)
            n -= 1
        else: 
            card = shared.piles['Illuminati Cards'].top()
            card.moveToTable(0,0, True)
            n -= 1
    notify("Shadowy superpowers generated.") 
    notify("Modifying global conditions, please stand by...")
    bonus = [c for c in shared.piles['Illuminati Cards']]
    remove = []
    for c in bonus:
        if c.Nick == "Bavaria":
            remove.append("8a7bdf06-9517-4330-a774-2e7acb4eca91")
            remove.append("92341ecc-a24e-4918-a0b7-2b0ba89250f0")
        if c.Nick == "Bermuda":
            remove.append("987744ec-c32a-4912-9773-562a49276c5b")
            remove.append("857c7c98-aad8-4ceb-bd99-8812bf7c4668")
        if c.Nick == "Zurich":
            remove.append("868dc052-ebfa-45e8-9941-8af568d5117d")
            remove.append("883cf074-074a-4f38-b26d-f4c938be5818")
        if c.Nick == "Cthulhu":
            remove.append("91b748b6-e6e1-4bca-9874-b96e927724e7")
            remove.append("85d2f5b3-0088-48a6-83c3-c79fa1faf14b")
        if c.Nick == "The Network":
            remove.append("8a627127-a243-4c45-8d67-cfb33c963873")
            remove.append("95be4552-d451-4a85-9653-ae78cea95b10")
        if c.Nick == "Discordia":
            remove.append("8c1b26fb-cd1c-47ad-b234-c56d40a67442")
            remove.append("8ef99c50-39e2-4099-85b8-9971f13a49db")
        if c.Nick == "UFOs":
            remove.append("8595c9ed-5dac-45c4-a197-a822bd0eba36")
            remove.append("88260c01-6e7b-41dd-8471-486d35d7c264")
        if c.Nick == "Shangri-La":
            remove.append("8ac9a4c8-adb4-4100-80ce-05c05e744392")
            remove.append("9243ed29-157f-4128-9d86-8c29e5c62ff1")
        if c.Nick == "The Assassins":
            remove.append("97f27a98-0cb2-4e8d-a99e-96996a264edd")
            remove.append("913ed2b1-cf7a-46f7-954d-ab5b6cfcf6c0")
        if c.Nick == "SubGenius":
            remove.append("946dfa4e-851a-44c2-b28b-cfef447d206c")
            remove.append("8b4c475c-fb6c-4df6-ae5c-1a469fd6d527")
    for c in shared.Deck:
        if c.model in remove:
            c.delete()
    for c in table:
        if c.position == (-160, 150): c.controller = players[1]
        if c.position == (60, 150): c.controller = players[2]
        if c.position == (-270, 150): c.controller = players[3]
        if c.position == (170, 150): c.controller = players[4]
        if c.position == (-380, 150): c.controller = players[5]
        if c.position == (280, 150): c.controller = players[6]
        if c.position == (-490, 150): c.controller = players[7]
        if c.position == (390, 150): c.controller = players[8]
    for p in players:
        remoteCall(p, "grabIlluminati", [table])
    notify("Global conditions reconfigured.")
    notify("Identifying targets, please stand by...")
    targets = 0
    while targets < 4:
        c = shared.Deck.top()
        if c.properties['Card Type'] != "Group": c.moveToBottom(shared.Deck)
        else: 
            startingTargets(c)
            targets += 1
    notify("Targets identified. Prepare for global domination.")        

#################################
#      Adding/Removing MB       #
#################################       

#def add1mb(card, x = 0, y = 0, qty = 1):
#   mute()
#   card.markers[MB] += qty
#   notify("{} adds 1MB to {}.".format(me, card))

#def add2mb(card, x = 0, y = 0, qty = 1):
#   mute()
#   card.markers[MMB] += qty
#   notify("{} adds 2MB to {}.".format(me, card))

#def add3mb(card, x = 0, y = 0, qty = 1):
#   mute()
#   card.markers[MMMB] += qty
#   notify("{} adds 3MB to {}.".format(me, card))
    
#def add5mb(card, x = 0, y = 0, qty = 1):
#   mute()
#   card.markers[MMMMB] += qty
#   notify("{} adds 5MB to {}.".format(me, card))

#def add10mb(card, x = 0, y = 0, qty = 1):
#   mute()
#   card.markers[MMMMMB] += qty
#   notify("{} adds 10MB to {}.".format(me, card))

#def add20mb(card, x = 0, y = 0, qty = 1):
#   mute()
#   card.markers[MMMMMMB] += qty
#   notify("{} adds 20MB to {}.".format(me, card))

#def sub1mb(card, x = 0, y = 0, qty = 1):
#   mute()
#   card.markers[MB] -= qty
#   notify("{} removes 1MB from {}.".format(me, card))
    
#def sub2mb(card, x = 0, y = 0, qty = 1):
#   mute()
#   card.markers[MMB] -= qty
#   notify("{} removes 2MB from {}.".format(me, card))
    
#def sub3mb(card, x = 0, y = 0, qty = 1):
#   mute()
#   card.markers[MMMB] -= qty
#   notify("{} removes 3MB from {}.".format(me, card))
    
#def sub5mb(card, x = 0, y = 0, qty = 1):
#   mute()
#   card.markers[MMMMB] -= qty
#   notify("{} removes 5MB from {}.".format(me, card))
    
#def sub10mb(card, x = 0, y = 0, qty = 1):
#   mute()
#   card.markers[MMMMMB] -= qty
#   notify("{} removes 10MB from {}.".format(me, card))
    
#def sub20mb(card, x = 0, y = 0, qty = 1):
#   mute()
#   card.markers[MMMMMMB] -= qty
#   notify("{} removes 20MB from {}.".format(me, card))

