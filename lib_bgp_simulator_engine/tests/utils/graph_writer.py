import csv

class _AS:
    def __init__(self, asn):
        self.asn = asn
        self.as_type = None
        self.rank = 0
        self.peer_asns = list()
        self.customer_asns = list()
        self.provider_asns = list()

def write_graph(peers, customer_providers, as_types, path_obj):
    """Writes DAG to a TSV to be read in later"""

    # Dict of asn: as_obj
    as_dict = _generate_as_dict(peers, customer_providers, as_types)
    # Later change to logging
    print("asn, peers, customers, providers")
    for asn_obj in as_dict.values():
        print(asn_obj.asn, asn_obj.peer_asns, asn_obj.customer_asns, asn_obj.provider_asns)
    _assign_ranks(as_dict)
    with path_obj.open("w") as f:
        fieldnames = vars(list(as_dict.values())[0]).keys()
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        for x in as_dict.values():
            # https://stackoverflow.com/a/62680/8903959
            writer.writerow(vars(x)) 

def _generate_as_dict(peers, customer_providers, as_types):
    """Generates as dict"""

    as_dict = dict()

    # Add all peers to dict
    for peer_link in peers:
        p1, p2 = peer_link.ases
        as_dict[p1] = as_dict.get(p1, _AS(p1))
        as_dict[p1].peer_asns.append(p2)
        as_dict[p2] = as_dict.get(p2, _AS(p2))
        as_dict[p2].peer_asns.append(p1)
    # Add all customer providers to dict
    for cp_link in customer_providers:
        c, p = cp_link.customer, cp_link.provider
        as_dict[c] = as_dict.get(c, _AS(c))
        as_dict[c].provider_asns.append(p)
        as_dict[p] = as_dict.get(p, _AS(p))
        as_dict[p].customer_asns.append(c)

    for asn, as_obj in as_dict.items():
        as_obj.as_type = as_types[asn]
        for attr in ["peer_asns", "customer_asns", "provider_asns"]:
            # Make unique and sort
            setattr(as_obj, attr, list(sorted(set(getattr(as_obj, attr)))))

    return as_dict

def _assign_ranks(as_dict):
    """Assigns ranks to all AS objects from customers up"""

    # I know this could be done faster but idc
    # Assign ranks to ASes
    for as_obj in as_dict.values():
        _assign_ranks_helper(as_obj, 0, as_dict)

def _assign_ranks_helper(as_obj, rank, as_dict):
    """Assigns ranks to all ases in customer/provider chain recursively"""

    if as_obj.rank < rank:
        as_obj.rank = rank

    for provider_asn in as_obj.provider_asns:
        _assign_ranks_helper(as_dict[provider_asn], rank + 1, as_dict)
