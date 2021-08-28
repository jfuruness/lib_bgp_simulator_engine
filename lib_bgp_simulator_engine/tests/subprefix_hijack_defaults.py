from .defaults import ASNs, Prefixes, Timestamps
from ..local_rib import LocalRib
from ..roa_validity import ROAValidity


subprefix_hijack_announcements = [SubprefixHijackVicAnn(),
                                  SubprefixHijackAtkAnn()]

class SubprefixHijackVicAnn(Announcement):
    """Default subprefix hijack victim announcement"""

    def __init__(self,
                 prefix=Prefixes.VICTIM.value,
                 timestamp=Timestamps.VICTIM.value,
                 as_path=[ASNs.VICTIM.value],
                 roa_validity=ROAValidity.VALID):
        super(SubprefixHijackVicAnn, self).__init__(prefix=prefix,
                                                    timestamp=timestamp,
                                                    as_path=as_path,
                                                    roa_validity=roa_validity)

class SubprefixHijackAtkAnn(Announcement):
    """Default subprefix hijack attacker announcement"""

    def __init__(self,
                 prefix=Prefixes.ATTACKER.value,
                 timestamp=Timestamps.ATTACKER.value,
                 as_path=[ASNs.ATTACKER.value],
                 roa_validity=ROAValidity.INVALID):
        super(SubprefixHijackAtkAnn, self).__init__(prefix=prefix,
                                                    timestamp=timestamp,
                                                    as_path=as_path,
                                                    roa_validity=roa_validity)


class SubprefixHijackLocalRib(LocalRib):
    """Local Rib for Subprefix Hijack for easy test writing"""

    def __init__(self, vic_as_path=None, atk_as_path=None):
        super(SubprefixHijackLocalRib, self).__init__()
        announcements = []
        if vic_as_path:
            announcements.append(SubprefixHijackVicAnn(as_path=vic_as_path))
        if atk_as_path:
            announcements.append(SubprefixHijackAtkAnn(as_path=atk_as_path)

        self.prefix_ann_dict = {ann.prefix: ann for ann in announcements}
