# To-do
This is a to-do list that just goes into greater depth than the roadmap.

## 1. Complex AI

Currently the AI will always shoot by default. The code for this right now is extremely basic and goes through a sequence of logic as follows:
```
1. if aiLives <= 0:, player wins
2. if aiHandcuffed = True, skip turn
3. regradless of shell, always shoot player
4. if playerLives = <0:, player loses
```
### Solution

While it works for now, we need it to be able to use items (or not), and consequently determine who it wants to shoot.

The logic for this should work as such:


1. Import from all_items: `game.aiItems = random.sample(all_items, 3)`,
2. Add gamestate, does the AI know what bullet is chambered?: `state.aiKnowsShell`,
3. At the start of the AI's turn, call gamestate:,
```
if gamestate = True:
    use an item or choose who to shoot
if gamestate = False:
    use an item to gain info
      if no items:
          50/50 shoot self  # (we dont need AI counting bullets)
```
5. They act upon this and it either ends in a win, loss, player turn, or AI turn.

Obviously there is much more logic that goes into using an item. For example, they may be low on health so using cigarettes or medicine should ALWAYS take priority if they recently took damage. They may also take a risk - say 20% of all moves - where they will just shoot the player for the sake of it. But generally, it should act as a player would only based on the information they have stored in gamestates.

## 2. Money system.

This should be dynamic according to the number of rounds played and something else like times near death. I don't know how it works for the original game so maybe I'll need to look into that.

As a placeholder, I might make it work like this:

`moneyGain = ((rounds * roundsAbove2HP * correctShells) / incorrectShells)`

---

If you played 4 rounds (reloads), had 2 rounds above 2HP, got 7 correct shells, and 2 incorrect it returns:
 
`moneyGain = ((4 * 2 * 7) / 2) * 100` = $2800

If you played 2 rounds, had 1 round above 2HP, got 5 correct shells, and 4 incorrect it returns:

`moneyGain = ((2 * 1 * 5) / 4) * 100` = $250

---

You are compensated quite well for playing a good game with little mistakes.

As for what you do with this money... nothing. It's sort of useless in Buckshot Roulette but there is a double or nothing mode where new items are added. 

As of now, I don't plan on changing the item pool based on if it's double or nothing, but this may come later down the line once the main game is 100% complete.
        
