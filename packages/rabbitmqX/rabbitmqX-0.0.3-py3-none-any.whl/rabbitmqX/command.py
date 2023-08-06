class Command(Object):
    
    @abstractmethod
    def do(self, data): raise NotImplementedError