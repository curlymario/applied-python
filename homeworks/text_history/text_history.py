class TextHistory:
    def __init__(self):
        self._text = ''
        self._version = 0
        self._actions = []

    @property
    def text(self) -> str:
        """
        возвращает текущий текст, read only
        """
        return self._text

    @property
    def version(self) -> int:
        """
        возвращает текущую версия, read only
        """
        return self._version

    def _check_versions(self, from_version, to_version, history=False):
        if to_version is not None:
            if from_version > to_version:
                raise ValueError('Wrong version order')
            if to_version < 0:
                raise ValueError('Version can not be negative')
            if history and to_version > len(self._actions):
                raise ValueError('Incorrect `to_version` — no such version')
        if from_version < 0:
            raise ValueError('Version can not be negative')
        if from_version > self._version:
            raise ValueError('Incorrect `from_version` — no such version')

    def _check_pos(self, pos, length=None):
        if pos is None:
            pos = len(self._text)
            return pos
        if pos is not None:
            if not isinstance(pos, int):
                raise ValueError('Position must be integer')
            if pos < 0:
                raise ValueError("""Please skip `pos` argument to work with the end of string.
                                 Otherwise, use positive integer for `pos` argument""")
            if len(self._text) < pos:
                raise ValueError('No such `pos`. Text is smaller than the suggested position')
            if length is not None:
                if pos + length > len(self._text):
                    raise ValueError('No such text. Delete size is to big or outside the text')
        return pos

    def insert(self, text, pos=None) -> int:
        """
        вставить текст с позиции pos (по умолчанию — конец строки).
        Кидает ValueError, если указана недопустимая позиция.
        Возвращает номер новой версии.
        """
        pos = self._check_pos(pos)
        action = InsertAction(pos=pos, text=text, from_version=self._version, to_version=self._version + 1)
        self._actions.append(action)
        self._text = action.apply(self._text)
        self._version += 1
        return self._version

    def replace(self, text, pos=None) -> int:
        """
        заменить текст с позиции pos (по умолчанию — конец строки).
        Кидает ValueError, если указана недопустимая позиция.
        Замена за пределами строки работает как вставка (т. е. текст дописывается).
        Возвращает номер новой версии
        """
        pos = self._check_pos(pos)
        action = ReplaceAction(pos=pos, text=text, from_version=self._version, to_version=self._version + 1)
        self._actions.append(action)
        self._text = action.apply(self._text)
        self._version += 1
        return self._version

    def delete(self, pos=None, length=0) -> int:
        """
        удаляет length символов начиная с позиции pos.
        Возвращает номер новой версии.
        """
        pos = self._check_pos(pos, length)
        action = DeleteAction(pos=pos, length=length, from_version=self._version, to_version=self._version + 1)
        self._actions.append(action)
        self._text = action.apply(self._text)
        self._version += 1
        return self._version

    def action(self, action) -> int:
        """
        применяет действие action.
        Возвращает номер новой версии.
        Версия растет не на 1, а устанавливается та, которая указана в action
        """
        self._check_versions(action.from_version, action.to_version)
        self._actions.append(action)
        self._text = action.apply(self._text)
        self._version = action.to_version
        return self.version

    def get_actions(self, from_version=0, to_version=None) -> list:
        """
        возвращает list всех действий между двумя версиями
        Если версии указаны неверно, кидается ValueError
        """
        self._check_versions(from_version, to_version, history=True)
        if to_version is not None:
            return self._actions[from_version:to_version]
        else:
            return self._actions[from_version:]


class Action:
    """
    Конструктор принимает позицию (pos) и строку (text) или позицию и длину (length),
    а так же стартовую и конечную версию.
    Если версии указаны неверно, кидается ValueError.
    Единственный публичный метод apply принимает строку и возвращает модифицированную строку.
    """
    def __init__(self, pos=None, text='', length=0, from_version=0, to_version=None):
        self.pos = pos
        self.text = text
        self.length = length
        self.from_version = from_version
        self.to_version = to_version

    def apply(self, string):
        return string


class InsertAction(Action):
    def apply(self, original_text):
        if self.pos is None:
            new_text = ''.join([original_text, self.text])
        else:
            new_text = ''.join([original_text[:self.pos], self.text, original_text[self.pos:]])
        return new_text


class ReplaceAction(Action):
    def apply(self, original_text):
        if self.pos is None:
            new_text = ''.join([original_text, self.text])
        else:
            end_pos = self.pos + len(self.text)
            if end_pos > len(original_text):
                new_text = ''.join([original_text[:self.pos], self.text])
            else:
                new_text = ''.join([original_text[:self.pos], self.text, original_text[end_pos:]])
        return new_text


class DeleteAction(Action):
    def apply(self, original_text):
        if self.length == 0:
            return original_text
        else:
            new_text = ''.join([original_text[:self.pos], original_text[(self.pos + self.length):]])
            return new_text
