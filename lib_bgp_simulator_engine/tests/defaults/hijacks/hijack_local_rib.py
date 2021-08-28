from .subprefix_hijack_atk_ann import SubprefixHijackAtkAnn
from .subprefix_hijack_vic_ann import SubprefixHijackVicAnn
from ..default_enums import ASNs
from ...local_rib import LocalRib


class HijackLocalRib(LocalRib):
    """Local Rib for Subprefix Hijack for easy test writing"""

    def __init__(self,
                 prefix_as_path=None,
                 superprefix_as_path=None,
                 subprefix_as_path=None):
        super(SubprefixHijackLocalRib, self).__init__()
        anns = []
        if prefix_as_path:
            if ASNs.VICTIM.value in prefix_as_path:
                ann_cls = PrefixHijackVicAnn
            else:
                ann_cls = PrefixHijackAtkAnn
            anns.append(ann_cls(as_path=prefix_as_path)
        if superprefix_as_path:
            anns.append(SuperprefixHijackAthAnn(as_path=superprefix_as_path))
        if subprefix_as_path:
            anns.append(SubprefixHijackAtkAnn(as_path=subprefix_as_path))

        self.prefix_ann_dict = {ann.prefix: ann for ann in anns}
