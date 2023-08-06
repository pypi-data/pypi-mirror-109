from hein_robots.kinova.kortex import KortexConnection


class KinovaGripper:
    def __init__(self, connection: KortexConnection):
        self.connection = connection

    