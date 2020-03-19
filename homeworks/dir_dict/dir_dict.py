class DirDict(dict):
    def __init__(self, working_dir, *args, **kwargs):
        self._dir = working_dir
        self.update(*args, **kwargs)

    def __getitem__(self, key):
        file = open('/'.join((self._dir, key)), 'r')
        value = file.read()
        file.close()
        return value

    def __setitem__(self, key, value):
        file = open('/'.join((self._dir, key)), 'w')
        file.write(value)
        file.close()

    def __delitem__(self, key):
        pass

    def __contains__(self):
        pass

    def __iter__(self):
        pass

    def __len__(self):
        pass

    def __eq__(self):
        pass

    def __ne__(self):
        pass

    def __repr__(self):
        pass

    def __str__(self):
        pass

    def __hash__(self):
        pass

    def clear(self):
        pass

    def copy(self):
        pass

    def fromkeys(self):
        pass

    def get(self):
        pass

    def items(self):
        pass

    def keys(self):
        pass

    def pop(self):
        pass

    def popitem(self):
        pass

    def setdefault(self):
        pass

    def update(self, *args, **kwargs):
        for key, value in dict(*args, **kwargs).iteritems():
            self[key] = value

    def values(self):
        pass
