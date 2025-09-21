import os, json, sys, time, random

save_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "savegame.json")

def typing(text, delay=0.025):
    for character in text:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def save_game(game):
    savegame = {
        "wins": game.wins,
    }

    save_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "savegame.json")
    with open(save_path, 'w') as f:
        json.dump(savegame, f, indent=4)
    typing("Game saved.")

# Game states
class GameState:
    def __init__(self):
        self.playerLives = 3
        self.aiLives = 3
        self.isSawed = False
        self.aiSkipTurn = False
        self.wins = 0
        self.liveShells = 0
        self.blankShells = 0
        self.shellPool = []
        self.playerItems = []

    def reset_lives(self):
        self.playerLives = 3
        self.aiLives = 3

    def cap_lives(self):
        self.playerLives = min(self.playerLives, 3)
        self.aiLives = min(self.aiLives, 3)

# ITEM FUNCTIONS

def beer(game):
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

def saw(game):
    game.isSawed = True
    typing("\nYou saw off the barrel. Double damage next shot.")
    if saw in game.playerItems:
        game.playerItems.remove(saw)
    yourTurn(game)

def magnifying_glass(game):
    typing("\nYou check the chamber...")
    if not game.shellPool:
        typing("The chamber is empty.") # This shouldn't happen, but it's here in case something goes horribly wrong
    else:
        chambered = game.shellPool[0]
        typing(f"The next shell is a {chambered.upper()}.")

    if magnifying_glass in game.playerItems:
        game.playerItems.remove(magnifying_glass)

    yourTurn(game)

def handcuffs(game):
    typing("You pass your opponent the handcuffs. They pass the next turn.") # What a sucker
    game.aiSkipTurn = True
    if handcuffs in game.playerItems:
        game.playerItems.remove(handcuffs)
    yourTurn(game)

# SHOOTING

def shootSelf(game):
    if checkShells(game):
        return

    shell = game.shellPool.pop(0) # Selects the first shell in the sequence

    if shell == 'live':
        typing("You point the barrel at yourself..."), time.sleep(1), typing("BANG.")
        if game.isSawed:
            typing("\nSawed-off barrel deals double damage...\n-2 lives") # Rough
            game.playerLives -= 2
        else:
            typing("-1 life.")
            game.playerLives -= 1
        game.liveShells -= 1
    else:
        typing("Blank.")
        game.blankShells -= 1

    if game.isSawed:
        typing("Barrel restored to default.") # The barrel is restored to default regardless of shell outcome
        game.isSawed = False

    game.cap_lives()

    if game.playerLives <= 0:
        dead()
    elif shell == 'blank':
        yourTurn(game) 
    else:
        aiTurn(game)



def shootAI(game):
    if checkShells(game):
        return

    shell = game.shellPool.pop(0)

    if shell == 'live':
        typing("\nYou aim at the AI..."), time.sleep(1), typing("BANG.")
        if game.isSawed:
            typing("\nSawed-off barrel deals double damage.\n-2 AI lives.") # Good call dude
            game.aiLives -= 2
        else:
            typing("\n-1 AI life.")
            game.aiLives -= 1
        game.liveShells -= 1
    else:
        typing("\nBlank.")
        game.blankShells -= 1

    if game.isSawed:
        typing("Barrel restored to default.")
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

    if checkShells(game):
        return

    time.sleep(0.5)
    typing("\nYOUR TURN\n")
    time.sleep(0.5)

    typing("Inventory:")
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
    else:
        typing("Invalid input.")
        yourTurn(game)

def aiTurn(game):
    if game.aiLives <= 0:
        win(game)
        return

    if game.aiSkipTurn:
        typing("\nAI skips its turn due to handcuffs.")
        game.aiSkipTurn = False
        yourTurn(game)
        return

    if checkShells(game):
        return

    time.sleep(0.5)
    typing("\nAI'S TURN.")

    shell = game.shellPool.pop(0)

    if shell == 'live':
        typing("\nThe AI aims at you..."), time.sleep(1), typing("BANG.")
        typing("-1 life.")
        game.playerLives -= 1
        game.liveShells -= 1
        game.isSawed = False
    else:
        typing("\nThe AI aims at you..."), time.sleep(1), typing("BLANK.")
        game.blankShells -= 1
        game.isSawed = False

    game.cap_lives()

    if game.playerLives <= 0:
        dead()
    else:
        yourTurn(game)

# GAME STATE CHECKS

def checkShells(game):
    if not game.shellPool:
        typing("\nNo shells left.")
        if game.playerLives > game.aiLives:
            typing("You win by having more lives!")
        elif game.aiLives > game.playerLives:
            typing("AI wins by having more lives.")
        else:
            typing("It's a draw.")
        menu(game)
        return True
    return False

def win(game):
    typing("You survived.")
    game.wins += 1
    menu(game)

def dead():
    typing("You died. Exiting...")
    quit()

# DISPLAY

def shellDisplay(game): # Displays on each turn
    typing(f"\n{game.liveShells} live shell(s), {game.blankShells} blank shell(s)") 

def itemGuide(): # Only for use on the menu
    lines = [
        "BEER:               Ejects 1 shell from the chamber.",
        "SAW:                Saws off the barrel, doubling damage for next shot.",
        "MAGNIFYING_GLASS:   Shows the next shell.",
        "HANDCUFFS:          Wearer skips their next turn."
    ]
    for line in lines:
        typing(line)

# ACTUAL GAME SHIT

def preGame(game):
    game.liveShells = random.randint(1, 4)
    game.blankShells = random.randint(1, 4)
    game.shellPool = ['live'] * game.liveShells + ['blank'] * game.blankShells
    random.shuffle(game.shellPool)

    all_items = [beer, saw, magnifying_glass, handcuffs]
    game.playerItems = random.sample(all_items, 3)

    game.reset_lives()
    shellDisplay(game)
    yourTurn(game)

def menu(game):
    game.reset_lives()
    time.sleep(0.5)
    typing("-----------------\nFAKESHOT ROULETTE\n-----------------")
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
        typing("Saving and exiting game...")
        quit()
    else:
        typing("Not a valid input.")
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