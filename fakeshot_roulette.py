import pygame, os, json, sys, time, random, msvcrt

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
    play_sound("click1"), print("Game saved.")

def play_sound(sound_name):
    base_dir = os.path.dirname(os.path.abspath(__file__)) 
    sound_path = os.path.join(base_dir, "sounds", f"{sound_name}.mp3")  
    if os.path.exists(sound_path):
        sound = pygame.mixer.Sound(sound_path)
        sound.play()
    else:
        print(f"Sound file {sound_name}.mp3 not found at {sound_path}")

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
        print(line)
    time.sleep(2), play_sound("click1"), print("\nPress any key to resume...")
    msvcrt.getch(), play_sound("click2"), time.sleep(0.5)

    yourTurn(game)

def beer(game):

    play_sound("item_beer"), time.sleep(2)

    if not game.shellPool:
        play_sound("click1"), print("\nNo shells left to eject.")
        return
    ejected = game.shellPool.pop(0)
    if ejected == 'live':
        play_sound("eject_live"), time.sleep(1)
        play_sound("click1"), print("\nYou ejected a live shell.")
        game.liveShells -= 1
    else:
        play_sound("eject_blank"), time.sleep(1)
        play_sound("click1"), print("\nYou ejected a blank shell.")
        game.blankShells -= 1
    if beer in game.playerItems:
        game.playerItems.remove(beer)

    yourTurn(game)

def saw(game):

    play_sound("item_saw"), time.sleep(3)

    game.isSawed = True
    play_sound("click1"), print("\nYou saw off the barrel. Double damage next shot.")
    if saw in game.playerItems:
        game.playerItems.remove(saw)

    yourTurn(game)

def magnifying_glass(game):
    play_sound("click1"), print("\nYou check the chamber...")
    if not game.shellPool:
        play_sound("click1"), print("The chamber is empty.")
    else:
        chambered = game.shellPool[0]
        play_sound("click1"), print(f"The next shell is a {chambered.upper()}.")
    if magnifying_glass in game.playerItems:
        game.playerItems.remove(magnifying_glass)

    yourTurn(game)

def handcuffs(game):
    play_sound("click1"), print("\nYou give your opponent the handcuffs. They pass the next turn.")
    game.aiHandcuffed = True
    if handcuffs in game.playerItems:
        game.playerItems.remove(handcuffs)

    yourTurn(game)

def cigarettes(game):
    global money
    roll500 = random.randint(1,100)
    if roll500 == 1:
        play_sound("click1"), print("\nFive Hundred Cigarettes.")
        play_sound("click1"), print("\nYou gain $500")
        game.money += 500
    game.money += 500
    play_sound("click1"), print("\nYou smoke a cigarette...")
    if game.playerLives == 3:
        play_sound("click1"), print("Max health already.")
    else:
        play_sound("click1"), print("+1 life.")
        game.playerLives += 1
    if cigarettes in game.playerItems:
        game.playerItems.remove(cigarettes)

    yourTurn(game)

def phone(game):
    play_sound("click1"), print("\nYou pick up your burner phone..."), time.sleep(1)
    play_sound("phone"), time.sleep(1)

    shellNum = random.randint(1, len(game.shellPool))  
    shellType = game.shellPool[shellNum - 1] 

    play_sound("buzz"), print(f"SHELL {shellNum}. {shellType.upper()}.")

    if phone in game.playerItems:
        game.playerItems.remove(phone)

    time.sleep(2.7)

    yourTurn(game)

def medicine(game):
    play_sound("click1"), print("\nYou take a pill...")
    time.sleep(1)
    medicineResult = random.randint(0,1)
    if medicineResult == 1:
        if game.playerLives == 1:
            play_sound("click1"), print("Success... +2 lives.")
            game.playerLives += 2
        elif game.playerLives ==2:
            play_sound("click1"), print("Success... +1 life.")
            game.playerLives += 1
        else:
            play_sound("click1"), print("Success... Max health already.")
    else:
        play_sound("click1"), print("It was expired. -1 life.")

    yourTurn(game)

    if medicine in game.playerItems:
        game.playerItems.remove(medicine)

def inverter(game):
    chambered = game.shellPool[0]
    play_sound("click1"), print("\nYou invert the polarity of the shell...")
    if chambered == 'live':
        game.shellPool[0] = 'blank' 
    else:
        game.shellPool[0] = 'live' 

    yourTurn(game)

    if inverter in game.playerItems:
        game.playerItems.remove(inverter)

def shootSelf(game):
    checkShells(game)
    shell = game.shellPool.pop(0) 
    if shell == 'live':
        play_sound("click1"), print("You point the barrel at yourself...\n"), time.sleep(1)
        play_sound("live_self"), play_sound("heartbeat")
        if game.isSawed:
            play_sound("click1"), print("\nSawed-off barrel deals double damage...\n-2 lives")
            game.playerLives -= 2
        else:
            play_sound("click1"), print("-1 life.")
            game.playerLives -= 1
        game.liveShells -= 1
    else:
        play_sound("click1"), print("\nYou point the barrel at yourself...\n"), time.sleep(1)
        play_sound("shot_blank"), time.sleep(1)
        play_sound("click1"), print("BLANK"), time.sleep(0.2)
        game.blankShells -= 1
    time.sleep(1.5), play_sound("rack") 
    if game.isSawed:
        play_sound("click1"), print("Barrel restored to default.")
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
        play_sound("click1"), print("\nYou point the barrel at the AI...\n"), time.sleep(1)
        play_sound("live_ai"), time.sleep(1)
        play_sound("click1"), print("LIVE"), time.sleep(1)
        if game.isSawed:
            play_sound("click1"), print("\nSawed-off barrel deals double damage.\n-2 AI lives.")
            game.aiLives -= 2
        else:
            play_sound("click1"), print("\n-1 AI life.")
            game.aiLives -= 1
        game.liveShells -= 1
    else:
        play_sound("click1"), print("\nYou point the barrel at the AI...\n"), time.sleep(1)
        play_sound("shot_blank"), time.sleep(1) 
        play_sound("click1"), print("BLANK"), time.sleep(0.2)
        game.blankShells -= 1
    time.sleep(1.5), play_sound("rack") 
    if game.isSawed:
        play_sound("click1"), print("Barrel restored to default.")
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
    play_sound("click2"), print("\n----- YOUR TURN -----\n")
    time.sleep(0.5)
    play_sound("click1"), print(f"YOU: {game.playerLives} LIVES. AI: {game.aiLives} LIVES.\n"), time.sleep(0.4)
    play_sound("click1"), print("INVENTORY:"), time.sleep(0.4)
    itemsDisplay = ", ".join(item.__name__ for item in game.playerItems)
    play_sound("click1"), print(itemsDisplay), time.sleep(0.4)
    play_sound("click1"), print("\n[itemname] or [me/ai]")
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
        play_sound("click1"), print("Invalid input.")
        yourTurn(game)

def aiTurn(game):
    if game.aiLives <= 0:
        win(game)
        return
    if game.aiHandcuffed:
        play_sound("click1"), print("\nAI skips its turn due to handcuffs.")
        game.aiHandcuffed = False
        yourTurn(game)
        return
    checkShells(game)
    time.sleep(0.5)
    play_sound("click1"), print("\n----- AI'S TURN -----")
    shell = game.shellPool.pop(0)
    if shell == 'live':
        play_sound("click1"), print("\nThe AI points the barrel at you...\n"), time.sleep(1)
        play_sound("live_self"), play_sound("heartbeat"), time.sleep(1)
        play_sound("click1"), print("LIVE"), time.sleep(1)
        play_sound("click1"), print("-1 life.")
        game.playerLives -= 1
        game.liveShells -= 1
        game.isSawed = False
        if game.playerLives == 1:
            play_sound("buzz"), print("\nCAREFUL NOW...")
    else:
        play_sound("click1"), print("\nThe AI points the barrel at you...\n"), time.sleep(1)
        play_sound("shot_blank"), time.sleep(1)
        play_sound("click1"), print("BLANK"), time.sleep(0.2)
        game.blankShells -= 1
        game.isSawed = False
    game.cap_lives()
    if game.playerLives <= 0:
        dead(game)
    else:
        yourTurn(game)

def checkShells(game):
    if not game.shellPool:
        play_sound("click1"), print("\nNO SHELLS LEFT...")
        time.sleep(0.2)
        preGame(game)

def win(game):
    global money
    play_sound("click1"), print("\nYou beat the AI.\n"), time.sleep(0.5), play_sound("click1"), print("Your winnings:"), time.sleep(0.5)
    play_sound("click1"), print("$2000")
    game.money += 2000
    game.wins += 1
    game.rounds += 1
    menu(game)

def dead(game):
    play_sound("click1"), print("\nYou died. Exiting...")
    game.rounds == 0
    menu()

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
        "INVERTER:           Changes the type of round currently chambered."
    ]
    for line in lines:
        print(line)

    time.sleep(2), play_sound("click1"), print("\nPress any key to resume...")
    msvcrt.getch()
    menu(game)

def preGame(game):
    game.liveShells = random.randint(1, 4)
    game.blankShells = random.randint(1, 4)
    game.shellPool = ['live'] * game.liveShells + ['blank'] * game.blankShells
    random.shuffle(game.shellPool)

    all_items = [phone, phone, phone]
    # all_items = [beer, saw, magnifying_glass, handcuffs, cigarettes, phone, medicine, inverter]
    game.playerItems = random.sample(all_items, 3)
    game.reset_lives()
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

def menu(game):
    global logoText
    game.reset_lives()
    time.sleep(0.5)
    start_bgm()
    print(logoText)
    time.sleep(0.5)
    play_sound("click2"), print(f"You have {game.wins} win(s)."), time.sleep(0.5)
    play_sound("click1"), print("Use [start], [info], or [quit] to save and quit...")
    menuInput = input("> ").strip().lower()
    if menuInput == "start":
        pause_bgm(), play_sound("start")
        time.sleep(1), preGame(game)
    elif menuInput == "info":
        pause_bgm(), play_sound("crt_sfx"), time.sleep(0.25)
        print("Loading info...\n"), time.sleep(1.6)
        play_sound("click2"), print(infoTitle1), playGuide(), time.sleep(1)
        play_sound("click2"), print(infoTitle2), itemGuide(game)
        return menu(game)
    elif menuInput == "quit":
        pause_bgm(), play_sound("select")
        save_game(game)
        play_sound("click1"), print("\nExiting...")
        quit()
    else:
        play_sound("click1"), print("\nNot a valid input.")
        return menu(game)

if __name__ == "__main__":
    game = GameState()
    if os.path.exists(save_path):
        with open(save_path, 'r') as f:
            savegame = json.load(f)
            game.wins = savegame.get("wins", 0)
    menu(game)