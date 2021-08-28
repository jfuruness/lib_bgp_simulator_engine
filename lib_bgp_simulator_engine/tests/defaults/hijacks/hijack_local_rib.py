from .prefix_hijack_vic_ann import PrefixHijackVicAnn
from .prefix_hijack_atk_ann import PrefixHijackAtkAnn
from .subprefix_hijack_atk_ann import SubprefixHijackAtkAnn
from .superprefix_hijack_atk_ann import SuperprefixHijackAtkAnn
from ..enums import ASNs
from ....local_rib import LocalRib


class HijackLocalRib(LocalRib):
    """Local Rib for Subprefix Hijack for easy test writing"""

    def __init__(self,
                 prefix_as_path=None,
                 superprefix_as_path=None,
                 subprefix_as_path=None):
        super(HijackLocalRib, self).__init__()
        anns = []
        if prefix_as_path:
            if ASNs.VICTIM.value in prefix_as_path:
                AnnCls = PrefixHijackVicAnn
            else:
                AnnCls = PrefixHijackAtkAnn
            anns.append(AnnCls(as_path=prefix_as_path))
        if superprefix_as_path:
            anns.append(SuperprefixHijackAthAnn(as_path=superprefix_as_path))
        if subprefix_as_path:
            anns.append(SubprefixHijackAtkAnn(as_path=subprefix_as_path))

        self.prefix_ann_dict = {ann.prefix: ann for ann in anns}
