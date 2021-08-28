from ..defaults import ASNs
from ..defaults import ASTypes
from ..defaults import subprefix_hijack_announcements
from ..defaults import HijackLocalRib


from ...bgp_as import BGPAS


def test_hidden_hijack_bgp(tmp_path):
    r"""Hidden hijack example with BGP

        1
         \
         2 - 3
        /     \
       777     666
    """

    # Graph data
    peers = [[2, 3]]
    customer_providers = [[1, 2],
                          [2, ASNs.VICTIM.value],
                          [3, ASNs.ATTACKER.value]]
    # Number identifying the type of AS class
    as_types = {asn: ASTypes.BGP.value for asn in
                list(range(1, 4)) + [ASNs.VICTIM, ASNs.ATTACKER]}
    # Convert number back to AS class
    as_classes_dict = {ASTypes.BGP.value: BGPAS}

    # Local RIB data
    local_ribs = {
        1: HijackLocalRib(prefix_as_path=(1, 2, ASNs.VICTIM.value)),
        2: HijackLocalRib(prefix_as_path=(2, ASNs.VICTIM.value),
                          subprefix_as_path=(2, 3, ASNs.ATTACKER.value)),
        3: HijackLocalRib(prefix_as_path=(3, 2, ASNs.VICTIM.value),
                          subprefix_as_path=(3, ASNs.ATTACKER.value)),
        ASNs.VICTIM.value: HijackLocalRib(prefix_as_path=(ASNs.VICTIM.value,)),
        ASNs.ATTACKER.value: HijackLocalRib(subprefix_as_path=(ASNs.VICTIM.value,)),
    }

    run_example(tmp_path,
                peers=peers,
                customer_providers=customer_providers,
                as_types=as_types,
                as_classes_dict=as_classes_dict,
                announcements=subprefix_hijack_announcements,
                local_ribs=local_ribs)
