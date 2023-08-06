from abc import ABCMeta, abstractmethod
class Command():
    
    @abstractmethod
    def do(self, data): raise NotImplementedError