import csv

from lib_caida_collector import CaidaCollector

from .defaults import SubprefixHijackAtkAnn, PrefixHijackVicAnn
from .utils import CustomerProviderLink, PeerLink, run_example

def test_proof_of_concept(tmp_path):
    collector = CaidaCollector()
    collector.run()
    path = collector.tsv_path

    peers = set()
    cps = set()

    with open(path, "r") as f:
        reader = csv.DictReader(f, delimiter="\t")
        asns = []
        for row in reader:
            asns.append(int(row["asn"]))
            if row["peers"] == "{}":
                row_peers = []
            else:
                row_peers = [int(x) for x in row["peers"][1:-1].split(",")]
            if row["customers"] == "{}":
                row_customers = []
            else:
                row_customers = [int(x) for x in row["customers"][1:-1].split(",")]
            if row["providers"] == "{}":
                row_providers = []
            else:
                row_providers = [int(x) for x in row["providers"][1:-1].split(",")]

            for peer in row_peers:
                peers.add(tuple(list(sorted([int(row["asn"]), peer]))))
            for customer in row_customers:
                cps.add(tuple(list(sorted([customer, int(row["asn"])]))))
            for provider in row_providers:
                cps.add(tuple(list(sorted([int(row["asn"]), provider]))))

    peer_classes = [PeerLink(*x) for x in sorted(peers)]
    cp_classes = [CustomerProviderLink(customer=x[0], provider=x[1]) for x in sorted(cps)]
    as_types = {asn: 0 for asn in asns}
    # These ASes are mh with lots of providers
    announcements = [PrefixHijackVicAnn(as_path=(393226,)),
                     SubprefixHijackAtkAnn(as_path=(262194,))]

    run_example(tmp_path, peers=peer_classes, customer_providers=cp_classes,
                as_types=as_types, announcements=announcements)
