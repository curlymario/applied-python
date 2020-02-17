from collections import Counter

class Message:
    DEFAULT_AUTHOR = 'UFO'

    def __init__(self, *, author=None, text):
        if author == None:
            author = self._guess_author(text)
        self._author = author
        self.text = text

    @property
    def author(self):
        return self._author

    @classmethod
    def _guess_author(cls, text):
        if text in ['bark', 'bow-wow']:
            return 'dog'

        return cls.DEFAULT_AUTHOR


class ChatHistory:
    def __init__(self):
        self._messages = []

    def new_message(self, message: Message) -> None:
        self._messages.append(message)

    def most_freq_author(self):
        counter = Counter()
        for message in self._messages:
            counter[message.author] += 1

        return max(counter.keys(), key=lambda k: counter[k])


history = ChatHistory()
history.new_message(Message(text = 'meow'))
history.new_message(Message(text = 'meow'))
history.new_message(Message(text = 'bark'))
history.new_message(Message(text = 'bow-wow'))
history.new_message(Message(author = 'dog', text = 'bark'))
history.new_message(Message(author = 'cat', text = 'meow'))

print(history.most_freq_author())