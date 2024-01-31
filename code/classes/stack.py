class Stack(object) :
    """This class creates and handles a stack.
    """
    
    def __init__ (self) -> None:
        self.items: list = []
        
    def push(self, item: all) -> None:
        self.items.append(item)
        
    def pop(self) -> all:
        assert len(self.items) >= 1
        return self.items.pop()
        
    def top(self) -> all:
        assert len(self.items) >= 1
        return self.items[len(self.items) - 1]
        
    def size(self) -> int:
        return len(self.items)