from itertools import combinations


class State:
    def __init__(self, players, game_state):
        self._f = 0  # f timh
        self._h = 0  # timh euretikhs
        self._g = 0  # kostos apo tin riza mexri auto to state
        self._father = None
        self._total_time = 0  # diathesimos xronos
        self.player_states = [{'name': player['name'], 'speed': player['speed'], 'side': player['side']} for player in
                              players]
        self.game_state = game_state  # AtoB h BtoA pros ta pou kinoumaste meta apo auto to state
        self.children = []
        self.hash = None

    @property
    def f(self):
        return self._f

    @property
    def g(self):
        return self._g

    @property
    def h(self):
        return self._h

    @property
    def father(self):
        return self._father

    @property
    def total_time(self):
        return self._total_time

    @f.setter
    def f(self, f):
        self._f = f

    @g.setter
    def g(self, g):
        self._g = g

    @h.setter
    def h(self, h):
        self._h = h

    @father.setter
    def father(self, f):
        self._father = f

    @total_time.setter
    def total_time(self, time):
        self._total_time = time

    def print_state(self):  # synartisi pou xrisimopoieitai gia euanagnosti ektypwsh tou path
        for player in self.player_states:
            print(f"{player['name']} side -> {player['side']}",
                  end=' | ')  # Parametros end pou mou epitrepei na typothoun ta iterates tou for se ena line me keno
        print()
        print(f"State values : Cost -> {self.g} minutes / Heuristic value -> {self.h} / f value -> {self.f}")
        print(f"Time remaining = {self.total_time} minutes \n", )

    def get_state(self):
        return self.player_states

    def get_children(self):
        if not self.children:
            self.children = self.generate_children()  # An den exoun dhmiourghthei ta paidia, ta dhmiourgei
        return self.children

    def change_state(self):
        if self.game_state == "AtoB":
            return "BtoA"
        elif self.game_state == "BtoA":
            return "AtoB"

    def generate_children(self):
        possible_moves = []
        outcomes = []
        if self.game_state == "AtoB":
            players_on_A = [player for player in self.player_states if
                            player["side"] == "A"]  # Oi paiktes pou einai sto A
            if len(players_on_A) > 1:
                comb = combinations(players_on_A, 2) # Oi sunduasmoi twn paiktwn pou mporoun na metakinithoun
                for combin in comb:
                    possible_moves.append(list(combin))  # Prosthiki twn sunduasmwn sthn lista possible_moves
            else:
                possible_moves = players_on_A  # An exoume mono enan paikth, o monos sunduasmos einai o paikths
            for possible_move in possible_moves:
                current_state_copy = [player.copy() for player in self.player_states]  # Copy kathe current state
                for possible_player in possible_move:  # Gia kathe paikth pou tha metakinithei
                    for player in current_state_copy:  # Gia kathe paikth sto current state
                        if possible_player["name"] == player["name"]:
                            player["side"] = "B"  # Allagh tou side tou paikth pou tha metakinithei
                outcomes.append(current_state_copy)  # Prosthiki tou neou state sthn lista me ta outcomes
        elif self.game_state == "BtoA":
            players_on_B = [player for player in self.player_states if
                            player["side"] == "B"]  # Oi paiktes pou einai sto B
            possible_moves = players_on_B  # An exoume mono enan paikth, o monos sunduasmos einai o paikths
            for possible_player in possible_moves:
                current_state_copy = [player.copy() for player in self.player_states]
                for player in current_state_copy:
                    if possible_player["name"] == player["name"]:
                        player["side"] = "A"  # Allagh tou side tou paikth pou tha metakinithei
                outcomes.append(current_state_copy)  # Prosthiki tou neou state sthn lista me ta outcomes
        return outcomes  # Epistrofh olwn twn outcomes

    def is_final(self):
        for player in self.player_states:  # An kapoios paikths einai sto A, den einai teliko state
            if player['side'] == "A":
                return False
        return True

    def calculate_heuristic(self, game_state):
        persons_A_side = [player for player in self.player_states if player['side'] == 'A']  # Oi paiktes pou einai sto A
        persons_B_side = [player for player in self.player_states if player['side'] == 'B']
        if len(persons_A_side) == 0:  # Periptwsh final state
            self.h = 0
        elif len(persons_B_side) == 0:  # Periptwsh initial state
            self.h = self.total_time
        else:
            # Ypologismos tou megistou xronou apo tous paiktes poy einai sthn A
            max_time_A_side = max(player['speed'] for player in persons_A_side)

            # Ypologismos tou elaxistou xronou apo tous paiktes poy einai sthn B
            min_time_B_side = min(player['speed'] for player in persons_B_side)

            if game_state == 'AtoB':
                self.h = max_time_A_side  # perissotera gia tin logiki ths heuristic function sto report !!!
            elif game_state == 'BtoA':
                self.h = max_time_A_side + min_time_B_side

    def __eq__(self, other):
        if isinstance(other, State):  # An einai instance ths klashs State
            return hash(self) == hash(other)  # An ta hash einai idia, ta states einai idia
        return False

    def __hash__(self):
        if self.hash is None:  # An den exei ypologistei to hash
            self.hash = hash((self.f, self.game_state, self.total_time, self.h, self.g))  # Ypologismos tou hash
        return self.hash  # Epistrofh tou hash