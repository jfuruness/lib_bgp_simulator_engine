class AS:
    """Autonomous System class. Contains attributes of an AS"""

    def __init__(self,
                 asn: int = None,
                 rank: int = None,
                 peer_asns=list(),
                 customer_asns=list(),
                 provider_asns=list(),
                 input_clique=False,
                 ixp=False):
        self.asn: int = asn
        # Rank of that AS. Not to be confused with AS rank
        self.rank: int = rank
        self.peers: list = peer_asns
        self.customers: list = customer_asns
        self.providers: list = provider_asns
        # Caida says that there is a known clique at the top of the AS graph
        self.input_clique: bool = input_clique
        # Caida hand selects a few IXPs
        self.ixp: bool = ixp
        assert hasattr(self, "process_announcements")
        assert hasattr(self, "send_announcements")

    def __lt__(self, other):
        """Just for sorting when getting the ranks"""

        if isinstance(other, AS):
            return self.asn < other.asn
        else:
            raise NotImplementedError

    @property
    def stub(self):
        """Returns True if AS is a stub by RFC1772"""

        if len(self.peers) + len(self.customers) + len(self.providers) == 1:
            return True
        else:
            return False

    @property
    def multihomed(self):
        """Returns True if AS is multihomed by RFC1772"""

        if (len(self.customers) == 0
                and len(self.peers) + len(self.providers) > 1):
            return True
        else:
            return False

    @property
    def transit(self):
        """Returns True if AS is a transit AS by RFC1772"""

        return True if len(self.customers) > 1 else False

    @property
    def stubs(self):
        """Returns a list of any stubs connected to that AS"""

        return [x for x in self.customers if x.stub]
