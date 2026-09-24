import numpy as np
import pandas as pd
from itertools import permutations, product
from pathlib import Path

from src.datagen import BLACK, RED, DATA_FOLDER, DECKS_FOLDER, get_next_seed, load_decks

# file paths and columns
PROC_FOLDER = DATA_FOLDER / 'processed'
TRICKS_DATA = PROC_FOLDER / 'tricks_scores.csv'
CARDS_DATA = PROC_FOLDER / 'cards_scores.csv'
COUNT_COLUMNS = ['p2_wins', 'ties', 'n_decks']

def make_all_combinations() -> list[tuple[str, str]]:
    '''
    Makes all 56 combinations of 3-card sequences.
    Excludes the 8 combinations where player 1 and player 2 pick the same pattern (invalid).
    '''
    seqs = [''.join(seq) for seq in product('BR', repeat = 3)]
    return list(permutations(seqs, 2))

# make the combinations
COMBOS = make_all_combinations()

def play_one_combo(decks: list[str], p1_seq: str, p2_seq: str) -> tuple[dict, dict]:
    '''
    Plays one combination for every deck.
    '''
    p2_trick_wins = 0
    trick_ties = 0
    p2_card_wins = 0
    card_ties = 0

    for d in decks:
        pos = 0
        p1_tricks = 0
        p2_tricks = 0
        p1_cards = 0
        p2_cards = 0

        while True:
            # start seach for patterns from pos
            p1_idx = d.find(p1_seq, pos)
            p2_idx = d.find(p2_seq, pos)

            # if there aren't enough cards left in deck/no more sequences
            if p1_idx == -1 and p2_idx == -1:
                break
            # player 1 seq found first or player 2 seq is gone (but pl's isn't)
            if (p1_idx < p2_idx and p1_idx != -1) or (p2_idx == -1):
                p1_tricks += 1
                p1_cards += (p1_idx - pos) + 3
                pos = p1_idx + 3
            # player 2 seq found first
            else:
                p2_tricks += 1
                p2_cards += (p2_idx - pos) + 3
                pos = p2_idx + 3

        # assign points to winner
        if p2_tricks > p1_tricks:
            p2_trick_wins += 1
        elif p2_tricks == p1_tricks:
            trick_ties += 1
        if p2_cards > p1_cards:
            p2_card_wins += 1
        elif p2_cards == p1_cards:
            card_ties += 1

    # info for plotting dataframe
    n_decks = len(decks)
    tricks_counts = {'p2_wins': p2_trick_wins, 'ties': trick_ties, 'n_decks': n_decks}
    cards_counts = {'p2_wins': p2_card_wins, 'ties': card_ties, 'n_decks': n_decks}
    return tricks_counts, cards_counts
        

# play each deck for all 56 combinations
def play_all_batches(decks: list[str]) -> tuple[pd.DataFrame, pd.DataFrame]:
    '''
    Plays each deck with all 56 combinations of player card sequences.
    '''
    tricks_rows = []
    cards_rows = []

    for p1_seq, p2_seq in COMBOS:
        tricks_counts, cards_counts = play_one_combo(decks, p1_seq, p2_seq)

        # merge player choices as first two cols, p2 win stats, tie stat, and num decks as rest of cols
        # two dfs - one for tricks and one for cards
        tricks_rows.append({'p1_choice': p1_seq, 'p2_choice': p2_seq, **tricks_counts})
        cards_rows.append({'p1_choice': p1_seq, 'p2_choice': p2_seq, **cards_counts})
    
    return pd.DataFrame(tricks_rows), pd.DataFrame(cards_rows)


# calculate the percentages
def calculate_percents(df: pd.DataFrame) -> pd.DataFrame:
    '''
    Calculate win and tie percentages based on the counts in the dataframes.
    '''
    df = df.copy()
    df['p2_win_pct'] = df['p2_wins']/df['n_decks']*100
    df['tie_pct'] = df['ties']/df['n_decks']*100
    return df


def load_existing(file: Path) -> pd.DataFrame | None:
    '''
    If the game has been played before, load those scores.
    Otherwise, return nothing.
    '''
    if file.exists():
        return pd.read_csv(file)
    return None


def merge_scores(existing_data: pd.DataFrame | None, new_data: pd.DataFrame) -> pd.DataFrame:
    '''
    Adds new scores to the existing scores if additional decks are added to the game.
    Otherwise calls function to calculate percentages for the new data.
    '''
    if existing_data is None:
        return calculate_percents(new_data)
        
    merged_data = existing_data.set_index(['p1_choice','p2_choice'])
    new_indices = new_data.set_index(['p1_choice','p2_choice'])

    for col in COUNT_COLUMNS:
        merged_data[col] = merged_data[col] + new_indices[col]
    
    merged_data = merged_data[COUNT_COLUMNS].reset_index()
    return calculate_percents(merged_data)

    
def process_decks(raw_data: Path) -> None:
    '''
    Loads the raw decks and converts them to strings.
    Plays the game for all 56 combinations and adds scores to existing data (if any).
    '''
    # from datagen.py
    decks = load_decks(raw_data)

    # assign R to 1, B to 0 and combine into strings
    deck_grid = np.where(decks == RED, 'R', 'B')
    deck_strs = [''.join(deck) for deck in deck_grid]

    # play the game for all decks
    new_tricks, new_cards = play_all_batches(deck_strs)

    # gets existing score data
    existing_trick_data = load_existing(TRICKS_DATA)
    existing_card_data = load_existing(CARDS_DATA)

    # combine new data and existing data
    tricks_df = merge_scores(existing_trick_data, new_tricks)
    cards_df = merge_scores(existing_card_data, new_cards)

    # make processed data folder in directory and save dataframes as csv files
    PROC_FOLDER.mkdir(parents = True, exist_ok = True)
    tricks_df.to_csv(TRICKS_DATA, index = False)
    cards_df.to_csv(CARDS_DATA, index = False)

    #return tricks_df, cards_df


# if __name__ == '__main__':
#     seed = get_next_seed() - 1
#     raw = DECKS_FOLDER / f'decks_seed_{seed}.npy'

#     tricks_df, cards_df = process_decks(raw)
    