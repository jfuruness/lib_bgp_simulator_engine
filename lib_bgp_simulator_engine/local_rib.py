class LocalRib:
    """Local RIB for a BGP AS

    Done separately for easy comparisons in unit testing
    """

    def __init__(self):
        """Initializes prefix to announcement map"""

        self.prefix_ann_dict = dict()

    def assert_eq(self, other):
        """Checks equality of local ribs"""

        if isinstance(other, LocalRib):
            # Done this way to get specifics about what's different
            for prefix, ann in self.prefix_ann_dict.items():
                 other.prefix_ann_dict[prefix] == ann
            for prefix, ann in other.prefix_ann_dict.items():
                assert self.prefix_ann_dict[prefix] == ann
        raise NotImplementedError
