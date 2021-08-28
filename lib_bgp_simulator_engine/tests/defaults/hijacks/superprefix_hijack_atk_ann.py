from .prefix_hijack_atk_ann import PrefixHijackAtkAnn

from ...roa_validity import ROAValidity


class SuperprefixHijackAtkAnn(PrefixHijackAtkAnn):
    """Superprefix of a hijack. ROA validity is unknown, not invalid"""

    def __init__(self, prefix=Prefixes.SUPERPREFIX.value, **kwargs)
        super(self.__class__, self).__init__(prefix=prefix,
                                             roa_validity=ROAValidity.UNKNOWN,
                                             **kwargs)
