import abc

class DataInterface(object, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __str__(self):
        raise NotImplementedError('users must define __str__ to use this base class.')

class BotData(DataInterface):
    def __str__(self):
        return "Success"