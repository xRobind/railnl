class Station:
    """This class creates stations with its coordinates and connections
    """

    def __init__(self, name: str, y: str, x: str) -> None:
        self.station_name: str = name
        self.station_y: str = y
        self.station_x: str = x

        self.connections_: dict[str: int] = {}

    def add_connection(self, connection: str, time: int):
        self.connections_[connection] = time