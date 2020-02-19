class Player:
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name


class Match:
    def __init__(self, holes, players):
        self._holes = holes
        self._players = players

        self._finished = False
        self._current_hole = 0
        self._current_player = 0
        for player in self._players:
            player.hits = 0

        self._table = [[player.name for player in players]]+[[None]*len(players) for _ in range(holes)]
        self._winners = set()


    def hit(self, success=False):
        """
        сообщает матчу, что произошел очередной удар.
        Кидает RuntimeError, если матч завершен.
        success — булево значение, указываюшее, попал ли матч в лунку (по умолчанию False).
        """
        if self.finished:
            raise RuntimeError('Матч завершён')

        self._hit(success)

        self._current_player += 1
        if self._current_player == len(self._players):
            self._current_player = 0


    @property
    def finished(self):
        """
        True — матч закончен, False — нет
        """
        return self._finished

    def get_winners(self):
        """
        возвращает массив победителей в том же порядке, в которым игроки были переданы в конструктор.
        Кидает RuntimeError, если матч еще не завершен.
        """
        if not self.finished:
            raise RuntimeError('Матч ещё идёт')
        else:
            return tuple(player.name for player in self._players if player in self._winners)

    def get_table(self):
        """
        возвращает таблицу результатов.
        Это list, в котором содержится H + 1 tuple-ов.
        Первый — имена игроков, остальные — очки игроков на соответсвующих лунках.
        Если результата еще нет, то tuple содержит None
        (причем, если игрок совершил 3 удара, но еще не забил, то это все еще None, а не 3).
        """
        return [tuple(item for item in line) for line in self._table]


class HitsMatch(Match):
    """
    Игра на очки
    Лунка играется до тех пор, пока все игроки не забили свой мяч.
    Игроки, уже забившие, пропускают свой удар.
    Каждый игрок получает столько очков, сколько ударов он потратил (соответственно, чем меньше очков, тем лучше).
    Десятый удар защитывается автоматически, игрок получает 10 очков, удар не требуется.
    """
    def _hit(self, success):
        pass


class HolesMatch(Match):
    """
    Игра на лунки
    Все игроки делают по одному удару.
    Если никто не забил, делают еще один круг.
    Если хоть кто-то забил, то забившие получают 1 очко, промахнувшиеся – 0 очков, лунка более не разыгрывается.
    Если за десять таких кругов никто не забил, все получают 0 очков и переходят к следующей лунке.
    """
    def _hit(self, success):
        pass
