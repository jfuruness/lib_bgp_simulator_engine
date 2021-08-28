from .defaults import ASNs, Prefixes, Timestamps
from ...announcement import Announcement
from ...roa_validity import ROAValidity


class PrefixHijackVicAnn(Announcement):
    """Default hijack victim announcement"""

    def __init__(self,
                 prefix=Prefixes.PREFIX.value,
                 timestamp=Timestamps.VICTIM.value,
                 as_path=(ASNs.VICTIM.value,),
                 roa_validity=ROAValidity.VALID):
        super(HijackVicAnn, self).__init__(prefix=prefix,
                                           timestamp=timestamp,
                                           as_path=as_path,
                                           roa_validity=roa_validity)
