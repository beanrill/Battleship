class ShipGame:
    """A class representing the Battleship game"""

    def __init__(self):
        """A constructor for the ShipGame class. Takes no parameters."""
        self._board1 = []
        self._board2 = []
        self._current_turn = "first"
        self._current_state = "UNFINISHED"
        self._ships1 = []
        self._ships2 = []
        # Change alpha coordinates into numerical indices
        self._letter_to_num = dict((letter, number) for number, letter in enumerate(['A', 'B', 'C', 'D', 'E', 'F', 'G',
                                                                                     'H', 'I', 'J']))
        # Create board
        for row in range(11):
            self._board1.append(["0"] * 10)
            self._board2.append(["0"] * 10)
        # Set up should look something like:
        #   1 2 3 4 5 6 7 8 9 10
        # A 0 0 0 0 0 0 0 0 0 0
        # B 0 0 0 0 0 0 0 0 0 0
        # C 0 0 0 0 0 0 0 0 0 0
        # D 0 0 0 0 0 0 0 0 0 0
        # E 0 0 0 0 0 0 0 0 0 0
        # F 0 0 0 0 0 0 0 0 0 0
        # G 0 0 0 0 0 0 0 0 0 0
        # H 0 0 0 0 0 0 0 0 0 0
        # I 0 0 0 0 0 0 0 0 0 0
        # J 0 0 0 0 0 0 0 0 0 0

    def get_current_state(self):
        """Gets current state of the game."""
        return self._current_state

    def get_num_ships_remaining(self, player):
        """
        Gets how many ships the player has left on their board.

        :param player: either 'first' or 'second'
        """
        board = self._board1
        ships = self._ships1
        if player == "second":
            board = self._board2
            ships = self._ships2

        count = 0
        # Check if ship is alive
        for ship in ships:
            for row, column in ship:
                if board[row][column] == 'x':
                    count += 1
                    break
        return count

    def place_ship(self, player, ship_len, coordinates, orientation):
        """
        Player chooses a ship and places ship on their board using coordinates and ship orientation.
        Validates player's ship placement.

        :param player: either 'first' or 'second'
        :param ship_len: length of ship that is at minimum a length of 2
        :param coordinates: a string of two elements with the first being A-J and the second 1-10
        :param orientation: orientation of ship placement, 'R' for horizontal and 'C' for vertical
        """
        # Valid ship length
        if ship_len < 2:
            return False

        # Get coordinates
        row = self._letter_to_num[coordinates[0]]
        column = int(coordinates[1:]) - 1

        # If row or column are less than 0, it's out of bounds
        if row < 0 or column < 0:
            return False

        # Check if ship will go out of bounds
        if orientation == 'R' and ship_len + column > 11:
            return False
        if orientation == 'C' and ship_len + row > 11:
            return False

        # Assign the board to the correct player
        board = self._board1
        ships = self._ships1
        if player == "second":
            board = self._board2
            ships = self._ships2

        # Check player's ship does not overlap with preexisting one
        if orientation == 'R':
            for c in range(column, ship_len + column):
                if board[row][c] == 'x':
                    return False
        else:
            for r in range(row, ship_len + row):
                if board[r][column] == 'x':
                    return False

        # Holds the coordinates of ship placement
        new_ship = []
        # Valid ship placement
        if orientation == "R":
            for c in range(column, ship_len + column):
                board[row][c] = "x"
                new_ship.append((row, c))
        else:
            for r in range(row, ship_len + row):
                board[r][column] = "x"
                new_ship.append((r, column))
        ships.append(new_ship)
        return True

    def fire_torpedo(self, player, coordinates):
        """
        Player fires torpedo on opposing player's board.

        :param player: either 'first' or 'second'
        :param coordinates: a string of two elements with the first being A-J and the second 1-10
        """
        # Get coordinates
        row = self._letter_to_num[coordinates[0]]
        column = int(coordinates[1:]) - 1

        # Not the player's turn
        if self._current_turn != player:
            return False
        # A player has already won
        if self._current_state == "FIRST_WON" or self._current_state == "SECOND_WON":
            return False

        # Record the move, update turn, update current state, then return true
        if self._current_turn == "first":
            # Successful hit on ship
            if self._board2[row][column] == "x":
                self._board2[row][column] = "0"
            # If number of ships remaining of opponent is 0, first player won
            if self.get_num_ships_remaining("second") == 0:
                self._current_state = "FIRST_WON"
            # Update turn
            self._current_turn = "second"
            return True
        else:
            # Successful hit on ship
            if self._board1[row][column] == "x":
                self._board1[row][column] = "0"
            # If number of ships remaining of opponent is 0, second player won
            if self.get_num_ships_remaining("first") == 0:
                self._current_state = "SECOND_WON"
            # Update turn
            self._current_turn = "first"
            return True