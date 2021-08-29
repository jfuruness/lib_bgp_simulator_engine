from .announcement import Announcement as Ann
from .base_as import AS
from .relationships import Relationships


class BGPAS(AS):
    def propogate(self, propogate_to: Relationships):
        """Propogates announcements from local rib to other ASes

        Later you can change this so it's not the local rib that's
        being sent. But this is just proof of concept.
        """

        for asn_obj in getattr(self, propogate_to.name.lower()):
            for prefix, ann in self.local_rib.items():
                incoming_ann_list = asn_obj.incoming_anns.get(prefix, list())
                asn_obj.incomming_anns[prefix] = incoming_ann_list + [ann]

    def process_incoming_anns(self, recv_relationship: Relationships):
        """Process all announcements that were incoming from a specific rel"""

        for prefix, ann_list in self.incoming_anns:
            # Get announcement currently in local rib
            best_ann = self.local_rib[prefix]
            # If there is no announcement currently in local rib,
            if best_ann is None:
                # Make the best announcement be the first one in the list
                best_ann = ann_list[0]
                # And assign the priority to it
                self._assign_priority(best_ann, recv_relationship)
                # If that was the only ann, just continue
                if len(ann_list) == 1:
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

    def _assign_priority(self, ann: Ann, recv_relationship: Relationships):
        """Assigns the priority to an announcement according to Gao Rexford"""

        ann.recv_relationship = recv_relationship
        # Relationship
        # Path length
        ann.priority = recv_relationship.value * 100 + len(ann.as_path)
