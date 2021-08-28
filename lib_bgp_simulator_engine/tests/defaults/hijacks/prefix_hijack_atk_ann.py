from .defaults import ASNs, Prefixes, Timestamps
from ...announcement import Announcement
from ...roa_validity import ROAValidity


class PrefixHijackAtkAnn(Announcement):
    """Default subprefix hijack attacker announcement"""

    def __init__(self,
                 prefix=Prefixes.PREFIX.value,
                 timestamp=Timestamps.ATTACKER.value,
                 as_path=(ASNs.ATTACKER.value,),
                 roa_validity=ROAValidity.INVALID):
        super(SubprefixHijackAtkAnn, self).__init__(prefix=prefix,
                                                    timestamp=timestamp,
                                                    as_path=as_path,
                                                    roa_validity=roa_validity)
