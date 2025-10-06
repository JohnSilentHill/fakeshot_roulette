import pygame, os, json, time, random, msvcrt

pygame.mixer.init()

logoText = """
 _____ _____ _____ _____ _____ _____ _____ _____    _____ _____ _____ __    _____ _____ _____ _____ 
|   __|  _  |  |  |   __|   __|  |  |     |_   _|  | __  |     |  |  |  |  |   __|_   _|_   _|   __|
|   __|     |    -|   __|__   |     |  |  | | |    |    -|  |  |  |  |  |__|   __| | |   | | |   __|
|__|  |__|__|__|__|_____|_____|__|__|_____| |_|    |__|__|_____|_____|_____|_____| |_|   |_| |_____|
"""

infoTitle1 = """
ＨＯＷ  ＴＯ  ＰＬＡＹ
"""

infoTitle2 = """
ＩＴＥＭ  ＧＵＩＤＥ
"""

save_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "savegame.json")

def save_game(game):
    savegame = {
        "wins": game.wins,
        "money": game.money
    }
    save_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "savegame.json")
    with open(save_path, 'w') as f:
        json.dump(savegame, f, indent=4)
    echo1("Game saved.")

def play_sound(sound_name):
    base_dir = os.path.dirname(os.path.abspath(__file__)) 
    sound_path = os.path.join(base_dir, "sounds", f"{sound_name}.mp3")  
    if os.path.exists(sound_path):
        sound = pygame.mixer.Sound(sound_path)
        sound.play()
    else:
        print(f"Sound file {sound_name}.mp3 not found at {sound_path}")

# Both of the below replace typing 'play_sound("click1"), print("")'

def echo1(text): 
    play_sound("click1")
    print(text)

def echo2(text):
    play_sound("click2")
    print(text)

def play_bgm(filename):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    music_path = os.path.join(base_dir, "sounds", filename)
    if os.path.exists(music_path):
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1, fade_ms=500)
    else:
        print(f"Background music file {filename} not found.")

def start_bgm():
    if not pygame.mixer.music.get_busy():
        play_bgm("general_release.wav")
    else:
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.unpause()

def pause_bgm():
    pygame.mixer.music.fadeout(500)
    time.sleep(0.5)

class GameState:
    def __init__(state):
        state.money = 0
        state.rounds = 0
        state.roundsAbove2HP = 0
        state.correctShells = 0
        state.incorrectShells = 0
        state.wins = 0
        state.playerLives = 3
        state.aiLives = 3
        state.isSawed = False
        state.aiHandcuffed = False
        state.playerHandcuffed = False
        state.liveShells = 0
        state.blankShells = 0
        state.shellPool = []
        
        all_items = [beer, saw, magnifying_glass, handcuffs, cigarettes, phone, medicine, inverter]
        state.playerItems = random.sample(all_items, 3)

    def reset_lives(state):
        state.playerLives = 3
        state.aiLives = 3

    def cap_lives(state):
        state.playerLives = min(state.playerLives, 3)
        state.aiLives = min(state.aiLives, 3)

def debug(game):
    itemsDisplay = ", ".join(item.__name__ for item in game.playerItems)
    shell = game.shellPool.pop(0)
    debugOutput = [
        "",
        "----- DEBUG & OTHER INFO -----",
        "",
        f"money:             {game.money}",
        f"wins:              {game.wins}",
        f"rounds:            {game.rounds}",
        f"roundsAbove2HP:    {game.roundsAbove2HP}",
        f"playerLives:       {game.playerLives}",
        f"aiLives:           {game.aiLives}",
        f"isSawed?:          {game.isSawed}",
        f"playerHandcuffed?: {game.playerHandcuffed}", 
        f"aiHandcuffed?:     {game.aiHandcuffed}",
        f"liveShells:        {game.liveShells}",
        f"liveShells:        {game.blankShells}",
        f"correctShells:     {game.correctShells}",
        f"incorrectShells:   {game.incorrectShells}",
        f"currentShell:      {shell}",
        f"shellPool:         {game.shellPool}",
        f"playerItems:       [{itemsDisplay}]"
        
    ]
    for line in debugOutput:
        print(line)
    time.sleep(2), echo1("\nPress any key to resume...")
    msvcrt.getch(), play_sound("click2"), time.sleep(0.5)

    yourTurn(game)

def beer(game):

    play_sound("item_beer"), time.sleep(2)

    if not game.shellPool:
        echo1("\nNo shells left to eject.")
        return
    ejected = game.shellPool.pop(0)
    if ejected == 'live':
        play_sound("eject_live"), time.sleep(1)
        echo1("\nYou ejected a live shell.")
        game.liveShells -= 1
    else:
        play_sound("eject_blank"), time.sleep(1)
        echo1("\nYou ejected a blank shell.")
        game.blankShells -= 1
    if beer in game.playerItems:
        game.playerItems.remove(beer)

    yourTurn(game)

def saw(game):

    play_sound("item_saw"), time.sleep(3)

    game.isSawed = True
    echo1("\nYou saw off the barrel. Double damage next shot.")
    if saw in game.playerItems:
        game.playerItems.remove(saw)

    yourTurn(game)

def magnifying_glass(game):
    time.sleep(0.5), echo1("\nYou check the chamber...")
    time.sleep(1)
    if not game.shellPool:
        echo1("The chamber is empty.")
    else:
        chambered = game.shellPool[0]
        echo1(f"The next shell is a {chambered.upper()}.")
    if magnifying_glass in game.playerItems:
        game.playerItems.remove(magnifying_glass)

    yourTurn(game)

def handcuffs(game):
    echo1("\nYou give your opponent the handcuffs. They pass the next turn.")
    game.aiHandcuffed = True
    if handcuffs in game.playerItems:
        game.playerItems.remove(handcuffs)

    yourTurn(game)

def cigarettes(game):
    global money
    roll500 = random.randint(1,100)
    if roll500 == 1:
        echo1("\nFive Hundred Cigarettes.")
        echo1("\nYou gain $500")
        game.money += 500
    game.money += 500
    echo1("\nYou smoke a cigarette...")
    if game.playerLives == 3:
        echo1("Max health already.")
    else:
        echo1("+1 life.")
        game.playerLives += 1
    if cigarettes in game.playerItems:
        game.playerItems.remove(cigarettes)

    yourTurn(game)

def phone(game):
    echo1("\nYou pick up your burner phone..."), time.sleep(1)
    play_sound("phone"), time.sleep(1)

    shellNum = random.randint(1, len(game.shellPool))  
    shellType = game.shellPool[shellNum - 1] 

    play_sound("buzz"), print(f"SHELL {shellNum}. {shellType.upper()}.")

    if phone in game.playerItems:
        game.playerItems.remove(phone)

    time.sleep(2.7)

    yourTurn(game)

def medicine(game):
    echo1("\nYou take a pill...")
    time.sleep(1)
    medicineResult = random.randint(0,1)
    if medicineResult == 1:
        if game.playerLives == 1:
            echo1("Success... +2 lives.")
            game.playerLives += 2
        elif game.playerLives ==2:
            echo1("Success... +1 life.")
            game.playerLives += 1
        else:
            echo1("Success... Max health already.")
    else:
        echo1("It was expired. -1 life.")

    yourTurn(game)

    if medicine in game.playerItems:
        game.playerItems.remove(medicine)

def inverter(game):
    chambered = game.shellPool[0]
    echo1("\nYou invert the polarity of the shell...")
    if chambered == 'live':
        game.shellPool[0] = 'blank' 
    else:
        game.shellPool[0] = 'live' 

    yourTurn(game)

    if inverter in game.playerItems:
        game.playerItems.remove(inverter)

def adrenaline(game):
    print("Your opponent's items:")

# ITEMS END

def shootSelf(game):
    checkShells(game)
    shell = game.shellPool.pop(0) 
    if shell == 'live':
        echo1("You point the barrel at yourself...\n"), time.sleep(1)
        play_sound("live_self"), play_sound("heartbeat")
        if game.isSawed:
            echo1("\nSawed-off barrel deals double damage...\n-2 lives")
            game.playerLives -= 2
        else:
            echo1("-1 life.")
            game.playerLives -= 1
        game.liveShells -= 1
        game.incorrectShells += 1
    else:
        echo1("\nYou point the barrel at yourself...\n"), time.sleep(1)
        play_sound("shot_blank"), time.sleep(1)
        echo1("BLANK"), time.sleep(0.2)
        game.blankShells -= 1
        game.correctShells += 1
    time.sleep(1.5), play_sound("rack") 
    if game.isSawed:
        echo1("Barrel restored to default.")
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
        echo1("\nYou point the barrel at the AI...\n"), time.sleep(1)
        play_sound("live_ai"), time.sleep(1)
        echo1("LIVE"), time.sleep(1)
        if game.isSawed:
            echo1("\nSawed-off barrel deals double damage.\n-2 AI lives.")
            game.aiLives -= 2
        else:
            echo1("\n-1 AI life.")
            game.aiLives -= 1
        game.liveShells -= 1
        game.correctShells += 1
    else:
        echo1("\nYou point the barrel at the AI...\n"), time.sleep(1)
        play_sound("shot_blank"), time.sleep(1) 
        echo1("BLANK"), time.sleep(0.2)
        game.blankShells -= 1
        game.incorrectShells += 1
    time.sleep(1.5), play_sound("rack") 
    if game.isSawed:
        echo1("Barrel restored to default.")
        game.isSawed = False
    game.cap_lives()
    if game.aiLives <= 0:
        win(game)
    else:
        aiTurn(game)

def yourTurn(game):
    if game.aiLives <= 0:
        win(game)
        return
    checkShells(game)
    time.sleep(0.5)
    echo2("\n----- YOUR TURN -----\n")
    time.sleep(0.5)
    echo1(f"YOU: {game.playerLives} LIVES. AI: {game.aiLives} LIVES.\n"), time.sleep(0.4)
    echo1("INVENTORY:"), time.sleep(0.4)
    itemsDisplay = ", ".join(item.__name__ for item in game.playerItems)
    echo1(itemsDisplay)
    echo1("\n[itemname] or [me/ai]")
    turnAction = input("> ").strip().lower()
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
        echo1("Invalid input.")
        yourTurn(game)

def aiTurn(game):
    if game.aiLives <= 0:
        win(game)
        return
    if game.aiHandcuffed:
        echo1("\nAI skips its turn due to handcuffs.")
        game.aiHandcuffed = False
        yourTurn(game)
        return
    checkShells(game)
    time.sleep(0.5)
    echo1("\n----- AI'S TURN -----")
    shell = game.shellPool.pop(0)
    if shell == 'live':
        echo1("\nThe AI points the barrel at you...\n"), time.sleep(1)
        play_sound("live_self"), play_sound("heartbeat"), time.sleep(1)
        echo1("LIVE"), time.sleep(1)
        echo1("-1 life.")
        game.playerLives -= 1
        game.liveShells -= 1
        game.isSawed = False
        if game.playerLives == 1:
            play_sound("buzz"), print("\nCAREFUL NOW...")
    else:
        echo1("\nThe AI points the barrel at you...\n"), time.sleep(1)
        play_sound("shot_blank"), time.sleep(1)
        echo1("BLANK"), time.sleep(0.2)
        game.blankShells -= 1
        game.isSawed = False
    game.cap_lives()
    if game.playerLives <= 0:
        dead(game)
    else:
        yourTurn(game)

def checkShells(game):
    if not game.shellPool:
        echo1("\nNO SHELLS LEFT...")
        time.sleep(0.2)
        reloadShotgun(game)

def win(game):
    echo1("\nYou beat the AI in this round.\n")
    game.rounds += 1

    if game.playerLives > 2:
        game.roundsAbove2HP += 1

    echo1(f"Round {game.rounds}/3 complete.")

    if game.rounds >= 3:
        echo1("You win.")

        incorrects = game.incorrectShells if game.incorrectShells > 0 else 1

        raw_gain = (game.rounds * game.roundsAbove2HP * game.correctShells) / incorrects
        moneyGain = round(raw_gain * 100)

        echo1("Your winnings:")
        echo1(f"${moneyGain}")
        game.money += moneyGain

        game.wins += 1
        save_game(game)
        menu(game)
    else:
        echo1("\nReloading for next round...")
        time.sleep(2)
        startNewRound(game)  

def dead(game):
    echo1("\nYou died.")
    echo1(f"You survived {game.rounds} rounds.")
    save_game(game)
    menu(game)

def shellDisplay(game):
    play_sound("buzz"), print(f"\n{game.liveShells} LIVE. {game.blankShells} BLANK.") 
    time.sleep(0.7)

def playGuide():
    lines = [
        "A random amount of shells are placed in the shotgun in a random order.",
        "To win, you must shoot your opponent with live rounds enough times so they run out of health.",
        "",
        "You can shoot yourself too. If it is a blank shell you play again, else it is your opponent's go.",
        "You must use your items and your own smarts to determine what type of shell is chambered, and shoot accordingly.",
        "",
        "Good luck."
    ]
    for line in lines:
        print(line)

def itemGuide(game):
    lines = [
        "BEER:               Ejects 1 shell from the chamber.",
        "SAW:                Saws off the barrel, doubling damage for next shot.",
        "MAGNIFYING_GLASS:   Shows the next shell.",
        "HANDCUFFS:          Wearer skips their next turn.",
        "CIGARETTES:         Restores 1 health.",
        "PHONE:              Reveals info about a random shell.",
        "MEDICINE:           If normal: restores 2 lives, if expired: removes 1 life.",
        "INVERTER:           Changes the type of round currently chambered.",
        "ADRENALINE:         Allows the user to take an item from their opponent."
    ]
    for line in lines:
        print(line)

    time.sleep(2), echo1("\nPress any key to resume...")
    msvcrt.getch()
    menu(game)

def reloadShotgun(game):
    game.liveShells = random.randint(1, 4)
    game.blankShells = random.randint(1, 4)
    game.shellPool = ['live'] * game.liveShells + ['blank'] * game.blankShells
    random.shuffle(game.shellPool)

    game.cap_lives() # Max lives is always 3... for now

    shellDisplay(game)

    shellCount = game.liveShells + game.blankShells
    for _ in range(shellCount):
        play_sound("insert_shell")
        time.sleep(0.275) 

    play_sound("insert_end")
    time.sleep(0.25)
    play_sound("rack")
    time.sleep(0.6)

    yourTurn(game)

def startNewRound(game):
    echo1("\n--- NEW ROUND ---") # CHANGE THIS TO DISPLAY ROUND NUMBER

    # Resets lives and stuff
    game.reset_lives()

    # Resets your dumb items
    # all_items = [saw, saw, saw] -- Unhash this for debug
    all_items = [beer, saw, magnifying_glass, handcuffs, cigarettes, phone, medicine, inverter, adrenaline]
    game.playerItems = random.sample(all_items, 3)

    reloadShotgun(game)

def menu(game):
    global logoText
    game.reset_lives()
    time.sleep(0.5)
    start_bgm()
    print(logoText)
    time.sleep(0.5)
    echo2(f"You have {game.wins} win(s)."), time.sleep(0.5)
    echo1("Use [start], [info], or [quit] to save and quit...")
    menuInput = input("> ").strip().lower()
    if menuInput == "start":
        pause_bgm(), play_sound("start")
        time.sleep(1), startNewRound(game)
    elif menuInput == "info":
        pause_bgm(), play_sound("crt_sfx"), time.sleep(0.25)
        print("Loading info...\n"), time.sleep(1.6)
        echo2(infoTitle1), playGuide(), time.sleep(1)
        echo2(infoTitle2), itemGuide(game)
        return menu(game)
    elif menuInput == "quit":
        pause_bgm(), play_sound("select")
        save_game(game)
        echo1("\nExiting...")
        quit()
    else:
        echo1("\nNot a valid input.")
        return menu(game)

if __name__ == "__main__":
    game = GameState()
    if os.path.exists(save_path):
        with open(save_path, 'r') as f:
            savegame = json.load(f)
            game.wins = savegame.get("wins", 0)
    menu(game)