class Connection:
    """This class creates connections
    """

    def __init__(self, station1, station2, time, connection_id = 0) -> None:
        # name and coordinates of the station
        self.station = station1
        self.connection = station2
        self.time = time
        self.corresponding = None
        self.connection_id = connection_id
        
    def add_corresponding_connection(self, corresponding):
        self.corresponding = corresponding
        