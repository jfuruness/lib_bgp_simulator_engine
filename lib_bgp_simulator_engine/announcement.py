from .relationships import Relationships


class Announcement:
    """MRT Announcement"""

    def __init__(self,
                 prefix=None,
                 timestamp=None,
                 as_path=None,
                 roa_validity=None):
        self.prefix = prefix
        self.timestamp = timestamp
        if as_path:
            self.as_path = as_path
        # Tuples are faster
        assert isinstance(self.as_path, tuple)
        self.roa_validity = roa_validity
        # Where the announcement came from
        self.recv_relationship = Relationships.SEEDED
        self.priority = None

    def __lt__(self, other):
        assert isinstance(other, Announcement)
        assert isinstance(self.priority, int)
        assert isinstance(other.priority, int)

        return self.priority < other.priority
        
    def seed(self, as_dict):
        """Seeds announcement at the proper AS

        Since this is the simulator engine, we should
        never have to worry about overlapping announcements
        """

        as_dict[self.origin].local_rib[self.prefix] = self

    def __eq__(self, other):
        """Checks if two announcements are equal"""

        if isinstance(other, Announcement):
            return vars(self) == vars(other)
        raise NotImplementedError

    @property
    def origin(self):
        return self.as_path[-1]
