"""Draws the tricks and cards heatmaps from the processed score files."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src.datagen import REPO_FOLDER
from src.dataproc import TRICKS_DATA, CARDS_DATA

FIGURES_FOLDER = REPO_FOLDER / 'figures'

# Row and column order for both heatmaps
SEQ_ORDER = ['BBB', 'BBR', 'BRB', 'BRR', 'RBB', 'RBR', 'RRB', 'RRR']


def make_grid(scores: pd.DataFrame, column: str) -> pd.DataFrame:
    '''
    Reshape one column of the scores into an 8x8 grid.
    Rows are my choice (player 2), columns are the opponent's choice (player 1).
    The diagonal has no games, so it comes out as NaN.
    '''
    grid = scores.pivot(index='p1_choice', columns='p2_choice', values=column)
    return grid.reindex(index=SEQ_ORDER, columns=SEQ_ORDER)


def make_labels(win_grid: pd.DataFrame, tie_grid: pd.DataFrame) -> pd.DataFrame:
    '''
    Make the text for each cell, like "76(3)": win % with tie % in parentheses.
    The diagonal gets an empty label.
    '''
    labels = pd.DataFrame('', index=SEQ_ORDER, columns=SEQ_ORDER)

    for my_seq in SEQ_ORDER:
        for opp_seq in SEQ_ORDER:
            win = win_grid.loc[my_seq, opp_seq]
            tie = tie_grid.loc[my_seq, opp_seq]
            if not pd.isna(win):
                labels.loc[my_seq, opp_seq] = f'{win:.0f}({tie:.0f})'

    return labels


def draw_heatmap(win_grid: pd.DataFrame, labels: pd.DataFrame, title: str) -> plt.Figure:
    '''
    Draw one heatmap. The diagonal is shown in gray because those games are invalid.
    '''
    fig, ax = plt.subplots(figsize=(8, 7))

    # Hide the NaN diagonal so it gets the "bad" color (gray)
    colors = plt.get_cmap('Blues').copy()
    colors.set_bad('lightgray')
    cells = np.ma.masked_invalid(win_grid.to_numpy())

    image = ax.imshow(cells, cmap=colors, vmin=0, vmax=100)

    # Write the label in each cell, white text on the dark cells so it stays readable
    for row, my_seq in enumerate(SEQ_ORDER):
        for col, opp_seq in enumerate(SEQ_ORDER):
            win = win_grid.loc[my_seq, opp_seq]
            text_color = 'white' if win > 70 else 'black'
            ax.text(col, row, labels.loc[my_seq, opp_seq],
                    ha='center', va='center', color=text_color, fontsize=10)

    # Axis labels and ticks
    ax.set_xticks(range(len(SEQ_ORDER)))
    ax.set_xticklabels(SEQ_ORDER)
    ax.set_yticks(range(len(SEQ_ORDER)))
    ax.set_yticklabels(SEQ_ORDER)
    ax.set_xlabel('My Choice')
    ax.set_ylabel('Opponent Choice')
    ax.set_title(title)

    fig.tight_layout()

    return fig


def make_heatmap(scores_file: Path, game_name: str, figure_name: str) -> Path:
    '''
    Read one processed score file, draw its heatmap, and save it to figures/.
    Returns the figure's file path.
    '''
    scores = pd.read_csv(scores_file)

    win_grid = make_grid(scores, 'p2_win_pct')
    tie_grid = make_grid(scores, 'tie_pct')
    labels = make_labels(win_grid, tie_grid)

    # Every combo is played on every deck, so any row has the total deck count
    n_decks = scores['n_decks'].iloc[0]
    title = f'My Chance of Winning, {game_name}\n(N = {n_decks:,} decks)'

    fig = draw_heatmap(win_grid, labels, title)

    FIGURES_FOLDER.mkdir(parents=True, exist_ok=True)
    figure_path = FIGURES_FOLDER / figure_name
    fig.savefig(figure_path, dpi=200)
    plt.close(fig)

    return figure_path


def make_all_heatmaps() -> list[Path]:
    '''
    Make both heatmaps: one scored by tricks, one scored by cards.
    '''
    tricks_path = make_heatmap(TRICKS_DATA, 'Scored by Tricks', 'heatmap_tricks.png')
    cards_path = make_heatmap(CARDS_DATA, 'Scored by Cards', 'heatmap_cards.png')
    return [tricks_path, cards_path]

def show_heatmaps(paths: list[Path]) -> None:
    '''
    Displays the heatmaps without needing to regenerate them.
    Uses the paths returned from make_all_heatmaps.
    '''
    plt.ioff()
    for path in paths:
        image = plt.imread(path)
        fig, ax = plt.subplots()
        ax.imshow(image)
        ax.axis('off')
    plt.show()

