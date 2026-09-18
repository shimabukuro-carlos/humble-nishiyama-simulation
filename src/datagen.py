"""Makes shuffled decks, saves them, and records the seed used."""

import json
from datetime import datetime
from pathlib import Path

import numpy as np

# Folders, based on where this file is
REPO_FOLDER = Path(__file__).parent.parent
DATA_FOLDER = REPO_FOLDER / 'data'
DECKS_FOLDER = DATA_FOLDER / 'raw'
SEED_FILE = DATA_FOLDER / 'seed.json'

CARDS_IN_DECK = 52
BLACK = 0
RED = 1


def get_next_seed() -> int:
    '''
    Return the last seed used plus 1. Start at 1 if there is none.
    '''
    # First batch
    if not SEED_FILE.exists():
        return 1

    # Read the last seed
    with open(SEED_FILE, 'r') as f:
        seed_info = json.load(f)

    return seed_info['seed'] + 1


def save_seed(seed: int) -> None:
    '''
    Save the seed and the time it was used.
    '''
    seed_info = {
        'seed': seed,
        'seed_time': str(datetime.now())
    }

    with open(SEED_FILE, 'w') as f:
        json.dump(seed_info, f)


def shuffle_decks(seed: int, n_decks: int) -> np.ndarray:
    '''
    Make n_decks shuffled decks.
    '''
    rng = np.random.default_rng(seed)

    # One deck in order: 26 black, 26 red
    one_deck = np.array([BLACK] * 26 + [RED] * 26, dtype=np.uint8)

    # Make n_decks copies, one per row
    all_decks = np.tile(one_deck, (n_decks, 1))

    # Shuffle each row
    shuffled = rng.permuted(all_decks, axis=1)

    return shuffled


def make_decks(n_decks: int) -> Path:
    '''
    Make n_decks decks, save them, and save the seed.
    Returns the file path.
    '''
    seed = get_next_seed()
    filename = DECKS_FOLDER / f'decks_seed_{seed}.npy'

    # Don't reuse a seed
    if filename.exists():
        raise FileExistsError(f'{filename} already exists. Check {SEED_FILE}.')

    decks = shuffle_decks(seed, n_decks)

    # Pack 8 cards into each byte to save space
    packed = np.packbits(decks, axis=1)

    DECKS_FOLDER.mkdir(parents=True, exist_ok=True)
    np.save(filename, packed)

    # Save the seed after the decks are saved
    save_seed(seed)

    return filename


def load_decks(filename: Path) -> np.ndarray:
    '''
    Load a deck file as 0s and 1s.
    '''
    packed = np.load(filename)

    # Unpack, keeping 52 cards per deck
    decks = np.unpackbits(packed, axis=1, count=CARDS_IN_DECK)

    return decks


def show_decks(filename: Path, n_decks: int = 5) -> None:
    '''
    Print the first few decks as R and B.
    '''
    decks = load_decks(filename)
    print(f'{filename.name} has {len(decks)} decks. First {n_decks}:')

    for deck in decks[:n_decks]:
        letters = ''
        for card in deck:
            if card == RED:
                letters += 'R'
            else:
                letters += 'B'
        print(letters)


if __name__ == '__main__':
    # Make a batch and print a few decks
    file = make_decks(100_000)
    show_decks(file, 3)