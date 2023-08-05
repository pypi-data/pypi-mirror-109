class FootballProbabilityGrid(list):
    def __init__(self, goal_matrix):
        list.__init__(self, goal_matrix)

    def _sum(self, func):
        return sum(
            [
                self[a][b]
                for a in range(len(self))
                for b in range(len(self))
                if func(a, b)
            ]
        )

    @property
    def home_win(self):
        """
        Probability of home win

        Returns
        ------
        float
            Probability of home win
        """
        return self._sum(lambda a, b: a > b)

    @property
    def draw(self):
        """
        Probability of draw

        Returns
        ------
        float
            Probability of draw
        """
        return self._sum(lambda a, b: a == b)

    @property
    def away_win(self):
        """
        Probability of away win

        Returns
        ------
        float
            Probability of away win
        """
        return self._sum(lambda a, b: a < b)

    @property
    def home_draw_away(self):
        """
        1x2 Probabilities

        Returns
        ------
        list
            Probability of home win
        """
        return [self.home_win, self.draw, self.away_win]

    def total_goals(self, over_under, strike):
        """
        Predicts the probabilities of `total goals` market

        Parameters
        ----------
        over_under : str
            Whether probabilities are for over / under the total goals value - must be one of ['over', 'under']

        strike : float
            The total goals value for the market

        Returns
        ------
        float
            Probability of over / under the strike occurring
        """
        if over_under == "over":
            func = lambda a, b: a + b > strike
        elif over_under == "under":
            func = lambda a, b: a + b < strike
        else:
            raise ValueError("over_under must be one of ['over', 'under']")
        return self._sum(func)

    def asian_handicap(self, home_away, strike):
        """
        Predicts the probabilities of `asian handicap` market

        Parameters
        ----------
        home_away : str
            Whether probabilities are for home / away team - must be one of ['home', 'away']

        goals : float
            The total goals value

        Returns
        ------
        float
            Probability of home / away team outscoring the strike
        """
        if home_away == "home":
            func = lambda a, b: a - b > strike
        elif home_away == "away":
            func = lambda a, b: b - a > strike
        else:
            raise ValueError("home_away must be one of ['home', 'away']")
        return self._sum(func)
