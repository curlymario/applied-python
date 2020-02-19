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

    def insert(self, text, pos=-1) -> int:
        """
        вставить текст с позиции pos (по умолчанию — конец строки).
        Кидает ValueError, если указана недопустимая позиция.
        Возвращает номер новой версии.
        """
        action = InsertAction(pos=pos, text=text, from_version=self._version, to_version=self._version + 1)
        self._actions.append(action)
        self._text = action.apply(self._text)
        self._version += 1
        return self._version

    def replace(self, text, pos=-1) -> int:
        """
        заменить текст с позиции pos (по умолчанию — конец строки).
        Кидает ValueError, если указана недопустимая позиция.
        Замена за пределами строки работает как вставка (т. е. текст дописывается).
        Возвращает номер новой версии
        """
        action = ReplaceAction(pos=pos, text=text, from_version=self._version, to_version=self._version + 1)
        self._actions.append(action)
        self._text = action.apply(self._text)
        self._version += 1
        return self._version

    def delete(self, pos, length) -> int:
        """
        удаляет length символов начиная с позиции pos.
        Возвращает номер новой версии.
        """
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
        self._actions.append(action)
        self._text = action.apply(self._text)
        self._version = action.to_version
        return self.version

    def get_actions(self, from_version=0, to_version=-1) -> list:
        """
        возвращает list всех действий между двумя версиями
        """
        return self._actions[from_version:to_version]


class Action:
    """
    Конструктор принимает позицию (pos) и строку (text) или позицию и длину (length),
    а так же стартовую и конечную версию.
    Если версии указаны неверно, кидается ValueError.
    Единственный публичный метод apply принимает строку и возвращает модифицированную строку.
    """
    def __init__(self, pos=-1, text='', length=0, from_version=0, to_version=-1):
        self.pos = pos
        self.text = text
        self.length = length
        self.from_version = from_version
        self.to_version = to_version

    def apply(self, str):
        self._check_pos(self.pos, str)
        return self._action(str)

    def _check_pos(self, pos, str):
        if not isinstance(pos, int):
            raise ValueError('Position must be integer')
        if pos < 0 and pos != -1:
            raise ValueError("""Please use "-1" or skip `pos` argument to work with the end of string.
                             Otherwise, use positive integer for `pos` argument""")
        if len(str) < pos:
            raise ValueError('Text is smaller than the suggested position')


class InsertAction(Action):
    def _action(self, original_text):
        return original_text


class ReplaceAction(Action):
    def _action(self, original_text):
        return original_text


class DeleteAction(Action):
    def _action(self, original_text):
        return original_text
