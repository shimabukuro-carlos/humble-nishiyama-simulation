## How to Play

[Penney’s Game](https://en.wikipedia.org/wiki/Penney%27s_game): Player 1 and Player 2 each select a sequence of at least 3 coin flip outcomes (heads and tails). Player 1 selects first, and then Player 2 picks. When a coin is flipped repeatedly, whoever’s chosen sequence appears first is the winner. Player 2 always has an advantage because they can pick a sequence that overlaps with Player 1’s choice.

The optimal sequence for Player 2 to pick, based on what Player 1 picks, is opposite of 2, 1, 2, where Player 1’s choice is in the format 1 2 3.

[Humble-Nishiyama Randomness Game](https://mathwo.github.io/assets/files/penney_game/humble-nishiyama_randomness_game-a_new_variation_on_penneys_coin_game.pdf): This is a variation on Penney’s Game using playing cards instead of a coin. Player 1 and Player 2 will each pick a sequence of three playing cards, either black or red. Player 2 can always pick a better sequence when they pick after Player 1, and Player 2 has a greater chance of winning with there only being 52 cards (instead of an unlimited number of coin flips). 

The first variation of the Humble-Nishiyama Randomness Game counts player wins based on number of **tricks**. When a player’s 3-card sequence appears, these cards are removed and counted as a trick. The player with the most tricks (i.e. the most pattern appearances) is the winner.

The second variation of the Humble-Nishiyama Randomness Game counts player wins based on the number of **cards** acquired by the end of the game. Every time a player’s 3-card sequence appears, these three cards and all cards before them are removed and counted for that player. The player who has the most cards at the end of the deck wins the game.

## Purpose of Investigation

The purpose of this investigation is to compare both Humble-Nishiyama Randomness Game variations. This project can simulate the game on a much larger scale than just playing the game with physical cards. The heatmaps allow us to visually compare the difference in Player 2’s chance of winning based on tricks and cards using all possible combinations of three cards.

## How to Run the Code

After downloading this repo, run the following line:
```
uv run main.py
```
The game will prompt you to either view heatmaps, add decks to the simulation, or quit. If you view the heatmaps, you must close them before being able to choose another menu option.


## Findings
