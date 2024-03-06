from state import State
from tree_generator import Tree_Generator

if __name__ == "__main__":
    game = int(input("Default game 30min time limit 5 players with times 1,3,6,8,12 OR make your own game (0 OR 1): "))
    players_dict = []
    total_time = 0
    if game == 0:
        players_dict = [  # Default game
            {"name": "Son", "speed": 1, "side": "A"},
            {"name": "Daughter", "speed": 3, "side": "A"},
            {"name": "Father", "speed": 6, "side": "A"},
            {"name": "Uncle", "speed": 8, "side": "A"},
            {"name": "Grandma", "speed": 12, "side": "A"},
        ]
        total_time = 30
    elif game == 1:
        N = int(input("Enter the number of players: "))
        players_dict = []  # lista gia to initial state
        for i in range(1, N + 1):
            name = input(f"Enter the name of Player {i}: ")
            speed = int(input(f"Enter the time of Player {i} to cross the bridge (min): "))
            player_info = {"name": name, "speed": speed, "side": "A"}
            players_dict.append(player_info)
        total_time = int(input("Enter the maximum allowed time to cross the bridge (min) -> "))
    starting_state = State(players_dict, "AtoB")  # Dimiourgia arxikis katastasis
    starting_state.total_time = total_time  # Arxikopoiisi total time

    execute = Tree_Generator()
    execute.generate_path(starting_state)  # Dimiourgia path