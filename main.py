from src.datagen import make_decks, get_next_seed, DECKS_FOLDER
from src.dataproc import process_decks
from src.datavis import make_all_heatmaps, show_heatmaps

def main():
    # make_decks for first time, 1000000 decks?
    make_decks(10)
    seed = get_next_seed() - 1
    raw = DECKS_FOLDER / f'decks_seed_{seed}.npy'
    process_decks(raw)
    path_to_heatmaps = make_all_heatmaps()

    user_choice = 0
    while user_choice != '3':
        # num_decks_generated = get_deck_count() --> make some sort of function to count decks
        # print(f'There are currently {num_decks_generated} generated.')
        user_choice = input('Enter 1 to display heatmaps, 2 to add more decks to the simulation, or 3 to quit: ')
        if user_choice == '1':
            print('Generating heatmaps...')
            # datavis
            #make_all_heatmaps()
            show_heatmaps(path_to_heatmaps)
        elif user_choice == '2':
            num_new_decks = int(input('Enter the number of decks to add to the simulation: '))
            # datagen:
            make_decks(num_new_decks)
            # dataproc:
            seed = get_next_seed() - 1
            raw = DECKS_FOLDER / f'decks_seed_{seed}.npy'
            process_decks(raw)
            #print updated number of decks generated 
            # datavis - doesn't display the heatmaps, just makes them
            make_all_heatmaps()
        elif user_choice == '3':
            # quit simulation
            break
        else:
            print('Invalid input.')
    


if __name__ == '__main__':
    main()