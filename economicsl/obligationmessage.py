class ObligationMessage:
    def __init__(self, sender, message) -> None:
        self.sender = sender
        self.message = message
        self._is_read = False

    def getSender(self):
        return self.sender

    def getMessage(self):
        self._is_read = True
        return self.message

    def is_read(self) -> bool:
        return self._is_read

