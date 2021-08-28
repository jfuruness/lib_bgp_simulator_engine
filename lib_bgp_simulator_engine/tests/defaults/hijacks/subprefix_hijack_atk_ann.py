from .prefix_hijack_atk_ann import PrefixHijackAtkAnn


class SubprefixHijackAtkAnn(PrefixHijackAtkAnn):
    def __init__(self, prefix=Prefixes.SUBPREFIX.value, **kwargs)
        super(self.__class__, self).__init__(prefix=prefix, **kwargs)
