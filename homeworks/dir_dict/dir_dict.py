import pathlib


class DirDict():
    def __init__(self, working_dir, *args, **kwargs):
        self._dir = pathlib.Path(working_dir)
        self._dir.mkdir(parents=True, exist_ok=True)  # TODO: обработать случай, когда директория существует
        self.update(*args, **kwargs)

    def __contains__(self, key):
        return self._dir.joinpath(key).exists()

    def __getitem__(self, key):
        if self.__contains__(key):
            with self._dir.joinpath(key).open('r') as file:
                value = file.read()
            return value
        else:
            raise KeyError

    def __setitem__(self, key, value):
        path = self._dir.joinpath(key)
        if not path.exists():
            path.touch()
        with path.open('w') as file:
            file.write(str(value))

    def __delitem__(self, key):
        if self.__contains__(key):
            path = self._dir.joinpath(key)
            path.unlink()
        else:
            raise KeyError

    def __iter__(self):
        return self._dir.iterdir()

    def __len__(self):
        return len(list(self.__iter__()))

    # def __eq__(self, other):
    #     pass
    #
    # def __ne__(self, other):
    #     pass
    #
    # def __repr__(self):
    #     pass
    #
    # def __str__(self):
    #     pass
    #
    # def __hash__(self):
    #     pass

    def clear(self):
        for file in self.__iter__():
            file.unlink()

    # def copy(self):
    #     return

    # def fromkeys(self):
    #     pass

    def get(self, key, default='None'):
        if self.__contains__(key):
            return self.__getitem__(key)
        else:
            return default

    def _iter_keys(self):
        for file in self.__iter__():
            yield file.name

    def keys(self):
        return [key for key in self._iter_keys()]

    def items(self):
        return [(key, self.__getitem__(key)) for key in self._iter_keys()]

    def values(self):
        return [self.__getitem__(key) for key in self._iter_keys()]

    def pop(self, key):
        value = self.get(key, default='None')
        self.__delitem__(key)
        return value

    def popitem(self, key):
        value = self.get(key, default='None')
        self.__delitem__(key)
        return key, value

    def setdefault(self, key, default='None'):
        if not self.__contains__(key):
            self.__setitem__(key, default)

    def update(self, *args, **kwargs):
        for key, value in dict(*args, **kwargs).items():
            self[key] = value
