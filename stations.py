class Station:
    """This class creates stations with its coordinates and connections
    """

    def __init__(self, name: str, y: str, x: str) -> None:
        self.name: str = name
        self.y: str = y
        self.x: str = x

        self.connections_: dict[str: int] = {}
#comment
    def add_connection(self, connection: str, time: int):
        self.connections_[connection] = time
        