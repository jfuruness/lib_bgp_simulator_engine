class LocalRib(dict):
    """Local RIB for a BGP AS

    Done separately for easy comparisons in unit testing
    """

    def assert_eq(self, other):
        """Checks equality of local ribs"""

        if isinstance(other, LocalRib):
            # Done this way to get specifics about what's different
            for prefix, ann in self.items():
                assert other[prefix] == ann
            for prefix, ann in other.items():
                assert self[prefix] == ann
        raise NotImplementedError
