from src.datagen import make_decks, get_next_seed, DECKS_FOLDER
from src.dataproc import process_decks
from src.datavis import make_all_heatmaps, show_heatmaps
from pathlib import Path

def main():
    '''
    Operates the simulation using user input to see heatmaps, add decks, or quit the program.
    '''

    # file paths for where heatmaps should be
    PATH = [Path(__file__).parent / 'figures' / 'heatmap_cards.png', Path(__file__).parent / 'figures' / 'heatmap_tricks.png']

    user_choice = 0
    while user_choice != '3':
        user_choice = input('Enter 1 to display heatmaps, 2 to add more decks to the simulation, or 3 to quit: ')
        if user_choice == '1':
            # if heatmaps already exist
            if PATH[0].exists() and PATH[1].exists():
                print('Generating heatmaps...')
                # datavis:
                show_heatmaps(PATH)
            # if heatmaps don't exist, user needs to add decks first
            else:
                print('Add decks first before displaying heatmaps.')
        elif user_choice == '2':
            num_new_decks = int(input('Enter the number of decks to add to the simulation: '))
            # datagen:
            make_decks(num_new_decks)
            # dataproc:
            seed = get_next_seed() - 1
            raw = DECKS_FOLDER / f'decks_seed_{seed}.npy'
            process_decks(raw)
            # datavis - doesn't display the heatmaps, just makes them
            make_all_heatmaps()
        elif user_choice == '3':
            # quit simulation
            break
        else:
            print('Invalid input.')
    


if __name__ == '__main__':
    main()