class TurnTracker:
    def __init__(self, num_players):
        self.num_players = num_players
        self.current_player = 1
        self.current_turn = 1

    def next_turn(self):
        self.current_player = self.current_turn % self.num_players + 1
        self.current_turn += 1

    def get_current_player(self):
        return self.current_player

    def get_current_turn(self):
        return self.current_turn


turn_tracker = TurnTracker(3)
for i in range(10):
    print(f'Current Player: {turn_tracker.get_current_player()}')
    print(f'Current Turn: {turn_tracker.get_current_turn()}')
    turn_tracker.next_turn()
