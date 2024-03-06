from state import State


class Tree_Generator:
    def __init__(self):
        self.path = []  # to beltisto path pou briskei o algorithmos
        self.open_set = []  # metwpo anazitisis
        self.closed_set = set()  # kleisto synolo

    def calculate_cost(self, current_state):
        players_in_current_state = current_state.get_state()  # Oi paixtes pou einai sto current state

        if current_state.father is not None:  # An den einai to arxiko state
            players_in_father_state = current_state.father.get_state()
            different_side_players = [player for player in players_in_current_state if
                                      player not in players_in_father_state]  # Oi paixtes pou metakinithikan
            max_speed = max(player['speed'] for player in
                            different_side_players)  # O megistos xronos twn paixtwn pou metakinithikan
            current_state.g = max_speed + current_state.father.g
            current_state.total_time = current_state.father.total_time - max_speed  # xronos pou mas menei stin diathesi mas
            current_state.calculate_heuristic(current_state.game_state)  # Ypologismos heuristic tou current state
            current_state.f = current_state.g + current_state.h  # f = g + h
        else:
            current_state.calculate_heuristic(current_state.game_state)  # periptosi initial state

    def generate_path(self, current_state):
        if not self.open_set:
            self.open_set.append(current_state)  # Arxikopoihsh me to starting_state
            self.calculate_cost(current_state)  # ypologismos f g h gia initial state
        self.closed_set.add(current_state)  # Prosthiki tou current state sto kleisto synolo
        outcomes = current_state.get_children()  # Ta paidia tou current state
        game_state = current_state.change_state()  # To neo game state
        for outcome in outcomes:  # Dhmiourgia states gia kathe outcome, kai eisagwgh tous sto open set
            new_state = State(outcome, game_state)
            new_state.father = current_state
            self.open_set.append(new_state)
        self.open_set.remove(current_state)  # Afairesi tou current state apo to open set
        current_state = self.astar_helper()  # Epilogh tou neou current state (ousiastika ginetai sort to metwpo kai epilegoume to proto apo to openset)
        if current_state.is_final():  # An to current state einai to teliko state
            if current_state.total_time < 0:  # An eimaste ektos xronikou oriou
                print("No solution found!")
            else:  # An vrethike lisi entos tou xronou epistrefoume to path tis beltistis lyshs
                while True:
                    self.path.append(current_state)
                    if current_state.father is None:
                        break
                    current_state = current_state.father

                print("Solution found!")
                finalPath = self.path[::-1]  # Antistrofh ths listas me ta states

                for node in finalPath:  # Ektypwsh tou path
                    print("~~~~>", end=' ')
                    node.print_state()
                print()
                print(f"The time limit was {finalPath[0].total_time} minutes")
                print(
                    f"A* algorithm found as best solution the path above with a total crossing time of {finalPath[-1].g} minutes")
            return
        else:  # An den einai to teliko state
            if current_state not in self.closed_set:  # an to current_state den uparxei sto kleisto synolo sunexizoume
                self.generate_path(current_state)
            else:  # ama uparxei tote
                self.open_set.remove(current_state)  # aferese to apo to metwpo anazitisis
                for state in self.open_set:
                    if state not in self.closed_set:  # kai bres to epomeno state pou den uparxei sto kleisto synolo kai sunexise
                        self.generate_path(state)
                        break

    def astar_helper(self):
        for state in self.open_set:  # Ypologismos tou f gia kathe state tou open set
            self.calculate_cost(state)
        cost_of_open_set = [state.f for state in self.open_set]  # Lista me ta f twn states tou open set
        min_cost = min(cost_of_open_set)  # To min f
        min_cost_index = cost_of_open_set.index(min_cost)  # To index tou min f
        return self.open_set[min_cost_index]