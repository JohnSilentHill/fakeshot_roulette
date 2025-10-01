import pygame, os, json, sys, time, random, msvcrt

pygame.mixer.init()

logoText = """
 _____ _____ _____ _____ _____ _____ _____ _____    _____ _____ _____ __    _____ _____ _____ _____ 
|   __|  _  |  |  |   __|   __|  |  |     |_   _|  | __  |     |  |  |  |  |   __|_   _|_   _|   __|
|   __|     |    -|   __|__   |     |  |  | | |    |    -|  |  |  |  |  |__|   __| | |   | | |   __|
|__|  |__|__|__|__|_____|_____|__|__|_____| |_|    |__|__|_____|_____|_____|_____| |_|   |_| |_____|

"""

# SAVING

save_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "savegame.json")

def save_game(game):
    savegame = {
        "wins": game.wins,
        "money": game.money
    }

    save_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "savegame.json")
    with open(save_path, 'w') as f:
        json.dump(savegame, f, indent=4)
    typing("Game saved.")

# TEXT OUTPUT

def typing(text, delay=0.025):
    for character in text:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def typingFast(text, delay=0.0125):
    for character in text:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(delay)
    print()

# SOUNDS

def play_sound(sound_name):
    base_dir = os.path.dirname(os.path.abspath(__file__)) 
    sound_path = os.path.join(base_dir, "sounds", f"{sound_name}.mp3")  

    if os.path.exists(sound_path):
        sound = pygame.mixer.Sound(sound_path)
        sound.play()
    else:
        print(f"Sound file {sound_name}.mp3 not found at {sound_path}")

# GAME STATES

class GameState:
    def __init__(state):
        state.money = 0
        state.rounds = 0
        state.wins = 0
        state.playerLives = 3
        state.aiLives = 3
        state.isSawed = False
        state.aiHandcuffed = False
        state.playerHandcuffed = False
        state.liveShells = 0
        state.blankShells = 0
        state.shellPool = []
        state.playerItems = []

    def reset_lives(state):
        state.playerLives = 3
        state.aiLives = 3

    def cap_lives(state):
        state.playerLives = min(state.playerLives, 3)
        state.aiLives = min(state.aiLives, 3)

# DEBUG

def debug(game):

    itemsDisplay = ", ".join(item.__name__ for item in game.playerItems)
    shell = game.shellPool.pop(0)

    debugOutput = [
        "",
        "----- DEBUG & OTHER INFO -----",
        "",
        f"money:             {game.money}",
        f"wins:              {game.wins}",
        f"playerLives:       {game.playerLives}",
        f"aiLives:           {game.aiLives}",
        f"isSawed?:          {game.isSawed}",
        f"playerHandcuffed?: {game.playerHandcuffed}", 
        f"aiHandcuffed?:     {game.aiHandcuffed}",
        f"liveShells:        {game.liveShells}",
        f"liveShells:        {game.blankShells}",
        f"currentShell:      {shell}",
        f"shellPool:         {game.shellPool}",
        f"playerItems:       [{itemsDisplay}]"
    ]

    for line in debugOutput:
            typingFast(line)

    typingFast("\nPress any key to resume...")
    msvcrt.getch()
    yourTurn(game)
    

# ITEM FUNCTIONS

def beer(game): # -----> BEER
    if not game.shellPool:
        typing("\nNo shells left to eject.")
        return

    ejected = game.shellPool.pop(0)
    if ejected == 'live':
        typing("\nYou ejected a live shell.")
        game.liveShells -= 1
    else:
        typing("\nYou ejected a blank shell.")
        game.blankShells -= 1

    if beer in game.playerItems:
        game.playerItems.remove(beer) # Removes the item from your inventory

    yourTurn(game)

def saw(game): # -----> SAW
    game.isSawed = True
    typing("\nYou saw off the barrel. Double damage next shot.")
    if saw in game.playerItems:
        game.playerItems.remove(saw)
    yourTurn(game)

def magnifying_glass(game):
    typing("\nYou check the chamber...")
    if not game.shellPool:
        typing("The chamber is empty.") # This is here in case something goes horribly wrong
    else:
        chambered = game.shellPool[0]
        typing(f"The next shell is a {chambered.upper()}.")

    if magnifying_glass in game.playerItems:
        game.playerItems.remove(magnifying_glass)

    yourTurn(game)

def handcuffs(game): # -----> HANDCUFFS
    typing("\nYou give your opponent the handcuffs. They pass the next turn.") # What a sucker
    game.aiHandcuffed = True
    if handcuffs in game.playerItems:
        game.playerItems.remove(handcuffs)
    yourTurn(game)

def cigarettes(game): # -----> CIGARETTES
    global money
    roll500 = random.randint(1,100)
    if roll500 == "1":
        typing("\nFive Hundred Cigarettes.")
        typing("\nYou gain $500")
        game.money += 500
    game.money += 500
    typing("\nYou smoke a cigarette...")
    if game.playerLives == 3:
        typing("Max health already.")
    else:
        typing("+1 life.")
        game.playerLives += 1
    if cigarettes in game.playerItems:
        game.playerItems.remove(cigarettes)
    yourTurn(game)

def phone(game): # -----> PHONE
    typing("\nYou pick up your burner phone..."), time.sleep(1)
    # typing("'Shell {shellnum}, {shelltype}.") # E.g: 'Shell 4, blank.'
    if phone in game.playerItems:
        game.playerItems.remove(phone)
    yourTurn(game)

def medicine(game): # -----> MEDICINE
    typing("\nYou take a pill...")
    time.sleep(1)
    medicineResult = random.randint(0,1)
    if medicineResult == 1:
        if game.playerLives == 1:
            typing("Success... +2 lives.")
            game.playerLives += 2
        elif game.playerLives ==2:
            typing("Success... +1 life.")
            game.playerLives += 1
        else:
            typing("Success... Max health already.")
    else:
        typing("It was expired. -1 life.")
    
    yourTurn(game)

def inverter(game): # -----> INVERTER
    chambered = game.shellPool[0]

    typing("\nYou invert the polarity of the shell...")
    
    if chambered == 'live':
        game.shellPool[0] = 'blank' 
    else:
        game.shellPool[0] = 'live' 

    yourTurn(game)

# SHOOTING

def shootSelf(game):
    checkShells(game)

    shell = game.shellPool.pop(0) 

    if shell == 'live':
        typing("You point the barrel at yourself...\n"), time.sleep(1) # LIVE
        play_sound("live_self")  
        if game.isSawed:
            typing("\nSawed-off barrel deals double damage...\n-2 lives")  # Rough
            game.playerLives -= 2
        else:
            typing("-1 life.")
            game.playerLives -= 1
        game.liveShells -= 1
    else:
        typing("You point the barrel at yourself...\n"), time.sleep(1) # BLANK
        play_sound("shot_blank")
        game.blankShells -= 1

    time.sleep(1.5), play_sound("rack") 

    if game.isSawed:
        typing("Barrel restored to default.")  # The barrel is restored to default regardless of shell outcome
        game.isSawed = False

    game.cap_lives()

    if game.playerLives <= 0:
        dead(game)
    elif shell == 'blank':
        yourTurn(game)
    else:
        aiTurn(game)

def shootAI(game):
    checkShells(game)

    shell = game.shellPool.pop(0)

    if shell == 'live':
        typing("\nYou point the barrel at the AI...\n"), time.sleep(1) # LIVE
        play_sound("live_ai") 
        if game.isSawed:
            typing("\nSawed-off barrel deals double damage.\n-2 AI lives.")  # Good call dude
            game.aiLives -= 2
        else:
            typing("\n-1 AI life.")
            game.aiLives -= 1
        game.liveShells -= 1
    else:
        typing("\nYou point the barrel at the AI...\n"), time.sleep(1) # BLANK
        play_sound("shot_blank")  
        game.blankShells -= 1

    time.sleep(1.5), play_sound("rack") 

    if game.isSawed:
        typing("Barrel restored to default.")
        game.isSawed = False

    game.cap_lives()

    if game.aiLives <= 0:
        win(game)
    else:
        aiTurn(game)

def yourTurn(game): # YOUR TURN
    if game.aiLives <= 0:
        win(game)
        return

    checkShells(game)

    time.sleep(0.5)
    typing("\n----- YOUR TURN -----\n")
    time.sleep(0.5)
    typing(f"YOU: {game.playerLives} LIVES. AI: {game.aiLives} LIVES.\n")

    typing("INVENTORY:")
    itemsDisplay = ", ".join(item.__name__ for item in game.playerItems)
    typing(itemsDisplay)

    typing("\nUse item [itemname] or [me/ai] to shoot...") # Crappy input dialogue, oh well
    turnAction = input("> ").strip().lower() # Do I need this?

    for item in game.playerItems:
        if turnAction == item.__name__.lower():
            item(game)
            return

    if turnAction == "me":
        shootSelf(game)
    elif turnAction == "ai":
        shootAI(game)
    elif turnAction == "debug":
        debug(game)
    else:
        typing("Invalid input.")
        yourTurn(game)

def aiTurn(game): # AI TURN
    if game.aiLives <= 0:
        win(game)
        return

    if game.aiHandcuffed:
        typing("\nAI skips its turn due to handcuffs.")
        game.aiHandcuffed = False
        yourTurn(game)
        return

    checkShells(game)

    time.sleep(0.5)
    typing("\n----- AI'S TURN -----")

    shell = game.shellPool.pop(0)

    if shell == 'live':
        typing("\nThe AI points the barrel at you...\n"), time.sleep(1)
        play_sound("shot_live")  # LIVE
        typing("-1 life.")
        game.playerLives -= 1
        game.liveShells -= 1
        game.isSawed = False

        if game.playerLives == 1:
            typing("\nCAREFUL NOW...")
    else:
        typing("\nThe AI points the barrel at you...\n"), time.sleep(1) # BLANK
        play_sound("shot_blank")
        game.blankShells -= 1
        game.isSawed = False

    game.cap_lives()

    if game.playerLives <= 0:
        dead(game)
    else:
        yourTurn(game)

# GAME STATE CHECKS

def checkShells(game):
    if not game.shellPool:
        typing("\nNO SHELLS LEFT\nRELOADING IN A RANDOM ORDER..."), time.sleep(1), typing("\nDone.")
        time.sleep(1)
        preGame(game)

def win(game):
    global money
    typing("\nYou beat the AI.\n"), time.sleep(0.5), typing("Your winnings:"), time.sleep(0.5)
    typing("$2000")
    game.money += 2000
    game.wins += 1
    game.rounds += 1
    menu(game)

def dead(game):
    typing("You died. Exiting...")
    game.rounds == 0
    quit()

# DISPLAY

def shellDisplay(game): # Displays on each turn
    typing(f"\n{game.liveShells} LIVE. {game.blankShells} BLANK.") 

def itemGuide(): # Only for use on the menu
    lines = [
        "BEER:               Ejects 1 shell from the chamber.",
        "SAW:                Saws off the barrel, doubling damage for next shot.",
        "MAGNIFYING_GLASS:   Shows the next shell.",
        "HANDCUFFS:          Wearer skips their next turn.",
        "CIGARETTES:         Restores 1 health.",
        "PHONE:              Reveals info about a random shell.",
        "MEDICINE:           If normal: restores 2 lives, if expired: removes 1 life.",
        "INVERTER:           Changes the type of round currently chambered."
    ]
    for line in lines:
        typing(line)

# ACTUAL GAME STUFF

def preGame(game): # This is only for functions, not any text output
    game.liveShells = random.randint(1, 4)
    game.blankShells = random.randint(1, 4)
    game.shellPool = ['live'] * game.liveShells + ['blank'] * game.blankShells
    random.shuffle(game.shellPool)

    all_items = [beer, saw, magnifying_glass, handcuffs, cigarettes, phone, medicine, inverter]
    game.playerItems = random.sample(all_items, 3)

    game.reset_lives()
    shellDisplay(game)
    yourTurn(game)

def menu(game):
    global logoText
    game.reset_lives()
    time.sleep(0.5)
    print(logoText)
    time.sleep(0.5)
    typing(f"You have {game.wins} win(s).")
    typing("Use [start], [info], or [quit] to save and quit...")

    menuInput = input("> ").strip().lower()
    if menuInput == "start":
        preGame(game)
    elif menuInput == "info":
        typing("-----------------\nINFO\n-----------------")
        itemGuide()
        menu(game)
    elif menuInput == "quit":
        save_game(game)
        typing("\nExiting...")
        quit()
    else:
        typing("\nNot a valid input.")
        menu(game)

# START GAME

if __name__ == "__main__":
    game = GameState()

    save_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "savegame.json")
    if os.path.exists(save_path):
        with open(save_path, 'r') as f:
            savegame = json.load(f)
            game.wins = savegame.get("wins", 0)

    menu(game)