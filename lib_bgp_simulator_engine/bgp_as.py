from copy import deepcopy

from .announcement import Announcement as Ann
from .base_as import AS
from .incoming_anns import IncomingAnns
from .relationships import Relationships


class BGPAS(AS):
    __slots__ = []

    def propogate_to_providers(self):
        """Propogates to providers"""

        send_rels = set([Relationships.SEEDED, Relationships.CUSTOMERS])
        self._propogate(Relationships.PROVIDERS, send_rels)

    def propogate_to_customers(self):
        """Propogates to customers"""

        send_rels = set([Relationships.SEEDED,
                         Relationships.PEERS,
                         Relationships.PROVIDERS])
        self._propogate(Relationships.CUSTOMERS, send_rels)

    def propogate_to_peers(self):
        """Propogates to peers"""

        send_rels = set([Relationships.SEEDED,
                         Relationships.CUSTOMERS])
        self._propogate(Relationships.PEERS, send_rels)

    def _propogate(self, propogate_to: Relationships, send_rels: list):
        """Propogates announcements from local rib to other ASes

        send_rels is the relationships that are acceptable to send

        Later you can change this so it's not the local rib that's
        being sent. But this is just proof of concept.
        """

        for as_obj in getattr(self, propogate_to.name.lower()):
            for prefix, ann in self.local_rib.items():
                if ann.recv_relationship in send_rels:
                    incoming_anns = as_obj.incoming_anns.get(prefix, [])
                    incoming_anns.append(deepcopy(ann))
                    as_obj.incoming_anns[prefix] = incoming_anns

    def process_incoming_anns(self, recv_relationship: Relationships):
        """Process all announcements that were incoming from a specific rel"""

        for prefix, ann_list in self.incoming_anns.items():
            # Add to the AS path of all announcements incoming
            for ann in ann_list:
                ann.as_path = (self.asn, *ann.as_path)

            # Get announcement currently in local rib
            best_ann = self.local_rib.get(prefix)
            # If there is no announcement currently in local rib,
            if best_ann is None:
                # Make the best announcement be the first one in the list
                best_ann = ann_list[0]
                # And assign the priority to it
                self._assign_priority(best_ann, recv_relationship)
                # If that was the only ann, just continue
                if len(ann_list) == 1:
                    self.local_rib[prefix] = best_ann
                    continue
            # For each announcement that was incoming
            for ann in ann_list:
                # Assign priority and relationship
                # Without assigning priority, we would have to recalculate it
                # For the best ann every time
                # Also, without priority as an int it's a bunch of if's
                self._assign_priority(ann, recv_relationship)
                # If the new announcement is better, save it
                # Don't bother tiebreaking, if priority is same, keep existing
                # Just like normal BGP
                # Tiebreaking with time and such should go into the priority
                # If we ever decide to do that
                if best_ann < ann:
                    best_ann = ann
            # Save to local rib
            self.local_rib[prefix] = best_ann
        self.incoming_anns = IncomingAnns()

    def _assign_priority(self, ann: Ann, recv_relationship: Relationships):
        """Assigns the priority to an announcement according to Gao Rexford"""

        ann.recv_relationship = recv_relationship
        # Relationship
        # Path length
        # 100 - is to invert the as_path so that longer paths are worse
        assert len(as_path) < 100
        ann.priority = recv_relationship.value * 100 + (100 - len(ann.as_path))
