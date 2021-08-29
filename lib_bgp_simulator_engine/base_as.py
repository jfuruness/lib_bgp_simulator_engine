from .incoming_anns import IncomingAnns
from .local_rib import LocalRib
from .relationships import Relationships

class AS:
    """Autonomous System class. Contains attributes of an AS"""

    __slots__ = ["asn", "rank", Relationships.PEERS.name.lower(),
                 Relationships.CUSTOMERS.name.lower(),
                 Relationships.PROVIDERS.name.lower(),
                 "ixp", "local_rib", "incoming_anns",
                 "input_clique"]

    def __init__(self,
                 asn: int = None,
                 rank: int = None,
                 peer_asns=list(),
                 customer_asns=list(),
                 provider_asns=list(),
                 input_clique=False,
                 ixp=False,
                 **kwargs):
        self.asn: int = asn
        # Rank of that AS. Not to be confused with AS rank
        self.rank: int = rank
        # Note that these must be the same names. Propogation function
        # in the BGP AS depend on it
        setattr(self, Relationships.PEERS.name.lower(), peer_asns)
        setattr(self, Relationships.CUSTOMERS.name.lower(), customer_asns)
        setattr(self, Relationships.PROVIDERS.name.lower(), provider_asns)
        # Caida says that there is a known clique at the top of the AS graph
        self.input_clique: bool = input_clique
        # Caida hand selects a few IXPs
        self.ixp: bool = ixp
        self.local_rib = LocalRib()
        self.incoming_anns = IncomingAnns()

        assert hasattr(self, "propogate_to_peers")
        assert hasattr(self, "propogate_to_customers")
        assert hasattr(self, "propogate_to_providers")
        assert hasattr(self, "process_incoming_anns")

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
