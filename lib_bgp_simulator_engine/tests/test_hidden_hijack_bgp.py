from .default_enums import ASNs, ASTypes, Timestamps, Prefixes
from .subprefix_hijack_defaults import subprefix_hijack_announcements
from .subprefix_hijack_defaults import SubprefixHijackLocalRib as SubHjLocalRib


from ..announcement import Announcement
from ..bgp_as import BGPAS


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
        1: SubHjLocalRib(vic_as_path=[1, 2, ASNs.VICTIM.value])
        2: SubHjLocalRib(vic_as_path=[2, ASNs.VICTIM.value],
                                   atk_as_path=[2, 3, ASNs.ATTACKER.value])
        3: SubHjLocalRib(vic_as_path=[3, 2, ASNs.VICTIM.value],
                                   atk_as_path=[3, ASNs.ATTACKER.value])
        ASNs.VICTIM.value: SubHjLocalRib(vic_as_path=[ASNs.VICTIM.value])
        ASNs.ATTACKER.value: SubHjLocalRib(vic_as_path=[ASNs.VICTIM.value])
    }

    run_example(tmp_path,
                peers=peers,
                customer_providers=customer_providers,
                as_types=as_types,
                as_classes_dict=as_classes_dict,
                announcements=subprefix_hijack_announcements,
                local_ribs=local_ribs)
